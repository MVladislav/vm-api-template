"""
    holds schemas for account request
"""

from typing import Optional

from pydantic.main import BaseModel

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class RequestRegistrationSchema(BaseModel):
    """
        handles attributes to send on request
    """
    name: str
    surname: str
    username: str
    password: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "name": "john",
                "surname": "doo",
                "username": "john_doo",
                "password": "mySecretPw",
                "email": "john@example.gg",
            }
        }


class RequestLoginSchema(BaseModel):
    """
        handles attributes to send on request
    """
    authCode: Optional[str]
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doo",
                "password": "mySecretPw",
                "authCode": "******",
            }
        }
