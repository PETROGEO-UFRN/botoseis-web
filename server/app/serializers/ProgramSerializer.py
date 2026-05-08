from marshmallow import Schema, fields


class ProgramCreateSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    # ! path_to_executable_file should be validated to system security
    path_to_executable_file = fields.String(required=True)

class ProgramUpdateSchema(ProgramCreateSchema):
    pass
