'''
This file implements the backend logic for the Personal Blog web application.
It handles routing for all frontend pages, user authentication, and file operations
for storing user data and blog posts.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
POSTS_FILE = os.path.join(DATA_DIR, 'posts.txt')
LOGS_FILE = os.path.join(DATA_DIR, 'logs.txt')
def log_event(event):
    '''Logs events to the logs.txt file.'''
    with open(LOGS_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()}|{event}\n")
def read_users():
    '''Reads user data from users.txt file.'''
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
    return users
def write_user(username, password):
    '''Writes a new user to the users.txt file.'''
    with open(USERS_FILE, 'a') as file:
        file.write(f"{username},{password}\n")
def read_posts():
    '''Reads blog posts from posts.txt file.'''
    posts = []
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                posts.append({'title': title, 'content': content})
    return posts
def write_post(title, content):
    '''Writes a new blog post to the posts.txt file.'''
    with open(POSTS_FILE, 'a') as file:
        file.write(f"{title}|{content}\n")
def delete_post(title):
    '''Deletes a blog post from the posts.txt file.'''
    posts = read_posts()
    posts = [post for post in posts if post['title'] != title]
    with open(POSTS_FILE, 'w') as file:
        for post in posts:
            file.write(f"{post['title']}|{post['content']}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    '''Displays the login page and handles user login.'''
    if request.method == 'POST':
        username = request.form['username_input']
        password = request.form['password_input']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username
            log_event(f"User {username} logged in.")
            return redirect(url_for('main_blog'))
        else:
            return render_template('login.html', login_message='Invalid username or password.')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Handles user registration.'''
    if request.method == 'POST':
        username = request.form['reg_username_input']
        password = request.form['reg_password_input']
        email = request.form['reg_email_input']  # Email is not used in this implementation
        users = read_users()
        if username in users:
            return render_template('register.html', register_message='Username already exists.')
        write_user(username, password)
        log_event(f"User {username} registered.")
        return redirect(url_for('login'))
    return render_template('register.html', register_message='')
@app.route('/main_blog', methods=['GET'])
def main_blog():
    '''Displays the main blog page with the list of posts.'''
    posts = read_posts()
    return render_template('main_blog.html', post_list=posts)
@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    '''Handles the creation of a new blog post.'''
    if request.method == 'POST':
        title = request.form['post_title_input']
        content = request.form['post_content_area']
        write_post(title, content)
        log_event(f"User created a new post titled '{title}'.")
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')
@app.route('/view_post/<title>', methods=['GET'])
def view_post(title):
    '''Displays a specific blog post.'''
    posts = read_posts()
    post = next((p for p in posts if p['title'] == title), None)
    if post is None:
        return render_template('view_post.html', view_post_title='Post Not Found', view_post_content='This post does not exist.')
    return render_template('view_post.html', view_post_title=post['title'], view_post_content=post['content'])
@app.route('/delete_post/<title>', methods=['POST'])
def delete_post_route(title):
    '''Handles the deletion of a blog post.'''
    delete_post(title)
    log_event(f"User deleted the post titled '{title}'.")
    return redirect(url_for('main_blog'))
@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    '''Handles editing of an existing blog post.'''
    posts = read_posts()
    post = next((p for p in posts if p['title'] == title), None)
    if post is None:
        return redirect(url_for('main_blog', blog_message='Post not found.'))
    if request.method == 'POST':
        new_title = request.form['post_title_input']
        new_content = request.form['post_content_input']
        # Remove the old post
        posts = [p for p in posts if p['title'] != title]
        # Add the updated post
        posts.append({'title': new_title, 'content': new_content})
        # Write all posts back to the posts.txt file
        with open(POSTS_FILE, 'w') as file:
            for p in posts:
                file.write(f"{p['title']}|{p['content']}\n")
        log_event(f"User edited the post titled '{title}' to '{new_title}'.")
        return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post_title=post['title'], post_content=post['content'])
@app.route('/logout')
def logout():
    '''Logs out the user and redirects to the login page.'''
    session.clear()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)