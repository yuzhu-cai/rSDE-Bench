'''
This is the main backend application for the GreenLivingGuide web application.
It implements routing for all frontend pages and handles file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages
# Helper functions for file operations
def read_users():
    try:
        with open('data/users.txt', 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
def write_user(username, password):
    users = read_users()  # Read existing users
    if any(user[0] == username for user in users):
        return False  # Indicate that the username already exists
    with open('data/users.txt', 'a') as file:
        file.write(f"{username},{password}\n")
    return True  # Indicate successful write
def read_tips():
    try:
        with open('data/tips.txt', 'r') as file:
            return [line.strip().split(':') for line in file.readlines()]
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
def read_articles():
    try:
        with open('data/articles.txt', 'r') as file:
            return [line.strip().split(':') for line in file.readlines()]
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
def read_community_posts():
    try:
        with open('data/community_posts.txt', 'r') as file:
            return [line.strip().split(':') for line in file.readlines()]
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if any(user[0] == username and user[1] == password for user in users):
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password."
    return render_template('login.html', error=error)
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check for empty username or password
        if not username or not password:
            error = "Username and password cannot be empty."
        elif write_user(username, password):
            flash("Registration successful! You can now log in.")  # Add a success message
            return redirect(url_for('login'))  # Redirect to login page
        else:
            error = "Username already exists."
    return render_template('register.html', error=error)
@app.route('/home')
def home():
    tips = read_tips()
    articles = read_articles()
    return render_template('home.html', tips=tips, articles=articles)
@app.route('/tips')
def tips():
    tips = read_tips()
    if not tips:  # Check if tips data is empty
        flash("No tips available.")  # Flash message if no tips are found
    return render_template('tips.html', tips=tips)
@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    tip_title = request.form['tip_title']
    tip_description = request.form['tip_description']
    with open('data/tips.txt', 'a') as file:
        file.write(f"{tip_title}:{tip_description}\n")
    flash("Tip submitted successfully!")  # Store the success message
    return redirect(url_for('tips'))
@app.route('/articles')
def articles():
    articles = read_articles()
    return render_template('articles.html', articles=articles)
@app.route('/submit_article', methods=['POST'])
def submit_article():
    article_title = request.form['article_title']
    article_content = request.form['article_content']
    with open('data/articles.txt', 'a') as file:
        file.write(f"{article_title}:{article_content}\n")
    flash("Article submitted successfully!")  # Store the success message
    return redirect(url_for('articles'))
@app.route('/community')
def community():
    posts = read_community_posts()
    return render_template('community.html', posts=posts)
@app.route('/submit_post', methods=['POST'])
def submit_post():
    post_title = request.form['post_title']
    post_content = request.form['post_content']
    with open('data/community_posts.txt', 'a') as file:
        file.write(f"{post_title}:{post_content}\n")
    flash("Post submitted successfully!")  # Store the success message
    return redirect(url_for('community'))
if __name__ == '__main__':
    app.run(port=5000)