from uuid import UUID

from src.exceptions.entity_not_found import EntityNotFoundError
from src.mappers.mappers import ProductDataMapper, ProductReviewDataMapper
from src.repositories.products import ProductsRepository
from src.schemas.pagination_params import ProductPaginationParams, ReviewPaginationParams

from src.schemas.products import (
    ProductCreate,
    ProductPatch,
    Product,
    ProductDelete
)
from src.models import Product as ProductModel


class ProductService:
    def __init__(self, products_repository: ProductsRepository, product_mapper: type[ProductDataMapper], product_review_mapper: type[ProductReviewDataMapper]):
        self.products_repository = products_repository
        self.product_mapper = product_mapper
        self.product_review_mapper = product_review_mapper

    async def _get_product_or_raise(self, product_id: UUID) -> ProductModel:
        product = await self.products_repository.get_by_id(product_id)
        if product is None:
            raise EntityNotFoundError(product_id)
        return product

    async def get_product_by_id(self, product_id: UUID) -> Product:
        product_model = await self._get_product_or_raise(product_id)

        return self.product_mapper.map_to_schema(product_model)

    async def get_products(self, product_pagination: ProductPaginationParams, review_pagination: ReviewPaginationParams) -> list[Product]:
        product_models = await self.products_repository.get_all(
            product_pagination.product_per_page,
            (product_pagination.product_page - 1) * product_pagination.product_per_page,
            review_pagination.review_per_page,
            (review_pagination.review_page - 1) * review_pagination.review_per_page
        )
        return self.product_mapper.map_to_schemas(product_models)

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

        if product.product_reviews:
            existing_review_ids = {
                review.id for review in product_model.product_reviews
            }

            for review in product.product_reviews:
                if review.id not in existing_review_ids:
                    raise EntityNotFoundError(review.id)

        self.product_mapper.map_to_existing_model(product, product_model)

        updated_product = await self.products_repository.update(
            product_model,
            product.product_reviews,
        )

        return self.product_mapper.map_to_schema(updated_product)

    async def soft_delete_product(self, product_id: UUID) -> ProductDelete:
        product_model = await self._get_product_or_raise(product_id)

        deleted_product = await self.products_repository.delete(product_model)

        return self.product_mapper.map_to_schema(deleted_product, ProductDelete)
