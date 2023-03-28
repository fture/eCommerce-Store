from decimal import Decimal
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    customer_first_name = Column(String(255), nullable=False)
    customer_last_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phonenum = Column(String(30), nullable=True, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    bag_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bags.bag_id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )


class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    product_name = Column(String(255), nullable=False, unique=True)
    product_price = Column(
        Numeric(precision=12, scale=2, decimal_return_scale=2),
        nullable=False,
        default=Decimal("0.00"),
    )
    product_left = Column(Integer, nullable=False, default=0)


class Bag(Base):
    __tablename__ = "bags"
    bag_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    count = Column(Integer, nullable=False, default=1)
    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.product_id", ondelete="SET NULL")
    )
    customer = relationship("Customer", backref="bags", foreign_keys=[customer_id])
    product = relationship("Product", backref="bags")


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    bag_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bags.bag_id", ondelete="SET NULL"),
        nullable=True,
    )
    price = Column(
        Numeric(precision=12, scale=2, decimal_return_scale=2), nullable=False
    )
    bag = relationship("Bag", backref="orders")
