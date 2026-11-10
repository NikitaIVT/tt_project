from uuid import UUID

from src.schemas.products import ProductCreate, ProductPatch, ProductDelete


class ProductService:
    def __init__(self, db):
        self.db = db

    async def get_products(self):
        products = await self.db.products.get_all()
        return {"status": "ok", "data": products}

    async def create_product(self, product: ProductCreate):
        await self.db.products.create(product)
        await self.db.commit()
        return {"status": "ok"}

    async def partially_update_product(
        self,
        product_id: UUID,
        product: ProductPatch,
    ):
        updated_rows = await self.db.products.update(
            product,
            exclude_unset=True,
            id=product_id,
        )
        await self.db.commit()
        return {"status": "ok", "info": f"Updated {updated_rows} rows"}

    async def edit_product(
        self,
        product_id: UUID,
        product: ProductCreate,
    ):
        updated_rows = await self.db.products.update(
            product,
            exclude_unset=False,
            id=product_id,
        )
        await self.db.commit()
        return {"status": "ok", "info": f"Updated {updated_rows} rows"}

    async def soft_delete_product(
        self,
        product_id: UUID,
    ):
        deleted_rows = await self.db.products.set_is_deleted(product_id)
        await self.db.commit()
        return {"status": "ok", "info": f"Deleted {deleted_rows} rows"}
