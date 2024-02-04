from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils.types.choice import ChoiceType

from .base import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


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
    user_id: Mapped[Integer] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"Order <{self.id}>"
