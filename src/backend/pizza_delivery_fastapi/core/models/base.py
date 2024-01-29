from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return ''.join(
            ['_' + ltr.lower()
             if ltr.isupper() else ltr
             for ltr in f"{cls.__name__}s"]
        ).lstrip('_')

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
        nullable=False,
    )
    update_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        default=datetime.utcnow,
    )
