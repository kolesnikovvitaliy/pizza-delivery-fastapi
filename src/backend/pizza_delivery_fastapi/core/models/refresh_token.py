import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


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


class RefreshToken(Base):
    uuid: Mapped[GUID] = mapped_column(
        GUID(),
        default=lambda: str(uuid.uuid4()),
    )
    user_id: Mapped[Integer] = mapped_column(
        ForeignKey(
            'users.id',
            ondelete="CASCADE"
        ),
        nullable=False
    )
    refresh_token: Mapped[String] = mapped_column(
        String,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
    )

    user = relationship('User', back_populates='refresh_tokens')

    def __str__(self):
        return f"{__class__.__name__}(RefreshToken: <{self.refresh_token!r}>, expires_at: <{self.expires_at!r}>)"

    def __repr__(self):
        return str(self)
