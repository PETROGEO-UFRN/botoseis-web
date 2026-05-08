from marshmallow import ValidationError


class FormatError(ValidationError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.statusCode = 422
