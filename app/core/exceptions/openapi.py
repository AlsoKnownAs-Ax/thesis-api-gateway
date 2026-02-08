from app.core.exceptions.base import ApiError

DEFAULT_ERROR_RESPONSES = {
    400: {"model": ApiError},
    401: {"model": ApiError},
    403: {"model": ApiError},
    404: {"model": ApiError},
    409: {"model": ApiError},
    422: {"model": ApiError},
    500: {"model": ApiError},
}
