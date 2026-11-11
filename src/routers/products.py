from uuid import UUID

from fastapi import APIRouter

from src.dependencies.product import ProductServiceDep
from src.schemas.products import ProductCreate, ProductPatch

router = APIRouter(prefix="/products", tags=["Продукты"])



@router.get("")
async def get_products(product_service: ProductServiceDep):
    return await product_service.get_products()


@router.get("/{product_id}")
async def get_product(product_id: UUID, product_service: ProductServiceDep):
    return await product_service.get_product_by_uuid(product_id)


@router.post("")
async def create_product(
    product_service: ProductServiceDep,
    product: ProductCreate,
):
    return await product_service.create_product(product)


@router.patch("/{product_id}")
async def partially_update_product(
    product_service: ProductServiceDep,
    product_id: UUID,
    product: ProductPatch,
):
    return await product_service.partially_update_product(product_id, product)


@router.delete("/{product_id}")
async def soft_delete_product(
    product_service: ProductServiceDep,
    product_id: UUID,
):
    return await product_service.soft_delete_product(product_id)
