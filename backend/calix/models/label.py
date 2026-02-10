from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from calix.db import db


class Label(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    color: Mapped[str] = mapped_column(Text)
    """Hex code with alpha. #RRGGBBAA"""
