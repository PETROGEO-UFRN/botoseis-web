from uuid import UUID
from types import SimpleNamespace

from ..database.connection import database
from ..models.UserModel import UserModel
from ..models.WorkflowModel import WorkflowModel
from ..models.FileLinkModel import FileLinkModel
from ..factories.postProcessingOptionsFactory import createPostProcessingOptions

from ..errors.AppError import AppError
from ..services.validateWorkflowParent import validateWorkflowParent


def create(userId, newWorkflowData, parentId):
    parentType = newWorkflowData["parentType"]

    user = UserModel.query.filter_by(id=UUID(userId)).first()

    # ! raise error when find any issue
    # ! thats unused here, parents domain shall be refactored
    validateWorkflowParent(parentType, parentId)

    newWorkflow = WorkflowModel(
        name=newWorkflowData["name"],
        owner_email=user.email,
        output_name=newWorkflowData.get("output_name") or "",
        post_processing_options=(createPostProcessingOptions())
    )

    database.session.add(newWorkflow)
    database.session.commit()

    return newWorkflow


def updateFilePath(workflowId, fileLinkId):
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    if not workflow:
        raise AppError("Workflow does not exist", 409)

    fileLink = FileLinkModel.query.filter_by(id=fileLinkId).first()
    if not fileLink:
        raise AppError("FileLink does not exist", 409)

    workflow.input_file_link_id = fileLink.id

    database.session.commit()
    return workflow


workflowRepository = SimpleNamespace(
    create=create,
    updateFilePath=updateFilePath,
)
