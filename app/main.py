"""
    main start function
    will include all
        - startup tools (logging, db, ...)
        - app
        - middleware
        - api
"""

import logging
import sys

import gunicorn
import uvicorn
from fastapi import FastAPI
from uvicorn.config import LOG_LEVELS

from app.db.mongoDb import DBConnection
from app.middleware.corse import middlewareCorse
from app.routes.account import router as accountApi
from app.utils.api.exceptionHandler import InitExceptionHandler
from app.utils.config import (API_PREFIX, DEBUG, DEBUG_RELOAD, HOST,
                              LOGGING_LEVEL, PORT, PROJECT_NAME, VERSION)
from app.utils.logHelper import LogHelper

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


# Program Header
# Basic user interface header
print(r'''    __  ____    ____          ___      __
   /  |/  / |  / / /___ _____/ (_)____/ /___ __   __
  / /|_/ /| | / / / __ `/ __  / / ___/ / __ `/ | / /
 / /  / / | |/ / / /_/ / /_/ / (__  ) / /_/ /| |/ /
/_/  /_/  |___/_/\__,_/\__,_/_/____/_/\__,_/ |___/''')
print('**************** 4D 56 6C 61 64 69 73 6C 61 76 *****************')
print('****************************************************************')
print('* Copyright of MVladislav, 2021                                *')
print('* https://mvladislav.online                                    *')
print('* https://github.com/MVladislav                                *')
print('****************************************************************')
print()

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


def main() -> FastAPI:
    """
        init and startup
    """
    try:
        start_up()
        connect_db()
        app = application()

        @app.on_event("startup")
        async def startup():
            logging.log(logging.DEBUG, "STARTUP...")
            handler(app)
            middleware(app)
            api(app)
            logging.log(logging.DEBUG, "...READY")

        @app.on_event("shutdown")
        async def shutdown():
            logging.log(logging.DEBUG, "SHUTDOWN...")
            pass
            logging.log(logging.DEBUG, "...BYE")

        return app
    except Exception as ex:
        logging.log(logging.ERROR, ex)
        sys.exit(4)

# ------------------------------------------------------------------------------
#
# DEFINE base methods
#
# ------------------------------------------------------------------------------


def start_up() -> None:
    """
        inti some general start ups before all other
    """
    logging.log(logging.DEBUG, "init start_up...")
    LogHelper()


def connect_db() -> None:
    """
        inti database connection
    """
    logging.log(logging.DEBUG, "init connect_db...")
    DBConnection().get_connection()

# ------------------------------------------------------------------------------
#
# DEFINE base methods
#
# ------------------------------------------------------------------------------


def application() -> FastAPI:
    """
        create the application it self
    """
    logging.log(logging.DEBUG, "init application...")
    return FastAPI(
        title=PROJECT_NAME,
        version=VERSION,
        debug=DEBUG
    )

# ------------------------------------------------------------------------------
#
# DEFINE base methods
#
# ------------------------------------------------------------------------------


def handler(app: FastAPI) -> None:
    """
        include own excaption handlers
    """
    logging.log(logging.DEBUG, "init handler...")
    InitExceptionHandler(app)

# ------------------------------------------------------------------------------
#
# DEFINE base methods
#
# ------------------------------------------------------------------------------


def middleware(app: FastAPI) -> None:
    """
        include middleware
    """
    logging.log(logging.DEBUG, "init middleware...")
    middlewareCorse(app)


def api(app: FastAPI) -> None:
    """
        include api's
    """
    logging.log(logging.DEBUG, "init api...")
    # ACCOUNT: for login and registration
    app.include_router(
        accountApi,
        prefix=API_PREFIX,
        dependencies=[],
    )
    # ...: for ... logic
    # app.include_router(
    #     ...Api,
    #     prefix=API_PREFIX,
    #     dependencies=[],
    # )

# ------------------------------------------------------------------------------
#
# OTHER
#
# ------------------------------------------------------------------------------


def app():
    uvicorn.run("app.main:main", host=HOST, port=PORT, reload=DEBUG_RELOAD,
                log_level=logging.getLevelName(LOGGING_LEVEL), factory=True)
