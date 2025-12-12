import pytest
from unittest.mock import patch
from rpg_companion.types.armour_slot_type import ArmorSlotType


# Test pour vérifier que les valeurs de l'énumération sont correctes
def test_armour_slot_type_enum_values():
    """Test pour vérifier que les valeurs de l'énumération sont correctes."""
    assert ArmorSlotType.ARMS.value == "ARMS"
    assert ArmorSlotType.BACK.value == "BACK"
    assert ArmorSlotType.FEET.value == "FEET"
    assert ArmorSlotType.HANDS.value == "HANDS"
    assert ArmorSlotType.HEAD.value == "HEAD"
    assert ArmorSlotType.LEGS.value == "LEGS"
    assert ArmorSlotType.OFF_HAND.value == "OFF_HAND"
    assert ArmorSlotType.TORSO.value == "TORSO"
    assert ArmorSlotType.WAIST.value == "WAIST"


# Test pour vérifier que les noms de l'énumération sont corrects
def test_armour_slot_type_enum_names():
    """Test pour vérifier que les noms de l'énumération sont corrects."""
    assert ArmorSlotType.ARMS.name == "ARMS"
    assert ArmorSlotType.BACK.name == "BACK"
    assert ArmorSlotType.FEET.name == "FEET"
    assert ArmorSlotType.HANDS.name == "HANDS"
    assert ArmorSlotType.HEAD.name == "HEAD"
    assert ArmorSlotType.LEGS.name == "LEGS"
    assert ArmorSlotType.OFF_HAND.name == "OFF_HAND"
    assert ArmorSlotType.TORSO.name == "TORSO"
    assert ArmorSlotType.WAIST.name == "WAIST"


# Test paramétré pour vérifier la méthode label de ArmorSlotType
@pytest.mark.parametrize(
    "hands_type, expected_label",
    [
        (ArmorSlotType.ARMS, "ARMS"),
        (ArmorSlotType.BACK, "BACK"),
        (ArmorSlotType.FEET, "FEET"),
        (ArmorSlotType.HANDS, "HANDS"),
        (ArmorSlotType.HEAD, "HEAD"),
        (ArmorSlotType.LEGS, "LEGS"),
        (ArmorSlotType.OFF_HAND, "OFF_HAND"),
        (ArmorSlotType.TORSO, "TORSO"),
        (ArmorSlotType.WAIST, "WAIST"),
    ]
)

@patch("builtins._", side_effect=lambda x: x)  # Mock de `_` pour qu'il retourne simplement la valeur donnée
def test_armour_slot_type_label(mock_gettext, hands_type, expected_label):
    """Test pour vérifier la méthode label de ArmorSlotType avec un mock de _."""
    
    # Vérification de la méthode `label`
    assert hands_type.label == expected_label
