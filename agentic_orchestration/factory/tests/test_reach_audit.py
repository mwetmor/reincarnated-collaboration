"""Gate-2 C2 — every assertion in this suite is PROVEN to execute.

The thing this replaces
-----------------------
Round eight closed jack-ryan's never-executed-assert finding with a regex that
scanned the wall for `if "<phrase>" in reason:` gates and checked the phrase still
appeared in `permissions.py`. It shipped with a sentinel, which was the right
instinct and the wrong target: the sentinel proved the regex could recognise a
phrase-gate, not that the regex could see the suite. Its scope was one file, one
quote style, one spelling of the pattern, and — measured by the mechanism below —
the assertion inside its own loop never executed once, because the scanner
collected zero phrases from the wall. A scanner that finds nothing, passing.

So this stops pattern-matching source and measures execution. Every `assert`
statement under `tests/` must be executed at least once by a full run of the suite.
That subsumes the phrase-gate check strictly: an assertion gated on a phrase the
product can no longer emit is unreachable, so no row reaches it, so it shows up
here — and so does the same defect wearing single quotes, an aliased variable, a
different file, or a shape nobody thought to write a regex for.

How it runs
-----------
The suite cannot trace itself: this test runs DURING the session whose coverage it
wants to judge. So it spawns one child run of the full suite under
`tests/_reach_tracer.py` (`sys.settrace`, line events restricted to the trees named
in `FACTORY_REACH_DIRS`, defaulting to `tests/`) and compares the executed lines
against every `ast.Assert` node in the tree.

Cost, measured on this host: 53s untraced, 55s traced — the tracer returns None for
frames outside `tests/`, which switches off line events for the product entirely.
Total suite time roughly doubles because the suite is run twice. That is the price
of the claim; it is paid once per run, not once per assertion.

In the CHILD the audit does not recurse, and it carries no branch that the child
skips: the child-run checks are DATA returned by `audit_problems`, adjudicated by a
single assertion that executes in both modes. The first version put them behind an
`else:` and the audit reported its own three assertions as unreached — correctly.
Exempting its own file would have been the self-certification this spine refuses.

Three power checks stand behind the claim, because each covers a different way for
it to be vacuous: the SENTINEL proves the tracer can tell reached from unreached,
`len(expected) > 300` proves the enumerator still finds the suite, and
`test_C2_the_comparison_reports_a_line_the_trace_does_not_contain` proves the
comparison still looks.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
FACTORY = TESTS.parent
CHILD_ENV = "FACTORY_REACH_CHILD"
IN_CHILD = bool(os.environ.get(CHILD_ENV))


def assert_lines(files: list[Path]) -> dict[str, str]:
    """Every `assert` statement in `files`, keyed `<abs path>:<line>`.

    Keyed off the AST, not a regex: an assert is a statement kind, and asking the
    parser is the only way to enumerate them that cannot be fooled by a string
    literal, a comment, or a line continuation.
    """
    found: dict[str, str] = {}
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                found[f"{path}:{node.lineno}"] = f"{path.name}:{node.lineno}"
    return found


def _traced_run(
    args: list[str], out: Path, timeout: int, trace_dir: Path = TESTS
) -> tuple[int, set[str], str]:
    env = {
        **os.environ,
        CHILD_ENV: "1",
        "FACTORY_REACH_OUT": str(out),
        "FACTORY_REACH_DIRS": str(trace_dir),
        "PYTHONPATH": f"{TESTS}{os.pathsep}{os.environ.get('PYTHONPATH', '')}",
    }
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *args, "-q", "--no-header", "--tb=no",
         "-p", "_reach_tracer", "-p", "no:cacheprovider"],
        cwd=str(FACTORY), capture_output=True, text=True, env=env, timeout=timeout,
    )
    reached = set(json.loads(out.read_text(encoding="utf-8"))) if out.exists() else set()
    return proc.returncode, reached, proc.stdout[-2000:]


SENTINEL_SRC = '''
def test_sentinel_reached():
    assert True, "REACHED"

def _never_called():
    assert False, "UNREACHED"
'''


def sentinel_verdict(tmp_path: Path) -> tuple[bool, bool]:
    """Run the tracer over a file with one reached and one unreached assert.

    Returns (reached_seen, unreached_seen). The tracer must report exactly the first.
    Without this, "no unreached assertions" and "the tracer saw nothing at all" are
    the same green — which is the defect class the whole exercise is about.
    """
    probe = tmp_path / "test_sentinel_probe.py"
    probe.write_text(SENTINEL_SRC, encoding="utf-8")
    lines = {
        node.msg.value: f"{probe.resolve()}:{node.lineno}"
        for node in ast.walk(ast.parse(SENTINEL_SRC))
        if isinstance(node, ast.Assert)
    }
    _, reached, _ = _traced_run(
        [str(probe)], tmp_path / "sentinel.json", timeout=120, trace_dir=tmp_path
    )
    return lines["REACHED"] in reached, lines["UNREACHED"] in reached


def audit_problems(tmp_path: Path, expected: dict[str, str]) -> list[str]:
    """Run the traced child and return every problem found, as text. `[]` is a pass.

    The checks here are DATA, not assertions, and that is the point. The first
    version put them in an `else:` branch — so in the child run they were three
    assert statements that never executed, and the audit reported itself. Rather
    than exempt its own file (the self-certification this spine refuses) or fabricate
    a fixture that would satisfy them (the fake-green it refuses harder), the branch
    is gone: one assertion in the caller adjudicates a list that a child run either
    fills or does not.
    """
    if IN_CHILD:
        return []
    code, reached, tail = _traced_run(["tests"], tmp_path / "reach.json", timeout=1800)
    return problems_from(code, reached, tail, expected)


def problems_from(
    code: int, reached: set[str], tail: str, expected: dict[str, str]
) -> list[str]:
    """Adjudicate one child result. Pure, so every arm has a row that reaches it.

    Round-ten mutation S7 (`if code != 0:` -> `if False:`) survived the first C2 set:
    on a green suite that branch is dead, so its only evidence was the happy path.
    A check whose failing arm nothing executes is the finding, one level up.
    """
    if code != 0:
        return [f"the traced child run of the suite was not green:\n{tail}"]
    if len(reached) <= 1000:
        return [
            f"the traced child executed the suite but recorded only {len(reached)} "
            "lines under tests/. The tracer is not attached, so its report of zero "
            "unreached assertions is a report about nothing."
        ]
    return unreached_of(expected, reached)


def test_C2_a_red_or_untraced_child_run_is_a_problem_not_a_pass():
    """Both failing arms of the child adjudication, reached without spending a run."""
    expected = {"/x/test_a.py:9": "test_a.py:9"}
    plenty = {f"/x/t.py:{i}" for i in range(2000)} | {"/x/test_a.py:9"}

    assert problems_from(0, plenty, "", expected) == [], "the green arm must be silent"
    red = problems_from(1, plenty, "boom", expected)
    assert red and "not green" in red[0] and "boom" in red[0], (
        "a child run that failed must be reported, and reported with its output — "
        "otherwise the parent certifies coverage measured by a suite that broke"
    )
    detached = problems_from(0, {"/x/test_a.py:9"}, "", expected)
    assert detached and "not attached" in detached[0], (
        "a child that recorded almost nothing has not proven coverage; it has proven "
        "the tracer was not running"
    )


def unreached_of(expected: dict[str, str], reached: set[str]) -> list[str]:
    """The comparison, alone and pure, so that it can be refuted without a child run."""
    return sorted(label for key, label in expected.items() if key not in reached)


def test_C2_the_comparison_reports_a_line_the_trace_does_not_contain():
    """The sentinel proves the TRACER has power; this proves the COMPARISON does.

    Without it, `if key not in reached` could be switched to `if False` and every
    row above would still be green — the audit would report zero unreached
    assertions because it had stopped looking, which is the failure it exists to
    name. Runs in-process against a fixed pair; costs nothing.
    """
    expected = {"/x/test_a.py:9": "test_a.py:9", "/x/test_a.py:10": "test_a.py:10"}
    assert unreached_of(expected, {"/x/test_a.py:9"}) == ["test_a.py:10"]
    assert unreached_of(expected, {"/x/test_a.py:9", "/x/test_a.py:10"}) == []


def test_C2_every_assert_under_tests_is_proven_to_execute(tmp_path):
    files = sorted(TESTS.glob("*.py"))
    assert files, f"no test modules found under {TESTS}: the audit has no subject"

    expected = assert_lines(files)
    assert len(expected) > 300, (
        f"only {len(expected)} assert statements enumerated across {len(files)} files. "
        "The suite is known to carry ~390; a collapse means the enumerator broke, and "
        "an enumerator that finds nothing passes this test trivially."
    )

    reached_seen, unreached_seen = sentinel_verdict(tmp_path)
    assert reached_seen, (
        "the tracer did not record an assert that DEFINITELY executed, so its silence "
        "about the real suite means nothing. Fix the tracer before trusting this test."
    )
    assert not unreached_seen, (
        "the tracer recorded an assert inside a function nobody called. It is reporting "
        "presence, not execution — the same measurement error it exists to catch."
    )

    problems = audit_problems(tmp_path, expected)
    assert not problems, (
        f"{len(problems)} problem(s) from the traced run of this suite:\n  "
        + "\n  ".join(problems)
        + "\n\nAn assertion that does not run is not coverage — it is a comment that "
        "reads as a check. Either give it a row that reaches it, or delete it."
    )
