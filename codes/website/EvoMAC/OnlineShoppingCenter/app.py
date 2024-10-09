'''
This is the backend code for the Online Shopping Center web application.
It implements routing for all frontend pages and handles file read/write operations.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data/'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.txt')
CART_FILE = os.path.join(DATA_DIR, 'shopping_cart.txt')
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['reg_username_input']
        password = request.form['reg_password_input']
        email = request.form['reg_email_input']
        with open(USERS_FILE, 'a') as f:
            f.write(f"{username},{password},{email}\n")
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    with open(USERS_FILE, 'r') as f:
        for line in f:
            user, pwd, email = line.strip().split(',')
            if user == username and pwd == password:
                session['username'] = username
                return redirect(url_for('product_listing'))
    return redirect(url_for('login'))  # Redirect back to login on failure
@app.route('/product_listing')
def product_listing():
    products = []
    with open(PRODUCTS_FILE, 'r') as f:
        for line in f:
            product_id, product_name, product_price = line.strip().split(',')
            products.append({'id': product_id, 'name': product_name, 'price': product_price})
    return render_template('product_listing.html', products=products)
@app.route('/shopping_cart')
def shopping_cart():
    cart_items = []
    if 'username' in session:
        username = session['username']
        if os.path.exists(CART_FILE):
            with open(CART_FILE, 'r') as f:
                for line in f:
                    user, product_id, quantity = line.strip().split(',')
                    if user == username:
                        cart_items.append({'product_id': product_id, 'quantity': quantity})
    return render_template('shopping_cart.html', cart_items=cart_items)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address_input']
        payment_info = request.form['payment_info_input']
        # Here you would process the payment and save the order
        return redirect(url_for('order_confirmation', shipping_address=shipping_address, payment_info=payment_info))
    return render_template('checkout.html')
@app.route('/order_confirmation')
def order_confirmation():
    shipping_address = request.args.get('shipping_address')
    payment_info = request.args.get('payment_info')
    return render_template('order_confirmation.html', shipping_address=shipping_address, payment_info=payment_info)
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login page
    username = session['username']
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    # Read existing cart items
    cart_items = {}
    if os.path.exists(CART_FILE):
        with open(CART_FILE, 'r') as f:
            for line in f:
                user, prod_id, qty = line.strip().split(',')
                if user == username:
                    cart_items[prod_id] = int(qty)
    else:
        # Initialize the cart if it doesn't exist
        with open(CART_FILE, 'w') as f:
            pass  # Create an empty file
    # Update quantity
    if product_id in cart_items:
        cart_items[product_id] += quantity
    else:
        cart_items[product_id] = quantity
    # Write updated cart back to file
    with open(CART_FILE, 'w') as f:
        for prod_id, qty in cart_items.items():
            f.write(f"{username},{prod_id},{qty}\n")
    return '', 204  # No content response
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login page
    username = session['username']
    product_id = request.form['product_id']
    # Read existing cart items
    cart_items = []
    if os.path.exists(CART_FILE):
        with open(CART_FILE, 'r') as f:
            for line in f:
                user, prod_id, qty = line.strip().split(',')
                if user == username and prod_id != product_id:
                    cart_items.append(line.strip())
    else:
        # If the file doesn't exist, there's nothing to remove
        return '', 204  # No content response
    # Write updated cart back to file
    with open(CART_FILE, 'w') as f:
        for item in cart_items:
            f.write(f"{item}\n")
    return '', 204  # No content response
if __name__ == '__main__':
    app.run(port=5000)