import pytest
from PySide6.QtWebEngineWidgets import QWebEngineView

from rpg_companion.ui.views.result_webview import ResultWebView
from rpg_companion.ui.views.weapons_result_webview import WeaponsResultWebView


def test_weapons_result_webview_inherits_resultwebview():
    """Test que WeaponsResultWebView hérite bien de ResultWebView."""
    assert issubclass(WeaponsResultWebView, ResultWebView)

