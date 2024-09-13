"""
This module initializes the core packages of the
Flask REST API and defines application routes.

Dependencies:
* Flask: A micro web framework for Python.
* Flask_SQLAlchemy: SQLAlchemy integration for Flask.
* Flask_Restful: An extension for building REST APIs with Flask.
* Flask_Marshmallow: Integration of Marshmallow for Flask.
* Flask_Alembic: Alembic integration for Flask.

Doc:
* [Flask](https://flask.palletsprojects.com/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Flask-Restful](https://flask-restful.readthedocs.io/)
* [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/)
* [Flask-Alembic](https://flask-alembic.readthedocs.io/)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_alembic import Alembic

db = SQLAlchemy()
ma = Marshmallow()
alembic = Alembic()


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize the app with the extension
    db.init_app(app)

    # Initialize alembic
    alembic.init_app(app)

    # Initialize marshmallow
    ma.init_app(app)

    # Initialize api
    api = Api(app, prefix='/api/v1/')    # Set a prefix for API routes

    with app.app_context():
        # Creates database models
        db.create_all()

        # App routes
        from .routes import api_routes

        api_routes(api)

        return app
