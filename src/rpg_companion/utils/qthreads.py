from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from typing import Callable, Any

class WorkerSignals(QObject):
    finished = Signal(object, object)  # result, error

class DBWorker(QRunnable):
    def __init__(self, fn: Callable[..., Any], *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result, None)
        except Exception as exc:
            self.signals.finished.emit(None, exc)
