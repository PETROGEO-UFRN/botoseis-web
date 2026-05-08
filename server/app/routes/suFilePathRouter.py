from flask import Blueprint, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..models.WorkflowModel import WorkflowModel
from ..controllers.suFilePathController import suFilePathController


suFilePathRouter = Blueprint(
    "su-file-name-routes",
    __name__,
    url_prefix="/su-file-path"
)


@suFilePathRouter.route("/<workflowId>/show-path/<path_type>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def showSuFilePath(_, workflowId, path_type):
    file_path = suFilePathController.showByWorkflowId(workflowId, path_type)
    return jsonify(file_path)
