from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody
from ..serializers.HelperFileSerializer import TableHelperFileUploadSchema
from ..models.LineModel import LineModel
from ..controllers.helperFileController import helperFileController

helperFileRouter = Blueprint(
    "helper-file-routes",
    __name__,
    url_prefix="/helper-file"
)


@helperFileRouter.route("/list/<lineId>/models", methods=['GET'])
@helperFileRouter.route("/list/<lineId>/tables", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=LineModel)
def listHelperFiles(_, lineId):
    if "/models" in str(request.url_rule):
        data_type = "model"
    if "/tables" in str(request.url_rule):
        data_type = "table"

    fileLinksList = helperFileController.listByLineId(
        lineId,
        data_type
    )
    return jsonify(fileLinksList)


@helperFileRouter.route("/upload/<lineId>/model", methods=['POST'])
@helperFileRouter.route("/upload/<lineId>/table", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=TableHelperFileUploadSchema)
@decorator_factory(requireAuthentication, routeModel=LineModel)
def createHelperFile(_, lineId):
    file = request.files['file']

    if "/model" in str(request.url_rule):
        data_type = "model"
    if "/table" in str(request.url_rule):
        data_type = "table"

    fileLink = helperFileController.create(
        file=file,
        lineId=lineId,
        data_type=data_type,
    )
    return {"fileLink": fileLink}
