"""
This module defines a configuration class (Config) for Flask applications,
allowing users to set various configuration options.
"""
import os


class Config:
    """Set Flask configuration."""

    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
