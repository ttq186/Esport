from pydantic import Field

from src.product.schemas import Product
from src.schemas import ORJSONModel


class Cart(ORJSONModel):
    id: int | None


class ProductCartIn(ORJSONModel):
    id: int
    quantity: int = Field(gt=0)


class CartIn(Cart):
    products: list[ProductCartIn]


class CartOut(Cart):
    id: int
    user_id: int
    products: list[Product] | None = []


class CartUpdate(Cart):
    products: list[ProductCartIn]
