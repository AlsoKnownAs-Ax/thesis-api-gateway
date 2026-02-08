from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import config
from app.features.auth.schemas.token import AccessTokenResponse
from app.features.auth.services.auth import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", operation_id="login", response_model=AccessTokenResponse)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(get_auth_service),
):
    user = service.authenticate_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = service.create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires, user_id=user.id
    )

    response.set_cookie(
        key=config.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=config.ENV == "production",
        samesite="lax",
        max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return AccessTokenResponse(access_token=access_token)


@router.post("/logout", operation_id="logout")
async def logout(
    refresh_token: Annotated[str | None, Cookie(alias=config.REFRESH_TOKEN_COOKIE_NAME)] = None,
    service: AuthService = Depends(get_auth_service),
):
    if refresh_token:
        service.revoke_refresh_token(refresh_token)

    return {"message": "Successfully logged out"}


@router.post("/refresh", operation_id="refreshToken", response_model=AccessTokenResponse)
async def refresh_token(
    refresh_token: Annotated[str | None, Cookie(alias=config.REFRESH_TOKEN_COOKIE_NAME)] = None,
    service: AuthService = Depends(get_auth_service),
):
    access_token = service.refresh_access_token(refresh_token)

    return AccessTokenResponse(access_token=access_token)
