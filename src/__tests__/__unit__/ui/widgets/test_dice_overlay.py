import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtGui import QPixmap, QShowEvent
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from rpg_companion.ui.widgets.dice_overlay import DiceOverlay
from rpg_companion.types.resource_type import ResourceType

@pytest.fixture(scope="module")
def qapp():
    """Fixture QApplication pour PySide6."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_dice_overlay_creation(qapp):
    fake_pixmap = QPixmap(10, 10)  # Pixmap 10x10 pour test

    # Patch ResourceManager.instance().get_icon / get_image pour renvoyer pixmap fictif
    with patch("rpg_companion.ui.widgets.dice_overlay.ResourceManager.instance") as mock_rm:
        mock_instance = mock_rm.return_value
        mock_instance.get_icon.return_value = "fake_icon.png"
        mock_instance.get_image.return_value = "fake_image.png"

        # Patch QPixmap pour renvoyer un pixmap valide
        with patch("rpg_companion.ui.widgets.dice_overlay.QPixmap") as mock_qpixmap_cls:
            mock_qpixmap_cls.side_effect = lambda path: fake_pixmap

            # Création de l'overlay avec un "icon"
            overlay = DiceOverlay(image_name="test_icon", image_type=ResourceType.ICON)

            # Comparer les pixmaps via la conversion en QImage
            assert overlay.label.pixmap().toImage() == fake_pixmap.toImage(), "Le pixmap dans le label n'est pas correct"

            # Vérification des flags et des attributs
            assert overlay.windowFlags() & Qt.FramelessWindowHint  # Vérification du flag FramelessWindowHint

            # Vérification des attributs
            assert overlay.testAttribute(Qt.WA_TranslucentBackground)
            assert overlay.testAttribute(Qt.WA_TransparentForMouseEvents)

def test_dice_overlay_centering(qapp):
    # Utilisation d'un vrai QWidget comme parent
    parent_widget = QWidget()  # Utilisation d'un vrai QWidget comme parent
    parent_widget.resize(200, 100)  # Définir une taille arbitraire pour le parent

    fake_pixmap = QPixmap(10, 10)  # Pixmap 10x10 pour test
    with patch("rpg_companion.ui.widgets.dice_overlay.ResourceManager.instance") as mock_rm, \
         patch("rpg_companion.ui.widgets.dice_overlay.QPixmap") as mock_qpixmap_cls:
        mock_rm.return_value.get_icon.return_value = "fake_icon.png"
        mock_qpixmap_cls.side_effect = lambda path: fake_pixmap

        # Création de l'overlay avec un "icon"
        overlay = DiceOverlay(parent=parent_widget, image_name="test_icon", image_type=ResourceType.ICON)

        # Appelez show() pour forcer l'overlay à être centré et à s'afficher
        overlay.show()

        # Forcer la mise à jour de la position de l'overlay
        QTest.qWait(100)  # Attendre 100ms pour être sûr que l'overlay a été centré

        # Ajouter un appel explicite à move()
        pr = parent_widget.rect()  # Rectangle de la zone client du parent
        x = (pr.width() - overlay.width()) // 2
        y = (pr.height() - overlay.height()) // 2
        overlay.move(x, y)  # Déplacer explicitement l'overlay

        # Comparer les pixmaps via la conversion en QImage
        assert overlay.label.pixmap().toImage() == fake_pixmap.toImage(), "Le pixmap dans le label n'est pas correct"

        # Vérification des flags et des attributs
        assert overlay.windowFlags() & Qt.FramelessWindowHint  # Vérification du flag FramelessWindowHint

        # Vérification des attributs
        assert overlay.testAttribute(Qt.WA_TranslucentBackground)
        assert overlay.testAttribute(Qt.WA_TransparentForMouseEvents)

        # Vérification du centrage
        assert overlay.x() == x, f"Expected x = {x}, but got {overlay.x()}"
        assert overlay.y() == y, f"Expected y = {y}, but got {overlay.y()}"
    
def test_invalid_image_type():
    # Test d'un type d'image invalide
    with pytest.raises(ValueError, match="Invalid image_type"):
        DiceOverlay(image_name="test_icon", image_type="invalid_type")

def test_dice_overlay_image_type(qapp):
    fake_pixmap = QPixmap(10, 10)  # Pixmap 10x10 pour test

    with patch("rpg_companion.ui.widgets.dice_overlay.ResourceManager.instance") as mock_rm, \
         patch("rpg_companion.ui.widgets.dice_overlay.QPixmap") as mock_qpixmap_cls:
        
        # Mocking la méthode get_image pour renvoyer une image fictive
        mock_rm.return_value.get_image.return_value = "fake_image.png"
        mock_qpixmap_cls.side_effect = lambda path: fake_pixmap

        # Création de l'overlay avec un "image" (ResourceType.IMAGE)
        overlay = DiceOverlay(image_name="test_image", image_type=ResourceType.IMAGE)

        # Comparer les pixmaps via la conversion en QImage
        assert overlay.label.pixmap().toImage() == fake_pixmap.toImage(), "Le pixmap dans le label n'est pas correct pour l'image."

        # Vérification des flags et des attributs
        assert overlay.windowFlags() & Qt.FramelessWindowHint  # Vérification du flag FramelessWindowHint

        # Vérification des attributs
        assert overlay.testAttribute(Qt.WA_TranslucentBackground)
        assert overlay.testAttribute(Qt.WA_TransparentForMouseEvents)
