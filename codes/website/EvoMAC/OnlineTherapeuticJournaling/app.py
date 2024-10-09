'''
This file implements the backend code for the Online Therapeutic Journaling web application using Flask.
It sets up the web server, handles routing for all frontend pages, and manages user authentication and journal entries.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production
# File paths
USER_DATA_FILE = 'data/users.txt'
ENTRY_DATA_FILE = 'data/entries.txt'
def read_users():
    '''Read user accounts from the users.txt file.'''
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]
def write_users(users):
    '''Write user accounts to the users.txt file.'''
    with open(USER_DATA_FILE, 'w') as file:
        for user in users:
            file.write(f"{user[0]}:{user[1]}\n")
def read_entries():
    '''Read journal entries from the entries.txt file.'''
    if not os.path.exists(ENTRY_DATA_FILE):
        return []
    with open(ENTRY_DATA_FILE, 'r') as file:
        return [line.strip().split('|') for line in file.readlines()]
def write_entries(entries):
    '''Write journal entries to the entries.txt file.'''
    with open(ENTRY_DATA_FILE, 'w') as file:
        for entry in entries:
            file.write('|'.join(entry) + '\n')
@app.route('/')
def login():
    '''Render the login page.'''
    return render_template('login.html')
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    '''Render the dashboard page and handle user login.'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        return "Invalid credentials", 401
    if 'username' in session:
        entries = read_entries()
        user_entries = [entry for entry in entries if entry[1] == session['username']]
        return render_template('dashboard.html', entries=user_entries)
    return redirect(url_for('login'))
@app.route('/create_entry', methods=['GET', 'POST'])
def create_entry():
    '''Render the create journal entry page and handle entry submission.'''
    if request.method == 'POST':
        title = request.form['entry-title']
        content = request.form['entry-content']
        entries = read_entries()
        entry_id = len(entries) + 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entries.append([str(entry_id), session['username'], title, content, timestamp])
        write_entries(entries)
        return redirect(url_for('dashboard'))
    return render_template('create_entry.html')
@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    '''Render the edit journal entry page and handle entry updates.'''
    entries = read_entries()
    entry = next((entry for entry in entries if int(entry[0]) == entry_id), None)
    if request.method == 'POST':
        if entry:  # Check if entry exists
            entry[2] = request.form['edit-title']
            entry[3] = request.form['edit-content']
            write_entries(entries)
            return redirect(url_for('dashboard'))
        else:
            return "Entry not found", 404  # Return a 404 error if entry not found
    if entry:
        return render_template('edit_entry.html', entry=entry)
    return redirect(url_for('dashboard'))
@app.route('/about')
def about():
    '''Render the about page.'''
    return render_template('about.html')
@app.route('/logout')
def logout():
    '''Log out the user and redirect to the login page.'''
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)