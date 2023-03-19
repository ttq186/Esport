from fastapi import APIRouter, Depends, status

from src.auth import schemas as auth_schemas
from src.auth.jwt import parse_jwt_user_data, validate_admin_access
from src.product import service
from src.product.dependencies import valid_product
from src.product.schemas import Product, ProductIn, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductOut)
async def create_product(
    product_in: ProductIn,
    _=Depends(validate_admin_access),
):
    product = await service.create_product(product_data=product_in)
    return product


@router.get("", response_model=list[ProductOut])
async def get_products(
    token: auth_schemas.JWTData = Depends(parse_jwt_user_data),
):
    return await service.get_products(get_out_of_stocks=token.is_admin)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    token: auth_schemas.JWTData = Depends(parse_jwt_user_data),
    product: Product = Depends(valid_product),
):
    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    update_data: ProductUpdate,
    _=Depends(validate_admin_access),
    product: Product = Depends(valid_product),
):
    await service.update_product(id=product_id, update_data=update_data)
    return {**product.dict(), **update_data.dict(exclude_unset=True), "id": product_id}


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    _=Depends(validate_admin_access),
    product: Product = Depends(valid_product),
):
    await service.delete_product_by_id(product_id)
