from fastapi import APIRouter
from schemas.order import CreateOrderResponse

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

@router.post("/create", response_model=CreateOrderResponse, operation_id="createOrder")
def create_order():
    return