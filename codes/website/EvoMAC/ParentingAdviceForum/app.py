'''
This is the main application file for the ParentingAdviceForum web application.
It implements routing for all frontend pages and handles file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
# Function to check user credentials
def check_user_credentials(username, password):
    if not os.path.exists('data/users.txt'):
        return False
    with open('data/users.txt', 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if stored_username == username and stored_password == password:
                return True
    return False
# Function to get the next thread ID
def get_next_thread_id():
    if not os.path.exists('data/threads.txt'):
        return 1
    with open('data/threads.txt', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        last_thread_id = int(last_line.split(',')[0])
        return last_thread_id + 1
# Function to get the next comment ID
def get_next_comment_id():
    if not os.path.exists('data/comments.txt'):
        return 1
    with open('data/comments.txt', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        last_comment_id = int(last_line.split(',')[0])
        return last_comment_id + 1
# Function to get the next advice ID
def get_next_advice_id():
    if not os.path.exists('data/advice_posts.txt'):
        return 1
    with open('data/advice_posts.txt', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        last_advice_id = int(last_line.split(',')[0])
        return last_advice_id + 1
# Function to fetch threads from threads.txt
def fetch_threads():
    threads = []
    if os.path.exists('data/threads.txt'):
        with open('data/threads.txt', 'r') as file:
            for line in file:
                thread_id, thread_title, thread_content, username = line.strip().split(',')
                threads.append({
                    'thread_id': int(thread_id),
                    'thread_title': thread_title,
                    'thread_content': thread_content,
                    'username': username
                })
    return threads
# Function to fetch recent posts
def fetch_recent_posts():
    posts = []
    if os.path.exists('data/threads.txt'):
        with open('data/threads.txt', 'r') as file:
            for line in file:
                thread_id, thread_title, thread_content, username = line.strip().split(',')
                posts.append({
                    'thread_id': int(thread_id),
                    'thread_title': thread_title,
                    'thread_content': thread_content,
                    'username': username
                })
    return posts[-5:]  # Return the last 5 posts for recent posts section
# Function to fetch comments for a specific thread
def fetch_comments(thread_id):
    comments = []
    if os.path.exists('data/comments.txt'):
        with open('data/comments.txt', 'r') as file:
            for line in file:
                comment_id, comment_thread_id, comment_content, username = line.strip().split(',')
                if int(comment_thread_id) == thread_id:
                    comments.append({
                        'comment_id': int(comment_id),
                        'comment_content': comment_content,
                        'username': username
                    })
    return comments
# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user_credentials(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    return render_template('login.html')
# Route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username already exists
        if os.path.exists('data/users.txt'):
            with open('data/users.txt', 'r') as file:
                for line in file:
                    stored_username, _ = line.strip().split(',')
                    if stored_username == username:
                        return render_template('register.html', error='Username already exists. Please choose a different one.')
        with open('data/users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')
# Route for the home page
@app.route('/home')
def home():
    recent_posts = fetch_recent_posts()  # Fetch recent posts
    return render_template('home.html', recent_posts=recent_posts)  # Pass recent posts to the template
# Route for the forum page
@app.route('/forum')
def forum():
    threads = fetch_threads()  # Fetch threads from the data file
    return render_template('forum.html', threads=threads)  # Pass threads to the template
# Route for creating a new thread
@app.route('/create_thread', methods=['POST'])
def create_thread():
    thread_title = request.form['thread_title']
    thread_content = request.form['thread_content']
    username = session.get('username')
    # Logic to save the thread to the threads.txt file
    with open('data/threads.txt', 'a') as file:
        thread_id = get_next_thread_id()
        file.write(f"{thread_id},{thread_title},{thread_content},{username}\n")
    return redirect(url_for('forum'))
# Route for viewing a thread
@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    # Logic to fetch and display the thread based on thread_id
    threads = fetch_threads()
    thread = next((t for t in threads if t['thread_id'] == thread_id), None)
    comments = fetch_comments(thread_id)
    return render_template('view_thread.html', thread={'title': thread['thread_title'], 'content': thread['thread_content']}, comments=comments, thread_id=thread_id)
# Route for submitting a comment
@app.route('/submit_comment/<int:thread_id>', methods=['POST'])
def submit_comment(thread_id):
    comment_content = request.form['comment_content']
    username = session.get('username')
    # Logic to save the comment to the comments.txt file
    with open('data/comments.txt', 'a') as file:
        comment_id = get_next_comment_id()
        file.write(f"{comment_id},{thread_id},{comment_content},{username}\n")
    return redirect(url_for('view_thread', thread_id=thread_id))
# Route for posting advice
@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        advice_title = request.form['advice_title']
        advice_content = request.form['advice_content']
        username = session.get('username')
        # Logic to save the advice to the advice_posts.txt file
        with open('data/advice_posts.txt', 'a') as file:
            advice_id = get_next_advice_id()
            file.write(f"{advice_id},{advice_title},{advice_content},{username}\n")
        return redirect(url_for('home'))
    return render_template('post_advice.html')
# Route for my account page
@app.route('/my_account')
def my_account():
    username = session.get('username')
    return render_template('my_account.html', username=username)  # Pass username to the template
# Route for updating profile
@app.route('/update_profile', methods=['POST'])
def update_profile():
    new_username = request.form['username']
    old_username = session.get('username')
    # Update the username in users.txt
    users = []
    with open('data/users.txt', 'r') as file:
        for line in file:
            if line.startswith(old_username + ','):
                users.append(f"{new_username},{line.strip().split(',')[1]}\n")
            else:
                users.append(line)
    with open('data/users.txt', 'w') as file:
        file.writelines(users)
    session['username'] = new_username  # Update session username
    return redirect(url_for('my_account'))
# Route for deleting account
@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    # Remove the user from users.txt
    users = []
    with open('data/users.txt', 'r') as file:
        for line in file:
            if not line.startswith(username + ','):
                users.append(line)
    with open('data/users.txt', 'w') as file:
        file.writelines(users)
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))
# Route for contact us page
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_message = request.form['contact_message']
        with open('data/contact.txt', 'a') as file:
            file.write(f"{contact_name},{contact_email},{contact_message}\n")
        flash('Message sent successfully!', 'success')  # Use flash to store the message
        return redirect(url_for('contact_us'))  # Redirect to the same page to show the message
    return render_template('contact_us.html')
if __name__ == '__main__':
    app.run(port=5000)