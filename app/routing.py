from flask import Blueprint, render_template, session, redirect, url_for

routing = Blueprint('routing', __name__)


@routing.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('routing.chat'))
    return render_template('login.html')


@routing.route('/chat')
def chat():
    return render_template('app.html')
