'''
This is the main backend application for the Digital Storytelling Platform.
It handles routing for the login, registration, and story creation pages,
as well as user authentication and story management using local text files.
'''
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
# File paths
USER_DATA_FILE = 'data/users.txt'
STORY_DATA_FILE = 'data/stories.txt'
def read_users():
    '''Read user data from the users.txt file.'''
    users = {}
    with open(USER_DATA_FILE, 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users
def write_user(username, password):
    '''Write a new user to the users.txt file.'''
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username}|{password}\n")
def write_story(user_id, story_title, story_content):
    '''Write a new story to the stories.txt file.'''
    with open(STORY_DATA_FILE, 'a') as file:
        file.write(f"{user_id}|{story_title}|{story_content}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    '''Render the login page and handle user authentication.'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('create_story'))  # Redirect to story creation page
        else:
            return "Invalid credentials", 401
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Handle user registration.'''
    if request.method == 'POST':
        username = request.form['reg_username_input']
        password = request.form['reg_password_input']
        write_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    '''Handle story creation.'''
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    if request.method == 'POST':
        user_id = session['username']  # Get username from session
        story_title = request.form['story_title_field']
        story_content = request.form['story_content_field']
        write_story(user_id, story_title, story_content)
        return redirect(url_for('create_story'))  # Redirect to story creation page after saving
    return render_template('create_story.html')
if __name__ == '__main__':
    app.run(port=5000)