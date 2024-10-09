'''
This is the backend code for the Movie Recommendation System. It implements routing for all frontend pages,
handles user login and registration, and manages file read/write operations for user, movie, and favorites data.
The application runs on local port 5000.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
MOVIES_FILE = os.path.join(DATA_DIR, 'movies.txt')
FAVORITES_FILE = os.path.join(DATA_DIR, 'favorites.txt')
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(USERS_FILE, 'a') as f:
            f.write(f"{username},{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    recommendations = get_movie_recommendations()
    return render_template('home.html', username=username, recommendations=recommendations)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['searchField']
        results = search_movies(query)
        return render_template('search.html', results=results)
    return render_template('search.html', results=[])
@app.route('/movie_details/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    return render_template('movie_details.html', movie=movie)
@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    favorites = get_user_favorites(username)
    return render_template('favorites.html', favorites=favorites)
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html', error="Invalid credentials")
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/add_to_favorites/<int:movie_id>', methods=['POST'])
def add_to_favorites(movie_id):
    if 'username' not in session:
        return 'Unauthorized', 401
    username = session['username']
    with open(FAVORITES_FILE, 'a') as f:
        f.write(f"{username},{movie_id}\n")
    return 'Success', 200
@app.route('/remove_from_favorites/<int:movie_id>', methods=['POST'])
def remove_from_favorites(movie_id):
    if 'username' not in session:
        return 'Unauthorized', 401
    username = session['username']
    lines = []
    with open(FAVORITES_FILE, 'r') as f:
        lines = f.readlines()
    with open(FAVORITES_FILE, 'w') as f:
        for line in lines:
            if line.strip() != f"{username},{movie_id}":
                f.write(line)
    return 'Success', 200
def validate_user(username, password):
    with open(USERS_FILE, 'r') as f:
        for line in f:
            user, pwd = line.strip().split(',')
            if user == username and pwd == password:
                return True
    return False
def get_movie_recommendations():
    recommendations = []
    with open(MOVIES_FILE, 'r') as f:
        for line in f:
            movie_id, title, description, rating = line.strip().split(',')
            recommendations.append({
                'id': movie_id,
                'title': title,
                'description': description,
                'rating': rating
            })
    return recommendations
def search_movies(query):
    results = []
    with open(MOVIES_FILE, 'r') as f:
        for line in f:
            movie_id, title, description, rating = line.strip().split(',')
            if query.lower() in title.lower():
                results.append({
                    'id': movie_id,
                    'title': title,
                    'description': description,
                    'rating': rating
                })
    return results
def get_movie_details(movie_id):
    with open(MOVIES_FILE, 'r') as f:
        for line in f:
            id, title, description, rating = line.strip().split(',')
            if int(id) == movie_id:
                return {
                    'id': id,
                    'title': title,
                    'description': description,
                    'rating': rating
                }
    return None
def get_user_favorites(username):
    favorites = []
    with open(FAVORITES_FILE, 'r') as f:
        for line in f:
            user, movie_id = line.strip().split(',')
            if user == username:
                favorites.append(movie_id)
    return favorites
if __name__ == '__main__':
    app.run(port=5000)