from enum import StrEnum, auto

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from calix.db import db


class DayOfMonth(StrEnum):
    MON = auto()
    TUE = auto()
    WED = auto()
    THU = auto()
    FRI = auto()
    SAT = auto()
    SUN = auto()


class RecurrenceToDOM(db.Model):
    day_of_week: Mapped[DayOfMonth] = mapped_column(primary_key=True)
    recurrence_id: Mapped[int] = mapped_column(ForeignKey("recurrence.id"), primary_key=True)
