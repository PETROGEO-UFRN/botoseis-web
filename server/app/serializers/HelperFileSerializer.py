from marshmallow import Schema, fields


class PickDataSchema(Schema):
    x = fields.List(fields.Float(), required=True)
    y = fields.List(fields.Float(), required=True)


class HelperFileUploadSchema(Schema):
    file = fields.Raw(required=True)


class TableFileGenerateSchema(Schema):
    picks = fields.Dict(
        keys=fields.Integer(),
        values=fields.Nested(PickDataSchema),
        required=True
    )
