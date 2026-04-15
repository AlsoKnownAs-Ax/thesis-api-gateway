from clients.generated.order.v1 import order_pb2_grpc
from grpc.aio import Channel


class OrderClient():
    def __init__(self, channel: Channel):
        self.stub = order_pb2_grpc.OrderServiceStub(channel)

    # TODO: Complete this client