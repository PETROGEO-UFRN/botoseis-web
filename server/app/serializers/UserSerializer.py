from marshmallow import Schema, fields
from re import search

from ..errors.FormatError import FormatError


def validatePassword(password: str):
    passwordPattern = r"^.{8,}$"

    if not search(passwordPattern, password):
        raise FormatError("Invalid Credentials")


class UserUpdateSchema(Schema):
    name = fields.String(required=True)


class UserCreateSchema(UserUpdateSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validatePassword)
