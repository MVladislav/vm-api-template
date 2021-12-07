import logging
from pathlib import Path
from typing import List, Union

import verboselogs
from pydantic import BaseSettings, EmailStr
from starlette.config import Config
from stringcolor.ops import Bold


class Settings(BaseSettings):
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    config = Config(".env")
    config_project = Config(".env_project")
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    PROJECT_NAME: str = config_project("PROJECT_NAME", default="vm_api")
    VERSION: str = config_project("VERSION", default="0.0.1")
    ENV_MODE: str = config("ENV_MODE", default="KONS")
    # CRITICAL | ERROR | SUCCESS | WARNING | NOTICE | INFO | VERBOSE | DEBUG | SPAM | NOTSET
    LOGGING_LEVEL: str = config("LOGGING_LEVEL", default="DEBUG")
    LOGGING_VERBOSE: int = config("LOGGING_VERBOSE", cast=int, default=0)
    DEBUG: bool = True if LOGGING_LEVEL == "DEBUG" or LOGGING_LEVEL == "VERBOSE" or LOGGING_LEVEL == "SPAM" else False
    DEBUG_RELOAD: bool = True if DEBUG else False
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    BASE_PATH: str = config("VM_BASE_PATH", default=".")
    HOME_PATH: str = config("VM_HOME_PATH", default=str(Path.home()))
    USE_SUDO: List[str] = [config("USE_SUDO", default="")]
    DISABLE_SPLIT_PROJECT: bool = config(
        "DISABLE_SPLIT_PROJECT", cast=bool, default=False
    )
    DISABLE_SPLIT_HOST: bool = config("DISABLE_SPLIT_HOST", cast=bool, default=False)
    PRINT_ONLY_MODE: bool = config("PRINT_ONLY_MODE", cast=bool, default=False)
    TERMINAL_READ_MODE: bool = config("TERMINAL_READ_MODE", cast=bool, default=False)
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    # It is required to do a free registration and create a license key
    GEO_LICENSE_KEY: Union[str, None] = config("GEO_LICENSE_KEY", default=None)
    # docs: https://dev.maxmind.com/geoip/geoip2/geolite2/
    GEO_LITE_TAR_FILE_URL = (
        f"https://download.maxmind.com/app/geoip_download"
        f"?edition_id=GeoLite2-City"
        f"&license_key={GEO_LICENSE_KEY}"
        f"&suffix=tar.gz"
    )
    # TODO: add legacy
    # http://dev.maxmind.com/geoip/legacy/geolite/
    GEO_DB_FNAME = "/GeoLite2-City.mmdb"
    GEO_DB_ZIP_FNAME = "/GeoIP2LiteCity.tar.gz"
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    PROTOCOL: str = config("PROTOCOL", default="http")
    HOST: str = config("HOST", default="127.0.0.1")
    PORT: int = config("PORT", cast=int, default=8000)
    ALLOW_CREDENTIALS: bool = config("ALLOW_CREDENTIALS", cast=bool, default=True)
    ALLOWED_METHODES: List[str] = config(
        "ALLOWED_METHODES", cast=str, default="OPTIONS,GET"
    ).split(
        ","
    )
    ALLOWED_HEADER: List[str] = config("ALLOWED_HEADERS", cast=str, default="*").split(
        ","
    )
    API_PREFIX = config("API_PREFIX", default="/api/v1")
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    TOKEN_API_NAME: str = config("TOKEN_API_NAME", default="x-access-token")
    # to get a string like this run:
    # openssl rand -hex 64
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM", default="HS512")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30
    )
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    ACCOUNT_REGISTER_EXPIRE_MINUTES: int = config("", cast=int, default=5)  # in minutes
    TOTP_ACTIVE: bool = config("TOTP_ACTIVE", cast=bool, default=False)
    TOTP_DIGITS: int = config("TOTP_DIGITS", cast=int, default=6)
    TOTP_INTERVAL: int = config("TOTP_INTERVAL", cast=int, default=30)
    TOTP_VALIDE_WINDOW: int = config("TOTP_VALIDE_WINDOW", cast=int, default=0)
    QR_VERSION: int = config("QR_VERSION", cast=int, default=1)
    QR_BOX_SIZE: int = config("QR_BOX_SIZE", cast=int, default=10)
    QR_BORDER: int = config("QR_BORDER", cast=int, default=5)
    QR_FACTORY: str = config("QR_FACTORY", default=None)  # basic | fragment | None
    QR_FILLED: bool = config("QR_FILLED", cast=bool, default=False)
    QR_FIT: bool = config("QR_FIT", cast=bool, default=True)
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    # mongodb | mongodb+srv
    DB_PROTOCOL: str = config("DB_PROTOCOL", default="mongodb")
    DB_HOST: str = config("DB_HOST", default="localhost")
    DB_PORT: int = config("DB_PORT", cast=int, default=27017)
    DB_SCHEMA: str = config("DB_SCHEMA", default=None)
    # mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase
    DB_URL: Union[str, None] = config("DB_URL", default=None)
    DB_USER: str = config("DB_USER", default=None)
    DB_PASSWORD: str = config("DB_PASSWORD", default=None)
    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    SMTP_TLS: bool = config("SMTP_TLS", cast=bool, default=None)
    SMTP_PORT: Union[int, None] = config("SMTP_PORT", cast=int, default=None)
    SMTP_HOST: Union[str, None] = config("SMTP_HOST", default=None)
    SMTP_USER: Union[str, None] = config("SMTP_USER", default=None)
    SMTP_PASSWORD: Union[str, None] = config("SMTP_PASSWORD", default=None)
    EMAILS_FROM_EMAIL: Union[EmailStr, None] = config("EMAILS_FROM_EMAIL", default=None)
    EMAILS_FROM_NAME: Union[str, None] = config("EMAILS_FROM_NAME", default=None)

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    class Config:
        case_sensitive = True

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def print(self) -> None:
        if self.LOGGING_LEVEL == logging.getLevelName(logging.DEBUG):
            print()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            logging.log(
                verboselogs.VERBOSE,
                f"PROJECT_NAME           : {Bold(self.PROJECT_NAME)}",
            )
            logging.log(
                verboselogs.VERBOSE, f"VERSION                : {Bold(self.VERSION)}"
            )
            logging.log(
                verboselogs.VERBOSE, f"ENV_MODE               : {Bold(self.ENV_MODE)}"
            )
            logging.log(
                verboselogs.VERBOSE,
                f"LOGGING-LEVEL          : {Bold(self.LOGGING_LEVEL)}",
            )
            logging.log(
                verboselogs.VERBOSE,
                f"LOGGING-VERBOSE        : {Bold(self.LOGGING_VERBOSE)}",
            )
            logging.log(
                verboselogs.VERBOSE,
                f"DISABLED SPLIT PROJECT : {Bold(self.DISABLE_SPLIT_PROJECT)}",
            )
            logging.log(
                verboselogs.VERBOSE,
                f"DISABLED SPLIT HOST    : {Bold(self.DISABLE_SPLIT_HOST)}",
            )
            logging.log(
                verboselogs.VERBOSE,
                f"PRINT ONLY MODE        : {Bold(self.PRINT_ONLY_MODE)}",
            )
            # logging.log(
            #     verboselogs.VERBOSE,
            #     f'PROJECT-PATH           : {Bold(create_service_path(None))}{Bold("/")}',
            # )
            logging.log(
                verboselogs.VERBOSE, f"ENV-MODE               : {Bold(self.ENV_MODE)}"
            )
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print()


settings = Settings()
