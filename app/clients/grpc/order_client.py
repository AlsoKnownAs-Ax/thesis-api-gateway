from typing import Annotated

from fastapi import Depends, Request
from grpc.aio import Channel

from app.clients.generated.order.v1 import order_pb2_grpc
from app.schemas.order import CreateOrderRequest, CreateOrderResponse


class OrderClient():
    def __init__(self, channel: Channel):
        self.stub = order_pb2_grpc.OrderServiceStub(channel)

    async def create_order(self, request: CreateOrderRequest):
        grpc_request = request.to_grpc()
        grpc_response = await self.stub.CreateOrder(grpc_request)

        return CreateOrderResponse.from_grpc(grpc_response)


def get_order_client(request: Request) -> OrderClient:
    return OrderClient(request.app.state.order_channel)


OrderClientDep = Annotated[OrderClient, Depends(get_order_client)]