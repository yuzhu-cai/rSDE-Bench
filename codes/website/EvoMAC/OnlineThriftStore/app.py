'''
This is the main application file for the OnlineThriftStore web application.
It implements the backend functionality using Flask, including routing for all frontend pages,
and handling file read/write operations for user data, item listings, shopping carts, and sold items.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
DATA_DIR = 'data'
# Helper functions for file operations
def read_users():
    users = {}
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users[username] = password
    return users
def write_user(username, password):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'a') as f:
        f.write(f"{username}:{password}\n")
def read_items():
    items = []
    with open(os.path.join(DATA_DIR, 'on_sale.txt'), 'r') as f:
        for line in f:
            title, description, price, seller_username = line.strip().split('|')
            items.append({
                'title': title,
                'description': description,
                'price': price,
                'seller_username': seller_username
            })
    return items
def write_item(title, description, price, seller_username):
    with open(os.path.join(DATA_DIR, 'on_sale.txt'), 'a') as f:
        f.write(f"{title}|{description}|{price}|{seller_username}\n")
def read_cart(username):
    cart_items = []
    with open(os.path.join(DATA_DIR, 'carts.txt'), 'r') as f:
        for line in f:
            user, item_title = line.strip().split('|')
            if user == username:
                cart_items.append(item_title)
    return cart_items
def write_cart(username, item_title):
    # Read existing cart items
    existing_cart = read_cart(username)
    if item_title not in existing_cart:  # Check for duplicates
        with open(os.path.join(DATA_DIR, 'carts.txt'), 'a') as f:
            f.write(f"{username}|{item_title}\n")
def read_sold_items():
    sold_items = []
    with open(os.path.join(DATA_DIR, 'sold.txt'), 'r') as f:
        for line in f:
            buyer_username, title, description, price, seller_username = line.strip().split('|')
            sold_items.append({
                'title': title,
                'buyer_username': buyer_username,
                'description': description,
                'price': price,
                'seller_username': seller_username
            })
    return sold_items
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['register_username_field']
        password = request.form['register_password_field']
        confirm_password = request.form['confirm_password_field']
        if password == confirm_password:
            write_user(username, password)
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Passwords do not match.')
    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    items = read_items()
    return render_template('dashboard.html', items=items)
@app.route('/item/<title>')
def item_details(title):
    items = read_items()
    sold_items = read_sold_items()  # Read sold items here
    item = next((item for item in items if item['title'] == title), None)
    if item is None:
        return render_template('item_not_found.html', title=title)  # Handle item not found
    item_status = 'on_sale' if item['title'] not in [sold_item['title'] for sold_item in sold_items] else 'sold'
    return render_template('item_details.html', item=item, item_status=item_status)
@app.route('/shopping_cart')
def shopping_cart():
    username = session.get('username')
    cart_items = read_cart(username)
    item_details = read_items()  # Read items to get details for cart items
    return render_template('shopping_cart.html', cart_items=cart_items, item_details=item_details)
@app.route('/remove_item/<item_title>', methods=['POST'])
def remove_item(item_title):
    username = session.get('username')
    cart_items = read_cart(username)
    cart_items = [item for item in cart_items if item != item_title]  # Remove the item
    # Rewrite the cart file
    with open(os.path.join(DATA_DIR, 'carts.txt'), 'w') as f:
        for item in cart_items:
            f.write(f"{username}|{item}\n")
    return redirect(url_for('shopping_cart'))
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    username = session.get('username')
    cart_items = read_cart(username)
    total_price = 0.0
    item_details = read_items()  # Read items to get details for checkout
    items_info = []
    for item_title in cart_items:
        item_info = next((item for item in item_details if item['title'] == item_title), None)
        if item_info:
            total_price += float(item_info['price'])
            items_info.append(item_info)  # Collect item details for the template
    if request.method == 'POST':
        # Handle payment and finalize purchase
        # Here you would also want to write the sold item details to the sold.txt file
        for item_title in cart_items:
            item_info = next((item for item in item_details if item['title'] == item_title), None)
            if item_info:
                write_sold_item(username, item_info)  # Write sold item details
        return redirect(url_for('dashboard'))
    return render_template('checkout.html', total_price=total_price, items_info=items_info)  # Pass item details to the template
@app.route('/sell_item', methods=['GET', 'POST'])
def sell_item():
    if request.method == 'POST':
        title = request.form['item_title_field']
        description = request.form['item_description_field']
        price = request.form['item_price_field']
        seller_username = session.get('username')
        write_item(title, description, price, seller_username)
        return redirect(url_for('dashboard'))
    return render_template('sell_item.html')
@app.route('/user_profile')
def user_profile():
    username = session.get('username')
    items = read_items()
    purchased_items = read_sold_items()
    on_sale_items = [item for item in items if item['seller_username'] == username]
    return render_template('user_profile.html', username=username, on_sale_items=on_sale_items, purchased_items=purchased_items)
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item_title = data.get('title')
    username = session.get('username')
    if username and item_title:
        write_cart(username, item_title)  # Add the item to the user's cart
        return '', 200  # Return a success response
    return '', 400  # Return a bad request response if something goes wrong
def write_sold_item(buyer_username, item_info):
    with open(os.path.join(DATA_DIR, 'sold.txt'), 'a') as f:
        f.write(f"{buyer_username}|{item_info['title']}|{item_info['description']}|{item_info['price']}|{item_info['seller_username']}\n")
if __name__ == '__main__':
    app.run(port=5000, debug=True)