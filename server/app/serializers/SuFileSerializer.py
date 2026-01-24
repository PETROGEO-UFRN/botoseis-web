from marshmallow import Schema, fields


class SuFileUploadSchema(Schema):
    file = fields.Raw(required=True)
