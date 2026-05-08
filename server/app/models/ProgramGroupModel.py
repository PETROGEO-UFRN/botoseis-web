import sqlalchemy as dbTypes
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database.connection import database
from .ProgramModel import ProgramModel


class ProgramGroupModel(database.Model):  # type: ignore
    __tablename__ = "program_groups_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    description = dbTypes.Column(dbTypes.String)

    programs: Mapped[
        List[ProgramModel]
    ] = relationship(ProgramModel)

    def getAttributes(self) -> dict[str, str | list[dict[str, str]]]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "programs": [program.getAttributes() for program in self.programs]
        }
