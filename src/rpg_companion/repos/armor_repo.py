# src/rpg_companion/repos/armor_repo.py
from sqlalchemy.orm import Session
from rpg_companion.models.armor import Armor
from typing import Optional

class ArmorRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_roll(self, roll: int) -> Optional[Armor]:
        return (
            self._session.query(Armor)
            .filter(Armor.roll_min <= roll, Armor.roll_max >= roll)
            .one_or_none()
        )
