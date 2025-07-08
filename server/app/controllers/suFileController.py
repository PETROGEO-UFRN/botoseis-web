from os import path, makedirs
from types import SimpleNamespace
import subprocess
from datetime import datetime

from ..database.connection import database
from ..models.FileLinkModel import FileLinkModel
from ..models.WorkflowModel import WorkflowModel
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel

from ..services.datasetServices import createDataset, deleteDatasets
from ..factories.filePathFactory import createUploadedFilePath, createDatasetFilePath
from ..factories.seismicUnixCommandStringFactory import createSemicUnixCommandString
from ..factories.simplifiedProcessStringFactory import createSimplifiedProcessString

from ..errors.FileError import FileError


def listByProjectId(projectId):
    fileLinks = FileLinkModel.query.filter_by(projectId=projectId).all()

    # *** iterate fileLinks and convert it to list of dicts
    # *** so the api can return this as route response
    fileLinksResponse = list(map(
        lambda link: link.getAttributes(),
        fileLinks
    ))

    return fileLinksResponse


def create(file, projectId):
    filePath = createUploadedFilePath(
        file.filename,
        projectId
    )

    newFileLink = FileLinkModel(
        projectId=projectId,
        path=filePath,
        data_type="su",
    )
    database.session.add(newFileLink)
    database.session.commit()

    directory = path.dirname(filePath)
    if not path.exists(directory):
        makedirs(directory)
    file.save(filePath)

    return newFileLink.getAttributes()


def update(userId, workflowId):
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    workflowParent = WorkflowParentsAssociationModel.query.filter_by(
        workflowId=workflowId
    ).first()

    if not workflow.output_name:
        raise FileError("Output name should be set before running workflow")
    if not workflow.input_file_link_id:
        raise FileError("Input file should be set before running workflow")

    source_file_path = workflow.getSelectedInputFile().path
    target_file_path = createDatasetFilePath(workflowId)

    datasetsDirectory = path.dirname(target_file_path)
    if not path.exists(datasetsDirectory):
        makedirs(datasetsDirectory)

    seismicUnixProcessString = createSemicUnixCommandString(
        workflow.orderedCommandsList,
        source_file_path,
        target_file_path
    )

    try:
        processStartTime = datetime.now()
        process_output = subprocess.run(
            seismicUnixProcessString,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as error:
        return str(error)
    finally:
        # *** delete datasets with the same output name as the new one
        deleteDatasets(workflow)
        datasetAttributes = createDataset(userId, workflowId)

        newFileLink = FileLinkModel(
            projectId=workflowParent.getProjectId(),
            datasetId=datasetAttributes["id"],
            data_type="su",
            path=target_file_path
        )
        database.session.add(newFileLink)
        database.session.commit()

        process_details = {
            "executionSimplifiedString": createSimplifiedProcessString(process_output),
            "logMessage": process_output.stderr,
            "returncode": process_output.returncode,
            "processStartTime": processStartTime,
            "executionEndTime": datetime.now(),
        }
        return {
            "result_workflow_id": datasetAttributes["workflows"][0]["id"],
            "process_details": process_details
        }


suFileController = SimpleNamespace(
    listByProjectId=listByProjectId,
    create=create,
    update=update,
)
