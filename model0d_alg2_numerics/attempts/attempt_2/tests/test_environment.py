import pytest

from src.io_utils import APPROVED_EXECUTION_ENV, validate_execution_environment


def test_approved_execution_environment_passes(monkeypatch):
    for key, value in APPROVED_EXECUTION_ENV.items():
        monkeypatch.setenv(key, value)
    validate_execution_environment()


def test_execution_environment_drift_fails(monkeypatch):
    for key, value in APPROVED_EXECUTION_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv("OMP_NUM_THREADS", "2")
    with pytest.raises(RuntimeError, match="OMP_NUM_THREADS"):
        validate_execution_environment()
