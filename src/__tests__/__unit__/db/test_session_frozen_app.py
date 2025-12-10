import sys
from pathlib import Path
from unittest.mock import patch
import importlib

import pytest

import rpg_companion.db.session as session_module

def test_base_dir_and_database_file_pyinstaller(tmp_path):
    """Test que BASE_DIR et DATABASE_FILE sont corrects quand sys.frozen est True (PyInstaller)."""

    fake_meipass = tmp_path / "meipass"
    fake_meipass.mkdir(parents=True)

    with patch.object(sys, "frozen", True, create=True), patch.object(sys, "_MEIPASS", fake_meipass, create=True):
        # Recharger le module pour recalculer BASE_DIR et DATABASE_FILE
        importlib.reload(session_module)

        expected_base_dir = fake_meipass / "rpg_companion" / "data"
        expected_database_file = expected_base_dir / "d100.sqlite3"

        assert session_module.BASE_DIR == expected_base_dir
        assert session_module.DATABASE_FILE == expected_database_file
        assert session_module.BASE_DIR.exists()
