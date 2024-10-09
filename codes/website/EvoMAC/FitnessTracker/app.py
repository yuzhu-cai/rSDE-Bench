'''
This is the main application file for the FitnessTracker web application.
It handles routing for all frontend pages and manages file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
GOALS_FILE = os.path.join(DATA_DIR, 'goals.txt')
ACTIVITIES_FILE = os.path.join(DATA_DIR, 'activities.txt')
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    with open(USERS_FILE, 'r') as f:
        users = f.readlines()
    for user in users:
        user_info = user.strip().split(':')
        if user_info[0] == username and user_info[1] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    flash('Invalid credentials!', 'error')
    return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['register_username_field']
        password = request.form['register_password_field']
        confirm_password = request.form['confirm_password_field']
        current_weight = request.form['current_weight_field']
        goal_weight = request.form['goal_weight_field']
        if password == confirm_password:
            with open(USERS_FILE, 'a') as f:
                f.write(f"{username}:{password}\n")
            with open(GOALS_FILE, 'a') as f:
                f.write(f"{username}|{current_weight}|{goal_weight}\n")
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match!', 'error')
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    current_weight, goal_weight = get_user_goals(username)
    return render_template('dashboard.html', current_weight=current_weight, goal_weight=goal_weight)
@app.route('/update_goal', methods=['GET', 'POST'])
def update_goal():
    if request.method == 'POST':
        username = session.get('username')
        goal_weight = request.form['goal_value_field']
        update_goal_weight(username, goal_weight)
        return redirect(url_for('dashboard'))
    return render_template('update_goal.html', username=session.get('username'))
@app.route('/log_activity', methods=['GET', 'POST'])
def log_activity():
    if request.method == 'POST':
        username = session.get('username')
        activity_type = request.form['activity_type_field']
        calories_burned = request.form['calories_burned_field']
        current_weight = request.form['current_weight_field']
        with open(ACTIVITIES_FILE, 'a') as f:
            f.write(f"{username}|{activity_type}|{calories_burned}|{current_weight}\n")
        return redirect(url_for('dashboard'))
    return render_template('log_activity.html', username=session.get('username'))
@app.route('/view_activity')
def view_activity():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    activities = get_user_activities(username)
    return render_template('view_activity.html', activities=activities)
@app.route('/edit_activity', methods=['GET', 'POST'])
def edit_activity():
    username = session.get('username')
    if request.method == 'POST':
        activity_type = request.form['activity_type_field']
        calories_burned = request.form['calories_burned_field']
        current_weight = request.form['current_weight_field']
        update_activity(username, activity_type, calories_burned, current_weight)
        return redirect(url_for('view_activity'))
    else:
        activity_type = request.args.get('activity_type')
        activities = get_user_activities(username)
        # Find the activity to edit
        for activity in activities:
            if activity[1] == activity_type:
                return render_template('edit_activity.html', 
                                       activity_type=activity[1], 
                                       calories_burned=activity[2], 
                                       current_weight=activity[3], 
                                       username=username)
        flash('Activity not found!', 'error')
        return redirect(url_for('view_activity'))
@app.route('/delete_activity', methods=['POST'])
def delete_activity():
    username = session.get('username')
    activity_type = request.form['activity_type']
    activities = []
    activity_found = False  # Flag to check if activity exists
    with open(ACTIVITIES_FILE, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if not (line.startswith(username) and line.split('|')[1] == activity_type):
            activities.append(line)
        else:
            activity_found = True  # Activity found and marked for deletion
    with open(ACTIVITIES_FILE, 'w') as f:
        f.writelines(activities)
    if activity_found:
        flash('Activity deleted successfully!', 'success')  # Notify user of successful deletion
    else:
        flash('Activity not found!', 'error')  # Notify user if activity was not found
    return redirect(url_for('view_activity'))
def update_goal_weight(username, goal_weight):
    with open(GOALS_FILE, 'r') as f:
        lines = f.readlines()
    with open(GOALS_FILE, 'w') as f:
        for line in lines:
            if line.startswith(username):
                parts = line.strip().split('|')
                f.write(f"{parts[0]}|{parts[1]}|{goal_weight}\n")
            else:
                f.write(line)
def get_user_goals(username):
    with open(GOALS_FILE, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith(username):
            parts = line.strip().split('|')
            return parts[1], parts[2]  # current_weight, goal_weight
    return None, None
def get_user_activities(username):
    activities = []
    with open(ACTIVITIES_FILE, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith(username):
            activities.append(line.strip().split('|'))
    return activities
def update_activity(username, activity_type, calories_burned, current_weight):
    activities = []
    activity_found = False  # Flag to check if activity exists
    with open(ACTIVITIES_FILE, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith(username) and line.split('|')[1] == activity_type:
            activities.append(f"{username}|{activity_type}|{calories_burned}|{current_weight}\n")
            activity_found = True  # Activity found and updated
        else:
            activities.append(line)
    with open(ACTIVITIES_FILE, 'w') as f:
        f.writelines(activities)
    if not activity_found:
        flash('Activity not found!', 'error')  # Notify user if activity was not found
if __name__ == '__main__':
    app.run(port=5000)