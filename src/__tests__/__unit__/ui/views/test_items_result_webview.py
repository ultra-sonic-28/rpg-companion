import inspect
import pytest
from PySide6.QtWebEngineWidgets import QWebEngineView

from rpg_companion.ui.views.items_result_webview import ItemResultWebView
from rpg_companion.ui.views.result_webview import ResultWebView


def test_items_result_webview_inherits_resultwebview():
    """Test que ItemResultWebView hérite bien de ResultWebView."""
    assert issubclass(ItemResultWebView, ResultWebView)


def test_items_result_webview_implements_format_result():
    """
    Vérifie que ItemResultWebView implémente bien la méthode abstraite
    _format_result() définie dans ResultWebView.
    """

    # 1. La classe doit être instantiable (donc ne plus être abstraite)
    try:
        view = ItemResultWebView()
    except TypeError as exc:
        pytest.fail(f"ItemResultWebView ne devrait pas être abstraite : {exc}")

    # 2. Vérifie que la méthode existe bien dans la classe enfant
    assert hasattr(ItemResultWebView, "_format_result"), \
        "La classe ItemResultWebView doit définir _format_result()"

    # 3. Vérifie que la méthode est surchargée (définie dans la classe elle-même)
    method = ItemResultWebView._format_result
    parent_method = ResultWebView._format_result

    assert method.__qualname__.split('.')[0] == "ItemResultWebView", \
        "_format_result() doit être implémentée dans ItemResultWebView et non héritée"

    # Facultatif : vérifier la signature
    sig_child = inspect.signature(method)
    sig_parent = inspect.signature(parent_method)
    assert sig_child == sig_parent, \
        "La signature de _format_result() doit correspondre à celle définie dans la classe abstraite"

# Test de la méthode _format_result()
@pytest.fixture
def sample_result():
    # Un exemple de dictionnaire de résultat à passer à la méthode
    return {
        'roll': '1d100',
        'range': '47-48',
        'details': 'Lantern Oil',
        'value': '48 pièces d\'or',
    }

def test_format_result_html_structure(sample_result):
    # Création d'une instance de la classe à tester
    items_view = ItemResultWebView()

    result_html = items_view._format_result(sample_result)
    
    # Vérification de la structure du HTML retourné

    # Vérifier que la table a bien la classe "entry"
    assert '<table class="entry">' in result_html

    # Vérifier le nombre de lignes (tr) dans la table
    assert result_html.count('<tr>') == 4  # 4 lignes dans la table, une pour chaque propriété

    # Vérifier que la première cellule (label) est bien "Jet" et la deuxième (data) contient le bon résultat
    assert '<td class="label">Jet</td>' in result_html
    assert '<td class="data">1d100</td>' in result_html

    # Vérifier la présence des autres labels et data
    assert '<td class="label">Intervalle</td>' in result_html
    assert '<td class="data">47-48</td>' in result_html
    assert '<td class="label">Détails</td>' in result_html
    assert '<td class="data">Lantern Oil' in result_html
    assert '<td class="label">Valeur</td>' in result_html
    assert '<td class="data">48 pièces d\'or</td>' in result_html
