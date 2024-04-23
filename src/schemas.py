"""
This module defines data schemas using Marshmallow for serializing
and deserializing data in the application.

Dependencies:
* Marshmallow: A library for object serialization/deserialization.

Doc: https://marshmallow.readthedocs.io/en/stable/
"""
import re
from typing import Optional

from marshmallow import Schema, fields, validate, validates, ValidationError

from .messages import ApiMessages as msg
from .models import UserModel, PasswordModel, AuthTokenModel


class UserSchema(Schema):

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'confirm_user')

    username = fields.Str(required=True, validate=validate.Length(max=60))
    email = fields.Email(required=True, validate=validate.Length(max=60))

    @validates('username')
    def validate_username(self, value: str) -> Optional[dict]:
        if len(value) < 4:
            raise ValidationError(msg.USERNAME_ISTO_SHORT_ERROR)

        if value.isdigit() is True:
            raise ValidationError(msg.USERNAME_IS_ALL_DIGITS_ERROR)

        existing_user = UserModel.query.filter_by(username=value).first()
        if existing_user is not None:
            raise ValidationError(msg.USER_EXIST)

    @validates('email')
    def validate_email(self, value: str) -> Optional[dict]:
        if len(value) == 0 or '@' not in value or '.' not in value:
            raise ValidationError(msg.EMAIL_INVALID_FORMAT_ERROR)

        existing_user = UserModel.query.filter_by(email=value).first()
        if existing_user is not None:
            raise ValidationError(msg.EMAIL_EXIST)


class PasswordSchema(Schema):

    password = fields.Str(required=True, validate=validate.Length(min=8, max=60))

    @validates('password')
    def validate_password(self, value: str) -> Optional[dict]:
        """
        Checking uppercase and lowercase letters,
        numbers and special characters.
        """
        if not re.search(r'[A-Z]', value) \
                or not re.search(r'[a-z]', value) \
                or not re.search(r'\d', value) \
                or not re.search(r'[^A-Za-z0-9]', value) \
                or not re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?/~`]", value):
            raise ValidationError(msg.PASSWORD_ISNOT_SECURE_ERROR)


class AuthTokenSchema(Schema):

    class Meta:
        model = AuthTokenModel
        fields = ('id', 'userid', 'token')
