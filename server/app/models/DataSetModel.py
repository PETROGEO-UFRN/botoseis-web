import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .WorkflowModel import WorkflowModel
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel


class DataSetModel(database.Model):
    __tablename__ = "datasets_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)

    owner_email = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.email",
        name="FK_users_table_dataset_table"
    ))

    originWorkflowId = dbTypes.Column(dbTypes.ForeignKey(
        "workflows_table.id",
        name="FK_workflows_tables_datasets_table",
        ondelete="CASCADE"
    ))

    workflowParentAssociations: Mapped[
        List[WorkflowParentsAssociationModel]
    ] = relationship(
        WorkflowParentsAssociationModel,
        passive_deletes=True
    )

    def getWorkflows(self) -> list[dict[str, str]]:
        if len(self.workflowParentAssociations) == 0:
            return []
        workflows = WorkflowModel.query.filter(
            WorkflowModel.id.in_(
                [association.workflowId for association in self.workflowParentAssociations]
            )
        ).all()
        return [workflow.getAttributes() for workflow in workflows]

    def getAttributes(self) -> dict:
        return {
            "id": self.id,
            "workflows": self.getWorkflows()
        }
