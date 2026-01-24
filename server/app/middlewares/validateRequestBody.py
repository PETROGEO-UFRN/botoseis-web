from flask import request
from marshmallow import EXCLUDE


def validateRequestBody(routeFunction, SerializerSchema):
    def wrapper(*args, **kwargs):
        # *** json is usualy better but gives issues when uploading files
        try:
            data = request.get_json()
        except:
            data = {
                **request.form.to_dict(),
                **request.files.to_dict()
            }

        # *** unexpected fields on request body will be
        # *** excluded and ignored, not raising any error.
        SerializerSchema(unknown=EXCLUDE).load(data)

        response = routeFunction(*args, **kwargs)
        return response
    return wrapper
