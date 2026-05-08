from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..controllers import projectController
from ..serializers.ProjectSerializer import ProjectCreateSchema, ProjectUpdateSchema
from ..models.ProjectModel import ProjectModel

projectRouter = Blueprint(
    "project-routes",
    __name__,
    url_prefix="/project"
)


@projectRouter.route("/list", methods=['GET'])
@decorator_factory(requireAuthentication)
def showProject(userId):
    project = projectController.showByUserId(userId)
    return jsonify(project)


@projectRouter.route("/create", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=ProjectCreateSchema)
@decorator_factory(requireAuthentication)
def createProject(userId):
    data = request.get_json()
    newProject = projectController.create(userId, data["name"])
    return jsonify(newProject)


@projectRouter.route("/update/<id>", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=ProjectUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def updateProject(_, id):
    data = request.get_json()
    updatedProject = projectController.updateName(id, data["name"])
    return jsonify(updatedProject)


@projectRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def deleteProject(_, id):
    project = projectController.delete(id)
    return jsonify(project)


# ! breaks MVC !
# * It does not include workflows inside lines
@projectRouter.route("/root-workflows/list/<id>", methods=['GET'])  # ??
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def listProjectRootWorkflows(_, id):
    projectWorkflows = projectController.listWorkflowsByProjectId(id)
    return jsonify(projectWorkflows)
