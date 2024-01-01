from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from passlib.hash import sha256_crypt

from database import connection

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    form_values = request.form
    email = form_values['username']
    password = form_values['password']

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


@auth.route('/signup', methods=['GET', 'POST'])
def register():
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


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
