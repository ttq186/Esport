from src.exceptions import NotFound


class OrderNotFound(NotFound):
    DETAIL = "Order not found!"
