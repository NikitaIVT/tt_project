from http import HTTPStatus

from cadwyn import Cadwyn
from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.product import ProductNotFoundError
from src.schemas.responses import ErrorResponse


async def product_not_found_handler(request: Request, exc: ProductNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=ErrorResponse(message=f"Product {exc.uuid} not found.").model_dump(),
    )


def add_exception_handlers(app: Cadwyn):
    app.add_exception_handler(ProductNotFoundError, product_not_found_handler)
