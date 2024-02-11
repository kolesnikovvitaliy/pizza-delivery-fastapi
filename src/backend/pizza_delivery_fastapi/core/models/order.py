from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils.types.choice import ChoiceType


from .base import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .product import Product  # noqa: F401
    from .order_product_association import OrderProductAssociation  # noqa: F401


class Order(Base):
    ORDER_STATUSES = (
        ("PENDING", "pending"),
        ("IN_TRANSIT", "in-transit"),
        ("DELIVERED", "delivered"),
    )
    PIZZA_SIZES = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large"),
        ("EXTRA-LARGE", "extra-large"),
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    order_status: Mapped[str] = mapped_column(
        ChoiceType(choices=ORDER_STATUSES), default="PENDING"
    )
    pizza_size: Mapped[str] = mapped_column(
        ChoiceType(choices=PIZZA_SIZES), default="SMALL"
    )
    pizza_name: Mapped[str] = mapped_column(String, nullable=False)
    promo_code: Mapped[str | None]

    # products: Mapped[list["Product"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="orders",
    # )
    # association between Parent -> Association -> Child
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order",
    )

    user_id: Mapped[Integer] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    user = relationship(argument="User", back_populates="orders")

    def __repr__(self):
        return f"Order <{self.id}>"
