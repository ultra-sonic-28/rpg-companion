import os
import pytest
from pathlib import Path
from unittest.mock import mock_open, patch

from rpg_companion.config.config_manager import ConfigManager

@pytest.fixture
def tmp_config_file(tmp_path):
    """Fichier TOML temporaire."""
    file_path = tmp_path / "config.toml"
    return str(file_path)

def test_defaults_file_creation(tmp_config_file):
    """Si le fichier n'existe pas, il doit être créé avec les valeurs par défaut."""
    cfg = ConfigManager(filename=tmp_config_file)
    assert os.path.exists(tmp_config_file)
    assert cfg.window()["width"] == 1280
    assert cfg.logging()["enabled"] is True
    assert cfg.theme()["mode"] == "auto"
    assert cfg.general()["language"] == "en_US"

def test_save_and_load(tmp_config_file):
    """Test l'écriture et la lecture du fichier TOML."""
    cfg = ConfigManager(filename=tmp_config_file)
    cfg.window()["width"] = 1920
    cfg.save()

    cfg2 = ConfigManager(filename=tmp_config_file)
    assert cfg2.window()["width"] == 1920

def test_load_corrupted_file(tmp_config_file):
    """Si le fichier TOML est corrompu, il doit être réécrit avec les valeurs par défaut."""
    # Écrire du contenu corrompu
    with open(tmp_config_file, "w", encoding="utf-8") as f:
        f.write("<< this is not valid TOML >>")

    cfg = ConfigManager(filename=tmp_config_file)
    # Le fichier est réécrit avec les valeurs par défaut
    assert cfg.window()["width"] == 1280
    # Le contenu du fichier contient 'window' section
    with open(tmp_config_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "window" in content

def test_sections_access(tmp_config_file):
    cfg = ConfigManager(filename=tmp_config_file)
    assert isinstance(cfg.window(), dict)
    assert isinstance(cfg.logging(), dict)
    assert isinstance(cfg.theme(), dict)
    assert isinstance(cfg.general(), dict)

def test_deep_update_merges_dicts():
    base = {"a": 1, "b": {"x": 10, "y": 20}}
    updates = {"b": {"y": 30, "z": 40}, "c": 5}
    ConfigManager._deep_update(base, updates)
    assert base["a"] == 1
    assert base["b"]["x"] == 10
    assert base["b"]["y"] == 30
    assert base["b"]["z"] == 40
    assert base["c"] == 5
