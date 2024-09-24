"""
This module defines a configuration class (Config) for Flask applications,
allowing users to set various configuration options.
"""

import os


class Config:
    """
    ** Set Flask configuration. **
    """

    # General
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True    # Only for debugging while developing
    HOST = '0.0.0.0'
    PORT = 8000
    API_URL_PREFIX = '/api/v1/'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
