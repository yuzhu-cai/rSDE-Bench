'''
This file implements the backend for the PersonalFinanceBlog web application.
It handles routing for all frontend pages and manages file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
POSTS_FILE = os.path.join(DATA_DIR, 'posts.txt')
def read_users():
    '''Reads user data from the users.txt file.'''
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                username, password, occupation = line.strip().split(':')
                users[username] = (password, occupation)
    return users
def write_user(username, password, occupation):
    '''Writes a new user to the users.txt file.'''
    with open(USERS_FILE, 'a') as file:
        file.write(f"{username}:{password}:{occupation}\n")
def read_posts():
    '''Reads blog post data from the posts.txt file.'''
    posts = []
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as file:
            for line in file:
                post_id, username, title, date, category, content = line.strip().split('|')
                posts.append({
                    'id': post_id,
                    'username': username,
                    'title': title,
                    'date': date,
                    'category': category,
                    'content': content
                })
    return posts
def write_post(username, title, date, category, content):
    '''Writes a new blog post to the posts.txt file.'''
    posts = read_posts()
    post_id = len(posts) + 1
    with open(POSTS_FILE, 'a') as file:
        file.write(f"{post_id}|{username}|{title}|{date}|{category}|{content}\n")
def update_post(post_id, title, date, category, content):
    '''Updates an existing blog post in the posts.txt file.'''
    posts = read_posts()
    with open(POSTS_FILE, 'w') as file:
        for post in posts:
            if post['id'] == str(post_id):
                file.write(f"{post_id}|{post['username']}|{title}|{date}|{category}|{content}\n")
            else:
                file.write(f"{post['id']}|{post['username']}|{post['title']}|{post['date']}|{post['category']}|{post['content']}\n")
def delete_post_from_file(post_id):
    '''Deletes a blog post from the posts.txt file.'''
    posts = read_posts()
    with open(POSTS_FILE, 'w') as file:
        for post in posts:
            if post['id'] != str(post_id):
                file.write(f"{post['id']}|{post['username']}|{post['title']}|{post['date']}|{post['category']}|{post['content']}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    '''Render the login page.'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username][0] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        flash('Invalid credentials. Please try again.')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Handle user registration.'''
    if request.method == 'POST':
        username = request.form['register_username_field']
        password = request.form['register_password_field']
        confirm_password = request.form['confirm_password_field']
        occupation = request.form['occupation_field']
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return render_template('register.html')
        # Check if username already exists
        users = read_users()
        if username in users:
            flash('Username already taken. Please choose a different one.')
            return render_template('register.html')
        write_user(username, password, occupation)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
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
        username = session.get('username')  # Retrieve username from session
        if not username:
            flash('You must be logged in to add a post.')
            return redirect(url_for('login'))
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
@app.route('/category/<category_name>')
def category_post(category_name):
    '''Render the category post page.'''
    posts = [post for post in read_posts() if post['category'] == category_name]
    return render_template('category_post.html', posts=posts)
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    '''Render the post details page.'''
    posts = read_posts()
    post = next((p for p in posts if int(p['id']) == post_id), None)
    if request.method == 'POST':
        title = request.form['post_title_field']
        date = request.form['post_date']
        category = request.form['post_category']
        content = request.form['post_content']
        update_post(post_id, title, date, category, content)
        return redirect(url_for('dashboard'))
    return render_template('post_details.html', post=post)
@app.route('/user_profile')
def user_profile():
    '''Render the user profile page.'''
    username = session.get('username')
    if not username:
        flash('You must be logged in to view your profile.')
        return redirect(url_for('login'))
    users = read_users()
    occupation = users[username][1] if username in users else ''
    return render_template('user_profile.html', username=username, occupation=occupation)
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post_route(post_id):
    '''Handle the deletion of a blog post.'''
    delete_post_from_file(post_id)  # Updated function name
    return {'status': 'success', 'message': 'Post deleted successfully.'}, 200  # Return JSON response
if __name__ == '__main__':
    app.run(port=5000)