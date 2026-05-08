from uuid import UUID
from types import SimpleNamespace

from ..database.connection import database
from ..models.ProjectModel import ProjectModel
from ..models.WorkflowModel import WorkflowModel
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from ..models.UserModel import UserModel
from ..errors.AppError import AppError


def showByUserId(userId):
    projects = ProjectModel.query.filter_by(
        userId=UUID(userId)
    ).all()
    if not projects:
        return []

    return [project.getAttributes() for project in projects]


def create(userId, newProjectName: str):
    user = UserModel.query.filter_by(id=UUID(userId)).first()

    newProject = ProjectModel(
        name=newProjectName,
        userId=user.id
    )
    database.session.add(newProject)
    database.session.commit()
    return newProject.getAttributes()


def updateName(projectId, newProjectName):
    project = ProjectModel.query.filter_by(
        id=projectId
    ).first()
    if not project:
        raise AppError("Project does not exist", 404)

    project.name = newProjectName
    database.session.commit()
    return project.getAttributes()


def delete(projectId):
    project = ProjectModel.query.filter_by(
        id=projectId
    ).first()
    if not project:
        raise AppError("Project does not exist", 404)

    database.session.delete(project)
    database.session.commit()
    return project.getAttributes()


def listWorkflowsByProjectId(projectId) -> list[dict[str, str]]:
    # ! breaks MVC !
    # * It does not include workflows inside lines
    project = ProjectModel.query.filter_by(
        id=projectId
    ).first()
    if not project:
        raise AppError("Project does not exist", 404)

    workflowParentAssociations = WorkflowParentsAssociationModel.query.filter_by(
        projectId=projectId
    ).all()

    if len(workflowParentAssociations) == 0:
        return []
    workflows = WorkflowModel.query.filter(
        WorkflowModel.id.in_(
            [association.workflowId for association in workflowParentAssociations]
        )
    ).all()

    return [workflow.getResumedAttributes() for workflow in workflows]


projectController = SimpleNamespace(
    showByUserId=showByUserId,
    create=create,
    updateName=updateName,
    delete=delete,
    listWorkflowsByProjectId=listWorkflowsByProjectId,
)
