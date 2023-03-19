from databases.interfaces import Record
from sqlalchemy import select

from src.cart.models import cart_item_tb, cart_tb
from src.cart.schemas import CartUpdate
from src.database import database
from src.product.models import product_tb


async def get_cart_by_user_id(user_id: int) -> Record | None:
    select_query = cart_tb.select().where(cart_tb.c.user_id == user_id)
    return await database.fetch_one(select_query)


async def get_cart_items(cart_id: int) -> list[Record]:
    select_query = (
        select(
            cart_item_tb.c.cart_id,
            cart_item_tb.c.quantity.label("cart_quantity"),
            product_tb.c.id.label("id"),
            product_tb.c.quantity,
            product_tb.c.name,
            product_tb.c.tag,
            product_tb.c.description,
            product_tb.c.price,
            product_tb.c.image_url,
        )
        .select_from(cart_item_tb)
        .join(product_tb)
        .where(cart_item_tb.c.cart_id == cart_id)
    )
    return await database.fetch_all(select_query)


async def get_or_create_cart_if_not_exist(user_id: int) -> Record:
    cart = await get_cart_by_user_id(user_id)
    if not cart:
        insert_query = cart_tb.insert().values({"user_id": user_id}).returning(cart_tb)
        cart = await database.fetch_one(insert_query)
    return cart  # type: ignore


async def get_my_cart(user_id: int) -> dict:
    cart = await get_or_create_cart_if_not_exist(user_id)
    cart_items = await get_cart_items(cart_id=cart["id"])
    return {**cart._mapping, "products": cart_items}


async def update_my_cart(user_id: int, update_data: CartUpdate) -> dict:
    # Delete the old cart_items
    cart = await get_or_create_cart_if_not_exist(user_id)
    await delete_cart_items_by_cart_id(cart_id=cart["id"])  # type: ignore

    # Save new cart_items
    insert_query = cart_item_tb.insert().values(
        [
            {
                "cart_id": cart["id"],  # type: ignore
                "product_id": product.id,
                "quantity": product.quantity,
            }
            for product in update_data.products
        ]
    )
    await database.execute(insert_query)

    # Refresh cart_items with products data
    cart_items = await get_cart_items(cart_id=cart["id"])
    return {**cart._mapping, "products": cart_items}


async def delete_cart_by_user_id(user_id: int) -> None:
    delete_query = cart_tb.delete().where(cart_tb.c.user_id == user_id)
    await database.execute(delete_query)


async def delete_cart_items_by_cart_id(cart_id: int) -> None:
    delete_query = cart_item_tb.delete().where(cart_item_tb.c.cart_id == cart_id)
    await database.execute(delete_query)
