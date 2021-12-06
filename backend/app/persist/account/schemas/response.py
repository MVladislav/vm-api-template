"""
    holds schemas for account response
"""

from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from app.schemas.response import ResponseSchema


# ------------------------------------------------------------------------------
#
# LOGIN schema
#
# ------------------------------------------------------------------------------
class ResponseLoginResultSchema(BaseModel):
    """
    handles response attributes on login
    """
    username: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    token: Optional[str]


class ResponseLoginSchema(ResponseSchema):
    """
    extends the base response schema for login attributes
    """
    RESULT: Optional[ResponseLoginResultSchema] = None




# ------------------------------------------------------------------------------
#
# REGISTRATION schema
#
# ------------------------------------------------------------------------------
class ResponseRegistrationResultSchema(BaseModel):
    """
    handles response attributes on registration
    """
    qrCode: Optional[str]
    secret: Optional[str]
    expireTime: Optional[str]
    expireDate: Optional[datetime]


class ResponseRegistrationSchema(ResponseSchema):
    """
    extends the base response schema for registration attributes
    """
    RESULT: Optional[ResponseRegistrationResultSchema] = None
