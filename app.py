from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__) 

conn = sqlite3.connect('gdsc.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS user(name TEXT, username TEXT, password TEXT)')

def login(username, password):
    cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        return user[0]
    else:
        return None

def register(name, username, password):
    cursor.execute('INSERT INTO user (name, username, password) VALUES (?, ?, ?)', (name, username, password))
    conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login(username, password)
        if user:
            return render_template('home.html', username=username)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register_route():
    if request.method == 'GET':
        return render_template('register.html')
    name = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    register(name, username, password)
    return render_template('home.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

