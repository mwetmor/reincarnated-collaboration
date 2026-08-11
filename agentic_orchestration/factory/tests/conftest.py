"""Make `factory` importable no matter where pytest is invoked from."""

import subprocess
import sys
from pathlib import Path

import pytest

FACTORY_DIR = Path(__file__).resolve().parents[1]
PARENT = FACTORY_DIR.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))


def _make_git_repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)

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


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """A throwaway git repo with one committed file — the substrate for tree tests."""
    return _make_git_repo(tmp_path / "repo")


@pytest.fixture
def git_repo_factory():
    """A SECOND repo at a path the caller chooses.

    Needed by Gate-2 F6, where the whole point is two declared repos whose basenames
    collide — which the single-repo fixture, fixed at `<tmp>/repo`, cannot express.
    """
    return _make_git_repo
