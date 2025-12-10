# src/rpg_companion/models/weapon.py
from sqlalchemy import Column, Integer, String
from rpg_companion.db.base import Base

class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True)
    roll_min = Column(Integer, nullable=False)
    roll_max = Column(Integer, nullable=False)
    hands = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    damage = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    fix_cost = Column(Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "range": f"{self.roll_min}-{self.roll_max}" if self.roll_min != self.roll_max else str(self.roll_min),
            "name": self.name,
            "hands": self.hands,
            "type": self.type,
            "damage": self.damage,
            "value": self.value,
            "fix_cost": self.fix_cost,
        }
