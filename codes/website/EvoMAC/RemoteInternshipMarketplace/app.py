'''
This is the main application file for the RemoteInternshipMarketplace web application.
It handles routing for the login, registration, dashboard, internship listings, 
posting internships, and internship details pages. It also manages user data 
and internship data storage in local text files, including session management for logged-in users.
'''
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
INTERNSHIPS_FILE = os.path.join(DATA_DIR, 'internships.txt')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'applications.txt')
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['input_username']
        password = request.form['input_password']
        with open(USERS_FILE, 'r') as f:
            users = f.readlines()
            for user in users:
                user_data = user.strip().split(',')
                if user_data[0] == username and user_data[1] == password:
                    session['username'] = username  # Store username in session
                    return redirect(url_for('dashboard'))  # Redirect to dashboard on successful login
        return "Invalid credentials", 401  # Handle invalid login
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['input_username']
        first_name = request.form['input_first_name']
        last_name = request.form['input_last_name']
        email = request.form['input_email']
        password = request.form['input_password']
        confirm_password = request.form['input_confirm_password']
        if password != confirm_password:
            return "Passwords do not match", 400  # Handle password mismatch
        with open(USERS_FILE, 'a') as f:
            f.write(f"{username},{password},{first_name},{last_name},{email}\n")
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    # Fetch available internships to display on the dashboard
    internships = []
    with open(INTERNSHIPS_FILE, 'r') as f:
        internships = [line.strip().split(',') for line in f.readlines()]
    return render_template('dashboard.html', internships=internships)
@app.route('/internship_listings')
def internship_listings():
    # Read internships from the file and pass to the template
    internships = []
    with open(INTERNSHIPS_FILE, 'r') as f:
        internships = [line.strip().split(',') for line in f.readlines()]
    return render_template('internship_listings.html', internships=internships)
@app.route('/search_internships', methods=['GET'])
def search_internships():
    query = request.args.get('query', '').lower()
    results = []
    with open(INTERNSHIPS_FILE, 'r') as f:
        internships = [line.strip().split(',') for line in f.readlines()]
        for internship in internships:
            if query in internship[1].lower():  # Check if the query is in the title
                results.append({
                    'internship_id': internship[0],
                    'title': internship[1],
                    'description': internship[2],
                    'category': internship[3],
                    'application_deadline': internship[4]
                })
    return jsonify(results)
@app.route('/post_internship', methods=['GET', 'POST'])
def post_internship():
    if request.method == 'POST':
        title = request.form['input_internship_title']
        description = request.form['input_internship_desc']
        category = request.form['input_internship_category']
        application_deadline = request.form['input_application_deadline']
        # Read existing internships to determine the next internship_id
        if os.path.exists(INTERNSHIPS_FILE):
            with open(INTERNSHIPS_FILE, 'r') as f:
                existing_internships = f.readlines()
                internship_id = len(existing_internships) + 1  # Increment from the count of existing lines
        else:
            internship_id = 1  # Start from 1 if the file does not exist
        with open(INTERNSHIPS_FILE, 'a') as f:
            f.write(f"{internship_id},{title},{description},{category},{application_deadline}\n")
        return redirect(url_for('dashboard'))
    return render_template('post_internship.html')
@app.route('/internship_details/<int:internship_id>')
def internship_details(internship_id):
    with open(INTERNSHIPS_FILE, 'r') as f:
        internships = f.readlines()
    # Check if the internship_id is valid
    if internship_id < 1 or internship_id > len(internships):
        return "Internship not found", 404  # Return a 404 error if not found
    internship = internships[internship_id - 1].strip().split(',')
    return render_template('internship_details.html', 
                           title=internship[1], 
                           description=internship[2], 
                           category=internship[3], 
                           deadline=internship[4])
if __name__ == '__main__':
    app.run(port=5000)