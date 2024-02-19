"""
This module defines the RESTful API endpoints using Flask-RESTful
for handling HTTP requests in the application.

Dependencies:
* Flask_RestFul:
* An extension for Flask that adds support for quickly building REST APIs.

* Doc: https://flask-restful.readthedocs.io/en/latest/
"""
from flask_restful import Resource

# from .messages import Missing as msg
from .messages import error_msg, success_msg
# from .models import ExampleModel
# from .schemas import ExampleSchema


class HelloWorld(Resource):

    def get(self) -> tuple[dict, int]:
        # Your request handling code
        return success_msg('Hello World'), 200
