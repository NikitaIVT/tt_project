from uuid import UUID

from src.exceptions.product import ProductNotFoundError
from src.models import Product as ProductModel
from src.repositories.products import ProductsRepository
from src.schemas.products import (
    ProductCreate,
    ProductPatch,
    Product as ProductSchema,
    ProductDelete
)


class ProductService:
    def __init__(self, products_repository: ProductsRepository):
        self.products_repository = products_repository

    async def get_products(self) -> list[ProductSchema]:
        products = await self.products_repository.get_all()
        return [ProductSchema.model_validate(product) for product in products]


    async def get_product_by_uuid(self, product_id: UUID) -> ProductSchema:
        product = await self.products_repository.get_by_uuid(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return ProductSchema.model_validate(product)

    async def create_product(self, product: ProductCreate) -> ProductModel:
        product_model = ProductModel(**product.model_dump())
        created_product = await self.products_repository.create(product_model)

        return ProductSchema.model_validate(created_product)


    async def update_product(
        self,
        product_id: UUID,
        product: ProductPatch,
    ) -> ProductSchema:
        product_model = await self.products_repository.get_by_uuid(product_id)
        if product_model is None:
            raise ProductNotFoundError(product_id)

        update_data = product.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product_model, key, value)

        updated_product = await self.products_repository.update(product_model)

        return ProductSchema.model_validate(updated_product)


    async def soft_delete_product(self, product_id: UUID) -> ProductDelete:
        product_model = await self.products_repository.get_by_uuid(product_id)

        if product_model is None:
            raise ProductNotFoundError(product_id)

        product_model.is_deleted = True
        deleted_product = await self.products_repository.update(product_model)

        return ProductDelete.model_validate(deleted_product)
