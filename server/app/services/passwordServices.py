from bcrypt import hashpw, gensalt, checkpw


def hashPassword(textPassword: str) -> bytes:
    password = textPassword.encode()
    salt = gensalt()

    return hashpw(password, salt)


def checkPassword(password: str, hashedPassword: bytes) -> bool:
    return checkpw(password.encode(), hashedPassword)
