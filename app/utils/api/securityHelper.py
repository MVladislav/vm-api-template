import logging
from datetime import datetime, timedelta
from typing import Optional

import pyotp
from app.utils.config import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                              API_PREFIX, SECRET_KEY, TOKEN_API_NAME,
                              TOTP_DIGITS, TOTP_INTERVAL, TOTP_VALIDE_WINDOW)
from fastapi.param_functions import Security
from fastapi.security import (APIKeyCookie, APIKeyHeader, APIKeyQuery,
                              OAuth2PasswordBearer)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ------------------------------------------------------------------------------
#
# TYPES
#
# ------------------------------------------------------------------------------


class TokenObject(BaseModel):
    """
        object to handle return type of "create_access_token"
    """
    access_token: str
    token_type: str


class TokenDataObject(BaseModel):
    """
        object what is needed to add into JWT public part
    """
    id: Optional[str] = None
    username: Optional[str] = None
    isAdmin: Optional[bool] = None
    exp: Optional[datetime] = None

# ------------------------------------------------------------------------------
#
# GENERAL definitions
#
# ------------------------------------------------------------------------------


# defined context, for how to has a password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# define schema how to access token
# NOTE: not used oauth2, api key is used, with JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/account/token")


async def getTokenFromRequest(
    api_key_query: str = Security(APIKeyQuery(name=TOKEN_API_NAME, auto_error=False)),
    api_key_header: str = Security(APIKeyHeader(name=TOKEN_API_NAME, auto_error=False)),
    api_key_cookie: str = Security(APIKeyCookie(name=TOKEN_API_NAME, auto_error=False)),
):
    """
        auth depends helper, to get token from request
    """
    if api_key_header is not None:
        return api_key_header
    elif api_key_query is not None:
        return api_key_query
    elif api_key_cookie is not None:
        return api_key_cookie
    return None


# ------------------------------------------------------------------------------
#
# AUTH tooling
#
# ------------------------------------------------------------------------------


def create_access_token(data: TokenDataObject,
                        expires_delta: Optional[timedelta] = None) -> TokenObject:
    """
        creates and jwt token

        @data: add user information into jwt token
        @expires_delta: the time how long a token should be valid
        @return a object where the JWT-token is included
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.exp = expire
        encoded_jwt = jwt.encode(claims=to_encode.dict(), key=SECRET_KEY, algorithm=ALGORITHM)
        return TokenObject(access_token=encoded_jwt, token_type="api_key")
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None


def validateToken(token: str) -> TokenDataObject:
    """
        validates a token and returns user information if valid
        else empty
    """
    result: TokenDataObject = None
    try:
        if token is not None:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            result = TokenDataObject(**payload)
    except JWTError as ex:
        logging.log(logging.ERROR, ex)
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return result

# ------------------------------------------------------------------------------
#
# PASSWORD tooling
#
# ------------------------------------------------------------------------------


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None


def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None


# ------------------------------------------------------------------------------
#
# TOTP tooling
#
# ------------------------------------------------------------------------------


def totpCreate() -> str:
    try:
        return pyotp.TOTP(s=pyotp.random_base32(), digits=TOTP_DIGITS, interval=TOTP_INTERVAL)
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None


def totpVerify(secret: str, otp: str) -> bool:
    try:
        return pyotp.TOTP(s=secret, digits=TOTP_DIGITS,
                          interval=TOTP_INTERVAL).verify(otp=otp, valid_window=TOTP_VALIDE_WINDOW)
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None
