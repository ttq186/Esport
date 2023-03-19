from fastapi import APIRouter, Depends, status

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.order import service
from src.order.dependencies import valid_order
from src.order.schemas import Order, OrderIn, OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderOut)
async def create_order(
    order_data: OrderIn,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    return await service.create_order(user_id=jwt_data.user_id, order_data=order_data)


@router.get("", response_model=list[OrderOut])
async def get_orders(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    return await service.get_orders_by_user_id(user_id=jwt_data.user_id)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order: Order = Depends(valid_order)):
    return await service.get_order_info(order=order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    order: Order = Depends(valid_order),
):
    await service.delete_order(user_id=jwt_data.user_id, order_id=order.id)
