import re
import json
from types import SimpleNamespace

from ..database.connection import database
from ..models.WorkflowModel import WorkflowModel
from ..models.HelperFileLinkModel import HelperFileLinkModel

from ..errors.AppError import AppError
from ..factories.postProcessingOptionsFactory import createPostProcessingOptions
from ..repositories.WorkflowRepository import workflowRepository
from ..repositories.WorkflowParentsAssociationRepository import workflowParentsAssociationRepository
from ..repositories.OrderedCommandsListRepository import orderedCommandsListRepository


def showById(id):
    workflow = WorkflowModel.query.filter_by(id=id).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    return workflow.getAttributes()


def create(userId, newWorkflowData, parentId):
    newWorkflow = workflowRepository.create(userId, newWorkflowData, parentId)

    workflowParentsAssociationRepository.create(
        newWorkflow.id,
        newWorkflowData["parentType"],
        parentId
    )
    orderedCommandsListRepository.create(newWorkflow.id)

    return newWorkflow.getAttributes()


def updateName(workflowId, name):
    # ! breaks MVC !
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    workflow.name = name
    database.session.commit()
    return workflow.getResumedAttributes()


def updateInputFilePath(workflowId, fileLinkId):
    # ! breaks MVC !
    workflow = workflowRepository.updateInputFilePath(workflowId, fileLinkId)
    return workflow.getAttributes()


def updateWorkflowPicksTable(workflowId, helperFileLinkId):
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    helperFileLink = HelperFileLinkModel.query.filter_by(
        id=helperFileLinkId
    ).first()
    if not helperFileLink:
        raise AppError("Workflow does not exist", 404)

    workflow.picks_table_file_id = helperFileLink.id


def updateOutput(workflowId, newOutputValue):
    # ! breaks MVC !
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    workflow.output_name = re.sub(r'[^a-zA-Z0-9\-_()]', '', newOutputValue)
    database.session.commit()
    return workflow.getAttributes()


def updatePostProcessingOptions(workflowId, key, options):
    # ! breaks MVC !
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    workflow.post_processing_options = createPostProcessingOptions(
        key=key,
        options=options,
    )
    database.session.commit()

    return {
        "post_processing_options": json.loads(workflow.post_processing_options)
    }


def delete(id):
    workflow = WorkflowModel.query.filter_by(id=id).first()
    if not workflow:
        raise AppError("Workflow does not exist", 404)

    database.session.delete(workflow)
    database.session.commit()
    return workflow.getAttributes()


workflowController = SimpleNamespace(
    showById=showById,
    create=create,
    updateName=updateName,
    updateWorkflowPicksTable=updateWorkflowPicksTable,
    updateInputFilePath=updateInputFilePath,
    updateOutput=updateOutput,
    updatePostProcessingOptions=updatePostProcessingOptions,
    delete=delete,
)
