from pydantic import Field

from src.schemas import ORJSONModel


class Product(ORJSONModel):
    id: int | None
    name: str | None
    description: str | None
    tag: str | None
    price: int | None = Field(gt=0)
    quantity: int | None = Field(ge=0)
    image_url: str | None = Field(alias="image")


class ProductIn(Product):
    price: int = Field(gt=0)
    quantity: int = Field(gt=0)
    image_url: str = Field(alias="image")

    class Config:
        exclude = {"id"}


class ProductOut(Product):
    id: int


class ProductUpdate(Product):
    pass
