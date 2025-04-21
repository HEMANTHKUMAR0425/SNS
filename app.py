from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import sqlite3
from bcrypt import hashpw, checkpw, gensalt

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production!
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

# Initialize DB before first request
@app.before_first_request
def setup():
    init_db()

# --- User Registration ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        # Input validation
        if not username or not email or not password:
            flash('All fields are required.')
            return redirect('/register')

        hashed_password = hashpw(password.encode('utf-8'), gensalt())

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            conn.commit()
            flash('Registration successful. Please log in.')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username or email already exists.')
            return redirect('/register')
        finally:
            conn.close()

    return render_template('register.html')
