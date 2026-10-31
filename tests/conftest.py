import pytest


@pytest.fixture(autouse=True)
def isolated_runs(tmp_path, monkeypatch):
    """Keep every test's runs out of the real runs/ folder."""
    monkeypatch.setenv("ADS_RUNS_DIR", str(tmp_path / "runs"))
    return tmp_path
