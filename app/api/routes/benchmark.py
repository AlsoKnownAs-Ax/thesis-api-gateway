from fastapi import APIRouter, Query

from app.clients.grpc.banchmark_client import BenchmarkClientDep
from app.schemas.benchmark import BenchmarkRequest, StreamBenchmarkResponse, UnaryBenchmarkResponse

router = APIRouter(
    prefix="/benchmark",
    tags=["benchmark"]
)

@router.get("/unary", response_model=UnaryBenchmarkResponse)
async def unary_benchmark(
    benchmark_client: BenchmarkClientDep,
    item_count: int = Query(..., alias="itemCount"),
    payload_size_bytes: int = Query(..., alias="payloadSizeBytes"),
):
    request = BenchmarkRequest(
        item_count=item_count,
        payload_size_bytes=payload_size_bytes
    )
    return await benchmark_client.unary(request)

@router.get("/stream", response_model=StreamBenchmarkResponse)
async def stream_benchmark(
    benchmark_client: BenchmarkClientDep,
    item_count: int = Query(..., alias="itemCount"),
    payload_size_bytes: int = Query(..., alias="payloadSizeBytes"),
):
    request = BenchmarkRequest(
        item_count=item_count,
        payload_size_bytes=payload_size_bytes
    )
    return await benchmark_client.stream(request)