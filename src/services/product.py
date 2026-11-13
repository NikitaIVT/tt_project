from uuid import UUID

from src.exceptions.exceptions import EntityNotFoundError

from src.repositories.mappers.mappers import ProductDataMapper
from src.repositories.products import ProductsRepository
from src.schemas.products import (
    ProductCreate,
    ProductPatch,
    Product,
    ProductDelete
)


class ProductService:
    def __init__(self, products_repository: ProductsRepository):
        self.products_repository = products_repository

    async def get_products(self) -> list[Product]:
        products = await self.products_repository.get_all()
        return [ProductDataMapper.map_to_schema(product) for product in products]

    async def get_product_by_uuid(self, product_id: UUID) -> Product:
        product = await self.products_repository.get_by_id(product_id)
        if product is None:
            raise EntityNotFoundError(product_id)
        return ProductDataMapper.map_to_schema(product)

    async def create_product(self, product: ProductCreate) -> Product:
        product_model = ProductDataMapper.map_to_db_model(product)
        created_product = await self.products_repository.create(product_model)

        return ProductDataMapper.map_to_schema(created_product)

    async def update_product(
        self,
        product_id: UUID,
        product: ProductPatch,
    ) -> Product:
        product_model = await self.products_repository.get_by_id(product_id)
        if product_model is None:
            raise EntityNotFoundError(product_id)
        update_data = product.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product_model, key, value)

        updated_product = await self.products_repository.update(product_model)

        return ProductDataMapper.map_to_schema(updated_product)


    async def soft_delete_product(self, product_id: UUID) -> ProductDelete:
        product_model = await self.products_repository.get_by_id(product_id)

        if product_model is None:
            raise EntityNotFoundError(product_id)

        deleted_product = await self.products_repository.delete(product_model)

        return ProductDataMapper.map_to_schema(deleted_product, ProductDelete)
