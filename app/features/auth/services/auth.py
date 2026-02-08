from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth.utils import verify_password
from app.core.config import config
from app.core.database import get_db
from app.features.auth.exceptions.access_token import InvalidAccessToken
from app.features.auth.exceptions.auth import AuthenticationErrorType, AuthenticationException
from app.features.auth.exceptions.refresh_token import ExpiredRefreshToken, InvalidRefreshToken
from app.features.auth.models.refresh_token import RefreshToken
from app.features.user.services.user import UserService


class AuthService:
    def __init__(self, session: Session):
        self._db = session
        self.user_service = UserService(session)

    def authenticate_user(self, email: str, password: str):
        user = self.user_service.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise AuthenticationException(
                AuthenticationErrorType.INVALID_CREDENTIALS, headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.is_verified:
            raise AuthenticationException(AuthenticationErrorType.NOT_VERIFIED)

        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config.ACCESS_SECRET_KEY, algorithm=config.HASHING_ALGORITHM
        )
        return encoded_jwt

    def create_refresh_token(
        self, data: dict, user_id: UUID, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, config.REFRESH_SECRET_KEY, algorithm=config.HASHING_ALGORITHM)

        refresh_token_record = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=int(expire.timestamp()),
        )

        self._db.add(refresh_token_record)
        self._db.commit()

        return token

    def verify_refresh_token(self, token: str):
        try:
            token_record = (
                self._db.query(RefreshToken)
                .filter(
                    RefreshToken.token == token,
                )
                .first()
            )

            if not token_record:
                raise AuthenticationException()

            expires_at = datetime.fromtimestamp(token_record.expires_at, tz=timezone.utc)
            if expires_at < datetime.now(timezone.utc):
                raise ExpiredRefreshToken()

            payload = jwt.decode(token, config.REFRESH_SECRET_KEY, config.HASHING_ALGORITHM)
            email: str = payload.get("sub")
            if email is None:
                raise InvalidRefreshToken()

            return payload
        except jwt.ExpiredSignatureError:
            raise ExpiredRefreshToken()
        except jwt.InvalidTokenError:
            raise InvalidRefreshToken()

    def revoke_refresh_token(self, token: str):
        token_record = self._db.query(RefreshToken).filter(RefreshToken.token == token).first()

        if token_record:
            self._db.delete(token_record)
            self._db.commit()

    def refresh_access_token(self, refresh_token: str):
        if not refresh_token:
            raise InvalidAccessToken()

        payload = self.verify_refresh_token(refresh_token)
        email = payload.get("sub")

        # Verify user still exists
        user = self.user_service.get_user_by_email(email)
        if not user:
            raise InvalidRefreshToken()

        # Create new access token
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return access_token


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(session=db)