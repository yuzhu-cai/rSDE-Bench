'''
Main Python file containing the backend logic for the Fitness Equipment Rental web application, handling user authentication, data management, and routing between different pages.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
# File paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
EQUIPMENT_FILE = os.path.join(DATA_DIR, 'equipment.txt')
RENTALS_FILE = os.path.join(DATA_DIR, 'rentals.txt')
RETURNS_FILE = os.path.join(DATA_DIR, 'returns.txt')
def read_users():
    users = []
    with open(USERS_FILE, 'r') as file:
        for line in file.readlines():  # Read all lines including the header
            if line.strip():  # Check if the line is not empty
                username, password, full_name, email = line.strip().split(',')
                users.append({'username': username, 'password': password, 'full_name': full_name, 'email': email})
    return users
def read_equipment():
    equipment = []
    with open(EQUIPMENT_FILE, 'r') as file:
        for line in file.readlines():  # Read all lines including the header
            if line.strip():  # Check if the line is not empty
                equipment_id, name, description, availability, rental_price = line.strip().split(',')
                equipment.append({'equipment_id': equipment_id, 'name': name, 'description': description, 'availability': int(availability), 'rental_price': float(rental_price)})
    return equipment
def read_rentals():
    rentals = []
    with open(RENTALS_FILE, 'r') as file:
        for line in file.readlines():  # Read all lines including the header
            if line.strip():  # Check if the line is not empty
                rental_id, username, equipment_id, rental_duration, start_date, status = line.strip().split(',')
                rentals.append({'rental_id': rental_id, 'username': username, 'equipment_id': equipment_id, 'rental_duration': int(rental_duration), 'start_date': start_date, 'status': status})
    return rentals
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['name']
        email = request.form['email']
        with open(USERS_FILE, 'a') as file:
            file.write(f"{username},{password},{full_name},{email}\n")
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/home')
def home():
    equipment = read_equipment()
    return render_template('home.html', equipment=equipment)
@app.route('/equipment')
def equipment():
    equipment = read_equipment()
    return render_template('equipment.html', equipment=equipment)
@app.route('/rental_form', methods=['GET', 'POST'])
def rental_form():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    equipment_id = request.args.get('equipment_id')  # Get equipment_id from URL parameters
    if not equipment_id:
        return redirect(url_for('equipment'))  # Redirect to equipment page if no equipment_id is provided
    if request.method == 'POST':
        rental_duration = request.form['rental_duration']
        username = session.get('username')
        rental_id = str(int(datetime.now().timestamp()))  # Simple rental ID based on timestamp
        start_date = datetime.now().strftime('%Y-%m-%d')
        status = 'active'
        with open(RENTALS_FILE, 'a') as file:
            file.write(f"{rental_id},{username},{equipment_id},{rental_duration},{start_date},{status}\n")
        return redirect(url_for('my_rentals'))
    return render_template('rental_form.html', equipment_id=equipment_id)  # Pass equipment_id to the template
@app.route('/my_rentals')
def my_rentals():
    username = session.get('username')
    rentals = read_rentals()
    user_rentals = [rental for rental in rentals if rental['username'] == username]
    return render_template('my_rentals.html', rentals=user_rentals)
@app.route('/return_equipment', methods=['GET', 'POST'])
def return_equipment():
    if request.method == 'POST':
        rental_id = request.form['rental_id']
        date_returned = datetime.now().strftime('%Y-%m-%d')
        with open(RETURNS_FILE, 'a') as file:
            file.write(f"{str(int(datetime.now().timestamp()))},{rental_id},{date_returned}\n")
        return redirect(url_for('my_rentals'))
    return render_template('return_equipment.html')
@app.route('/help')
def help_page():
    return render_template('help.html')
if __name__ == '__main__':
    app.run(port=5000)