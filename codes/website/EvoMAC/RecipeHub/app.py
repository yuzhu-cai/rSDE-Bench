'''
This is the main application file for the RecipeHub web application.
It implements routing for all frontend pages and handles file operations for user and recipe data.
'''
from flask import Flask, render_template, request, redirect, url_for, session  # Import session for user management
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
# Helper functions to read and write data
def read_users():
    with open('data/users.txt', 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]
def write_user(username, password):
    with open('data/users.txt', 'a') as file:
        file.write(f"{username}:{password}\n")
def read_recipes():
    with open('data/recipes.txt', 'r') as file:
        return [line.strip().split(';') for line in file.readlines()]
def write_recipe(recipe_title, ingredients, instructions):
    recipe_id = len(read_recipes())
    username = session.get('username')  # Get the current user's username
    if username:  # Ensure username is available
        with open('data/recipes.txt', 'a') as file:
            file.write(f"{recipe_id};{recipe_title};{ingredients};{instructions};{username}\n")  # Include username
    else:
        raise Exception("User must be logged in to submit a recipe.")
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username_input']
        password = request.form['password_input']
        users = read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('home'))
        return render_template('login.html', error_message="Invalid username or password.")
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username_input']
        password = request.form['password_input']
        write_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    if request.method == 'POST':
        recipe_title = request.form['recipe_title_input']
        ingredients = request.form['ingredients_input']
        instructions = request.form['instructions_input']
        write_recipe(recipe_title, ingredients, instructions)  # Include username
        return render_template('submit_recipe.html', submission_success_message="Recipe submitted successfully!")
    return render_template('submit_recipe.html')
@app.route('/browse_recipes')
def browse_recipes():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    recipes = read_recipes()
    return render_template('browse_recipes.html', recipe_list=recipes)
@app.route('/user_profile')
def user_profile():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    username = session.get('username')  # Retrieve the username from the session
    user_recipes = read_recipes()  # Get all recipes
    return render_template('user_profile.html', username=username, user_recipes=user_recipes)
@app.route('/recipe_details/<int:recipe_id>')
def recipe_details(recipe_id):
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    recipes = read_recipes()
    recipe = next((r for r in recipes if int(r[0]) == recipe_id), None)
    return render_template('recipe_details.html', recipe=recipe)
@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    users = read_users()
    users = [user for user in users if user[0] != username]  # Remove the user from the list
    with open('data/users.txt', 'w') as file:
        for user in users:
            file.write(f"{user[0]}:{user[1]}\n")
    session.pop('username', None)  # Remove the user from the session
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(port=5000)