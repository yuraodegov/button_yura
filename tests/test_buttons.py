import subprocess
import os


APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
BINARY = os.path.join(APP_DIR, "test_button")


def build():
    """Собираем C проект перед тестами"""
    subprocess.run(
        [
            "gcc",
            "button.c",
            "mocks.c",
            "test_runner.c",
            "-o",
            "test_button"
        ],
        cwd=APP_DIR,
        check=True
    )


def run_button():
    """Собираем + запускаем бинарник"""
    build()
    result = subprocess.run(
        [BINARY],
        capture_output=True,
        text=True
    )
    return result.stdout


def test_has_output():
    output = run_button()
    assert "START TEST" in output
    assert "END TEST" in output


def test_first_press_detected():
    output = run_button()
    assert "First press" in output


def test_release_detected():
    output = run_button()
    assert "released" in output.lower()


def test_long_press_detected():
    output = run_button()
    assert "Long press" in output


def test_business_logic():
    output = run_button()
    assert "DISPENSE" in output
    assert "LEVEL UPDATE" in output