import sqlalchemy as dbTypes

from ..database.connection import database

class ProgramModel(database.Model):  # type: ignore
    __tablename__ = "programs_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    description = dbTypes.Column(dbTypes.String)
    # that could be a better name for it, once "path_to_executable_file"
    # can also store command keys that work as shell commands
    # like for the seismicunix package commands
    path_to_executable_file = dbTypes.Column(dbTypes.String)

    groupId = dbTypes.Column(dbTypes.ForeignKey(
        "program_groups_table.id",
        name="FK_program_groups_table_programs_table"
    ))

    def getAttributes(self) -> dict[str, int | str]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "path_to_executable_file": self.path_to_executable_file,
            "groupId": self.groupId
        }
