from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_read_session, get_session
from src.repositories.products import ProductsRepository
from src.services.product import ProductService


def product_service_dependency(session_dependency):
    def dependency(
        session: Annotated[AsyncSession, Depends(session_dependency)],
    ) -> ProductService:
        repository = ProductsRepository(session)
        return ProductService(repository)

    return dependency


get_read_product_service = product_service_dependency(get_read_session)
get_product_service = product_service_dependency(get_session)

ProductServiceReadDep = Annotated[
    ProductService,
    Depends(get_read_product_service),
]

ProductServiceDep = Annotated[
    ProductService,
    Depends(get_product_service),
]
