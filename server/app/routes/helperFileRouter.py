from flask import Blueprint, request, jsonify

from ..middlewares.decoratorsFactory import decorator_factory
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.validateRequestBody import validateRequestBody
from ..serializers.HelperFileSerializer import HelperFileUploadSchema, TableFileGenerateSchema
from ..models.LineModel import LineModel
from ..models.WorkflowModel import WorkflowModel
from ..models.DataSetModel import DataSetModel
from ..models.HelperFileLinkModel import HelperFileLinkModel
from ..factories.pickingASCTableFactory import createPickingASCTable
from ..factories.pickingDictFactory import createPickingDict
from ..controllers.helperFileController import helperFileController
from ..controllers.workflowController import workflowController
from ..errors.AppError import AppError

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
@decorator_factory(validateRequestBody, SerializerSchema=HelperFileUploadSchema)
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


@helperFileRouter.route("/path/<workflowId>/table", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def getTableHelperFile(_, workflowId):

    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    table_file = HelperFileLinkModel.query.filter_by(
        id=workflow.picks_table_file_id
    ).first()

    picks = createPickingDict(table_file.path)

    return {'picks': picks}


@helperFileRouter.route("/generate/<workflowId>/table", methods=['POST'])
@decorator_factory(validateRequestBody, SerializerSchema=TableFileGenerateSchema)
@decorator_factory(requireAuthentication, routeModel=WorkflowModel)
def generateTableHelperFile(_, workflowId):
    data = request.get_json()

    workflow = WorkflowModel.query.filter_by(id=workflowId).first()

    lineId = workflow.workflowParent.lineId
    if not lineId:
        try:
            # *** consider workflow as dataset result
            originWorkflowId = DataSetModel.query.filter_by(
                id=workflow.workflowParent.datasetId
            ).first().originWorkflowId
            originWorkflow = WorkflowModel.query.filter_by(
                id=originWorkflowId
            ).first()
            lineId = originWorkflow.workflowParent.lineId
        except:
            raise AppError("Workflow missing lineId", 500)

    file = createPickingASCTable(data['picks'])
    file.filename = f"table_from_workflow_{workflow.id}.dat"

    fileLink = helperFileController.create(
        file=file,
        lineId=lineId,
        data_type='table',
    )

    workflowController.updateWorkflowPicksTable(
        helperFileLinkId=fileLink["id"],
        workflowId=workflowId,
    )

    return {"fileLink": fileLink}
