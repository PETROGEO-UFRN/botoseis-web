class AuthError(Exception):
    def __init__(self, message: str = "Request not authorized"):
        self.message = message
        self.statusCode = 401
