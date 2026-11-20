from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.product_review import ProductReview, ProductReviewCreate, ProductReviewPatch, ProductReviewDelete

ProductName = Annotated[str, Field(min_length=1, max_length=20)]
ProductPrice = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
ProductQuantity = Annotated[int, Field(ge=0)]
ProductDescription = Annotated[str | None, Field(default=None, max_length=100)]


class ProductCreate(BaseModel):
    name: ProductName
    description: ProductDescription
    price: ProductPrice
    quantity: ProductQuantity
    product_reviews: list[ProductReviewCreate] = []


class Product(BaseModel):
    id: UUID
    name: ProductName
    description: ProductDescription
    price: ProductPrice
    quantity: ProductQuantity
    product_reviews: list[ProductReview] = []

    model_config = ConfigDict(from_attributes=True)


class ProductPatch(BaseModel):
    name: ProductName | None = None
    description: ProductDescription
    price: ProductPrice | None = None
    quantity: ProductQuantity | None = None

    product_reviews: list[ProductReviewPatch] | None = None


class ProductDelete(BaseModel):
    id: UUID
    is_deleted: bool = True
    product_reviews: list[ProductReviewDelete] = []

    model_config = ConfigDict(from_attributes=True)
