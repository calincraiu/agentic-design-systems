import pytest


@pytest.fixture(autouse=True)
def isolated_folders(tmp_path, monkeypatch):
    """Keep every test's runs and bridge files out of the real repo folders."""
    monkeypatch.setenv("ADS_RUNS_DIR", str(tmp_path / "runs"))
    monkeypatch.setenv("ADS_EXCHANGE_DIR", str(tmp_path / "exchange"))
    return tmp_path
