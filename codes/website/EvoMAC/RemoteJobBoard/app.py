'''
This is the main backend application for the RemoteJobBoard web application.
It handles routing for all frontend pages and manages file read/write operations
for user and job data.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
JOBS_FILE = os.path.join(DATA_DIR, 'jobs.txt')
APPLIED_JOBS_FILE = os.path.join(DATA_DIR, 'applied_jobs.txt')
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('home'))
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login'))
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')  # Optional email field
        # Check for existing users
        users = read_users()
        if any(user[0] == username for user in users):
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('register'))
        with open(USERS_FILE, 'a') as file:
            file.write(f"{username},{password},{email}\n")
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/home')
def home():
    jobs = read_jobs()
    return render_template('home.html', jobs=jobs)
@app.route('/job_listings')
def job_listings():
    jobs = read_jobs()
    return render_template('job_listings.html', jobs=jobs)
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job_title = request.form['job-title']
        company_name = request.form['company-name']
        job_description = request.form['job-description']
        write_job(job_title, company_name, job_description)
        flash('Job posted successfully!')
        return redirect(url_for('home'))
    return render_template('post_job.html')
@app.route('/user_profile')
def user_profile():
    username = session.get('username')  # Get the logged-in user's username
    if not username:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    users = read_users()
    applied_jobs = read_applied_jobs(username)  # Get applied jobs for the user
    user_info = next((user for user in users if user[0] == username), None)
    if user_info:
        email = user_info[2]
    else:
        email = ''
    return render_template('user_profile.html', username=username, email=email, applied_jobs=applied_jobs)
@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    new_username = request.form['username']
    new_email = request.form['email']
    # Read current users
    users = read_users()
    # Update user information
    updated_users = []
    for user in users:
        if user[0] == username:
            updated_users.append(f"{new_username},{user[1]},{new_email}\n")
        else:
            updated_users.append(f"{user[0]},{user[1]},{user[2]}\n")
    # Write updated users back to the file
    with open(USERS_FILE, 'w') as file:
        file.writelines(updated_users)
    session['username'] = new_username  # Update session username
    flash('Profile updated successfully!')
    return redirect(url_for('user_profile'))
@app.route('/apply_job', methods=['POST'])
def apply_job():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    job_title = request.form['job_title']  # Get job title from the form
    company_name = request.form['company_name']  # Get company name from the form
    job_description = request.form['job_description']  # Get job description from the form
    with open(APPLIED_JOBS_FILE, 'a') as file:
        file.write(f"{username}:{job_title},{company_name},{job_description}\n")
    flash('Job application submitted successfully!')
    return redirect(url_for('job_listings'))
def read_users():
    users = []
    with open(USERS_FILE, 'r') as file:
        for line in file:
            users.append(line.strip().split(','))
    return users
def read_jobs():
    jobs = []
    with open(JOBS_FILE, 'r') as file:
        for line in file:
            jobs.append(line.strip().split(','))
    return jobs
def write_job(job_title, company_name, job_description):
    with open(JOBS_FILE, 'a') as file:
        file.write(f"{job_title},{company_name},{job_description}\n")
def read_applied_jobs(username):
    applied_jobs = []
    with open(APPLIED_JOBS_FILE, 'r') as file:
        for line in file:
            if line.startswith(username + ':'):
                applied_jobs.append(line.strip().split(':')[1])  # Extract job title
    return applied_jobs
if __name__ == '__main__':
    app.run(port=5000)