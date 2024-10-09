'''
This is the main backend application for the Health Consultation Platform.
It handles routing for all frontend pages, user authentication, consultation scheduling,
and feedback submission while managing data storage in plain text files.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data/'
# Helper functions for file operations
def read_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
    except FileNotFoundError:
        return users
    return users
def write_user(username, password):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'a') as file:
        file.write(f"{username},{password}\n")
def read_consultations():
    consultations = []
    try:
        with open(os.path.join(DATA_DIR, 'consultations.txt'), 'r') as file:
            for line in file:
                consultations.append(line.strip().split(','))
    except FileNotFoundError:
        return consultations
    return consultations
def write_consultation(username, date, time):
    with open(os.path.join(DATA_DIR, 'consultations.txt'), 'a') as file:
        file.write(f"{username},{date},{time}\n")
def write_feedback(username, feedback):
    with open(os.path.join(DATA_DIR, 'feedback.txt'), 'a') as file:
        file.write(f"{username},{feedback}\n")
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = read_users()
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('schedule_consultation'))
    else:
        flash('Invalid username or password.')
        return render_template('login.html', error_message='Invalid username or password.')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['reg_username_input']
        password = request.form['reg_password_input']
        email = request.form['reg_email_input']
        write_user(username, password)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('registration.html', registration_success_message='Registration successful! Please log in.')
@app.route('/schedule_consultation', methods=['GET', 'POST'])
def schedule_consultation():
    if request.method == 'POST':
        username = session.get('username')
        date = request.form['date_field']
        time = request.form['time_slot_field']
        if username and date and time:  # Ensure all data is present
            write_consultation(username, date, time)
            flash('Consultation scheduled successfully!')
            return redirect(url_for('my_appointments'))
        else:
            flash('Please fill in all fields.')
    return render_template('schedule_consultation.html')
@app.route('/my_appointments')
def my_appointments():
    username = session.get('username')
    consultations = read_consultations()
    user_appointments = [c for c in consultations if c[0] == username]
    return render_template('my_appointments.html', appointments=user_appointments)
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        flash('You must be logged in to leave feedback.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = session.get('username')
        feedback_text = request.form['feedback_textarea']
        write_feedback(username, feedback_text)
        flash('Feedback submitted successfully!')
        return redirect(url_for('my_appointments'))
    return render_template('feedback.html')
if __name__ == '__main__':
    app.run(port=5000)