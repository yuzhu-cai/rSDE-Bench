'''
This is the backend code for the Daily Journal App. It implements routing for the login, registration, dashboard, and new entry pages. 
It handles user authentication, journal entry management, and file operations for storing user credentials and journal entries.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USER_CREDENTIALS_FILE = os.path.join(DATA_DIR, 'user_credentials.txt')
JOURNAL_ENTRIES_FILE = os.path.join(DATA_DIR, 'journal_entries.txt')
def read_user_credentials():
    '''Reads user credentials from the file and returns a dictionary.'''
    credentials = {}
    if os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                credentials[username] = password
    return credentials
def write_user_credentials(username, password):
    '''Writes new user credentials to the file.'''
    with open(USER_CREDENTIALS_FILE, 'a') as file:
        file.write(f"{username}|{password}\n")
def read_journal_entries():
    '''Reads journal entries from the file and returns a list of entries.'''
    entries = []
    if os.path.exists(JOURNAL_ENTRIES_FILE):
        with open(JOURNAL_ENTRIES_FILE, 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                entries.append((title, content))
    return entries
def write_journal_entry(title, content):
    '''Writes a new journal entry to the file.'''
    with open(JOURNAL_ENTRIES_FILE, 'a') as file:
        file.write(f"{title}|{content}\n")
@app.route('/')
def login():
    '''Render the login page.'''
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Handle user registration.'''
    if request.method == 'POST':
        username = request.form['reg_username_input']
        password = request.form['reg_password_input']
        # Check if the username already exists
        credentials = read_user_credentials()
        if username in credentials:
            return render_template('register.html', error="Username already exists. Please choose a different one.")
        write_user_credentials(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    '''Render the dashboard page with journal entries.'''
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = read_journal_entries()
    return render_template('dashboard.html', entries=entries)
@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    '''Handle new journal entry creation.'''
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['entry_title_field']
        content = request.form['entry_content_field']
        write_journal_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')
@app.route('/login', methods=['POST'])
def do_login():
    '''Authenticate user login.'''
    username = request.form['username_input']
    password = request.form['password_input']
    credentials = read_user_credentials()
    if username in credentials and credentials[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
    '''Log out the user.'''
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)