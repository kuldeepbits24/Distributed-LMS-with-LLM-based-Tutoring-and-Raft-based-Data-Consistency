import grpc
from concurrent import futures
import lms_pb2
import lms_pb2_grpc
import logging
import threading
import time
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LMSServerFollower(lms_pb2_grpc.LMSServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.leader_id = None
        self.sessions={}
        # Use a larger random range to reduce election conflicts
        self.election_timeout = random.uniform(8, 12)  # Randomized election timeout in seconds
        self.last_heartbeat_time = time.time()

        # Start a thread to monitor heartbeats and initiate elections
        self.election_thread = threading.Thread(target=self.monitor_heartbeat)
        self.election_thread.start()

    def monitor_heartbeat(self):
        """Monitors heartbeats from the leader and initiates election if timeout occurs."""
        while True:
            time_since_last_heartbeat = time.time() - self.last_heartbeat_time
            if time_since_last_heartbeat >= self.election_timeout:
                logging.warning(f"Election timeout occurred on {self.node_id}, initiating leader election...")
                self.start_election()
            time.sleep(1)

    def Heartbeat(self, request, context):
        """Handles heartbeat requests from clients."""
        logging.info("Heartbeat received from client.")
        return lms_pb2.HeartbeatResponse(success=True)
    def start_election(self):
        """Starts a leader election process if no heartbeat is received."""
        self.term += 1
        self.voted_for = self.node_id
        votes_received = 1  # Starts with self-vote
        self.election_timeout = random.uniform(8, 12)  # Reset and randomize election timeout
        logging.info(f"{self.node_id} started an election for term {self.term}")

        # Send RequestVote to other nodes
        for follower_port in ['50051', '50053', '50054']:  # Replace with all nodes' ports
            if follower_port == self.node_id:
                continue
            try:
                with grpc.insecure_channel(f'localhost:{follower_port}') as channel:
                    stub = lms_pb2_grpc.LMSStub(channel)
                    vote_request = lms_pb2.RequestVoteRequest(
                        candidateId=self.node_id,
                        term=self.term,
                        lastLogIndex=len(self.log) - 1,
                        lastLogTerm=self.log[-1].term if self.log else 0,
                    )
                    response = stub.requestVote(vote_request)
                    if response.voteGranted:
                        votes_received += 1
                        logging.info(f"{self.node_id} received a vote from {follower_port}")
            except grpc.RpcError as e:
                logging.error(f"Failed to contact {follower_port} during election: {e}")

        # Check if the node won the election and stabilize leadership
        if votes_received > 1:  # Majority vote threshold for a 3-node system
            self.leader_id = self.node_id
            logging.info(f"{self.node_id} is now the new leader for term {self.term}")
            self.send_heartbeats_as_leader()
        else:
            logging.info(f"{self.node_id} did not receive enough votes to become the leader")

    def send_heartbeats_as_leader(self):
        """Sends heartbeats to followers to stabilize leadership after election."""
        while self.leader_id == self.node_id:
          for follower_ip in ['172.20.10.6:50053']:
             with grpc.insecure_channel(follower_ip) as channel:
              stub = lms_pb2_grpc.LMSStub(channel)
              heartbeat = lms_pb2.AppendEntriesRequest(term=self.term, leaderId=self.node_id, entries=[])
              try:
                 stub.appendEntries(heartbeat)
                 logging.info(f"Leader {self.node_id} sent heartbeat to follower {follower_ip}")
              except grpc.RpcError as e:
                  logging.error(f"Failed to send heartbeat to follower {follower_ip}: {e}")


          time.sleep(2)  # Heartbeat interval

    def requestVote(self, request, context):
        """Handles incoming RequestVote RPC calls from other nodes."""
        # If the request term is higher, update term and reset voted_for
        if request.term > self.term:
            self.term = request.term
            self.voted_for = None

        vote_granted = False
        if (self.voted_for is None or self.voted_for == request.candidateId) and request.term >= self.term:
            self.voted_for = request.candidateId
            vote_granted = True
            logging.info(f"{self.node_id} voted for {request.candidateId} in term {request.term}")

        return lms_pb2.RequestVoteResponse(term=self.term, voteGranted=vote_granted)

    def SubmitAssignment(self, request, context):
        """Handles assignment submission by students."""
        if request.token not in self.sessions:
            logging.warning("SubmitAssignment request denied: Invalid session token.")
            return lms_pb2.SubmitAssignmentResponse(success=False)

        # Process the assignment submission
        student_username = self.sessions[request.token]
        logging.info(f"Assignment submitted by {student_username}: {request.submissionContent}")

        return lms_pb2.SubmitAssignmentResponse(success=True)
       
    def GradeAssignment(self, request, context):
        """Handles grading assignments by instructors."""
        if request.token not in self.sessions:
            logging.warning("GradeAssignment request denied: Invalid session token.")
            return lms_pb2.GradeAssignmentResponse(success=False, errorMessage="Invalid session token.")

        # Check if the user is an instructor
        instructor_username = self.sessions[request.token]
        user_info = self.users[instructor_username]
        if user_info["userType"] != "Instructor":
            logging.warning(f"GradeAssignment request denied: User '{instructor_username}' is not an instructor.")
            return lms_pb2.GradeAssignmentResponse(success=False, errorMessage="User  is not authorized to grade assignments.")

        # Assign the grade
        student_username = request.studentUsername
        grade = request.grade

        # Store the grade in the grades database
        self.grades_db[student_username] = grade
        logging.info(f"Graded assignment for {student_username} with grade {grade}")

        return lms_pb2.GradeAssignmentResponse(success=True)

    def ViewGrades(self, request, context):
        """Handles viewing grades for a student."""
        if request.token not in self.sessions:
            logging.warning("ViewGrades request denied: Invalid session token.")
            return lms_pb2.ViewGradesResponse(success=False, errorMessage="Invalid session token.")

        # Retrieve the student username from the session
        student_username = self.sessions[request.token]
        
        # Check if the student has any grades
        if student_username in self.grades_db:
            grade_info = lms_pb2.GradeInfo(studentUsername=student_username, grade=self.grades_db[student_username])
            return lms_pb2.ViewGradesResponse(success=True, grades=[grade_info])
        else:
            logging.info(f"No grades found for student {student_username}.")
            return lms_pb2.ViewGradesResponse(success=False, errorMessage="No grades found for this student.")

    def PostQuery(self, request, context):
        """Handles posting a query from a student."""
        if request.token not in self.sessions:
            logging.warning("PostQuery request denied: Invalid session token.")
            return lms_pb2.PostQueryResponse(success=False, message="Invalid session token.")

        # Process the query content
        student_username = self.sessions[request.token]
        logging.info(f"Query posted by {student_username}: {request.queryContent}")

        # Store the query in the queries list
        self.queries.append(request.queryContent)

        return lms_pb2.PostQueryResponse(success=True, message="Query posted successfully.")

    def ViewAllQueries(self, request, context):
        """Handles viewing all queries posted by students."""
        if request.token not in self.sessions:
            logging.warning("ViewAllQueries request denied: Invalid session token.")
            return lms_pb2.ViewAllQueriesResponse(success=False, queries=[])

        # Check if the user is an instructor
        username = self.sessions[request.token]
        user_info = self.users[username]
        if user_info["userType"] != "Instructor":
            logging.warning(f"ViewAllQueries request denied: User '{username}' is not an instructor.")
            return lms_pb2.ViewAllQueriesResponse(success=False, queries=[])

        # Return the list of queries
        logging.info(f"Returning queries to instructor {username}.")
        return lms_pb2.ViewAllQueriesResponse(success=True, queries=self.queries)


    def appendEntries(self, request, context):
     if request.term >= self.term:
        self.term = request.term
        self.leader_id = request.leaderId
        self.last_heartbeat_time = time.time()
        
        # Replicate log entries
        for entry in request.entries:
            self.log.append(LogEntry(term=entry.term, command=entry.command))
        
        logging.info(f"Log entries replicated from leader {self.leader_id} on follower {self.node_id}")
        return lms_pb2.AppendEntriesResponse(success=True)
    
     return lms_pb2.AppendEntriesResponse(success=False)

    # LMS functionalities
    def Login(self, request, context):
        return lms_pb2.LoginResponse(success=True, token=f"token-{request.username}")

    def Logout(self, request, context):
        return lms_pb2.LogoutResponse(success=True)

    def Post(self, request, context):
    # Create a log entry
     entry = LogEntry(term=self.term, command=request.command)
     self.log.append(entry)
    
    # Process the command as needed
     return lms_pb2.PostResponse(success=True)
     
  
    def Get(self, request, context):
        data = [entry.command for entry in self.log]
        return lms_pb2.GetResponse(success=True, data=data)
    
    class LogEntry:
     def __init__(self, term, command):
        self.term = term
        self.command = command

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lms_pb2_grpc.add_LMSServicer_to_server(LMSServerFollower('node_4'), server)
    server.add_insecure_port('172.20.10.7:50054')  # Updated IP address for Node 4
    logging.info("Raft Follower (Node 4) running on IP 172.20.10.7, port 50054")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
