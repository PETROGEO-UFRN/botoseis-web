import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .CommandModel import CommandModel
from .OrderedCommandsListModel import OrderedCommandsListModel
from .WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from .FileLinkModel import FileLinkModel


class WorkflowModel(database.Model):  # type: ignore
    __tablename__ = "workflows_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    output_name = dbTypes.Column(dbTypes.String)

    input_file_link_id = dbTypes.Column(dbTypes.ForeignKey(
        "file_link_table.id",
        name="FK_file_links_table_workflows_table"
    ))

    owner_email = dbTypes.Column(dbTypes.ForeignKey(
        "users_table.email",
        name="FK_users_table_workflows_table"
    ))

    commands: Mapped[
        List[CommandModel]
    ] = relationship(CommandModel, cascade='all, delete-orphan')

    orderedCommandsList: Mapped[
        List[OrderedCommandsListModel]
    ] = relationship(OrderedCommandsListModel, cascade='all, delete-orphan')

    workflowParent: Mapped[
        WorkflowParentsAssociationModel
    ] = relationship(
        WorkflowParentsAssociationModel,
        cascade="all, delete-orphan",
    )

    def getSelectedInputFile(self):
        fileLink = FileLinkModel.query.filter_by(
            id=self.input_file_link_id
        ).first()
        return fileLink

    def getResumedAttributes(self) -> dict[str, str | int]:
        return {
            "id": self.id,
            "name": self.name,
        }

    def getAttributes(self) -> dict[str, str | int | dict[str, str | int]]:
        return {
            "id": self.id,
            "name": self.name,
            "input_file_link_id": self.input_file_link_id,
            "output_name": self.output_name,
            "commands": self.orderedCommandsList[0].getCommands(),
            "parentType": self.workflowParent.getParentType(),
        }
