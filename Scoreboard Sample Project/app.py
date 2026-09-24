# Import the necessary modules from Flask and sqlite3
from time import time

from flask import Flask, render_template, request, redirect
import sqlite3

# Create the Flask app
app = Flask(__name__)

@app.template_filter('hrsminsec')
def format_time(total_seconds):
    total_seconds = int(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f'{hours}h {minutes}m {seconds}s'
    elif minutes > 0:
        return f'{minutes}m {seconds}s'
    else:
        return f'{seconds}s'
    
# Name of the database file 
DB_NAME = 'scores.db'
PER_PAGE = 10

@app.route('/data-deal-home')
def data_deal_home():
    return render_template('Aarav-Main.html')
@app.route('/leaderboard-page')
def leaderboard_page():
    return leaderboard()

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

@app.route('/', methods=['GET', 'POST'])
def leaderboard():
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        seconds = request.form['seconds']
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                'INSERT INTO scores (name, score, seconds) VALUES (?, ?, ?)',
                (name, score, seconds)
            )
        return redirect('/')

    search = request.args.get('search', '').strip()
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    if page < 1:
        page = 1
    offset = (page - 1) * PER_PAGE
    like_term = f'%{search}%'
    with sqlite3.connect(DB_NAME) as conn:
        total_count = conn.execute(
            'SELECT COUNT(*) FROM scores WHERE name LIKE ?',
            (like_term,)
        ).fetchone()[0]
        entries = conn.execute(
            'SELECT name, score, seconds FROM scores WHERE name LIKE ? ORDER BY score DESC, seconds ASC LIMIT ? OFFSET ?',
            (like_term, PER_PAGE, offset)
        ).fetchall()

    total_pages = max(1, (total_count + PER_PAGE - 1) // PER_PAGE)
    if page > total_pages:
        page = total_pages

    return render_template(
        'index.html',
        entries=entries,
        page=page,
        total_pages=total_pages,
        search=search
    )


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
