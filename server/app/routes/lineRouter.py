from flask import Blueprint, request, jsonify


from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..controllers import lineController
from ..serializers.LineSerializer import LineCreateSchema, LineUpdateSchema
from ..models.LineModel import LineModel
from ..models.ProjectModel import ProjectModel

lineRouter = Blueprint(
    "line-routes",
    __name__,
    url_prefix="/line"
)


@lineRouter.route("/list/<projectId>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def listLines(_, projectId):
    lines = lineController.showByProjectId(projectId)
    return jsonify(lines)


@lineRouter.route("/create/<projectId>", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=LineCreateSchema)
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def createLine(userId, projectId):
    data = request.get_json()
    newLine = lineController.create(
        userId,
        projectId,
        data["name"]
    )
    return jsonify(newLine)


@lineRouter.route("/update/<lineId>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=LineUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=LineModel)
def updateLine(_, lineId):
    data = request.get_json()
    updatedLine = lineController.update(
        lineId,
        data["name"]
    )
    return jsonify(updatedLine)


@lineRouter.route("/delete/<lineId>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=LineModel)
def deleteLine(_, lineId):
    line = lineController.delete(lineId)
    return jsonify(line)
