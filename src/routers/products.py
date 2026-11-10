from uuid import UUID

from fastapi import APIRouter

from src.routers.dependencies import DBDep, ProductServiceDep
from src.schemas.products import Product, ProductCreate, ProductPatch

router = APIRouter(prefix="/products", tags=["Продукты"])



@router.get("")
async def get_products(service: ProductServiceDep):
    return await service.get_products()


@router.post("")
async def create_product(
    service: ProductServiceDep,
    product: ProductCreate,
):
    return await service.create_product(product)


@router.patch("/{product_id}")
async def partially_update_product(
    service: ProductServiceDep,
    product_id: UUID,
    product: ProductPatch,
):
    return await service.partially_update_product(product_id, product)


@router.delete("/{product_id}")
async def soft_delete_product(
    service: ProductServiceDep,
    product_id: int,
):
    return await service.soft_delete_product(product_id)
