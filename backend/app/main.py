"""
    main start function
    will include all
        - startup tools (logging, db, ...)
        - app
        - middleware
        - api
"""

import logging
from typing import Union

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from app.db.mongoDb import DBConnection
from app.middleware.corse import middlewareCorse
from app.routes.account import router as accountApi
from app.utils.api.exceptionHandler import InitExceptionHandler
from app.utils.config import settings
from app.utils.logHelper import LogHelper

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
# Program Header
# Basic user interface header
print(
    r"""    __  ____    ____          ___      __
   /  |/  / |  / / /___ _____/ (_)____/ /___ __   __
  / /|_/ /| | / / / __ `/ __  / / ___/ / __ `/ | / /
 / /  / / | |/ / / /_/ / /_/ / (__  ) / /_/ /| |/ /
/_/  /_/  |___/_/\__,_/\__,_/_/____/_/\__,_/ |___/"""
)
print("**************** 4D 56 6C 61 64 69 73 6C 61 76 *****************")
print("****************************************************************")
print("* Copyright of MVladislav, 2021                                *")
print("* https://mvladislav.online                                    *")
print("* https://github.com/MVladislav                                *")
print("****************************************************************")
print()


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def main() -> Union[FastAPI, None]:
    """
    init and startup
    """
    try:
        application.start_up()
        application.connect_db()
        app = application.application()

        @app.on_event("startup")
        async def startup():
            logging.log(logging.DEBUG, "STARTUP...")
            application.handler(app)
            application.middleware(app)
            application.api(app)
            application.scheduler()
            logging.log(logging.DEBUG, "...READY")

        @app.on_event("shutdown")
        async def shutdown():
            logging.log(logging.DEBUG, "SHUTDOWN...")
            application.scheduler_stop()
            logging.log(logging.DEBUG, "...BYE")

        return app

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    # sys.exit(4)
    return None


class Application:
    schedule: Union[AsyncIOScheduler, None] = None
    scheduleSeconds = 1

    # ------------------------------------------------------------------------------
    #
    # DEFINE base methods
    #
    # ------------------------------------------------------------------------------
    def start_up(self) -> None:
        """
            inti some general start ups before all other
        """
        # INIT: log helper global
        LogHelper(
            logging_verbose=settings.LOGGING_VERBOSE,
            logging_level=settings.LOGGING_LEVEL,
        )
        logging.log(logging.DEBUG, "init start_up...")
        settings.print()

    def connect_db(self) -> None:
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
    def application(self) -> FastAPI:
        """
            create the application it self
        """
        logging.log(logging.DEBUG, "init application...")
        return FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            debug=settings.DEBUG,
            docs_url=f"{settings.API_PREFIX}/docs",
            openapi_url=f"{settings.API_PREFIX}/openapi.json",
        )


    # ------------------------------------------------------------------------------
    #
    # DEFINE base methods
    #
    # ------------------------------------------------------------------------------
    def handler(self, app: FastAPI) -> None:
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
    def middleware(self, app: FastAPI) -> None:
        """
            include middleware
        """
        logging.log(logging.DEBUG, "init middleware...")
        middlewareCorse(app)

    def api(self, app: FastAPI) -> None:
        """
            include api's
        """
        logging.log(logging.DEBUG, "init api...")
        # ACCOUNT: for login and registration
        app.include_router(accountApi, prefix=settings.API_PREFIX, dependencies=[])


    # ...: for ... logic
    # app.include_router(
    #     ...Api,
    #     prefix=API_PREFIX,
    #     dependencies=[],
    # )
    # ------------------------------------------------------------------------------
    #
    # DEFINE scheduled methods
    #
    # ------------------------------------------------------------------------------
    def scheduler(self) -> None:
        logging.log(logging.DEBUG, "init scheduler...")
        self.schedule = AsyncIOScheduler()
        # self.schedule.add_job(func=add_here, trigger="interval", seconds=self.scheduleSeconds)
        self.schedule.start()

    def scheduler_stop(self) -> None:
        if self.schedule is not None:
            logging.log(logging.DEBUG, "shuting down scheduler...")
            self.schedule.shutdown()


application = Application()


# ------------------------------------------------------------------------------
#
# OTHER
#
# ------------------------------------------------------------------------------
def app():
    uvicorn.run(
        "app.main:main",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=logging.getLevelName(settings.LOGGING_LEVEL),
        factory=True,
    )
