"""
This module defines the API routes for the Flask application.

It imports the necessary view classes and maps them to specific API endpoints
using Flask-RESTful's `add_resource` method.
"""

from .views import (
    UserApi,
    AuthApi,
    PasswordApi,
    HelloWorld
)


def api_routes(api) -> None:
    api.add_resource(UserApi, 'user')
    api.add_resource(AuthApi, 'user/auth')
    api.add_resource(PasswordApi, 'user/password')
    api.add_resource(HelloWorld, 'hello')
