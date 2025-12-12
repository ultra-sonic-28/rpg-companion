import inspect
import pytest
from PySide6.QtWebEngineWidgets import QWebEngineView

from rpg_companion.types.armour_slot_type import ArmorSlotType
from rpg_companion.ui.views.armors_result_webview import ArmorResultWebView
from rpg_companion.ui.views.result_webview import ResultWebView


def test_armors_result_webview_inherits_resultwebview():
    """Test que ArmorResultWebView hérite bien de ResultWebView."""
    assert issubclass(ArmorResultWebView, ResultWebView)


def test_armor_result_webview_implements_format_result():
    """
    Vérifie que ArmorResultWebView implémente bien la méthode abstraite
    _format_result() définie dans ResultWebView.
    """

    # 1. La classe doit être instantiable (donc ne plus être abstraite)
    try:
        view = ArmorResultWebView()
    except TypeError as exc:
        pytest.fail(f"ArmorResultWebView ne devrait pas être abstraite : {exc}")

    # 2. Vérifie que la méthode existe bien dans la classe enfant
    assert hasattr(ArmorResultWebView, "_format_result"), \
        "La classe ArmorResultWebView doit définir _format_result()"

    # 3. Vérifie que la méthode est surchargée (définie dans la classe elle-même)
    method = ArmorResultWebView._format_result
    parent_method = ResultWebView._format_result

    assert method.__qualname__.split('.')[0] == "ArmorResultWebView", \
        "_format_result() doit être implémentée dans ArmorResultWebView et non héritée"

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
        'range': '17-20',
        'name': 'Leather Gauntlets',
        'slot': ArmorSlotType.HANDS.value,
        'type': 'A',
        'as_modifier': '0',
        'value': '73 pièces d\'or',
        'fix_cost': '15 pièces d\'or',
    }

def test_format_result_html_structure(sample_result):
    # Création d'une instance de la classe à tester
    armor_view = ArmorResultWebView()

    result_html = armor_view._format_result(sample_result)
    
    # Vérification de la structure du HTML retourné

    # Vérifier que la table a bien la classe "entry"
    assert '<table class="entry">' in result_html

    # Vérifier le nombre de lignes (tr) dans la table
    assert result_html.count('<tr>') == 8  # 8 lignes dans la table, une pour chaque propriété

    # Vérifier que la première cellule (label) est bien "Jet" et la deuxième (data) contient le bon résultat
    assert '<td class="label">Jet</td>' in result_html
    assert '<td class="data">1d100</td>' in result_html

    # Vérifier la présence des autres labels et data
    assert '<td class="label">Intervalle</td>' in result_html
    assert '<td class="data">17-20</td>' in result_html
    assert '<td class="label">Nom</td>' in result_html
    assert '<td class="data">Leather Gauntlets</td>' in result_html
    assert '<td class="label">Emplacement</td>' in result_html
    assert '<td class="data">HANDS</td>' in result_html
    assert '<td class="label">Type</td>' in result_html
    assert '<td class="data">A</td>' in result_html
    assert '<td class="label">Modificateur AS</td>' in result_html
    assert '<td class="data">0</td>' in result_html
    assert '<td class="label">Valeur</td>' in result_html
    assert '<td class="data">73 pièces d\'or</td>' in result_html
    assert '<td class="label">Réparation</td>' in result_html
    assert '<td class="data">15 pièces d\'or</td>' in result_html