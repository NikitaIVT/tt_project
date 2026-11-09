from src.models import Product
from src.repositories.base import BaseRepository


class ProductsRepository(BaseRepository):
    model = Product