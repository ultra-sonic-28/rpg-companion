from __future__ import annotations
from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect

from rpg_companion.types.resource_type import ResourceType
from rpg_companion.utils.resource_manager import ResourceManager


class DiceOverlay(QWidget):
    """
    Overlay animé pour afficher une image (icône ou image complète).
    - Centré par rapport au parent
    - Fond transparent
    - Taille = image + 20px de marge
    - Animation fade-in → pause → fade-out + translation verticale
    """

    DURATION = 2000  # durée totale en ms
    FADE_DURATION = 600  # durée du fade-in / fade-out
    MARGIN = 20  # marge autour de l'image

    def __init__(self, parent=None, image_name: str = "", image_type: ResourceType = ResourceType.ICON):
        """
        :param image_name: nom du fichier dans assets/icons ou assets/images
        :param parent: parent QWidget
        :param image_type: "icon" ou "image"
        """
        super().__init__(parent)

        # --- Flags et attributs ---
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # --- Chargement de l'image selon type ---
        rm = ResourceManager.instance()
        if image_type == ResourceType.ICON:
            path = rm.get_icon(image_name)
        elif image_type == ResourceType.IMAGE:
            path = rm.get_image(image_name)
        else:
            raise ValueError(f"Invalid image_type: {image_type}.")

        pixmap = QPixmap(str(path))
        w, h = pixmap.width() + self.MARGIN * 2, pixmap.height() + self.MARGIN * 2
        self.resize(w, h)

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(self.MARGIN // 2, self.MARGIN // 2,
                                  self.MARGIN // 2, self.MARGIN // 2)
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel()
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # --- Effet d'opacité ---
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self._anim_started = False

        # Fermeture auto
        QTimer.singleShot(self.DURATION, self.close)

    # ----------------------------------------------------------------------
    # Centrage automatique
    # ----------------------------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)

        parent = self.parentWidget()
        if parent is None:
            return

        # Centre dans la zone client du parent
        pr = parent.rect()
        x = (pr.width() - self.width()) // 2
        y = (pr.height() - self.height()) // 2
        self.move(x, y)

        if not self._anim_started:
            self._anim_started = True
            QTimer.singleShot(0, self._start_animation)

    # ----------------------------------------------------------------------
    # Animation
    # ----------------------------------------------------------------------
    def _start_animation(self):
        # Fade-in
        fade_in = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        fade_in.setDuration(self.FADE_DURATION)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)

        # Translation verticale
        move_anim = QPropertyAnimation(self, b"pos", self)
        move_anim.setDuration(self.FADE_DURATION)
        move_anim.setStartValue(QPoint(self.x(), self.y() - 30))
        move_anim.setEndValue(QPoint(self.x(), self.y()))
        move_anim.setEasingCurve(QEasingCurve.OutQuad)

        # Fade-out
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        fade_out.setDuration(self.FADE_DURATION)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)

        # Groupe fade-in + translation
        fade_in_group = QParallelAnimationGroup()
        fade_in_group.addAnimation(fade_in)
        fade_in_group.addAnimation(move_anim)

        # Séquence complète : fade-in → pause → fade-out
        seq = QSequentialAnimationGroup(self)
        seq.addAnimation(fade_in_group)
        pause_duration = max(0, self.DURATION - 2 * self.FADE_DURATION)
        if pause_duration > 0:
            seq.addPause(pause_duration)
        seq.addAnimation(fade_out)

        seq.start()
