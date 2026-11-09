from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.schemas.types import NullableStr, NullableDecimal, NullableInt


class ProductCreate(BaseModel):
    name: str
    description: NullableStr
    price: Decimal
    quantity: int


class Product(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductPatch(BaseModel):
    name: NullableStr
    description: NullableStr
    price: NullableDecimal
    quantity: NullableInt


class ProductDelete(BaseModel):
    id: int
    is_deleted: bool = True
