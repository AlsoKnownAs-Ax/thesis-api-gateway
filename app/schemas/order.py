from pydantic import BaseModel

from app.clients.generated.order.v1 import order_pb2


class CreateOrderResponse(BaseModel):
    order_id: int
    status: str
    total_price: float
    message: str

    @classmethod
    def from_grpc(cls, order: order_pb2.CreateOrderResponse) -> "CreateOrderResponse":
        return cls(
            order_id=order.order_id,
            status=order.status,
            total_price=order.total_price,
            message=order.message,
        )


class CreateOrderRequest(BaseModel):
    user_id: str
    product_id: str
    quantity: int

    def to_grpc(self) -> order_pb2.CreateOrderRequest:
        return order_pb2.CreateOrderRequest(
            user_id=self.user_id, product_id=self.product_id, quantity=self.quantity
        )