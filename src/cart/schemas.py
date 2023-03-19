from pydantic import Field

from src.product.schemas import Product
from src.schemas import ORJSONModel


class Cart(ORJSONModel):
    id: int | None


class CartItemIn(ORJSONModel):
    id: int
    quantity: int = Field(
        gt=0,
    )


class CartIn(Cart):
    products: list[CartItemIn] = Field(min_items=1)


class CartProductOut(Product):
    cart_quantity: int


class CartOut(Cart):
    id: int
    user_id: int
    products: list[CartProductOut]


class CartUpdate(Cart):
    products: list[CartItemIn]
