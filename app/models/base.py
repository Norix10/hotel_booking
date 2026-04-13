import re
from datetime import datetime
from sqlalchemy import func

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


def camel_to_snake(name: str) -> str:
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return f"{snake}s"


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
