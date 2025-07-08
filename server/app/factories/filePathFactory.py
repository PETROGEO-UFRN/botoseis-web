from os import path

from ..models.WorkflowModel import WorkflowModel
from ..models.UserModel import UserModel
from ..models.ProjectModel import ProjectModel


def _createFolderPath(user_email, projectId) -> str:
    folder_path = path.join(
        "static",
        user_email,
        str(projectId)
    )
    return folder_path


def createUploadedFilePath(input_file_name, projectId) -> str:
    project = ProjectModel.query.filter_by(id=projectId).first()
    user = UserModel.query.filter_by(id=str(project.userId)).first()

    filePath = path.join(
        _createFolderPath(user.email, projectId),
        input_file_name
    )

    return filePath


def createDatasetFilePath(originWorkflowId) -> str:
    workflow = WorkflowModel.query.filter_by(id=originWorkflowId).first()

    base_directory = _createFolderPath(
        workflow.owner_email,
        workflow.workflowParent.getProjectId()
    )
    directory = path.join(
        base_directory,
        "datasets",
        f"from_workflow_{originWorkflowId}"
    )
    target_file_name = f'{workflow.output_name}.su'

    target_file_path = path.join(
        directory,
        target_file_name
    )

    return target_file_path
