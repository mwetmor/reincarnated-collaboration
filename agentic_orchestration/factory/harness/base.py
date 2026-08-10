"""Harness interface — one shape, two lanes."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from ..usage import UsageBreakdown


@dataclass
class RawResult:
    """What a labor harness hands back. The spine never sees vendor frames directly."""

    ok: bool
    text: str = ""
    usage: UsageBreakdown = field(default_factory=lambda: UsageBreakdown.absent("not set"))
    harness: str = ""
    harness_session_id: str | None = None
    model: str | None = None
    exit_code: int | None = None
    raw_output_path: str | None = None
    prompt_path: str | None = None
    error: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


class HarnessAdapter(Protocol):
    name: str

    def run(self, prompt: str, cwd: Path, config: dict[str, Any]) -> RawResult:  # pragma: no cover
        ...


_HARNESSES: dict[str, HarnessAdapter] = {}


def register_harness(adapter: HarnessAdapter) -> HarnessAdapter:
    _HARNESSES[adapter.name] = adapter
    return adapter


def get_harness(name: str) -> HarnessAdapter:
    if name not in _HARNESSES:
        raise KeyError(f"no harness registered as {name!r}; known: {sorted(_HARNESSES)}")
    return _HARNESSES[name]


def available_harnesses() -> list[str]:
    return sorted(_HARNESSES)
