import logging
from typing import Any, Callable, Coroutine, List, Union

from fastapi import Response, status

from app.schemas.response import ResponseSchema
from app.utils.api.responseHelper import (
    ErrorTypeEnum,
    MsgTypeEnum,
    ResponseHandlerObject,
    ResponseHolderObject,
    responseHandler,
)
from app.utils.api.securityHelper import TokenDataObject


async def requestHelper(
    funcCallerName: Union[str, None],
    response: Union[Response, None],
    func: Union[
        Callable[[Any], Coroutine[Any, Any, Union[ResponseHolderObject, None]]], None
    ],
    keys: Union[Any, None],
    keysNeeded: Union[type, None],
    token: Union[TokenDataObject, None] = None,
) -> Union[ResponseSchema, None]:
    if response is not None:
        result: ResponseHolderObject = responseHandler(
            [
                ResponseHandlerObject(
                    msgType=MsgTypeEnum.ERROR,
                    errorType=ErrorTypeEnum.API_FUNCTION_ERROR,
                ),
                ResponseHandlerObject(
                    msgType=MsgTypeEnum.STATE, errorType=ErrorTypeEnum.INTERNAL_ERROR
                ),
            ],
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        try:
            if funcCallerName is not None and func is not None:
                if (
                    keys is not None and
                    keysNeeded is not None and
                    type(keys) == keysNeeded
                ) or (
                    keys is None and keysNeeded is None
                ):
                    resp: Union[ResponseHolderObject, None] = None
                    if keys is None and keysNeeded is None:
                        if token is None:
                            resp = await func()
                        else:
                            resp = await func(keys)
                    else:
                        if token is None:
                            resp = await func(keys)
                        else:
                            resp = await func(token, keys)
                    if resp is not None:
                        result = resp
                    else:
                        logging.log(
                            logging.WARNING,
                            f"api function call return 'None' for api:: {funcCallerName}",
                        )
                else:
                    result = responseHandler(
                        [
                            ResponseHandlerObject(
                                msgType=MsgTypeEnum.ERROR,
                                errorType=ErrorTypeEnum.API_MISSING_ATTRIBUTES,
                            ),
                            ResponseHandlerObject(
                                msgType=MsgTypeEnum.STATE,
                                errorType=ErrorTypeEnum.INTERNAL_ERROR,
                            ),
                        ],
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                logging.log(
                    logging.WARNING,
                    f"not all values are set ({funcCallerName}): response: : {response is not None},func:: {func is not None}, keysNeeded: : {keysNeeded is not None},funcCallerName: : {funcCallerName is not None}",
                )
                result = responseHandler(
                    [
                        ResponseHandlerObject(
                            msgType=MsgTypeEnum.ERROR,
                            errorType=ErrorTypeEnum.API_MISSING_PARAMS,
                        ),
                        ResponseHandlerObject(
                            msgType=MsgTypeEnum.STATE,
                            errorType=ErrorTypeEnum.INTERNAL_ERROR,
                        ),
                    ],
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            all_codes: List[int] = [
                100,
                101,
                102,
                103,
                200,
                201,
                202,
                203,
                204,
                205,
                206,
                207,
                208,
                226,
                300,
                301,
                302,
                303,
                304,
                305,
                306,
                307,
                308,
                400,
                401,
                402,
                403,
                404,
                405,
                406,
                407,
                408,
                409,
                410,
                411,
                412,
                413,
                414,
                415,
                416,
                417,
                418,
                421,
                422,
                423,
                424,
                425,
                426,
                428,
                429,
                431,
                451,
                500,
                501,
                502,
                503,
                504,
                505,
                506,
                507,
                508,
                510,
                511,
                1000,
                1001,
                1002,
                1003,
                1004,
                1005,
                1007,
                1008,
                1009,
                1010,
                1011,
                1012,
                1013,
                1014,
                1015,
            ]
            if result.httpCode in all_codes:
                response.status_code = result.httpCode
            else:
                logging.log(
                    logging.WARNING,
                    f"status code is wrong, need internal fix ({funcCallerName}): {result.httpCode}",
                )
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            logging.log(logging.CRITICAL, e, exc_info=True)
        return result.msg

    else:
        logging.log(logging.ERROR, "response is not set, can not send any response")
    return None
