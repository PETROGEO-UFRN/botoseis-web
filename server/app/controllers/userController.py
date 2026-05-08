from uuid import uuid4, UUID
from types import SimpleNamespace

from ..database.connection import database
from ..models.UserModel import UserModel
from ..errors.AppError import AppError
from ..services.passwordServices import hashPassword


def showAll() -> list[dict]:
    users: list[UserModel] = UserModel.query.all()
    if not users:
        return []

    return [user.getAttributes() for user in users]


def create(newUserData) -> dict:
    user = UserModel.query.filter_by(email=newUserData["email"]).first()
    if user:
        raise AppError("Email alredy used")
    newId = uuid4()

    newUser = UserModel(
        id=newId,
        name=newUserData["name"],
        email=newUserData["email"],
        password=hashPassword(newUserData["password"]),
    )
    database.session.add(newUser)
    database.session.commit()
    return newUser.getAttributes()


def update(id, newUserData) -> dict:
    user = UserModel.query.filter_by(id=UUID(id)).first()

    if "name" in newUserData:
        user.name = newUserData["name"]
    if "email" in newUserData:
        user.email = newUserData["email"]

    database.session.commit()
    return user.getAttributes()


def delete(id) -> dict:
    user = UserModel.query.filter_by(id=UUID(id)).first()

    database.session.delete(user)
    database.session.commit()
    return user.getAttributes()


userController = SimpleNamespace(
    showAll=showAll,
    create=create,
    update=update,
    delete=delete,
)
