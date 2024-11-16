import grpc
import lms_pb2
import lms_pb2_grpc
import tutoring_pb2
import tutoring_pb2_grpc
import sys

session_token = None  
user_type = None  
nodes = [
    '172.20.10.5:50051',  # Node 2 (Leader)
    '172.20.10.6:50053',  # Node 3 (Follower)
    '172.20.10.8:50054'   # Node 4 (Follower)
]

TUTORING_SERVER_ADDRESS = '172.20.10.5:50052'


def connect_to_lms():
    for node in nodes:
        try:
            # Connect to the node and check if it is responsive
            channel = grpc.insecure_channel(node)
            stub = lms_pb2_grpc.LMSStub(channel)
            # Sending a heartbeat request to check if the node is available
            response = stub.Heartbeat(lms_pb2.HeartbeatRequest())
            if response.success:
                print(f"Connected to LMS at {node}")
                return stub
        except grpc.RpcError as e:
            print(f" ")
    print("Could not connect to any LMS node.")
    return None

# Function to connect to the tutoring server
def connect_to_tutoring_server():
    try:
        channel = grpc.insecure_channel(TUTORING_SERVER_ADDRESS)
        stub = tutoring_pb2_grpc.TutoringStub(channel)
        print("Connected to Tutoring Server.")
        return stub
    except Exception as e:
        print(" ", e)
        sys.exit(1)

def ask_question():
    if not session_token or user_type != "Student":
        print("Only students can ask questions.")
        return
    stub = connect_to_tutoring_server()  
    if stub:
        question = input("Enter your question: ")
        response = stub.GetLLMAnswer(tutoring_pb2.GetLLMAnswerRequest(query=question))
        if response.success:
            print("LLM Answer:", response.answer)
        else:
            print("Failed to get answer from LLM")



def login():
    global session_token, user_type
    stub = connect_to_lms()
    if stub:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        response = stub.Login(lms_pb2.LoginRequest(username=username, password=password))
        if response.success:
            session_token = response.token
            user_type = response.userType
            print(f"Login successful as {user_type}")
        else:
            print("Login failed")

def register():
    stub = connect_to_lms()
    if stub:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user_type = input("Enter user type (Instructor/Student): ")
        response = stub.Register(lms_pb2.RegisterRequest(username=username, password=password, userType=user_type))
        if response.success:
            print("Registration successful")
        else:
            print("Registration failed")

def logout():
    global session_token, user_type
    stub = connect_to_lms()
    if stub and session_token:
        response = stub.Logout(lms_pb2.LogoutRequest(token=session_token))
        if response.success:
            print("Logged out successfully")
            session_token = None
            user_type = None  # Reset user type on logout
        else:
            print("Logout failed")

# Instructor-only functionalities
def post_assignment():
    if not session_token or user_type != "Instructor":
        print("Only instructors can post assignments.")
        return
    stub = connect_to_lms()
    if stub:
        assignment = input("Enter the assignment content: ")
        response = stub.PostAssignment(lms_pb2.PostAssignmentRequest(token=session_token, assignmentContent=assignment))
        if response.success:
            print("Assignment posted successfully")
        else:
            print("Failed to post assignment")

def view_all_queries():
    if not session_token or user_type != "Instructor":
        print("Only instructors can view all queries.")
        return
    stub = connect_to_lms()
    if stub:
        response = stub.ViewAllQueries(lms_pb2.ViewAllQueriesRequest(token=session_token))
        if response.success:
            print("All Student Queries:")
            for query in response.queries:
                print(f"- {query}")
        else:
            print("Failed to retrieve queries")

def grade_assignment():
    if not session_token or user_type != "Instructor":
        print("Only instructors can grade assignments.")
        return
    stub = connect_to_lms()
    if stub:
        try:
            student_username = input("Enter the student's username: ")
            grade = input("Enter the grade: ")
            response = stub.GradeAssignment(
                lms_pb2.GradeAssignmentRequest(
                    token=session_token,
                    studentUsername=student_username,
                    grade=grade
                )
            )
            if response.success:
                print("Grade assigned successfully")
            else:
                print(f"Failed to assign grade: {response.errorMessage}")
        except grpc.RpcError as e:
            print(f"gRPC error occurred: {e.code()} - {e.details()}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

# Student-only functionalities
def submit_assignment():
    print(f"Session Token: {session_token}, User Type: {user_type}")  # Debugging line
    if not session_token or user_type != "Student":
        print("Only students can submit assignments.")
        return
    stub = connect_to_lms()
    if stub:
        
        submission = input("Enter your assignment submission: ")
        response = stub.SubmitAssignment(lms_pb2.SubmitAssignmentRequest(token=session_token, submissionContent=submission))
        if response.success:
            print("Assignment submitted successfully")
        else:
            print("Failed to submit assignment")
    
def view_grades():
    if not session_token or user_type != "Student":
        print("Only students can view grades.")
        return
    stub = connect_to_lms()
    if stub:
        response = stub.ViewGrades(lms_pb2.ViewGradesRequest(token=session_token))
        if response.success:
            print("Your Grades:")
            for grade in response.grades:
                print(f"- {grade}")  # Ensure this line is properly indented
        else:
            print("Grades are not GIVEN yet...")

def post_query():
    if not session_token or user_type != "Student":
        print("Only students can post queries.")
        return
    stub = connect_to_lms()
    if stub:
        query_content = input("Enter your query: ")
        response = stub.PostQuery(tutoring_pb2.PostQueryRequest(token=session_token, queryContent=query_content))
        if response.success:
            print("Query posted successfully")
        else:
            print("Failed to post query")

def main_menu():
    while True:
        if session_token:
            print("\nMain Menu:")
            if user_type == "Instructor":
                print("1. Post Assignment")
                print("2. View All Queries")
                print("3. Grade Assignment")
                print("4. Logout")
            elif user_type == "Student":
                print("1. Submit Assignment")
                print("2. View Grades")
                print("3. Post Query")
                print("4. Ask Question to LLM")
                print("5. Logout")
        else:
            print("\nMain Menu:")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            if user_type == "Instructor":
                post_assignment()
            elif user_type == "Student":
                submit_assignment()
            else:
                login()
        elif choice == "2":
            if user_type == "Instructor":
                view_all_queries()
            elif user_type == "Student":
                view_grades()
            else:
                register()
        elif choice == "3":
            if user_type == "Instructor":
                grade_assignment()
            elif user_type == "Student":
                post_query()
        elif choice == "4":
            if user_type == "Student":
                ask_question()
        elif choice == "5":
            logout()
        elif choice == "4" and not session_token:
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()