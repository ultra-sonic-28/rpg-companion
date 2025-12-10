import pytest
from unittest.mock import Mock, patch
from rpg_companion.services.weapon_service import WeaponService

def test_roll_weapon_returns_expected_dict():
    # Création d'un fake weapon avec to_dict()
    fake_weapon = Mock()
    fake_weapon.to_dict.return_value = {"name": "Sword", "damage": 10}

    # Mock du repo pour renvoyer notre fake weapon
    mock_repo = Mock()
    mock_repo.get_by_roll.return_value = fake_weapon

    service = WeaponService(mock_repo)

    # Patch random.randint pour contrôler le roll
    with patch("rpg_companion.services.weapon_service.random.randint", return_value=42):
        result = service.roll_weapon()

    # Vérifie que le repo a été interrogé avec le bon roll
    mock_repo.get_by_roll.assert_called_once_with(42)

    # Vérifie le contenu du résultat
    assert result["name"] == "Sword"
    assert result["damage"] == 10
    assert result["roll"] == 42

def test_roll_weapon_raises_if_no_entry():
    # Repo renvoie None → doit lever ValueError
    mock_repo = Mock()
    mock_repo.get_by_roll.return_value = None
    service = WeaponService(mock_repo)

    with patch("rpg_companion.services.weapon_service.random.randint", return_value=99):
        with pytest.raises(ValueError) as exc:
            service.roll_weapon()
    
    # Vérifie le message d'erreur
    assert "99" in str(exc.value)
