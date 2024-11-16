import tkinter as tk
from tkinter import messagebox, simpledialog
import grpc
import lms_pb2
import lms_pb2_grpc
import tutoring_pb2
import tutoring_pb2_grpc

# Global variables
session_token = None
user_type = None
nodes = ['172.20.10.5:50051', '172.20.10.6:50053', '172.20.10.8:50054']
TUTORING_SERVER_ADDRESS = '172.20.10.5:50052'

# Function to connect to LMS
def connect_to_lms():
    for node in nodes:
        try:
            channel = grpc.insecure_channel(node)
            stub = lms_pb2_grpc.LMSStub(channel)
            response = stub.Heartbeat(lms_pb2.HeartbeatRequest())
            if response.success:
                return stub
        except grpc.RpcError:
            continue
    messagebox.showerror("Error", "Could not connect to any LMS node.")
    return None

# Function to connect to tutoring server
def connect_to_tutoring_server():
    try:
        channel = grpc.insecure_channel(TUTORING_SERVER_ADDRESS)
        return tutoring_pb2_grpc.TutoringStub(channel)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to Tutoring Server: {e}")
        return None

# Function to refresh the menu based on user type
def refresh_menu():
    clear_window()
    if session_token:
        if user_type == "Student":
            show_student_menu()
        elif user_type == "Instructor":
            show_instructor_menu()
    else:
        show_home_menu()

# Function to clear the window
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# Home Menu
def show_home_menu():
    clear_window()
    tk.Label(window, text="WELCOME TO BITS PILANI LMS PORTAL", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(window, text="Login", command=login, width=20).pack(pady=10)
    tk.Button(window, text="Register", command=register, width=20).pack(pady=10)
    tk.Button(window, text="Exit", command=window.quit, width=20).pack(pady=10)

# Student Menu
def show_student_menu():
    clear_window()
    tk.Label(window, text="Student Dashboard", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(window, text="Submit Assignment", command=submit_assignment, width=30).pack(pady=10)
    tk.Button(window, text="View Grades", command=view_grades, width=30).pack(pady=10)
    tk.Button(window, text="Post Query", command=post_query, width=30).pack(pady=10)
    tk.Button(window, text="Ask Question to LLM", command=ask_question, width=30).pack(pady=10)
    tk.Button(window, text="Logout", command=logout, width=30).pack(pady=10)

# Instructor Menu
def show_instructor_menu():
    clear_window()
    tk.Label(window, text="Instructor Dashboard", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(window, text="Post Assignment", command=post_assignment, width=30).pack(pady=10)
    tk.Button(window, text="View All Queries", command=view_all_queries, width=30).pack(pady=10)
    tk.Button(window, text="Grade Assignment", command=grade_assignment, width=30).pack(pady=10)
    tk.Button(window, text="Logout", command=logout, width=30).pack(pady=10)

# Function to handle login
def login():
    global session_token, user_type
    stub = connect_to_lms()
    if stub:
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:", show='*')
        response = stub.Login(lms_pb2.LoginRequest(username=username, password=password))
        if response.success:
            session_token = response.token
            user_type = response.userType
            messagebox.showinfo("Success", f"Logged in as {user_type}")
            refresh_menu()
        else:
            messagebox.showerror("Error", "Login failed")

def register():
    stub = connect_to_lms()
    if stub:
        username = simpledialog.askstring("Register", "Enter your username:")
        password = simpledialog.askstring("Register", "Enter your password:", show='*')
        user_type = simpledialog.askstring("Register", "Enter user type (Instructor/Student):")
        response = stub.Register(lms_pb2.RegisterRequest(username=username, password=password, userType=user_type))
        if response.success:
            messagebox.showinfo("Success", "Registration successful")
        else:
            messagebox.showerror("Error", "Registration failed")

# Student functionalities
def ask_question():
    if user_type != "Student":
        return
    stub = connect_to_tutoring_server()
    if stub:
        question = simpledialog.askstring("Ask Question", "Enter your question:")
        response = stub.GetLLMAnswer(tutoring_pb2.GetLLMAnswerRequest(query=question))
        if response.success:
            messagebox.showinfo("LLM Answer", response.answer)
        else:
            messagebox.showerror("Error", "Failed to get an answer")

def post_query():
    stub = connect_to_lms()
    if stub:
        query = simpledialog.askstring("Post Query", "Enter your query:")
        response = stub.PostQuery(lms_pb2.PostQueryRequest(token=session_token, queryContent=query))
        if response.success:
            messagebox.showinfo("Success", "Query posted")

def submit_assignment():
    stub = connect_to_lms()
    if stub:
        assignment = simpledialog.askstring("Submit Assignment", "Enter your assignment:")
        response = stub.SubmitAssignment(lms_pb2.SubmitAssignmentRequest(token=session_token, submissionContent=assignment))
        if response.success:
            messagebox.showinfo("Success", "Assignment submitted")

def view_grades():
    stub = connect_to_lms()
    if stub:
        response = stub.ViewGrades(lms_pb2.ViewGradesRequest(token=session_token))
        if response.success:
            grades = "\n".join([f"{grade.studentUsername}: {grade.grade}" for grade in response.grades])
            messagebox.showinfo("Grades", grades)

# Instructor functionalities
def post_assignment():
    stub = connect_to_lms()
    if stub:
        assignment = simpledialog.askstring("Post Assignment", "Enter assignment content:")
        response = stub.PostAssignment(lms_pb2.PostAssignmentRequest(token=session_token, assignmentContent=assignment))
        if response.success:
            messagebox.showinfo("Success", "Assignment posted")

def view_all_queries():
    stub = connect_to_lms()
    if stub:
        response = stub.ViewAllQueries(lms_pb2.ViewAllQueriesRequest(token=session_token))
        queries = "\n".join(response.queries)
        messagebox.showinfo("All Queries", queries)

def grade_assignment():
    stub = connect_to_lms()
    if stub:
        student = simpledialog.askstring("Grade Assignment", "Student username:")
        grade = simpledialog.askstring("Grade Assignment", "Enter grade:")
        response = stub.GradeAssignment(lms_pb2.GradeAssignmentRequest(token=session_token, studentUsername=student, grade=grade))
        if response.success:
            messagebox.showinfo("Success", "Grade assigned")
        else:
            messagebox.showerror("Error", "Failed to assign grade")

def logout():
    global session_token, user_type
    session_token = None
    user_type = None
    refresh_menu()

# Main GUI Window
window = tk.Tk()
window.title("WELCOME TO BITS LMS PORTAL")
window.geometry("400x500")
show_home_menu()
window.mainloop()
