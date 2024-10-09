'''
This is the main backend application for the DigitalArtworkGallery. 
It handles routing for all frontend pages, user authentication, 
and file operations for storing user and artwork data.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
ARTWORKS_FILE = os.path.join(DATA_DIR, 'artworks.txt')
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/gallery')
def gallery():
    artworks = load_artworks()
    return render_template('gallery.html', artworks=artworks)
@app.route('/view_artwork/<artwork_id>')
def view_artwork(artwork_id):
    artwork = get_artwork_by_id(artwork_id)
    return render_template('view_artwork.html', artwork=artwork)
@app.route('/upload_artwork', methods=['GET', 'POST'])
def upload_artwork():
    if request.method == 'POST':
        title = request.form['artwork_title']
        description = request.form['artwork_description']
        save_artwork(title, description)
        return redirect(url_for('gallery'))
    return render_template('upload_artwork.html')
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    if authenticate_user(username, password):
        return redirect(url_for('gallery'))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('login'))
@app.route('/delete_artwork/<artwork_id>', methods=['POST'])
def delete_artwork(artwork_id):
    artworks = load_artworks()
    artworks = [artwork for artwork in artworks if artwork[0] != artwork_id]
    save_artworks(artworks)
    return redirect(url_for('gallery'))
def authenticate_user(username, password):
    with open(USERS_FILE, 'r') as file:
        for line in file:
            user, pwd = line.strip().split(':')
            if user == username and pwd == password:
                return True
    return False
def load_artworks():
    artworks = []
    if os.path.exists(ARTWORKS_FILE):
        with open(ARTWORKS_FILE, 'r') as file:
            for line in file:
                artworks.append(line.strip().split('|'))
    return artworks
def get_artwork_by_id(artwork_id):
    artworks = load_artworks()
    for artwork in artworks:
        if artwork[0] == artwork_id:
            return artwork
    return None
def save_artwork(title, description):
    artwork_id = str(len(load_artworks()) + 1)
    with open(ARTWORKS_FILE, 'a') as file:
        file.write(f"{artwork_id}|{title}|{description}\n")
def save_artworks(artworks):
    with open(ARTWORKS_FILE, 'w') as file:
        for artwork in artworks:
            file.write(f"{artwork[0]}|{artwork[1]}|{artwork[2]}\n")
if __name__ == '__main__':
    app.run(port=5000)