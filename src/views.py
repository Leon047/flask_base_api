"""
This module defines the RESTful API endpoints using Flask-RESTful
for handling HTTP requests in the application.

Dependencies:
* Flask_RestFul:
* An extension for Flask that adds support for quickly building REST APIs.

Doc: https://flask-restful.readthedocs.io/en/latest/
"""

from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from .messages import success_msg, error_msg
from .messages import ApiMessages as msg
from .utils import authenticate
from .models import UserModel, AuthTokenModel, PasswordModel
from .schemas import UserSchema, PasswordSchema , AuthTokenSchema


class UserApi(Resource):

    @authenticate
    def get(self, auth):
        user = UserModel.query.filter_by(id=auth['sub']).first()
        dump_user = UserSchema().dump(user)
        return success_msg(dump_user), 200

    def put(self):
        user_data = request.json
        password = user_data.pop('password', None)

        try:
            user_load = UserSchema().load(user_data)
        except ValidationError as e:
            return error_msg(e.messages), 400

        try:
            password_load = PasswordSchema().load({'password': password})
        except ValidationError as e:
            return  error_msg(e.messages), 400

        user = UserModel(**user_load)
        user.create(user)

        new_password = PasswordModel(userid=user.id)
        new_password.hash_password(password_load['password'])
        new_password.create(new_password)

        return success_msg(user_load), 201

    @authenticate
    def patch(self, auth):
        try:
            load_user = UserSchema().load(request.json)
        except ValidationError as e:
            return error_msg(e.messages), 404

        user = UserModel.query.filter_by(id=auth['sub']).first()
        user.update(load_user)

        return success_msg(load_user), 200

    @authenticate
    def delete(self, auth):
        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            return error_msg(msg.MISSING_ARGUMENT), 400

        user = UserModel.query.filter_by(username=username).first()
        if user is None or user.id is not auth['sub']:
            return error_msg(msg.VALIDATION_ERROR), 404

        user_password = PasswordModel.query.filter_by(userid=user.id).first()
        password_is_valid = user_password.verify_password(
            password,
            user_password.password_hash
        )
        if password_is_valid:
            user.delete(user)
            return {}, 204
        else:
            return error_msg(msg.AUTHORIZATION_ERROR), 401


class PasswordApi(Resource):

    @authenticate
    def post(self, auth):
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')

        if old_password is None or new_password is None:
            return error_msg(msg.MISSING_ARGUMENT), 400

        user_password = PasswordModel.query.filter_by(userid=auth['sub']).first()
        old_pssword_is_valid = user_password.verify_password(
            old_password,
            user_password.password_hash
        )

        if old_pssword_is_valid:
            try:
                password_schema = PasswordSchema().load({'password': new_password})
            except ValidationError as e:
                return error_msg(e.messages), 400

            user_password.hash_password(new_password)
            user_password.new_datetime()
            user_password.update()

            return success_msg({}), 201
        else:
            return error_msg(msg.INVALID_PASSWORD), 401


class AuthApi(Resource):

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            return error_msg(msg.MISSING_ARGUMENT), 400

        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return error_msg(msg.INVALID_USERNAME), 404

        user_password = PasswordModel.query.filter_by(userid=user.id).first()
        password_is_valid = user_password.verify_password(
            password,
            user_password.password_hash
        )

        if password_is_valid:
            user_token = AuthTokenModel.query.filter_by(userid=user.id).first()

            if user_token is None:
                new_auth = AuthTokenModel(userid=user.id)
                new_token = new_auth.get_auth_token(user.id)
                new_auth.create(new_auth)

                return success_msg({'auth_token': new_token}), 201
            else:
                new_token = user_token.get_auth_token(user.id)
                user_token.token = new_token
                user_token.update()

                return success_msg({'auth_token': new_token}), 201
        else:
            return error_msg(msg.INVALID_PASSWORD), 401

    @authenticate
    def delete(self, auth):
        user_auth_token = AuthTokenModel.query.filter_by(userid=auth['sub']).first()
        user_auth_token.delete(user_auth_token)
        return {}, 204


class HelloWorld(Resource):

    def get(self):
        return success_msg('Hello World'), 200
