'''
This file contains the backend code for the CharitableGivingPlatform web application.
It handles routing for the login, dashboard, and charity details pages, as well as user authentication
and data management using local text files.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
# Define the path for data files
DATA_DIR = 'data/'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
CONTRIBUTIONS_FILE = os.path.join(DATA_DIR, 'contributions.txt')
CHARITIES_FILE = os.path.join(DATA_DIR, 'charities.txt')
@app.route('/')
def login():
    '''
    Render the login page.
    '''
    return render_template('login.html')
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    '''
    Render the dashboard page and handle user login.
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."
    if 'username' in session:
        charities = load_charities()
        contributions = load_contributions(session['username'])
        return render_template('dashboard.html', charities=charities, contributions=contributions)
    return redirect(url_for('login'))
@app.route('/charity/<charity_name>')
def charity_details(charity_name):
    '''
    Render the charity details page for a specific charity.
    '''
    charity_info = get_charity_info(charity_name)
    return render_template('charity_details.html', charity=charity_info)
@app.route('/logout')
def logout():
    '''
    Log the user out and redirect to the login page.
    '''
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/donate', methods=['POST'])
def donate():
    '''
    Record a donation made by the user.
    '''
    if 'username' in session:
        username = session['username']
        charity_name = request.form['charity_name']
        amount = request.form['amount']
        with open(CONTRIBUTIONS_FILE, 'a') as file:
            file.write(f"{username},{charity_name},{amount}\n")
        return redirect(url_for('charity_details', charity_name=charity_name))
    return redirect(url_for('login'))
def authenticate_user(username, password):
    '''
    Check if the provided username and password match any user in the users file.
    '''
    with open(USERS_FILE, 'r') as file:
        for line in file:
            user_data = line.strip().split(',')
            if user_data[0] == username and user_data[1] == password:
                return True
    return False
def load_charities():
    '''
    Load the list of charities from the charities file.
    '''
    charities = []
    with open(CHARITIES_FILE, 'r') as file:
        for line in file:
            charity_data = line.strip().split(',')
            charities.append({'name': charity_data[0], 'description': charity_data[1]})
    return charities
def load_contributions(username):
    '''
    Load the contribution history for the specified user.
    '''
    contributions = []
    with open(CONTRIBUTIONS_FILE, 'r') as file:
        for line in file:
            contribution_data = line.strip().split(',')
            if contribution_data[0] == username:
                contributions.append({'charity': contribution_data[1], 'amount': contribution_data[2]})
    return contributions
def get_charity_info(charity_name):
    '''
    Get detailed information about a specific charity.
    '''
    with open(CHARITIES_FILE, 'r') as file:
        for line in file:
            charity_data = line.strip().split(',')
            if charity_data[0] == charity_name:
                return {'name': charity_data[0], 'description': charity_data[1]}
    return None
if __name__ == '__main__':
    app.run(port=5000)