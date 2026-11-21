from sqlalchemy.orm import Mapped
from src.models.types import created_at, updated_at, is_deleted


class TimestampSoftDeleteMixin:
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_deleted: Mapped[is_deleted]
