"""
This module configures and sets up fixtures for
testing the Flask application using pytest.

Dependencies:
* pytest: A testing framework for Python.

Doc: https://flask.palletsprojects.com/en/3.0.x/testing/
"""

import pytest
from dotenv import load_dotenv

from src import create_app, db
from src.models import UserModel, PasswordModel, AuthTokenModel

load_dotenv()

TEST_USER = {
    'email': 'base_test_user@gmail.com',
    'username': 'base_test_user'
}
TEST_USER_PASSWORD = 'BaseTestUser1234'


@pytest.fixture()
def app():
    """
    Fixture for creating a Flask app instance configured for testing.

    * Initializes the app in testing mode.
    * Sets up a test database.
    * Adds a test user and related models for testing purposes.

    Yields:
    * app (Flask app): Flask app instance configured for testing.
    """

    app = create_app()
    app.config.update({
        'TESTING': True
    })

    # ** other setup can go here **

    # create a test database
    with app.app_context():
        db.create_all()

        # Add test user in db
        test_user = UserModel(**TEST_USER)
        test_user.create(test_user)

        test_user_pswrd = PasswordModel(userid=test_user.id)
        test_user_pswrd.hash_password(TEST_USER_PASSWORD)
        test_user_pswrd.create(test_user_pswrd)

        test_auth = AuthTokenModel(userid=test_user.id)
        test_auth.get_auth_token(test_user.id)
        test_user.create(test_auth)

    yield app

    # ** other tear down can go here **

    # remove a test user
    with app.app_context():
        try:
            test_user.delete(test_user)
        except:
            print('The user has already been deleted.')


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
