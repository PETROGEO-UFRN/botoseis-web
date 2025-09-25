from os import path, makedirs
from types import SimpleNamespace

from ..database.connection import database
from ..models.FileLinkModel import FileLinkModel

from ..factories.filePathFactory import createHelperFilePath


def listByProjectId(projectId, data_type):
    fileLinks = FileLinkModel.query.filter_by(
        projectId=projectId,
        data_type=data_type,
    ).all()

    # *** iterate fileLinks and convert it to list of dicts
    # *** so the api can return this as route response
    fileLinksResponse = list(map(
        lambda link: link.getAttributes(),
        fileLinks
    ))

    return fileLinksResponse


def create(file, projectId, data_type) -> str:
    filePath = createHelperFilePath(
        projectId,
        data_type,
        file.filename
    )

    newFileLink = FileLinkModel(
        projectId=projectId,
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
    listByProjectId=listByProjectId,
    create=create,
)
