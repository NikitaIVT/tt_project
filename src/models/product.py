from __future__ import annotations

from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.timestamp_soft_delete_mixin import TimestampSoftDeleteMixin


class Product(Base, TimestampSoftDeleteMixin):
    __tablename__ = 'product'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer)

    product_reviews: Mapped[list["ProductReview"]] = relationship(back_populates="product")
