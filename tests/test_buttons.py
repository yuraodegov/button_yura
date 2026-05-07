import subprocess
import os


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
            "test_button"
        ],
        cwd=APP_DIR,
        check=True
    )


def run_button():
    build()

    result = subprocess.run(
        [BINARY],
        capture_output=True,
        text=True
    )

    return result.stdout


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