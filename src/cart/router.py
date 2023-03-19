from fastapi import APIRouter, Depends, status

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.cart import service

from src.cart.schemas import CartOut, CartUpdate

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.get("/me", response_model=CartOut)
async def get_my_cart(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    return await service.get_my_cart(user_id=jwt_data.user_id)


@router.put("/me", response_model=CartOut)
async def update_my_cart(
    update_data: CartUpdate,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    return await service.update_my_cart(
        user_id=jwt_data.user_id, update_data=update_data
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_cart(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    await service.delete_cart_by_user_id(user_id=jwt_data.user_id)
