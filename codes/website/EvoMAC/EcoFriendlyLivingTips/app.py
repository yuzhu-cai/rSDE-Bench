'''
Main Python file for the EcoFriendlyLivingTips web application backend.
Handles routing for all frontend pages and file operations for user data, tips, resources, forum posts, and contact messages.
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                return redirect(url_for('home'))  # Redirect to home page on successful login
        return "Invalid username or password", 401  # Handle invalid login
    return render_template('login.html')
# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        write_user(username, password)
        return redirect(url_for('login'))  # Redirect to login page after registration
    return render_template('register.html')
# Route for the home page
@app.route('/home')
def home():
    return render_template('home.html')
# Route for the eco-friendly tips page
@app.route('/eco-friendly-tips', methods=['GET', 'POST'])
def eco_friendly_tips():
    if request.method == 'POST':
        tip = request.form['tip']
        write_tip(tip)
    tips = read_tips()
    return render_template('eco_friendly_tips.html', tips=tips)
# Route for the resources page
@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        resource = request.form['resource']
        write_resource(resource)
    resources = read_resources()
    return render_template('resources.html', resources=resources)
# Route for the community forum page
@app.route('/community-forum', methods=['GET', 'POST'])
def community_forum():
    if request.method == 'POST':
        username = request.form['username']  # Assuming username is obtained from session or similar
        post_content = request.form['post_content']
        write_forum_post(username, post_content)
    posts = read_forum_posts()
    return render_template('community_forum.html', posts=posts)
# Route for the user profile page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        # Update user logic here (not implemented in this example)
    return render_template('profile.html', username='CurrentUsername')  # Replace with actual username
# Route for the contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        write_contact_message(name, email, message)
    return render_template('contact.html')
# Function to read user data from the file
def read_users():
    with open('data/users.txt', 'r') as file:
        users = file.readlines()
    return [user.strip().split(',') for user in users]
# Function to write user data to the file
def write_user(username, password):
    with open('data/users.txt', 'a') as file:
        file.write(f"{username},{password}\n")
# Function to read tips from the file
def read_tips():
    with open('data/tips.txt', 'r') as file:
        tips = file.readlines()
    return [tip.strip() for tip in tips]
# Function to write a tip to the file
def write_tip(tip):
    with open('data/tips.txt', 'a') as file:
        file.write(f"{tip}\n")
# Function to read resources from the file
def read_resources():
    with open('data/resources.txt', 'r') as file:
        resources = file.readlines()
    return [resource.strip() for resource in resources]
# Function to write a resource to the file
def write_resource(resource):
    with open('data/resources.txt', 'a') as file:
        file.write(f"{resource}\n")
# Function to read forum posts from the file
def read_forum_posts():
    with open('data/forum_posts.txt', 'r') as file:
        posts = file.readlines()
    return [post.strip().split(',') for post in posts]
# Function to write a forum post to the file
def write_forum_post(username, post_content):
    with open('data/forum_posts.txt', 'a') as file:
        file.write(f"{username},{post_content}\n")
# Function to read contact messages from the file
def read_contact_messages():
    with open('data/contact_messages.txt', 'r') as file:
        messages = file.readlines()
    return [message.strip().split(',') for message in messages]
# Function to write a contact message to the file
def write_contact_message(name, email, message):
    with open('data/contact_messages.txt', 'a') as file:
        file.write(f"{name},{email},{message}\n")
if __name__ == '__main__':
    app.run(port=5000)