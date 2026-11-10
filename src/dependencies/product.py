from typing import Annotated

from fastapi import Depends

from src.dependencies.db import DBDep
from src.services.product import ProductService


def get_product_service(db: DBDep) -> ProductService:
    return ProductService(db)


ProductServiceDep = Annotated[
    ProductService,
    Depends(get_product_service),
]