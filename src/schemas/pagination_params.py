from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProductPaginationParams(BaseModel):
    product_per_page: int = Field(default=5, ge=1, le=100)
    product_last_seen_created_at: datetime | None = None
    product_last_seen_id: UUID | None = None
