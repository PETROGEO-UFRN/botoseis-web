from .AuthError import AuthError


class AdminError(AuthError):
    def __init__(self):
        self.message = "User not authorized to do this action"
        self.statusCode = 403
