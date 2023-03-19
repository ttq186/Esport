from pydantic import Field

from src.schemas import ORJSONModel


class OrderItem(ORJSONModel):
    id: int | None
    order_id: int | None
    product_id: int | None
    quantity: int | None
    price: int | None


class OrderItemIn(ORJSONModel):
    product_id: int
    quantity: int = Field(gt=0)
    price: int = Field(gt=0)


class OrderItemProductOut(ORJSONModel):
    name: str
    description: str | None
    tag: str | None
    image_url: str | None = Field(alias="image")


class OrderItemOut(OrderItem):
    product: OrderItemProductOut | None


class Order(ORJSONModel):
    id: int | None
    user_id: int | None
    shipping_address: str | None
    city: str | None


class OrderIn(Order):
    shipping_address: str
    city: str
    order_items: list[OrderItemIn] = Field(min_items=1)


class OrderOut(Order):
    id: int
    user_id: int
    shipping_address: str
    city: str
    total_price: int | None
    order_items: list[OrderItemOut]
