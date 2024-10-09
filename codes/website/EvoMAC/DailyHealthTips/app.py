'''
This is the main application file for the DailyHealthTips web application.
It implements the backend functionality, including routing for the login page,
daily tips page, and tips archive page. It also handles file read and write
operations for user data, daily tips, and feedback.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
# Function to read users from the users.txt file
def read_users():
    users = {}
    with open('data/users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split(',')
            users[username] = (password, email)
    return users
# Function to read daily tips from the daily_tips.txt file
def read_daily_tips():
    tips = []
    with open('data/daily_tips.txt', 'r') as file:
        for line in file:
            date, tip = line.strip().split(',', 1)
            tips.append((date, tip))
    return tips
# Function to write feedback to the feedback.txt file
def write_feedback(username, feedback):
    with open('data/feedback.txt', 'a') as file:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        file.write(f"{username},{date},{feedback}\n")
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/daily_tips', methods=['GET', 'POST'])
def daily_tips():
    tips = read_daily_tips()
    if 'current_tip_index' not in session:
        session['current_tip_index'] = 0
    if request.method == 'POST':
        if 'previous_tip_button' in request.form:
            session['current_tip_index'] = max(0, session['current_tip_index'] - 1)
        elif 'next_tip_button' in request.form:
            session['current_tip_index'] = min(len(tips) - 1, session['current_tip_index'] + 1)
        elif 'submit_feedback_button' in request.form:
            username = request.form.get('username')
            feedback = request.form.get('feedback_text_area')
            write_feedback(username, feedback)
    current_tip_index = session['current_tip_index']
    current_tip = tips[current_tip_index] if tips else ("", "")
    return render_template('daily_tips.html', tip=current_tip[1], username=request.args.get('username'))
@app.route('/tips_archive', methods=['GET'])
def tips_archive():
    tips = read_daily_tips()
    return render_template('tips_archive.html', tips=tips)
if __name__ == '__main__':
    app.run(port=5000)