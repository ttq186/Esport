from fastapi import Depends

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.order import service
from src.order.exceptions import OrderNotFound
from src.order.schemas import Order


async def valid_order(
    order_id: int, jwt_data: JWTData = Depends(parse_jwt_user_data)
) -> Order:
    order = await service.get_order_by_user_id_and_order_id(
        user_id=jwt_data.user_id, order_id=order_id
    )
    if not order:
        raise OrderNotFound()
    return Order(**order._mapping)
