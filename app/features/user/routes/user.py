
from datetime import timedelta

from fastapi import APIRouter, Depends, Response

from app.core.config import config
from app.features.auth.dependencies import CurrentUser
from app.features.auth.schemas.token import AccessTokenResponse
from app.features.auth.services.auth import AuthService, get_auth_service
from app.features.user.schemas.user import UserCreate, UserRead
from app.features.user.services.user import UserService, get_user_service

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/", response_model=UserRead, operation_id="getUser")
async def get_user(
    current_user: CurrentUser,
):
    return current_user


@router.post("/create", operation_id="createUser", response_model=AccessTokenResponse)
def create_user(
    response: Response,
    userData: UserCreate,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    new_user = user_service.create_user(userData)
    
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = auth_service.create_refresh_token(
        data={"sub": new_user.email}, expires_delta=refresh_token_expires, user_id=new_user.id
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
