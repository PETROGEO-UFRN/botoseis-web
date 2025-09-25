from flask import Blueprint, request, jsonify

from ..errors.AppError import AppError

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..models.ProjectModel import ProjectModel
from ..controllers.helperFileController import helperFileController

helperFileRouter = Blueprint(
    "helper-file-routes",
    __name__,
    url_prefix="/helper-file"
)


@helperFileRouter.route("/list/<projectId>/models", methods=['GET'])
@helperFileRouter.route("/list/<projectId>/tables", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def listHelperFiles(_, projectId):
    if "/models" in str(request.url_rule):
        data_type = "model"
    if "/tables" in str(request.url_rule):
        data_type = "table"

    fileLinksList = helperFileController.listByProjectId(
        projectId,
        data_type
    )
    return jsonify(fileLinksList)


@helperFileRouter.route("/create/<projectId>/model", methods=['POST'])
@helperFileRouter.route("/create/<projectId>/table", methods=['POST'])
@decorator_factory(requireAuthentication, routeModel=ProjectModel)
def createHelperFile(_, projectId):
    if 'file' not in request.files:
        raise AppError("No file part in the request")
    file = request.files['file']

    if "/model" in str(request.url_rule):
        data_type = "model"
    if "/table" in str(request.url_rule):
        data_type = "table"

    fileLink = helperFileController.create(
        file,
        projectId,
        data_type,
    )
    return {"fileLink": fileLink}
