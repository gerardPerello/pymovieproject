from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from .api import api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/models')

    socketio.init_app(app, cors_allowed_origins="*")

    return app


