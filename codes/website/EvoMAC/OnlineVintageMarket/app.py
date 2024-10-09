'''
This file implements the backend logic for the OnlineVintageMarket web application.
It handles routing for the login, home, listing, and item details pages, as well as user authentication and data management.
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
# Function to read users from the users.txt file
def read_users():
    users = {}
    with open('data/users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            users[username] = password
    return users
# Function to read listings from the listings.txt file
def read_listings():
    listings = []
    with open('data/listings.txt', 'r') as file:
        for line in file:
            item_name, item_description, item_price = line.strip().split(',')
            listings.append({
                'name': item_name,
                'description': item_description,
                'price': item_price
            })
    return listings
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:  # Check if user is logged in
        flash("You need to log in to access this page.", "warning")  # Add this line
        return redirect(url_for('login'))  # Redirect to login if not logged in
    listings = read_listings()  # Read all listings
    search_results = []
    # Handle search functionality
    search_query = request.args.get('search')
    if search_query:
        search_results = [item for item in listings if search_query.lower() in item['name'].lower()]
    return render_template('home.html', listings=listings, search_results=search_results)  # Pass search results to template
@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        item_name = request.form['item-name']
        item_description = request.form['item-description']
        item_price = request.form['item-price']
        with open('data/listings.txt', 'a') as file:
            file.write(f"{item_name},{item_description},{item_price}\n")
        return redirect(url_for('home'))
    return render_template('listing.html')
@app.route('/item/<int:item_id>')
def item_details(item_id):
    listings = read_listings()
    if 0 <= item_id < len(listings):
        item = listings[item_id]
        return render_template('item_details.html', item=item)
    return "Item not found", 404
if __name__ == '__main__':
    app.run(port=5000)