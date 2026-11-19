from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


ProductReviewAuthorName = Annotated[str, Field(min_length=1, max_length=20)]
ProductReviewStars = Annotated[int, Field(ge=1, le=5)]
ProductReviewText = Annotated[str | None, Field(default=None, max_length=100)]


class ProductReviewCreate(BaseModel):
    author_name: ProductReviewAuthorName
    text: ProductReviewText
    stars: ProductReviewStars


class ProductReview(ProductReviewCreate):
    id: UUID
    product_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProductReviewPatch(BaseModel):
    id: UUID
    author_name: ProductReviewAuthorName | None = None
    text: ProductReviewText
    stars: ProductReviewStars | None = None


class ProductReviewDelete(BaseModel):
    id: UUID
    is_deleted: bool = True

    model_config = ConfigDict(from_attributes=True)
