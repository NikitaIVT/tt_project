from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from src.models.types import created_at, updated_at, is_deleted


class TimestampSoftDeleteMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_deleted: Mapped[is_deleted]
