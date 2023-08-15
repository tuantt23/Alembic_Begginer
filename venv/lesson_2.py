from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy import BIGINT,VARCHAR,ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
class Base(DeclarativeBase):
    pass
"""
CREATE TABLE users
(
    telegram_id   BIGINT PRIMARY KEY,
    full_name     VARCHAR(255) NOT NULL,
    username      VARCHAR(255),
    language_code VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT NOW(),
    referrer_id   BIGINT,
    FOREIGN KEY (referrer_id)
        REFERENCES users (telegram_id)
        ON DELETE SET NULL
);
"""
class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, onupdate=func.now(), server_default=func.now())

# class User(Base, TimestampMixin, TableNameMixin):
#     # __tablename__ = "users"
#     telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
#     full_name: Mapped[str] = mapped_column(VARCHAR(255))
#     username: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
#     language_code: Mapped[str] = mapped_column(VARCHAR(255))
#     referrer_id: Mapped[Optional[int]] = mapped_column(BIGINT,ForeignKey('users.telegram_id', ondelete='SET NULL'))

int_pk = Annotated[int,mapped_column(Integer,primary_key=True)]
user_fk = Annotated[int,mapped_column(BIGINT, ForeignKey("user.telegram_id",ondelete="SET NULL"))]
str_255 = Annotated[str,mapped_column(VARCHAR(255))]

class User(Base, TimestampMixin, TableNameMixin):
    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    full_name: Mapped[str_255]
    language_code: Mapped[str_255]
    username: Mapped[Optional[str_255]]
    referrer_id: Mapped[user_fk]
"""
CREATE TABLE products
(
    product_id   SETIAL PRIMARY KEY,
    title     VARCHAR(255) NOT NULL,
    description      TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
"""
class Product(Base,TimestampMixin,TableNameMixin):
    product_id: Mapped[int_pk] #= mapped_column(Integer,primary_key=True)
    title: Mapped[str_255]
    description: Mapped[Optional[str]]
"""
CREATE TABLE orders
(
    order_id   SETIAL PRIMARY KEY,
    user_id     VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
    FOREIGN KEY (user_id)
        REFERENCE users(telegram_id)
        ON DELETE CASCADE
);
"""
class Order(Base,TimestampMixin,TableNameMixin):
    order_id: Mapped(int_pk)
    user_id: Mapped(user_fk)

"""
CREATE TABLE order_products
(
    order_id   INTEGER NOT NULL,
    product_id     INTEGER NOT NULL,
    quantity    INTEGER NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCE orders(order_id)
        ON DELETE CASCADE
    FOREIGN KEY (product_id)
        REFERENCE products (product_id)
        ON DELETE RESTRICT
);
"""
class OrderProduct(Base,TableNameMixin):
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.order_id",ondelete="CASCADE"),primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.product_id",ondelete="RESTRICT"),primary_key=True)
    quatity: Mapped[int]