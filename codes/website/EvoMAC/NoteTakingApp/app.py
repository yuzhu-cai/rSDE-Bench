'''
This is the main backend application for the NoteTakingApp.
It handles routing for all frontend pages and manages user authentication and note management.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
NOTES_FILE = os.path.join(DATA_DIR, 'notes.txt')
def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                username, password = line.strip().split(':')
                users[username] = password
    return users
def write_user(username, password):
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}:{password}\n")
def read_notes():
    notes = []
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            for line in f:
                note_id, title, content = line.strip().split('|')
                notes.append({'id': note_id, 'title': title, 'content': content})
    return notes
def write_note(title, content):
    notes = read_notes()
    # Determine the next ID
    note_id = str(max(int(note['id']) for note in notes) + 1) if notes else '1'
    with open(NOTES_FILE, 'a') as f:
        f.write(f"{note_id}|{title}|{content}\n")
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    users = read_users()
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error_message="Invalid username or password.")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['register_username_field']
        password = request.form['register_password_field']
        # Check if the username already exists
        users = read_users()
        if username in users:
            return render_template('register.html', registration_success_message="Username already exists! Please choose another.")
        write_user(username, password)
        return render_template('register.html', registration_success_message="Registration successful!")
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = read_notes()
    return render_template('dashboard.html', notes=notes)
@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['note_title_field']
        content = request.form['note_content_field']
        write_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')
@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        title = request.form['search_note_field']
        notes = read_notes()
        search_results = [note for note in notes if title.lower() in note['title'].lower()]
        return render_template('search_note.html', search_note_result=search_results)
    return render_template('search_note.html')
@app.route('/view_note/<note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    notes = read_notes()
    note = next((note for note in notes if note['id'] == note_id), None)
    if note is None:
        return redirect(url_for('dashboard'))  # Redirect if note not found
    if request.method == 'POST':
        if 'delete_note_button' in request.form:
            notes = [n for n in notes if n['id'] != note_id]  # Remove the note
            # Reassign IDs only if necessary
            for index, n in enumerate(notes):
                n['id'] = str(index + 1)  # Reassign IDs sequentially
            with open(NOTES_FILE, 'w') as f:
                for n in notes:
                    f.write(f"{n['id']}|{n['title']}|{n['content']}\n")
            return redirect(url_for('dashboard'))
        elif 'edit_note_button' in request.form:
            note['title'] = request.form['note_title_field']
            note['content'] = request.form['note_content_field']
            with open(NOTES_FILE, 'w') as f:
                for n in notes:
                    f.write(f"{n['id']}|{n['title']}|{n['content']}\n")
            return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=note)
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)