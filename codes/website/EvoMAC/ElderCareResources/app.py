'''
This file implements the backend for the ElderCareResources web application.
It handles user authentication, routing for all frontend pages, and file operations
for user data and inquiries. The application runs on local port 5000.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
# Define the data directory
DATA_DIR = 'data'
# Function to read user data from the file
def read_users():
    users = {}
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            users[username] = password
    return users
# Function to read resources from the file
def read_resources():
    resources = []
    with open(os.path.join(DATA_DIR, 'resources.txt'), 'r') as file:
        for line in file:
            resource_id, title, description = line.strip().split(',')
            resources.append({'resource_id': resource_id, 'title': title, 'description': description})
    return resources
# Function to write contact inquiries to the file
def write_inquiry(name, email, message):
    with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'a') as file:
        file.write(f"{name},{email},{message}\n")
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', resources=read_resources())
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username
            return render_template('dashboard.html', resources=read_resources())
        else:
            return "Invalid credentials", 401
    return redirect(url_for('login'))
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['contact-name']
        email = request.form['contact-email']
        message = request.form['contact-message']
        write_inquiry(name, email, message)
        return redirect(url_for('login'))
    return render_template('contact.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)