from pydantic import BaseModel, EmailStr

from app.clients.generated.user.v1 import user_pb2


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str

    @classmethod
    def from_grpc(cls, user: user_pb2.User) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

class CreateUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    def to_grpc(self) -> user_pb2.CreateUserRequest:
        return user_pb2.CreateUserRequest(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
        )
    
