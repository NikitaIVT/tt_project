from cadwyn import Cadwyn


from src.routers.products import router as product_router
from src.routers.healthcheck import router as healthcheck_router


def add_routers(app: Cadwyn):
    app.generate_and_include_versioned_routers(
        product_router,
        healthcheck_router,
    )
