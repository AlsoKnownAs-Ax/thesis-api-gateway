from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str

class TokenData(BaseModel):
    email: str | None = None


class RefreshTokenRequest(BaseModel):
    token: str