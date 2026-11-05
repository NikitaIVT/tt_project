from decimal import Decimal

from sqlalchemy import String, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.types import created_at, updated_at, intpk, is_deleted


class Product(Base):
    __tablename__ = 'product'
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer(), nullable=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_deleted: Mapped[is_deleted]

