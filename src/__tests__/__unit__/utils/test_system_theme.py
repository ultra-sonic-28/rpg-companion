from platform import platform
import pytest
from unittest.mock import patch
import sys
from rpg_companion.utils.theme_utils import is_windows_dark_mode, is_macos_dark_mode, get_system_theme


# Tests pour is_windows_dark_mode()
def test_is_windows_dark_mode_dark():
    """Test que is_windows_dark_mode() retourne True quand le mode sombre est activé."""
    with patch("winreg.QueryValueEx", return_value=(0, None)):
        assert is_windows_dark_mode() is True


def test_is_windows_dark_mode_light():
    """Test que is_windows_dark_mode() retourne False quand le mode sombre est désactivé."""
    with patch("winreg.QueryValueEx", return_value=(1, None)):
        assert is_windows_dark_mode() is False


def test_is_windows_dark_mode_exception():
    """Test que is_windows_dark_mode() gère les exceptions correctement."""
    with patch("winreg.QueryValueEx", side_effect=Exception("Mocked exception")):
        assert is_windows_dark_mode() is False


# Tests pour is_macos_dark_mode()
def test_is_macos_dark_mode_dark():
    """Test que is_macos_dark_mode() retourne True quand le mode sombre est activé."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "dark\n"
        assert is_macos_dark_mode() is True


def test_is_macos_dark_mode_light():
    """Test que is_macos_dark_mode() retourne False quand le mode sombre est désactivé."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "light\n"
        assert is_macos_dark_mode() is False


def test_is_macos_dark_mode_exception():
    """Test que is_macos_dark_mode() gère les exceptions correctement."""
    with patch("subprocess.run", side_effect=Exception("Mocked exception")):
        assert is_macos_dark_mode() is False


# Tests pour get_system_theme()
@pytest.mark.parametrize("platform, dark_mode, expected", [
    ("win32", True, "dark"),
    ("win32", False, "light"),
    ("darwin", True, "dark"),
    ("darwin", False, "light"),
    ("linux", False, "light"),  # Cas par défaut pour Linux
])
@patch("rpg_companion.utils.theme_utils.is_windows_dark_mode")
@patch("rpg_companion.utils.theme_utils.is_macos_dark_mode")
@patch("sys.platform", side_effect=lambda: platform)
def test_get_system_theme(mock_platform, mock_is_macos, mock_is_windows, platform, dark_mode, expected):
    """Test que get_system_theme() retourne le bon thème en fonction du système d'exploitation."""
    sys.platform = platform  # On simule la plateforme

    if platform.startswith("win"):
        mock_is_windows.return_value = dark_mode
        result = get_system_theme()
        assert result == expected

    elif platform == "darwin":
        mock_is_macos.return_value = dark_mode
        result = get_system_theme()
        assert result == expected

    else:  # Linux ou autres
        result = get_system_theme()
        assert result == "light"  # Le cas par défaut pour les systèmes non pris en charge est "light"
