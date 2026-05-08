from types import SimpleNamespace

from ..errors.AppError import AppError
from ..database.connection import database

from ..models.DataSetModel import DataSetModel


def showById(id):
    dataset = DataSetModel.query.filter_by(id=id).first()
    if not dataset:
        raise AppError("Dataset does not exist", 404)
    return dataset.getAttributes()


def showAll(workflowId):
    datasets = DataSetModel.query.filter_by(originWorkflowId=workflowId).all()
    if len(datasets) == 0:
        raise AppError("There are no datasets", 404)

    # ! to complex, could be refactored
    return [workflow for dataset in datasets for workflow in dataset.getWorkflows()]


def delete(id):
    dataset = DataSetModel.query.filter_by(id=id).first()
    if not dataset:
        raise AppError("Dataset does not exist", 404)

    database.session.delete(dataset)
    database.session.commit()

    return dataset.getAttributes()


datasetController = SimpleNamespace(
    showById=showById,
    showAll=showAll,
    delete=delete,
)
