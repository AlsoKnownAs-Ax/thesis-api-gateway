
from pydantic import BaseModel

from app.clients.generated import benchmark_pb2


class BenchmarkItem(BaseModel):
    id: int
    payload: str

    @classmethod
    def from_grpc(cls, item: benchmark_pb2.BenchmarkItem) -> "BenchmarkItem":
        return cls(
            id=item.id,
            payload=item.payload,
        )
    
class BenchmarkRequest(BaseModel):
    item_count: int
    payload_size_bytes: int

    @classmethod
    def to_grpc(self) -> benchmark_pb2.BenchmarkRequest:
        return benchmark_pb2.BenchmarkRequest(
            item_count=self.item_count,
            payload_size_bytes=self.payload_size_bytes
        )

class UnaryBenchmarkResponse(BaseModel):
    items: list[BenchmarkItem]

    @classmethod
    def from_grpc(cls, benchmark: benchmark_pb2.BenchmarkResponse) -> "UnaryBenchmarkResponse":
        return cls(
            items=[BenchmarkItem.from_grpc(item) for item in benchmark.items]
        )
    
# Duplicate just to be explicit
class StreamBenchmarkResponse(BaseModel):
    items: list[BenchmarkItem]

    @classmethod
    def from_grpc(cls, benchmark: benchmark_pb2.BenchmarkResponse) -> "StreamBenchmarkResponse":
        return cls(
            items=[BenchmarkItem.from_grpc(item) for item in benchmark.items]
        )
    
