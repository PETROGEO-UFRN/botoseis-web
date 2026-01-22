import sqlalchemy as dbTypes
from os import path

from ..database.connection import database


class SuFileLinkModel(database.Model):  # type: ignore
    __tablename__ = "su_file_link_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    path = dbTypes.Column(dbTypes.String)

    projectId = dbTypes.Column(dbTypes.ForeignKey(
        "projects_table.id",
        name="FK_projects_table_su_file_link_table",
        ondelete="CASCADE"
    ))

    datasetId = dbTypes.Column(dbTypes.ForeignKey(
        "datasets_table.id",
        name="FK_datasets_table_su_file_link_table",
        ondelete="CASCADE"
    ))

    created_at = dbTypes.Column(
        dbTypes.DateTime(timezone=True),
        server_default=dbTypes.func.now()
    )
    modified_at = dbTypes.Column(
        dbTypes.DateTime(timezone=True),
        onupdate=dbTypes.func.now()
    )

    def getFileName(self):
        return path.basename(self.path)

    def getAttributes(self):
        return {
            "id": self.id,
            "name": self.getFileName(),
            "projectId": self.projectId,
        }
