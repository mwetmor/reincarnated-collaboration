"""sha256_matches — the digest pin, compiled.

KC2 practice: nothing downstream of a pinned artifact moves until the constant
moves BY HAND. The consumer verifies the supplier's bytes rather than taking the
supplier's word (AGENT_STATE 2026-08-09: the re-point that raised until the pin
was moved deliberately).
"""

from __future__ import annotations

import hashlib
from typing import Any

from .base import GateReport, RunContext, gate

_CHUNK = 1 << 20


def sha256_of(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(_CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


@gate("sha256_matches")
def sha256_matches(
    envelope: Any,
    run: RunContext,
    path: str | None = None,
    expected: str | None = None,
    size_bytes: int | None = None,
) -> GateReport:
    """The file at `path` must hash to `expected`. Optional exact size cross-check."""
    if not path or not expected:
        return GateReport.not_runnable(
            "sha256_matches",
            "both `path` and `expected` are required -- a digest gate with no pin is not a gate",
            path=path,
            expected=expected,
        )
    resolved = run.resolve(path)
    if not resolved.exists():
        return GateReport.failed(
            "sha256_matches", f"pinned artifact does not exist: {resolved}", path=str(resolved)
        )
    actual = sha256_of(resolved)
    actual_size = resolved.stat().st_size
    if actual != expected:
        return GateReport.failed(
            "sha256_matches",
            f"digest mismatch on {path}: expected {expected[:12]}… got {actual[:12]}…",
            path=str(resolved),
            expected=expected,
            actual=actual,
            size_bytes=actual_size,
        )
    if size_bytes is not None and actual_size != size_bytes:
        return GateReport.failed(
            "sha256_matches",
            f"digest matched but size did not: expected {size_bytes} B, got {actual_size} B",
            path=str(resolved),
            expected_size=size_bytes,
            actual_size=actual_size,
        )
    return GateReport.passed(
        "sha256_matches",
        f"{path} verified at {actual[:12]}… ({actual_size} B)",
        path=str(resolved),
        sha256=actual,
        size_bytes=actual_size,
    )
