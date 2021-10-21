from typing import List

from app.utils.config import (ALLOW_CREDENTIALS, ALLOWED_HEADERS,
                              ALLOWED_METHODES, HOST, PORT, PROTOCOL)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


def middlewareCorse(app: FastAPI) -> None:
    origins: List = [
        f"{PROTOCOL}://{HOST}:{PORT}",
    ]

    credentials: bool = ALLOW_CREDENTIALS
    methods: List[str] = ALLOWED_METHODES
    headers: List[str] = ALLOWED_HEADERS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=credentials,
        allow_methods=methods,
        allow_headers=headers
    )
