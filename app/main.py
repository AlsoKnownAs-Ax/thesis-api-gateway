from contextlib import asynccontextmanager

import grpc
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import benchmark
from app.clients.grpc.error_handler import translate_grpc_error
from app.core.config import config
from app.core.exceptions.openapi import DEFAULT_ERROR_RESPONSES
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.benchmark_channel = grpc.aio.insecure_channel(config.BENCHMARK_SERVICE_URL)
    yield
    # Shut down
    await app.state.benchmark_channel.close()


setup_logging()
app = FastAPI(title=config.app_name, lifespan=lifespan)

main_router = APIRouter(responses=DEFAULT_ERROR_RESPONSES)

# Register routes
main_router.include_router(benchmark.router)

app.include_router(main_router, prefix="/api/gateway")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register error handling
@app.exception_handler(grpc.RpcError)
async def grpc_error_handler(request: Request, exc: grpc.RpcError):
    base_exception = translate_grpc_error(exc)
    return JSONResponse(
        status_code=base_exception.status_code,
        content={
            "code": base_exception.code,
            "message": base_exception.message,
            "details": base_exception.details,
        },
    )
