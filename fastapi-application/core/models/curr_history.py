from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin


class CurrHistory(IntIdPkMixin,Base):

    __tablename__ = "curr_histories"

    USD: Mapped[float] = mapped_column()
    EUR: Mapped[float]
    JPY: Mapped[float]
    GBP: Mapped[float]
    AUD: Mapped[float]
    CAD: Mapped[float]
    CHF: Mapped[float]
    CNY: Mapped[float]
    SEK: Mapped[float]
    NZD: Mapped[float]
    BYN: Mapped[float]
    DATE: Mapped[datetime] = mapped_column(DateTime)
