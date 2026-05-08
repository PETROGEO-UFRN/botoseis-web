import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from .WorkflowModel import WorkflowModel


class LineModel(database.Model):  # type: ignore
    __tablename__ = "lines_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)

    owner_email = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.email",
        name="FK_users_table_lines_table"
    ))

    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_projects_table_lines_table"
    ))
    workflowParentAssociations: Mapped[
        List[WorkflowParentsAssociationModel]
    ] = relationship(WorkflowParentsAssociationModel)

    def _getWorkflows(self) -> list[dict[str, str]]:
        if len(self.workflowParentAssociations) == 0:
            return []
        workflows = WorkflowModel.query.filter(
            WorkflowModel.id.in_(
                [association.workflowId for association in self.workflowParentAssociations]
            )
        ).all()
        return [workflow.getResumedAttributes() for workflow in workflows]

    def getAttributes(self) -> dict[str, str | list[dict[str, str]]]:
        return {
            "id": self.id,
            "projectId": self.projectId,
            "name": self.name,
            "workflows": self._getWorkflows()
        }
