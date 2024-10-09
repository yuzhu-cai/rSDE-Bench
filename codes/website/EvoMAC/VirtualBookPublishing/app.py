'''
This file implements the backend code for the VirtualBookPublishing web application.
It handles routing for all frontend pages and manages file read/write operations for user and book data.
'''
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
# File paths
USER_DATA_FILE = 'data/users.txt'
BOOK_DATA_FILE = 'data/books.txt'
def read_users():
    '''Reads user data from the users file.'''
    users = {}
    with open(USER_DATA_FILE, 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users
def write_user(username, password):
    '''Writes a new user to the users file if the username does not already exist.'''
    users = read_users()  # Read existing users
    if username in users:
        return False  # Indicate that the username already exists
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username}|{password}\n")
    return True  # Indicate successful write
def read_books():
    '''Reads book data from the books file.'''
    books = []
    with open(BOOK_DATA_FILE, 'r') as file:
        for line in file:
            title, author, content = line.strip().split('|')
            books.append({'title': title, 'author': author, 'content': content})
    return books
def write_book(title, author, content):
    '''Writes a new book to the books file.'''
    with open(BOOK_DATA_FILE, 'a') as file:
        file.write(f"{title}|{author}|{content}\n")
@app.route('/', methods=['GET', 'POST'])
def login_page():
    '''Renders the login page and handles user login.'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard_page'))
    return render_template('login.html')
@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    '''Handles user registration.'''
    if request.method == 'POST':
        username = request.form['regUsername']
        password = request.form['regPassword']
        if write_user(username, password):
            return redirect(url_for('login_page'))
        else:
            return render_template('registration.html', error="Username already exists.")  # Show error message
    return render_template('registration.html')
@app.route('/dashboard')
def dashboard_page():
    '''Renders the dashboard page.'''
    return render_template('dashboard.html')
@app.route('/create_book', methods=['GET', 'POST'])
def create_book_page():
    '''Handles book creation.'''
    if request.method == 'POST':
        title = request.form['bookTitle']
        author = request.form['bookAuthor']
        content = request.form['bookContent']
        write_book(title, author, content)
        return redirect(url_for('my_books_page'))
    return render_template('create_book.html')
@app.route('/my_books')
def my_books_page():
    '''Renders the my books page.'''
    books = read_books()
    return render_template('my_books.html', books=books)
@app.route('/book_details/<int:index>')
def book_details_page(index):
    '''Renders the book details page for a specific book.'''
    books = read_books()
    book = books[index]
    return render_template('book_details.html', book=book)
@app.route('/about')
def about_page():
    '''Renders the about page.'''
    return render_template('about.html')
@app.route('/delete_book', methods=['POST'])
def delete_book():
    '''Handles book deletion.'''
    title = request.form['title']
    books = read_books()
    books = [book for book in books if book['title'] != title]  # Filter out the deleted book
    with open(BOOK_DATA_FILE, 'w') as file:
        for book in books:
            file.write(f"{book['title']}|{book['author']}|{book['content']}\n")
    return redirect(url_for('my_books_page'))
if __name__ == '__main__':
    app.run(port=5000)