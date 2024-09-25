import pytest

from ..conftest import client, app
from src.models import UserModel, AuthTokenModel, PasswordModel

USER_API_URL = '/api/v1/user'
AUTH_API_URL = '/api/v1/user/auth'

TEST_USER = {
    'email': 'base_test_user@gmail.com',
    'username': 'base_test_user',
    'password': 'BaseTestUser1234'
}


@pytest.fixture()
def test_auth_with_valid_data(client, app):
    new_user = {
        'username': 'test_user',
        'email': 'test_user@gmail.com',
        'password': 'TestUser@12345',
    }
    mk_new_user = client.put(USER_API_URL, json=new_user)

    assert mk_new_user.status_code == 201

    with app.app_context():
        new_user = UserModel.query.filter_by(username=new_user['username']).first()
        token = AuthTokenModel.query.filter_by(userid=new_user.id).first()

        assert new_user.username == new_user['username']
        assert token == None

    respons = client.post(
        AUTH_API_URL,
        json={
            'username': new_user['username'],
            'password': new_user['password']
        }
    )

    assert respons.status_code == 201

    with app.app_context():
        token = AuthTokenModel.query.filter_by(userid=new_user.id).first()

        assert token != None
        assert token.token in respons.data

        new_user.delete(new_user)


@pytest.mark.parametrize(
    ('username', 'password', 'code'),
    [
        (None, None, 400),
        ('none_user', TEST_USER['password'], 404),
        (TEST_USER['username'], 'NonePassword12345', 401)
    ]
)
def test_auth_with_invalid_data(client, username, password, code):
    respons = client.post(
        AUTH_API_URL,
        json={
            'username': username,
            'password': password
        }
    )

    assert respons.status_code == code


def test_delete_auth_user_token(client, app):
    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()

        assert token != None

    respons = client.delete(
        AUTH_API_URL,
        headers={'Authorization': token.token}
    )

    assert respons.status_code == 204

    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        password = PasswordModel.query.filter_by(userid=user.id).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()

        assert user != None
        assert password != None
        assert token is None
