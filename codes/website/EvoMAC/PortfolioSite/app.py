'''
This is the main application file for the PortfolioSite web application.
It handles routing for all frontend pages and manages file read/write operations
for user credentials, projects, blogs, and contacts.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data'
USER_FILE = os.path.join(DATA_DIR, 'users.txt')
PROJECT_FILE = os.path.join(DATA_DIR, 'projects.txt')
BLOG_FILE = os.path.join(DATA_DIR, 'blogs.txt')
CONTACT_FILE = os.path.join(DATA_DIR, 'contacts.txt')
def read_file(file_path):
    '''Reads the content of a file and returns a list of lines.'''
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        return file.readlines()
def write_file(file_path, data):
    '''Writes data to a file.'''
    with open(file_path, 'a') as file:
        file.write(data + '\n')
@app.route('/')
def login():
    '''Render the login page.'''
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def handle_login():
    '''Handle user login.'''
    username = request.form['login_username']
    password = request.form['login_password']
    users = read_file(USER_FILE)
    for user in users:
        stored_username, stored_password, _ = user.strip().split(',')
        if stored_username == username and stored_password == password:
            session['username'] = username
            return redirect(url_for('portfolio'))
    flash('Invalid username or password.')
    return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Handle user registration.'''
    if request.method == 'POST':
        email = request.form['reg_email']
        username = request.form['reg_username']
        password = request.form['reg_password']
        write_file(USER_FILE, f"{username},{password},{email}")
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    '''Render the user's portfolio page and handle project submissions.'''
    if request.method == 'POST':
        username = session['username']  # Get username from session
        project_link = request.form['new_project_link']
        project_description = request.form['new_project_description']
        write_file(PROJECT_FILE, f"{username},{project_link},{project_description}")
        flash('Project added successfully!')
    projects = read_file(PROJECT_FILE)
    return render_template('portfolio.html', projects=projects)
@app.route('/delete_project', methods=['POST'])
def delete_project():
    '''Handle project deletion.'''
    username = request.form['username']
    project_link = request.form['project_link']
    projects = read_file(PROJECT_FILE)
    if not any(project.startswith(username) and project_link in project for project in projects):
        flash('Project not found.')
        return redirect(url_for('portfolio'))
    updated_projects = [project for project in projects if not (project.startswith(username) and project_link in project)]
    with open(PROJECT_FILE, 'w') as file:
        file.writelines(updated_projects)
    flash('Project deleted successfully!')
    return redirect(url_for('portfolio'))
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    '''Render the user's blog page and handle blog submissions.'''
    if request.method == 'POST':
        username = session['username']  # Get username from session
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        write_file(BLOG_FILE, f"{username},{blog_title},{blog_content}")
        flash('Blog post published successfully!')
    blogs = read_file(BLOG_FILE)
    return render_template('blog.html', blogs=blogs)
@app.route('/delete_blog', methods=['POST'])
def delete_blog():
    '''Handle blog deletion.'''
    username = request.form['username']
    blog_title = request.form['blog_title']
    blogs = read_file(BLOG_FILE)
    if not any(blog.startswith(username) and blog_title in blog for blog in blogs):
        flash('Blog post not found.')
        return redirect(url_for('blog'))
    updated_blogs = [blog for blog in blogs if not (blog.startswith(username) and blog_title in blog)]
    with open(BLOG_FILE, 'w') as file:
        file.writelines(updated_blogs)
    flash('Blog post deleted successfully!')
    return redirect(url_for('blog'))
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    '''Render the contact page and handle contact form submissions.'''
    if request.method == 'POST':
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        message_content = request.form['contact_message']
        write_file(CONTACT_FILE, f"{contact_name},{contact_email},{message_content}")
        flash('Message sent successfully!')
    return render_template('contact.html')
if __name__ == '__main__':
    app.run(port=5000, debug=True)