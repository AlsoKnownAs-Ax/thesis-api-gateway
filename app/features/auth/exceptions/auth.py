from enum import Enum

from fastapi import status

from app.core.exceptions.base import BaseAppException


class AuthenticationErrorType(Enum):
    INVALID_CREDENTIALS = (
        "INVALID_CREDENTIALS",
        "Incorrect email or password",
        status.HTTP_401_UNAUTHORIZED,
    )

    INVALID_REFRESH_TOKEN = (
        "INVALID_REFRESH_TOKEN",
        "Invalid Refresh Token",
        status.HTTP_401_UNAUTHORIZED,
        {"WWW-Authenticate": "Bearer"},
    )

    EXPIRED_REFRESH_TOKEN = (
        "EXPIRED_REFRESH_TOKEN",
        "Invalid Refresh Token",
        status.HTTP_401_UNAUTHORIZED,
        {"WWW-Authenticate": "Bearer"},
    )


# Factory class to create auth related exceptions
class AuthenticationException(BaseAppException):
    def __init__(self, error_type: AuthenticationErrorType, **kwargs):
        code, message, status_code, headers = error_type.value

        super().__init__(
            code=code, message=message, status_code=status_code, headers=headers**kwargs
        )
