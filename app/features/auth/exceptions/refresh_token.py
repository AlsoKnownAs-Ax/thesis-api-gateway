from fastapi import status

from app.core.exceptions.base import BaseAppException


class InvalidRefreshToken(BaseAppException):
    code = "INVALID_REFRESH_TOKEN"
    message = "Invalid Refresh Token"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, **kwargs):
        super().__init__(
            code=self.code,
            message=self.message,
            status_code=self.status_code,
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs,
        )


class ExpiredRefreshToken(BaseAppException):
    code = "EXPIRED_REFRESH_TOKEN"
    message = "Expired Refresh Token"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, **kwargs):
        super().__init__(
            code=self.code,
            message=self.message,
            status_code=self.status_code,
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs,
        )
