from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import config
from app.core.database import Base, engine
from app.core.exceptions.base import BaseAppException
from app.core.exceptions.openapi import DEFAULT_ERROR_RESPONSES
from app.core.logging import setup_logging
from app.features.auth.routes import auth
from app.features.user.routes import user

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)

main_router = APIRouter(responses=DEFAULT_ERROR_RESPONSES)

# Register routes
main_router.include_router(user.router)
main_router.include_router(auth.router)

app.include_router(main_router, prefix="/api/v1")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register error handling
@app.exception_handler(BaseAppException)
async def base_app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )
