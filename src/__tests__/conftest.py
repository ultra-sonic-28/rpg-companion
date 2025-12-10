import pytest
from rpg_companion.i18n.i18n import install_global_translation

import tracemalloc
tracemalloc.start()

# Fixture globale pour installer la traduction avant chaque test
@pytest.fixture(autouse=True)
def setup_translation():
    """Installe la traduction globale avant chaque test"""
    install_global_translation()
