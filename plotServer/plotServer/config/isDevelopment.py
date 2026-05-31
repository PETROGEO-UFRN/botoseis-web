from os import getenv

__FLASK_ENV = getenv(
    'FLASK_ENV',
    False
)

isDevelopment = False if __FLASK_ENV == "PRODUCTION" else True
