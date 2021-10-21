from typing import List

from starlette.config import Config

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

config = Config(".env")

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


LICENSE: str = config("LICENSE", default="GNU AGPLv3")
AUTHOR: str = config("AUTHOR", default="MVladislav")
AUTHOR_EMAIL: str = config("AUTHOR_EMAIL", default="info@mvladislav.online")

PROJECT_NAME: str = config("PROJECT_NAME", default="Project Name")
ENV_MODE: str = config("ENV_MODE", default="KONS")
VERSION: str = config("VERSION", default="0.0.1")

# NOTICE | SPAM | DEBUG | VERBOSE | INFO | NOTICE | WARNING | SUCCESS | ERROR | CRITICAL
LOGGING_LEVEL: str = config("LOGGING_LEVEL",  default="DEBUG")
LOGGING_VERBOSE: int = config("LOGGING_VERBOSE", cast=int,  default=2)
DEBUG: bool = True if LOGGING_LEVEL == "DEBUG" or \
    LOGGING_LEVEL == "VERBOSE" or LOGGING_LEVEL == "SPAM" else False
DEBUG_RELOAD: bool = True if DEBUG else False

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

PROTOCOL: str = config("PROTOCOL",  default="http")
HOST: str = config("HOST",  default="127.0.0.1")
PORT: int = config("PORT", cast=int, default=8000)

ALLOW_CREDENTIALS: bool = config("ALLOW_CREDENTIALS", cast=bool, default=True)
ALLOWED_METHODES: List[str] = config("ALLOWED_METHODES", cast=str,
                                     default=["OPTIONS", "GET"]).split(",")
ALLOWED_HEADERS: List[str] = config("ALLOWED_HEADERS", cast=str, default=["*"]).split(",")

API_PREFIX = config("API_PREFIX",  default="/api/v1")

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

TOKEN_API_NAME: str = config("TOKEN_API_NAME", default="x-access-token")
# to get a string like this run:
# openssl rand -hex 64
SECRET_KEY: str = config("SECRET_KEY")
ALGORITHM: str = config("ALGORITHM",  default="HS512")
ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

ACCOUNT_REGISTER_EXPIRE_MINUTES: int = config("", cast=int,  default=5)  # in minutes

TOTP_ACTIVE: bool = config("TOTP_ACTIVE", cast=bool,  default=False)
TOTP_DIGITS: int = config("TOTP_DIGITS", cast=int,  default=6)
TOTP_INTERVAL: int = config("TOTP_INTERVAL", cast=int,  default=30)
TOTP_VALIDE_WINDOW: int = config("TOTP_VALIDE_WINDOW", cast=int,  default=0)

QR_VERSION: int = config("QR_VERSION", cast=int,  default=1)
QR_BOX_SIZE: int = config("QR_BOX_SIZE", cast=int,  default=10)
QR_BORDER: int = config("QR_BORDER", cast=int,  default=5)
QR_FACTORY: str = config("QR_FACTORY",  default=None)  # basic | fragment | None
QR_FILLED: bool = config("QR_FILLED", cast=bool,  default=False)
QR_FIT: bool = config("QR_FIT", cast=bool,  default=True)

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

# mongodb | mongodb+srv
DB_PROTOCOL: str = config("DB_PROTOCOL",  default="mongodb")
DB_HOST: str = config("DB_HOST",  default="localhost")
DB_PORT: int = config("DB_PORT", cast=int,  default=27017)
DB_SCHEMA: str = config("DB_SCHEMA",  default=None)
# mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase
DB_URL: str = config("DB_URL",  default=None)
DB_USER: str = config("DB_USER",  default=None)
DB_PASSWORD: str = config("DB_PASSWORD",  default=None)
