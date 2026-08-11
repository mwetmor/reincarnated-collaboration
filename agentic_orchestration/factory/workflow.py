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
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .gates import available_gates
from .harness import get_harness

MAX_RETRIES = 3
FORBIDDEN_PHASE_KEYS = ("model",)

# Adjudicates the reports that ran before it, so it is only meaningful last.
LAST_GATE = "verdict_consistent"


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
        # `verdict_consistent` reads the reports accumulated BEFORE it. Anywhere but
        # last, it greens vacuously over gates it never saw (DRIFT-CRITIC D-3).
        for position, gspec in enumerate(gates):
            if gspec.gate == LAST_GATE and position != len(gates) - 1:
                raise WorkflowError(
                    f"phase {pname!r} runs `{LAST_GATE}` at position {position + 1} of "
                    f"{len(gates)}. It adjudicates the gates that ran before it, so "
                    "anywhere but last it passes over gates it never saw. Move it to the end."
                )

        agent = raw.get("agent")
        prompt = raw.get("prompt")
        harness = raw.get("harness", "claude_code")
        if agent:
            # The lane must be open BEFORE the phases ahead of it burn (D-6).
            try:
                adapter = get_harness(harness)
            except KeyError as exc:
                raise WorkflowError(
                    f"phase {pname!r} names harness {harness!r}: {exc}"
                ) from exc
            available = getattr(adapter, "available", None)
            if callable(available) and not available():
                blocked = getattr(
                    __import__(adapter.__module__, fromlist=["BLOCKED_ON"]), "BLOCKED_ON", ""
                )
                raise WorkflowError(
                    f"phase {pname!r} runs on the {harness!r} lane, which is not open"
                    + (f" — blocked on {blocked}" if blocked else "")
                    + ". A closed lane fails at LOAD, not after the phases ahead of it burn."
                )
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
    repos = [(r if r.is_absolute() else (wf_root / r)).resolve() for r in repos]
    read_only = [_expand(r).resolve() for r in (data.get("read_only_trees") or [])]
    _validate_containment(repos, read_only)

    return Workflow(
        name=name,
        path=wf_path,
        root=wf_root,
        phases=phases,
        description=data.get("description", ""),
        repos=repos,
        read_only_trees=read_only,
        on_fail=on_fail,
        sha256=hashlib.sha256(wf_path.read_bytes()).hexdigest(),
    )


def git_toplevel(path: Path) -> Path | None:
    """The worktree ROOT enclosing `path`, or None if there is no worktree at all.

    The return CODE is not the answer. `git rev-parse` succeeds from any depth
    inside a worktree, so a returncode check accepts a subdirectory — and a
    subdirectory is precisely what the fingerprinter cannot measure: `git status`
    reports paths relative to the worktree root, so every one of them would be
    joined against the wrong base and stat to nothing. The tree would fingerprint
    as `usable=True` with every signature empty, which is the F2 fail-open wearing
    a passing guard (Gate-2 re-review G1).
    """
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(path),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return Path(proc.stdout.strip()).resolve()


def _validate_containment(repos: list[Path], read_only: list[Path]) -> None:
    """Every containment claim the run will make must be *measurable* — at LOAD.

    Containment is fingerprint-based (D5 deferred sandboxes). A fingerprint of a
    non-git directory carries no change-set, so a run over one would report a clean
    diff and call it proof. That is the F2 fail-open: an unmeasurable tree must stop
    the run before it starts, not read as innocent afterwards.

    A `read_only_trees` entry that no `repos` entry covers is the same hole wearing a
    stricter label: nothing fingerprints it, so the read-only promise is never checked.
    """
    for r in repos:
        if not r.exists():
            raise WorkflowError(f"declared repo does not exist: {r}")
        if not r.is_dir():
            raise WorkflowError(f"declared repo is not a directory: {r}")
        top = git_toplevel(r)
        if top is None:
            raise WorkflowError(
                f"declared repo {r} is not a git worktree. Containment is measured by "
                "diffing the git change-set, so an untracked tree cannot be fenced — it "
                "would report clean no matter what the phase wrote to it."
            )
        if top != r:
            raise WorkflowError(
                f"declared repo {r} is a SUBDIRECTORY of the git worktree at {top}. "
                "`git status` reports paths relative to the worktree root, so every "
                "signature would be computed against the wrong base and come back "
                "empty — the tree would measure as clean whatever a phase wrote to it. "
                f"Declare `{top}` and scope the phase with `writes:` instead."
            )
    for ro in read_only:
        # F2's own sentence, applied to the half that never got the existence check
        # (Gate-2 verdict H2). A read-only tree that is not there protects nothing —
        # it is a promise about no bytes, and it loads CLEAN, which is the shape of
        # every defect this function exists to refuse. The likely cause is a typo,
        # and a typo'd read-only claim is the most dangerous kind: the author walks
        # away believing the tree they meant is fenced.
        if not ro.exists():
            raise WorkflowError(
                f"read_only tree {ro} does not exist, so declaring it protects nothing. "
                "Check the path — a misspelled read-only tree loads clean and fences "
                "nothing, while the tree you meant stays writable."
            )
        if not ro.is_dir():
            raise WorkflowError(
                f"read_only tree {ro} is not a directory. Read-only is a claim about a "
                "tree; scope a single file with `writes:` instead."
            )
        if not any(ro == r or r in ro.parents for r in repos):
            enclosing = git_toplevel(ro) if ro.is_dir() else None
            hint = (
                f" Declare `{enclosing}` in `repos` — it is the worktree root that "
                f"contains {ro}, and a repo entry must BE a worktree root."
                if enclosing
                else " It must sit inside a declared worktree root."
            )
            raise WorkflowError(
                f"read_only tree {ro} is not covered by any `repos` entry, so it is never "
                "fingerprinted and its read-only status is never enforced. (Read-only is "
                "a verdict about a measured tree, not a substitute for measuring it.)"
                + hint
            )


def _default_root(wf_path: Path) -> Path:
    """The meta-repo root: walk up from the workflow file to the enclosing git tree."""
    for parent in [wf_path, *wf_path.parents]:
        if (parent / ".git").exists():
            return parent
    return wf_path.parent
