from src.exceptions import BadRequest


class CartAlreadyExists(BadRequest):
    DETAIL = "Your cart already exists!"
