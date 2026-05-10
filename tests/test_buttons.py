import subprocess
import os
import pytest

APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
BINARY = os.path.join(APP_DIR, "test_button")


def build():
    subprocess.run(
        [
            "gcc",
            "button.c",
            "mocks.c",
            "test_runner.c",
            "-o",
            "test_button",
        ],
        cwd=APP_DIR,
        check=True,
    )


@pytest.fixture(scope="session", autouse=True)
def compiled_binary():
    build()


def run_button() -> str:
    result = subprocess.run(
        [BINARY],
        capture_output=True,
        text=True,
    )
    return result.stdout


# ── tests ──────────────────────────────────────────────────────────────────────

def test_binary_runs():
    output = run_button()
    assert len(output) > 0

def test_has_start():
    output = run_button()
    assert "START TEST" in output

def test_has_end():
    output = run_button()
    assert "END TEST" in output

def test_no_crash():
    output = run_button()
    assert "Segmentation fault" not in output

def test_process_completed():
    output = run_button()
    assert output.strip().endswith("END TEST")

def test_multiple_clicks():
    output = run_button()
    assert output.count("Push button") > 1

def test_button_fsm_flow():
    output = run_button()
    assert "First press" in output
    assert "Long press" in output
    assert "released" in output.lower()

def test_all_buttons_released():
    output = run_button()
    assert "No. 0 Long press released" in output
    assert "No. 1 Long press released" in output
    assert "No. 2 Long press released" in output

def test_dispense_triggered():
    output = run_button()
    assert "DISPENSE" in output

def test_level_update():
    output = run_button()
    assert "LEVEL UPDATE" in output

def test_hello_world():
    output = run_button()
    assert "HELLO WORLD" in output