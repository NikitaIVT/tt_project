from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from src.models.base import Base
from src.models.types import created_at, updated_at, is_deleted


class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String())

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_deleted: Mapped[is_deleted]