from src.auth import service
from src.auth.exceptions import EmailTaken
from src.auth.schemas import AuthUser


async def valid_user_create(user: AuthUser) -> AuthUser:
    if await service.get_user_by_email(user.email):
        raise EmailTaken()
    return user
