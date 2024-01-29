from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .order import Order  # noqa: F401
    from .refresh_token import RefreshToken  # noqa: F401


class User(Base):
    username: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(25),
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[Text] = mapped_column(
        Text,
        nullable=False,
    )
    is_staff: Mapped[Boolean] = mapped_column(
        Boolean,
        default=False,
    )
    is_active: Mapped[Boolean] = mapped_column(
        Boolean,
        default=False,
    )

    orders = relationship('Order', back_populates='user')
    refresh_tokens = relationship('RefreshToken', back_populates='user')

    def __str__(self):
        return f"{__class__.__name__}(ID: <{self.id!r}>, Username: <{self.username!r}>, Mail: <{self.email}>)"

    def __repr__(self):
        return str(self)