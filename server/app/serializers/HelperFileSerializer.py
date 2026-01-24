from marshmallow import Schema, fields


class TableHelperFileUploadSchema(Schema):
    file = fields.Raw(required=True)
