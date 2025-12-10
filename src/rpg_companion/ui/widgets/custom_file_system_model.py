from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtWidgets import QFileSystemModel

from typing import Any

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

class CustomFileSystemModel(QFileSystemModel):
    def __init__(self):
        super().__init__()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # Personnalisation des en-têtes
            headers = [
                _("Nom"),                   # Colonne 0 : Nom du fichier
                _("Taille"),                # Colonne 1 : Taille
                _("Type"),                  # Colonne 2 : Type
                _("Date de modification")   # Colonne 3 : Date
            ]
            return headers[section] if 0 <= section < len(headers) else super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int) -> Any:
            if role == Qt.DisplayRole:
                # Si l'on est dans la colonne "Type" (généralement colonne 2)
                if index.column() == 2:  # Vérifier si on est bien dans la colonne "Type"
                    file_info = self.fileInfo(index)
                    if file_info.isDir():  # Si c'est un répertoire
                        return _("Dossier")  # Traduction pour "file folder"
                    else:
                        # Pour les autres types de fichiers, on retourne le type par défaut
                        return super().data(index, role)
                else:
                    # Si ce n'est pas la colonne "Type", on retourne simplement la donnée normale
                    return super().data(index, role)

            return super().data(index, role)
