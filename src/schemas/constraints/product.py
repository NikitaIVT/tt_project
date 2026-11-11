from decimal import Decimal
from typing import Annotated

from pydantic import Field


ProductName = Annotated[str, Field(min_length=1, max_length=20)]
ProductPrice = Annotated[Decimal, Field(gt=0)]
ProductQuantity = Annotated[int, Field(ge=0)]
ProductDescription = Annotated[str | None, Field(default=None, max_length=100)]
