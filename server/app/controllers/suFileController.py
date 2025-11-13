import subprocess
import json
from os import path, makedirs
from types import SimpleNamespace
from datetime import datetime
from flask import jsonify, make_response, current_app

from ..database.connection import database
from ..models.FileLinkModel import FileLinkModel
from ..models.WorkflowModel import WorkflowModel
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel

from ..services.datasetServices import createDataset, deleteDatasets
from ..factories.filePathFactory import createUploadedSUFilePath, createDatasetFilePath
from ..factories.seismicUnixCommandStringFactory import createSemicUnixCommandString
from ..factories.simplifiedProcessStringFactory import createSimplifiedProcessString

from ..errors.FileError import FileError


def listByProjectId(projectId):
    fileLinks = FileLinkModel.query.filter_by(
        projectId=projectId,
        data_type="su"
    ).all()

    # *** iterate fileLinks and convert it to list of dicts
    # *** so the api can return this as route response
    fileLinksResponse = list(map(
        lambda link: link.getAttributes(),
        fileLinks
    ))

    return fileLinksResponse


def create(file, projectId):
    filePath = createUploadedSUFilePath(
        projectId,
        file.filename
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

    # !!! seismicUnixProcessString is empty when running on pytest
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
        # *** delete datasets with the same output name as the new one
        deleteDatasets(workflow)
        datasetAttributes = createDataset(userId, workflowId)

        newFileLink = FileLinkModel(
            projectId=workflowParent.getProjectId(),
            datasetId=datasetAttributes["id"],
            path=target_file_path,
            data_type="su"
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

        responseBody = {
            "result_workflow_id": datasetAttributes["workflows"][0]["id"],
            "process_details": process_details
        }
        response = make_response(jsonify(responseBody))

        # ! cookie domain needs more testing
        cookie_domain = current_app.config.get("JWT_COOKIE_DOMAIN")
        if not cookie_domain:
            cookie_domain = None
        post_processing_options = json.loads(workflow.post_processing_options)
        if 'options' in post_processing_options:
            response.set_cookie(
                "velan_starter_props",
                json.dumps(post_processing_options["options"]),
                httponly=current_app.config["JWT_COOKIE_HTTPONLY"],
                secure=current_app.config["JWT_COOKIE_SECURE"],
                samesite=current_app.config["JWT_COOKIE_SAMESITE"],
                path="/",
                domain=cookie_domain
            )
        return response
    except Exception as error:
        return str(error)


suFileController = SimpleNamespace(
    listByProjectId=listByProjectId,
    create=create,
    update=update,
)
