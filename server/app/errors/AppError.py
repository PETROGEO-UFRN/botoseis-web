class AppError(Exception):
    def __init__(self, message: str, statusCode=400):
        self.message = message
        self.statusCode = statusCode
