from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from calix.db import db


class Label(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    color: Mapped[str] = mapped_column(Text)
    """Hex code with alpha. #RRGGBBAA"""

    def __init__(
            self,
            name: str,
            color: str,
    ):
        self.name = name
        self.color = color

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
        }

