import os
from flask import Flask
from flask.cli import load_dotenv
from flask_socketio import SocketIO
from routing import routing
from auth import auth
import pymysql.cursors

app = Flask(__name__)

# Configuration
app.debug = True
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# SocketIO setup
socketio = SocketIO(app)

# Blueprint registration
app.register_blueprint(auth)
app.register_blueprint(routing)

if __name__ == '__main__':
    # Run the application using SocketIO
    socketio.run(app, allow_unsafe_werkzeug=True)
