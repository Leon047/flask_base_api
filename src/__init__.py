"""
This module initializes the core packages of the Flask REST API
and the application's routes.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize the app with the extension
    db.init_app(app)

    # Initialize marshmallow
    ma.init_app(app)

    # Initialize api
    global api
    api = Api(app, prefix='/api/v1/')  # Set a prefix for API routes

    with app.app_context():
        # Creates database models
        db.create_all()

        """ Importing Classes and Creating a Route

        * Import the HelloWorld class from the views module.
        * Add the HelloWorld resource to the Flask-RESTful API with the endpoint 'hello'.
        """
        from .views import HelloWorld

        # App routes
        api.add_resource(HelloWorld, 'hello')

        return app
