'''
This is the main application file for the Nutrition Information Hub.
It implements the backend logic for user authentication, routing, and data management.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
# File paths
users_file = 'data/users.txt'
nutrition_info_file = 'data/nutrition_info.txt'
recipes_file = 'data/recipes.txt'
def read_users():
    '''Read user credentials from the users.txt file.'''
    users = {}
    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
    return users
@app.route('/')
def login():
    '''Render the login page.'''
    return render_template('login.html', errorMessage='')  # Initialize errorMessage
@app.route('/home')
def home():
    '''Render the home page after successful login.'''
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))
@app.route('/nutrition_info')
def nutrition_info():
    '''Render the nutrition information page.'''
    if 'username' in session:
        return render_template('nutrition_info.html')
    return redirect(url_for('login'))
@app.route('/recipe_tracker')
def recipe_tracker():
    '''Render the recipe tracker page.'''
    if 'username' in session:
        return render_template('recipe_tracker.html')
    return redirect(url_for('login'))
@app.route('/login', methods=['POST'])
def do_login():
    '''Handle user login.'''
    username = request.form['usernameField']
    password = request.form['passwordField']
    users = read_users()
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('login.html', errorMessage='Invalid credentials')  # Pass error message
@app.route('/logout')
def logout():
    '''Handle user logout.'''
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/save_recipe', methods=['POST'])
def save_recipe():
    '''Handle saving a new recipe.'''
    data = request.get_json()
    recipe_name = data['recipeName']
    ingredients = data['ingredients']
    instructions = data['instructions']
    # Check if the recipe already exists
    if os.path.exists(recipes_file):
        with open(recipes_file, 'r') as file:
            for line in file:
                if line.startswith(recipe_name + '|'):
                    return 'Recipe already exists', 400  # Return an error if it exists
    # Save the recipe to recipes.txt
    with open(recipes_file, 'a') as file:
        file.write(f"{recipe_name}|{ingredients}|{instructions}\n")
    return 'Recipe saved successfully', 200
@app.route('/search_nutrition')
def search_nutrition():
    '''Handle searching for nutritional information.'''
    query = request.args.get('query', '')
    results = []
    if os.path.exists(nutrition_info_file):
        with open(nutrition_info_file, 'r') as file:
            for line in file:
                if query.lower() in line.lower():  # Case insensitive search
                    results.append(line.strip())
    return {'results': results}
@app.route('/get_saved_recipes')
def get_saved_recipes():
    '''Handle retrieving saved recipes.'''
    recipes = []
    if os.path.exists(recipes_file):
        with open(recipes_file, 'r') as file:
            for line in file:
                recipes.append(line.strip())
    return {'recipes': recipes}
if __name__ == '__main__':
    app.run(port=5000)