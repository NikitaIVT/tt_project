from uuid import UUID

from src.exceptions.entity_not_found import EntityNotFoundError
from src.mappers.mappers import ProductDataMapper
from src.repositories.products import ProductsRepository
from src.schemas.products import (
    ProductCreate,
    ProductPatch,
    Product,
    ProductDelete
)
from src.models import Product as ProductModel


class ProductService:
    def __init__(self, products_repository: ProductsRepository, product_mapper: type[ProductDataMapper]):
        self.products_repository = products_repository
        self.product_mapper = product_mapper

    async def _get_product_or_raise(self, product_id: UUID) -> ProductModel:
        product = await self.products_repository.get_by_id(product_id)
        if product is None:
            raise EntityNotFoundError(product_id)
        return product

    async def get_products(self) -> list[Product]:
        products = await self.products_repository.get_all()
        return self.product_mapper.map_to_schemas(products)

    async def get_product_by_uuid(self, product_id: UUID) -> Product:
        product_model = await self._get_product_or_raise(product_id)

        return self.product_mapper.map_to_schema(product_model)

    async def create_product(self, product: ProductCreate) -> Product:
        product_model = self.product_mapper.map_to_db_model(product)
        created_product = await self.products_repository.create(product_model)

        return self.product_mapper.map_to_schema(created_product)

    async def update_product(
        self,
        product_id: UUID,
        product: ProductPatch,
    ) -> Product:
        product_model = await self._get_product_or_raise(product_id)

        self.product_mapper.map_to_existing_model(product, product_model)

        updated_product = await self.products_repository.update(product_model)

        return self.product_mapper.map_to_schema(updated_product)


    async def soft_delete_product(self, product_id: UUID) -> ProductDelete:
        product_model = await self._get_product_or_raise(product_id)

        deleted_product = await self.products_repository.delete(product_model)

        return self.product_mapper.map_to_schema(deleted_product, ProductDelete)
