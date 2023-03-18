from fastapi import APIRouter, Depends, Response, status

from src.auth import jwt, service
from src.auth.dependencies import valid_user_create
from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import AccessTokenResponse, AuthUser, JWTData, UserResponse

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def register_user(
    auth_data: AuthUser = Depends(valid_user_create),
) -> UserResponse:
    user = await service.create_user(auth_data)
    return user  # type: ignore


@router.get("/users/me")
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> UserResponse:
    user = await service.get_user_by_id(jwt_data.user_id)
    return user  # type: ignore


@router.post("/users/tokens")
async def auth_user(auth_data: AuthUser, response: Response) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    access_token = jwt.create_access_token(user=user)
    return AccessTokenResponse(access_token=access_token)
