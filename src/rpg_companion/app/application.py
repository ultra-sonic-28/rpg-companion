# app/application.py
import sys
import os
from pathlib import Path
import builtins

from PySide6.QtWidgets import QApplication, QStyleFactory, QSplashScreen
from PySide6.QtCore import Qt, QRect, QPoint, QEvent, QTimer
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile

from rpg_companion.utils.logger import setup_logging
from rpg_companion.config.config_manager import ConfigManager
from rpg_companion.ui.main_window import MainWindow
from rpg_companion.ui.theme_manager import ThemeManager
from rpg_companion.utils.resource_manager import ResourceManager
from rpg_companion.version.version import version_app
from rpg_companion.utils.translator import Translator

class Application(QApplication):
    """
    Classe centralisant la logique de l'application :
    - gestion de la configuration
    - restauration de la fenêtre
    - stockage de l'état à la fermeture
    """

    APP_NAME = "RPG Companion"

    def __init__(self):
        super().__init__(sys.argv)

        self.rm = ResourceManager.instance()

        # charge le fichier de configuration
        self.config = ConfigManager()

        setup_logging(self.config)

        import logging
        self.log = logging.getLogger("rpg_companion")
        self.log.info("Application starting...")
        self.log.info(f"{self.APP_NAME} v{version_app}")

        # --- Splash Screen ---
        splash_pix = QPixmap(str(self.rm.get_image("splash.png")))  # image dans assets/images
        self.splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        self.splash.setWindowFlag(Qt.FramelessWindowHint)
        self.splash.show()

        # Pour un meilleur rendu sur Windows / HiDPI
        self.setApplicationName(self.APP_NAME)
        self.setOrganizationName("4x4.Chris")
        self.setApplicationDisplayName(self.APP_NAME)

        # charge les traductions selon config
        self.translator = Translator.instance()
        self.translator.reload_from_config()

        theme_mode = self.config.theme()["mode"]

        self.setStyle(QStyleFactory.create("Fusion"))

        # Appliquer le mode sombre / clair dans toutes les WebViews
        self.theme_manager = ThemeManager(self, self.config)
        profile_settings = QWebEngineProfile.defaultProfile().settings()
        if theme_mode == "dark":
            profile_settings.setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, True)
        elif theme_mode == "light":
            profile_settings.setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, False)
        else:
            # auto → on laisse le style CSS gérer l'apparence selon l'OS / ThemeManager
            profile_settings.setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, False)

        app_icon = QIcon(str(self.rm.get_icon("icon.ico")))
        self.setWindowIcon(app_icon)

        # --- Création de la fenêtre principale après un petit délai ---
        QTimer.singleShot(1000, self._show_main_window)  # 1 sec de splash

        # connecte l'évènement de fermeture globale
        self.aboutToQuit.connect(self.on_app_quit)

    # ----------------------------------------
    # Création de la fenêtre principale
    # et fermeture de ls splash
    # ----------------------------------------
    def _show_main_window(self):
            """Créer et afficher la fenêtre principale, fermer le splash."""
            self.window = MainWindow(app=self)
            self.restore_window_state()
            self.window.show()

            if self.splash:
                self.splash.finish(self.window)
                self.splash = None

    # ----------------------------------------
    # Lors de la fermeture de l'application
    # ----------------------------------------
    def on_app_quit(self):
        self.log.info("Application closing…")
        self.save_window_state()

    # ----------------------------------------
    # Restaurer la fenêtre à partir de la config
    # ----------------------------------------
    def restore_window_state(self):
        wcfg = self.config.window()

        if wcfg["maximized"]:
            self.window.setWindowState(Qt.WindowMaximized)
        else:
            width = wcfg["width"]
            height = wcfg["height"]

            # Position connue ?
            if wcfg["x"] is not None and wcfg["y"] is not None:
                self.window.setGeometry(QRect(wcfg["x"], wcfg["y"], width, height))
            else:
                # Sinon on centre la fenêtre
                self.window.resize(width, height)
                screen = QApplication.primaryScreen()
                geo = screen.availableGeometry()

                x = (geo.width() - width) // 2
                y = (geo.height() - height) // 2
                self.window.move(QPoint(x, y))

    # -------------------------------------------------------------
    # Sauvegarde lors de la fermeture
    # -------------------------------------------------------------
    def save_window_state(self):

        wcfg = self.config.window()

        wcfg["maximized"] = self.window.isMaximized()

        if not self.window.isMaximized():
            geo = self.window.geometry()
            wcfg["x"] = geo.x()
            wcfg["y"] = geo.y()
            wcfg["width"] = geo.width()
            wcfg["height"] = geo.height()

        # Sauvegarde via tomlkit
        self.config.save()
