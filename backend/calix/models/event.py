from datetime import datetime
from sqlalchemy import ForeignKey, Text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from calix.db import db
from calix.error import CalixError
from calix.models.label import Label
from calix.models.recurrence import Recurrence


class Event(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(Text)
    start: Mapped[datetime] = mapped_column()
    end: Mapped[datetime] = mapped_column()
    recurrence_id: Mapped[int | None] = mapped_column(ForeignKey("recurrence.id"))
    label_id: Mapped[int] = mapped_column(ForeignKey("label.id"))

    recurrence: Mapped[Recurrence | None] = relationship(
        lazy="joined", cascade="all, delete-orphan"
    )
    label: Mapped[Label] = relationship(
        back_populates="events", lazy="joined", innerjoin=True
    )

    def __init__(
        self,
        start: datetime,
        end: datetime,
        description: str,
        location: str,
        recurrence: Recurrence | None,
        label: Label,
    ):
        if start > end:
            raise CalixError("Start time cannot be after end time")
        self.start = start
        self.end = end
        self.description = description
        self.location = location
        self.recurrence = recurrence
        self.label = label

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_range(cls, start: datetime, end: datetime):
        return db.session.scalars(
            select(cls).where(cls.start >= start).where(cls.end <= end)
        )

    @classmethod
    def get_by_id(cls, id: int):
        return db.session.scalar(select(cls).where(cls.id == id))

    def update(
        self,
        start: datetime,
        end: datetime,
        description: str,
        location: str,
        recurrence: Recurrence | None,
        label: Label,
    ):
        self.start = start
        self.end = end
        self.description = description
        self.location = location
        self.recurrence = recurrence
        self.label = label
        db.session.commit()

    def delete(self):
        return db.session.delete(self)

    def to_dict(self):
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "description": self.description,
            "location": self.location,
            "recurrence": self.recurrence.to_dict() if self.recurrence else None,
            "label": self.label.to_dict() if self.label else None,
        }
