import builtins
import types
from typing import Any
from unittest.mock import patch
import pytest

from rpg_companion.i18n import i18n

_: Any

def test_q_translation_called():
    with patch("rpg_companion.i18n.i18n.QCoreApplication.translate") as mock_translate:
        mock_translate.return_value = "translated"
        result = i18n._q("MyContext", "Hello")
        mock_translate.assert_called_once_with("MyContext", "Hello")
        assert result == "translated"

def test_install_global_translation_module_context():
    i18n.install_global_translation()
    
    # Simuler un appel depuis un module
    def fake_module_call():
        return _("Hello")  # builtins._ a été installé
    
    with patch("rpg_companion.i18n.i18n._q") as mock_q:
        mock_q.side_effect = lambda context, text: f"{context}:{text}"
        result = fake_module_call()
        # Contexte = nom du "module" (ici le nom du test)
        assert result.endswith(":Hello")

def test_install_global_translation_class_context():
    i18n.install_global_translation()
    
    class Dummy:
        def method(self):
            return _("Hello")
    
    dummy = Dummy()
    with patch("rpg_companion.i18n.i18n._q") as mock_q:
        mock_q.side_effect = lambda context, text: f"{context}:{text}"
        result = dummy.method()
        # Contexte = nom de la classe
        assert result.startswith("Dummy:")
        assert result.endswith(":Hello")

def test_auto_with_frame_none(monkeypatch):
    """Test le cas où inspect.currentframe() retourne None"""
    i18n.install_global_translation()

    def fake_currentframe():
        return None

    monkeypatch.setattr("inspect.currentframe", fake_currentframe)

    assert _("Hello") == "Hello"  # doit retourner le texte brut

def test_auto_with_caller_none(monkeypatch):
    """Test le cas où frame.f_back est None"""
    i18n.install_global_translation()

    class Frame:
        f_back = None

    def fake_currentframe():
        return Frame()

    monkeypatch.setattr("inspect.currentframe", fake_currentframe)

    assert _("Hello") == "Hello"  # doit retourner le texte brut
    