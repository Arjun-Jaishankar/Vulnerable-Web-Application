from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
import random
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key'  # Used for session management

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    if os.path.exists('database.db'):
        os.remove('database.db')  # Delete the database file to reset on restart
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, comment TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (account_number INTEGER PRIMARY KEY, balance REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    
    # Create default admin user
    admin_password = hash_password("admin")
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("admin", admin_password))
    
    # Create predefined accounts
    cursor.execute('INSERT INTO accounts (account_number, balance) VALUES (?, ?)', (100, 110.00))
    cursor.execute('INSERT INTO accounts (account_number, balance) VALUES (?, ?)', (101, 0.00))
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'account_number' not in session:
        session['account_number'] = 100  # Default account number
    return render_template('index.html', account_number=session['account_number'])

# Stored XSS Vulnerability
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        comment = request.form['comment']
        if "script" in comment.lower():
            comment = "Nice Try! Maybe try again?"
        cursor.execute('INSERT INTO comments (comment) VALUES (?)', (comment,))
        conn.commit()
    cursor.execute('SELECT * FROM comments')
    comments = cursor.fetchall()
    conn.close()
    return render_template('comments.html', comments=comments)

# Reflected XSS Vulnerability
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    return f"<h1>Search results for: {query}</h1>"

# Session Fixation Vulnerability
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return "<h1>Login failed: Incorrect username.</h1>"
        elif user[0] != hash_password(password):
            return "<h1>Login failed: Incorrect password.</h1>"
        else:
            session['user'] = username  # Set session only if credentials are correct
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"<h1>Welcome {session['user']}</h1>"

# CSRF Vulnerability with Balance Feature
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        amount = float(request.form['amount'])
        cursor.execute('SELECT balance FROM accounts WHERE account_number = ?', (100,))
        sender_account = cursor.fetchone()
        
        if sender_account and sender_account[0] >= amount:
            new_sender_balance = sender_account[0] - amount
            cursor.execute('UPDATE accounts SET balance = ? WHERE account_number = ?', (new_sender_balance, 100))
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE account_number = ?', (amount, 101))
            conn.commit()
            message = f"Successfully transferred ${amount} to account 101."
        else:
            message = "Transfer failed: Insufficient balance."
        
        conn.close()
        return render_template('transfer.html', account=session['account_number'], message=message)
    
    cursor.execute('SELECT account_number, balance FROM accounts WHERE account_number = ?', (session['account_number'],))
    account = cursor.fetchone()
    conn.close()
    return render_template('transfer.html', account=account)

@app.route('/check_balance', methods=['GET'])
def check_balance():
    account_number = request.args.get('account_number')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM accounts WHERE account_number = ?', (account_number,))
    account = cursor.fetchone()
    conn.close()
    
    return jsonify({"balance": account[0] if account else None})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
