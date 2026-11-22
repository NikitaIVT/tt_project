from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProductPaginationParams(BaseModel):
    product_per_page: int = Field(default=5, ge=1, le=100)
    product_last_seen_created_at: datetime | None = None
    product_last_seen_id: UUID | None = None


class ReviewPaginationParams(BaseModel):
    review_page: int = Field(default=1, ge=1)
    review_per_page: int = Field(default=2, ge=1, le=100)