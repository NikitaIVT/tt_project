from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, with_loader_criteria

from src.models import Product as ProductModel, ProductReview as ProductReviewModel
from src.repositories.base import BaseRepository


class ProductsRepository(BaseRepository):
    model = ProductModel
    review_model = ProductReviewModel

    excluded_update_fields = {"id", "created_at", "updated_at", "is_deleted", "product_id"}


    async def get_by_id(self, uuid: UUID) -> ProductModel | None:
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.product_reviews),
                with_loader_criteria(self.review_model, self.review_model.is_deleted.is_not(True)),
            )
            .where(self.model.id == uuid)
        )
        res = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def update(
            self,
            data: ProductModel,
            product_reviews: list[ProductReviewModel] | None = None,
    ) -> ProductModel | None:
        updated_product = await super().update(data)

        if updated_product is None or not product_reviews:
            return updated_product

        updates = [
            {
                col.key: getattr(review, col.key)
                for col in self.review_model.__table__.columns
                if col.key not in self.excluded_update_fields
            } | {"id": review.id}
            for review in product_reviews
        ]

        stmt = (
            update(self.review_model)
            .where(
                self.review_model.product_id == data.id,
                self.review_model.is_deleted.is_not(True),
            )
            .execution_options(synchronize_session=False)
        )

        await self.session.execute(stmt, updates)
        await self.session.refresh(updated_product, ["product_reviews"])

        return updated_product

    async def delete(self, data: ProductModel) -> ProductModel:
        data.is_deleted = True
        for review in data.product_reviews:
            review.is_deleted = True
        await self.session.flush()
        return data
