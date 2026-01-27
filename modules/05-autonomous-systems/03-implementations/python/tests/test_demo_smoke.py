import subprocess
import sys
from pathlib import Path


def test_demo_smoke():
    demo_path = Path(__file__).resolve().parents[1] / "src" / "demo.py"
    result = subprocess.run(
        [sys.executable, str(demo_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    stdout = result.stdout
    assert "Example A" in stdout
    assert "G(!bad)" in stdout
    assert "Example B" in stdout
