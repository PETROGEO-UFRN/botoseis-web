from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..controllers import commandController
from ..repositories.OrderedCommandsListRepository import orderedCommandsListRepository

from ..serializers.CommandSerializer import CommandCreateSchema, CommandUpdateParametersSchema, CommandsUpdateOrderSchema
from ..models.WorkflowModel import WorkflowModel
from ..models.CommandModel import CommandModel


commandRouter = Blueprint(
    "command-routes",
    __name__,
    url_prefix="/command"
)


@commandRouter.route("/show/<id>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def showCommand(_, id):
    command = commandController.show(id)
    return jsonify(command)


@commandRouter.route("/create/<workflowId>", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=CommandCreateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def createCommand(userId, workflowId):
    data = request.get_json()
    newCommand = commandController.create(
        userId,
        workflowId,
        data["name"],
        data["parameters"],
        data["program_id"]
    )
    return jsonify(newCommand)


@commandRouter.route("/update/<id>/parameters", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=CommandUpdateParametersSchema)
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def updateCommand(_, id):
    data = request.get_json()
    updatedCommand = commandController.updateParameters(
        id,
        data["parameters"]
    )
    return jsonify(updatedCommand)


@commandRouter.route("/update/<id>/is_active", methods=['PUT'])
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def updateCommand(_, id):
    updatedCommand = commandController.updateIsActive(id)
    return jsonify(updatedCommand)


@commandRouter.route("/order/<workflowId>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=CommandsUpdateOrderSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateOrder(_, workflowId):
    # ! need refactor
    data = request.get_json()
    updatedCommandList = orderedCommandsListRepository.update(
        workflowId,
        data["newOrder"]
    )
    return jsonify(updatedCommandList)


@commandRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=CommandModel)
def deleteCommand(_, id):
    command = commandController.delete(id)
    return jsonify(command)
