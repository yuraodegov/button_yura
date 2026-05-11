"""
Unified button tests:
  - Section 1: C binary (test_runner.c) — проверяем FSM напрямую через stdout
  - Section 2: HTTP server (simulator/server.py) — проверяем Python обёртку через /event и /status

Запуск: pytest tests/test_buttons.py -v
"""

import subprocess
import os
import time
import socket
import sys
import pytest
import requests

# ── paths ──────────────────────────────────────────────────────────────────
APP_DIR       = os.path.join(os.path.dirname(__file__), "..", "app")
SIMULATOR_DIR = os.path.join(os.path.dirname(__file__), "..", "simulator")
BINARY        = os.path.join(APP_DIR, "test_button")


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session", autouse=True)
def compiled_binary():
    """Собираем C бинарник один раз на всю сессию."""
    subprocess.run(
        ["gcc", "button.c", "mocks.c", "test_runner.c", "-o", "test_button"],
        cwd=APP_DIR,
        check=True,
    )


def get_free_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def server():
    """Поднимаем Python сервер один раз на всю сессию."""
    port = get_free_port()
    env  = os.environ.copy()
    env["PORT"] = str(port)

    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        cwd=SIMULATOR_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

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

def run_binary() -> str:
    return subprocess.run(
        [BINARY], capture_output=True, text=True
    ).stdout


def event(server, button, action):
    return requests.post(
        f"{server}/event",
        json={"button": button, "action": action},
        timeout=3,
    ).json()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — C BINARY (button.c → test_runner.c)
# ══════════════════════════════════════════════════════════════════════════════

class TestCBinary:

    def test_binary_runs(self):
        assert len(run_binary()) > 0

    def test_has_start(self):
        assert "START TEST" in run_binary()

    def test_has_end(self):
        assert "END TEST" in run_binary()

    def test_no_crash(self):
        assert "Segmentation fault" not in run_binary()

    def test_process_completed(self):
        assert run_binary().strip().endswith("END TEST")

    def test_multiple_clicks(self):
        assert run_binary().count("Push button") > 1

    def test_button_fsm_flow(self):
        out = run_binary()
        assert "First press" in out
        assert "Long press"  in out
        assert "released"    in out.lower()

    def test_all_buttons_released(self):
        out = run_binary()
        assert "No. 0 Long press released" in out
        assert "No. 1 Long press released" in out
        assert "No. 2 Long press released" in out

    def test_dispense_triggered(self):
        assert "DISPENSE" in run_binary()

    def test_level_update(self):
        assert "LEVEL UPDATE" in run_binary()

    def test_hello_world(self):
        assert "HELLO WORLD" in run_binary()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — HTTP SERVER (simulator/server.py → model.py)
# ══════════════════════════════════════════════════════════════════════════════

class TestHTTPServer:

    # ── /status ──────────────────────────────────────────────────────────

    def test_status_ok(self, server):
        assert requests.get(f"{server}/status", timeout=3).status_code == 200

    def test_status_has_fields(self, server):
        data = requests.get(f"{server}/status", timeout=3).json()
        assert "buttons"                 in data
        assert "long_press_threshold_ms" in data
        assert "double_click_window_ms"  in data
        assert "pod"                     in data

    def test_status_thresholds(self, server):
        data = requests.get(f"{server}/status", timeout=3).json()
        assert data["long_press_threshold_ms"] == 1000
        assert data["double_click_window_ms"]  == 500

    # ── press ─────────────────────────────────────────────────────────────

    def test_press_returns_press_event(self, server):
        res = event(server, button=1, action="press")
        assert res.get("event")  == "PRESS"
        assert res.get("button") == 1
        event(server, button=1, action="release")

    def test_press_appears_in_status(self, server):
        event(server, button=2, action="press")
        data = requests.get(f"{server}/status", timeout=3).json()
        btn  = data["buttons"].get(2) or data["buttons"].get("2")
        assert btn["state"] == "PRESSED"
        event(server, button=2, action="release")

    def test_held_ms_increases(self, server):
        event(server, button=3, action="press")
        time.sleep(0.3)
        d1 = requests.get(f"{server}/status", timeout=3).json()
        time.sleep(0.3)
        d2 = requests.get(f"{server}/status", timeout=3).json()
        ms1 = (d1["buttons"].get(3) or d1["buttons"].get("3"))["held_ms"]
        ms2 = (d2["buttons"].get(3) or d2["buttons"].get("3"))["held_ms"]
        assert ms2 > ms1
        event(server, button=3, action="release")

    # ── click types ───────────────────────────────────────────────────────

    def test_short_click(self, server):
        event(server, button=1, action="press")
        time.sleep(0.1)
        res = event(server, button=1, action="release")
        assert res.get("event") == "SHORT_CLICK"
        assert res["duration"]  <  1.0

    def test_short_click_state_back_to_idle(self, server):
        event(server, button=1, action="press")
        time.sleep(0.1)
        event(server, button=1, action="release")
        data = requests.get(f"{server}/status", timeout=3).json()
        btn  = data["buttons"].get(1) or data["buttons"].get("1")
        assert btn["state"]   == "IDLE"
        assert btn["held_ms"] is None

    def test_long_click(self, server):
        event(server, button=1, action="press")
        time.sleep(1.1)
        res = event(server, button=1, action="release")
        assert res.get("event")    == "LONG_CLICK"
        assert res.get("duration") >= 1.0

    def test_double_click(self, server):
        event(server, button=1, action="press")
        time.sleep(0.05)
        event(server, button=1, action="release")
        time.sleep(0.1)
        event(server, button=1, action="press")
        time.sleep(0.05)
        res = event(server, button=1, action="release")
        assert res.get("event") == "DOUBLE_CLICK"

    def test_no_double_click_after_timeout(self, server):
        event(server, button=1, action="press")
        time.sleep(0.05)
        event(server, button=1, action="release")
        time.sleep(0.6)
        event(server, button=1, action="press")
        time.sleep(0.05)
        res = event(server, button=1, action="release")
        assert res.get("event") == "SHORT_CLICK"

    # ── error cases ───────────────────────────────────────────────────────

    def test_release_without_press_returns_error(self, server):
        res = event(server, button=99, action="release")
        assert "error" in res

    def test_unknown_action_returns_error(self, server):
        res = event(server, button=1, action="explode")
        assert "error" in res

    def test_invalid_json_returns_400(self, server):
        r = requests.post(
            f"{server}/event",
            data="not json",
            headers={"Content-Type": "application/json"},
            timeout=3,
        )
        assert r.status_code == 400

    # ── misc ──────────────────────────────────────────────────────────────

    def test_multiple_buttons_independent(self, server):
        event(server, button=10, action="press")
        event(server, button=11, action="press")
        data = requests.get(f"{server}/status", timeout=3).json()
        b10  = data["buttons"].get(10) or data["buttons"].get("10")
        b11  = data["buttons"].get(11) or data["buttons"].get("11")
        assert b10["state"] == "PRESSED"
        assert b11["state"] == "PRESSED"
        event(server, button=10, action="release")
        event(server, button=11, action="release")

    def test_pod_field_present(self, server):
        res = event(server, button=1, action="press")
        assert "pod" in res
        event(server, button=1, action="release")