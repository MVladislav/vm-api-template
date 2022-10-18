from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic.fields import Field
from pydantic.networks import EmailStr

from app.db.mongoDb import MongoModel


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class UserStatusEnum(str, Enum):
    ACTIVE = ("ACTIVE",)
    DEACTIVATE = ("DEACTIVATE",)
    DELETED = ("DELETED",)
    NEW = ("NEW",)


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class UserEntity(MongoModel):
    name: str = Field()
    surname: str = Field()
    username: str = Field(unique=True)
    password: str = Field()
    email: EmailStr = Field()
    token: Optional[str] = Field(default=None)
    totpToken: Optional[str] = Field()
    accountExpireDate: Optional[datetime] = Field()
    status: UserStatusEnum = Field()
    created: datetime = Field(default=datetime.now())
    lastLogin: datetime = Field(default=datetime.now())
    isAdmin: bool = Field(default=False)
