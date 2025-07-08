from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody

from ..controllers import workflowController
from ..serializers.WorkflowSerializer import WorkflowCreateSchema, WorkflowNameUpdateSchema, WorkflowFileLinkUpdateSchema, WorkflowOutputNameUpdateSchema
from ..models.WorkflowModel import WorkflowModel


workflowRouter = Blueprint(
    "workflow-routes",
    __name__,
    url_prefix="/workflow"
)


@workflowRouter.route("/show/<id>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showWorkflow(_, id):
    workflow = workflowController.showById(id)
    return jsonify(workflow)


# *** shall have an line id or project id the route params
@workflowRouter.route("/create/<parentId>", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowCreateSchema)
@decorator_factory(requireAuthentication)
def createWorkflow(userId, parentId):
    data = request.get_json()
    newWorkflow = workflowController.create(userId, data, parentId)
    return jsonify(newWorkflow)


# !missing test
@workflowRouter.route("/update/<workflowId>/name", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowNameUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateWorkflow(_, workflowId):
    # ! breaks MVC !
    data = request.get_json()
    updatedWorkflow = workflowController.updateName(
        workflowId,
        data["name"]
    )
    return jsonify(updatedWorkflow)


# !missing test
@workflowRouter.route("/update/<workflowId>/file", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowFileLinkUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateWorkflow(_, workflowId):
    # ! breaks MVC !
    data = request.get_json()
    updatedWorkflow = workflowController.updateFilePath(
        workflowId,
        data["fileLinkId"]
    )
    return jsonify(updatedWorkflow)

# !missing test


@workflowRouter.route("/update/<workflowId>/output-name", methods=['PUT'])
@decorator_factory(validateRequestBody, SerializerSchema=WorkflowOutputNameUpdateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateWorkflow(_, workflowId):
    # ! breaks MVC !
    data = request.get_json()
    updatedWorkflow = workflowController.updateOutput(
        workflowId,
        data["outputName"]
    )
    return jsonify(updatedWorkflow)


@workflowRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def deleteWorkflow(_, id):
    workflow = workflowController.delete(id)
    return jsonify(workflow)
