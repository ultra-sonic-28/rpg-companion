from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPalette, QColor

from rpg_companion.utils.theme_utils import get_system_theme


class ThemeManager(QObject):
    theme_changed = Signal(str)  # "light" ou "dark"

    def __init__(self, app, config):
        super().__init__()
        self.app = app
        self.config = config

        # mode défini dans config.toml : auto | light | dark
        self.user_mode = self.config.theme()["mode"].lower()

        # thème courant
        self.current = self._determine_effective_theme()

        # Appliquer le thème dès le démarrage
        self._apply_theme_to_qt(self.current)

        # Qt 6 → signal natif
        app.paletteChanged.connect(self._on_palette_changed)

    # ------------------------------------------------------------------
    # Déterminer le thème effectif = force ou auto
    # ------------------------------------------------------------------
    def _determine_effective_theme(self) -> str:
        mode = self.user_mode

        if mode == "light":
            return "light"
        if mode == "dark":
            return "dark"

        # sinon mode = auto → détecter OS
        return get_system_theme()

    # ------------------------------------------------------------------
    # Réagit aux changements du thème OS
    # ------------------------------------------------------------------
    def _on_palette_changed(self, palette):
        # On ne fait rien si l'utilisateur force light/dark
        if self.user_mode != "auto":
            return

        new_theme = self._detect_os_theme()
        if new_theme != self.current:
            self.current = new_theme
            self._apply_theme_to_qt(new_theme)
            self.theme_changed.emit(new_theme)

    # ------------------------------------------------------------------
    # Appelé si la config change (pas encore utile ici, mais dispo)
    # ------------------------------------------------------------------
    def reload_user_mode(self):
        self.user_mode = self.config.theme()["mode"].lower()
        new_theme = self._determine_effective_theme()

        if new_theme != self.current:
            self.current = new_theme
            self._apply_theme_to_qt(new_theme)
            self.theme_changed.emit(new_theme)

    # ------------------------------------------------------------------
    # Appliquer le thème Qt global
    # ------------------------------------------------------------------
    def _apply_theme_to_qt(self, theme):
        if theme == "dark":
            self.app.setPalette(self._dark_palette())
        else:
            self.app.setPalette(self.app.style().standardPalette())

    # ------------------------------------------------------------------
    # Palettes
    # ------------------------------------------------------------------
    def _dark_palette(self) -> QPalette:
        palette = QPalette()

        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(45, 45, 45))
        palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))

        palette.setColor(QPalette.Highlight, QColor(90, 150, 255))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        return palette
