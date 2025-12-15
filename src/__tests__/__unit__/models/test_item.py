import pytest
from rpg_companion.models.item import Item


@pytest.mark.parametrize(
    "roll_min, roll_max, expected_range, details, value",
    [
        # Cas classiques
        (1, 2, "1-2", "Pestle and Mortar", 2),      # min < max
        (97, 97, "97", "Skeleton Key", 300),    # min == max

        # Variantes supplémentaires
        (47, 48, "47-48", "Lantern Oil", 45),
        (79, 80, "79-80", "Silver Crucifix", 88),
        (99, 100, "99-100", "Treasure", 0),
    ]
)
def test_item_to_dict(
    roll_min, roll_max, expected_range, details, value
):
    """Test paramétré de Item.to_dict() sur plusieurs cas variés."""

    item = Item(
        roll_min=roll_min,
        roll_max=roll_max,
        details=details,
        value=value,
    )

    result = item.to_dict()

    assert result["range"] == expected_range
    assert result["details"] == details
    assert result["value"] == value
