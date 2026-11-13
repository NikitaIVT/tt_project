from src.repositories.mappers.base import DataMapper
from src.models import Product as ProductModel
from src.schemas.products import Product as ProductSchema



class ProductDataMapper(DataMapper):
    db_model = ProductModel
    schema = ProductSchema
