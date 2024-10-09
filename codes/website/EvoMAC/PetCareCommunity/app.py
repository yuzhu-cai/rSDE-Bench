'''
This is the main backend application for the PetCareCommunity web application.
It handles routing for all frontend pages and manages file read/write operations
for user data, posts, resources, and profiles.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
DATA_DIR = 'data/'
def read_users():
    users = {}
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            users[username] = password
    return users
def read_posts():
    posts = []
    with open(os.path.join(DATA_DIR, 'posts.txt'), 'r') as file:
        for line in file:
            post_id, username, timestamp, content = line.strip().split(',')
            posts.append({'id': post_id, 'username': username, 'timestamp': timestamp, 'content': content})
    return posts
def read_resources():
    resources = []
    with open(os.path.join(DATA_DIR, 'resources.txt'), 'r') as file:
        for line in file:
            title, description, link = line.strip().split(',')
            resources.append({'title': title, 'description': description, 'link': link})
    return resources
def read_profile(username):
    with open(os.path.join(DATA_DIR, 'profiles.txt'), 'r') as file:
        for line in file:
            user, pet_name, pet_age = line.strip().split(',')
            if user == username:
                return {'pet_name': pet_name, 'pet_age': pet_age}
    return None
def write_post(username, content):
    post_id = str(len(read_posts()) + 1)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(os.path.join(DATA_DIR, 'posts.txt'), 'a') as file:
        file.write(f"{post_id},{username},{timestamp},{content}\n")
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/community_feed', methods=['GET', 'POST'])
def community_feed():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            if 'post-content' in request.form:
                content = request.form['post-content']
                write_post(username, content)
            posts = read_posts()
            return render_template('community_feed.html', posts=posts)
        else:
            return redirect(url_for('login'))
    return redirect(url_for('login'))
@app.route('/resources')
def resources():
    resources = read_resources()
    return render_template('resources.html', resources=resources)
@app.route('/profile/<username>')
def profile(username):
    user_profile = read_profile(username)
    return render_template('profile.html', profile=user_profile, username=username)
if __name__ == '__main__':
    app.run(port=5000)