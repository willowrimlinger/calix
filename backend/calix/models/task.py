from calix.db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(Text)
    start: Mapped[datetime] = mapped_column()
    end: Mapped[datetime] = mapped_column()
    recurrence_id: Mapped[int] = mapped_column(ForeignKey("recurrence.id"))

    recurrence: Mapped[Recurrence] = relationship(lazy="joined", innerjoin=True)
