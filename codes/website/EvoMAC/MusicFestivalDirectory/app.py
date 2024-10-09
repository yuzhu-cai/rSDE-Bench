'''
This is the main backend code file that handles the web application logic,
including user authentication, festival data management, and routing between different pages.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
# Function to ensure the data directory and files exist
def ensure_data_files():
    if not os.path.exists('data'):
        os.makedirs('data')  # Create the data directory if it doesn't exist
    if not os.path.isfile('data/users.txt'):
        with open('data/users.txt', 'w') as file:
            pass  # Create the file if it doesn't exist
    if not os.path.isfile('data/festivals.txt'):
        with open('data/festivals.txt', 'w') as file:
            pass  # Create the file if it doesn't exist
# Function to read users from the users.txt file
def read_users():
    users = {}
    ensure_data_files()  # Ensure data files exist
    with open('data/users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users
# Function to read festivals from the festivals.txt file
def read_festivals():
    festivals = []
    ensure_data_files()  # Ensure data files exist
    with open('data/festivals.txt', 'r') as file:
        for line in file:
            name, location, date, lineup = line.strip().split('|')
            festivals.append({'name': name, 'location': location, 'date': date, 'lineup': lineup})
    return festivals
# Function to write a new festival to the festivals.txt file
def write_festival(name, location, date, lineup):
    try:
        with open('data/festivals.txt', 'a') as file:
            file.write(f"{name}|{location}|{date}|{lineup}\n")
        flash('Festival added successfully!', 'success')  # Add success message
    except Exception as e:
        print(f"Error writing to festivals.txt: {e}")
        flash('An error occurred while adding the festival. Please try again.', 'error')
@app.route('/')
def login():
    return render_template('login.html', error_message='')  # Always render error_message
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = read_users()
    if username in users and users[username] == password:
        return redirect(url_for('festival_list'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))
@app.route('/festival_list')
def festival_list():
    festivals = read_festivals()
    return render_template('festival_list.html', festivals=festivals)
@app.route('/festival_details/<int:index>')
def festival_details(index):
    festivals = read_festivals()
    if index < len(festivals):
        festival = festivals[index]
        return render_template('festival_details.html', festival=festival)
    else:
        return redirect(url_for('festival_list'))
@app.route('/add_festival', methods=['GET', 'POST'])
def add_festival():
    if request.method == 'POST':
        name = request.form['add_festival_name']
        location = request.form['add_festival_location']
        date = request.form['add_festival_date']
        lineup = request.form['add_festival_lineup']
        write_festival(name, location, date, lineup)
        return redirect(url_for('festival_list'))
    return render_template('add_festival.html', admin_message='')  # Always render admin_message
if __name__ == '__main__':
    app.run(port=5000)