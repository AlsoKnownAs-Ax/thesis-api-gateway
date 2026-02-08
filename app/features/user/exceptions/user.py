from fastapi import status

from app.core.exceptions.base import BaseAppException


class UserAlreadyExistsException(BaseAppException):
    code = "USER_ALREADY_EXISTS"
    message = "User already exists"
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, **kwargs):
        super().__init__(
            code=self.code, message=self.message, status_code=self.status_code, **kwargs
        )
