'''
This is the main backend application for the PeerTutoringNetwork web application.
It implements routing for all frontend pages and handles file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
# Helper functions to read and write data
def read_users():
    with open('data/users.txt', 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]
def write_user(username, password, email):
    with open('data/users.txt', 'a') as file:
        file.write(f"{username}:{password}:{email}\n")
def read_tutors():
    with open('data/tutors.txt', 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]
def read_requests():
    with open('data/requests.txt', 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]
def write_request(username, subject, details, date):
    with open('data/requests.txt', 'a') as file:
        file.write(f"{username}:{subject}:{details}:{date}\n")
def write_contact(name, email, message):
    with open('data/contacts.txt', 'a') as file:
        file.write(f"{name}:{email}:{message}\n")
# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('dashboard'))  # Redirect to dashboard if credentials are valid
        flash('Invalid username or password. Please try again.')  # Show error message if invalid
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        email = request.form['email']
        # Check for existing username
        users = read_users()
        if any(user[0] == new_username for user in users):
            flash('Username already exists. Please choose a different username.')  # Show error message
            return redirect(url_for('register'))  # Redirect back to registration
        write_user(new_username, new_password, email)  # Save the new user data
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/tutors')
def tutors():
    return render_template('tutors.html', tutors=read_tutors())
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
    email = next((user[2] for user in users if user[0] == username), None)
    return render_template('profile.html', username=username, email=email)
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['txt_contact_name']
        email = request.form['txt_contact_email']
        message = request.form['txt_contact_message']
        write_contact(name, email, message)
        return redirect(url_for('dashboard'))
    return render_template('contact_us.html')
if __name__ == '__main__':
    app.run(port=5000)