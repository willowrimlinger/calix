from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from calix.db import db
from enum import StrEnum


class RecurrenceType(StrEnum):
    DOW = "dow"
    """Every n day(s) of the week. Uses association table."""
    DOM = "dom"
    """Every n date(s) of the month. Uses association table."""
    DAY = "day"
    """Every n days."""
    WEEK = "week"
    """Every n weeks."""
    MONTH = "month"
    """Every n months."""
    YEAR = "year"
    """Every n years."""

class Recurrence(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    n: Mapped[int] = mapped_column()
    """The n in \"Every n days\" or \"The nth week of every other year\"."""
    type: Mapped[RecurrenceType] = mapped_column()
    """The days in \"Every n days\"."""
    start_date: Mapped[date] = mapped_column()
    """The date the recurrence starts (may not correspond to the date of the first event)."""
    end_date: Mapped[date] = mapped_column()
    """The date the recurrence ends."""

    def __init__(
            self,
            n: int,
            type: RecurrenceType,
            start_date: date,
            end_date: date,
    ):
        self.n = n
        self.type = type
        self.start_date = start_date
        self.end_date = end_date
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)

    def to_dict(self):
        return {
            "id": self.id,
            "n": self.n,
            "type": self.type,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

