'''
Main Python file containing the backend logic for the FitnessChallenges web application.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
import logging
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production
# File paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
CHALLENGES_FILE = os.path.join(DATA_DIR, 'challenges.txt')
CURRENT_CHALLENGES_FILE = os.path.join(DATA_DIR, 'current_challenges.txt')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.txt')
ACTIVITY_LOG_FILE = os.path.join(DATA_DIR, 'activityLog.txt')
# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)
@app.route('/')
def login():
    '''
    Render the login page.
    '''
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    '''
    Render the user dashboard after successful login.
    '''
    if 'username' in session:
        username = session['username']
        current_challenges = get_current_challenges(username)
        activity_log = get_activity_log(username)
        return render_template('dashboard.html', username=username, current_challenges=current_challenges, activity_log=activity_log)
    return redirect(url_for('login'))
@app.route('/challenges')
def challenges():
    '''
    Render the challenges list page.
    '''
    available_challenges = get_available_challenges()
    return render_template('challenges.html', challenges=available_challenges)
@app.route('/progress_tracker')
def progress_tracker():
    '''
    Render the progress tracker page for the logged-in user.
    '''
    if 'username' in session:
        username = session['username']
        current_challenges = get_current_challenges(username)
        return render_template('progress_tracker.html', challenges=current_challenges)
    return redirect(url_for('login'))
@app.route('/login', methods=['POST'])
def do_login():
    '''
    Handle user login.
    '''
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        session['username'] = username
        log_activity(username, 'Logged in')
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
    '''
    Handle user logout.
    '''
    if 'username' in session:
        log_activity(session['username'], 'Logged out')
        session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/join_challenge', methods=['POST'])
def join_challenge():
    '''
    Handle joining a challenge.
    '''
    if 'username' in session:
        username = session['username']
        challenge_name = request.json['challenge_name']
        with open(CURRENT_CHALLENGES_FILE, 'a') as file:
            file.write(f"{username}:{challenge_name}\n")
        log_activity(username, f'Joined {challenge_name}')
        return '', 200
    return '', 403
@app.route('/update_progress', methods=['POST'])
def update_progress():
    '''
    Handle updating user progress.
    '''
    if 'username' in session:
        username = session['username']
        data = request.json
        progress = data['progress']
        notes = data['notes']
        challenge_name = data['challenge_name']  # Get challenge name from request
        # Check if the user is part of the challenge
        if not is_user_in_challenge(username, challenge_name):
            return '', 403  # Forbidden if the user is not in the challenge
        # Check if the user already has progress recorded for this challenge
        existing_progress = []
        with open(PROGRESS_FILE, 'r') as file:
            for line in file:
                if line.startswith(f"{username}:{challenge_name}:"):
                    existing_progress.append(line.strip())
        if existing_progress:
            # Update the existing entry
            updated_line = f"{username}:{challenge_name}:{progress}:{notes}\n"
            with open(PROGRESS_FILE, 'w') as file:
                for line in file:
                    if line.strip() != existing_progress[0]:  # Remove the old entry
                        file.write(line)
                file.write(updated_line)  # Write the updated entry
        else:
            # Append a new entry if no existing progress
            with open(PROGRESS_FILE, 'a') as file:
                file.write(f"{username}:{challenge_name}:{progress}:{notes}\n")
        log_activity(username, f'Updated progress for {challenge_name}')
        return '', 200
    return '', 403
def validate_user(username, password):
    '''
    Validate user credentials against the users.txt file.
    '''
    with open(USERS_FILE, 'r') as file:
        for line in file:
            user, pwd = line.strip().split(':')
            if user == username and pwd == password:
                return True
    return False
def get_current_challenges(username):
    '''
    Retrieve the current challenges for a specific user.
    '''
    challenges = []
    with open(CURRENT_CHALLENGES_FILE, 'r') as file:
        for line in file:
            user, challenge = line.strip().split(':')
            if user == username:
                challenges.append(challenge)
    return challenges
def get_available_challenges():
    '''
    Retrieve the list of available challenges from challenges.txt.
    '''
    challenges = []
    try:
        with open(CHALLENGES_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 3:  # Ensure the line is properly formatted
                    challenges.append(line.strip())
                else:
                    logging.error(f"Improperly formatted line in challenges file: {line.strip()}")
    except FileNotFoundError:
        logging.error(f"{CHALLENGES_FILE} not found.")
    except Exception as e:
        logging.error(f"Error reading {CHALLENGES_FILE}: {str(e)}")
    return challenges
def get_activity_log(username):
    '''
    Retrieve the activity log for a specific user.
    '''
    log = []
    with open(ACTIVITY_LOG_FILE, 'r') as file:
        for line in file:
            try:
                timestamp, user, activity = line.strip().split(':')
                if user == username:
                    log.append(f"{timestamp}: {activity}")
            except ValueError:
                logging.error(f"Improperly formatted line in activity log: {line.strip()}")
    return log
def log_activity(username, activity_description):
    '''
    Log user activities to the activityLog.txt file.
    '''
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ACTIVITY_LOG_FILE, 'a') as file:
        file.write(f"{timestamp}:{username}:{activity_description}\n")
def is_user_in_challenge(username, challenge_name):
    '''
    Check if the user is part of the specified challenge.
    '''
    with open(CURRENT_CHALLENGES_FILE, 'r') as file:
        for line in file:
            user, challenge = line.strip().split(':')
            if user == username and challenge == challenge_name:
                return True
    return False
if __name__ == '__main__':
    app.run(port=5000)