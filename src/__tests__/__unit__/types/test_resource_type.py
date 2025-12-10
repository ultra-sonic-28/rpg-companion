import pytest
from rpg_companion.types.resource_type import ResourceType


def test_resource_type_enum_values():
    """Test pour vérifier que les valeurs de l'énumération sont correctes."""
    
    # Vérifie les valeurs des éléments de l'énumération
    assert ResourceType.ICON.value == "icon"
    assert ResourceType.IMAGE.value == "image"


def test_resource_type_enum_names():
    """Test pour vérifier les noms des éléments de l'énumération."""
    
    # Vérifie les noms des éléments de l'énumération
    assert ResourceType.ICON.name == "ICON"
    assert ResourceType.IMAGE.name == "IMAGE"


@pytest.mark.parametrize(
    "resource_type, expected_value, expected_name",
    [
        (ResourceType.ICON, "icon", "ICON"),
        (ResourceType.IMAGE, "image", "IMAGE")
    ]
)
def test_resource_type_enum_properties(resource_type, expected_value, expected_name):
    """Test paramétré pour vérifier les propriétés des éléments de l'énumération."""

    assert resource_type.value == expected_value
    assert resource_type.name == expected_name
