from json import dumps
from types import SimpleNamespace
from copy import copy

from ..database.connection import database
from ..models.CommandModel import CommandModel
from ..models.OrderedCommandsListModel import OrderedCommandsListModel

from ..repositories.CommandRepository import commandRepository
from ..repositories.OrderedCommandsListRepository import orderedCommandsListRepository
from ..errors.AppError import AppError


def show(id):
    command = CommandModel.query.filter_by(id=id).first()
    return command.getAttributes()


def create(userId, workflowId, name, parameters, program_id):
    newCommand = commandRepository.create(
        userId,
        workflowId,
        name,
        parameters,
        program_id
    )
    return newCommand.getAttributes()


def updateParameters(id, newParameters):
    if isinstance(newParameters, dict):
        newParameters = dumps(newParameters)
    command = CommandModel.query.filter_by(id=id).first()
    if not command:
        raise AppError("Command does not exist", 404)

    command.parameters = newParameters
    database.session.commit()

    return command.getAttributes()


def updateIsActive(id):
    command = CommandModel.query.filter_by(id=id).first()
    if not command:
        raise AppError("Command does not exist", 404)
    command.is_active = not command.is_active
    database.session.commit()

    return command.getAttributes()


def delete(id):
    command = CommandModel.query.filter_by(id=id).first()
    if not command:
        raise AppError("Command does not exist", 404)

    orderedCommandsList = OrderedCommandsListModel.query.filter_by(
        workflowId=command.workflowId
    ).first()

    # ? not sure "copy" is necessary, but removing directly from
    # ? original orderedCommandsList was not working
    tempOrderedCommandsList = copy(orderedCommandsList.commandIds)
    tempOrderedCommandsList.remove(int(id))
    
    orderedCommandsListRepository.update(
        command.workflowId,
        tempOrderedCommandsList
    )

    database.session.delete(command)
    database.session.commit()

    return command.getAttributes()


commandController = SimpleNamespace(
    show=show,
    create=create,
    updateParameters=updateParameters,
    updateIsActive=updateIsActive,
    delete=delete,
)
