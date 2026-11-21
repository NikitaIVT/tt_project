from src.mappers.base import DataMapper
from src.models import Product as ProductModel, ProductReview as ProductReviewModel
from src.schemas.product_review import ProductReview as ProductReviewSchema
from src.schemas.products import Product as ProductSchema


class ProductReviewDataMapper(DataMapper):
    db_model = ProductReviewModel
    schema = ProductReviewSchema


class ProductDataMapper(DataMapper):
    db_model = ProductModel
    schema = ProductSchema
    nested_mappers = {"product_reviews": ProductReviewDataMapper}
