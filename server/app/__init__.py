from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from .api import api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/models')

    return app