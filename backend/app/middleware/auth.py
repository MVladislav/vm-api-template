"""
    authentication middleware
    checks if a token is present and if the token is valid
    will the forward token user info to next handlers
"""

from typing import Union

from fastapi import Depends, status
from fastapi.openapi.models import APIKey

from app.utils.api.exceptionHandler import UnicornException
from app.utils.api.responseHelper import ErrorTypeEnum, MsgTypeEnum, ResponseHandlerObject, responseHandler
from app.utils.api.securityHelper import TokenDataObject, getTokenFromRequest, validateToken
from app.utils.config import settings

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
# security = HTTPBearer()   # :HTTPBasicCredentials
security = getTokenFromRequest  # :APIKey


# security = oauth2_scheme    # :...
async def middlewareAuth(
    token: Union[APIKey, None] = Depends(security)
) -> TokenDataObject:
    if token is None:
        resp = responseHandler(
            [
                ResponseHandlerObject(
                    msgType=MsgTypeEnum.ERROR,
                    errorType=ErrorTypeEnum.TOKEN_ACCESS_DENIED_EMPTY,
                ),
                ResponseHandlerObject(
                    msgType=MsgTypeEnum.STATE, errorType=ErrorTypeEnum.ACCESS_DECLINE
                ),
            ],
            status.HTTP_401_UNAUTHORIZED,
        )
        raise UnicornException(
            status_code=resp.httpCode,
            detail=resp.msg,
            headers={settings.TOKEN_API_NAME: "***"},
        )

    # validate token
    user = validateToken(token.name)
    if user is None:
        resp = responseHandler(
            [
                ResponseHandlerObject(
                    msgType=MsgTypeEnum.ERROR,
                    errorType=ErrorTypeEnum.TOKEN_ACCESS_DENIED_WRONG,
                ),
                ResponseHandlerObject(
                    msgType=MsgTypeEnum.STATE, errorType=ErrorTypeEnum.ACCESS_DECLINE
                ),
            ],
            status.HTTP_401_UNAUTHORIZED,
        )
        raise UnicornException(
            status_code=resp.httpCode,
            detail=resp.msg,
            headers={settings.TOKEN_API_NAME: "***"},
        )

    return user
