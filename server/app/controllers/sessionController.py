from types import SimpleNamespace

from flask import jsonify, make_response, current_app
from jwt import encode

from ..errors.AuthError import AuthError
from ..models.UserModel import UserModel
from ..config.private_key import private_key

from ..services.passwordServices import checkPassword
from ..services.validateToken import validateToken


def create(email, password):
    user = UserModel.query.filter_by(email=email).first()
    if not user or not checkPassword(password, user.password):
        raise AuthError("Invalid email or password")

    try:
        token = encode(
            payload=user.getAttributes(),
            key=private_key,
            algorithm="HS256"
        )
    except:
        raise AuthError("Could not generate token")

    response = make_response(jsonify({"message": "Logged in"}))

    # ! cookie domain needs more testing
    cookie_domain = current_app.config.get("JWT_COOKIE_DOMAIN")
    if not cookie_domain:
        cookie_domain = None
    response.set_cookie(
        "Authorization",
        token,
        httponly=current_app.config["JWT_COOKIE_HTTPONLY"],
        secure=current_app.config["JWT_COOKIE_SECURE"],
        samesite=current_app.config["JWT_COOKIE_SAMESITE"],
        path="/",
        domain=cookie_domain
    )

    return response


def validate(token: str):
    payload = validateToken(token)
    return payload


def revalidate():
    # todo: revalidateSession shall be implemented but is not a priority
    pass


sessionController = SimpleNamespace(
    create=create,
    validate=validate,
    revalidate=revalidate,
)
