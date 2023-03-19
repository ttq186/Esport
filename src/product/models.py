from sqlalchemy import Column, DateTime, Identity, Integer, String, Table, func

from src.database import metadata

product_tb = Table(
    "product",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("tag", String),
    Column("price", Integer, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("image_url", String, nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)
