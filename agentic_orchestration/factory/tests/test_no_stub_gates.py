"""Zero stub gates — Spec A § 11, acceptance item 3, made grep-provable.

The strategy imports SSSF's mechanisms but refuses its gaps, and the loudest
refused gap is the stub gate: a checker that returns green because nobody wrote
it yet. This file is the mechanical proof that none exists.

Three independent proofs, because "no stubs" fails in three different ways:

1. **Marker scan** — no TODO/FIXME/stub/NotImplementedError anywhere in the
   gate tree, and — since 2026-08-24 — nowhere in the factory at all. The one
   declared exception was the Codex adapter, permitted while Matt action T16
   blocked the lane on terms it had to state and honour (declare itself, and
   RAISE rather than return green). T16 is done and the lane is live, so the
   carve-out is gone WITH the thing it forgave rather than outliving it. An
   exemption for a condition that has passed is an exemption nobody maintains.
2. **Red-path proof** — every registered gate's own source contains a path to
   `failed` or `not_runnable`. A gate that can only return `passed` is a stub
   wearing a gate's name.
3. **Evidence proof** — every gate touches the world (disk, subprocess, or the
   measured change-set). A gate that reads only the envelope is taking the
   agent's word, which is the thing gates exist to refuse.
"""

import inspect
import io
import re
import tokenize
from pathlib import Path

from factory.gates import available_gates

FACTORY_DIR = Path(__file__).resolve().parents[1]
GATES_DIR = FACTORY_DIR / "gates"

STUB_MARKERS = (
    "TODO",
    "FIXME",
    "XXX",
    "NotImplementedError",
    "raise NotImplemented",
    "not implemented",
    "placeholder",
    "for now, return",
)

#: There is no declared stub in this tree any more. This used to be
#: `HONEST_STUB_MODULE = harness/codex.py`, and the row below used to assert
#: `flagged == [HONEST_STUB_MODULE]`. Now it asserts `flagged == []`, which is the
#: same row with the exemption removed rather than a different row — the direction
#: matters, because relaxing this to a membership test would let the next stub in.
NO_STUB_MODULES: list[Path] = []


def _python_files(root: Path) -> list[Path]:
    return [p for p in sorted(root.rglob("*.py")) if "__pycache__" not in p.parts]


def _code_lines(path: Path) -> list[tuple[int, str]]:
    """Source with string literals blanked, comments KEPT.

    Prose is not a stub. These modules describe the no-stub law in their
    docstrings, and a scan that cannot tell a law from its violation would
    force the law to go unwritten. Comments survive the blanking on purpose:
    `# TODO: make this actually check something` is exactly the thing to catch.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    blanked = list(lines)
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except tokenize.TokenError:  # pragma: no cover - unparseable source fails elsewhere
        return list(enumerate(lines, 1))
    for tok in tokens:
        if tok.type != tokenize.STRING:
            continue
        (srow, scol), (erow, ecol) = tok.start, tok.end
        for row in range(srow, erow + 1):
            line = blanked[row - 1]
            start = scol if row == srow else 0
            end = ecol if row == erow else len(line)
            blanked[row - 1] = line[:start] + " " * (end - start) + line[end:]
    return list(enumerate(blanked, 1))


def _code_text(path: Path) -> str:
    return "\n".join(line for _, line in _code_lines(path))


# ---------------------------------------------------------------------------
# 1 — marker scan
# ---------------------------------------------------------------------------
def test_gate_tree_carries_no_stub_markers():
    offenders: list[str] = []
    for path in _python_files(GATES_DIR):
        for lineno, line in _code_lines(path):
            for marker in STUB_MARKERS:
                if marker.lower() in line.lower():
                    offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, "stub markers found in the gate tree:\n" + "\n".join(offenders)


def test_there_is_NO_stub_left_in_the_factory():
    """The carve-out is gone with the thing it forgave.

    While the Codex lane was blocked on T16 this asserted `flagged == [codex.py]`.
    T16 is done and the lane is live, so the equality target is the EMPTY list —
    the same row, one exemption smaller. It is still an equality and not a
    membership test, because `in` cannot tell a shorter list from a longer one.
    """
    flagged: list[Path] = []
    for path in _python_files(FACTORY_DIR):
        if "tests" in path.parts:
            continue
        if "NotImplementedError" in _code_text(path):
            flagged.append(path)
    assert flagged == NO_STUB_MODULES, (
        "NotImplementedError may appear in NO module of this package; found it in "
        f"{[str(p.relative_to(FACTORY_DIR)) for p in flagged]}. There is no longer a "
        "declared-stub exemption to add one to."
    )


def test_the_codex_lane_no_longer_declares_itself_closed():
    """The stub markers are DELETED, not left lying next to a working body.

    A `HONEST_STUB = True` beside a live `run()` is worse than either half alone: it
    tells its reader the lane is shut while the lane executes jobs. This row is what
    stops the markers being re-added out of habit, and what stops a future reader
    trusting `BLOCKED_ON` after the block was lifted.
    """
    from factory.harness import codex

    assert not hasattr(codex, "HONEST_STUB"), (
        "`HONEST_STUB` is back in a module with a live body. If the lane closes again, "
        "it closes through `available()`/`unavailable_reason()`, which report the "
        "CURRENT state — a module constant fixed at import time cannot."
    )
    assert not hasattr(codex, "BLOCKED_ON")


# ---------------------------------------------------------------------------
# 2 — red-path proof
# ---------------------------------------------------------------------------
def test_every_gate_has_a_reachable_red_path():
    """A gate whose source cannot produce FAIL or NOT_RUNNABLE is a stub."""
    stubs: list[str] = []
    for name, fn in available_gates().items():
        source = inspect.getsource(fn)
        # `tests_pass` / `command_succeeds` delegate to a shared executor; follow it.
        if "_exec_verdict(" in source:
            from factory.gates import core

            source += inspect.getsource(core._exec_verdict)
        has_red = "GateReport.failed(" in source or "GateReport.not_runnable(" in source
        if not has_red:
            stubs.append(name)
    assert not stubs, f"gate(s) with no reachable red verdict: {stubs}"


def test_no_gate_returns_a_bare_unconditional_pass():
    """The first statement of a gate is never `return GateReport.passed(...)`."""
    offenders: list[str] = []
    for name, fn in available_gates().items():
        body = inspect.getsource(fn)
        # strip decorator, signature and docstring, then look at what comes first
        stripped = re.sub(r'"""(?:.|\n)*?"""', "", body)
        lines = [
            ln.strip()
            for ln in stripped.splitlines()
            if ln.strip() and not ln.strip().startswith(("@", "#"))
        ]
        # drop the def line(s) up to the closing paren of the signature
        while lines and not lines[0].endswith(":"):
            lines.pop(0)
        if lines:
            lines.pop(0)
        if lines and lines[0].startswith("return GateReport.passed"):
            offenders.append(name)
    assert not offenders, f"gate(s) that pass unconditionally: {offenders}"


# ---------------------------------------------------------------------------
# 3 — evidence proof
# ---------------------------------------------------------------------------
WORLD_TOUCHING = (
    "run.resolve(",          # reads a path off disk
    "subprocess.run(",       # runs a real command
    "_exec_verdict(",        # delegates to the real command executor
    "run.changed_paths",     # reads the measured fingerprint change-set
    "run.prior_reports",     # reads other gates' measured verdicts
    ".exists()",
    ".stat()",
    "read_bytes()",
    "read_text(",
)


def test_every_gate_consults_something_other_than_the_envelope():
    """Post-hoc claim gates adjudicate the world, never the envelope's word."""
    envelope_only: list[str] = []
    for name, fn in available_gates().items():
        source = inspect.getsource(fn)
        if not any(marker in source for marker in WORLD_TOUCHING):
            envelope_only.append(name)
    assert not envelope_only, (
        f"gate(s) that only read the envelope: {envelope_only}. A gate that takes "
        "the agent's word is not a gate."
    )


def test_not_runnable_is_red_everywhere_it_is_constructed():
    """No module may treat NOT_RUNNABLE as green by comparing against FAIL alone."""
    from factory.gates.base import GateReport

    assert GateReport.not_runnable("x", "y").is_green is False
    offenders: list[str] = []
    for path in _python_files(FACTORY_DIR):
        if "tests" in path.parts:
            continue
        for lineno, line in _code_lines(path):
            if re.search(r"status\s*[=!]=\s*FAIL\b", line):
                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, (
        "greenness must be tested as `status == PASS`, never as `!= FAIL` or "
        "`== FAIL`, or NOT_RUNNABLE silently becomes green:\n" + "\n".join(offenders)
    )
