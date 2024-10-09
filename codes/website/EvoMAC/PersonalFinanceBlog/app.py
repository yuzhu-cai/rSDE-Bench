'''
This file contains the backend code for the PersonalFinanceBlog application.
It handles routing for all frontend pages and manages file read/write operations
for user and blog post data.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
POSTS_FILE = os.path.join(DATA_DIR, 'posts.txt')
def read_users():
    '''Read user data from the users file.'''
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                username, password, occupation = line.strip().split(':')
                users[username] = {'password': password, 'occupation': occupation}
    return users
def write_user(username, password, occupation):
    '''Write a new user to the users file.'''
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}:{password}:{occupation}\n")
def read_posts():
    '''Read blog post data from the posts file.'''
    posts = []
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            for line in f:
                post_id, username, title, date, category, content = line.strip().split('|')
                posts.append({
                    'post_id': post_id,
                    'username': username,
                    'title': title,
                    'date': date,
                    'category': category,
                    'content': content
                })
    return posts
def write_post(username, title, date, category, content):
    '''Write a new blog post to the posts file.'''
    posts = read_posts()
    post_id = len(posts) + 1
    with open(POSTS_FILE, 'a') as f:
        f.write(f"{post_id}|{username}|{title}|{date}|{category}|{content}\n")
@app.route('/')
def login():
    '''Render the login page.'''
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Handle user registration.'''
    if request.method == 'POST':
        username = request.form['register_username_field']
        password = request.form['register_password_field']
        occupation = request.form['occupation_field']
        if username and password and occupation:
            write_user(username, password, occupation)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Please fill in all fields.')
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    '''Render the dashboard page.'''
    posts = read_posts()
    return render_template('dashboard.html', posts=posts)
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    '''Handle adding a new blog post.'''
    if request.method == 'POST':
        username = request.form['username']  # Assume username is passed from session
        title = request.form['post_title_field']
        date = request.form['post_date_field']
        category = request.form['post_category_field']
        content = request.form['post_content_field']
        write_post(username, title, date, category, content)
        return redirect(url_for('dashboard'))
    return render_template('add_post.html')
@app.route('/search_post')
def search_post():
    '''Render the search post page.'''
    return render_template('search_post.html')
@app.route('/category_post/<category>')
def category_post(category):
    '''Render the category post page.'''
    posts = [post for post in read_posts() if post['category'] == category]
    return render_template('category_post.html', posts=posts, category=category)
@app.route('/post_details/<int:post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    '''Render the post details page.'''
    posts = read_posts()
    post = next((p for p in posts if int(p['post_id']) == post_id), None)
    if request.method == 'POST':
        # Handle post editing logic here
        title = request.form['post_title_field']
        date = request.form['post_date']
        category = request.form['post_category']
        content = request.form['post_content']
        # Update the post in the list
        post['title'] = title
        post['date'] = date
        post['category'] = category
        post['content'] = content
        # Write all posts back to the file
        with open(POSTS_FILE, 'w') as f:
            for p in posts:
                f.write(f"{p['post_id']}|{p['username']}|{p['title']}|{p['date']}|{p['category']}|{p['content']}\n")
        return redirect(url_for('dashboard'))
    return render_template('post_details.html', post=post)
@app.route('/user_profile')
def user_profile():
    '''Render the user profile page.'''
    return render_template('user_profile.html')
if __name__ == '__main__':
    app.run(port=5000)