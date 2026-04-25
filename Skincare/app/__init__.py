from flask import Flask
from .db import db_connection

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        db_connection()  # Initialize database connection

    from .routes import main
    app.register_blueprint(main)

    return app