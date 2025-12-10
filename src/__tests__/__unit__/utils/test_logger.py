import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from rpg_companion.utils.logger import setup_logging


class DummyConfig:
    """Classe factice pour simuler ConfigManager."""

    def __init__(self, enabled=True, level="INFO", file="./rpg-companion.log", mode="write"):
        self._logging = {
            "enabled": enabled,
            "level": level,
            "file": file,
            "mode": mode
        }

    def logging(self):
        return self._logging


@pytest.mark.parametrize(
    "enabled, level, mode",
    [
        (True, "INFO", "write"),
        (True, "DEBUG", "append"),
        (False, "INFO", "write"),
    ]
)
@patch("rpg_companion.utils.logger.Path.mkdir")
@patch("rpg_companion.utils.logger.logging.FileHandler")
@patch("rpg_companion.utils.logger.logging.StreamHandler")
@patch("rpg_companion.utils.logger.logging.basicConfig")
def test_setup_logging(mock_basicConfig, mock_stream, mock_fileHandler, mock_mkdir, enabled, level, mode):
    """Teste setup_logging() avec différents paramètres."""

    config = DummyConfig(enabled=enabled, level=level, mode=mode)

    # Appel de la fonction
    setup_logging(config)

    if not enabled:
        # Si logging désactivé, basicConfig ne doit pas être appelé
        mock_basicConfig.assert_not_called()
        assert logging.root.manager.disable == logging.CRITICAL
    else:
        # Sinon, vérifie que les handlers ont été créés et basicConfig appelé
        mock_mkdir.assert_called_once()
        assert mock_fileHandler.called
        assert mock_stream.called
        mock_basicConfig.assert_called_once()

        # Vérifie que le niveau est bien passé
        args, kwargs = mock_basicConfig.call_args
        expected_level = getattr(logging, level.upper(), logging.INFO)
        assert kwargs["level"] == expected_level

        # Vérifie que le mode du FileHandler correspond
        file_handler_args, file_handler_kwargs = mock_fileHandler.call_args
        expected_mode = "w" if mode == "write" else "a"
        assert file_handler_kwargs["mode"] == expected_mode
