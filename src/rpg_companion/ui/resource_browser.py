from pathlib import Path
import json
from typing import Any
from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTreeView, QLabel, QHeaderView
)
from PySide6.QtGui import QPixmap
from rpg_companion.ui.widgets.custom_file_system_model import CustomFileSystemModel
from rpg_companion.utils.resource_manager import ResourceManager

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

class ResourceBrowser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rm = ResourceManager.instance()

        self.assets_root = Path(self.rm._resolve("."))  # répertoire assets/
        self.strNoPreview = _("Aucun aperçu")
        self.strNoPreviewAvailable = _("Aucun aperçu disponible")

        # ---- Barre de recherche ----
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText(_("Rechercher une ressource..."))
        self.search_bar.textChanged.connect(self.apply_filter)

        # ---- Modèle fichier ----
        self.model = CustomFileSystemModel()
        self.model.setRootPath(str(self.assets_root))
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        # ---- TreeView ----
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        root_index = self.model.index(str(self.assets_root))
        self.tree.setRootIndex(root_index)
        self.tree.setColumnWidth(0, 350)
        self.tree.setSortingEnabled(True)
        self.tree.setAnimated(True)

        # Traduire les en-têtes des colonnes après avoir défini le modèle
        #self.translate_headers()

        # ---- Preview ----
        self.preview_label = QLabel(self.strNoPreview)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedSize(400, 400)

        # Sélection → aperçu
        self.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)

        # Double-clic → ouvrir dans l'explorateur
        self.tree.doubleClicked.connect(self.on_double_click)

        # ---- Layout ----
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(self.tree)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.preview_label)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)


    # ------------------------------------------------------------------
    def apply_filter(self, text: str):
        """
        Recherche récursive dans le dossier assets.
        Sélection automatique de la première correspondance.
        """
        # Reset root index sur assets
        root_index = self.model.index(str(self.assets_root))
        self.tree.setRootIndex(root_index)
        self.tree.collapseAll()

        if not text.strip():
            return  # aucune recherche = juste afficher tout

        # Parcours récursif avec Path.rglob
        matches = list(self.assets_root.rglob(f"*{text}*"))
        if not matches:
            return

        first_match = matches[0]
        source_index = self.model.index(str(first_match))
        if not source_index.isValid():
            return

        # Expander les parents pour voir l'item
        parent = source_index.parent()
        while parent.isValid():
            self.tree.expand(parent)
            parent = parent.parent()

        # Sélectionner et scroller sur la première occurrence
        self.tree.setCurrentIndex(source_index)
        self.tree.scrollTo(source_index)

    # ------------------------------------------------------------------
    def on_selection_changed(self, *_):
        """Met à jour l’aperçu à droite."""
        index = self.tree.currentIndex()
        if not index.isValid():
            self.preview_label.setText(self.strNoPreview)
            self.preview_label.setPixmap(QPixmap())
            return

        path = Path(self.model.filePath(index))

        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            pix = QPixmap(str(path))
            if not pix.isNull():
                scaled = pix.scaled(
                    self.preview_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
                self.preview_label.setPixmap(scaled)
            else:
                self.preview_label.setText(_("Impossible de charger l'image"))
        elif path.is_file() and path.suffix.lower() in {".txt", ".json", ".toml"}:
            try:
                content = path.read_text(encoding="utf-8")
                self.preview_label.setText(content[:2000])  # limite 2000 caractères
            except Exception as e:
                strExcep = _("Impossible de lire le fichier :")
                self.preview_label.setText(f"{strExcep}\n{e}")
        else: 
            self.preview_label.setText(self.strNoPreviewAvailable)
            self.preview_label.setPixmap(QPixmap())

    # ------------------------------------------------------------------
    def on_double_click(self, index):
        """Ouvre le fichier ou dossier dans l'explorateur du système."""
        import subprocess, platform
        path = Path(self.model.filePath(index))
        system = platform.system()
        if system == "Windows":
            subprocess.Popen(["explorer", str(path)])
        elif system == "Darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
