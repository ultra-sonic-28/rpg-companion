import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

from rpg_companion.utils.resource_manager import ResourceManager


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset du singleton entre chaque test."""
    ResourceManager._instance = None
    yield
    ResourceManager._instance = None


# ----------------------------------------------------------------------
# Test singleton
# ----------------------------------------------------------------------
def test_resource_manager_singleton():
    rm1 = ResourceManager.instance()
    rm2 = ResourceManager.instance()
    assert rm1 is rm2


# ----------------------------------------------------------------------
# Test singleton -> Levée d'exception
# ----------------------------------------------------------------------
def test_singleton_enforces_single_instance():
    # On récupère l'instance unique
    rm1 = ResourceManager.instance()

    # Tenter de créer manuellement une nouvelle instance doit lever une erreur
    with pytest.raises(RuntimeError, match="ResourceManager est un singleton"):
        ResourceManager()


# ----------------------------------------------------------------------
# Mode PyInstaller (_MEIPASS actif)
# ----------------------------------------------------------------------
def test_resolve_pyinstaller_mode(tmp_path):
    fake_meipass_root = tmp_path / "bundle"
    fake_meipass_assets = fake_meipass_root / "rpg_companion" / "assets"
    fake_meipass_assets.mkdir(parents=True)

    # On injecte _MEIPASS dans sys via patch.dict
    with patch.dict(sys.__dict__, {"_MEIPASS": fake_meipass_root}):
        rm = ResourceManager.instance()

        # Vérification du mode PyInstaller
        assert rm._is_pyinstaller is True
        assert rm._meipass == fake_meipass_assets

        # Résolution d’un fichier
        result = rm.get("icons/test.png")
        assert result == fake_meipass_assets / "icons/test.png"


# ----------------------------------------------------------------------
# Test du cache interne
# ----------------------------------------------------------------------
def test_resource_cache(monkeypatch, tmp_path):
    rm = ResourceManager.instance()

    # Nettoyer le cache avant test
    rm._cache.clear()

    # On simule un fichier réel
    fake_file = tmp_path / "icons" / "a.png"
    fake_file.parent.mkdir(parents=True)
    fake_file.write_text("x")

    # Fake importlib.files
    class FakePkg:
        def __init__(self, path):
            self._path = path
        def joinpath(self, name):
            return FakePkg(self._path / name)

    monkeypatch.setattr(
        "rpg_companion.utils.resource_manager.files",
        lambda package: FakePkg(tmp_path)
    )

    # Fake as_file -> renvoie fake_file
    def simple_context_manager(value):
        class Ctx:
            def __enter__(self): return value
            def __exit__(self, *args): pass
        return Ctx()

    monkeypatch.setattr(
        "rpg_companion.utils.resource_manager.as_file",
        lambda pkg: simple_context_manager(fake_file)
    )

    # ---- Appels ----
    p1 = rm.get_icon("a.png")
    p2 = rm.get_icon("a.png")

    # Les chemins doivent être identiques
    assert p1 == fake_file
    assert p2 == fake_file

    # ---- Vérification du cache interne ----
    assert "icons/a.png" in rm._cache
    assert rm._cache["icons/a.png"] == fake_file

    # Le second appel doit retourner **exactement** l’objet du cache
    assert p2 is rm._cache["icons/a.png"]


# ----------------------------------------------------------------------
# Test importlib.resources (mode normal)
# ----------------------------------------------------------------------
def test_resolve_importlib():
    rm = ResourceManager.instance()

    fake_pkg = MagicMock()
    fake_pkg.joinpath.return_value = fake_pkg  # chaque joinpath renvoie le mock

    with patch("rpg_companion.utils.resource_manager.files", return_value=fake_pkg), \
         patch("rpg_companion.utils.resource_manager.as_file") as mock_as_file:

        mock_as_file.return_value.__enter__.return_value = Path("/tmp/extracted/file.png")

        result = rm.get("images/test.png")

        assert result == Path("/tmp/extracted/file.png")
        fake_pkg.joinpath.assert_any_call("images")
        fake_pkg.joinpath.assert_any_call("test.png")


# ----------------------------------------------------------------------
# Test fallback: importlib fail → assets locaux
# ----------------------------------------------------------------------
def test_resolve_fallback(tmp_path):
    rm = ResourceManager.instance()

    # On force _cache vide
    rm._cache.clear()

    # Simuler un crash d'importlib.resources
    with patch("rpg_companion.utils.resource_manager.files", side_effect=Exception):
        result = rm.get("images/test.png")

        import rpg_companion.utils.resource_manager as rm_module

        # Reproduit exactement le fallback du code
        expected_base = Path(os.path.dirname(rm_module.__file__)).parent / "assets"
        expected = (expected_base / "images/test.png").resolve()

        assert result == expected


# ----------------------------------------------------------------------
# Test API publique: get_icon, get_image, get
# ----------------------------------------------------------------------
def test_public_api_methods():
    rm = ResourceManager.instance()

    with patch.object(rm, "_resolve", return_value=Path("/tmp/path")) as mock_resolve:

        assert rm.get_icon("sword.png") == Path("/tmp/path")
        mock_resolve.assert_called_with("icons/sword.png")

        assert rm.get_image("orc.png") == Path("/tmp/path")
        mock_resolve.assert_called_with("images/orc.png")
