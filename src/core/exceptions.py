from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.core.utils import api_response

# Handler for validation errors (422 Unprocessable Entity)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return api_response(
        422,
        "Validation Error",
        error=exc.errors()
    )

# Handler for HTTP exceptions (e.g., 401, 403, 404, etc.)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return api_response(
        exc.status_code,
        "Unauthorized",
        error=str(exc.detail)
    )

# Handler for uncaught exceptions (500 Internal Server Error)
async def internal_server_error_handler(request: Request, exc: Exception):
    return api_response(
        500,
        "Internal Server Error",
        error=str(exc)
    )
