import pytest
from unittest.mock import patch
from PySide6.QtWebEngineWidgets import QWebEngineView

from rpg_companion.ui.views.result_webview import ResultWebView


class DummyResultWebView(ResultWebView):
    """Sous-classe concrète pour permettre l'instanciation."""
    def _format_result(self, result):
        return "<div>dummy</div>"

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

def test_css_light_is_used_and_covered_when_theme_is_light(qapp):
    view = DummyResultWebView(initial_theme="light")

    html = view._create_base_html("light")

    # Preuve que _css_light() a été exécutée
    assert "background: #fafafa" in html
    assert "color: #222" in html



def test_css_dark_is_used_and_covered_when_theme_is_dark(qapp):
    view = DummyResultWebView(initial_theme="dark")

    html = view._create_base_html("dark")

    # Preuve que _css_dark() a été exécutée
    assert "background: #1e1e1e" in html
    assert "color: #ddd" in html
