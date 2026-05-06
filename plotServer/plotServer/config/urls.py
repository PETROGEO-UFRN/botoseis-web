from os import getenv

baseServerURL = getenv(
    'API_URL',
    'http://localhost:5006'
)
