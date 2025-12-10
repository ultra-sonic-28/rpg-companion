import pytest
from unittest.mock import patch
from rpg_companion.types.weapon_hands_type import WeaponHandsType


# Test pour vérifier que les valeurs de l'énumération sont correctes
def test_weapon_hands_type_enum_values():
    """Test pour vérifier que les valeurs de l'énumération sont correctes."""
    assert WeaponHandsType.ONE_HAND.value == "ONE_HAND"
    assert WeaponHandsType.TWO_HANDS.value == "TWO_HANDS"


# Test pour vérifier que les noms de l'énumération sont corrects
def test_weapon_hands_type_enum_names():
    """Test pour vérifier que les noms de l'énumération sont corrects."""
    assert WeaponHandsType.ONE_HAND.name == "ONE_HAND"
    assert WeaponHandsType.TWO_HANDS.name == "TWO_HANDS"


# Test paramétré pour vérifier la méthode label de WeaponHandsType
@pytest.mark.parametrize(
    "hands_type, expected_label",
    [
        (WeaponHandsType.ONE_HAND, "ONE_HAND"),
        (WeaponHandsType.TWO_HANDS, "TWO_HANDS"),
    ]
)

@patch("builtins._", side_effect=lambda x: x)  # Mock de `_` pour qu'il retourne simplement la valeur donnée
def test_weapon_hands_type_label(mock_gettext, hands_type, expected_label):
    """Test pour vérifier la méthode label de WeaponHandsType avec un mock de _."""
    
    # Vérification de la méthode `label`
    assert hands_type.label == expected_label
