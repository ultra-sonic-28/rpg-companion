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


def test_show_event(overlay, qtbot):
    overlay, parent_widget = overlay

    parent_widget.show()
    overlay.show()

    # Attendre que l'overlay soit centré
    qtbot.waitUntil(lambda: overlay.y() == (parent_widget.rect().height() - overlay.height()) // 2, timeout=1000)

    # Vérifier la position de l'overlay après avoir été centré
    pr = parent_widget.rect()
    x = (pr.width() - overlay.width()) // 2
    y = (pr.height() - overlay.height()) // 2

    assert overlay.x() == x, f"Expected x = {x}, but got {overlay.x()}"
    assert overlay.y() == y, f"Expected y = {y}, but got {overlay.y()}"


def test_show_event_no_parent(qtbot):
    overlay = DiceOverlay(parent=None, image_name="test_icon", image_type=ResourceType.ICON)

    # Mock _start_animation pour s'assurer qu'il n'est pas appelé
    overlay._start_animation = MagicMock()

    # Créer un QShowEvent et appeler showEvent manuellement
    event = QShowEvent()
    overlay.showEvent(event)

    # Vérifier que l'overlay n'a pas essayé de démarrer l'animation
    overlay._start_animation.assert_not_called()

    # Vérifier que _anim_started est resté False
    assert overlay._anim_started is False
