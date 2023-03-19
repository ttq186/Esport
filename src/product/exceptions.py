from src.exceptions import NotFound


class ProductNotFound(NotFound):
    DETAIL = "Product not found!"
