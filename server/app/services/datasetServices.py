from uuid import UUID
from copy import copy

from ..database.connection import database
from ..models.UserModel import UserModel
from ..models.DataSetModel import DataSetModel
from ..models.WorkflowModel import WorkflowModel
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from ..models.CommandModel import CommandModel

from ..repositories.WorkflowRepository import workflowRepository
from ..repositories.CommandRepository import commandRepository
from ..repositories.OrderedCommandsListRepository import orderedCommandsListRepository
from ..repositories.WorkflowParentsAssociationRepository import workflowParentsAssociationRepository


def createDataset(userId, originWorkflowId) -> dict:
    # *** this method duplicate a workflow and keep it as history
    # *** being chidren of the dataset table.
    # *** Keeping the generated file and the workflow used to get it
    user = UserModel.query.filter_by(id=UUID(userId)).first()

    originWorkflow = WorkflowModel.query.filter_by(
        id=originWorkflowId
    ).first()

    commands = CommandModel.query.filter_by(
        workflowId=originWorkflowId
    ).all()

    dataset = DataSetModel(
        originWorkflowId=originWorkflowId,
        owner_email=user.email
    )
    database.session.add(dataset)
    database.session.commit()

    newWorkflowData = {
        "name": f"{originWorkflow.name} - dataset",
        "parentType": "datasetId",
        "output_name": originWorkflow.output_name,
    }

    newWorkflow = workflowRepository.create(
        userId,
        newWorkflowData,
        dataset.id,
    )
    orderedCommandsList = orderedCommandsListRepository.create(newWorkflow.id)

    workflowParentsAssociationRepository.create(
        newWorkflow.id,
        "datasetId",
        dataset.id
    )

    workflowRepository.updateFilePath(
        newWorkflow.id,
        originWorkflow.input_file_link_id
    )

    # ? not sure "copy" is necessary, but removing directly from
    # ? original orderedCommandsList was not working
    tempOrderedCommandsList = copy(orderedCommandsList.commandIds)

    for command in commands:
        # *** no need to save the commented command at dataset history
        if not command.is_active:
            tempOrderedCommandsList.remove(int(id))
            continue
        commandRepository.create(
            userId,
            newWorkflow.id,
            command.name,
            command.parameters,
            command.program_id
        )
        database.session.add(command)

    database.session.commit()

    return dataset.getAttributes()


def deleteDatasets(originWorkflow):
    # *** overwrite any dataset with the same output name
    datasets_to_delete = DataSetModel.query \
        .join(WorkflowParentsAssociationModel, DataSetModel.id == WorkflowParentsAssociationModel.datasetId) \
        .join(WorkflowModel, WorkflowModel.id == WorkflowParentsAssociationModel.workflowId) \
        .filter(WorkflowModel.output_name == originWorkflow.output_name) \
        .all()
    for dataset in datasets_to_delete:
        if dataset.workflowParentAssociations:
            workflow_to_delete = WorkflowModel.query.filter_by(
                id=dataset.workflowParentAssociations[0].workflowId
            ).first()
            # dataset.workflowParentAssociations
            database.session.delete(workflow_to_delete)
        database.session.delete(dataset)
