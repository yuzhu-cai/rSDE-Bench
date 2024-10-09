'''
This file implements the backend logic for the TravelDiary web application.
It handles routing for all frontend pages and manages file read/write operations
for user and diary entry data.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DIARY_ENTRIES_FILE = os.path.join(DATA_DIR, 'diary_entries.txt')
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        with open(USERS_FILE, 'r') as f:
            users = f.readlines()
            for user in users:
                u, p, _ = user.strip().split(',')
                if u == username and p == password:
                    session['username'] = username  # Store username in session
                    return redirect(url_for('home'))
        flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        email = request.form['inputEmail']
        # Check for existing username
        with open(USERS_FILE, 'r') as f:
            users = f.readlines()
            for user in users:
                u, _, _ = user.strip().split(',')
                if u == username:
                    flash('Username already exists. Please choose a different one.', 'danger')
                    return redirect(url_for('register'))
        # If username is unique, proceed to register
        with open(USERS_FILE, 'a') as f:
            f.write(f"{username},{password},{email}\n")
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/home')
def home():
    entries = []
    with open(DIARY_ENTRIES_FILE, 'r') as f:
        entries = f.readlines()
    return render_template('home.html', entries=entries)
@app.route('/diary_entry', methods=['GET', 'POST'])
def diary_entry():
    if request.method == 'POST':
        title = request.form['inputEntryTitle']
        content = request.form['textareaEntry']
        username = session.get('username')  # Get the actual logged-in user
        with open(DIARY_ENTRIES_FILE, 'a') as f:
            entry_id = sum(1 for line in open(DIARY_ENTRIES_FILE)) + 1
            f.write(f"{entry_id},{username},{title},{content}\n")
        flash('Diary entry saved!', 'success')
        return redirect(url_for('home'))
    return render_template('diary_entry.html')
@app.route('/view_diary')
def view_diary():
    entries = []
    with open(DIARY_ENTRIES_FILE, 'r') as f:
        entries = f.readlines()
    return render_template('view_diary.html', entries=entries)
@app.route('/edit_diary/<int:entry_id>', methods=['GET', 'POST'])
def edit_diary(entry_id):
    if request.method == 'POST':
        title = request.form['inputEntryTitle']
        content = request.form['textareaEntry']
        username = session.get('username')  # Get the actual logged-in user
        # Read all entries
        entries = []
        with open(DIARY_ENTRIES_FILE, 'r') as f:
            entries = f.readlines()
        # Update the specific entry
        with open(DIARY_ENTRIES_FILE, 'w') as f:
            for entry in entries:
                if entry.startswith(str(entry_id)):
                    f.write(f"{entry_id},{username},{title},{content}\n")
                else:
                    f.write(entry)
        flash('Diary entry updated!', 'success')
        return redirect(url_for('view_diary'))
    # Load the entry to edit
    entry_to_edit = None
    with open(DIARY_ENTRIES_FILE, 'r') as f:
        for entry in f:
            if entry.startswith(str(entry_id)):
                entry_to_edit = entry.split(',')
                break
    if entry_to_edit is None:
        flash('Entry not found!', 'danger')
        return redirect(url_for('view_diary'))
    return render_template('edit_diary.html', entry=entry_to_edit)
@app.route('/delete_diary/<int:entry_id>', methods=['POST'])
def delete_diary(entry_id):
    entries = []
    with open(DIARY_ENTRIES_FILE, 'r') as f:
        entries = f.readlines()
    # Write back all entries except the one to delete
    with open(DIARY_ENTRIES_FILE, 'w') as f:
        for entry in entries:
            if not entry.startswith(str(entry_id)):
                f.write(entry)
    flash('Diary entry deleted!', 'success')
    return redirect(url_for('view_diary'))
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))
@app.route('/contact_support')
def contact_support():
    return render_template('contact_support.html')  # Assuming you have a contact support page
if __name__ == '__main__':
    app.run(port=5000)