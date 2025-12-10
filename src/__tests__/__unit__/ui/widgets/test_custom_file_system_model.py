from typing import Any
import pytest
from PySide6.QtCore import QDir, Qt, QModelIndex
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileSystemModel

from unittest.mock import MagicMock

from rpg_companion.i18n import i18n
from rpg_companion.ui.widgets.custom_file_system_model import CustomFileSystemModel

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

i18n.install_global_translation()

@pytest.fixture
def custom_model():
    """Fixture qui initialise un modèle personnalisé"""
    return CustomFileSystemModel()


def test_header_data(custom_model):
    """Test pour vérifier si les en-têtes sont bien traduits"""

    # Tester pour chaque colonne (Nom, Taille, Type, Date de modification)
    for col, expected_header in enumerate([
        _("Nom"),                   # Colonne 0 : Nom du fichier
        _("Taille"),                # Colonne 1 : Taille
        _("Type"),                  # Colonne 2 : Type
        _("Date de modification")   # Colonne 3 : Date
    ]):
        # Appel de la méthode headerData
        result = custom_model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
        assert result == expected_header, f"Erreur sur l'en-tête de la colonne {col}"


def test_data_for_directory(custom_model):
    """Test de la méthode data pour un répertoire"""
    
    # Mocking de fileInfo pour simuler un répertoire
    mock_file_info = MagicMock()
    mock_file_info.isDir.return_value = True  # Simule un répertoire

    # Création d'un index fictif
    mock_index = MagicMock(spec=QModelIndex)
    mock_index.column.return_value = 2  # On se place sur la colonne "Type"

    # Simuler l'appel à fileInfo() pour qu'il retourne notre mock
    custom_model.fileInfo = MagicMock(return_value=mock_file_info)

    # Test de la méthode data
    result = custom_model.data(mock_index, Qt.DisplayRole)
    assert result == _("Dossier"), f"Le type d'un répertoire devrait être 'Dossier', mais c'est '{result}'"


@pytest.mark.parametrize(
    "col, expected_header",
    [
        (0, _("Nom")),  # Colonne 0 : Nom du fichier
        (1, _("Taille")),  # Colonne 1 : Taille
        (2, _("Type")),  # Colonne 2 : Type
        (3, _("Date de modification")),  # Colonne 3 : Date
    ]
)
def test_header_data_with_parametrize(custom_model, col, expected_header):
    """Test paramétré pour vérifier les en-têtes"""
    result = custom_model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
    assert result == expected_header, f"Erreur sur l'en-tête de la colonne {col}"


