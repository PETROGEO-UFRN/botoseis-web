from uuid import UUID
from copy import copy
from types import SimpleNamespace

from ..models.UserModel import UserModel
from ..database.connection import database
from ..models.CommandModel import CommandModel
from ..models.OrderedCommandsListModel import OrderedCommandsListModel
from ..models.WorkflowModel import WorkflowModel
from ..models.ProgramModel import ProgramModel
from ..errors.AppError import AppError


def create(userId, workflowId, name, parameters, program_id):
    user = UserModel.query.filter_by(id=UUID(userId)).first()
    if not user:
        raise AppError("User does not exist", 404)
    
    program = ProgramModel.query.filter_by(id=program_id).first()
    if not program:
        raise AppError("Program does not exist", 404)

    workflow = WorkflowModel.query.filter_by(
        id=workflowId
    ).first()
    if not workflow:
        raise AppError("Workflow does not exist", 409)

    orderedCommandsList = OrderedCommandsListModel.query.filter_by(
        workflowId=workflowId
    ).first()

    newCommand = CommandModel(
        name=name,
        parameters=parameters,
        workflowId=workflowId,
        owner_email=user.email,
        program_id=program_id,
        # *** "is_active" usually will be True, so it shall be initialized as True
        is_active=True
    )

    database.session.add(newCommand)
    database.session.commit()

    newCommandsList = copy(orderedCommandsList.commandIds)
    newCommandsList.append(newCommand.id)
    orderedCommandsList.commandIds = newCommandsList

    database.session.commit()

    return newCommand


commandRepository = SimpleNamespace(
    create=create,
)
