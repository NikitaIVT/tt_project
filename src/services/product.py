from collections.abc import Sequence
from uuid import UUID

from src.models import Product as ProductModel
from src.repositories.products import ProductsRepository
from src.schemas.products import ProductCreate, ProductPatch


class ProductService:
    def __init__(self, products_repository: ProductsRepository):
        self.products_repository = products_repository

    async def get_products(self) -> dict[str, str | Sequence[ProductModel]]:
        products = await self.products_repository.get_all()
        return {"status": "ok", "data": products}

    async def create_product(self, product: ProductCreate):
        await self.products_repository.create(product)
        return {"status": "ok"}

    async def partially_update_product(
        self,
        product_id: UUID,
        product: ProductPatch,
    ):
        updated_rows = await self.products_repository.update(
            product,
            exclude_unset=True,
            id=product_id,
        )
        return {"status": "ok", "info": f"Updated {updated_rows} rows"}

    async def edit_product(
        self,
        product_id: UUID,
        product: ProductCreate,
    ):
        updated_rows = await self.products_repository.update(
            product,
            exclude_unset=False,
            id=product_id,
        )
        return {"status": "ok", "info": f"Updated {updated_rows} rows"}

    async def soft_delete_product(
        self,
        product_id: UUID,
    ):
        deleted_rows = await self.products_repository.set_is_deleted(product_id)
        return {"status": "ok", "info": f"Deleted {deleted_rows} rows"}
