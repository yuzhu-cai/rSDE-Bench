'''
This is the main backend application for the FreelancerMarketplace web application.
It handles routing for all frontend pages and manages file read/write operations for user, freelancer, and project data.
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement login logic here
        return redirect(url_for('home'))
    return render_template('login.html')
# Route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement registration logic here
        return redirect(url_for('login'))
    return render_template('register.html')
# Route for the home page
@app.route('/home')
def home():
    return render_template('home.html')
# Route for the freelancer profile page
@app.route('/freelancer_profile')
def freelancer_profile():
    return render_template('freelancer_profile.html')
# Route for the projects page
@app.route('/projects')
def projects():
    return render_template('projects.html')
# Route for the profile management page
@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')
# Function to read user data from the file
def read_users():
    with open('data/users.txt', 'r') as file:
        users = file.readlines()
    return [user.strip().split(',') for user in users]
# Function to write user data to the file
def write_user(username, password):
    with open('data/users.txt', 'a') as file:
        file.write(f"{username},{password}\n")
# Function to read freelancer data from the file
def read_freelancers():
    with open('data/freelancers.txt', 'r') as file:
        freelancers = file.readlines()
    return [freelancer.strip().split(',') for freelancer in freelancers]
# Function to write freelancer data to the file
def write_freelancer(name, contact_info, portfolio_links):
    with open('data/freelancers.txt', 'a') as file:
        file.write(f"{name},{contact_info},{portfolio_links}\n")
# Function to read project data from the file
def read_projects():
    with open('data/projects.txt', 'r') as file:
        projects = file.readlines()
    return [project.strip().split(',') for project in projects]
# Function to write project data to the file
def write_project(project_name, description, freelancer_id):
    with open('data/projects.txt', 'a') as file:
        file.write(f"{project_name},{description},{freelancer_id}\n")
if __name__ == '__main__':
    app.run(port=5000)