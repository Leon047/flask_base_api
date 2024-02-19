"""
In 'messages.py', you can add messages that will be used in
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
    # MISSING_ARGUMENT = {'error': 'Missing argument'}
    # VALIDATION_ERROR = {'error': 'Validation error'}
    # AUTHORIZATION_ERROR = {'error': 'Authorization error'}
    # PERMISSION_ERROR = {'error': 'Permission error'}
    # NOT_FOUND_ERROR = {'error': 'Not found'}
    INTERNAL_ERROR = {'error': 'Internal Server Error'}

    # Other messages
