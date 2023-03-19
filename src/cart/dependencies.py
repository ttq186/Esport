from src.product import service
from src.product.exceptions import ProductNotFound
from src.product.schemas import Product


async def valid_product(product_id: int) -> Product:
    product = await service.get_product_by_id(product_id)
    if not product:
        raise ProductNotFound()
    return Product(**product._mapping)
