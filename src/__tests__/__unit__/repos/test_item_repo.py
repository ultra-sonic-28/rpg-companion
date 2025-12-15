import pytest
from unittest.mock import Mock
from rpg_companion.repos.item_repo import ItemRepository
from rpg_companion.models.item import Item

def test_get_by_roll_returns_item():
    """Doit retourner un objet Item correspondant au roll."""
    # Création d'un faux Item
    item = Item()
    item.roll_min = 1
    item.roll_max = 10

    # Mock de la session et de la query
    mock_query = Mock()
    mock_query.filter.return_value.one_or_none.return_value = item
    mock_session = Mock()
    mock_session.query.return_value = mock_query

    repo = ItemRepository(mock_session)

    result = repo.get_by_roll(5)

    # Vérifie que la query a été construite correctement
    mock_session.query.assert_called_once_with(Item)
    mock_query.filter.assert_called_once()
    mock_query.filter.return_value.one_or_none.assert_called_once()

    # Vérifie que le résultat est celui attendu
    assert result == item

def test_get_by_roll_returns_none_if_not_found():
    """Doit retourner None si aucun Item ne correspond."""
    mock_query = Mock()
    mock_query.filter.return_value.one_or_none.return_value = None
    mock_session = Mock()
    mock_session.query.return_value = mock_query

    repo = ItemRepository(mock_session)

    result = repo.get_by_roll(99)

    assert result is None
