import inspect
import pytest
from PySide6.QtWebEngineWidgets import QWebEngineView

from rpg_companion.ui.views.result_webview import ResultWebView
from rpg_companion.ui.views.weapons_result_webview import WeaponsResultWebView


def test_weapons_result_webview_inherits_resultwebview():
    """Test que WeaponsResultWebView hérite bien de ResultWebView."""
    assert issubclass(WeaponsResultWebView, ResultWebView)


def test_weapons_result_webview_implements_format_result():
    """
    Vérifie que WeaponsResultWebView implémente bien la méthode abstraite
    _format_result() définie dans ResultWebView.
    """

    # 1. La classe doit être instantiable (donc ne plus être abstraite)
    try:
        view = WeaponsResultWebView()
    except TypeError as exc:
        pytest.fail(f"WeaponsResultWebView ne devrait pas être abstraite : {exc}")

    # 2. Vérifie que la méthode existe bien dans la classe enfant
    assert hasattr(WeaponsResultWebView, "_format_result"), \
        "La classe WeaponsResultWebView doit définir _format_result()"

    # 3. Vérifie que la méthode est surchargée (définie dans la classe elle-même)
    method = WeaponsResultWebView._format_result
    parent_method = ResultWebView._format_result

    assert method.__qualname__.split('.')[0] == "WeaponsResultWebView", \
        "_format_result() doit être implémentée dans WeaponsResultWebView et non héritée"

    # Facultatif : vérifier la signature
    sig_child = inspect.signature(method)
    sig_parent = inspect.signature(parent_method)
    assert sig_child == sig_parent, \
        "La signature de _format_result() doit correspondre à celle définie dans la classe abstraite"
