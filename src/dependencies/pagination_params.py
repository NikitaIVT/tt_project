from typing import Annotated

from fastapi import Depends

from src.schemas.pagination_params import ProductPaginationParams, ReviewPaginationParams

ProductPaginationDep = Annotated[ProductPaginationParams, Depends()]
ReviewPaginationDep = Annotated[ReviewPaginationParams, Depends()]
