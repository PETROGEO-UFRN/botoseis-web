from flask import Blueprint, send_file, request, jsonify

from ..errors.AppError import AppError

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..models.ProjectModel import ProjectModel
from ..models.WorkflowModel import WorkflowModel
from ..controllers.suFileController import suFileController

suFileRouter = Blueprint("su-file-routes", __name__, url_prefix="/su-file")


@suFileRouter.route("/list/<projectId>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def listSuFiles(_, projectId):
    fileLinksList = suFileController.listByProjectId(projectId)
    return jsonify(fileLinksList)


@suFileRouter.route("/create/<projectId>", methods=['POST'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def createSuFile(_, projectId):
    if 'file' not in request.files:
        raise AppError("No file part in the request")
    file = request.files['file']

    fileLink = suFileController.create(file, projectId)
    return {"fileLink": fileLink}


# *** maybe not a great domain once a new file can be generated
# *** with the chosen commands not necesserily ocurring an update
# *** at the base seismic data file
@suFileRouter.route("/update/<workflowId>", methods=['PUT'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def updateSuFile(userId, workflowId):
    process_logs = suFileController.update(userId, workflowId)
    return jsonify(process_logs)
