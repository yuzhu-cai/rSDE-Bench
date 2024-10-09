'''
This file contains the backend code for the Music_Collaborator web application.
It implements routing for all frontend pages and handles file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# Route for the login page
@app.route('/')
def login():
    return render_template('login.html')
# Route for handling login
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    with open('data/users.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split('|')
            if stored_username == username and stored_password == password:
                return redirect(url_for('dashboard'))
    return redirect(url_for('login'))  # Redirect back to login if authentication fails
# Route for the registration page
@app.route('/register')
def register():
    return render_template('register.html')
# Route for handling registration
@app.route('/register', methods=['POST'])
def handle_registration():
    username = request.form['username']
    password = request.form['password']
    with open('data/users.txt', 'a') as file:
        file.write(f"{username}|{password}\n")
    return redirect(url_for('login'))  # Redirect to login after registration
# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
# Route for the create project page
@app.route('/create_project')
def create_project():
    return render_template('create_project.html')
# Route for the project details page
@app.route('/project_details')
def project_details():
    return render_template('project_details.html')
# Route for the profile settings page
@app.route('/profile_settings')
def profile_settings():
    return render_template('profile_settings.html')
# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(port=5000)