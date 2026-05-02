from contextlib import asynccontextmanager

import grpc
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import order, user
from app.clients.grpc.error_handler import translate_grpc_error
from app.core.config import config
from app.core.database import Base, engine
from app.core.exceptions.openapi import DEFAULT_ERROR_RESPONSES
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.user_channel = grpc.aio.insecure_channel(config.USER_SERVICE_URL)
    app.state.product_channel = grpc.aio.insecure_channel(config.PRODUCT_SERVICE_URL)
    app.state.order_channel = grpc.aio.insecure_channel(config.ORDER_SERVICE_URL)
    yield
    await app.state.user_channel.close()
    await app.state.product_channel.close()
    await app.state.order_channel.close()


setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name, lifespan=lifespan)

main_router = APIRouter(responses=DEFAULT_ERROR_RESPONSES)

# Register routes
main_router.include_router(order.router)
main_router.include_router(user.router)

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
