from typing import Annotated

from fastapi import Depends

from src.dependencies.db import DBDep
from src.repositories.products import ProductsRepository
from src.services.product import ProductService


def get_product_service(db: DBDep) -> ProductService:
    products_repository = ProductsRepository(db)
    return ProductService(products_repository)


ProductServiceDep = Annotated[
    ProductService,
    Depends(get_product_service),
]
