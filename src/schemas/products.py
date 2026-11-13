from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.constraints.product import ProductName, ProductPrice, ProductQuantity, ProductDescription


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
    description: ProductDescription | None = None
    price: ProductPrice | None = None
    quantity: ProductQuantity | None = None


class ProductDelete(BaseModel):
    id: UUID
    is_deleted: bool = True

    model_config = ConfigDict(from_attributes=True)
