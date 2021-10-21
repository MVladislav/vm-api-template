
import logging

from app.persist.account.schemas.response import ResponseSchema
from fastapi import FastAPI, Header, Request, status
from starlette.responses import JSONResponse

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class UnicornException(Exception):
    def __init__(self, status_code: status, detail: ResponseSchema, headers: Header):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class InitExceptionHandler:

    def __init__(self, app: FastAPI) -> None:

        @app.exception_handler(UnicornException)
        async def unicorn_exception_handler(request: Request, exc: UnicornException):
            try:
                return JSONResponse(
                    status_code=exc.status_code,
                    content=exc.detail.dict(),
                    headers=exc.headers,
                )
            except Exception as ex:
                logging.log(logging.ERROR, ex)
            return None
