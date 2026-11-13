from cadwyn import Cadwyn
from starlette.middleware.cors import CORSMiddleware

from src.exceptions.handlers import add_exception_handlers
from src.routers.routers import add_routers
from src.versions import versions


def get_app() -> Cadwyn:
    app = Cadwyn(versions=versions)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    add_exception_handlers(app)
    add_routers(app)

    return app
