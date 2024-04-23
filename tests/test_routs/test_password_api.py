import pytest

from ..conftest import client, app
from src.models import PasswordModel, UserModel, AuthTokenModel

TEST_USER = {
    'email': 'base_test_user@gmail.com',
    'username': 'base_test_user',
    'password': 'BaseTestUser1234'
}

PASSWORD_API_URL = '/api/v1/user/password'

@pytest.fixture()
def test_user_with_valid_data(client, app):
    new_password = 'Abcd@12345'

    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()
        old_password = PasswordModel.query.filter_by(userid=user.id).first()

        old_password_hash = old_password.password_hash

        respons = client.post(PASSWORD_API_URL, headers={'Authorization': token.token},
            json={'old_password': TEST_USER['password'], 'new_password': new_password})

        assert respons.status_code == 201

        new_password = PasswordModel.query.filter_by(userid=user.id).first()
        new_password_hash = new_password.password_hash

        assert old_password_hash != new_password_hash

@pytest.mark.parametrize(
    ('old_password', 'new_password', 'code'),
    [
        (None, None, 400),
        (TEST_USER['password'], '', 400),
        ('', 'Abcd@12345', 401),
    ]
)
def test_user_with_invalid_data(client, app, old_password, new_password, code):
    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()

    respons = client.post(PASSWORD_API_URL, headers={'Authorization': token.token},
        json={'old_password': old_password, 'new_password': new_password})

    assert respons.status_code == code
