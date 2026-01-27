from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import String
from src.database.db import Base

class HotelsORM(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]

    rooms_data: Mapped[list["RoomsORM"]] = relationship(
        back_populates="hotel_data",
        lazy="selectin"
    )