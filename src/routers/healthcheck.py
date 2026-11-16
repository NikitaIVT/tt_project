from http import HTTPStatus

from cadwyn import VersionedAPIRouter
from pydantic import BaseModel

router = VersionedAPIRouter()


class HealthcheckResponse(BaseModel):
    status: str


@router.get(
    "/healthcheck",
    response_model=HealthcheckResponse,
    status_code=HTTPStatus.OK,
)
async def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(status="ok")
