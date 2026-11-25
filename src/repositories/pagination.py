from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProductPagination(BaseModel):
    limit: int
    last_seen_created_at: datetime | None = None
    last_seen_id: UUID | None = None
