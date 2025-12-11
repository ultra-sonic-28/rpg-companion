import pytest
from unittest.mock import Mock, patch
from rpg_companion.services.armor_service import ArmorService

def test_roll_armor_returns_expected_dict():
    # Création d'un fake armor avec to_dict()
    fake_armor = Mock()
    fake_armor.to_dict.return_value = {"name": "Kite Shield", "as_modifier": 3}

    # Mock du repo pour renvoyer notre fake armor
    mock_repo = Mock()
    mock_repo.get_by_roll.return_value = fake_armor

    service = ArmorService(mock_repo)

    # Patch random.randint pour contrôler le roll
    with patch("rpg_companion.services.armor_service.random.randint", return_value=83):
        result = service.roll_armor()

    # Vérifie que le repo a été interrogé avec le bon roll
    mock_repo.get_by_roll.assert_called_once_with(83)

    # Vérifie le contenu du résultat
    assert result["name"] == "Kite Shield"
    assert result["as_modifier"] == 3
    assert result["roll"] == 83

def test_roll_armor_raises_if_no_entry():
    # Repo renvoie None → doit lever ValueError
    mock_repo = Mock()
    mock_repo.get_by_roll.return_value = None
    service = ArmorService(mock_repo)

    with patch("rpg_companion.services.armor_service.random.randint", return_value=99):
        with pytest.raises(ValueError) as exc:
            service.roll_armor()
    
    # Vérifie le message d'erreur
    assert "99" in str(exc.value)
