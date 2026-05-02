import grpc

from app.core.exceptions.base import BaseAppException

GRPC_TO_HTTP_STATUS = {
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.PERMISSION_DENIED: 403,
    grpc.StatusCode.UNAUTHENTICATED: 401,
    grpc.StatusCode.FAILED_PRECONDITION: 412,
    grpc.StatusCode.DEADLINE_EXCEEDED: 504,
    grpc.StatusCode.UNAVAILABLE: 503,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.UNKNOWN: 500,
}

def translate_grpc_error(error: grpc.RpcError) -> BaseAppException:
    """
    Translate any gRPC error to BaseAppException.
    Gateway is naive - doesn't care about specific service exceptions.
    """
    status = error.code()
    message = error.details()
    
    http_status = GRPC_TO_HTTP_STATUS.get(status, 500)
    
    error_code = status.name
    error_message = message
    
    return BaseAppException(
        code=error_code,
        message=error_message,
        status_code=http_status
    )