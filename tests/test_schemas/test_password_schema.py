import pytest
from marshmallow import ValidationError

from src import schemas

@pytest.mark.parametrize(
    'password, valid',
    [
        ('Abc@1234', True),
        ('Abcd1234', False),
        ('abc@1234', False),
        ('Abcdefj@', False),
        ('abcdefj@', False),
        ('Abc@123',  False),
        ('@1234567', False),
        ('12345678', False),
        ('@@@@@@@@', False)
    ]
)
def test_validate_password(password, valid):
    password_schema = schemas.PasswordSchema()
    data = {'password': password}

    try:
        is_valid_password = password_schema.load(data)
        assert valid is True

    except ValidationError:
        assert valid is False
