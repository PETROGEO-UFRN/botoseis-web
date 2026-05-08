from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from ..config.private_key import private_key
from ..errors.AuthError import AuthError


def validateToken(token: str):
    token = token.replace("Bearer ", "")

    try:
        payload = decode(token, key=private_key, algorithms=["HS256"])
    except InvalidSignatureError:
        raise AuthError("Invalid Token Signature")
    except ExpiredSignatureError:
        raise AuthError("Expired Token")
    except:
        raise AuthError()
    return payload
