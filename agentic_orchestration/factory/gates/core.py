"""The v1 six — Spec A § 4.

artifacts_exist · files_non_empty · json_parses · diff_matches_claims ·
verdict_consistent · tests_pass(command)
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any

from .base import GateReport, RunContext, gate

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _normalize(paths: list[str]) -> set[str]:
    return {str(Path(p)).lstrip("./") for p in paths}


def _declared(envelope: Any, only: list[str] | None) -> list[str]:
    if only:
        return list(only)
    return list(getattr(envelope, "artifacts", []) or [])


# ---------------------------------------------------------------------------
# 1 — artifacts_exist
# ---------------------------------------------------------------------------
@gate("artifacts_exist")
def artifacts_exist(envelope: Any, run: RunContext, paths: list[str] | None = None) -> GateReport:
    """Every declared artifact path exists on disk."""
    declared = _declared(envelope, paths)
    if not declared:
        return GateReport.not_runnable(
            "artifacts_exist",
            "the envelope declared no artifacts, so there is nothing to verify "
            "(declare paths: [] explicitly in the gate args if a phase truly writes nothing)",
        )
    missing = [p for p in declared if not run.resolve(p).exists()]
    if missing:
        return GateReport.failed(
            "artifacts_exist",
            f"{len(missing)} of {len(declared)} declared artifact(s) do not exist",
            missing=missing,
            declared=declared,
        )
    return GateReport.passed(
        "artifacts_exist",
        f"all {len(declared)} declared artifact(s) exist",
        declared=declared,
    )


# ---------------------------------------------------------------------------
# 2 — files_non_empty
# ---------------------------------------------------------------------------
@gate("files_non_empty")
def files_non_empty(envelope: Any, run: RunContext, paths: list[str] | None = None) -> GateReport:
    """No zero-byte deliverables. A missing file is also a red here."""
    declared = _declared(envelope, paths)
    if not declared:
        return GateReport.not_runnable(
            "files_non_empty", "no declared artifacts to size-check"
        )
    empty: list[str] = []
    absent: list[str] = []
    sizes: dict[str, int] = {}
    for p in declared:
        resolved = run.resolve(p)
        if not resolved.exists():
            absent.append(p)
            continue
        size = resolved.stat().st_size
        sizes[p] = size
        if size == 0:
            empty.append(p)
    if empty or absent:
        return GateReport.failed(
            "files_non_empty",
            f"{len(empty)} zero-byte and {len(absent)} absent deliverable(s)",
            empty=empty,
            absent=absent,
            sizes=sizes,
        )
    return GateReport.passed(
        "files_non_empty",
        f"all {len(declared)} deliverable(s) carry bytes (smallest {min(sizes.values())} B)",
        sizes=sizes,
    )


# ---------------------------------------------------------------------------
# 3 — json_parses
# ---------------------------------------------------------------------------
@gate("json_parses")
def json_parses(envelope: Any, run: RunContext, paths: list[str] | None = None) -> GateReport:
    """Declared JSON artifacts parse. Selects *.json / *.jsonl when paths are not pinned."""
    declared = _declared(envelope, paths)
    targets = (
        list(paths)
        if paths
        else [p for p in declared if p.endswith(".json") or p.endswith(".jsonl")]
    )
    if not targets:
        return GateReport.not_runnable(
            "json_parses",
            "no JSON artifact among the declared paths -- pin `paths:` if one was expected",
            declared=declared,
        )
    broken: dict[str, str] = {}
    parsed: dict[str, str] = {}
    for p in targets:
        resolved = run.resolve(p)
        if not resolved.exists():
            broken[p] = "file does not exist"
            continue
        try:
            text = resolved.read_text(encoding="utf-8")
            if p.endswith(".jsonl"):
                count = 0
                for lineno, line in enumerate(text.splitlines(), 1):
                    if line.strip():
                        json.loads(line)
                        count += 1
                parsed[p] = f"{count} JSONL record(s)"
            else:
                doc = json.loads(text)
                parsed[p] = type(doc).__name__
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            broken[p] = str(exc)
    if broken:
        return GateReport.failed(
            "json_parses",
            f"{len(broken)} of {len(targets)} JSON artifact(s) failed to parse",
            broken=broken,
            parsed=parsed,
        )
    return GateReport.passed(
        "json_parses", f"all {len(targets)} JSON artifact(s) parse", parsed=parsed
    )


# ---------------------------------------------------------------------------
# 4 — diff_matches_claims
# ---------------------------------------------------------------------------
@gate("diff_matches_claims")
def diff_matches_claims(
    envelope: Any, run: RunContext, ignore: list[str] | None = None
) -> GateReport:
    """The measured git change-set must be a SUBSET of what the envelope claims.

    An unclaimed write is the failure mode this gate exists for: the phase
    touched something it did not tell us about. `run.changed_paths` is measured
    by the permissions fingerprint (before/after), not asked for.
    """
    claimed = _normalize(getattr(envelope, "artifacts", []) or [])
    ignore_set = _normalize(ignore or [])
    measured = _normalize(run.changed_paths)
    unclaimed = sorted(measured - claimed - ignore_set)
    phantom = sorted(claimed - measured - ignore_set)
    if unclaimed:
        return GateReport.failed(
            "diff_matches_claims",
            f"{len(unclaimed)} path(s) changed on disk that the envelope never claimed",
            unclaimed=unclaimed,
            claimed=sorted(claimed),
            measured=sorted(measured),
        )
    return GateReport.passed(
        "diff_matches_claims",
        f"change-set ({len(measured)} path(s)) is a subset of the {len(claimed)} claimed"
        + (f"; {len(phantom)} claimed path(s) showed no git delta" if phantom else ""),
        measured=sorted(measured),
        claimed=sorted(claimed),
        claimed_without_delta=phantom,
    )


# ---------------------------------------------------------------------------
# 5 — verdict_consistent
# ---------------------------------------------------------------------------
@gate("verdict_consistent")
def verdict_consistent(envelope: Any, run: RunContext) -> GateReport:
    """A PASS envelope standing over red gates is itself a red.

    Runs last: it reads the reports accumulated so far in this phase.
    """
    claimed_status = getattr(envelope, "status", None)
    reds = [r for r in run.prior_reports if not r.is_green]
    red_names = [f"{r.gate}:{r.status}" for r in reds]
    if claimed_status == "PASS" and reds:
        return GateReport.failed(
            "verdict_consistent",
            f"envelope claims PASS over {len(reds)} red gate(s): {', '.join(red_names)}",
            claimed=claimed_status,
            reds=red_names,
        )
    if claimed_status in (None, ""):
        return GateReport.not_runnable(
            "verdict_consistent", "no envelope status to compare gate outcomes against"
        )
    if claimed_status != "PASS" and not reds:
        return GateReport.passed(
            "verdict_consistent",
            f"envelope claims {claimed_status} and no gate contradicts it "
            "(a self-declared shortfall is consistent, and the phase is still not a PASS)",
            claimed=claimed_status,
        )
    return GateReport.passed(
        "verdict_consistent",
        f"envelope claims {claimed_status} and all {len(run.prior_reports)} prior gate(s) are green",
        claimed=claimed_status,
    )


# ---------------------------------------------------------------------------
# 6 — tests_pass(command)
# ---------------------------------------------------------------------------
_FAILURE_MARKERS = (
    "FAILED",
    "ERROR",
    "error:",
    "Error:",
    "assert",
    "Traceback",
    "failed",
    "FAIL",
    "E   ",
)


def _failures_only(stdout: str, stderr: str, max_lines: int = 60) -> list[str]:
    """Extract the failing lines. Passing output NEVER travels into a later prompt."""
    lines: list[str] = []
    for stream in (stdout, stderr):
        for line in stream.splitlines():
            if any(marker in line for marker in _FAILURE_MARKERS):
                lines.append(line.rstrip())
    if not lines:
        tail = [ln.rstrip() for ln in (stdout + "\n" + stderr).splitlines() if ln.strip()]
        lines = tail[-10:]
    return lines[:max_lines]


def _gate_env() -> dict[str, str]:
    """The environment a gate command runs under.

    `PYTHONDONTWRITEBYTECODE` is containment, not tidiness. A gate that runs pytest
    inside a tree the workflow declares READ-ONLY writes `__pycache__` there, and the
    fingerprint — correctly — reports it as a write to a read-only tree. The v1 build
    never saw this because gitignored paths were exempt as a category; closing that
    hole (Gate-2 F1) made the interpreter's own side effect into a real breach.

    The right fix is to stop the write, not to re-exempt the path: a read-only claim
    that quietly tolerates one class of write is not a read-only claim. Suppressing
    bytecode caching costs a few hundred milliseconds of re-compilation per gate.

    `PYTEST_ADDOPTS=-p no:cacheprovider` closes the same hole for pytest's own
    `.pytest_cache/`.
    """
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    addopts = env.get("PYTEST_ADDOPTS", "")
    if "no:cacheprovider" not in addopts:
        env["PYTEST_ADDOPTS"] = f"{addopts} -p no:cacheprovider".strip()
    return env


#: Characters that mean something to a shell and nothing to `execve`. A gate holding
#: one of these was written expecting a shell it does not get.
_SHELL_METACHARACTERS = ("&&", "||", ";", "|", ">", "<", "$(", "`")


def _shell_metacharacters(command: str) -> set[str]:
    """Which shell operators appear OUTSIDE quotes in this command.

    Gates run as argv with no shell, which is the right design — no quoting bugs, no
    injection surface. The silent degradation is not: `cd X && git mv …` resolves to
    `/usr/bin/cd`, which accepts the remaining words as arguments, exits 0, and the
    gate reports PASS for a command that did nothing. A green that measures nothing
    is the exact shape the falsification wall exists to end (Gate-2 L5).

    Quoted occurrences are EXCLUDED: `grep -c ';' file` is a legitimate argv gate and
    refusing it would make this a nuisance rather than a guard.

    The question is therefore "does an operator appear OUTSIDE quotes", and it is
    asked directly, by deleting the quoted spans and looking at what is left. Two
    tidier-looking routes were tried and both answer a different question: the posix
    `shlex.split` strips quotes, so `';'` and `;` both arrive as the token `;` (false
    positive on the grep above); the non-posix split keeps them but will not break
    `a;b` into tokens at all (false negative). Asking the convenient question instead
    of the intended one is the entire subject of this review, and it does not get to
    happen in the fix for L5.

    A backslash-escaped quote inside a gate command would be mis-tracked here and the
    result is a spurious `not_runnable` — the refusing direction, which is the one
    this may be wrong in.
    """
    unquoted, quote = [], None
    for ch in command:
        if quote is not None:
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            continue
        unquoted.append(ch)
    bare = "".join(unquoted)
    return {op for op in _SHELL_METACHARACTERS if op in bare}


def _exec_verdict(
    gate_name: str,
    run: RunContext,
    command: str | None,
    cwd: str | None,
    timeout_s: int,
) -> GateReport:
    """Run a command; the exit code is the verdict. Only failures travel.

    On green, the evidence records the exit code and the output's shape -- not the
    output. Feeding a passing suite back into context is how a run drowns itself.
    """
    if not command:
        return GateReport.not_runnable(
            gate_name, "no `command` argument supplied -- nothing to run"
        )
    workdir = Path(os.path.expandvars(cwd)).expanduser() if cwd else run.root
    if not workdir.exists():
        return GateReport.not_runnable(
            gate_name, f"cwd {workdir} does not exist", cwd=str(workdir)
        )
    argv = shlex.split(command)
    bad = _shell_metacharacters(command)
    if bad:
        return GateReport.not_runnable(
            gate_name,
            f"the command holds shell metacharacters {sorted(bad)} but gates run as "
            "ARGV with no shell, so they would be passed to "
            f"{argv[0]!r} as literal arguments rather than interpreted. "
            "`cd X && pytest` becomes `/usr/bin/cd` with three extra arguments, exits "
            "0, and the gate reports PASS for a command that did nothing. Use the "
            "gate's `cwd:` argument, or a script, instead",
            command=command,
            cwd=str(workdir),
        )
    try:
        proc = subprocess.run(
            argv,
            cwd=str(workdir),
            env=_gate_env(),
            capture_output=True,
            text=True,
            timeout=timeout_s,
            stdin=subprocess.DEVNULL,
        )
    except FileNotFoundError as exc:
        return GateReport.not_runnable(
            gate_name, f"command not found: {exc}", command=command, cwd=str(workdir)
        )
    except subprocess.TimeoutExpired:
        return GateReport.failed(
            gate_name,
            f"command exceeded {timeout_s}s and was killed",
            command=command,
            cwd=str(workdir),
        )
    if proc.returncode == 0:
        stdout_lines = len(proc.stdout.splitlines())
        return GateReport.passed(
            gate_name,
            f"`{command}` exited 0",
            command=command,
            cwd=str(workdir),
            exit_code=0,
            stdout_lines=stdout_lines,
            note="passing output deliberately not retained (only-failures-travel)",
        )
    return GateReport.failed(
        gate_name,
        f"`{command}` exited {proc.returncode}",
        command=command,
        cwd=str(workdir),
        exit_code=proc.returncode,
        failures=_failures_only(proc.stdout, proc.stderr),
    )


@gate("tests_pass")
def tests_pass(
    envelope: Any,
    run: RunContext,
    command: str | None = None,
    cwd: str | None = None,
    timeout_s: int = 1800,
) -> GateReport:
    """The headless test wall: run the suite, exit code is the verdict."""
    return _exec_verdict("tests_pass", run, command, cwd, timeout_s)


@gate("command_succeeds")
def command_succeeds(
    envelope: Any,
    run: RunContext,
    command: str | None = None,
    cwd: str | None = None,
    timeout_s: int = 1800,
) -> GateReport:
    """The mechanical-cell exec primitive -- same verdict rule, different intent.

    This is what a render/promote step runs under (R-BR-56's promotion half), so
    that the write lands inside the phase window and passes through permissions
    fingerprinting. Distinct from `tests_pass` only in what it says about itself;
    both are falsification-tested independently.
    """
    return _exec_verdict("command_succeeds", run, command, cwd, timeout_s)
