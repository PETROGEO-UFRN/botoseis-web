from os import path
from types import SimpleNamespace
from typing import Literal

from server.app.errors.FileError import FileError
from ..models import WorkflowModel, DataSetModel


# ! needs fix for dataset
def showByWorkflowId(workflowId, path_type: Literal["input", "output"]):
    workflow = WorkflowModel.query.filter_by(id=workflowId).first()
    if path_type == "input":
        if not workflow.input_file_link_id:
            raise FileError("No input file found for this workflow")
        inputFilePath = workflow.getSelectedInputFile().path
        return {
            "file_path": inputFilePath
        }

    if path_type == "output":
        dataset = DataSetModel.query.filter_by(
            id=workflow.workflowParent.datasetId
        ).first()

        outputFilePath = path.join(
            path.dirname(workflow.getSelectedInputFile().path),
            "datasets",
            f"from_workflow_{dataset.originWorkflowId}",
            f"{workflow.output_name}.su"
        )
        return {
            "file_path": outputFilePath
        }


suFilePathController = SimpleNamespace(
    showByWorkflowId=showByWorkflowId
)
