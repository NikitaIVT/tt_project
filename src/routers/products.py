from uuid import UUID

from cadwyn import VersionedAPIRouter
from starlette import status

from src.dependencies.product import ProductServiceDep, ProductServiceReadDep
from src.schemas.products import ProductCreate, ProductPatch

router = VersionedAPIRouter(prefix="/products", tags=["Продукты"])


@router.get("")
async def get_products(product_service: ProductServiceReadDep):
    return await product_service.get_products()


@router.get("/{product_id}")
async def get_product(product_id: UUID, product_service: ProductServiceReadDep):
    return await product_service.get_product_by_uuid(product_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_service: ProductServiceDep,
    product: ProductCreate,
):
    return await product_service.create_product(product)


@router.patch("/{product_id}")
async def update_product(
    product_service: ProductServiceDep,
    product_id: UUID,
    product: ProductPatch,
):
    return await product_service.update_product(product_id, product)


@router.delete("/{product_id}")
async def soft_delete_product(
    product_service: ProductServiceDep,
    product_id: UUID,
):
    return await product_service.soft_delete_product(product_id)
