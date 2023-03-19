from databases.interfaces import Record
from sqlalchemy import and_, select

from src.database import database
from src.order.models import order_item_tb, order_tb
from src.order.schemas import Order, OrderIn, OrderItemOut, OrderItemProductOut
from src.product.models import product_tb


async def get_order_by_user_id_and_order_id(
    user_id: int, order_id: int
) -> Record | None:
    select_query = order_tb.select().where(
        and_(order_tb.c.id == order_id, order_tb.c.user_id == user_id)
    )
    return await database.fetch_one(select_query)


async def get_orders_by_user_id(user_id: int) -> list[dict]:
    select_query = (
        select(
            order_tb,
            order_item_tb,
            order_item_tb.c.id.label("order_item_id"),
            product_tb.c.name,
            product_tb.c.description,
            product_tb.c.tag,
            product_tb.c.image_url,
        )
        .select_from(order_tb)
        .join(order_item_tb)
        .join(product_tb)
        .where(order_tb.c.user_id == user_id)
    )
    results = await database.fetch_all(select_query)
    order_id_to_order = {}
    for result in results:
        order_id = result["id"]
        mapping = result._mapping

        order_item = OrderItemOut(**mapping)
        order_item.id = result["order_item_id"]
        order_item.product = OrderItemProductOut(**mapping)
        if order_id not in order_id_to_order:
            order = Order(**mapping)
            order_id_to_order[order_id] = {
                **order.dict(),
                "order_items": [order_item],
            }
        else:
            order_id_to_order[order_id]["order_items"].append(order_item)
    orders = list(order_id_to_order.values())
    for order in orders:
        order["total_price"] = sum(
            order_item.price * order_item.quantity
            for order_item in order["order_items"]
        )

    return list(order_id_to_order.values())


async def get_order_info(order: Order) -> dict:
    select_query = (
        select(
            order_item_tb,
            product_tb.c.name,
            product_tb.c.description,
            product_tb.c.tag,
            product_tb.c.image_url,
        )
        .select_from(order_item_tb)
        .join(product_tb)
        .where(order_item_tb.c.order_id == order.id)
    )
    results = await database.fetch_all(select_query)
    total_price = 0
    for result in results:
        total_price += result["price"] * result["quantity"]

    return {
        **order.dict(),
        "total_price": total_price,
        "order_items": [
            OrderItemOut(
                **result._mapping, product=OrderItemProductOut(**result._mapping)
            )
            for result in results
        ],
    }


async def create_order(user_id: int, order_data: OrderIn) -> Record:
    insert_query = (
        order_tb.insert()
        .values(
            {
                "user_id": user_id,
                "shipping_address": order_data.shipping_address,
                "city": order_data.city,
            }
        )
        .returning(order_tb)
    )
    order = await database.fetch_one(insert_query)

    insert_query = (
        order_item_tb.insert()
        .values(
            [
                {**order_item.dict(), "order_id": order["id"]}  # type: ignore
                for order_item in order_data.order_items
            ]
        )
        .returning(order_item_tb)
    )
    order_items = await database.fetch_all(insert_query)

    return {**order._mapping, "order_items": order_items}  # type: ignore


async def delete_order(user_id: int, order_id: int) -> None:
    delete_query = order_tb.delete().where(
        and_(order_tb.c.id == order_id, order_tb.c.user_id == user_id)
    )
    await database.execute(delete_query)
