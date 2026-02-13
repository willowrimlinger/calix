import re
from typing import TYPE_CHECKING

from calix.error import CalixError

if TYPE_CHECKING:
    from calix.models.event import Event
from sqlalchemy import Text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from calix.db import db


def is_valid_hex_alpha(text: str):
    re.search(
        "^#?[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]$",
        text,
    )


class Label(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    color: Mapped[str] = mapped_column(Text)
    """Hex code with alpha. #RRGGBBAA"""

    events: Mapped[list[Event]] = relationship(back_populates="label")

    def __init__(
        self,
        name: str,
        color: str,
    ):
        if not is_valid_hex_alpha(color):
            raise CalixError(f"{color} is not a valid hex with alpha color (#RRGGBBAA)")
        self.name = name
        self.color = color

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return db.session.scalars(select(cls))

    @classmethod
    def get_by_id(cls, id: int):
        return db.session.scalar(select(cls).where(cls.id == id))

    def update(self, name: str, color: str):
        self.name = name
        self.color = color
        db.session.commit()

    def delete(self):
        db.session.delete(self)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
        }
