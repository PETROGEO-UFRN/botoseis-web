from os import path, makedirs
from types import SimpleNamespace

from ..database.connection import database
from ..models.FileLinkModel import FileLinkModel

from ..factories.filePathFactory import createHelperFilePath


def listByLineId(lineId, data_type):
    fileLinks = FileLinkModel.query.filter_by(
        lineId=lineId,
        data_type=data_type,
    ).all()

    # *** iterate fileLinks and convert it to list of dicts
    # *** so the api can return it as route response
    fileLinksResponse = list(map(
        lambda link: link.getAttributes(),
        fileLinks
    ))

    return fileLinksResponse


def create(file, lineId, data_type) -> str:
    filePath = createHelperFilePath(
        lineId,
        data_type,
        file.filename
    )

    newFileLink = FileLinkModel(
        lineId=lineId,
        path=filePath,
        data_type=data_type,
    )
    database.session.add(newFileLink)
    database.session.commit()

    directory = path.dirname(filePath)
    if not path.exists(directory):
        makedirs(directory)
    file.save(filePath)

    return newFileLink.getAttributes()


helperFileController = SimpleNamespace(
    listByLineId=listByLineId,
    create=create,
)
