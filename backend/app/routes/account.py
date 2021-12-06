"""
    api to call for register a new user
    or login an existing user to get a token
"""

from typing import Any

from fastapi import APIRouter, Response
from fastapi.param_functions import Depends
from starlette import status

import app.persist.account.services.account as account
from app.middleware.auth import middlewareAuth
from app.persist.account.schemas.request import RequestLoginSchema, RequestRegistrationSchema
from app.persist.account.schemas.response import ResponseLoginSchema, ResponseRegistrationSchema
from app.schemas.response import ResponseSchema
from app.utils.api.requestHelper import requestHelper
from app.utils.api.securityHelper import TokenDataObject

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
router = APIRouter(prefix="/account", tags=["account"])


# TODO: 200,401,400
# NOTE: need to document what will resulted
# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
@router.post("/login", name="account:login", response_model=ResponseLoginSchema)
async def login(items: RequestLoginSchema, response: Response) -> Any:
    """
    login will handle usage for other api's

    - by response with a JWT-token
    - It will also return user information to display on GUI
    """
    return await requestHelper(
        response=response,
        func=account.login,
        keys=items,
        keysNeeded=RequestLoginSchema,
        funcCallerName="login",
    )


@router.post(
    "/register",
    name="account:register",
    response_model=ResponseRegistrationSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(items: RequestRegistrationSchema, response: Response) -> Any:
    """
    registration will handle creation for new users

    - all new user will have state = NEW
    - there will be 5min. to login and active the account
        - if login will called after 5min. the account will be deleted
    - if 2FA is activated, it will also return the secret-key and a SVG-QR-CODE
    """
    return await requestHelper(
        response=response,
        func=account.registration,
        keys=items,
        keysNeeded=RequestRegistrationSchema,
        funcCallerName="register",
    )


@router.delete("/remove", name="account:remove", response_model=ResponseSchema)
async def remove(
    response: Response, jwt: TokenDataObject = Depends(middlewareAuth)
) -> Any:
    """
    removes a existing user
    """
    return await requestHelper(
        token=jwt,
        response=response,
        func=account.remove,
        keys=None,
        keysNeeded=None,
        funcCallerName="remove",
    )
