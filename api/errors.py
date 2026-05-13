from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from neo4j.exceptions import Neo4jError
from pydantic import ValidationError

class APIError(Exception):
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}

async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message, "details": exc.details}
    )

async def neo4j_error_handler(request: Request, exc: Neo4jError):
    return JSONResponse(
        status_code=503,
        content={"code": "DATABASE_SERVICE_UNAVAILABLE", "message": str(exc)}
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"code": "VALIDATION_ERROR", "message": "Input validation failed", "details": exc.errors()}
    )

async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": "HTTP_ERROR", "message": exc.detail}
        )
    return JSONResponse(
        status_code=500,
        content={"code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred"}
    )
