'''
This is the main backend application for the SkillShare web application. 
It implements routing for all frontend pages and handles file read/write operations 
for user data, skills data, profile data, and about data, including session management for user authentication.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages
# Function to create data directory and initialize files if they do not exist
def initialize_data_files():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.isfile('data/users.txt'):
        with open('data/users.txt', 'w') as file:
            pass  # Create the file if it doesn't exist
    if not os.path.isfile('data/skills.txt'):
        with open('data/skills.txt', 'w') as file:
            pass  # Create the file if it doesn't exist
    if not os.path.isfile('data/profiles.txt'):
        with open('data/profiles.txt', 'w') as file:
            pass  # Create the file if it doesn't exist
    if not os.path.isfile('data/about.txt'):
        with open('data/about.txt', 'w') as file:
            file.write("This is a SkillShare application.|contact@example.com\n")  # Initialize with example content
# Call the function to ensure data files are set up
initialize_data_files()
# Function to read users from the users.txt file
def read_users():
    users = {}
    with open('data/users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            users[username] = password
    return users
# Function to read skills from the skills.txt file
def read_skills():
    skills = {}
    with open('data/skills.txt', 'r') as file:
        for line in file:
            username, skill_list = line.strip().split(':')
            skills[username] = skill_list.split(',')
    return skills
# Function to read profiles from the profiles.txt file
def read_profiles():
    profiles = []
    with open('data/profiles.txt', 'r') as file:
        for line in file:
            profiles.append(line.strip())
    return profiles
# Function to read about information from the about.txt file
def read_about():
    with open('data/about.txt', 'r') as file:
        info = file.readline().strip().split('|')
    return info[0], info[1]
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    users = read_users()
    if username in users and users[username] == password:
        session['username'] = username  # Create session for logged-in user
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()  # Read existing users
        if username in users:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('register'))  # Redirect back to the registration page
        with open('data/users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    username = session['username']  # Get the current user's username from the session
    skills = read_skills()
    user_skills = skills.get(username, [])  # Get the skills for the logged-in user
    return render_template('dashboard.html', user_skills=user_skills)  # Pass user skills to the template
@app.route('/skills', methods=['GET'])
def skills():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    username = session['username']  # Get the current user's username from the session
    skills = read_skills()
    user_skills = skills.get(username, [])  # Get the skills for the logged-in user
    return render_template('skills.html', skills=user_skills, current_user=username)  # Pass user skills and current user to the template
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    current_username = session['username']  # Get the current user's username from the session
    if request.method == 'POST':
        new_username = request.form['username']
        users = read_users()  # Read existing users
        if new_username in users:
            flash('Username already exists. Please choose a different username.')
            return render_template('profile.html', username=current_username)  # Return to profile page with error message
        # Logic to save the updated username to profiles.txt
        with open('data/profiles.txt', 'w') as file:
            file.write(f"{new_username}\n")
        # Update session username
        session['username'] = new_username
        return redirect(url_for('dashboard'))
    return render_template('profile.html', username=current_username)  # Pass the username to the template
@app.route('/about')
def about():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    about_info, contact_info = read_about()  # Call read_about function and get values
    return render_template('about.html', info=about_info, contact=contact_info)  # Pass values to the template
@app.route('/add_skill', methods=['GET'])
def add_skill():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    skill = request.args.get('skill')
    username = session['username']  # Get the current user's username from the session
    if skill and username:
        skills = read_skills()
        if username in skills:
            skills[username].append(skill)
        else:
            skills[username] = [skill]
        with open('data/skills.txt', 'w') as file:
            for user, skill_list in skills.items():
                file.write(f"{user}:{','.join(skill_list)}\n")
    return redirect(url_for('skills'))
@app.route('/remove_skill', methods=['GET'])
def remove_skill():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    skill = request.args.get('skill')
    username = session['username']  # Get the current user's username from the session
    if skill and username:
        skills = read_skills()
        if username in skills:
            skills[username].remove(skill)
            if not skills[username]:  # Remove user if no skills left
                del skills[username]
        with open('data/skills.txt', 'w') as file:
            for user, skill_list in skills.items():
                file.write(f"{user}:{','.join(skill_list)}\n")
    return redirect(url_for('skills'))
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)