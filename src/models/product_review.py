from __future__ import annotations
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.models.timestamp_soft_delete_mixin import TimestampSoftDeleteMixin


class ProductReview(Base, TimestampSoftDeleteMixin):
    __tablename__ = "product_review"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    author_name: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String, nullable=True)
    stars: Mapped[int] = mapped_column(Integer)

    product: Mapped["Product"] = relationship(back_populates="product_reviews")
