import pytest
from PySide6.QtWebEngineWidgets import QWebEngineView

from rpg_companion.ui.views.armors_result_webview import ArmorResultWebView
from rpg_companion.ui.views.result_webview import ResultWebView



def test_armors_result_webview_inherits_resultwebview():
    """Test que ResultWebView hérite bien de QWebEngineView."""
    assert issubclass(ArmorResultWebView, ResultWebView)

