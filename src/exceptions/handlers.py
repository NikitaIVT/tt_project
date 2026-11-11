from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions.product import ProductNotFoundError


async def product_not_found_handler(request: Request, exc: ProductNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": f"Product {exc.uuid} not found."},
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(ProductNotFoundError, product_not_found_handler)
