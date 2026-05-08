import sqlalchemy as dbTypes

from ..database.connection import database


class WorkflowParentsAssociationModel(database.Model):
    __tablename__ = "workflow_parents_association_table"

    workflowId = dbTypes.Column(
        dbTypes.ForeignKey(
            "workflows_table.id",
            name="FK_workflow_parents_association_table_workflows_table",
            ondelete="CASCADE"
        ),
        primary_key=True,
    )

    datasetId = dbTypes.Column(dbTypes.ForeignKey(
        "datasets_table.id",
        name="FK_workflow_parents_association_table_dataset_table",
        ondelete="CASCADE"
    ))
    lineId = dbTypes.Column(dbTypes.ForeignKey(
        "lines_table.id",
        name="FK_workflow_parents_association_table_lines_table",
        ondelete="CASCADE"
    ))
    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_workflow_parents_association_table_projects_table",
        ondelete="CASCADE"
    ))

    def getProjectId(self) -> int:
        # *** import inside function to avoid circular import
        # ! do not turn into global import
        from .LineModel import LineModel

        if self.projectId:
            return self.projectId
        if self.lineId:
            line = LineModel.query.filter_by(id=self.lineId).first()
            return line.projectId

    def getParentType(self) -> str:
        if self.projectId:
            return "project"
        if self.lineId:
            return "line"
        if self.datasetId:
            return "dataset"

    def getAttributes(self):
        return {
            "projectId": self.projectId,
            "lineId": self.lineId,
            "workflowId": self.workflowId,
        }
