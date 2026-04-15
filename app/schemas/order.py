from pydantic import BaseModel


class CreateOrderResponse(BaseModel):
    order_id: int