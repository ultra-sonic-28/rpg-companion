from datetime import datetime
from typing import Any

from PySide6.QtWidgets import (
    QMainWindow,  QTabWidget, QMessageBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QThreadPool, QCoreApplication
from PySide6.QtGui import QAction, QIcon

from rpg_companion.db.session import Session
from rpg_companion.types.resource_type import ResourceType
from rpg_companion.ui.resource_browser import ResourceBrowser
from rpg_companion.ui.views.armors_result_webview import ArmorResultWebView
from rpg_companion.ui.views.items_result_webview import ItemResultWebView
from rpg_companion.ui.views.weapons_result_webview import WeaponsResultWebView
from rpg_companion.ui.widgets.status_bar import StatusBar
from rpg_companion.utils.qthreads import DBWorker
from rpg_companion.ui.bridge import Bridge
from rpg_companion.utils.resource_manager import ResourceManager
from rpg_companion.ui.widgets.dice_overlay import DiceOverlay
from rpg_companion.ui.dialogs.about_dialog import AboutDialog
from rpg_companion.build_info import BUILD_DATE
from rpg_companion.version.version import version_app

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)

        import logging
        self.log = logging.getLogger("rpg_companion")

        self.app = app
        self.app.theme_manager.theme_changed.connect(self._on_theme_changed)

        self.rm = ResourceManager.instance()

        self.setWindowTitle("RPG Companion")

        self._threadpool = QThreadPool.globalInstance()

        self._setup_ui()
        self._setup_menu()

    # ----------------------------------------
    # UI
    # ----------------------------------------
    def _setup_ui(self):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._on_tab_closed)
        self.setCentralWidget(self.tabs)

        # Stockage des webviews
        self.weapon_view = None
        self.armor_view = None
        self.item_view = None
        self._resource_browser = None

        # Status bar personnalisée
        self.status_bar = StatusBar(self, show_datetime=True)
        self.setStatusBar(self.status_bar)
        # Exemple de message d'accueil
        self.status_bar.set_message(_("Prêt"))

    # ----------------------------------------
    # Menu
    # ----------------------------------------
    def _setup_menu(self):
        menu_bar = self.menuBar()

        # --- Menu Fichier ---
        file_menu = menu_bar.addMenu(_("Fichier"))

        # Action A Propos
        about_icon = QIcon(str(self.rm.get_icon("about-app.png")))
        about_action = QAction(about_icon, _("A propos"), self)
        about_action.triggered.connect(self._open_about)
        file_menu.addAction(about_action)

        # Action Quitter
        quit_icon = QIcon(str(self.rm.get_icon("quit-app.png")))
        quit_action = QAction(quit_icon, _("Quitter"), self)
        quit_action.setShortcut("Alt+F4")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # --- Menu Tables ---
        menu_tables = menu_bar.addMenu(_("Tables"))

        # Table des Armes (W)
        action_weapons = menu_tables.addAction(_("Armes (Table W)"))
        action_weapons.triggered.connect(self.on_roll_weapon)

        # Table des Armures (A)
        action_armors = menu_tables.addAction(_("Armures (Table A)"))
        action_armors.triggered.connect(self.on_roll_armor)

        # Table des Objets (I)
        action_items = menu_tables.addAction(_("Objets (Table I)"))
        action_items.triggered.connect(self.on_roll_item)

        # --- Menu Développeur ---
        dev_menu = menu_bar.addMenu(_("Développeur"))

        devmode_icon = QIcon(str(self.rm.get_icon("devmode.png")))
        browse_action = QAction(devmode_icon, _("Parcourir les ressources"), self)
        browse_action.triggered.connect(self.open_resource_browser)
        dev_menu.addAction(browse_action)

    # ----------------------------------------
    # Tabs
    # ----------------------------------------
    def _on_tab_closed(self, index):
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)

        # Destruction propre
        widget.deleteLater()

        # Nettoyer les références
        if widget is self.weapon_view:
            self.log.debug("Weapons view closed")
            self.weapon_view = None
        elif widget is self.armor_view:
            self.log.debug("Armors view closed")
            self.armor_view = None
        elif widget is self.item_view:
            self.log.debug("Items view closed")
            self.item_view = None
        elif widget is self._resource_browser:
            self.log.debug("Resource browser view closed")
            self._resource_browser = None

    # ----------------------------------------
    # Actions
    # ----------------------------------------
    def _on_theme_changed(self, theme):
        # Propager aux WebViews existantes
        if self.weapon_view:
            self.weapon_view.set_theme(theme)
        if self.armor_view:
            self.armor_view.set_theme(theme)
        if self.item_view:
            self.item_view.set_theme(theme)

    # ----------------------------------------
    # Actions - Roll on Weapon Table
    # ----------------------------------------
    def on_roll_weapon(self):
        self.log.info("Roll on weapons table")
        def work():
            with Session() as session:
                from rpg_companion.repos.weapon_repo import WeaponRepository
                from rpg_companion.services.weapon_service import WeaponService

                repo = WeaponRepository(session)
                svc = WeaponService(repo)
                return svc.roll_weapon()

        self.show_dice_animation()

        worker = DBWorker(work)
        worker.signals.finished.connect(self._on_weapon_result)
        self._threadpool.start(worker)

    def _on_weapon_result(self, result, error):
        if error:
            QMessageBox.critical(self, "Erreur", str(error))
            return

        view = self.get_weapon_view()
        view.append(result)
        self.tabs.setCurrentWidget(view)

    def get_weapon_view(self):
        if self.weapon_view is None:
            self.weapon_view = WeaponsResultWebView(_("Tirages d'Armes"), self, self.on_roll_weapon)

            self.tabs.addTab(self.weapon_view, _("Armes"))

        return self.weapon_view

    def _on_weapon_view_loaded(self, ok):
        if not ok:
            print("ERREUR: Webview Armes n'a pas chargé la page HTML.")
            return

        # Injecter tout ce qui était en attente
        for result in self.weapon_pending_results:
            self.append_result_to_view(self.weapon_view, result)

        # Puis vider la file
        self.weapon_pending_results.clear()

    # ----------------------------------------
    # Actions - Roll on Armor Table
    # ----------------------------------------
    def on_roll_armor(self):
        self.log.info("Roll on armors table")
        def work():
            with Session() as session:
                from rpg_companion.repos.armor_repo import ArmorRepository
                from rpg_companion.services.armor_service import ArmorService

                repo = ArmorRepository(session)
                svc = ArmorService(repo)
                return svc.roll_armor()

        self.show_dice_animation()

        worker = DBWorker(work)
        worker.signals.finished.connect(self._on_armor_result)
        self._threadpool.start(worker)

    def _on_armor_result(self, result, error):
        if error:
            QMessageBox.critical(self, "Erreur", str(error))
            return

        view = self.get_armor_view()
        view.append(result)
        self.tabs.setCurrentWidget(view)

    def get_armor_view(self):
        if self.armor_view is None:
            self.armor_view = ArmorResultWebView(_("Tirages d'Armures"), self, self.on_roll_armor)

            self.tabs.addTab(self.armor_view, _("Armures"))

        return self.armor_view

    def _on_armor_view_loaded(self, ok):
        if not ok:
            print("ERREUR: Webview Armures n'a pas chargé la page HTML.")
            return

        # Injecter tout ce qui était en attente
        for result in self.armor_pending_results:
            self.append_result_to_view(self.armor_view, result)

        # Puis vider la file
        self.armor_pending_results.clear()

    # ----------------------------------------
    # Actions - Roll on Item Table
    # ----------------------------------------
    def on_roll_item(self):
        self.log.info("Roll on items table")
        def work():
            with Session() as session:
                from rpg_companion.repos.item_repo import ItemRepository
                from rpg_companion.services.item_service import ItemService

                repo = ItemRepository(session)
                svc = ItemService(repo)
                return svc.roll_item()

        self.show_dice_animation()

        worker = DBWorker(work)
        worker.signals.finished.connect(self._on_item_result)
        self._threadpool.start(worker)

    def _on_item_result(self, result, error):
        if error:
            QMessageBox.critical(self, "Erreur", str(error))
            return

        view = self.get_item_view()
        view.append(result)
        self.tabs.setCurrentWidget(view)

    def get_item_view(self):
        if self.item_view is None:
            self.item_view = ItemResultWebView(_("Tirages d'Objets"), self, self.on_roll_item)

            self.tabs.addTab(self.item_view, _("Objets"))

        return self.item_view

    def _on_item_view_loaded(self, ok):
        if not ok:
            print("ERREUR: Webview Objets n'a pas chargé la page HTML.")
            return

        # Injecter tout ce qui était en attente
        for result in self.item_pending_results:
            self.append_result_to_view(self.item_view, result)

        # Puis vider la file
        self.item_pending_results.clear()

    # ----------------------------------------
    # Actions - Resource Browser
    # ----------------------------------------
    def open_resource_browser(self):
        view = self.get_resource_browser_view()
        self.tabs.setCurrentWidget(view)
    
    def get_resource_browser_view(self):
        if self._resource_browser is None:
            self._resource_browser = ResourceBrowser(self)
            self.tabs.addTab(self._resource_browser, _("Ressources"))

        return self._resource_browser

    # ----------------------------------------
    # Actions - About Dialog
    # ----------------------------------------
    def _open_about(self):
        self.log.info("Dialog: About")

        dlg = AboutDialog(
            app_name="RPG Companion",
            version=version_app,
            build_date=BUILD_DATE,
            parent=self
        )
        dlg.exec()

    # ----------------------------------------
    # Overlays
    # ----------------------------------------
    def show_dice_animation(self):
            """Affiche l'animation de lancer de dés."""
            overlay = DiceOverlay(self, "d10-dice.png", ResourceType.ICON)
            overlay.show()

    # ----------------------------------------
    # Events
    # ----------------------------------------
    def _on_theme_changed(self, theme):
        # Propager aux WebViews existantes
        if self.weapon_view:
            self.weapon_view.set_theme(theme)
        if self.armor_view:
            self.armor_view.set_theme(theme)
        if self.item_view:
            self.item_view.set_theme(theme)

        # Propager au status bar
        try:
            self.status_bar.set_theme(theme)
        except Exception:
            # Ne pas planter l'application si la status bar n'est pas encore créée
            pass
