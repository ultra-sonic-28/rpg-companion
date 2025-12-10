import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PySide6.QtGui import QPixmap, QShowEvent
from PySide6.QtCore import Qt, QTimer
from pytestqt import qtbot
from PySide6.QtTest import QTest

from rpg_companion.ui.widgets.dice_overlay import DiceOverlay, ResourceType

@pytest.fixture
def overlay(qtbot):
    # Créer un parent pour l'overlay
    parent_widget = QWidget()
    parent_widget.resize(200, 100)  # Taille arbitraire pour le parent

    fake_pixmap = QPixmap(10, 10)

    # Mocking la méthode get_icon et QPixmap
    with patch("rpg_companion.ui.widgets.dice_overlay.ResourceManager.instance") as mock_rm, \
         patch("rpg_companion.ui.widgets.dice_overlay.QPixmap") as mock_qpixmap_cls:
        mock_rm.return_value.get_icon.return_value = "fake_icon.png"
        mock_qpixmap_cls.side_effect = lambda path: fake_pixmap

        # Création de l'overlay
        overlay = DiceOverlay(parent=parent_widget, image_name="test_icon", image_type=ResourceType.ICON)

        # Ajout de l'overlay au qtbot pour gestion d'UI
        qtbot.addWidget(overlay)
        return overlay, parent_widget


def test_start_animation(overlay, qtbot):
    overlay, _ = overlay

    # Mock la méthode _start_animation
    overlay._start_animation = MagicMock()

    # Simuler manuellement l'appel à showEvent
    event = QShowEvent()  # Créer un événement de type showEvent
    overlay.showEvent(event)

    # Vérifier que QTimer a bien planifié l'animation
    assert overlay._anim_started is True, "L'animation n'a pas démarré comme prévu"

    # Attendre un peu pour s'assurer que l'animation a démarré
    QTest.qWait(100)

    # Vérifier que _start_animation a été appelé
    overlay._start_animation.assert_called_once()
