from fastapi import HTTPException, status
from http import HTTPStatus

class IException(Exception):
    _status_code: HTTPStatus = HTTPStatus.NOT_FOUND
    _message: str = ""

    def __init__(self, message: str):
        self._message = message
        super().__init__(message)

    @property
    def status_code(self):
        return self._status_code

    @property
    def message(self):
        return self._message
    
class NotFoundException(IException):
    _status_code: HTTPStatus = status.HTTP_404_NOT_FOUND

    def __init__(self):
        super().__init__("User not found")

class UnauthenticatedException(HTTPException):
    def __init__(self, detail: str = "Token has been expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
