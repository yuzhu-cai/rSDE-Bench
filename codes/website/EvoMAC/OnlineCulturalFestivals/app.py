'''
This file implements the backend routing for the Online Cultural Festivals web application.
It handles user login, festival overview, festival details, and user submissions.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
import re
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use a default for development
# Route for the login page
@app.route('/')
def login():
    return render_template('login.html', error=request.args.get('error'))
# Route for handling login logic
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    # Check credentials against user_data.txt
    with open('data/user_data.txt', 'r') as f:
        for line in f:
            stored_username, stored_password = line.strip().split(',')
            if stored_username == username and stored_password == password:
                session['username'] = username  # Set session variable
                return redirect(url_for('festival_overview'))
    # If login fails, return to login page with error message
    return render_template('login.html', error="Invalid username or password.")
# Route for the festival overview page
@app.route('/festivals')
def festival_overview():
    festivals = []
    with open('data/festival_data.txt', 'r') as f:
        for line in f:
            festivals.append(line.strip().split(';')[0])  # Get festival names
    return render_template('festival_overview.html', festivals=festivals)
# Route for the festival details page
@app.route('/festival/<festival_name>')
def festival_details(festival_name):
    festival_info = {}
    comments = []
    with open('data/festival_data.txt', 'r') as f:
        for line in f:
            details = line.strip().split(';')
            if details[0] == festival_name:
                festival_info = {
                    'title': details[0],
                    'description': details[1],
                    'date': details[2],
                    'category': details[3],
                    'performers': details[4]
                }
                break
    with open('data/comments.txt', 'r') as f:
        for line in f:
            comment_details = line.strip().split(';')
            if comment_details[0] == festival_name:
                comments.append(comment_details)
    return render_template('festival_details.html', festival=festival_info, comments=comments)
# Route for the user submissions page
@app.route('/submit_experience', methods=['GET', 'POST'])
def submit_experience():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login', error="You must be logged in to submit your experience."))
    if request.method == 'POST':
        user_name = request.form['user-name']
        experience_description = request.form['experience-description']
        # Input validation
        if not user_name or not experience_description:
            return render_template('user_submission.html', success_message="Please fill in all fields.")
        if not re.match("^[A-Za-z0-9_ ]*$", user_name):  # Allow only alphanumeric characters and underscores
            return render_template('user_submission.html', success_message="Invalid username format.")
        with open('data/user_experiences.txt', 'a') as f:
            f.write(f"{user_name};{experience_description}\n")
        return render_template('user_submission.html', success_message="Experience submitted successfully!")
    return render_template('user_submission.html')
# Route for submitting comments
@app.route('/festival/<festival_name>/comment', methods=['POST'])
def submit_comment(festival_name):
    comment_name = request.form['comment-name']
    comment_input = request.form['comment-input']
    with open('data/comments.txt', 'a') as f:
        f.write(f"{festival_name};{comment_name};{comment_input}\n")
    return redirect(url_for('festival_details', festival_name=festival_name))
if __name__ == '__main__':
    app.run(port=5000)