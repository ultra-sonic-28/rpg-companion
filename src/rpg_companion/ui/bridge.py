from PySide6.QtCore import QObject, Slot

class Bridge(QObject):
    """
    Bridge entre JavaScript dans la QWebEngineView et Python.
    Chaque vue peut avoir son propre bridge.
    """

    def __init__(self, callback, parent=None):
        """
        :param callback: fonction Python à appeler lorsqu'un tirage est demandé
        """
        super().__init__(parent)
        self._callback = callback

    @Slot()
    def request_new_roll(self):
        """
        Méthode exposée à JavaScript via QWebChannel.
        Appelle le callback Python pour effectuer un nouveau tirage.
        """
        if callable(self._callback):
            self._callback()
