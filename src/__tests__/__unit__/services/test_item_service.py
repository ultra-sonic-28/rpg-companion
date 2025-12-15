import pytest
from unittest.mock import Mock, patch
from rpg_companion.services.item_service import ItemService

def test_roll_item_returns_expected_dict():
    # Création d'un fake item avec to_dict()
    fake_item = Mock()
    fake_item.to_dict.return_value = {"details": "Lantern Oil", "value": 45}

    # Mock du repo pour renvoyer notre fake item
    mock_repo = Mock()
    mock_repo.get_by_roll.return_value = fake_item

    service = ItemService(mock_repo)

    # Patch random.randint pour contrôler le roll
    with patch("rpg_companion.services.item_service.random.randint", return_value=48):
        result = service.roll_item()

    # Vérifie que le repo a été interrogé avec le bon roll
    mock_repo.get_by_roll.assert_called_once_with(48)

    # Vérifie le contenu du résultat
    assert result["details"] == "Lantern Oil"
    assert result["value"] == 45
    assert result["roll"] == 48

def test_roll_item_raises_if_no_entry():
    # Repo renvoie None → doit lever ValueError
    mock_repo = Mock()
    mock_repo.get_by_roll.return_value = None
    service = ItemService(mock_repo)

    with patch("rpg_companion.services.item_service.random.randint", return_value=99):
        with pytest.raises(ValueError) as exc:
            service.roll_item()
    
    # Vérifie le message d'erreur
    assert "99" in str(exc.value)
