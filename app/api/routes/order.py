from fastapi import APIRouter

from app.clients.grpc.order_client import OrderClientDep
from app.schemas.order import CreateOrderRequest, CreateOrderResponse

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

@router.post("/create", response_model=CreateOrderResponse, operation_id="createOrder")
async def create_order(request: CreateOrderRequest, order_client: OrderClientDep):
    return await order_client.create_order(request)