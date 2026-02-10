from datetime import datetime
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from calix.db import db
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

