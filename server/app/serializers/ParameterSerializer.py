from marshmallow import Schema, fields, ValidationError, validates_schema


class ParameterUpdateSchema(Schema):
    name = fields.String(required=False)
    description = fields.String(required=False)
    example = fields.String(required=False)
    input_type = fields.String(required=False)
    isRequired = fields.Boolean(required=False)

    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided.")
        
        if not any(field in data for field in ["name", "description", "example", "input_type", "isRequired"]):
            raise ValidationError("At least one of ['name', 'description', 'example', 'input_type', 'isRequired'] is required.")

