'''
This is the main application file for the Online Library Management System.
It implements the backend logic for handling user authentication, book management,
and routing for all frontend pages.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
# File paths
BOOKS_FILE = 'data/books.txt'
USERS_FILE = 'data/users.txt'
# Helper functions
def read_books():
    """Read books from the books.txt file."""
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, 'r') as file:
        return [line.strip().split('|') for line in file.readlines()]
def read_users():
    """Read users from the users.txt file."""
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as file:
        return [line.strip().split('|') for line in file.readlines()]
def write_user(username, password):
    """Write a new user to the users.txt file."""
    with open(USERS_FILE, 'a') as file:
        file.write(f"{username}|{password}\n")
def authenticate_user(username, password):
    """Check if the provided username and password match any user in the users.txt file."""
    users = read_users()
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False
@app.route('/', methods=['GET', 'POST'])
def login():
    """Render the login page and handle user authentication."""
    if request.method == 'POST':
        username = request.form['login_username']
        password = request.form['login_password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['reg_username_input']
        password = request.form['reg_password_input']
        write_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html')
@app.route('/manage_books', methods=['GET', 'POST'])
def manage_books():
    """Render the manage books page and handle book addition."""
    if request.method == 'POST':
        title = request.form['add_book_title']
        author = request.form['add_book_author']
        isbn = request.form['add_book_isbn']
        with open(BOOKS_FILE, 'a') as file:
            file.write(f"{title}|{author}|{isbn}\n")
        return redirect(url_for('manage_books'))  # Redirect to the same page to see the updated list
    books = read_books()
    return render_template('manage_books.html', books=books)
@app.route('/manage_books/delete/<int:index>', methods=['DELETE'])
def delete_book(index):
    """Delete a book from the books.txt file."""
    books = read_books()
    if 0 <= index < len(books):
        del books[index]
        with open(BOOKS_FILE, 'w') as file:
            for book in books:
                file.write('|'.join(book) + '\n')
        return '', 204  # No content
    return '', 404  # Not found
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    """Render the manage users page and handle user addition."""
    if request.method == 'POST':
        username = request.form['add_user_username']
        password = request.form['add_user_password']
        write_user(username, password)  # Save the new user
        return redirect(url_for('manage_users'))  # Redirect to see the updated list
    users = read_users()
    return render_template('manage_users.html', users=users)
@app.route('/search_books')
def search_books():
    """Render the search books page."""
    return render_template('search_books.html')
@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return render_template('logout.html')
if __name__ == '__main__':
    app.run(port=5000)