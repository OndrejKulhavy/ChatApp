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


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    return render_template('app.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    form_values = request.form
    email = form_values.get('username')
    password = form_values.get('password')

    if not email or not password:
        return render_template('login.html', message='Please enter required fields')

    with connection.cursor() as cur:
        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

    if not result:
        return render_template('login.html', message='Invalid Email or Password')

    result = cur.fetchone()
    password_hash = result['password_hash']

    if not sha256_crypt.verify(password, password_hash):
        return render_template('login.html', message='Invalid Email or Password')

    session['logged_in'] = True
    session['email'] = result['email']
    session['username'] = result['username']
    session['user_id'] = result['user_id']
    return redirect(url_for('chat'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    form_values = request.form
    username = form_values.get('username')
    email = form_values.get('email')
    profile_picture_url = form_values.get('profilePictureUrl')
    password = form_values.get('password')
    password_hash = sha256_crypt.hash(str(password).encode('utf-8'))

    if not username or not email or not password:
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

    return redirect(url_for('login'))


from flask import redirect, url_for


@app.route('/chat/create_room', methods=['POST'])
def create_room():
    if 'logged_in' not in session:
        return {"error": "Not logged in"}

    form_values = request.form
    room_name = form_values.get('chat_room_name')
    list_of_users = form_values.getlist('users')
    owner_id = session['user_id']

    list_of_users.append(owner_id)

    if not room_name or not list_of_users:
        return {"error": "Please enter required fields"}

    # Insert into chat_rooms table
    with connection.cursor() as cur:
        cur.execute("INSERT INTO chat_rooms(room_name, owner_id) VALUES(%s, %s)", (room_name, owner_id))
        connection.commit()

        # Get the last inserted ID from the connection
        room_id = cur.lastrowid

    # Insert into chat_rooms_access table
    with connection.cursor() as cur:
        for user_id in list_of_users:
            cur.execute("INSERT INTO chat_rooms_access(room_id, user_id) VALUES(%s, %s)", (room_id, user_id))
        connection.commit()

    return redirect(url_for('chat'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/search_users')
def search_users():
    if 'logged_in' not in session:
        return {"error": "Not logged in"}
    search_term = request.args.get('search_term')
    if not search_term:
        return {"users": []}

    with connection.cursor() as cur:
        result = cur.execute("SELECT user_id, username, profile_picture FROM users WHERE username LIKE %s",
                             [f'%{search_term}%'])

    if not result:
        return {"users": []}

    users = cur.fetchall()
    return {"users": users}


if __name__ == '__main__':
    # Run the application using SocketIO
    socketio.run(app, host='0.0.0.0', allow_unsafe_werkzeug=True)
