from os import getenv

BASE_API_URL = getenv(
    'API_URL',
    'http://localhost:5000'
)

__FLASK_ENV = getenv(
    'FLASK_ENV',
    False
)

IS_DEVELOPMENT = False if __FLASK_ENV == "PRODUCTION" else True
