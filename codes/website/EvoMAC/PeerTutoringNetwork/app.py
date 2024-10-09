'''
This file implements the backend code for the PeerTutoringNetwork web application.
It handles routing for all frontend pages and manages file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
# Define the data directory
DATA_DIR = 'data'
# Function to read users from the file
def read_users():
    users = []
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as file:
        for line in file:
            users.append(line.strip().split(':'))
    return users
# Function to write a new user to the file
def write_user(username, password, email):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'a') as file:
        file.write(f"{username}:{password}:{email}\n")
# Function to read tutors from the file
def read_tutors():
    tutors = []
    with open(os.path.join(DATA_DIR, 'tutors.txt'), 'r') as file:
        for line in file:
            tutors.append(line.strip().split(':'))
    return tutors
# Function to read tutoring requests from the file
def read_requests():
    requests = []
    with open(os.path.join(DATA_DIR, 'requests.txt'), 'r') as file:
        for line in file:
            requests.append(line.strip().split(':'))
    return requests
# Function to write a tutoring request to the file
def write_request(username, subject, details, date):
    with open(os.path.join(DATA_DIR, 'requests.txt'), 'a') as file:
        file.write(f"{username}:{subject}:{details}:{date}\n")
# Function to write a contact message to the file
def write_contact(name, email, message):
    with open(os.path.join(DATA_DIR, 'contacts.txt'), 'a') as file:
        file.write(f"{name}:{email}:{message}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['txt_username']
        password = request.form['txt_password']
        users = read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('dashboard'))  # Redirect to dashboard on successful login
        return "Invalid credentials, please try again."  # Handle invalid login
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['txt_new_username']
        password = request.form['txt_new_password']
        email = request.form['txt_email']
        write_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/tutors')
def tutors():
    tutor_list = read_tutors()
    return render_template('tutors.html', tutors=tutor_list)
@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if request.method == 'POST':
        username = session.get('username')  # Retrieve username from session
        subject = request.form['txt_subject']
        details = request.form['txt_details']
        date = request.form['txt_date']
        write_request(username, subject, details, date)
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')
@app.route('/profile')
def profile():
    username = session.get('username')  # Retrieve username from session
    users = read_users()
    user_info = next((user for user in users if user[0] == username), None)
    if user_info:
        return render_template('profile.html', username=user_info[0], email=user_info[2])
    return redirect(url_for('login'))  # Redirect to login if user not found
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['txt_contact_name']
        email = request.form['txt_contact_email']
        message = request.form['txt_contact_message']
        write_contact(name, email, message)
        return redirect(url_for('dashboard'))
    return render_template('contact_us.html')
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))  # Redirect to login page
if __name__ == '__main__':
    app.run(port=5000)