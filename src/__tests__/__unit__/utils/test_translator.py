import pytest
import logging
from unittest.mock import patch, MagicMock

from rpg_companion.utils.translator import Translator


# --------------------------------------------------
#  Fixture : reset du singleton avant chaque test
# --------------------------------------------------
@pytest.fixture(autouse=True)
def reset_translator_singleton():
    Translator._instance = None
    yield
    Translator._instance = None


# --------------------------------------------------
#  Test : instance() renvoie bien un singleton
# --------------------------------------------------
def test_translator_singleton():
    t1 = Translator.instance()
    t2 = Translator.instance()
    assert t1 is t2


# --------------------------------------------------
#  Test : load_language ne recharge pas une langue déjà chargée
# --------------------------------------------------
def test_load_language_already_loaded():
    trad = Translator()
    trad.current_lang = "fr_FR"

    mock_translator = MagicMock()
    trad.translator = mock_translator

    trad.load_language("fr_FR")

    mock_translator.load.assert_not_called()


# --------------------------------------------------
#  Test : load_language — chargement réussi
# --------------------------------------------------
def test_load_language_success():
    trad = Translator()

    mock_translator = MagicMock()
    mock_translator.load.return_value = True
    trad.translator = mock_translator

    mock_app = MagicMock()
    with patch("rpg_companion.utils.translator.QApplication.instance", return_value=mock_app):
        with patch.object(trad.log, "info") as mock_info:

            trad.load_language("en_US")

            mock_translator.load.assert_called_once_with(":/i18n/en_US.qm")
            mock_app.installTranslator.assert_called_once_with(mock_translator)
            assert trad.current_lang == "en_US"
            mock_info.assert_called_once()


# --------------------------------------------------
#  Test : load_language — échec du chargement
# --------------------------------------------------
def test_load_language_failure():
    trad = Translator()

    mock_translator = MagicMock()
    mock_translator.load.return_value = False
    trad.translator = mock_translator

    with patch.object(trad.log, "error") as mock_error:
        trad.load_language("it_IT")

        mock_translator.load.assert_called_once_with(":/i18n/it_IT.qm")
        mock_error.assert_called_once()
        assert trad.current_lang is None   # pas modifié


# --------------------------------------------------
#  Test : reload_from_config utilise ConfigManager.general()
# --------------------------------------------------
def test_reload_from_config():
    trad = Translator()

    mock_config = MagicMock()
    mock_config.general.return_value = {"language": "de_DE"}
    trad.config = mock_config

    with patch.object(trad, "load_language") as mock_load:
        trad.reload_from_config()
        mock_load.assert_called_once_with("de_DE")
