import grpc
from concurrent import futures
import lms_pb2
import lms_pb2_grpc
import logging
import threading
import time

# Configure logging for detailed Raft operations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LMSServerLeader(lms_pb2_grpc.LMSServicer):
    def __init__(self, node_id, followers):
        self.node_id = node_id
        self.term = 1
        self.log = []
        self.commit_index = 0
        self.followers = followers
        self.sessions = {}
        self.users = { 
            "student1": {"password": "password123", "userType": "Student"},
            "instructor1": {"password": "password456", "userType": "Instructor"}
        }  # Dictionary to store registered users
        self.heartbeat_interval = 2  # Heartbeat interval in seconds
        self.grades_db = {}  # Dictionary to store grades
        self.queries = []  # List to store posted queries

        # Start sending heartbeats to followers
        self.heartbeat_thread = threading.Thread(target=self.send_heartbeats)
        self.heartbeat_thread.start()
        
    def send_heartbeats(self):
        """Sends periodic heartbeats to followers to maintain leadership."""
        while True:
            for follower in self.followers:
                with grpc.insecure_channel(follower) as channel:
                    stub = lms_pb2_grpc.LMSStub(channel)
                    heartbeat = lms_pb2.AppendEntriesRequest(term=self.term, leaderId=self.node_id, entries=[])
                    try:
                        stub.appendEntries(heartbeat)
                        logging.info(f"Sent heartbeat to follower {follower}")
                    except grpc.RpcError as e:
                        logging.error(f"Failed to send heartbeat to follower {follower}: {e}")
            time.sleep(self.heartbeat_interval)

    def Register(self, request, context):
        """Handles user registration."""
        # Check if the username already exists
        if request.username in self.users:
            logging.warning(f"Registration failed: Username '{request.username}' already exists.")
            return lms_pb2.RegisterResponse(success=False, message="Username already exists.")
        
        # Register the new user with both password and userType
        self.users[request.username] = {"password": request.password, "userType": request.userType}
        logging.info(f"User   '{request.username}' registered successfully.")
        return lms_pb2.RegisterResponse(success=True, message="Registration successful.")

    def send_heartbeats(self):
   #  """Sends periodic heartbeats to followers to maintain leadership."""
     while True:
      for follower in self.followers:
            with grpc.insecure_channel(follower) as channel:
                stub = lms_pb2_grpc.LMSStub(channel)
                heartbeat = lms_pb2.AppendEntriesRequest(term=self.term, leaderId=self.node_id, entries=[])
                try:
                    stub.appendEntries(heartbeat)
                    logging.info(f"Sent heartbeat to follower {follower}")
                except grpc.RpcError as e:
                    logging.error(f"Failed to send heartbeat to follower {follower}: {e}")
      time.sleep(self.heartbeat_interval)

     
    def Heartbeat(self, request, context):
        """Handles heartbeat requests from clients."""
        logging.info("Heartbeat received from client.")
        return lms_pb2.HeartbeatResponse(success=True) 
    
    def Login(self, request, context):
        """Handles user login."""
        # Check if the username exists in the users dictionary
        if request.username in self.users:
            user_info = self.users[request.username]  # Access user dictionary
            if user_info["password"] == request.password:  # Check password
                user_type = user_info["userType"]
                token = f"token-{request.username}"
                self.sessions[token] = request.username
                return lms_pb2.LoginResponse(success=True, token=token, userType=user_type)
        
        # Return unsuccessful response if login fails
        return lms_pb2.LoginResponse(success=False, token="", userType="")

    def Logout(self, request, context):
        """Handles user logout."""
        if request.token in self.sessions:
            del self.sessions[request.token]
            logging.info(f"User   logged out with token {request.token}")
            return lms_pb2.LogoutResponse(success=True)
        logging.warning(f"Logout failed: Invalid token {request.token}")
        return lms_pb2.LogoutResponse(success=False)

    def Post(self, request, context):
        """Handles posting data to the server."""
        if request.token not in self.sessions:
            logging.warning("Post request denied: Invalid session token.")
            return lms_pb2.PostResponse(success=False)
        self.log.append((self.term, request.data))
        self.commit_index += 1
        logging.info(f"Appended log entry for term {self.term} with data '{request.data}'")
        self.replicate_log()
        return lms_pb2.PostResponse(success=True)
     
    def Get(self, request, context):
        """Retrieves data from the log."""
        data = [entry for term, entry in self.log]
        logging.info(f"Retrieved content from logs: {data}")
        return lms_pb2.GetResponse(success=True, data=data)

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

    def replicate_log(self):
        """Replicates log entries to all followers."""
        for follower in self.followers:
            with grpc.insecure_channel(follower) as channel:
                stub = lms_pb2_grpc.LMSStub(channel)
                for term, command in self.log:
                    entry = lms_pb2.LogEntry(term=term, command=command)
                    request = lms_pb2.AppendEntriesRequest(term=self.term, leaderId=self.node_id, entries=[entry])
                    try:
                        response = stub.appendEntries(request)
                        if response.success:
                            logging.info(f"Replicated log entry '{command}' to follower {follower}")
                        else:
                            logging.warning(f"Follower {follower} rejected log entry '{command}'")
                    except grpc.RpcError as e:
                        logging.error(f"Failed to replicate log to follower {follower}: {e}")

def serve():
    followers = ['172.20.10.6:50053', '172.20.10.8:50054']
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lms_pb2_grpc.add_LMSServicer_to_server(LMSServerLeader('node_2', followers), server)
    server.add_insecure_port('172.20.10.5:50051')  # Updated IP address for Node 2
    logging.info("Raft Leader (Node 2) running on IP 172.20.10.5, port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()