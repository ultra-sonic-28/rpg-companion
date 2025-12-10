import os
import tomlkit

class ConfigManager:
    def __init__(self, filename="config.toml"):
        self.filename = filename

        # Valeurs par défaut
        self.data = tomlkit.table()
        self.data["window"] = {
            "x": 0,
            "y": 0,
            "width": 1280,
            "height": 720,
            "maximized": True,
        }

        self.data["logging"] = {
            "enabled": True,
            "level": "INFO",
            "file": "./rpg-companion.log",
            "mode": "write",
        }

        self.data["appearance"] = {
            "mode": "auto"  # light | dark | auto
        }

        self.data["general"] = {
            "language": "en_US"  # fr_FR | en_US
        }

        # Charge ou crée le fichier
        if os.path.exists(self.filename):
            self.load()
        else:
            self.save()  # ← crée le fichier TOML avec les valeurs par défaut

    def load(self) -> None:
        """Charge le fichier TOML si présent."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                file_data = tomlkit.parse(f.read())
            self._deep_update(self.data, file_data)
        except Exception:
            # Fichier corrompu → réécriture avec valeurs par défaut
            self.save()

    def save(self) -> None:
        """Écrit le TOML dans le fichier."""
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(tomlkit.dumps(self.data))

    def window(self) -> tomlkit.table:
        return self.data["window"]

    def theme(self) -> tomlkit.table:
        return self.data["appearance"]

    def logging(self) -> tomlkit.table:
        return self.data["logging"]

    def general(self) -> tomlkit.table:
        return self.data["general"]
    
    @staticmethod
    def _deep_update(base, updates):
        """Mise à jour récursive des tables TOML."""
        for key, value in updates.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                ConfigManager._deep_update(base[key], value)
            else:
                base[key] = value
