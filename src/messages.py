"""
In (messages.py), you can add messages that will be used in
the API for various responses.
"""

from typing import Any


def success_msg(data: Any) -> dict:
    msg = {
        "api": "v1",
        "status": "success",
        "data": data
    }
    return msg


def error_msg(error_msg: dict) -> dict:
    msg = {
        "api": "v1",
        "status": "error",
        "message": error_msg,
    }
    return msg


class ApiMessages:
    """
    Error message should be 'dict'
    """
    # General messages
    MISSING_ARGUMENT = {'error': 'Missing argument.'}
    VALIDATION_ERROR = {'error': 'Validation error.'}
    AUTHORIZATION_ERROR = {'error': 'Authorization error.'}
    PERMISSION_ERROR = {'error': 'Permission error.'}
    NOT_FOUND_ERROR = {'error': 'Not found.'}
    INTERNAL_ERROR = {'error': 'Internal Server Error.'}

    INVALID_USERNAME = {'error': 'Invalid username.'}
    INVALID_PASSWORD = {'error': 'Invalid password.'}
    USER_EXIST = {'error': 'This username is already exist.'}
    EMAIL_EXIST = {'error': 'This email is already exist.'}

    USERNAME_ISTO_SHORT_ERROR = {'error': 'The username must contain at least 4 characters.'}
    USERNAME_IS_ALL_DIGITS_ERROR = {'error': 'Username cannot consist only of digits.'}
    EMAIL_INVALID_FORMAT_ERROR = {'error': 'Invalid email format.'}
    PASSWORD_ISNOT_SECURE_ERROR = {'error': 'The password must contain uppercase and lowercase letters, numbers, and symbols.'}

    # Other messages
