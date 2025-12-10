# src/rpg_companion/services/weapon_service.py
import random
from rpg_companion.repos.weapon_repo import WeaponRepository

class WeaponService:
    def __init__(self, repo: WeaponRepository):
        self.repo = repo

    def roll_weapon(self) -> dict:
        roll = random.randint(1, 100)
        entry = self.repo.get_by_roll(roll)

        if not entry:
            raise ValueError(f"Aucun résultat pour le jet {roll} dans la table W")

        result = entry.to_dict()
        result["roll"] = roll
        return result
