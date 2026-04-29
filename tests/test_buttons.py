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


    def test_press_without_release(server):
    """Press без release — состояние должно быть PRESSED"""
    res = requests.post(f"{BASE}/event", json={"button": 2, "action": "press"})
    assert res.json()["event"] == "PRESS"


def test_multiple_buttons(server):
    """Несколько кнопок независимы друг от друга"""
    requests.post(f"{BASE}/event", json={"button": 1, "action": "press"})
    requests.post(f"{BASE}/event", json={"button": 2, "action": "press"})
    requests.post(f"{BASE}/event", json={"button": 3, "action": "press"})

    time.sleep(0.2)

    res1 = requests.post(f"{BASE}/event", json={"button": 1, "action": "release"})
    res2 = requests.post(f"{BASE}/event", json={"button": 2, "action": "release"})
    res3 = requests.post(f"{BASE}/event", json={"button": 3, "action": "release"})

    assert res1.json()["event"] == "SHORT_CLICK"
    assert res2.json()["event"] == "SHORT_CLICK"
    assert res3.json()["event"] == "SHORT_CLICK"


def test_invalid_action(server):
    """Неизвестный action — должен вернуть ошибку"""
    res = requests.post(f"{BASE}/event", json={"button": 1, "action": "unknown"})
    assert "error" in res.json()


def test_invalid_data_none(server):
    """button=None, action=None — не должен падать с 500"""
    res = requests.post(f"{BASE}/event", json={"button": None, "action": None})
    assert res.status_code == 200
    assert "error" in res.json()


def test_release_without_press(server):
    """Release без press — invalid state"""
    res = requests.post(f"{BASE}/event", json={"button": 99, "action": "release"})
    assert "error" in res.json()