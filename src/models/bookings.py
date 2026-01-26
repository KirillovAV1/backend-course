from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, func
from datetime import datetime

from src.database.db import Base

class BookingsORM(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime] = mapped_column(DateTime)
    date_to: Mapped[datetime] = mapped_column(DateTime)
    price: Mapped[int]

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to.date() - self.date_from.date()).days

    @total_cost.expression
    def total_cost(cls) -> int:
        return cls.price * func.date_part("day", cls.date_to - cls.date_from)