"""Make `factory` importable no matter where pytest is invoked from."""

import subprocess
import sys
from pathlib import Path

import pytest

FACTORY_DIR = Path(__file__).resolve().parents[1]
PARENT = FACTORY_DIR.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """A throwaway git repo with one committed file — the substrate for tree tests."""
    root = tmp_path / "repo"
    root.mkdir()

    def git(*args: str) -> None:
        subprocess.run(
            ["git", *args], cwd=str(root), check=True, capture_output=True, text=True
        )

    git("init", "-q")
    git("config", "user.email", "factory-test@example.invalid")
    git("config", "user.name", "factory test")
    (root / "tracked.txt").write_text("baseline\n")
    (root / ".gitignore").write_text("ignored/\n")
    git("add", "tracked.txt", ".gitignore")
    git("commit", "-q", "-m", "baseline")
    return root
