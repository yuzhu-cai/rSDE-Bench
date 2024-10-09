'''
This is the main backend application for the OnlineCulturalExchange web application.
It implements routing for all frontend pages and handles file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key for production
# File paths
USER_DATA_FILE = 'data/users.txt'
EXCHANGE_DATA_FILE = 'data/exchanges.txt'
CONTACT_DATA_FILE = 'data/contacts.txt'
def read_users():
    '''Reads user data from the users.txt file.'''
    users = {}
    with open(USER_DATA_FILE, 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            users[username] = password
    return users
def read_exchanges():
    '''Reads cultural exchange submissions from the exchanges.txt file.'''
    exchanges = []
    with open(EXCHANGE_DATA_FILE, 'r') as file:
        for line in file:
            title, description = line.strip().split(',')
            exchanges.append({'title': title, 'description': description})
    return exchanges
def write_exchange(title, description):
    '''Writes a new cultural exchange submission to the exchanges.txt file.'''
    with open(EXCHANGE_DATA_FILE, 'a') as file:
        file.write(f"{title},{description}\n")
def write_contact(name, email, message):
    '''Writes a contact message to the contacts.txt file.'''
    with open(CONTACT_DATA_FILE, 'a') as file:
        file.write(f"{name},{email},{message}\n")
@app.route('/', methods=['GET', 'POST'])
def login():
    '''Render the login page and handle login logic.'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))  # Redirect to home page on successful login
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')
@app.route('/home')
def home():
    '''Render the home page.'''
    return render_template('home.html', culture_list=read_exchanges())
@app.route('/cultural_exchange', methods=['GET', 'POST'])
def cultural_exchange():
    '''Handle cultural exchange submissions.'''
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        write_exchange(title, description)
        flash('Cultural exchange submitted successfully!')
        return redirect(url_for('cultural_exchange'))
    exchanges = read_exchanges()
    return render_template('cultural_exchange.html', exchange_list=exchanges)
@app.route('/profile')
def profile():
    '''Render the profile page.'''
    return render_template('profile.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    '''Handle contact inquiries.'''
    if request.method == 'POST':
        name = request.form['contact-name']
        email = request.form['contact-email']
        message = request.form['contact-message']
        write_contact(name, email, message)
        flash('Message sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')
if __name__ == '__main__':
    app.run(port=5000, debug=True)