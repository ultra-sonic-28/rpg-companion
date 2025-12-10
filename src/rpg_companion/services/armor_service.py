# src/rpg_companion/services/armor_service.py
import random
from rpg_companion.repos.armor_repo import ArmorRepository

class ArmorService:
    def __init__(self, repo: ArmorRepository):
        self.repo = repo

    def roll_armor(self) -> dict:
        roll = random.randint(1, 100)
        entry = self.repo.get_by_roll(roll)

        if not entry:
            raise ValueError(f"Aucun résultat pour le jet {roll} dans la table A")

        result = entry.to_dict()
        result["roll"] = roll
        return result
