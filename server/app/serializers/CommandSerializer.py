from marshmallow import Schema, fields


class CommandCreateSchema(Schema):
    name = fields.String(required=True)
    # ! maybe should validate if it is a stringfied json
    parameters = fields.String(required=True)
    program_id = fields.Integer(required=True)


class CommandUpdateParametersSchema(Schema):
    # ! maybe should validate if it is a stringfied json
    parameters = fields.String(required=True)


class CommandsUpdateOrderSchema(Schema):
    newOrder = fields.List(cls_or_instance=fields.Integer, required=True)
