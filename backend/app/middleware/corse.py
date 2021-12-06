from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.config import settings


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def middlewareCorse(app: FastAPI) -> None:
    origins: List[str] = [f"{settings.PROTOCOL}://{settings.HOST}:{settings.PORT}"]
    credentials: bool = settings.ALLOW_CREDENTIALS
    methods: List[str] = settings.ALLOWED_METHODES
    headers: List[str] = settings.ALLOWED_HEADER
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=credentials,
        allow_methods=methods,
        allow_headers=headers,
    )
