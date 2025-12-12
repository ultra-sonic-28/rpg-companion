# src/rpg_companion/models/items.py
from sqlalchemy import Column, Integer, String
from rpg_companion.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    roll_min = Column(Integer, nullable=False)
    roll_max = Column(Integer, nullable=False)
    details = Column(String(200), nullable=False)
    value = Column(Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "range": f"{self.roll_min}-{self.roll_max}" if self.roll_min != self.roll_max else str(self.roll_min),
            "details": self.details,
            "value": self.value,
        }
