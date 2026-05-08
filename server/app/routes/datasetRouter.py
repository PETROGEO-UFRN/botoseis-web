from flask import Blueprint, jsonify

from ..models.DataSetModel import DataSetModel
from ..middlewares.requireAuthentication import requireAuthentication
from ..middlewares.decoratorsFactory import decorator_factory

from ..controllers import datasetController

datasetRouter = Blueprint("dataset-routes", __name__, url_prefix="/dataset")


@datasetRouter.route("/delete/<id>", methods=['DELETE'])
@decorator_factory(requireAuthentication, routeModel=DataSetModel)
def deleteDataset(_, id):
    dataset = datasetController.delete(id)
    return jsonify(dataset)


@datasetRouter.route("/show/<id>", methods=['GET'])
@decorator_factory(requireAuthentication, routeModel=DataSetModel)
def showDataset(_, id):
    dataset = datasetController.showById(id)
    return jsonify(dataset)


@datasetRouter.route("/list/<workflowId>", methods=['GET'])
# @decorator_factory(requireAuthentication, routeModel=DataSetModel)
def listDatasets(workflowId):
    datasets = datasetController.showAll(workflowId)
    return jsonify(datasets)
