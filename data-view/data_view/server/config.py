from os import getenv

BASE_URL = getenv(
    'API_URL',
    'http://localhost:5000'
)

FLASK_ENV = getenv(
    'FLASK_ENV',
    False
)

IS_DEVELOPMENT = False if FLASK_ENV == "PRODUCTION" else True
