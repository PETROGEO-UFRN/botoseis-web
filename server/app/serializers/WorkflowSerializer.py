from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class WorkflowCreateSchema(Schema):
    name = fields.String(required=True)
    parentType = fields.String(
        required=True,
        # *** No "datasetId" becouse datasets should not be
        # *** created or modified in the route layer
        validate=validate.OneOf(["projectId", "lineId"])
    )


class WorkflowNameUpdateSchema(Schema):
    name = fields.String(required=True)


class WorkflowFileLinkUpdateSchema(Schema):
    fileLinkId = fields.Integer(required=True)


class WorkflowOutputNameUpdateSchema(Schema):
    outputName = fields.String(required=True)


class WorkflowPostProcessingUpdateSchema(Schema):
    key = fields.String(required=True)
    options = fields.Dict(
        required=True,
        keys=fields.String(required=True),
        values=fields.Raw(required=True)
    )

    @validates_schema
    def validate_options(self, data: dict[str, str | dict[str, any]]):
        """
        Validates that every value in the 'options' dictionary is a str or int.
        """
        for option_key, value in data['options'].items():
            if not isinstance(value, (str, int, float, bool)):
                raise ValidationError(
                    f"Value for key '{option_key}' at 'options' must be a primite. Got {type(value).__name__}.",
                    field_names=['options']
                )
