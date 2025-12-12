# src/rpg_companion/services/item_service.py
import random
from rpg_companion.repos.item_repo import ItemRepository

class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def roll_item(self) -> dict:
        roll = random.randint(1, 100)
        entry = self.repo.get_by_roll(roll)

        if not entry:
            raise ValueError(f"Aucun résultat pour le jet {roll} dans la table I")

        result = entry.to_dict()
        result["roll"] = roll
        return result
