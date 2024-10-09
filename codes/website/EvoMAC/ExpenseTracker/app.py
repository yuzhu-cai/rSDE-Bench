'''
This is the main application file for the ExpenseTracker web application. 
It sets up the Flask web server, defines routes for each page, and handles 
file read and write operations for user authentication, expenses, and income.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import uuid  # Importing uuid for unique identifier generation
import logging  # Importing logging for warning messages
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
# Set up logging
logging.basicConfig(level=logging.WARNING)
# Define the path for data files
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
EXPENSES_FILE = os.path.join(DATA_DIR, 'expenses.txt')
INCOME_FILE = os.path.join(DATA_DIR, 'income.txt')
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Logic to check username and password against users.txt
        with open(USERS_FILE, 'r') as file:
            users = file.readlines()
            for user in users:
                user_info = user.strip().split(':')
                if user_info[0] == username and user_info[1] == password:
                    return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Logic to save new user to users.txt
        with open(USERS_FILE, 'a') as file:
            file.write(f"{username}:{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense_name = request.form['expense-name']
        expense_amount = request.form['expense-amount']
        expense_date = request.form['expense-date']
        expense_category = request.form['expense-category']
        expense_id = str(uuid.uuid4())  # Generate a unique identifier for the expense
        # Logic to save expense to expenses.txt
        with open(EXPENSES_FILE, 'a') as file:
            file.write(f"{expense_id}|{expense_date}|{expense_name}|{expense_amount}|{expense_category}\n")
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')
@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        income_amount = request.form['income-amount']
        income_date = request.form['income-date']
        income_category = request.form['income-category']
        # Logic to save income to income.txt
        with open(INCOME_FILE, 'a') as file:
            file.write(f"{income_date}|{income_amount}|{income_category}\n")
        return redirect(url_for('dashboard'))
    return render_template('add_income.html')
@app.route('/view_expenses')
def view_expenses():
    expenses = []
    with open(EXPENSES_FILE, 'r') as file:
        for line in file:
            fields = line.strip().split('|')
            if len(fields) == 5:  # Check if the line has the expected number of fields
                expense_id, date, name, amount, category = fields
                expenses.append({'id': expense_id, 'date': date, 'name': name, 'amount': amount, 'category': category})
            else:
                logging.warning(f"Malformed line in expenses file: {line.strip()}")  # Log warning for malformed line
    return render_template('view_expenses.html', expenses=expenses)
@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    expense_id = request.form['expense_id']
    expenses = []
    # Read existing expenses
    with open(EXPENSES_FILE, 'r') as file:
        expenses = file.readlines()
    # Check if the expense ID exists
    expense_found = False
    with open(EXPENSES_FILE, 'w') as file:
        for expense in expenses:
            fields = expense.strip().split('|')
            if len(fields) == 5:
                if fields[0] == expense_id:  # If the ID matches, mark as found
                    expense_found = True
                    continue  # Skip writing this expense (delete it)
                file.write(expense)  # Write back the other expenses
            else:
                logging.warning(f"Malformed line in expenses file: {expense.strip()}")  # Log warning for malformed line
    if not expense_found:
        flash('Expense ID does not exist. No expense was deleted.')  # Inform user of non-existent ID
        logging.warning(f"Attempted to delete non-existent expense ID: {expense_id}")
    return redirect(url_for('view_expenses'))
@app.route('/reports')
def reports():
    return render_template('reports.html')
if __name__ == '__main__':
    app.run(port=5000)