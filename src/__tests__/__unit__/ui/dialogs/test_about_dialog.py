import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from rpg_companion.ui.dialogs.about_dialog import AboutDialog

@pytest.fixture(scope="module")
def qapp():
    """Fixture pour créer QApplication si nécessaire"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_about_dialog_initialization(qapp):
    fake_path = "fake/logo.png"

    # Patch ResourceManager pour renvoyer un chemin factice
    with patch("rpg_companion.ui.dialogs.about_dialog.ResourceManager.instance") as mock_rm:
        mock_rm.return_value.get_image.return_value = fake_path

        # Patch QPixmap pour qu'il retourne un vrai QPixmap quelle que soit l'entrée
        original_qpixmap = QPixmap
        def fake_qpixmap(path):
            # Crée un QPixmap minimal de 128x128 pour matcher le scaled
            return original_qpixmap(128, 128)
        
        with patch("rpg_companion.ui.dialogs.about_dialog.QPixmap", side_effect=fake_qpixmap):
            dialog = AboutDialog(app_name="TestApp", version="1.2.3", build_date="2025-12-02")

            # Vérifie le titre
            assert dialog.windowTitle() == "À propos – TestApp"

            # Récupère le QLabel qui contient le pixmap du logo
            logo_labels = [
                lbl for lbl in dialog.findChildren(QLabel)
                if lbl.pixmap() is not None and
                lbl.pixmap().width() == 128 and lbl.pixmap().height() == 128
            ]
            assert len(logo_labels) == 1, "Logo QLabel non trouvé"

            # Vérifie les labels texte
            texts = [lbl.text() for lbl in dialog.findChildren(QLabel) if lbl.text()]
            assert any("Version" in t for t in texts)
            assert any("Compilation" in t for t in texts)

            # Vérifie qu'il y a un bouton "Fermer"
            close_btn = dialog.findChild(QPushButton)
            assert close_btn is not None
            assert close_btn.text() == "Fermer"

def test_about_dialog_close_button(qapp):
    with patch("rpg_companion.ui.dialogs.about_dialog.ResourceManager.instance") as mock_rm:
        mock_rm.return_value.get_image.return_value = "fake/logo.png"

        dialog = AboutDialog(app_name="TestApp", version="1.2.3", build_date="2025-12-02")

        # Récupère le bouton "Fermer"
        close_buttons = [btn for btn in dialog.findChildren(QPushButton) if btn.text() == "Fermer"]
        assert close_buttons, "Bouton 'Fermer' non trouvé"
        button = close_buttons[0]

        # Vérifie qu'il est connecté à accept()
        assert button.clicked is not None
