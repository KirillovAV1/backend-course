from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.database.db import Base


class RoomsORM(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities_data: Mapped[list["FacilitiesORM"]] = relationship(
        back_populates="rooms_data",
        secondary="rooms_facilities",
        lazy="selectin"
    )

    hotel_data: Mapped["HotelsORM"] = relationship(
        back_populates="rooms_data",
        lazy="selectin"
    )
    bookings_data: Mapped[list["BookingsORM"]] = relationship(
        back_populates="room_data",
        lazy="selectin"
    )
