import pytest
from unittest.mock import Mock
from rpg_companion.repos.weapon_repo import WeaponRepository
from rpg_companion.models.weapon import Weapon

def test_get_by_roll_returns_weapon():
    """Doit retourner un objet Weapon correspondant au roll."""
    # Création d'un faux Weapon
    weapon = Weapon()
    weapon.roll_min = 1
    weapon.roll_max = 10

    # Mock de la session et de la query
    mock_query = Mock()
    mock_query.filter.return_value.one_or_none.return_value = weapon
    mock_session = Mock()
    mock_session.query.return_value = mock_query

    repo = WeaponRepository(mock_session)

    result = repo.get_by_roll(5)

    # Vérifie que la query a été construite correctement
    mock_session.query.assert_called_once_with(Weapon)
    mock_query.filter.assert_called_once()
    mock_query.filter.return_value.one_or_none.assert_called_once()

    # Vérifie que le résultat est celui attendu
    assert result == weapon

def test_get_by_roll_returns_none_if_not_found():
    """Doit retourner None si aucun Weapon ne correspond."""
    mock_query = Mock()
    mock_query.filter.return_value.one_or_none.return_value = None
    mock_session = Mock()
    mock_session.query.return_value = mock_query

    repo = WeaponRepository(mock_session)

    result = repo.get_by_roll(99)

    assert result is None
