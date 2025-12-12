import pytest
from rpg_companion.models.armor import Armor
from rpg_companion.types.armour_slot_type import ArmorSlotType


@pytest.mark.parametrize(
    "roll_min, roll_max, expected_range, slot, type_, name, as_modifier, value, fix_cost",
    [
        # Cas classiques
        (1, 6, "1-6", ArmorSlotType.FEET, 2, "Leather Boots", 0, 67, 14),      # min < max
        (3, 3, "3",   ArmorSlotType.WAIST, 2, "Leather Girdle", 0, 70, 14),    # min == max

        # Variantes supplémentaires
        (17, 20, "17-20", ArmorSlotType.HANDS, 3, "Leather Gauntlets", 0, 73, 15),
        (33, 36, "33-36", ArmorSlotType.HEAD, 4, "Leather Cap", 0, 75, 15),
        (73, 74, "73-74", ArmorSlotType.TORSO, 1, "Mail Shirt", 2, 187, 38),

        # Type armure
        (2, 4, "2-4", ArmorSlotType.LEGS, 2, "Leather Tasset", 0, 68, 14),

        # Type bouclier
        (46, 48, "46-48", ArmorSlotType.OFF_HAND, 5, "Targe Shield", 1, 123, 27),
    ]
)
def test_armor_to_dict(
    roll_min, roll_max, expected_range, slot, type_, name, as_modifier, value, fix_cost
):
    """Test paramétré de Armor.to_dict() sur plusieurs cas variés."""

    armor = Armor(
        roll_min=roll_min,
        roll_max=roll_max,
        slot=slot,
        type=type_,
        name=name,
        as_modifier=as_modifier,
        value=value,
        fix_cost=fix_cost,
    )

    result = armor.to_dict()

    assert result["range"] == expected_range
    assert result["slot"] == slot
    assert result["type"] == type_
    assert result["name"] == name
    assert result["as_modifier"] == as_modifier
    assert result["value"] == value
    assert result["fix_cost"] == fix_cost
