"""Workflow config — YAML in, validated objects out. Fails at LOAD, not mid-run.

Spec A § 9. Per phase: `agent` (named seam, or null for a mechanical phase) ·
`tools` (allowlist) · `writes` (path allowlist) · `gates` (list + args) ·
`retries`.

**No `model` field in v1.** Model policy belongs to the launcher session, not to a
workflow file, and the loader rejects the key loudly rather than ignoring it.

**Retries are bounded at 3** with exponential backoff (star-lord standing rule on
every LLM call site). A config asking for more is a load error, not a warning.

PyYAML availability verified on this host (Spec A § 13 item O3: PyYAML 6.0.3,
Python 3.12.0). If it ever goes missing, `.json` workflow files load through the
same validator via the stdlib.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .gates import available_gates

MAX_RETRIES = 3
FORBIDDEN_PHASE_KEYS = ("model",)


class WorkflowError(ValueError):
    """The workflow file is not runnable. Raised at load time, before anything executes."""


@dataclass
class GateSpec:
    gate: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class PhaseSpec:
    name: str
    agent: str | None = None            # None => mechanical phase (no model invoked)
    harness: str = "claude_code"
    prompt: str | None = None
    tools: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)
    gates: list[GateSpec] = field(default_factory=list)
    retries: int = 0
    timeout_s: int = 3600
    artifacts: list[str] = field(default_factory=list)
    claim: str = ""
    notes: str = ""

    @property
    def is_mechanical(self) -> bool:
        return self.agent is None


@dataclass
class Workflow:
    name: str
    path: Path
    root: Path
    phases: list[PhaseSpec]
    description: str = ""
    repos: list[Path] = field(default_factory=list)
    read_only_trees: list[Path] = field(default_factory=list)
    on_fail: str = "stop"
    sha256: str = ""


def _expand(p: str | Path) -> Path:
    return Path(os.path.expandvars(str(p))).expanduser()


def _load_text(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        try:
            import yaml  # noqa: PLC0415 - optional dependency, checked here on purpose
        except ImportError as exc:  # pragma: no cover - host-dependent
            raise WorkflowError(
                f"PyYAML is not available on this host, so {path.name} cannot be read. "
                "Convert the workflow to .json (same schema) or install PyYAML."
            ) from exc
        return yaml.safe_load(text)
    if path.suffix == ".json":
        return json.loads(text)
    raise WorkflowError(f"unsupported workflow extension {path.suffix!r} (want .yaml/.yml/.json)")


def load_workflow(path: str | Path, root: Path | None = None) -> Workflow:
    wf_path = _expand(path).resolve()
    if not wf_path.exists():
        raise WorkflowError(f"workflow not found: {wf_path}")
    data = _load_text(wf_path)
    if not isinstance(data, dict):
        raise WorkflowError(f"{wf_path.name} must contain a mapping at the top level")

    known = available_gates()
    name = data.get("name") or wf_path.stem
    wf_root = _expand(data["root"]) if data.get("root") else (root or _default_root(wf_path))
    wf_root = wf_root.resolve()
    if not wf_root.exists():
        raise WorkflowError(f"workflow root does not exist: {wf_root}")

    raw_phases = data.get("phases")
    if not isinstance(raw_phases, list) or not raw_phases:
        raise WorkflowError(f"{wf_path.name} declares no phases")

    phases: list[PhaseSpec] = []
    seen_names: set[str] = set()
    for i, raw in enumerate(raw_phases):
        if not isinstance(raw, dict):
            raise WorkflowError(f"phase #{i + 1} is not a mapping")
        pname = raw.get("name")
        if not pname:
            raise WorkflowError(f"phase #{i + 1} has no name")
        if pname in seen_names:
            raise WorkflowError(f"duplicate phase name {pname!r}")
        seen_names.add(pname)

        for forbidden in FORBIDDEN_PHASE_KEYS:
            if forbidden in raw:
                raise WorkflowError(
                    f"phase {pname!r} sets `{forbidden}` — not a v1 workflow field. Model "
                    "policy belongs to the launcher session, not the workflow file (Spec A § 9)."
                )

        retries = int(raw.get("retries", 0))
        if retries < 0 or retries > MAX_RETRIES:
            raise WorkflowError(
                f"phase {pname!r} asks for {retries} retries; the bound is {MAX_RETRIES} "
                "(exponential backoff, then stop and report)"
            )

        raw_gates = raw.get("gates") or []
        if not isinstance(raw_gates, list):
            raise WorkflowError(f"phase {pname!r}: `gates` must be a list")
        gates: list[GateSpec] = []
        for g in raw_gates:
            if isinstance(g, str):
                gname, gargs = g, {}
            elif isinstance(g, dict) and "gate" in g:
                gname, gargs = g["gate"], dict(g.get("args") or {})
            else:
                raise WorkflowError(
                    f"phase {pname!r}: each gate is either a name or {{gate: name, args: {{}}}}"
                )
            if gname not in known:
                raise WorkflowError(
                    f"phase {pname!r} names gate {gname!r}, which is not registered. "
                    f"Known gates: {', '.join(sorted(known))}"
                )
            gates.append(GateSpec(gate=gname, args=gargs))
        if not gates:
            raise WorkflowError(
                f"phase {pname!r} declares no gates — an unadjudicated phase is a claim "
                "nobody checked"
            )

        agent = raw.get("agent")
        prompt = raw.get("prompt")
        if agent and not prompt:
            raise WorkflowError(f"phase {pname!r} names an agent but carries no `prompt`")
        if not agent and prompt:
            raise WorkflowError(
                f"phase {pname!r} carries a prompt but no agent — mechanical phases invoke "
                "no model"
            )

        phases.append(
            PhaseSpec(
                name=pname,
                agent=agent,
                harness=raw.get("harness", "claude_code"),
                prompt=prompt,
                tools=list(raw.get("tools") or []),
                writes=list(raw.get("writes") or []),
                gates=gates,
                retries=retries,
                timeout_s=int(raw.get("timeout_s", 3600)),
                artifacts=list(raw.get("artifacts") or []),
                claim=raw.get("claim", ""),
                notes=raw.get("notes", ""),
            )
        )

    on_fail = data.get("on_fail", "stop")
    if on_fail not in ("stop", "continue"):
        raise WorkflowError(f"on_fail must be 'stop' or 'continue', got {on_fail!r}")

    repos = [_expand(r) if str(r) != "." else wf_root for r in (data.get("repos") or ["."])]
    repos = [r if r.is_absolute() else (wf_root / r) for r in repos]
    read_only = [_expand(r).resolve() for r in (data.get("read_only_trees") or [])]

    return Workflow(
        name=name,
        path=wf_path,
        root=wf_root,
        phases=phases,
        description=data.get("description", ""),
        repos=[r.resolve() for r in repos],
        read_only_trees=read_only,
        on_fail=on_fail,
        sha256=hashlib.sha256(wf_path.read_bytes()).hexdigest(),
    )


def _default_root(wf_path: Path) -> Path:
    """The meta-repo root: walk up from the workflow file to the enclosing git tree."""
    for parent in [wf_path, *wf_path.parents]:
        if (parent / ".git").exists():
            return parent
    return wf_path.parent
