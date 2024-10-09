'''
This file contains the backend code for the VolunteerMatch web application.
It handles routing for the login page, volunteer dashboard, and opportunity details page.
'''
from flask import Flask, render_template, redirect, url_for, request
import os
app = Flask(__name__)
# Create data directory and necessary text files if they do not exist
if not os.path.exists('data'):
    os.makedirs('data')
# Create users.txt with initial data if it does not exist
if not os.path.isfile('data/users.txt'):
    with open('data/users.txt', 'w') as file:
        file.write("username1,password1\n")
        file.write("username2,password2\n")
# Create opportunities.txt with initial data if it does not exist
if not os.path.isfile('data/opportunities.txt'):
    with open('data/opportunities.txt', 'w') as file:
        file.write("1,Opportunity Title 1,Description of opportunity 1\n")
        file.write("2,Opportunity Title 2,Description of opportunity 2\n")
# Create applications.txt if it does not exist
if not os.path.isfile('data/applications.txt'):
    with open('data/applications.txt', 'w') as file:
        file.write("")  # Create an empty file
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    # Validate user credentials against the data/users.txt file
    try:
        with open('data/users.txt', 'r') as file:
            lines = file.readlines()
            if not lines:  # Check if the file is empty
                return render_template('login.html', error_message="No users found. Please register.")
            for line in lines:
                stored_username, stored_password = line.strip().split(',')
                if stored_username == username and stored_password == password:
                    return redirect(url_for('dashboard'))
    except FileNotFoundError:
        return render_template('login.html', error_message="User credentials file not found. Please contact support.")
    except ValueError:
        return render_template('login.html', error_message="Invalid user data format.")
    # If credentials are invalid, redirect back to login with an error message
    return render_template('login.html', error_message="Invalid username or password.")
@app.route('/dashboard')
def dashboard():
    opportunities = []
    # Read volunteer opportunities from the data file
    try:
        with open('data/opportunities.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    opportunity_id, opportunity_title, opportunity_desc = parts
                    opportunities.append({
                        'id': int(opportunity_id),
                        'title': opportunity_title,
                        'description': opportunity_desc
                    })
    except FileNotFoundError:
        print("Opportunities file not found.")
    return render_template('dashboard.html', opportunities=opportunities)
@app.route('/opportunity/<int:opportunity_id>')
def opportunity_details(opportunity_id):
    opportunity = None
    # Read the opportunity details from the data file
    try:
        with open('data/opportunities.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3 and int(parts[0]) == opportunity_id:
                    opportunity = {
                        'id': int(parts[0]),
                        'title': parts[1],
                        'description': parts[2]
                    }
                    break
    except FileNotFoundError:
        print("Opportunities file not found.")
    if opportunity is None:
        return "Opportunity not found", 404  # Handle case where opportunity is not found
    return render_template('opportunity_details.html', opportunity=opportunity)
@app.route('/submit_application/<int:opportunity_id>', methods=['POST'])
def submit_application(opportunity_id):
    applicant_name = request.form['applicant_name']
    applicant_email = request.form['applicant_email']
    # Save the application data to the file
    with open('data/applications.txt', 'a') as file:
        file.write(f"{applicant_name},{applicant_email},{opportunity_id}\n")
    return redirect(url_for('dashboard'))  # Redirect to dashboard after submission
if __name__ == '__main__':
    app.run(port=5000)