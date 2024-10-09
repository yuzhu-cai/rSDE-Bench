'''
This is the main application file for the VirtualWellnessRetreats web application.
It handles routing for all frontend pages, manages user authentication, and retreat scheduling.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
RETREATS_FILE = os.path.join(DATA_DIR, 'retreats.txt')
def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                username, password = line.strip().split(':')
                users[username] = password
    return users
def write_user(username, password):
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}:{password}\n")
def read_retreats():
    retreats = []
    if os.path.exists(RETREATS_FILE):
        with open(RETREATS_FILE, 'r') as f:
            for line in f:
                retreats.append(line.strip().split('|'))
    return retreats
def write_retreat(retreat_id, username, title, date, time, instructor):
    with open(RETREATS_FILE, 'a') as f:
        f.write(f"{retreat_id}|{username}|{title}|{date}|{time}|{instructor}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['register_username_field']
        password = request.form['register_password_field']
        confirm_password = request.form['confirm_password_field']
        if password == confirm_password:
            users = read_users()
            if username not in users:
                write_user(username, password)
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists. Please choose another one.', 'error')
        else:
            flash('Passwords do not match. Please try again.', 'error')
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/schedule_retreat', methods=['GET', 'POST'])
def schedule_retreat():
    if request.method == 'POST':
        retreat_id = len(read_retreats()) + 1
        username = session.get('username')  # Retrieve username from session
        title = request.form['retreat_title_field']
        date = request.form['retreat_date_field']
        time = request.form['retreat_time_field']
        instructor = request.form['retreat_instructor_field']
        write_retreat(retreat_id, username, title, date, time, instructor)
        flash('Retreat scheduled successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('schedule_retreat.html')
@app.route('/view_bookings')
def view_bookings():
    username = session.get('username')  # Retrieve username from session
    if not username:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))
    retreats = read_retreats()
    user_retreats = [r for r in retreats if r[1] == username]
    return render_template('view_bookings.html', user_retreats=user_retreats)
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)