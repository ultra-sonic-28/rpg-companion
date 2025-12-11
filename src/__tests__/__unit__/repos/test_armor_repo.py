import pytest
from unittest.mock import Mock
from rpg_companion.repos.armor_repo import ArmorRepository
from rpg_companion.models.armor import Armor

def test_get_by_roll_returns_armor():
    """Doit retourner un objet Armor correspondant au roll."""
    # Création d'un faux Armor
    armor = Armor()
    armor.roll_min = 1
    armor.roll_max = 10

    # Mock de la session et de la query
    mock_query = Mock()
    mock_query.filter.return_value.one_or_none.return_value = armor
    mock_session = Mock()
    mock_session.query.return_value = mock_query

    repo = ArmorRepository(mock_session)

    result = repo.get_by_roll(5)

    # Vérifie que la query a été construite correctement
    mock_session.query.assert_called_once_with(Armor)
    mock_query.filter.assert_called_once()
    mock_query.filter.return_value.one_or_none.assert_called_once()

    # Vérifie que le résultat est celui attendu
    assert result == armor

def test_get_by_roll_returns_none_if_not_found():
    """Doit retourner None si aucun Armor ne correspond."""
    mock_query = Mock()
    mock_query.filter.return_value.one_or_none.return_value = None
    mock_session = Mock()
    mock_session.query.return_value = mock_query

    repo = ArmorRepository(mock_session)

    result = repo.get_by_roll(99)

    assert result is None
