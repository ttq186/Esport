from sqlalchemy import Column, DateTime, ForeignKey, Identity, Integer, Table, func

from src.database import metadata

cart_tb = Table(
    "cart",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

cart_item_tb = Table(
    "cart_item",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("cart_id", ForeignKey("cart.id", ondelete="CASCADE"), nullable=False),
    Column("product_id", ForeignKey("product.id", ondelete="CASCADE"), nullable=False),
    Column("quantity", Integer, nullable=False),
)
