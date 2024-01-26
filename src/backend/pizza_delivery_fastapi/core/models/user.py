import uuid

from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

if TYPE_CHECKING:
    from .order import Order  # noqa: F401


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class User(Base):
    id: Mapped[GUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    username: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(25),
        unique=True,
        nullable=False,
    )
    password: Mapped[Text] = mapped_column(
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

    def __repr__(self):
        return f'User: <{self.username}> Mail: <{self.email}>'
