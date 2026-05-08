from uuid import UUID

from flask import request

from ..models.ProjectModel import ProjectModel
from ..models.LineModel import LineModel

from ..models.UserModel import UserModel
from ..errors.AppError import AppError
from ..errors.AuthError import AuthError
from ..errors.AppError import AppError

from ..services.validateToken import validateToken


def requireAuthentication(routeFunction, routeModel=None, isAdminRequired=False):
    def wrapper(routeModel=routeModel, *args, **kwargs):
        token = request.cookies.get("Authorization")
        data = {}
    
        if not token:
            raise AuthError("No token")

        try:
            data = request.get_json()
        except:
            pass

        payload = validateToken(token)

        userId = payload["id"]
        user = UserModel.query.filter_by(id=UUID(userId)).first()
        if not user:
            raise AppError("User does not exist", 404)

        if isAdminRequired and not user.is_admin:
            raise AuthError("Must be admin")

        # ! Really bad implementation
        if not routeModel and "parentType" in data:
            routeModel = LineModel if data["parentType"] == "lineId" else ProjectModel

        if routeModel:
            modelId = int(list(kwargs.values())[0])
            modelObject = routeModel.query.filter_by(id=modelId).first()

            if not modelObject:
                raise AppError("No instance found for this id", 404)

            userAttr = modelObject.owner_email if hasattr(
                modelObject, 'owner_email'
            ) else modelObject.userId
            if userAttr != user.email and userAttr != user.id:
                raise AuthError("User unauthorized for this entity")

        # *** "payload.id" will be the first argument of any function
        # *** using "requireAuthentication" as decorator
        response = routeFunction(userId, *args, **kwargs)
        return response
    return wrapper
