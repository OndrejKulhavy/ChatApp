import os

import pymysql
from flask import Flask, redirect, render_template, request, session, url_for
from flask.cli import load_dotenv
from flask_socketio import SocketIO
from passlib.handlers.sha2_crypt import sha256_crypt

app = Flask(__name__)

# Configuration
app.debug = True
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# SocketIO setup
socketio = SocketIO(app)

connection = pymysql.connect(host=os.getenv("DB_HOST"),
                             user=os.getenv("DB_USER"),
                             password=os.getenv("DB_PASSWORD"),
                             db=os.getenv("DB_NAME"),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))


@app.route('/chat')
def chat():
    return render_template('app.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    form_values = request.form
    email = form_values.get('username')
    password = form_values.get('password')

    with connection.cursor() as cur:
        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

    if not result:
        return render_template('login.html', message='Invalid Email or Password')

    result = cur.fetchone()
    password_hash = result['password']

    if not sha256_crypt.verify(password, password_hash):
        return render_template('login.html', message='Invalid Email or Password')

    session['logged_in'] = True
    session['email'] = result['email']
    session['username'] = result['username']
    session['user_id'] = result['id']
    return redirect(url_for('main.index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    form_values = request.form
    username = form_values['username']
    email = form_values['email']
    profile_picture_url = form_values['profilePictureUrl']
    password_hash = sha256_crypt.hash(form_values['password'])

    if not username or not email or not form_values['password']:
        return render_template('signup.html', message='Please enter required fields')

    with connection.cursor() as cur:
        result_email = cur.execute("SELECT * FROM users WHERE email = %s", [email])

    if result_email:
        return render_template('signup.html', message='Email already exists')

    with connection.cursor() as cur:
        result_username = cur.execute("SELECT * FROM users WHERE username = %s", [username])

    if result_username:
        return render_template('signup.html', message='Username already exists')

    with connection.cursor() as cur:
        cur.execute("INSERT INTO users(username, email, password_hash, profile_picture) VALUES(%s, %s, %s, %s)",
                    (username, email, password_hash, profile_picture_url))

    connection.commit()

    return redirect(url_for('auth.login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    # Run the application using SocketIO
    socketio.run(app, host='0.0.0.0', allow_unsafe_werkzeug=True)
