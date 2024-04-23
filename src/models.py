"""
This module defines the data models used for interacting with
the database in the context of the application.

Dependencies:
* Flask_Sqlalchemy:
* Used for seamless interaction with the database in a Flask application.

Doc: https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
"""
import datetime
from typing import Type
from os import environ

import jwt
from sqlalchemy.sql import func
from sqlalchemy.orm import backref
from sqlalchemy.event import listens_for
from passlib.context import CryptContext

from src import db

# Configuration of CryptContext for using bcrypt
# and automatic management of deprecated algorithms.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    confirm_user = db.Column(db.Boolean, default=False)

    password = db.relationship('PasswordModel', backref='users', uselist=False,
                                cascade='all, delete-orphan', lazy=True)
    token = db.relationship('AuthTokenModel', backref='users', uselist=False,
                            cascade='all, delete-orphan', lazy=True)

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
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
            'sub': userid
        }
        self.token = jwt.encode(
            payload, environ.get('SECRET_KEY'), algorithm='HS256'
        )
        return self.token

    def verify_auth_token(self, token: str) -> dict or bool:
        try:
            decoded_token = jwt.decode(
                token, environ.get('SECRET_KEY'), algorithms='HS256',
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
