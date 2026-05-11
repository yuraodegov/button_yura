"""
HTTP integration tests for simulator/server.py

Запуск: pytest tests/test_server.py -v
Сервер поднимается автоматически на свободном порту, после тестов убивается.
"""

import pytest
import requests
import subprocess
import sys
import os
import time
import socket

SIMULATOR_DIR = os.path.join(os.path.dirname(__file__), "..", "simulator")


def get_free_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def server():
    port = get_free_port()
    env = os.environ.copy()
    env["PORT"] = str(port)

    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        cwd=SIMULATOR_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # ждём пока сервер поднимется
    base = f"http://127.0.0.1:{port}"
    for _ in range(20):
        try:
            requests.get(base + "/", timeout=0.5)
            break
        except Exception:
            time.sleep(0.2)
    else:
        proc.kill()
        pytest.fail("Server did not start in time")

    yield base

    proc.kill()
    proc.wait()


# ── helpers ────────────────────────────────────────────────────────────────

def event(server, button, action):
    return requests.post(
        f"{server}/event",
        json={"button": button, "action": action},
        timeout=3,
    ).json()


# ── /status ────────────────────────────────────────────────────────────────

def test_status_ok(server):
    r = requests.get(f"{server}/status", timeout=3)
    assert r.status_code == 200


def test_status_has_fields(server):
    data = requests.get(f"{server}/status", timeout=3).json()
    assert "buttons" in data
    assert "long_press_threshold_ms" in data
    assert "double_click_window_ms" in data
    assert "pod" in data


def test_status_thresholds(server):
    data = requests.get(f"{server}/status", timeout=3).json()
    assert data["long_press_threshold_ms"] == 1000
    assert data["double_click_window_ms"]  == 500


# ── /event — press ─────────────────────────────────────────────────────────

def test_press_returns_press_event(server):
    res = event(server, button=1, action="press")
    assert res.get("event") == "PRESS"
    assert res.get("button") == 1


def test_press_appears_in_status(server):
    event(server, button=2, action="press")
    data = requests.get(f"{server}/status", timeout=3).json()
    assert 2 in data["buttons"] or "2" in data["buttons"]
    btn = data["buttons"].get(2) or data["buttons"].get("2")
    assert btn["state"] == "PRESSED"
    # cleanup
    event(server, button=2, action="release")


def test_held_ms_increases(server):
    event(server, button=3, action="press")
    time.sleep(0.3)
    d1 = requests.get(f"{server}/status", timeout=3).json()
    time.sleep(0.3)
    d2 = requests.get(f"{server}/status", timeout=3).json()

    ms1 = (d1["buttons"].get(3) or d1["buttons"].get("3"))["held_ms"]
    ms2 = (d2["buttons"].get(3) or d2["buttons"].get("3"))["held_ms"]
    assert ms2 > ms1
    # cleanup
    event(server, button=3, action="release")


# ── /event — short click ───────────────────────────────────────────────────

def test_short_click(server):
    event(server, button=1, action="press")
    time.sleep(0.1)
    res = event(server, button=1, action="release")
    assert res.get("event") == "SHORT_CLICK"
    assert "duration" in res
    assert res["duration"] < 1.0


def test_short_click_state_back_to_idle(server):
    event(server, button=1, action="press")
    time.sleep(0.1)
    event(server, button=1, action="release")
    data = requests.get(f"{server}/status", timeout=3).json()
    btn = data["buttons"].get(1) or data["buttons"].get("1")
    assert btn["state"] == "IDLE"
    assert btn["held_ms"] is None


# ── /event — long click ────────────────────────────────────────────────────

def test_long_click(server):
    event(server, button=1, action="press")
    time.sleep(1.1)
    res = event(server, button=1, action="release")
    assert res.get("event") == "LONG_CLICK"
    assert res.get("duration") >= 1.0


# ── /event — double click ──────────────────────────────────────────────────

def test_double_click(server):
    event(server, button=1, action="press")
    time.sleep(0.05)
    event(server, button=1, action="release")
    time.sleep(0.1)                            # в пределах double_click_window
    event(server, button=1, action="press")
    time.sleep(0.05)
    res = event(server, button=1, action="release")
    assert res.get("event") == "DOUBLE_CLICK"


def test_no_double_click_after_timeout(server):
    event(server, button=1, action="press")
    time.sleep(0.05)
    event(server, button=1, action="release")
    time.sleep(0.6)                            # больше double_click_window
    event(server, button=1, action="press")
    time.sleep(0.05)
    res = event(server, button=1, action="release")
    assert res.get("event") == "SHORT_CLICK"   # не double


# ── /event — error cases ───────────────────────────────────────────────────

def test_release_without_press_returns_error(server):
    # новая кнопка которую ещё не трогали
    res = event(server, button=99, action="release")
    assert "error" in res


def test_unknown_action_returns_error(server):
    res = event(server, button=1, action="explode")
    assert "error" in res


def test_invalid_json_returns_400(server):
    r = requests.post(
        f"{server}/event",
        data="not json",
        headers={"Content-Type": "application/json"},
        timeout=3,
    )
    assert r.status_code == 400


# ── /event — multiple buttons ──────────────────────────────────────────────

def test_multiple_buttons_independent(server):
    event(server, button=10, action="press")
    event(server, button=11, action="press")

    data = requests.get(f"{server}/status", timeout=3).json()
    b10 = data["buttons"].get(10) or data["buttons"].get("10")
    b11 = data["buttons"].get(11) or data["buttons"].get("11")
    assert b10["state"] == "PRESSED"
    assert b11["state"] == "PRESSED"

    event(server, button=10, action="release")
    event(server, button=11, action="release")


def test_pod_field_present(server):
    res = event(server, button=1, action="press")
    assert "pod" in res
    event(server, button=1, action="release")