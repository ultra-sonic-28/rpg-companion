import pytest
from rpg_companion.models.weapon import Weapon


@pytest.mark.parametrize(
    "roll_min, roll_max, expected_range, hands, type_, name, damage, value, fix_cost",
    [
        # Cas classiques
        (1, 6, "1-6", 1, 2, "Sword", 5, 100, 20),      # min < max
        (3, 3, "3",   2, 1, "Hammer", 10, 150, 40),    # min == max

        # Variantes supplémentaires
        (0, 10, "0-10", 1, 3, "Dagger", 2, 20, 5),     # min = 0
        (5, 15, "5-15", 2, 4, "Longbow", 8, 200, 50),  # valeurs plus grandes
        (12, 12, "12", 1, 1, "Magic Wand", 20, 500, 100),  # cas min=max avec grosse valeur

        # Arme légère à une main
        (2, 4, "2-4", 1, 2, "Short Sword", 4, 80, 15),

        # Arme à deux mains
        (7, 12, "7-12", 2, 5, "War Axe", 12, 250, 60),
    ]
)
def test_weapon_to_dict(
    roll_min, roll_max, expected_range, hands, type_, name, damage, value, fix_cost
):
    """Test paramétré de Weapon.to_dict() sur plusieurs cas variés."""

    weapon = Weapon(
        roll_min=roll_min,
        roll_max=roll_max,
        hands=hands,
        type=type_,
        name=name,
        damage=damage,
        value=value,
        fix_cost=fix_cost,
    )

    result = weapon.to_dict()

    assert result["range"] == expected_range
    assert result["hands"] == hands
    assert result["type"] == type_
    assert result["name"] == name
    assert result["damage"] == damage
    assert result["value"] == value
    assert result["fix_cost"] == fix_cost
