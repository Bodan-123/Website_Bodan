from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, department TEXT, year TEXT, section TEXT, password TEXT)')
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        section = request.form['section']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO users (name, department, year, section, password) VALUES (?, ?, ?, ?, ?)',
                     (name, department, year, section, password))
        conn.commit()
        conn.close()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.')
            
    return render_template('login.html')

# Exit Page
@app.route('/exit')
def exit():
    session.pop('username', None)
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(debug=True)
