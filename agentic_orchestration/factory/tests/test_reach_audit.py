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
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

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


def subject_files(root: Path, collected: set[str]) -> list[Path]:
    """The files whose assertions must execute: everything under `root`, RECURSIVELY,
    plus every file the child actually collected.

    Gate-2 F2. This was `root.glob("*.py")` — flat — while the child runs
    `pytest tests`, which collects recursively. An assert in `tests/sub/` was
    collected by the child, never executed, and never enumerated, so the audit was
    asked about a set that omitted it and reported green. That is axis two — the
    check's ARGUMENTS — in the check that certifies the suite.

    Taking the collected set from the collector itself is the part that cannot drift:
    a pattern can disagree with pytest about what a test file is, and did.
    """
    return sorted({*root.rglob("*.py"), *(Path(c) for c in collected)})


def _traced_run(
    args: list[str], out: Path, timeout: int, trace_dir: Path = TESTS
) -> tuple[int, set[str], set[str], str]:
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
    data = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    return (
        proc.returncode,
        set(data.get("reached") or []),
        set(data.get("collected") or []),
        proc.stdout[-2000:],
    )


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
    _, reached, _, _ = _traced_run(
        [str(probe)], tmp_path / "sentinel.json", timeout=120, trace_dir=tmp_path
    )
    return lines["REACHED"] in reached, lines["UNREACHED"] in reached


def audit_problems(tmp_path: Path) -> list[str]:
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
    code, reached, collected, tail = _traced_run(
        ["tests"], tmp_path / "reach.json", timeout=1800
    )
    # The subject is re-enumerated from what the CHILD collected, not from what the
    # parent guessed before the child ran (F2).
    expected = assert_lines(subject_files(TESTS, collected))
    return problems_from(code, reached, tail, expected, collected)


def problems_from(
    code: int,
    reached: set[str],
    tail: str,
    expected: dict[str, str],
    collected: set[str],
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
    if len(collected) < 5:
        return [
            f"the child reported only {len(collected)} collected file(s). The subject "
            "of this audit is taken from the collector; a collector that reports "
            "almost nothing makes the enumeration vacuous (F2)."
        ]
    return unreached_of(expected, reached)


def test_C2_a_red_or_untraced_child_run_is_a_problem_not_a_pass():
    """Both failing arms of the child adjudication, reached without spending a run."""
    expected = {"/x/test_a.py:9": "test_a.py:9"}
    plenty = {f"/x/t.py:{i}" for i in range(2000)} | {"/x/test_a.py:9"}
    files = {f"/x/t{i}.py" for i in range(9)}

    assert problems_from(0, plenty, "", expected, files) == [], "the green arm is silent"
    red = problems_from(1, plenty, "boom", expected, files)
    assert red and "not green" in red[0] and "boom" in red[0], (
        "a child run that failed must be reported, and reported with its output — "
        "otherwise the parent certifies coverage measured by a suite that broke"
    )
    detached = problems_from(0, {"/x/test_a.py:9"}, "", expected, files)
    assert detached and "not attached" in detached[0], (
        "a child that recorded almost nothing has not proven coverage; it has proven "
        "the tracer was not running"
    )
    blind = problems_from(0, plenty, "", expected, {"/x/t0.py"})
    assert blind and "collector" in blind[0], (
        "the subject comes from the collector, so a collector reporting almost nothing "
        "makes the whole enumeration vacuous (F2)"
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


def test_C2_the_enumerator_descends_into_SUBDIRECTORIES(tmp_path):
    """F2, at the cost of a parse instead of a suite run.

    The child collects recursively; the enumerator used a flat glob. An assert in
    `tests/sub/test_x.py` was therefore collected, never executed, and never asked
    about — and the audit reported green. jack-ryan demonstrated it live. This is the
    fourth power check: the other three ask whether the tracer works and whether the
    comparison looks; this one asks whether the subject is the right SET.
    """
    nested = tmp_path / "sub" / "deeper"
    nested.mkdir(parents=True)
    (nested / "test_nested.py").write_text(
        "def _never_called():\n    assert False, 'planted'\n", encoding="utf-8"
    )
    (tmp_path / "test_top.py").write_text("def test_t():\n    assert True\n", encoding="utf-8")

    found = assert_lines(subject_files(tmp_path, set()))
    assert any("test_nested.py" in label for label in found.values()), (
        "the enumerator did not descend into a subdirectory, so an assertion living "
        f"there can never be reported unreached. Found: {sorted(found.values())}"
    )
    assert any("test_top.py" in label for label in found.values()), "flat files too"

    outside = tmp_path.parent / "collected_elsewhere.py"
    outside.write_text("def f():\n    assert False\n", encoding="utf-8")
    with_collected = assert_lines(subject_files(tmp_path, {str(outside)}))
    assert any("collected_elsewhere" in label for label in with_collected.values()), (
        "a file the CHILD collected from outside the tree is still part of the "
        "subject; the collector, not a pattern, decides what was under test"
    )


def test_C2_every_assert_under_tests_is_proven_to_execute(tmp_path):
    files = subject_files(TESTS, set())
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

    problems = audit_problems(tmp_path)
    assert not problems, (
        f"{len(problems)} problem(s) from the traced run of this suite:\n  "
        + "\n  ".join(problems)
        + "\n\nAn assertion that does not run is not coverage — it is a comment that "
        "reads as a check. Either give it a row that reaches it, or delete it."
    )


@pytest.mark.parametrize("args", [[], ["."]])
def test_the_QUARANTINE_is_not_part_of_the_suites_SUBJECT(args):
    """A breach quarantine lives INSIDE this tree and holds Python-shaped files.

    `rollback` refuses to undo some artifacts and quarantines them instead, durably, at
    `factory/sessions/<run>/breach/...`. The wall's own fenced trees contain test files,
    so the quarantine holds copies of `test_*.py` — and, from one symlink-out-of-tree
    breach, engine modules. Nothing escapes containment: the quarantine is the
    containment working. But `pytest` typed at the factory root — the obvious cwd, and
    the one a reviewer will use — walked into it and reported **33 collection errors**,
    because the suite's SUBJECT was whatever pytest's default walk happened to reach
    rather than anything this spine had said out loud.

    Two invocations, because a reviewer types both. The ablation, run rather than
    assumed: with `pytest.ini` absent, BOTH arms go red. With only `testpaths` removed,
    both stay green — so `norecursedirs` is the load-bearing exclusion, alone sufficient
    for both invocations. With only `norecursedirs` removed, the explicit `.` goes red
    and the bare call stays green, caught by `testpaths` narrowing the walk.

    `testpaths` is therefore redundant *for this row* and is kept anyway, for the reason
    the row exists: it states the subject out loud instead of leaving it to whatever
    pytest's walk happens to reach. The first draft of this docstring claimed the two
    mechanisms cover one invocation each; the ablation says otherwise, and the ablation
    is what shipped.

    This row plants an unparseable file exactly where quarantine puts things and
    requires the collection to stay clean. Asserting that `pytest.ini` merely *contains*
    the exclusion would be rule 20's defect one round after the round that named it: a
    test of declaration standing in for a test of behaviour.
    """
    planted = FACTORY / "sessions" / "_reach_probe_quarantine" / "breach" / "tree"
    planted.mkdir(parents=True, exist_ok=True)
    probe = planted / "test_unparseable_quarantined_artifact.py"
    probe.write_text("def test_(: this is not python\n", encoding="utf-8")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", *args, "--collect-only", "-q",
             "--no-header", "-p", "no:cacheprovider"],
            cwd=str(FACTORY), capture_output=True, text=True, timeout=300,
        )
    finally:
        shutil.rmtree(planted.parents[1], ignore_errors=True)
    assert probe.parent.exists() is False
    # `"error" in stdout` is NOT the predicate: `--collect-only -q` prints every test
    # NAME, and this suite contains `..._a_tree_that_errored_mid_run_...`. Substring
    # matching over collected names answers a different question than the one asked —
    # the shape this whole file exists to catch. Collection failure is an exit code (2)
    # and a counted summary line; both are asked for by name.
    summary = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    counted = re.search(r"\b(\d+)\s+errors?\b", summary)
    assert proc.returncode == 0 and not counted, (
        f"`pytest {' '.join(args)}` at the factory root reached into the quarantine.\n"
        f"exit={proc.returncode}  summary={summary!r}\n{proc.stdout[-1500:]}\n\n"
        "Quarantined artifacts are inert by intention; a tool run at the obvious "
        "directory must not treat them as the suite's subject."
    )
