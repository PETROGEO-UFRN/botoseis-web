from types import SimpleNamespace

from ..database.connection import database
from ..models.OrderedCommandsListModel import OrderedCommandsListModel
from ..errors.AppError import AppError


def create(workflowId):
    orderedCommandsList = OrderedCommandsListModel(
        workflowId=workflowId,
        commandIds=[],
    )
    database.session.add(orderedCommandsList)
    database.session.commit()
    return orderedCommandsList


def update(workflowId, newOrder):
    orderedCommandsList = OrderedCommandsListModel.query.filter_by(
        workflowId=workflowId
    ).first()
    if not orderedCommandsList:
        raise AppError("OrderedComandsList does not exist")

    orderedCommandsList.commandIds = newOrder
    database.session.commit()

    return orderedCommandsList.getCommands()


orderedCommandsListRepository = SimpleNamespace(
    create=create,
    update=update,
)
