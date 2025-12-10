import pytest
from unittest.mock import MagicMock, patch
from rpg_companion.db.session import get_session

# ------------------------------------------------------------------
# Test que la session est commitée après usage normal
# ------------------------------------------------------------------
def test_get_session_commit():
    mock_session = MagicMock()
    with patch("rpg_companion.db.session.Session", return_value=mock_session):
        with get_session() as session:
            # On doit récupérer la session mockée
            assert session == mock_session

        # Vérifie que commit a été appelé
        mock_session.commit.assert_called_once()
        # Rollback ne doit pas être appelé
        mock_session.rollback.assert_not_called()
        # Close doit toujours être appelé
        mock_session.close.assert_called_once()


# ------------------------------------------------------------------
# Test que la session fait rollback en cas d'exception
# ------------------------------------------------------------------
def test_get_session_rollback_on_exception():
    mock_session = MagicMock()
    with patch("rpg_companion.db.session.Session", return_value=mock_session):
        with pytest.raises(ValueError, match="force exception"):
            with get_session() as session:
                assert session == mock_session
                # On déclenche une exception pour tester rollback
                raise ValueError("force exception")

        # Commit ne doit pas être appelé
        mock_session.commit.assert_not_called()
        # Rollback doit être appelé
        mock_session.rollback.assert_called_once()
        # Close doit toujours être appelé
        mock_session.close.assert_called_once()


# ------------------------------------------------------------------
# Test que Session est bien créé via scoped_session
# ------------------------------------------------------------------
def test_get_session_returns_session_instance():
    mock_session = MagicMock()
    with patch("rpg_companion.db.session.Session", return_value=mock_session):
        with get_session() as session:
            # Vérifie que la session retournée est celle du scoped_session
            assert session == mock_session
