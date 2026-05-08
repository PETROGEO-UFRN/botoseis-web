from types import SimpleNamespace

from ...database.connection import database
from ...models.ProgramGroupModel import ProgramGroupModel
from ...errors.AppError import AppError


def listAll():
    programGroups = ProgramGroupModel.query.all()
    if not programGroups:
        return []

    return [programGroup.getAttributes() for programGroup in programGroups]


def create(newGroupData):
    newProgramGroup = ProgramGroupModel(
        name=newGroupData["name"],
        description=newGroupData["description"] if newGroupData["description"] else ""
    )
    database.session.add(newProgramGroup)
    database.session.commit()
    return newProgramGroup.getAttributes()


def update(id: str | int, newGroupData: dict[str, str]) -> dict[str, str]:
    programGroup = ProgramGroupModel.query.filter_by(id=id).first()

    if not programGroup:
        raise AppError("Group does not exist", 404)

    if "name" in newGroupData:
        programGroup.name = newGroupData["name"]
    if "description" in newGroupData:
        programGroup.description = newGroupData["description"]

    database.session.commit()
    return programGroup.getAttributes()


def delete(id):
    programGroup = ProgramGroupModel.query.filter_by(id=id).first()
    if not programGroup:
        raise AppError("Group does not exist", 404)

    database.session.delete(programGroup)
    database.session.commit()
    return programGroup.getAttributes()


programGroupController = SimpleNamespace(
    listAll=listAll,
    create=create,
    update=update,
    delete=delete,
)
