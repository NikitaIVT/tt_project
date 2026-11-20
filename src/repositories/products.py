from uuid import UUID

from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload, with_loader_criteria, contains_eager, aliased

from src.models import Product as ProductModel, ProductReview as ProductReviewModel
from src.repositories.base import BaseRepository


class ProductsRepository(BaseRepository):
    model = ProductModel
    review_model = ProductReviewModel

    excluded_update_fields = {"id", "created_at", "updated_at", "is_deleted", "product_id"}

    async def get_all(
            self,
            product_limit: int,
            product_offset: int,
            review_limit: int,
            review_offset: int,
    ) -> list[ProductModel]:
        products_cte = (
            select(self.model)
            .where(self.model.is_deleted.is_not(True))
            .order_by(self.model.created_at, self.model.id)
            .limit(product_limit)
            .offset(product_offset)
            .cte("products")
        )

        products = aliased(self.model, products_cte)

        reviews_cte = (
            select(
                self.review_model,
                func.row_number()
                .over(
                    partition_by=self.review_model.product_id,
                    order_by=(self.review_model.created_at, self.review_model.id),
                )
                .label("r_rn"),
            )
            .where(
                self.review_model.product_id.in_(
                    select(products.id)
                ),
                self.review_model.is_deleted.is_not(True),
            )
            .cte("reviews")
        )

        chosen_reviews_cte = (
            select(reviews_cte)
            .where(
                reviews_cte.c.r_rn > review_offset,
                reviews_cte.c.r_rn <= review_offset + review_limit,
            )
            .cte("chosen_reviews")
        )

        chosen_reviews = aliased(self.review_model, chosen_reviews_cte)

        stmt = (
            select(products)
            .outerjoin(
                chosen_reviews,
                chosen_reviews.product_id == products.id,
            )
            .options(
                contains_eager(
                    products.product_reviews,
                    alias=chosen_reviews,
                )
            )
            .order_by(
                products.created_at,
                products.id,
                chosen_reviews.created_at,
                chosen_reviews.id,
            )
        )

        res = await self.session.execute(stmt)
        return res.unique().scalars().all()

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
