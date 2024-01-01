from flask_socketio import SocketIO
from flask import Flask, Blueprint, render_template
from flask_login import LoginManager

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

# Initialize LoginManager

# Create a blueprint
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)


@main.route('/')
def index():
    return render_template('login.html')


@main.route('/chat')
def chat():
    return render_template('app.html')


@auth.route('/login')
def login():
    pass


@auth.route('/signup')
def register():
    pass


@auth.route('/logout')
def logout():
    pass


# Register the blueprint with the app
app.register_blueprint(auth)
app.register_blueprint(main)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
