from marshmallow import Schema, fields, ValidationError, validates_schema


class ProgramGroupCreateSchema(Schema):
    name = fields.String(required=False)
    description = fields.String(required=False)

class ProgramGroupUpdateSchema(ProgramGroupCreateSchema):
    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided.")
        
        if not any(field in data for field in ["name", "description"]):
            raise ValidationError("At least one of ['name', 'description'] is required.")

