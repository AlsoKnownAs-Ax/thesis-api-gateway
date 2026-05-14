from typing import Annotated

from fastapi import Depends, Request
from grpc.aio import Channel

from app.clients.generated import benchmark_pb2_grpc
from app.schemas.benchmark import BenchmarkRequest, StreamBenchmarkResponse, UnaryBenchmarkResponse


class BenchmarkClient():
    def __init__(self, channel: Channel):
        self.stub = benchmark_pb2_grpc.BenchmarkServiceStub(channel)

    async def unary(self, request: BenchmarkRequest):
        grpc_request = request.to_grpc()
        grpc_response = await self.stub.GetItemsUnary(grpc_request)

        return UnaryBenchmarkResponse.from_grpc(grpc_response)

    async def stream(self, request: BenchmarkRequest):
        grpc_request = request.to_grpc()
        grpc_response = await self.stub.GetItemsStream(grpc_request)

        return StreamBenchmarkResponse.from_grpc(grpc_response)
    

def get_benchmark_client(request: Request) -> BenchmarkClient:
    return BenchmarkClient(request.app.state.benchmark_channel)

BenchmarkClientDep = Annotated[BenchmarkClient, Depends(get_benchmark_client)]