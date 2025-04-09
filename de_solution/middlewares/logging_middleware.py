"""Request logging middleware."""

import collections.abc
import json
import typing as t
import uuid

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware."""

    @t.override
    async def dispatch(
        self,
        request: Request,
        call_next: t.Callable[[Request], collections.abc.Awaitable[Response]],
    ) -> Response:
        """Log the request details."""
        request_id = f"{uuid.uuid4()}"

        self._log_request(request, request_id)
        return await call_next(request)

    @staticmethod
    def _log_request(request: Request, request_id: str) -> None:
        """Log request details including headers and body."""
        log_structure = {
            "request_id": request_id,
            "type": "request",
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "client": request.client.host if request.client else None,
        }
        logger.debug(f"REQUEST: {json.dumps(log_structure, default=str)}")
