from types import SimpleNamespace

from ...database.connection import database
from ...models.ProgramModel import ProgramModel
from ...models.ParameterModel import ParameterModel
from ...errors.AppError import AppError


def showByProgramId(programId):
    program = ProgramModel.query.filter_by(id=programId).first()
    if not program:
        raise AppError("Program does not exist", 404)
    
    parameters = ParameterModel.query.filter_by(programId=programId).all()
    if not parameters:
        return []

    return [parameter.getAttributes() for parameter in parameters]


def create(programId):
    program = ProgramModel.query.filter_by(
        id=programId
    ).first()
    if not program:
        raise AppError("Program does not exist", 404)

    newParameter = ParameterModel(
        name="",
        description="",
        example="",
        input_type="",
        isRequired=False,
        programId=programId
    )
    database.session.add(newParameter)
    database.session.commit()
    return newParameter.getAttributes()


def update(parameterId, parameterNewData):
    parameter = ParameterModel.query.filter_by(
        id=parameterId
    ).first()
    if not parameter:
        raise AppError("Parameter does not exist", 404)

    if "name" in parameterNewData:
        parameter.name = parameterNewData["name"]
    if "description" in parameterNewData:
        parameter.description = parameterNewData["description"]
    if "example" in parameterNewData:
        parameter.example = parameterNewData["example"]
    if "input_type" in parameterNewData:
        parameter.input_type = parameterNewData["input_type"]
    if "isRequired" in parameterNewData:
        parameter.isRequired = parameterNewData["isRequired"]

    database.session.commit()
    return parameter.getAttributes()


def delete(id):
    parameter = ParameterModel.query.filter_by(id=id).first()
    if not parameter:
        raise AppError("Parameter does not exist", 404)

    database.session.delete(parameter)
    database.session.commit()
    return parameter.getAttributes()


parameterController = SimpleNamespace(
    showByProgramId=showByProgramId,
    create=create,
    update=update,
    delete=delete,
)
