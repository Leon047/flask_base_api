import pytest

from ..conftest import client, app
from src.models import UserModel, AuthTokenModel, PasswordModel

USER_API_URL = '/api/v1/user'

TEST_USER = {
    'email': 'base_test_user@gmail.com',
    'username': 'base_test_user',
    'password': 'BaseTestUser1234'
}

INVALID_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTg1OTIyMTIsInN1YiI6MX0.gxv1SaK4W23LwjP76mh4TM99aXqRaDWozxlOSnVEdmM'

@pytest.mark.parametrize('token', [(''), (INVALID_TOKEN)])
def test_get_user_with_invalid_token(client, token):
    response = client.get(USER_API_URL, headers={'Authorization': token})
    assert response.status_code == 401

def test_get_user_with_valid_token(client, app):
    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()

        response = client.get(USER_API_URL, headers={'Authorization': token.token})

        assert response.status_code == 200

        # Checkinf fields
        assert b'id' in response.data
        assert b'username' in response.data
        assert b'email' in response.data
        assert b'confirm_user' in response.data

        # Checking key values
        username = TEST_USER['username']
        email = TEST_USER['email']

        assert b'base_test_user' in response.data
        assert b'base_test_user@gmail.com' in response.data

def test_put_user_with_valid_creds(client, app):
    new_test_user = {
        'email': 'new_test_user@gmail.com',
        'username': 'new_test_user',
        'password': 'Abcd@1234'
    }
    response = client.put(USER_API_URL, json=new_test_user,
                          headers={'Content-Type': 'application/json'})

    assert response.status_code == 201
    assert b'new_test_user@gmail.com' in response.data
    assert b'new_test_user' in response.data

    with app.app_context():
        user = UserModel.query.filter_by(username=new_test_user['username'] ).first()
        assert UserModel.query.filter_by(
            username=new_test_user['username']).count() == 1
        assert user.username == new_test_user['username']
        assert user.email == new_test_user['email']
        user.delete(user)

@pytest.mark.parametrize(
    ('username', 'email', 'password'),
    [
        ('', '', ''),
        ('', 'test_user@gmail.com', 'Abc@1234'),
        ('test_user', '', 'Abcd@1234'),
        ('test_user', 'test_user@gmail.com', '')
    ]
)
def test_put_user_with_empty_field(client, username, email, password):
    response = client.put(USER_API_URL,
        json={
            'email': email,
            'username': username,
            'password': password
        }
    )
    assert response.status_code == 400

def test_put_with_existing_user(client, app):
    response = client.put(USER_API_URL, json=TEST_USER)

    assert response.status_code == 400
    assert b'username' in response.data  # check username error msg
    assert b'email' in response.data  # check email error msg

def test_patch_with_existing_user_and_new_data(client, app):
    new_username = 'new_test_user'
    new_email = 'new_test_user@gmail.com'

    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()

        # Check old data
        assert user.username == TEST_USER['username']
        assert user.email == TEST_USER['email']

    response = client.patch(USER_API_URL,
        headers={'Authorization': token.token},
        json={'username': new_username, 'email': new_email}
    )

    # Check new data
    assert response.status_code == 200
    assert b'new_test_user' in response.data
    assert b'new_test_user@gmail.com' in response.data

    with app.app_context():
        user_new = UserModel.query.filter_by(username=new_username).first()
        user_new.delete(user_new)

def test_patch_usernate_taken(client, app):
    new_test_user = {
        'email': 'new_test_user@gmail.com',
        'username': 'new_test_user',
        'password': 'Abcd@1234'
    }
    response = client.put(USER_API_URL, json=new_test_user)

    assert response.status_code == 201

    with app.app_context():
        base_user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        base_user_token = AuthTokenModel.query.filter_by(userid=base_user.id).first()

    # Passing data of a new user to the base user
    response = client.patch(USER_API_URL,
        headers={'Authorization': base_user_token.token},
        json={'username': new_test_user['username'], 'email': new_test_user['email']}
    )

    assert response.status_code == 404
    assert b'username' in response.data  # check username error msg
    assert b'email' in response.data     # check email error msg

    with app.app_context():
        new_user = UserModel.query.filter_by(username=new_test_user['username']).first()
        new_user.delete(new_user)

def test_delete_user_with_valid_data(client, app):
    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()

    response = client.delete(USER_API_URL,
        headers={'Authorization': token.token},
        json={'username':TEST_USER['username'], 'password': TEST_USER['password']}
    )

    assert response.status_code == 204

    with app.app_context():
        check_user = UserModel.query.filter_by(id=user.id).first()
        check_password = PasswordModel.query.filter_by(userid=user.id).first()
        check_token = AuthTokenModel.query.filter_by(userid=user.id).first()

        assert check_user == None
        assert check_password == None
        assert check_token == None

@pytest.mark.parametrize(
    ('username', 'password', 'code'),
    [
        ('none_test_user', TEST_USER['password'], 404),
        (TEST_USER['username'], 'NonePassword@123', 401)
    ]
)
def test_delete_user_with_invalid_data(client, app, username, password, code):
    invalid_username = 'none_test_user'
    invalid_password = 'NonePassword@123'
    with app.app_context():
        user = UserModel.query.filter_by(username=TEST_USER['username']).first()
        token = AuthTokenModel.query.filter_by(userid=user.id).first()

    response = client.delete(USER_API_URL,
        headers={'Authorization': token.token},
        json={'username': username, 'password': password}
    )

    assert response.status_code == code
