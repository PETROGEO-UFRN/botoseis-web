from flask import Blueprint, request

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.validateRequestBody import validateRequestBody

from ..controllers import sessionController
from ..serializers.SessionSerializer import SessionCreateSchema

sessionRouter = Blueprint("session-routes", __name__, url_prefix="/session")


@sessionRouter.route("/", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=SessionCreateSchema)
def create():
    data = request.get_json()

    response = sessionController.create(data["email"], data["password"])
    return response


@sessionRouter.route("/validate", methods=['GET'])
def validate():
    token = request.cookies.get("Authorization")
    sessionController.validate(token)
    return ('', 204)
