from __future__ import annotations
import os
from pathlib import Path
from importlib.resources import files, as_file
import sys
from threading import Lock
import logging


class ResourceManager:
    """
    Gestionnaire centralisé de ressources :
    - Singleton
    - Cache interne (paths résolus)
    - Compatible PyInstaller
    - Accès simplifié (icônes, images, fichiers)
    """

    _instance = None
    _lock = Lock()

    PACKAGE = "rpg_companion.assets"

    def __init__(self):
        if ResourceManager._instance is not None:
            raise RuntimeError("ResourceManager est un singleton. Utilisez ResourceManager.instance().")

        self.log = logging.getLogger("rpg_companion")

        # Cache interne : clé = chemin relatif, valeur = Path absolu
        self._cache: dict[str, Path] = {}

        # Détection PyInstaller
        self._is_pyinstaller = getattr(sys, "_MEIPASS", None) is not None
        if self._is_pyinstaller:
            self._meipass = Path(sys._MEIPASS) / "rpg_companion" / "assets"
        else:
            self._meipass = None

    # ----------------------------------------------------------------------
    # Singleton
    # ----------------------------------------------------------------------
    @classmethod
    def instance(cls) -> "ResourceManager":
        """Retourne l'instance unique du ResourceManager."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = ResourceManager()
        return cls._instance

    # ----------------------------------------------------------------------
    # Résolution des chemins
    # ----------------------------------------------------------------------
    def _resolve(self, resource_path: str | Path) -> Path:
        """
        Retourne un Path utilisable, gérant :
        - PyInstaller (_MEIPASS)
        - importlib.resources
        - extraction PyInstaller
        - cache interne
        """
        resource_path = str(resource_path).replace("\\", "/")

        # --- Cache ---------------------------------------------------------
        if resource_path in self._cache:
            self.log.debug(f"Load resource `{resource_path}` from cache")
            return self._cache[resource_path]
        
        # --- PyInstaller ---------------------------------------------------
        if self._is_pyinstaller and self._meipass:
            resolved = (self._meipass / resource_path).resolve()
            self._cache[resource_path] = resolved
            self.log.debug(f"Load resource `{resource_path}` from: `{resolved}`")
            return resolved

        # --- Tentative via importlib (mode normal + PyInstaller hook) ------
        try:
            pkg = files(self.PACKAGE)
            for part in resource_path.split("/"):
                pkg = pkg.joinpath(part)

            # as_file -> nécessaire pour PyInstaller
            with as_file(pkg) as extracted:
                resolved = Path(extracted)
                self._cache[resource_path] = resolved
                self.log.debug(f"Load resource `{resource_path}` from: `{resolved}`")
                return resolved

        except Exception:
            pass  # fallback ci-dessous

        # --- Fallback absolu (rare, mode dev) ------------------------------
        base_dir = Path(os.path.dirname(__file__)).parent / "assets"
        resolved = (base_dir / resource_path).resolve()
        self._cache[resource_path] = resolved
        self.log.debug(f"Load resource `{resource_path}` from: `{resolved}`")
        return resolved

    # ----------------------------------------------------------------------
    # API publique
    # ----------------------------------------------------------------------
    def get_icon(self, name: str) -> Path:
        return self._resolve(f"icons/{name}")

    def get_image(self, name: str) -> Path:
        return self._resolve(f"images/{name}")

    def get(self, relative_path: str | Path) -> Path:
        return self._resolve(relative_path)
