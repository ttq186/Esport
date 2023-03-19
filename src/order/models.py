from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Table,
    func,
)

from src.database import metadata

order_tb = Table(
    "order",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("shipping_address", String, nullable=False),
    Column("city", String),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
)

order_item_tb = Table(
    "order_item",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("order_id", ForeignKey("order.id", ondelete="CASCADE"), nullable=False),
    Column("product_id", ForeignKey("product.id", ondelete="CASCADE"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("price", Integer, nullable=False),
)
