from typing import Annotated

from fastapi import Depends, Request
from grpc.aio import Channel

from app.clients.generated.user.v1 import user_pb2_grpc
from app.schemas.user import CreateUserRequest, UserResponse


class UserClient:
    def __init__(self, channel: Channel):
        self.stub = user_pb2_grpc.UserServiceStub(channel)

    async def create_user(self, request: CreateUserRequest):
        grpc_request = request.to_grpc()
        grpc_response = await self.stub.CreateUser(grpc_request)

        return UserResponse.from_grpc(grpc_response.user)
    
def get_user_client(request: Request) -> UserClient:
    return UserClient(request.app.state.user_channel)

UserClientDep = Annotated[UserClient, Depends(get_user_client)]