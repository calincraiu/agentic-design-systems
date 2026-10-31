import pytest

from kit import bridge
from kit.paths import exchange_dir
from kit.runs import new_run, read_json

from .fake_gh import FakeGrasshopper


def test_ping_without_grasshopper_times_out():
    with pytest.raises(bridge.BridgeError, match="No answer"):
        bridge.ping(timeout=0.3)


def test_ping_and_generate_round_trip():
    exchange_dir().mkdir(parents=True)
    with FakeGrasshopper(exchange_dir()):
        assert bridge.ping(timeout=3)["system"] == "tower"
        run = new_run("bridge test")
        bridge.generate("tower", {"floors": 7}, run, timeout=3)
        assert len(read_json(run / "geometry.json")["curves"]) == 7


def test_errors_from_grasshopper_are_raised():
    exchange_dir().mkdir(parents=True)
    with FakeGrasshopper(exchange_dir(), active=False):
        with pytest.raises(bridge.BridgeError, match="OFF"):
            bridge.generate("tower", {}, new_run("x"), timeout=3)
    with FakeGrasshopper(exchange_dir(), system="facade"):
        with pytest.raises(bridge.BridgeError, match="facade"):
            bridge.generate("tower", {}, new_run("y"), timeout=3)
