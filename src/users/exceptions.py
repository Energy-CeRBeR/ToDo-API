from fastapi import HTTPException, status


class EmailExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this email already exists"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ShortNameExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this shortname already exists"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CredentialException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class TokenTypeException(HTTPException):

    def __new__(cls, *args, **kwargs):
        cls.detail = f"Invalid token type {args[0]!r} expected {args[1]!r}"
        cls.status_code = status.HTTP_401_UNAUTHORIZED

        return super().__new__(cls)

    def __init__(self, *args):  # noqa
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AccessException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access denied!"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
