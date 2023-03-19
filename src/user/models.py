from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    LargeBinary,
    String,
    Table,
    func,
)

from src.database import metadata

user_tb = Table(
    "user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False, index=True),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("is_active", Boolean, server_default="true", nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

customer_tb = Table(
    "customer",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("first_name", String, nullable=False),
    Column("last_name", String),
    Column("address", String),
    Column("city", String),
    Column("phone_number", String, nullable=False),
)

admin_tb = Table(
    "admin",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("first_name", String, nullable=False),
    Column("last_name", String),
)
