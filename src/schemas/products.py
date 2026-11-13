from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


ProductName = Annotated[str, Field(min_length=1, max_length=20)]
ProductPrice = Annotated[Decimal, Field(gt=0)]
ProductQuantity = Annotated[int, Field(ge=0)]
ProductDescription = Annotated[str | None, Field(default=None, max_length=100)]


class ProductCreate(BaseModel):
    name: ProductName
    description: ProductDescription
    price: ProductPrice
    quantity: ProductQuantity


class Product(ProductCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProductPatch(BaseModel):
    name: ProductName | None = None
    description: ProductDescription
    price: ProductPrice | None = None
    quantity: ProductQuantity | None = None


class ProductDelete(BaseModel):
    id: UUID
    is_deleted: bool = True

    model_config = ConfigDict(from_attributes=True)
