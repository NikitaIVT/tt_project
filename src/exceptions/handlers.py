from http import HTTPStatus

from cadwyn import Cadwyn
from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.exceptions import EntityNotFoundError
from src.schemas.responses import ErrorResponse


async def entity_not_found_handler(request: Request, exc: EntityNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=ErrorResponse(message=f"Entity {exc.uuid} not found.").model_dump(),
    )


def add_exception_handlers(app: Cadwyn):
    app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
