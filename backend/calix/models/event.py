from datetime import datetime
from sqlalchemy import ForeignKey, Text
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

    recurrence: Mapped[Recurrence | None] = relationship(lazy="joined")
    label: Mapped[Label] = relationship(lazy="joined", innerjoin=True)

    def __init__(
            self,
            start: datetime,
            end: datetime,
            description: str,
            location: str,
            recurrence: Recurrence,
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

