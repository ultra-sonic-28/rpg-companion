import pytest
from unittest.mock import Mock
from PySide6.QtCore import QObject

from rpg_companion.ui.bridge import Bridge

def test_bridge_stores_callback():
    """Le callback doit être stocké correctement."""
    mock_cb = Mock()
    bridge = Bridge(callback=mock_cb)
    assert bridge._callback == mock_cb
    assert isinstance(bridge, QObject)

def test_request_new_roll_calls_callback():
    """request_new_roll() doit appeler le callback Python."""
    mock_cb = Mock()
    bridge = Bridge(callback=mock_cb)

    bridge.request_new_roll()

    mock_cb.assert_called_once()

def test_request_new_roll_no_callback():
    """Si le callback n'est pas callable, la méthode ne doit rien faire."""
    bridge = Bridge(callback=None)
    # Ne doit pas lever d'exception
    bridge.request_new_roll()
