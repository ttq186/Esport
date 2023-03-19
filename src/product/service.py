from databases.interfaces import Record
from sqlalchemy import desc

from src.database import database
from src.product.models import product_tb
from src.product.schemas import ProductIn, ProductUpdate


async def create_product(product_data: ProductIn) -> Record | None:
    insert_query = (
        product_tb.insert()
        .values(**product_data.dict(exclude={"id"}))
        .returning(product_tb)
    )
    return await database.fetch_one(insert_query)


async def get_products(
    get_out_of_stocks: bool = False, ids: list[int] | None = None
) -> list[Record]:
    if get_out_of_stocks:
        select_query = product_tb.select().where(product_tb.c.quantity >= 0)
    else:
        select_query = product_tb.select().where(product_tb.c.quantity > 0)
    if ids:
        select_query = select_query.where(product_tb.c.id.in_(ids))
    select_query = select_query.order_by(desc(product_tb.c.created_at))
    return await database.fetch_all(select_query)


async def get_product_by_id(id: int) -> Record | None:
    select_query = product_tb.select().where(product_tb.c.id == id)
    return await database.fetch_one(select_query)


async def update_product(id: int, update_data: ProductUpdate) -> None:
    update_query = (
        product_tb.update()
        .where(product_tb.c.id == id)
        .values(update_data.dict(exclude_unset=True, exclude={"id"}))
    )
    await database.execute(update_query)


async def delete_product_by_id(id: int) -> None:
    delete_query = product_tb.delete().where(product_tb.c.id == id)
    await database.execute(delete_query)
