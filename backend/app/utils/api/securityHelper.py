import logging
from datetime import datetime, timedelta
from typing import Optional, Union

import pyotp
from fastapi.param_functions import Security
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.utils.config import settings


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
pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
# define schema how to access token
# NOTE: not used oauth2, api key is used, with JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/account/token")


async def getTokenFromRequest(
    api_key_query: Union[str, None] = Security(
        APIKeyQuery(name=settings.TOKEN_API_NAME, auto_error=False)
    ),
    api_key_header: Union[str, None] = Security(
        APIKeyHeader(name=settings.TOKEN_API_NAME, auto_error=False)
    ),
    api_key_cookie: Union[str, None] = Security(
        APIKeyCookie(name=settings.TOKEN_API_NAME, auto_error=False)
    ),
) -> Union[str, None]:
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
def create_access_token(
    data: TokenDataObject, expires_delta: Optional[timedelta] = None
) -> Union[TokenObject, None]:
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
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.exp = expire
        encoded_jwt = jwt.encode(
            claims=to_encode.dict(),
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return TokenObject(access_token=encoded_jwt, token_type="api_key")

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return None


def validateToken(token: Union[str, None]) -> Union[TokenDataObject, None]:
    """
    validates a token and returns user information if valid
    else empty
    """
    result: Union[TokenDataObject, None] = None
    try:
        if token is not None:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            result = TokenDataObject(**payload)
    except JWTError as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return result




# ------------------------------------------------------------------------------
#
# PASSWORD tooling
#
# ------------------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bool(pwd_context.verify(plain_password, hashed_password))

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return False


def get_password_hash(password: str) -> Union[str, None]:
    try:
        return str(pwd_context.hash(password))

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return None




# ------------------------------------------------------------------------------
#
# TOTP tooling
#
# ------------------------------------------------------------------------------
def totpCreate() -> Union[pyotp.TOTP, None]:
    try:
        return pyotp.TOTP(
            s=pyotp.random_base32(),
            digits=settings.TOTP_DIGITS,
            interval=settings.TOTP_INTERVAL,
        )

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return None


def totpVerify(secret: str, otp: str) -> bool:
    try:
        return pyotp.TOTP(
            s=secret, digits=settings.TOTP_DIGITS, interval=settings.TOTP_INTERVAL
        ).verify(
            otp=otp, valid_window=settings.TOTP_VALIDE_WINDOW
        )

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return False
