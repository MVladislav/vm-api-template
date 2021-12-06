import logging
from typing import Dict

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.schemas.response import ResponseSchema


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class UnicornException(Exception):

    def __init__(
        self, status_code: int, detail: ResponseSchema, headers: Dict[str, str]
    ):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class InitExceptionHandler:

    def __init__(self, app: FastAPI) -> None:

        @app.exception_handler(UnicornException)
        async def unicorn_exception_handler(_: Request, exc: UnicornException):
            try:
                return JSONResponse(
                    status_code=exc.status_code,
                    content=exc.detail.dict(),
                    headers=exc.headers,
                )

            except Exception as e:
                logging.log(logging.CRITICAL, e, exc_info=True)
            return None
