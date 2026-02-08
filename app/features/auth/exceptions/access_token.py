from fastapi import status

from app.core.exceptions.base import BaseAppException


class InvalidAccessToken(BaseAppException):
    code = "INVALID_ACCESS_TOKEN"
    message = "Invalid Access Token"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, **kwargs):
        super().__init__(
            code=self.code,
            message=self.message,
            status_code=self.status_code,
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs,
        )


class ExpiredAccessToken(BaseAppException):
    code = "EXPIRED_ACCESS_TOKEN"
    message = "Expired Access Token"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, **kwargs):
        super().__init__(
            code=self.code,
            message=self.message,
            status_code=self.status_code,
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs,
        )
