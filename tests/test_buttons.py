import subprocess


def run_button():
    result = subprocess.run(
        ["./test_button"],
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