from grpc.aio import Channel

from app.clients.generated.order.v1 import order_pb2_grpc


class OrderClient():
    def __init__(self, channel: Channel):
        self.stub = order_pb2_grpc.OrderServiceStub(channel)

    # TODO: Complete this client