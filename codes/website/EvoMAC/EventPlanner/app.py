'''
This file contains the backend code for the EventPlanner web application. 
It handles routing for all frontend pages, manages user authentication, 
and event management using local text files for data storage.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
EVENTS_FILE = os.path.join(DATA_DIR, 'events.txt')
def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                users[username] = password
    return users
def write_user(username, password):
    with open(USERS_FILE, 'a') as file:
        file.write(f"{username}:{password}\n")
def read_events():
    events = []
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as file:
            for line in file:
                event_id, title, date, location, description = line.strip().split('|')
                events.append({
                    'id': event_id,
                    'title': title,
                    'date': date,
                    'location': location,
                    'description': description
                })
    return events
def write_event(event):
    with open(EVENTS_FILE, 'a') as file:
        file.write(f"{event['id']}|{event['title']}|{event['date']}|{event['location']}|{event['description']}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['register_username_field']
        password = request.form['register_password_field']
        confirm_password = request.form['confirm_password_field']
        if password == confirm_password:
            users = read_users()
            if username not in users:
                write_user(username, password)
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists. Please choose another one.', 'error')
        else:
            flash('Passwords do not match.', 'error')
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', events=read_events())
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event_title = request.form['event_title_field']
        event_date = request.form['event_date_field']
        event_location = request.form['event_location_field']
        event_description = request.form['event_description_field']
        events = read_events()
        event_id = str(len(events) + 1)
        event = {
            'id': event_id,
            'title': event_title,
            'date': event_date,
            'location': event_location,
            'description': event_description
        }
        write_event(event)
        return redirect(url_for('dashboard'))
    return render_template('add_event.html')
@app.route('/search_event', methods=['GET', 'POST'])
def search_event():
    search_results = []
    if request.method == 'POST':
        search_query = request.form['search_event_field']
        events = read_events()
        search_results = [event for event in events if search_query in event['title'] or search_query in event['date']]
    return render_template('search_event.html', search_results=search_results)
@app.route('/view_event/<event_id>', methods=['GET', 'POST'])
def view_event(event_id):
    events = read_events()
    event = next((e for e in events if e['id'] == event_id), None)
    if event is None:
        flash('Event not found.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        event['title'] = request.form['event_title_field']
        event['date'] = request.form['event_date_field']
        event['location'] = request.form['event_location_field']
        event['description'] = request.form['event_description_field']
        # Rewrite the events file
        with open(EVENTS_FILE, 'w') as file:
            for e in events:
                file.write(f"{e['id']}|{e['title']}|{e['date']}|{e['location']}|{e['description']}\n")
        return redirect(url_for('dashboard'))
    return render_template('view_event.html', event=event)
@app.route('/delete_event/<event_id>', methods=['POST'])
def delete_event(event_id):
    events = read_events()
    events = [event for event in events if event['id'] != event_id]
    # Rewrite the events file without the deleted event
    with open(EVENTS_FILE, 'w') as file:
        for e in events:
            file.write(f"{e['id']}|{e['title']}|{e['date']}|{e['location']}|{e['description']}\n")
    return redirect(url_for('dashboard'))
@app.route('/logout')
def logout():
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)