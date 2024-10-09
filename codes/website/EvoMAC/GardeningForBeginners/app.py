'''
This is the main backend application for the GardeningForBeginners web application.
It handles routing for the login, gardening tips, and forum pages, as well as file operations
for user data, gardening tips, and forum posts.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
DATA_DIR = 'data'
def read_file(filename):
    with open(os.path.join(DATA_DIR, filename), 'r') as file:
        return file.readlines()
def write_file(filename, data):
    with open(os.path.join(DATA_DIR, filename), 'a') as file:
        file.write(data + '\n')
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would typically validate the username and password
        users = read_file('users.txt')
        for user in users:
            stored_username, stored_password, _ = user.strip().split(',')
            if stored_username == username and stored_password == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('gardening_tips'))
        return "Invalid username or password", 401  # Handle invalid login
    return render_template('login.html')
@app.route('/gardening_tips')
def gardening_tips():
    tips = read_file('tips.txt')
    return render_template('gardening_tips.html', tips=tips)
@app.route('/forum')
def forum():
    posts = read_file('forum_posts.txt')
    comments = read_file('comments.txt')
    return render_template('forum.html', posts=posts, comments=comments)
@app.route('/add_tip', methods=['POST'])
def add_tip():
    new_tip = request.form['add_tip_input']
    write_file('tips.txt', new_tip)
    return redirect(url_for('gardening_tips'))
@app.route('/add_post', methods=['POST'])
def add_post():
    username = session.get('username')  # Get username from session
    if username:  # Ensure username is provided
        new_post = request.form['new_post_input']
        post_id = len(read_file('forum_posts.txt')) + 1
        write_file('forum_posts.txt', f"{username},{new_post},{post_id}")
        return redirect(url_for('forum'))
    else:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    comment = request.form[f'comment_input_{post_id}']
    username = session.get('username')  # Get username from session
    if username:  # Ensure username is provided
        if comment.strip():  # Check if comment is not empty
            write_file('comments.txt', f"{post_id},{username},{comment}")
    return redirect(url_for('forum'))
if __name__ == '__main__':
    app.run(port=5000)