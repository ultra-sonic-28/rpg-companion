from typing import Any
from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from datetime import datetime

from rpg_companion.utils.resource_manager import ResourceManager

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

class AboutDialog(QDialog):

    def __init__(self, app_name: str, version: str, build_date: str, parent=None):
        super().__init__(parent)
        strTitle = _("À propos")
        self.setWindowTitle(f"{strTitle} – {app_name}")
        self.setModal(True)
        self.setMinimumWidth(450)

        rm = ResourceManager.instance()
        logo_path = rm.get_image("logo-512x512.png")
        pixmap = QPixmap(str(logo_path))

        # ---------- Widgets colonne gauche ----------
        logo_label = QLabel()
        logo_label.setPixmap(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)

        left_col = QVBoxLayout()
        left_col.addWidget(logo_label)
        left_col.setAlignment(Qt.AlignTop)

        # ---------- Widgets colonne droite ----------
        name_label = QLabel(f"<h2>{app_name}</h2>")
        strVersion = _("Version :")
        version_label = QLabel(f"<b>{strVersion}</b> {version}")
        strCompiled = _("Compilation :")
        date_label = QLabel(f"<b>{strCompiled}</b> {build_date}")

        text_col = QVBoxLayout()
        text_col.addWidget(name_label)
        text_col.addWidget(version_label)
        text_col.addWidget(date_label)
        text_col.addStretch()

        # ---------- Layout principal ----------
        hbox = QHBoxLayout()
        hbox.addLayout(left_col)
        hbox.addLayout(text_col)

        # ---------- Bouton fermer ----------
        close_btn = QPushButton(_("Fermer"))
        close_btn.clicked.connect(self.accept)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(hbox)
        main_layout.addSpacing(15)
        main_layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
