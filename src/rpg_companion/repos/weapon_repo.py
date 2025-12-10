# src/rpg_companion/repos/weapon_repo.py
from sqlalchemy.orm import Session
from rpg_companion.models.weapon import Weapon
from typing import Optional

class WeaponRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_roll(self, roll: int) -> Optional[Weapon]:
        return (
            self._session.query(Weapon)
            .filter(Weapon.roll_min <= roll, Weapon.roll_max >= roll)
            .one_or_none()
        )
