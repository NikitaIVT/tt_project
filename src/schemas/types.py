from decimal import Decimal
from typing import Annotated

from pydantic import Field


NullableStr = Annotated[str | None, Field(default=None)]
NullableDecimal = Annotated[Decimal | None, Field(default=None)]
NullableInt = Annotated[int | None, Field(default=None)]
