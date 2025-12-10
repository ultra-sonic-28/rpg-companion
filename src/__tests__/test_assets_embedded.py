import sys
from pathlib import Path
import pytest

# Répertoire source des assets
SRC_ASSETS = Path(__file__).parent.parent / "rpg_companion" / "assets"

def get_assets_in_meipass():
    """
    Retourne le chemin des assets quand l'exécutable PyInstaller est lancé.
    Sinon retourne le répertoire source.
    """
    if getattr(sys, "_MEIPASS", None):
        # chemin temporaire PyInstaller
        return Path(sys._MEIPASS) / "assets"
    return SRC_ASSETS

def test_assets_embedded():
    assets_root = get_assets_in_meipass()
    assert assets_root.exists(), f"Le répertoire assets est introuvable dans {assets_root}"

    # Parcours récursif des fichiers dans le dépôt
    for src_file in SRC_ASSETS.rglob("*"):
        if src_file.is_file():
            # Chemin correspondant dans l'exécutable
            relative = src_file.relative_to(SRC_ASSETS)
            embedded_file = assets_root / relative
            assert embedded_file.exists(), f"Asset manquant dans l'exécutable: {relative}"
