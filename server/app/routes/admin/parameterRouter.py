from flask import Blueprint, request, jsonify

from ...middlewares.decoratorsFactory import decorator_factory
from ...middlewares.validateRequestBody import validateRequestBody

from ...controllers.admin import parameterController
from ...serializers.ParameterSerializer import ParameterUpdateSchema

parameterRouter = Blueprint(
    "program-parameter-routes",
    __name__,
    url_prefix="/programs/parameters"
)


@parameterRouter.route("/list/<programId>", methods=['GET'])
def listPrograms(programId):
    programs = parameterController.showByProgramId(programId)
    return jsonify(programs)


@parameterRouter.route("/create/<programId>", methods=['POST'])
def createProgram(programId):
    newParameter = parameterController.create(programId)
    return jsonify(newParameter)


@parameterRouter.route("/update/<parameterId>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=ParameterUpdateSchema)
def updateParameter(parameterId):
    data = request.get_json()

    updatedParameter = parameterController.update(parameterId, data)
    return jsonify(updatedParameter)


@parameterRouter.route("/delete/<parameterId>", methods=['DELETE'])
def deleteProgram(parameterId):
    parameter = parameterController.delete(parameterId)
    return jsonify(parameter)
