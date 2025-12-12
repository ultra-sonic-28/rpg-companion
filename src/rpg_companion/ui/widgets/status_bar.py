# rpg_companion/ui/widgets/status_bar.py
from __future__ import annotations

from typing import Optional
from datetime import datetime

from PySide6.QtWidgets import QStatusBar, QLabel, QProgressBar, QWidget, QHBoxLayout
from PySide6.QtCore import QTimer, Qt, Signal, Slot


class StatusBar(QStatusBar):
    """
    StatusBar personnalisable pour l'application.
    Fournit :
     - message temporaire / permanent
     - horodatage (optionnel)
     - zone pour widgets additionnels (ex: icônes, compteurs)
     - barre de progression intégrée
     - méthode set_theme pour adapter les styles
    """

    # signal émis lorsqu'on change le message (utile pour tests ou logs)
    message_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None, show_datetime: bool = True):
        super().__init__(parent)

        self._main_label = QLabel("")
        self._main_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.addWidget(self._main_label, 1)

        # zone widgets additionnels (alignés à droite)
        self._widget_area = QWidget()
        self._widget_layout = QHBoxLayout(self._widget_area)
        self._widget_layout.setContentsMargins(0, 0, 0, 0)
        self._widget_layout.setSpacing(8)
        self._widget_layout.setAlignment(Qt.AlignRight)
        self.addPermanentWidget(self._widget_area)

        # timestamp label
        self._datetime_label = QLabel("")
        self._show_datetime = show_datetime
        if show_datetime:
            self.addPermanentWidget(self._datetime_label)

            # Timer pour mettre à jour l'heure chaque seconde (faible coût)
            self._datetime_timer = QTimer(self)
            self._datetime_timer.setInterval(1000)
            self._datetime_timer.timeout.connect(self._update_datetime)
            self._datetime_timer.start()
            self._update_datetime()
        else:
            self._datetime_timer = None

        # Barre de progression (cachée tant qu'inutilisée)
        self._progress = QProgressBar()
        self._progress.setMaximumWidth(200)
        self._progress.setVisible(False)
        self.addPermanentWidget(self._progress)

        # Timer pour messages temporaires
        self._temp_timer = QTimer(self)
        self._temp_timer.setSingleShot(True)
        self._temp_timer.timeout.connect(self.clearMessage)

    # -------- Public API --------
    def set_message(self, text: str) -> None:
        """Message permanent (reste affiché jusqu'à clearMessage)."""
        self._temp_timer.stop()
        self._main_label.setText(text)
        self.message_changed.emit(text)

    def set_temporary_message(self, text: str, timeout_ms: int = 3000) -> None:
        """
        Affiche un message temporaire pendant `timeout_ms` millisecondes.
        S'il y avait un message temporaire en cours, il est remplacé.
        """
        self._main_label.setText(text)
        self._temp_timer.start(timeout_ms)
        self.message_changed.emit(text)

    def clearMessage(self) -> None:
        """Efface le texte principal."""
        self._temp_timer.stop()
        self._main_label.setText("")
        self.message_changed.emit("")

    def set_progress(self, value: int, maximum: int = 100) -> None:
        """Met à jour la barre de progression (et la rend visible)."""
        self._progress.setMaximum(maximum)
        self._progress.setValue(value)
        self._progress.setVisible(True)

    def hide_progress(self) -> None:
        """Cache la barre de progression."""
        self._progress.setVisible(False)
        self._progress.setValue(0)

    def add_widget(self, widget: QWidget) -> None:
        """Ajoute un widget dans la zone permanente (à droite)."""
        self._widget_layout.addWidget(widget)
        widget.show()

    def remove_widget(self, widget: QWidget) -> None:
        """Retire un widget ajouté précédemment."""
        self._widget_layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()

    def set_show_datetime(self, show: bool) -> None:
        """Active / désactive l'affichage de la date/heure."""
        if show and not self._show_datetime:
            self.addPermanentWidget(self._datetime_label)
            if self._datetime_timer:
                self._datetime_timer.start()
            else:
                self._datetime_timer = QTimer(self)
                self._datetime_timer.setInterval(1000)
                self._datetime_timer.timeout.connect(self._update_datetime)
                self._datetime_timer.start()
            self._update_datetime()
        elif not show and self._show_datetime:
            self.removeWidget(self._datetime_label)
            if self._datetime_timer:
                self._datetime_timer.stop()
        self._show_datetime = show

    def set_theme(self, theme_name: str) -> None:
        """
        Application simple d'une classe de style selon le thème.
        On peut étendre pour charger CSS depuis ThemeManager.
        """
        # Exemple très simple : ajouter une classe CSS (Qt styleSheet) en fonction du thème
        if theme_name and "dark" in theme_name.lower():
            self.setStyleSheet("QStatusBar { background: #2b2b2b; color: #eaeaea; }")
        else:
            self.setStyleSheet("")  # fallback / hérite du style global

    # -------- Internal --------
    @Slot()
    def _update_datetime(self) -> None:
        if self._show_datetime:
            now = datetime.now()
            # Format compact : 2025-12-12 23:59:59
            self._datetime_label.setText(now.strftime("%Y-%m-%d %H:%M:%S"))
