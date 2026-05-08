from marshmallow import Schema, fields


class SessionCreateSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
