# src/rpg_companion/repos/item_repo.py
from sqlalchemy.orm import Session
from rpg_companion.models.item import Item
from typing import Optional

class ItemRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_roll(self, roll: int) -> Optional[Item]:
        return (
            self._session.query(Item)
            .filter(Item.roll_min <= roll, Item.roll_max >= roll)
            .one_or_none()
        )
