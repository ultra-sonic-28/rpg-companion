import pytest
from PySide6.QtWebEngineWidgets import QWebEngineView

from rpg_companion.ui.views.result_webview import ResultWebView


def test_result_webview_inherits_qwebengineview():
    """Test que ResultWebView hérite bien de QWebEngineView."""
    assert issubclass(ResultWebView, QWebEngineView)


def test_format_result_raises_not_implemented_error():
    """
    Test que _format_result() lève bien NotImplementedError.
    Pour pouvoir tester, on crée une sous-classe minimale.
    """

    class Dummy(ResultWebView):
        pass  # ne surcharge pas _format_result()

    with pytest.raises(NotImplementedError):
        Dummy._format_result(None, {})
