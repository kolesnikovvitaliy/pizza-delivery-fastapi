from datetime import datetime
from sqlalchemy import String, func, Integer
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(String(50))

    # role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role_id: Mapped[int] = mapped_column(Integer)

    registered_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
        nullable=False,
    )
