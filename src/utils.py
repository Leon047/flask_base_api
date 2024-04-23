from typing import Callable, Any
from functools import wraps
from flask import request

from .messages import ApiMessages as msg
from .messages import error_msg
from .models import AuthTokenModel

def authenticate(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator function for the API that performs user auth token validation.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        auth_token = request.headers.get('Authorization')
        is_auth = AuthTokenModel().verify_auth_token(auth_token)
        if is_auth is False:
            return error_msg(msg.AUTHORIZATION_ERROR), 401
        kwargs['auth'] = is_auth
        return func(*args, **kwargs)
    return wrapper
