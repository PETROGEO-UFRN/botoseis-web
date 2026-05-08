from ..models.ProjectModel import ProjectModel
from ..models.LineModel import LineModel
from ..models.DataSetModel import DataSetModel

from ..errors.AppError import AppError


def validateWorkflowParent(parentTypeKey: str, parentId: str) -> None:
    if parentTypeKey == "lineId":
        line = LineModel.query.filter_by(id=parentId).first()
        if not line:
            raise AppError("Line does not exist", 409)
    elif parentTypeKey == "projectId":
        project = ProjectModel.query.filter_by(id=parentId).first()
        if not project:
            raise AppError("Project does not exist", 409)
    elif parentTypeKey == "datasetId":
        dataset = DataSetModel.query.filter_by(id=parentId).first()
        if not dataset:
            raise AppError("Dataset does not exist", 409)
