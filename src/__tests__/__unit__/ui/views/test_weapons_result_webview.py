import inspect
from typing import Any
from unittest.mock import patch
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


# Test de la méthode _format_result()
@pytest.fixture
def sample_result():
    # Un exemple de dictionnaire de résultat à passer à la méthode
    return {
        'roll': '1d20',
        'range': '10m',
        'name': 'Epée longue',
        'hands': 1,  # 1 main
        'type': 'Tranchant',
        'damage': '1d6+2',
        'value': '50 pièces d\'or',
        'fix_cost': '10 pièces d\'or',
        'description': 'Une épée à une main, très tranchante.',
    }

def test_format_result_html_structure(sample_result):
    # Création d'une instance de la classe à tester
    weapons_view = WeaponsResultWebView()

    result_html = weapons_view._format_result(sample_result)
    
    # Vérification de la structure du HTML retourné

    # Vérifier que la table a bien la classe "entry"
    assert '<table class="entry">' in result_html

    # Vérifier le nombre de lignes (tr) dans la table
    assert result_html.count('<tr>') == 9  # 9 lignes dans la table, une pour chaque propriété

    # Vérifier que la première cellule (label) est bien "Jet" et la deuxième (data) contient le bon résultat
    assert '<td class="label">Jet</td>' in result_html
    assert '<td class="data">1d20</td>' in result_html

    # Vérifier la présence des autres labels et data
    assert '<td class="label">Intervalle</td>' in result_html
    assert '<td class="data">10m</td>' in result_html
    assert '<td class="label">Nom</td>' in result_html
    assert '<td class="data">Epée longue</td>' in result_html
    assert '<td class="label">Main</td>' in result_html
    assert '<td class="data">ONE_HAND</td>' in result_html
    assert '<td class="label">Type</td>' in result_html
    assert '<td class="data">Tranchant</td>' in result_html
    assert '<td class="label">Dégâts</td>' in result_html
    assert '<td class="data">1d6+2</td>' in result_html
    assert '<td class="label">Valeur</td>' in result_html
    assert '<td class="data">50 pièces d\'or</td>' in result_html
    assert '<td class="label">Réparation</td>' in result_html
    assert '<td class="data">10 pièces d\'or</td>' in result_html
    assert '<td class="label">Description</td>' in result_html
    assert '<td class="data">Une épée à une main, très tranchante.</td>' in result_html

