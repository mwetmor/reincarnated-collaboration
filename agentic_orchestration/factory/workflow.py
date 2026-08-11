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
    #: Regions the author has acknowledged measure COARSE, as `repo:region` strings.
    #: Required on the agentic lane, validated against what the tree measures, and
    #: refused when it names a region that is not coarse (Gate-2 C5).
    coarse_acknowledged: list[str] = field(default_factory=list)
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
        if agent:
            # Gate-2 C3. `tools` was the ONE allowlist in this spine that failed
            # OPEN: omit it and no `--tools` / `--allowedTools` flag is emitted, so
            # the phase runs against whatever the ambient .claude/settings.json
            # permits — `claude --help` is explicit that the default is the full
            # built-in set. Every sibling allowlist here fails closed (an empty
            # `writes` breaches everything; an empty `gates` is a load error), and
            # this is the only PRE-hoc containment the agentic lane has —
            # permissions.py is entirely post-hoc detect-and-abort.
            #
            # Gate-2 F4: C3 proved the guard REFUSES WHEN ABSENT and stopped there,
            # which is a test of declaration, not of restriction. `tools: [default]`
            # is exactly the state C3 exists to prevent, reached by writing one word,
            # and it reads as diligence. So the refusal is now the HARNESS's closed
            # vocabulary, called from both entry points against the same list — the
            # loader is not allowed to have its own opinion of what a tool name is.
            validator = getattr(adapter, "validate_tools", None)
            if not callable(validator):
                raise WorkflowError(
                    f"phase {pname!r} runs on the {harness!r} lane, which publishes no "
                    "`validate_tools`. A harness that cannot say which tool names it "
                    "accepts cannot be given an allowlist — the allowlist would pass "
                    "through unchecked, which is the fail-open this refusal exists to "
                    "prevent."
                )
            try:
                validator(raw.get("tools"), f"phase {pname!r}")
            except ValueError as exc:
                raise WorkflowError(str(exc)) from exc
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

    wf = Workflow(
        name=name,
        path=wf_path,
        root=wf_root,
        phases=phases,
        description=data.get("description", ""),
        repos=repos,
        read_only_trees=read_only,
        coarse_acknowledged=list(data.get("coarse_acknowledged") or []),
        on_fail=on_fail,
        sha256=hashlib.sha256(wf_path.read_bytes()).hexdigest(),
    )
    # Gate-2 C5. Measures the trees, so it needs the constructed workflow rather than
    # the raw dict -- but it is a LOAD refusal like the ones above it, not a runtime
    # one. A lane condition enforced after the run starts is a report, not a gate.
    validate_coarse_regions_are_acknowledged(wf)
    return wf


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


def validate_coarse_regions_are_acknowledged(wf) -> None:
    """An AGENTIC phase may not silently inherit a COARSE read-only tree (Gate-2 C5).

    The COARSE tier catches creation, deletion and rename, and misses an in-place
    rewrite of an existing file. Measured on this host: the engine tree has ZERO
    coarse regions; godot has exactly `.godot/` and `Assets/Synty/`. Both are also
    gitignored, so an in-place edit there is undetected AND unrecoverable from git —
    the two weaknesses compound, which README rule 3 does not say.

    For the mechanical lane this is bounded: every path is authored by a human in a
    reviewed YAML file. The agentic lane is DEFINED by a model choosing paths, and
    rule 3 discharges the gap with a receipt caveat. A caveat is a claim to a reader,
    not a gate — so on the agentic lane the workflow must acknowledge the region by
    name, and the acknowledgement is validated against what the tree actually
    measures. Naming a region that is not coarse is also refused: an acknowledgement
    that has drifted from the tree is worse than none, because it reads as diligence.

    SCOPE. The finding was written about read-only trees; this checks every declared
    repo, which is a superset (the loader already refuses a read-only tree no repo
    covers). The narrower reading would have been the same class of defect one more
    time: an undetected in-place write is undetected wherever it lands, and in a
    WRITABLE repo it is a change `classify` never gets to see at all. Costs nothing
    today — measured on this host, the meta-repo and the engine have zero coarse
    regions and godot has exactly two.
    """
    if not any(p.agent for p in wf.phases):
        return
    from .permissions import coarse_key, fingerprint

    acknowledged = set(getattr(wf, "coarse_acknowledged", []) or [])
    measured: set[str] = set()
    for repo in wf.repos:
        # `is_root_repo` gates the factory's own runtime exemptions. Passing it wrong
        # would make `sessions/` measurable, and a bogus acknowledgement is exactly
        # what the stale branch below exists to refuse.
        fp = fingerprint(repo, is_root_repo=repo.resolve() == wf.root.resolve())
        measured.update(coarse_key(repo, region) for region in fp.coarse)

    unacknowledged = measured - acknowledged
    if unacknowledged:
        raise WorkflowError(
            "this workflow has an agentic phase and these read-only regions measure "
            f"COARSE: {sorted(unacknowledged)}. COARSE catches creation, deletion and "
            "rename but NOT an in-place rewrite of an existing file, and these regions "
            "are gitignored, so such an edit is neither detected nor recoverable from "
            "git. A model choosing its own paths is exactly the case the caveat does "
            "not cover. Either declare a narrower read-only tree, raise the scan cap "
            "for this run, or acknowledge each region by name under "
            "`coarse_acknowledged:`."
        )
    stale = acknowledged - measured
    if stale:
        raise WorkflowError(
            f"`coarse_acknowledged` names {sorted(stale)}, which do not measure COARSE. "
            "An acknowledgement that has drifted from the tree reads as diligence and "
            "certifies nothing — the class this spine keeps finding. Remove them."
        )


def _default_root(wf_path: Path) -> Path:
    """The meta-repo root: walk up from the workflow file to the enclosing git tree."""
    for parent in [wf_path, *wf_path.parents]:
        if (parent / ".git").exists():
            return parent
    return wf_path.parent
