from fastapi import FastAPI

from src.routers.products import router as product_router
from src.routers.healthcheck import router as healthcheck_router


def add_routers(app: FastAPI):
    app.include_router(product_router)
    app.include_router(healthcheck_router)