"""
This module defines the data models used for interacting with
the database in the context of the application.

Dependencies:
* Flask_Sqlalchemy:
* Used for seamless interaction with the database in a Flask application.

Doc: https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
"""

import os
import datetime
from typing import Type

import jwt
from dotenv import load_dotenv
from sqlalchemy.sql import func
from sqlalchemy.orm import backref
from sqlalchemy.event import listens_for
from passlib.context import CryptContext

from src import db

load_dotenv()

# Configuration of CryptContext for using bcrypt
# and automatic management of deprecated algorithms.
PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = os.environ.get('SECRET_KEY')

# JWT settings
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DAYS = 3  # Token lifetime in days


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    confirm_user = db.Column(db.Boolean, default=False)
    password = db.relationship(
        'PasswordModel',
        backref='users',
        uselist=False,
        cascade='all, delete-orphan',
        lazy=True
    )
    token = db.relationship(
        'AuthTokenModel',
        backref='users',
        uselist=False,
        cascade='all, delete-orphan',
        lazy=True
    )

    def __repr__(self) -> str:
        return f'<User: {self.username}>'

    def create(self, user: Type['UserModel']) -> None:
        db.session.add(user)
        db.session.commit()

    def update(self, data: dict) -> None:
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
                db.session.commit()

    def delete(self, user: Type['UserModel']) -> None:
        db.session.delete(user)
        db.session.commit()


class PasswordModel(db.Model):
    __tablename__='passwords'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255))
    last_update = db.Column(db.DateTime(timezone=True), default=func.now())
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'<User_id: {self.userid}>'

    def new_datetime(self):
        self.last_update = func.now()

    def hash_password(self, password: str) -> None:
        self.password_hash = PWD_CONTEXT.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return PWD_CONTEXT.verify(password, password_hash)

    def create(self, password: Type['PasswordModel']) -> None:
        db.session.add(password)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()


class AuthTokenModel(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'<User_id: {self.userid}>'

    def get_auth_token(self, userid: int) -> str:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXPIRATION_DAYS),
            'sub': userid
        }
        self.token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )
        return self.token

    def verify_auth_token(self, token: str) -> dict or bool:
        try:
            decoded_token = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=JWT_ALGORITHM,
                options={'require': ['exp', 'sub']}
            )
            return decoded_token
        except jwt.DecodeError:
            return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def create(self, auth: Type['AuthTokenModel']) -> None:
        db.session.add(auth)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self, auth: Type['AuthTokenModel']) -> None:
        db.session.delete(auth)
        db.session.commit()
