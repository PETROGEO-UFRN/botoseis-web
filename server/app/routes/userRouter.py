from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..serializers.UserSerializer import UserCreateSchema, UserUpdateSchema
from ..controllers import userController

userRouter = Blueprint("user-routes", __name__, url_prefix="/user")


@userRouter.route("/create", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=UserCreateSchema)
def createUser() -> dict[str, str]:
    data = request.get_json()

    newUser = userController.create(data)
    return jsonify(newUser)


# *** debug/test route, should be turned of on production
@userRouter.route("/list", methods=['GET'])
def listUsers() -> dict[str, str]:
    users = userController.showAll()
    return jsonify(users)


@userRouter.route("/update", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=UserUpdateSchema)
@decorator_factory(requireAuthentication)
def updateUser(userId: str) -> dict[str, str]:
    data = request.get_json()
    updatedUser = userController.update(userId, data)
    return jsonify(updatedUser)


@userRouter.route("/delete", methods=['DELETE'])
@decorator_factory(requireAuthentication)
def deleteUser(userId: str) -> dict[str, str]:
    user = userController.delete(userId)
    return jsonify(user)
