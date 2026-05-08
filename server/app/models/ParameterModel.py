import sqlalchemy as dbTypes

from ..database.connection import database

class ParameterModel(database.Model):  # type: ignore
    __tablename__ = "parameters_table"

    id = dbTypes.Column(dbTypes.Integer, primary_key=True)
    name = dbTypes.Column(dbTypes.String)
    description = dbTypes.Column(dbTypes.String)
    example = dbTypes.Column(dbTypes.String)
    input_type = dbTypes.Column(dbTypes.String)
    isRequired = dbTypes.Column(dbTypes.Boolean)

    programId = dbTypes.Column(dbTypes.ForeignKey(
        "programs_table.id",
        name="FK_programs_table_parameters_table"
    ))

    def getAttributes(self) -> dict[str, str | int | bool]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "example": self.example,
            "input_type": self.input_type,
            "isRequired": self.isRequired,
        }
