from typing import Any, Optional

from pydantic import BaseModel


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class ResponseSchema(BaseModel):
    """
    handles base response attributes.
    will be used by other response schema to extends
    the attributes with more specific data
    """
    ERROR: Optional[Any] = None
    RESULT: Optional[Any] = None
    INFO: Optional[Any] = None
    STATE: Optional[Any] = None
