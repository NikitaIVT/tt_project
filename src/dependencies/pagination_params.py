from typing import Annotated

from fastapi import Depends

from src.schemas.pagination_params import ProductPaginationParams

ProductPaginationDep = Annotated[ProductPaginationParams, Depends()]
