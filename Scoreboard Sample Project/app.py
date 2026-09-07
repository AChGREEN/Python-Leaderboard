# Import the necessary modules from Flask and sqlite3
from time import time

from flask import Flask, render_template, request, redirect
import sqlite3

# Create the Flask app
app = Flask(__name__)

# Name of the database file 
DB_NAME = 'scores.db'

# This function sets up the database if it doesn't already exist
def init_db():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    with sqlite3.connect(DB_NAME) as conn:
        # Create the 'scores' table with three columns:
        # - id: an auto-incrementing number (primary key)
        # - name: the player's name
        # - score: the player's score
        conn.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                seconds INTEGER NOT NULL
            )
        ''')

#This specifies that the following function will run whenever there's any actions taken on the web page
@app.route('/', methods=['GET', 'POST'])

# This function handles both displaying the leaderboard and submitting scores
def leaderboard():
    # If someone has submitted the form (POST request), save their data
    if request.method == 'POST':
        # Get the name and score that the player entered in the form
        name = request.form['name']
        score = request.form['score']
        seconds = request.form['seconds']        
        
        # Save the new score into the database
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('INSERT INTO scores (name, score, seconds) VALUES (?, ?, ?)', (name, score, seconds))
        
        # Redirect the user back to the main page after submitting
        return redirect('/')
    
    # If it's a normal page load (GET request), show the leaderboard
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Get all name and score entries from the database (in order they were added)
        cur.execute('SELECT name, score, seconds FROM scores')
        entries = cur.fetchall()

    # Send the HTML page with the most recent leaderboard
    return render_template('index.html', entries=entries)

#----- Mainline program: This code executes when we run this file.-----#

init_db()  # Set up the database before starting the web app

# Start the Flask server for local testing (Comment the version not being used)
app.run(debug=True)  
# Use this version when testing on your computer only

#app.run(debug=True, host='0.0.0.0') 
# Use this version if you want to test it on a phone/tablet connected to the same Wi-Fi