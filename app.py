from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import sqlite3
from bcrypt import hashpw, checkpw, gensalt

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key for production
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
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

# --- User Registration ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

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
            flash('Email already registered.')
            return redirect('/register')
        finally:
            conn.close()

    return render_template('register.html')

# --- User Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and checkpw(password.encode('utf-8'), user[3]):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!')
            return redirect('/dashboard')
        else:
            flash('Invalid login credentials.')
            return redirect('/login')

    return render_template('login.html')

# --- User Dashboard ---
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first!')
        return redirect('/login')

    if request.method == 'POST':
        content = request.form['content'].strip()
        if content:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts (user_id, content) VALUES (?, ?)",
                           (session['user_id'], content))
            conn.commit()
            conn.close()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT users.username, posts.content FROM posts
                      JOIN users ON users.id = posts.user_id
                      ORDER BY posts.id DESC''')
    posts = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', posts=posts)

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect('/login')

# --- Start App ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
