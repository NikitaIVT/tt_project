from typing import Annotated

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    message: Annotated[str, Field(min_length=1, max_length=100)]