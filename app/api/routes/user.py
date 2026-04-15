from clients.grpc.user_client import UserClientDep
from fastapi import APIRouter
from schemas.user import CreateUserRequest, UserResponse

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/create", response_model=UserResponse, operation_id="createUser")
async def create_user(
    request: CreateUserRequest,
    user_client: UserClientDep
):
    return await user_client.create_user(request)