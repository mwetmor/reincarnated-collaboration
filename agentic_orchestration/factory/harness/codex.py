"""Codex CLI adapter — F2, honestly stubbed.

Ruling D2 authorizes the Codex lane; Matt action **T16** (ChatGPT subscription +
Codex CLI + login) blocks it. The interface is pinned NOW so the F2 pilot is a
body-fill rather than a redesign, and the body raises rather than pretending.

This is the ONLY stub in the tree, it is in an adapter, and it declares itself.
A stub in a gate would be observability theater; a stub here is a lane that
honestly says it is not open yet.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import RawResult, register_harness

HONEST_STUB = True
BLOCKED_ON = "T16 — Matt action: ChatGPT subscription + Codex CLI install + login"


class CodexHarness:
    name = "codex"

    def run(self, prompt: str, cwd: Path, config: dict[str, Any]) -> RawResult:
        raise NotImplementedError(f"F2 — blocked on {BLOCKED_ON}")

    def available(self) -> bool:
        """The lane is not open. Callers get a truthful no, not a green."""
        return False


HARNESS = register_harness(CodexHarness())
