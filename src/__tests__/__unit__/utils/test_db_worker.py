import pytest
from unittest.mock import MagicMock

from rpg_companion.utils.qthreads import DBWorker, WorkerSignals


# ---------------------------------------------------------
# Test de la classe WorkerSignals
# ---------------------------------------------------------
def test_worker_signals_exist():
    signals = WorkerSignals()
    assert hasattr(signals, "finished")
    assert callable(signals.finished.emit)


# ---------------------------------------------------------
# Test : DBWorker.run() — cas nominal
# ---------------------------------------------------------
def test_db_worker_run_success():
    mock_fn = MagicMock(return_value="OK")

    worker = DBWorker(mock_fn, 1, 2, value=3)

    # Mock du slot connecté au signal
    received = {}

    def slot(result, error):
        received["result"] = result
        received["error"] = error

    worker.signals.finished.connect(slot)

    worker.run()

    mock_fn.assert_called_once_with(1, 2, value=3)
    assert received["result"] == "OK"
    assert received["error"] is None


# ---------------------------------------------------------
# Test : DBWorker.run() — cas exception
# ---------------------------------------------------------
def test_db_worker_run_exception():
    def crashing_fn():
        raise ValueError("boom")

    worker = DBWorker(crashing_fn)

    received = {}

    def slot(result, error):
        received["result"] = result
        received["error"] = error

    worker.signals.finished.connect(slot)

    worker.run()

    assert received["result"] is None
    assert isinstance(received["error"], ValueError)
    assert str(received["error"]) == "boom"
