'''
Main application file for the Task_Manager web application.
This file handles routing for the login, registration, and home pages,
as well as user authentication and task management functionalities.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data'
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.txt')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
def read_users():
    '''Read user data from the users.txt file.'''
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        users = {}
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users
def write_user(username, password):
    '''Write a new user to the users.txt file.'''
    with open(USERS_FILE, 'a') as file:
        file.write(f"{username}|{password}\n")
def read_tasks():
    '''Read task data from the tasks.txt file.'''
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        tasks = []
        for line in file:
            task_id, task_title, due_date = line.strip().split('|')
            tasks.append({'id': task_id, 'title': task_title, 'due_date': due_date})
    return tasks
def write_task(task_title, due_date):
    '''Write a new task to the tasks.txt file.'''
    tasks = read_tasks()
    task_id = str(len(tasks) + 1)
    with open(TASKS_FILE, 'a') as file:
        file.write(f"{task_id}|{task_title}|{due_date}\n")
def remove_task(task_id):
    '''Remove a task from the tasks.txt file by task_id.'''
    tasks = read_tasks()
    with open(TASKS_FILE, 'w') as file:
        for task in tasks:
            if task['id'] != str(task_id):  # Ensure task_id is compared as a string
                file.write(f"{task['id']}|{task['title']}|{task['due_date']}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    '''Render the login page and handle user authentication.'''
    if request.method == 'POST':
        username = request.form['username_input']
        password = request.form['password_input']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Handle user registration.'''
    if request.method == 'POST':
        username = request.form['reg_username_input']
        password = request.form['reg_password_input']
        users = read_users()  # Read existing users
        if username in users:
            return render_template('register.html', error='Username already exists. Please choose a different one.')
        write_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/home', methods=['GET', 'POST'])
def home():
    '''Render the home page and manage tasks.'''
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'add_task_button' in request.form:
            task_title = request.form['add_task_input']
            due_date = request.form['due_date_input']
            write_task(task_title, due_date)
        if 'remove_task_button' in request.form:
            task_id = request.form['remove_task_button']
            remove_task(task_id)
    tasks = read_tasks()
    return render_template('home.html', tasks=tasks)
@app.route('/logout')
def logout():
    '''Handle user logout.'''
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)