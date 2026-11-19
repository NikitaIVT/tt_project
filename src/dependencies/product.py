from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_read_session, get_session
from src.mappers.mappers import ProductDataMapper, ProductReviewDataMapper
from src.repositories.products import ProductsRepository
from src.services.product import ProductService


def get_product_mapper() -> type[ProductDataMapper]:
    return ProductDataMapper

def get_product_review_mapper() -> type[ProductReviewDataMapper]:
    return ProductReviewDataMapper


def product_service_dependency(session_dependency):
    def dependency(
        session: Annotated[AsyncSession, Depends(session_dependency)],
        data_mapper: Annotated[type[ProductDataMapper], Depends(get_product_mapper)],
        product_review_mapper: Annotated[type[ProductReviewDataMapper], Depends(get_product_review_mapper)]
    ) -> ProductService:
        repository = ProductsRepository(session)
        return ProductService(repository, data_mapper, product_review_mapper)
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
