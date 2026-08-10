"""Gate registry, report type, and run context."""

from __future__ import annotations

import os
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

PASS = "PASS"
FAIL = "FAIL"
NOT_RUNNABLE = "NOT_RUNNABLE"


class GateStatus:
    PASS = PASS
    FAIL = FAIL
    NOT_RUNNABLE = NOT_RUNNABLE


@dataclass
class GateReport:
    gate: str
    status: str
    detail: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    args: dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 0

    @property
    def is_green(self) -> bool:
        """Only PASS is green. NOT_RUNNABLE is a red, by law."""
        return self.status == PASS

    def one_line(self) -> str:
        mark = "OK  " if self.is_green else "RED "
        return f"{mark} {self.gate}: {self.status} -- {self.detail}"

    @classmethod
    def passed(cls, gate_name: str, detail: str, **evidence: Any) -> "GateReport":
        return cls(gate=gate_name, status=PASS, detail=detail, evidence=dict(evidence))

    @classmethod
    def failed(cls, gate_name: str, detail: str, **evidence: Any) -> "GateReport":
        return cls(gate=gate_name, status=FAIL, detail=detail, evidence=dict(evidence))

    @classmethod
    def not_runnable(cls, gate_name: str, reason: str, **evidence: Any) -> "GateReport":
        """The gate could not execute. This is RED, never green."""
        return cls(
            gate=gate_name,
            status=NOT_RUNNABLE,
            detail=reason,
            evidence=dict(evidence),
        )


@dataclass
class RunContext:
    """Everything a gate is allowed to know about the run it is judging."""

    run_id: str
    root: Path                                   # primary repo root (the meta-repo)
    session_dir: Path
    phase_name: str = ""
    repos: list[Path] = field(default_factory=list)   # trees whose diffs are in scope
    changed_paths: list[str] = field(default_factory=list)  # measured this phase
    prior_reports: list[GateReport] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def resolve(self, candidate: str) -> Path:
        """Resolve a declared artifact path: absolute/~ first, then root, then each tree.

        Search order is root -> repos -> extra['search_trees'] (declared read-only
        trees). First hit wins; a miss returns the root-relative path so the
        failure message names where we looked first.
        """
        p = Path(os.path.expandvars(candidate)).expanduser()
        if p.is_absolute():
            return p
        primary = self.root / p
        if primary.exists():
            return primary
        for tree in [*self.repos, *self.extra.get("search_trees", [])]:
            alt = Path(tree) / p
            if alt.exists():
                return alt
        return primary


GateFn = Callable[..., GateReport]
_REGISTRY: dict[str, GateFn] = {}


def gate(name: str) -> Callable[[GateFn], GateFn]:
    """Register a gate under `name`. Duplicate names are a build-time error."""

    def _wrap(fn: GateFn) -> GateFn:
        if name in _REGISTRY:
            raise RuntimeError(f"gate {name!r} already registered by {_REGISTRY[name]!r}")
        _REGISTRY[name] = fn
        return fn

    return _wrap


def available_gates() -> dict[str, GateFn]:
    return dict(_REGISTRY)


def run_gate(name: str, envelope: Any, run: RunContext, **args: Any) -> GateReport:
    """Execute a registered gate. Unknown gate or raised exception => RED.

    A gate that blows up has NOT passed. There is no path from an exception to a
    green verdict.
    """
    started = time.monotonic()
    fn = _REGISTRY.get(name)
    if fn is None:
        report = GateReport.not_runnable(
            name, f"no gate registered under {name!r}", known=sorted(_REGISTRY)
        )
        report.args = dict(args)
        return report
    try:
        report = fn(envelope, run, **args)
    except TypeError as exc:
        report = GateReport.not_runnable(
            name, f"gate arguments rejected: {exc}", args=dict(args)
        )
    except Exception as exc:  # noqa: BLE001 -- any failure is a red, with the trace kept
        report = GateReport.not_runnable(
            name,
            f"gate raised {type(exc).__name__}: {exc}",
            traceback=traceback.format_exc(limit=6),
        )
    report.args = dict(args)
    report.duration_ms = int((time.monotonic() - started) * 1000)
    return report
