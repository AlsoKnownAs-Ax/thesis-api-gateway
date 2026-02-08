from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import config
from app.core.database import get_db
from app.features.auth.exceptions.access_token import ExpiredAccessToken, InvalidAccessToken
from app.features.auth.schemas.token import TokenData
from app.features.user.schemas.user import UserRead
from app.features.user.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, config.ACCESS_SECRET_KEY, algorithms=[config.HASHING_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise InvalidAccessToken()
        token_data = TokenData(email=email)
    except jwt.ExpiredSignatureError:
        raise ExpiredAccessToken()
    except jwt.InvalidTokenError:
        raise InvalidAccessToken()
    user_service = UserService(db)
    user = user_service.get_user_by_email(token_data.email)
    if user is None:
        raise InvalidAccessToken()
    
    return user

CurrentUser = Annotated[UserRead, Depends(get_current_user)]