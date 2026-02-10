from sqlalchemy.orm import Mapped, mapped_column
from calix.db import db
from enum import StrEnum, auto


class RecurrenceType(StrEnum):
    DOW = auto()
    """Every n day(s) of the week. Uses association table."""
    DOM = auto()
    """Every n date(s) of the month. Uses association table."""
    DAY = auto()
    """Every n days."""
    WEEK = auto()
    """Every n weeks."""
    MONTH = auto()
    """Every n months."""
    YEAR = auto()
    """Every n years."""


class Recurrence(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    n: Mapped[int] = mapped_column()
    """The n in \"Every n days\" or \"The nth week of every other year\"."""
    type: Mapped[RecurrenceType] = mapped_column()
    """The days in \"Every n days\"."""

