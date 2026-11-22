from pydantic import BaseModel, Field


class ProductPaginationParams(BaseModel):
    product_page: int = Field(default=1, ge=1)
    product_per_page: int = Field(default=2, ge=1, le=100)


class ReviewPaginationParams(BaseModel):
    review_page: int = Field(default=1, ge=1)
    review_per_page: int = Field(default=2, ge=1, le=100)