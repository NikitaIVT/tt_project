from src.models import Product as ProductModel
from src.repositories.base import BaseRepository


class ProductsRepository(BaseRepository):
    model = ProductModel
