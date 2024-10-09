'''
This is the main application file for the MotivationalQuotesApp. It handles routing for all frontend pages and manages file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)
DATA_DIR = 'data'
QUOTES_FILE = os.path.join(DATA_DIR, 'Quotes.txt')
USERS_FILE = os.path.join(DATA_DIR, 'Users.txt')
FAVORITES_FILE = os.path.join(DATA_DIR, 'Favorites.txt')
def ensure_data_files_exist():
    if not os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'w') as file:
            file.write("")  # Create an empty file
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            file.write("")  # Create an empty file
    if not os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'w') as file:
            file.write("")  # Create an empty file
def read_quotes():
    quotes = []
    with open(QUOTES_FILE, 'r') as file:
        for index, line in enumerate(file):
            quote, author = line.strip().split('|')
            quotes.append({'id': index, 'quote': quote, 'author': author})  # Include ID
    return quotes
def read_users():
    users = {}
    with open(USERS_FILE, 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users
def write_quote(quote, author):
    with open(QUOTES_FILE, 'a') as file:
        file.write(f"{quote}|{author}\n")
def delete_quote(quote_id):
    quotes = read_quotes()
    if any(q['id'] == quote_id for q in quotes):  # Check if ID exists
        quotes = [q for q in quotes if q['id'] != quote_id]  # Filter by ID
        # Reassign IDs
        for index, quote in enumerate(quotes):
            quote['id'] = index
        with open(QUOTES_FILE, 'w') as file:
            for q in quotes:
                file.write(f"{q['quote']}|{q['author']}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')
@app.route('/home')
def home():
    quotes = read_quotes()
    return render_template('home.html', quotes=quotes)
@app.route('/add_quote', methods=['GET', 'POST'])
def add_quote():
    if request.method == 'POST':
        quote = request.form['quote_input']
        author = request.form['author_input']
        write_quote(quote, author)
        return redirect(url_for('home'))
    return render_template('add_quote.html')
@app.route('/edit_quote/<int:quote_id>', methods=['GET', 'POST'])
def edit_quote(quote_id):
    quotes = read_quotes()
    if quote_id >= len(quotes):  # Check if ID is valid
        return redirect(url_for('home'))  # Redirect if invalid
    if request.method == 'POST':
        updated_quote = request.form['edit_quote_input']
        updated_author = request.form['edit_author_input']
        delete_quote(quote_id)  # Delete by ID
        write_quote(updated_quote, updated_author)
        return redirect(url_for('home'))
    return render_template('edit_quote.html', quote=quotes[quote_id])
@app.route('/delete_confirmation/<int:quote_id>')
def delete_confirmation(quote_id):
    quotes = read_quotes()
    if quote_id >= len(quotes):  # Check if ID is valid
        return redirect(url_for('home'))  # Redirect if invalid
    return render_template('delete_confirmation.html', quote=quotes[quote_id])
@app.route('/confirm_deletion/<int:quote_id>')
def confirm_deletion(quote_id):
    delete_quote(quote_id)  # Pass the ID directly
    return redirect(url_for('home'))
@app.route('/favorites')
def favorites():
    favorites = []
    with open(FAVORITES_FILE, 'r') as file:
        for line in file:
            username, quote, author = line.strip().split('|')
            favorites.append({'quote': quote, 'author': author})
    return render_template('favorites.html', favorites=favorites)
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    ensure_data_files_exist()  # Ensure data files exist before running the app
    app.run(port=5000)