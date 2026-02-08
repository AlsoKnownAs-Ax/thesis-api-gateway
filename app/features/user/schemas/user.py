from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str

class UserCreateResponse(BaseModel):
    verification_token: str


class UserRead(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
