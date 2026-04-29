import requests
import time
import subprocess
import pytest

BASE = "http://localhost:5000"


@pytest.fixture
def server():
    process = subprocess.Popen(["python", "simulator/server.py"])
    time.sleep(1)
    yield
    process.terminate()
    process.wait()


def test_short_click(server):
    requests.post(f"{BASE}/event", json={"button": 1, "action": "press"})
    time.sleep(0.2)
    res = requests.post(f"{BASE}/event", json={"button": 1, "action": "release"})
    assert res.json()["event"] == "SHORT_CLICK"


def test_long_click(server):
    requests.post(f"{BASE}/event", json={"button": 1, "action": "press"})
    time.sleep(1.5)
    res = requests.post(f"{BASE}/event", json={"button": 1, "action": "release"})
    assert res.json()["event"] == "LONG_CLICK"


def test_double_click(server):
    # первый клик
    requests.post(f"{BASE}/event", json={"button": 1, "action": "press"})
    time.sleep(0.1)
    res1 = requests.post(f"{BASE}/event", json={"button": 1, "action": "release"})
    assert res1.json()["event"] == "SHORT_CLICK"  # убрали SHORT_CLICK_PENDING

    # второй клик в окне
    time.sleep(0.2)
    requests.post(f"{BASE}/event", json={"button": 1, "action": "press"})
    time.sleep(0.1)
    res2 = requests.post(f"{BASE}/event", json={"button": 1, "action": "release"})
    assert res2.json()["event"] == "DOUBLE_CLICK"