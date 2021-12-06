import logging
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel

from app.schemas.response import ResponseSchema
from app.utils.logHelper import LoggingMsgType, loggingMsgHandler


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class MsgTypeEnum(str, Enum):
    ERROR = "ERROR"
    RESULT = "RESULT"
    INFO = "INFO"
    STATE = "STATE"


class ErrorTypeEnum(str, Enum):
    API_MISSING_ATTRIBUTES = "API_MISSING_ATTRIBUTES"
    API_MISSING_PARAMS = "API_MISSING_PARAMS"
    API_FUNCTION_ERROR = "API_FUNCTION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    ACCESS_GRANT = "ACCESS_GRANT"
    ACCESS_DECLINE = "ACCESS_DECLINE"
    ACCESS_FAILED = "ACCESS_FAILED"
    TOKEN_ACCESS_DENIED_WRONG = "TOKEN_ACCESS_DENIED_WRONG"
    TOKEN_ACCESS_DENIED_EMPTY = "TOKEN_ACCESS_DENIED_EMPTY"
    NOT_FOUND = "NOT_FOUND"
    REMOVED = "REMOVED"
    TOTP_DECLINE = "TOTP_DECLINE"


class ResponseHolderObject(BaseModel):
    httpCode: int
    msg: ResponseSchema


class ResponseHandlerObject(BaseModel):
    msgType: MsgTypeEnum
    msg: Optional[Any]
    errorType: Optional[ErrorTypeEnum]




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def responseHandler(
    params: List[ResponseHandlerObject], code: int = 200
) -> ResponseHolderObject:
    """
    an helper function to create a object for response
    which has a http code
    and a default json msg schema
    """
    result: ResponseHolderObject = ResponseHolderObject(
        httpCode=code, msg=ResponseSchema()
    )
    try:
        for param in params:
            if param.msg is None and param.errorType is None:
                logging.log(logging.WARNING, loggingMsgHandler(LoggingMsgType.EMPTY))
            if param.errorType is not None:
                param.msg = responseMsgHandler(param.errorType)
            for msgT in MsgTypeEnum:
                if param.msgType == msgT:
                    setattr(result.msg, msgT.name, param.msg)
        return result

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return result




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def responseMsgHandler(argument: ErrorTypeEnum) -> Union[str, None]:
    """
    holds some defalt msg, which can be usedmultiple times
    """
    try:
        switcher = {
            ErrorTypeEnum.API_MISSING_ATTRIBUTES: "missing attributes in body or header",
            ErrorTypeEnum.API_MISSING_PARAMS: "function on API call has not set all params",
            ErrorTypeEnum.API_FUNCTION_ERROR: "function on API call return null",
            ErrorTypeEnum.INTERNAL_ERROR: "INTERNAL ERROR",
            ErrorTypeEnum.ACCESS_GRANT: "ACCESS GRANT",
            ErrorTypeEnum.ACCESS_DECLINE: "ACCESS DECLINED",
            ErrorTypeEnum.ACCESS_FAILED: "your login credentials are wrong, or you have no access",
            ErrorTypeEnum.TOTP_DECLINE: "2FA verification failed",
            ErrorTypeEnum.TOKEN_ACCESS_DENIED_WRONG: "Access denied. Invalid token.",
            ErrorTypeEnum.TOKEN_ACCESS_DENIED_EMPTY: "Access denied. No token provided.",
        }
        return switcher.get(argument, None)

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return None
