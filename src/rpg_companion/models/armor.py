# src/rpg_companion/models/armor.py
from sqlalchemy import Column, Integer, String
from rpg_companion.db.base import Base

class Armor(Base):
    __tablename__ = "armours"

    id = Column(Integer, primary_key=True)
    roll_min = Column(Integer, nullable=False)
    roll_max = Column(Integer, nullable=False)
    slot = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    as_modifier = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    fix_cost = Column(Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "range": f"{self.roll_min}-{self.roll_max}" if self.roll_min != self.roll_max else str(self.roll_min),
            "name": self.name,
            "slot": self.slot,
            "type": self.type,
            "as_modifier": self.as_modifier,
            "value": self.value,
            "fix_cost": self.fix_cost,
        }
