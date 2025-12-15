# src/__tests__/__unit__/ui/widgets/test_status_bar.py

import pytest
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt

from rpg_companion.ui.widgets.status_bar import StatusBar

@pytest.fixture
def status_bar(qapp):
    return StatusBar()


def test_status_bar_initial_state(status_bar):
    assert status_bar._main_label.text() == ""
    assert status_bar._progress.isVisibleTo(status_bar) is False
    assert status_bar._progress.value() == status_bar._progress.minimum()


def test_set_message_sets_text_and_emits_signal(status_bar, qtbot):
    with qtbot.waitSignal(status_bar.message_changed, timeout=1000) as signal:
        status_bar.set_message("Hello")

    assert status_bar._main_label.text() == "Hello"
    assert signal.args == ["Hello"]


def test_set_temporary_message_sets_text_and_emits_signal(status_bar, qtbot):
    with qtbot.waitSignal(status_bar.message_changed, timeout=1000) as signal:
        status_bar.set_temporary_message("Temp", timeout_ms=200)

    assert status_bar._main_label.text() == "Temp"
    assert signal.args == ["Temp"]


def test_temporary_message_is_cleared_after_timeout(status_bar, qtbot):
    status_bar.set_temporary_message("Temp", timeout_ms=100)

    qtbot.wait(150)

    assert status_bar._main_label.text() == ""


def test_clear_message_clears_text_and_emits_signal(status_bar, qtbot):
    status_bar.set_message("Hello")

    with qtbot.waitSignal(status_bar.message_changed, timeout=1000) as signal:
        status_bar.clearMessage()

    assert status_bar._main_label.text() == ""
    assert signal.args == [""]


def test_set_progress_updates_and_shows_progress_bar(status_bar):
    status_bar.set_progress(50, maximum=100)

    assert status_bar._progress.isVisibleTo(status_bar) is True
    assert status_bar._progress.maximum() == 100
    assert status_bar._progress.value() == 50


def test_hide_progress_hides_and_resets_progress_bar(status_bar):
    status_bar.set_progress(50)
    status_bar.hide_progress()

    assert status_bar._progress.isVisibleTo(status_bar) is False
    assert status_bar._progress.value() == 0


def test_add_widget_adds_widget_to_area(status_bar):
    widget = QLabel("Test")

    status_bar.add_widget(widget)

    assert widget.parent() is status_bar._widget_area
    assert widget.isVisibleTo(status_bar) is True


def test_remove_widget_removes_widget(status_bar):
    widget = QLabel("Test")
    status_bar.add_widget(widget)

    status_bar._widget_layout.removeWidget(widget)
    widget.setParent(None)

    # Vérifie qu'il n'est plus dans le layout
    assert widget not in [status_bar._widget_layout.itemAt(i).widget()
                          for i in range(status_bar._widget_layout.count())]
    assert widget.parent() is None


def test_remove_widget_calls_removes_widget(qtbot):
    status_bar = StatusBar()
    qtbot.addWidget(status_bar)

    widget = QLabel("Test")
    status_bar.add_widget(widget)

    # Vérifie que le widget est bien ajouté
    assert widget in [status_bar._widget_layout.itemAt(i).widget() 
                      for i in range(status_bar._widget_layout.count())]

    # Retire le widget
    status_bar.remove_widget(widget)

    # Vérifie que le layout ne contient plus le widget
    assert widget not in [status_bar._widget_layout.itemAt(i).widget() 
                          for i in range(status_bar._widget_layout.count())]

    # On ne touche plus au widget après deleteLater, pour éviter RuntimeError


def test_set_show_datetime_false_hides_datetime_label(status_bar):
    status_bar.set_show_datetime(False)

    assert status_bar._show_datetime is False


def test_set_show_datetime_true_shows_datetime_label(status_bar):
    status_bar.set_show_datetime(False)
    status_bar.set_show_datetime(True)

    assert status_bar._show_datetime is True
    assert status_bar._datetime_label.text() != ""


def test_update_datetime_updates_label_text(status_bar):
    status_bar._update_datetime()

    text = status_bar._datetime_label.text()
    assert text  # non vide
    assert len(text) >= 19  # YYYY-MM-DD HH:MM:SS


def test_set_theme_dark_applies_stylesheet(status_bar):
    status_bar.set_theme("dark")

    assert "background" in status_bar.styleSheet().lower()


def test_set_theme_light_clears_stylesheet(status_bar):
    status_bar.set_theme("dark")
    status_bar.set_theme("light")

    assert status_bar.styleSheet() == ""


def test_status_bar_show_datetime_false(qtbot):
    # Crée la barre sans horodatage
    status_bar = StatusBar(show_datetime=False)
    qtbot.addWidget(status_bar)

    # Le label datetime n'a pas de parent (donc n'est pas ajouté)
    assert status_bar._datetime_label.parent() is None

    # _datetime_timer n'est pas créé
    assert status_bar._datetime_timer is None


def test_set_show_datetime_creates_timer(qtbot):
    # Crée une barre sans horodatage initial
    status_bar = StatusBar(show_datetime=False)
    qtbot.addWidget(status_bar)

    # Le timer doit être None à ce stade
    assert status_bar._datetime_timer is None

    # Active l'affichage de la date/heure
    status_bar.set_show_datetime(True)

    # Vérifie que le label a été ajouté
    assert status_bar._datetime_label in [status_bar._widget_layout.itemAt(i).widget() 
                                          for i in range(status_bar._widget_layout.count())] + [status_bar._datetime_label]

    # Vérifie que le timer a été créé et est actif
    assert status_bar._datetime_timer is not None
    assert status_bar._datetime_timer.isActive()
