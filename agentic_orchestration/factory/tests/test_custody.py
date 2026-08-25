"""D-10 — agent-level seam custody, made mechanical.

The rows this file exists for, in the order the ratification ranks them:

1. **THE LAW: `custody check` WRITES NOTHING.** No file changes, no telemetry, and —
   the trap `lane_status` already met once — asking does not CREATE the ledger. Held
   behaviourally by a tree fingerprint AND structurally over the call graph reachable
   from `custody_check`, because this module (unlike `lane_status`) contains three
   write verbs, so a blanket "no write mechanism in this file" scan would be a test
   that cannot fail.
2. **AMENDMENT K / the TOCTOU race.** *Check, then claim* lets two dispatchers both
   read free, both append, and both spawn — the founding incident, unprevented by the
   mechanism built to prevent it. Two rows: N concurrent claims through the real
   `flock` (exactly one wins, and every loser is TOLD WHO HOLDS IT), and a row proving
   the lock is actually on the claim path by holding it from outside.
3. **AMENDMENT L / a claim names the condition that ends it.** Refused, not defaulted —
   the same posture as the Grok harness's undeclared-vendor refusal. Plus one row per
   seam: no wildcards, no blanket rows.
4. **STALE IS NOT FREE, AND THERE IS NO TTL.** A dead holder's claim requires an
   explicit OVERRIDE with a note. An age-based auto-free is the thing this axis refuses,
   so there is a row asserting that an ancient claim with a live holder is still HELD.
5. **PID RECYCLING** (jack-ryan's Gate-2 INFO). Liveness compares PID *and* start time,
   so a recycled PID reads DEAD rather than confusing an operator mid-override.

No live agent is spawned anywhere in this file. The process table is a dict, the clock
is a string, and the lock is a real `flock` on a tmp path — because the lock is the one
thing a fake cannot stand in for.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from factory import custody as cu
from factory.lane import SerialLaneLock

FACTORY_DIR = Path(__file__).resolve().parents[1]

#: A process table with one live holder. Injected, so no test reads the real one.
LIVE = {4242: "Mon Aug 24 20:35:00 2026"}


@pytest.fixture
def ledger(tmp_path: Path) -> Path:
    return tmp_path / "agents" / "_custody.tsv"


def _row(seam, holder, event, intent="do a thing; RELEASE on the commit", detail=""):
    return cu.CustodyRow("2026-08-24T12:00:00Z", seam, holder, event, intent, detail)


def _seed(path: Path, *rows: cu.CustodyRow) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(r.to_line() + "\n" for r in rows), encoding="utf-8")
    return path


def _tree_fingerprint(root: Path) -> dict[str, str]:
    """Every file under `root`, by content digest AND mtime.

    Content alone would miss a rewrite with identical bytes; both, because the claim
    under test is *nothing changed*, not *nothing changed much*.
    """
    out: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            out[str(path.relative_to(root))] = f"{digest}:{path.stat().st_mtime_ns}"
    return out


# ===========================================================================
# 1 — THE LAW: the check emits nothing
# ===========================================================================
def test_THE_LAW_a_custody_check_changes_NOTHING_on_DISK(ledger, tmp_path):
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM))
    before = _tree_fingerprint(tmp_path)

    for _ in range(3):
        cu.custody_check("star-lord", ledger=ledger, starts=LIVE)
        cu.custody_check(ledger=ledger, starts=LIVE)

    assert _tree_fingerprint(tmp_path) == before, (
        "a READ-ONLY custody check modified the tree. A probe that writes converts a "
        "question into a side effect and walks the checker into the data path — and "
        "here the data path is the record two dispatchers use to see each other."
    )


def test_THE_LAW_asking_does_not_CREATE_the_ledger(tmp_path):
    """The `O_CREAT` trap, one level up from `lane_is_free`.

    `SerialLaneLock` opens with `O_CREAT`, so a check that took the ledger lock in order
    to read consistently would leave a ledger file behind on a host that had never made
    a claim. A ledger that does not exist holds no claims, and that answer is free.
    """
    absent = tmp_path / "never" / "_custody.tsv"
    answers = cu.custody_check("star-lord", ledger=absent)

    assert not absent.exists(), "the check CREATED a ledger that outlives the question"
    assert not absent.parent.exists(), "the check created the ledger's DIRECTORY"
    assert [a.state for a in answers] == [cu.SEAM_FREE]


def test_THE_LAW_the_check_does_not_run_PS_when_NOTHING_is_claimed(ledger):
    """No open claim, no subprocess. A seam nobody claimed cannot be held by anybody."""
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM),
          _row("star-lord", "holder-4242", cu.EVENT_RELEASE))

    def _explode() -> dict[int, str]:
        raise AssertionError("the check ran `ps` with no open claim to ask about")

    assert cu.custody_check("star-lord", ledger=ledger, scan=_explode)[0].state == cu.SEAM_FREE


def test_THE_LAW_the_CHECK_PATH_can_reach_NO_WRITE_MECHANISM(ledger):
    """Structural, over the CALL GRAPH — not over the file.

    `lane_status.py` could be scanned whole, because nothing in it writes. This module
    holds three write verbs on purpose (one file, one ledger, one vocabulary), so the
    same scan here would red on `claim` and prove nothing about `check`. Scanning only
    the functions REACHABLE FROM `custody_check` is the honest version of the claim.

    jack-ryan's Gate-2 INFO on the `lane_status` AST belt applies here unchanged: this
    is the belt, and `test_THE_LAW_a_custody_check_changes_NOTHING_on_DISK` is the
    braces. A reachability walk over names cannot see an indirect call through a
    variable — so it is not offered as a proof, only as the row that fails fast when
    somebody adds a write to the read path.
    """
    tree = ast.parse((FACTORY_DIR / "custody.py").read_text(encoding="utf-8"))
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    # `read_ledger` etc. are module-level; methods on the frozen row types are reached
    # by attribute and are covered by the behavioural row above.

    reachable: set[str] = set()
    frontier = ["custody_check"]
    while frontier:
        name = frontier.pop()
        if name in reachable or name not in functions:
            continue
        reachable.add(name)
        for node in ast.walk(functions[name]):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                frontier.append(node.func.id)

    assert "read_ledger" in reachable, (
        "the reachability walk found nothing — it is asserting over an empty set, "
        "which is the shape of a test that cannot fail"
    )
    assert "_append_row" not in reachable, "the check path reaches the ledger APPEND"
    assert "ledger_lock" not in reachable, (
        "the check path takes the ledger LOCK. Taking it would create the ledger file "
        "by `O_CREAT` and would make a question contend with a write."
    )

    mutating = {"write_text", "write_bytes", "mkdir", "touch", "unlink", "emit",
                "replace", "rename", "rmdir"}
    for name in sorted(reachable):
        called = {n.func.attr for n in ast.walk(functions[name])
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        assert not (called & mutating), (
            f"`{name}` is reachable from `custody_check` and calls "
            f"{sorted(called & mutating)} — no surviving file touch is permitted by a "
            "custody check."
        )
        opened_for_write = [
            n for n in ast.walk(functions[name])
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == "open"
            and any(isinstance(a, ast.Constant) and isinstance(a.value, str)
                    and set(a.value) & set("wax+")
                    for a in [*n.args[1:], *(k.value for k in n.keywords if k.arg == "mode")])
        ]
        assert opened_for_write == [], f"`{name}` opens a file for writing"

    imported = {alias.name for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) for alias in node.names}
    assert not (imported & {"RunLog", "Telemetry"}), (
        f"custody.py imports {sorted(imported & {'RunLog', 'Telemetry'})} — the two "
        "write mechanisms in this package. Custody is a different record from the run "
        "log, and a module that can reach both will eventually cross them."
    )


# ===========================================================================
# 2 — the derivation
# ===========================================================================
def test_an_OPEN_CLAIM_with_a_LIVE_holder_is_HELD(ledger):
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM,
                       detail="holder_started=Mon Aug 24 20:35:00 2026"))
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_HELD
    assert answer.safe_to_spawn is False
    assert answer.holder == "holder-4242"


def test_a_RELEASED_claim_is_FREE(ledger):
    _seed(ledger,
          _row("star-lord", "holder-4242", cu.EVENT_CLAIM),
          _row("star-lord", "holder-4242", cu.EVENT_RELEASE))
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].state == cu.SEAM_FREE


def test_a_RECLAIM_after_a_release_is_OPEN_again(ledger):
    _seed(ledger,
          _row("star-lord", "holder-4242", cu.EVENT_CLAIM),
          _row("star-lord", "holder-4242", cu.EVENT_RELEASE),
          _row("star-lord", "holder-4242", cu.EVENT_CLAIM))
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].state == cu.SEAM_HELD


def test_a_DEAD_holder_is_STALE_and_STALE_IS_NOT_FREE(ledger):
    _seed(ledger, _row("star-lord", "holder-9999", cu.EVENT_CLAIM))
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_STALE
    assert answer.safe_to_spawn is False, (
        "a dead holder's claim read as SPAWNABLE. Stale is not free: clearing it is an "
        "explicit OVERRIDE with a note, because the alternative — auto-free — is a "
        "timeout-based lock break, and the case it gets wrong is the live holder."
    )
    assert "override" in answer.reason


def test_a_RECYCLED_PID_reads_DEAD_not_ALIVE(ledger):
    """jack-ryan's Gate-2 INFO, mechanised.

    PIDs recycle. Without a start-time comparison, a dead session whose PID was
    reassigned reads *alive* — which fails in the FALSE-BUSY direction and is safe, but
    leaves an OVERRIDE refused for a reason that looks wrong to the operator at the
    moment the ledger most needs to make sense.
    """
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM,
                       detail="holder_started=Sun Aug 23 09:00:00 2026"))
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_STALE
    assert "RECYCLED" in answer.reason


def test_a_claim_with_NO_recorded_START_TIME_degrades_LOUDLY_not_silently(ledger):
    """The hand-append era's rows carry no start time. PID-only liveness SAYS SO."""
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM))
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_HELD
    assert "PID-only liveness" in answer.reason
    assert answer.legs["liveness"]["recorded_start"] is None


def test_a_holder_that_names_NO_PID_is_CUSTODY_UNKNOWN_never_free(ledger):
    """Measured against the LIVE ledger's own shape: `gandalf-session-53631d11`.

    Holder ids are not uniformly PID-bearing — a hex session id names no process, so
    leg 2 cannot be asked. The trailing-integer parse is ANCHORED at a separator so it
    does not answer `11` for that id: convicting an unrelated process of being the
    holder is worse than admitting we cannot tell, because the wrong answer is
    confidently `held` and the honest one is `custody-unknown`.
    """
    _seed(ledger, _row("star-lord", "gandalf-session-53631d11", cu.EVENT_CLAIM))
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_UNKNOWN
    assert answer.safe_to_spawn is False
    assert cu.holder_pid("gandalf-session-53631d11") is None
    assert cu.holder_pid("gandalf-session-85515") == 85515


def test_an_UNREADABLE_process_table_is_CUSTODY_UNKNOWN_never_free(ledger):
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM))

    def _broken() -> dict[int, str]:
        raise RuntimeError("`ps` exited 1")

    answer = cu.custody_check("star-lord", ledger=ledger, scan=_broken)[0]
    assert answer.state == cu.SEAM_UNKNOWN
    assert "`ps` exited 1" in answer.reason


def test_a_MALFORMED_row_makes_every_seam_read_OCCUPIED(ledger):
    """Fail-closed over the whole ledger, and LOUD — it is fixed by editing one line.

    A row this parser cannot read may be the CLAIM that closes the seam being asked
    about. There is no honest way to answer over a record that is partly unreadable, and
    silently skipping the row is the false-open direction.
    """
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text("2026-08-24T12:00:00Z\tstar-lord\tholder-4242\tCLAIM\n",
                      encoding="utf-8")
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_UNKNOWN
    assert "4 columns, expected 6" in answer.reason


def test_an_UNKNOWN_EVENT_is_MALFORMED_not_ignored(ledger):
    """`CUSTODY_EVENTS` is a CLOSED accept vocabulary; addition is the fail-open way."""
    _seed(ledger, _row("star-lord", "holder-4242", "SUSPEND"))
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_UNKNOWN
    assert "not one of" in answer.reason


def test_BLANK_LINES_and_COMMENTS_are_not_malformed(ledger):
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(
        "# the seam-custody ledger\n\n"
        + _row("star-lord", "holder-4242", cu.EVENT_CLAIM).to_line() + "\n\n",
        encoding="utf-8")
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].state == cu.SEAM_HELD


def test_NO_TTL_an_ANCIENT_claim_with_a_LIVE_holder_is_still_HELD(ledger):
    """The rule with the sharpest teeth, asserted rather than left to the docstring.

    A TTL is a timeout-based lock break wearing a different word. Age carries NO weight
    in this derivation: the only things that free a seam are a RELEASE row, an OVERRIDE
    row, or the holder's process ending.
    """
    ancient = cu.CustodyRow("2019-01-01T00:00:00Z", "star-lord", "holder-4242",
                            cu.EVENT_CLAIM, "a very long build; RELEASE on the commit",
                            "holder_started=Mon Aug 24 20:35:00 2026")
    _seed(ledger, ancient)
    answer = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert answer.state == cu.SEAM_HELD, (
        "an old claim with a LIVE holder was freed by its age. That is a TTL, and the "
        "case it gets wrong is a holder who is alive and mid-flight."
    )


def test_a_CHECK_with_no_seam_answers_for_EVERY_OPEN_CLAIM(ledger):
    _seed(ledger,
          _row("star-lord", "holder-4242", cu.EVENT_CLAIM),
          _row("gamora", "holder-9999", cu.EVENT_CLAIM),
          _row("rocket", "holder-4242", cu.EVENT_CLAIM),
          _row("rocket", "holder-4242", cu.EVENT_RELEASE))
    answers = cu.custody_check(ledger=ledger, starts=LIVE)
    assert {a.seam: a.state for a in answers} == {
        "star-lord": cu.SEAM_HELD, "gamora": cu.SEAM_STALE}


def test_the_ALL_view_exits_with_the_WORST_seams_code(ledger):
    _seed(ledger,
          _row("star-lord", "holder-4242", cu.EVENT_CLAIM),
          _row("gamora", "holder-9999", cu.EVENT_CLAIM))
    answers = cu.custody_check(ledger=ledger, starts=LIVE)
    assert cu.worst_exit_code(answers) == cu.CUSTODY_EXIT_CODES[cu.SEAM_STALE], (
        "the summary exit code reported the better seam. A caller reading only the exit "
        "code must never be told free while a seam is occupied."
    )


# ===========================================================================
# 3 — the vocabulary and the BAND
# ===========================================================================
def test_the_three_dispositions_PARTITION_the_answer_vocabulary():
    assert cu.SAFE_TO_SPAWN_STATES | cu.OCCUPIED_SEAM_STATES == cu.CUSTODY_STATES
    assert not (cu.SAFE_TO_SPAWN_STATES & cu.OCCUPIED_SEAM_STATES)
    assert set(cu.CUSTODY_STATE_PRECEDENCE) == cu.CUSTODY_STATES
    assert set(cu.CUSTODY_EXIT_CODES) == cu.CUSTODY_STATES, (
        "a state has no exit code, or an exit code names a state that no longer exists"
    )


def test_the_EXIT_CODES_are_BANDED_so_a_NEW_STATE_cannot_read_SPAWN_SAFE():
    """`[ $? -lt 20 ]` is the shell caller's binding to the predicate (Amendment H's
    shape, at the shell boundary, for the second axis)."""
    for state, code in cu.CUSTODY_EXIT_CODES.items():
        assert (code < 20) == cu.safe_to_spawn(state), (
            f"{state!r} exits {code}, which puts it on the wrong side of the band"
        )
    for refusal in (cu.EXIT_REFUSED, cu.EXIT_LEDGER_CONTENDED):
        assert refusal >= 20, (
            f"a refusal exits {refusal}, which reads SPAWN-SAFE to a band-checker. A "
            "refused claim is the one case where a fire-safe answer is catastrophic."
        )


def test_an_UNNAMED_state_exits_CUSTODY_UNKNOWN_never_FREE():
    assert cu.custody_exit_code("a-state-nobody-named") == cu.CUSTODY_EXIT_CODES[cu.SEAM_UNKNOWN]
    assert cu.custody_exit_code("a-state-nobody-named") >= 20


def test_the_PRECEDENCE_puts_AMBIGUITY_above_a_STATE_A_HUMAN_MUST_CLEAR():
    order = cu.CUSTODY_STATE_PRECEDENCE
    assert order.index(cu.SEAM_UNKNOWN) < order.index(cu.SEAM_STALE)
    assert order.index(cu.SEAM_STALE) < order.index(cu.SEAM_HELD)
    assert order.index(cu.SEAM_HELD) < order.index(cu.SEAM_FREE)


def test_the_two_axes_do_NOT_share_a_PREDICATE_NAME():
    """One name for two questions is Amendment J's defect wearing the opposite mask.

    The vendor lane answers *may I spend this CREDENTIAL*; custody answers *may I spawn
    into this SEAM*. They are different questions with different vocabularies, and if
    both had been called `SAFE_TO_FIRE_STATES` a consumer would eventually bind to the
    wrong one — while `test_vocabularies.py`'s name-keyed pins would have silently
    adjudicated only whichever module the walk reached last.
    """
    from factory import lane_status as ls

    assert cu.SAFE_TO_SPAWN_STATES != ls.SAFE_TO_FIRE_STATES
    assert not (cu.CUSTODY_STATES & set(ls.STATE_PRECEDENCE)), (
        "the two axes now share a state NAME, so a reader cannot tell which question a "
        "state answers"
    )


# ===========================================================================
# 4 — AMENDMENT L: a claim names the condition that ends it
# ===========================================================================
@pytest.mark.parametrize("condition", sorted(cu.VACUOUS_RELEASE_CONDITIONS - {""}))
def test_AMENDMENT_L_a_claim_whose_RELEASE_CONDITION_states_nothing_is_REFUSED(
    ledger, condition
):
    result = cu.claim(seam="star-lord", holder="holder-4242", intent="build the thing",
                      release_on=condition, ledger=ledger, starts=LIVE)
    assert result.ok is False
    assert result.exit_code == cu.EXIT_REFUSED
    assert "Amendment L" in result.reason
    assert not ledger.exists(), "a REFUSED claim created the ledger"


def test_AMENDMENT_L_the_refusal_happens_BEFORE_the_lock_is_taken(ledger, tmp_path):
    """A refused claim never holds the ledger — the Grok Amendment-E preflight's shape.

    Proven by holding the lock from outside: if the refusal ran after the acquire, this
    call would burn its whole retry budget and return CONTENDED instead of REFUSED.
    """
    _seed(ledger, _row("gamora", "holder-4242", cu.EVENT_CLAIM))
    with SerialLaneLock(ledger):
        result = cu.claim(seam="star-lord", holder="holder-4242", intent="x",
                          release_on="tbd", ledger=ledger, starts=LIVE,
                          lock_attempts=2, lock_delay_s=0.001)
    assert result.exit_code == cu.EXIT_REFUSED, (
        f"expected an argument refusal, got {result.exit_code}: {result.reason}"
    )


@pytest.mark.parametrize("seam", ["*", "star-lord,gamora", "all seams", "star lord"])
def test_AMENDMENT_L_a_WILDCARD_or_BLANKET_seam_is_REFUSED(ledger, seam):
    """One row per seam: a dispatcher checking seam X must find a row ABOUT seam X."""
    result = cu.claim(seam=seam, holder="holder-4242", intent="the whole run",
                      release_on="the run closes", ledger=ledger, starts=LIVE)
    assert result.ok is False
    assert result.exit_code == cu.EXIT_REFUSED
    assert "one row per seam" in result.reason


def test_a_RUN_SCOPED_charter_claims_its_seams_ONE_ROW_AT_A_TIME(ledger):
    """The composed door L closes, walked forwards: partial release stays expressible."""
    for seam in ("star-lord", "gamora", "rocket"):
        assert cu.claim(seam=seam, holder="holder-4242", intent=f"run U1 work on {seam}",
                        release_on=f"{seam}'s completion record lands", ledger=ledger,
                        starts=LIVE).ok

    assert cu.release(seam="gamora", holder="holder-4242", evidence="commit deadbee",
                      ledger=ledger).ok

    states = {a.seam: a.state for a in cu.custody_check(ledger=ledger, starts=LIVE)}
    assert states == {"star-lord": cu.SEAM_HELD, "rocket": cu.SEAM_HELD}, (
        "a partial release was not expressible — which is what a blanket row costs"
    )


def test_the_CLAIM_ROW_carries_its_RELEASE_CONDITION_where_a_READER_finds_it(ledger):
    result = cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
                      release_on="the completion-record commit", ledger=ledger,
                      starts=LIVE)
    assert result.ok
    assert result.row.intent == "build D-9; RELEASE on the completion-record commit"
    assert len(result.row.to_line().split("\t")) == len(cu.LEDGER_COLUMNS)


def test_the_CLAIM_records_the_HOLDERS_START_TIME_at_the_one_moment_it_can(ledger):
    result = cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
                      release_on="the commit", ledger=ledger, starts=LIVE)
    assert result.row.tokens["holder_started"] == LIVE[4242]
    # And the recorded value is what makes the recycled-PID reading possible later.
    assert cu.custody_check("star-lord", ledger=ledger,
                            starts={4242: "a different start"})[0].state == cu.SEAM_STALE


# ===========================================================================
# 5 — AMENDMENT K: the claim is ATOMIC
# ===========================================================================
def test_CLAIM_BEFORE_SPAWN_is_EXPRESSIBLE_as_an_ORDERING(ledger):
    """§ 11.3's rule, walked in order: claim, spawn, release — and the check answers
    correctly at each step, which is what makes the rule followable rather than merely
    stated. The 'spawn' is not simulated; what is asserted is that the CUSTODY answer a
    dispatcher reads is different before, during, and after."""
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].safe_to_spawn

    claimed = cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
                       release_on="the completion-record commit", ledger=ledger,
                       starts=LIVE)
    assert claimed.ok

    during = cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0]
    assert during.safe_to_spawn is False and during.state == cu.SEAM_HELD

    released = cu.release(seam="star-lord", holder="holder-4242",
                          evidence="star-lord/v1.4-custody-1", ledger=ledger)
    assert released.ok
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].safe_to_spawn

    events = [r.event for r in cu.read_ledger(ledger)[0]]
    assert events == [cu.EVENT_CLAIM, cu.EVENT_RELEASE], (
        "the ledger does not read as a claim/release PAIR, which is what makes a "
        "dispatch auditable after the fact"
    )


def test_AMENDMENT_K_TWO_CONCURRENT_CLAIMS_exactly_ONE_wins_and_losers_are_TOLD_WHO(
    ledger,
):
    """**The row Amendment K exists for.** Real threads, real `flock`, one seam.

    `SerialLaneLock` opens a FRESH descriptor per acquire, and `flock` binds to the open
    file description — so a second acquisition inside the SAME process fails, which is
    what makes threads a faithful stand-in for two dispatcher sessions here.

    Eight claimants at a barrier rather than two: with two, a scheduler could run the
    winner to completion before the loser starts, and the row would pass without ever
    exercising the lock. With eight it is contended in practice — and the assertion
    holds either way, because the exclusion is not *whoever got the lock first*. Both
    claimants serialise through the lock and RE-DERIVE the answer under it, so the
    second sees the first's row. That is a test-and-set, and it is why the loser gets a
    NAME instead of a retry.
    """
    claimants = 8
    barrier = threading.Barrier(claimants)
    results: list[cu.CustodyWrite] = []
    guard = threading.Lock()

    def _race(n: int) -> None:
        barrier.wait()
        outcome = cu.claim(
            seam="star-lord", holder=f"holder-4242", intent=f"dispatcher {n}'s build",
            release_on="the completion record", ledger=ledger, starts=LIVE,
            lock_attempts=500, lock_delay_s=0.002)
        with guard:
            results.append(outcome)

    threads = [threading.Thread(target=_race, args=(n,)) for n in range(claimants)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    winners = [r for r in results if r.ok]
    losers = [r for r in results if not r.ok]

    assert len(winners) == 1, (
        f"{len(winners)} claimants won the same seam. That is the founding incident — "
        "two dispatchers, two spawns, one build — arriving through the mechanism built "
        "to prevent it, because check-then-append without atomicity is a TOCTOU race."
    )
    assert len(losers) == claimants - 1

    rows, malformed = cu.read_ledger(ledger)
    assert malformed == [], f"concurrent appends corrupted the ledger: {malformed}"
    assert [r.event for r in rows] == [cu.EVENT_CLAIM], (
        f"the ledger carries {len(rows)} rows; exactly one CLAIM may be written"
    )

    for loser in losers:
        assert loser.exit_code >= 20, "a losing claim exited SPAWN-SAFE"
        assert loser.holder == "holder-4242" and loser.state == cu.SEAM_HELD, (
            "the loser was not told WHO holds the seam. A refusal that says only 'busy' "
            "sends a dispatcher back to the ledger to work out who to talk to — and the "
            "whole point of the axis is that two live routers see each other without a "
            "conversation."
        )
        assert "DO NOT SPAWN" in loser.reason


def test_AMENDMENT_K_the_claim_path_REALLY_TAKES_the_ledger_lock(ledger):
    """The proof that the flock is load-bearing, not decorative.

    The concurrency row above would still pass if the lock were removed and the threads
    happened to serialise. This one cannot: the lock is held from OUTSIDE, so a claim
    path that does not take it would sail through and succeed.
    """
    with SerialLaneLock(ledger):
        result = cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
                          release_on="the commit", ledger=ledger, starts=LIVE,
                          lock_attempts=3, lock_delay_s=0.001)

    assert result.ok is False, "the claim was written while the ledger lock was HELD"
    assert result.exit_code == cu.EXIT_LEDGER_CONTENDED
    assert "NOT breaking the lock" in result.reason
    assert cu.read_ledger(ledger)[0] == [], "a contended claim still appended a row"


def test_the_LEDGER_LOCK_is_taken_on_the_LEDGER_FILE_ITSELF(ledger, tmp_path):
    """Amendment K names the file, not a sidecar: `an flock on the ledger file itself`."""
    _seed(ledger, _row("gamora", "holder-4242", cu.EVENT_CLAIM))
    with cu.ledger_lock(ledger):
        with pytest.raises(Exception):
            SerialLaneLock(ledger).acquire()


def test_the_LEDGER_LOCK_never_covers_a_SUBPROCESS(ledger):
    """The claim that makes the bounded WAIT legitimate, made mechanical.

    `ledger_lock` is allowed to wait — unlike the vendor lane's lock, which never does —
    and the entire justification is *the critical section is a read plus one appended
    line: no subprocess, no spawn.* An argument like that decays into a sentence the
    moment nothing checks it, and the first version of `claim` DID run `ps` inside the
    lock: found by re-reading the module against the paragraph written about it.

    The probe is the lock itself. `flock` binds to the open file description, so a fresh
    acquire from this same process FAILS while the lock is held — which makes "is the
    ledger lock held right now?" answerable from inside the injected `ps` call.
    """
    inside_the_lock: list[bool] = []

    def _scan() -> dict[int, str]:
        try:
            probe = SerialLaneLock(ledger).acquire()
        except Exception:
            inside_the_lock.append(True)
        else:
            probe.release()
            inside_the_lock.append(False)
        return LIVE

    assert cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
                    release_on="the commit", ledger=ledger, scan=_scan).ok

    assert inside_the_lock, (
        "the process scan was never called, so this row asserted over nothing"
    )
    assert not any(inside_the_lock), (
        "`ps` ran while the ledger lock was HELD. A subprocess under the flock falsifies "
        "the bounded-critical-section argument that lets this lock wait at all, and "
        "under contention it burns every other claimant's retry budget."
    )


def test_a_CONTENDED_claim_REFUSES_rather_than_WAITING_FOREVER(ledger):
    """Bounded, and the bound is what makes waiting legitimate here at all."""
    slept: list[float] = []
    with SerialLaneLock(ledger):
        with pytest.raises(cu.LedgerContended):
            with cu.ledger_lock(ledger, attempts=4, delay_s=0.001,
                                sleep=slept.append):
                pass
    assert len(slept) == 4, "the wait was not bounded by its attempt budget"


# ===========================================================================
# 6 — release + override
# ===========================================================================
def test_a_RELEASE_cites_its_COMPLETION_EVIDENCE(ledger):
    cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
             release_on="the commit", ledger=ledger, starts=LIVE)
    result = cu.release(seam="star-lord", holder="holder-4242",
                        evidence="commit dddd232d", ledger=ledger)
    assert result.ok
    assert result.row.tokens["completion"] == "commit dddd232d"


def test_a_RELEASE_with_NO_EVIDENCE_is_REFUSED(ledger):
    cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
             release_on="the commit", ledger=ledger, starts=LIVE)
    result = cu.release(seam="star-lord", holder="holder-4242", evidence="  ",
                        ledger=ledger)
    assert result.ok is False and result.exit_code == cu.EXIT_REFUSED


def test_a_RELEASE_over_a_seam_NOBODY_HOLDS_is_REFUSED(ledger):
    result = cu.release(seam="star-lord", holder="holder-4242", evidence="commit abc",
                        ledger=ledger)
    assert result.ok is False
    assert "nothing to release" in result.reason
    assert cu.read_ledger(ledger)[0] == [], (
        "a RELEASE row that closes nothing was written. It teaches a false history to "
        "everyone who reads the ledger afterwards."
    )


def test_a_RELEASE_by_a_DIFFERENT_SESSION_is_ACCEPTED_and_RECORDED(ledger):
    """jack-ryan's Gate-2 INFO on RELEASE authorship, resolved by recording not refusing.

    The holder column names the SESSION THAT MUST BE ALIVE, not the agent — so the
    dispatcher normally writes the RELEASE when its sub-agent's completion lands, and
    that is a different string from the sub-agent. Refusing would strand every such
    claim and push routine closures through `override`, which must stay rare to stay
    meaningful.
    """
    cu.claim(seam="star-lord", holder="holder-4242", intent="build D-9",
             release_on="the commit", ledger=ledger, starts=LIVE)
    result = cu.release(seam="star-lord", holder="dispatcher-7", evidence="commit abc",
                        ledger=ledger)
    assert result.ok
    assert result.row.tokens["claimed_by"] == "holder-4242"
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].state == cu.SEAM_FREE


def test_an_OVERRIDE_clears_a_STALE_claim_and_RECORDS_WHO_it_cleared(ledger):
    _seed(ledger, _row("star-lord", "holder-9999", cu.EVENT_CLAIM))
    result = cu.override(seam="star-lord", holder="kr-4242",
                         note="holder session died mid-build; verified in `ps`",
                         ledger=ledger, starts=LIVE)
    assert result.ok
    assert result.row.tokens["cleared_holder"] == "holder-9999"
    assert result.row.tokens["note"].startswith("holder session died")
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].state == cu.SEAM_FREE


def test_an_OVERRIDE_with_NO_NOTE_is_REFUSED(ledger):
    _seed(ledger, _row("star-lord", "holder-9999", cu.EVENT_CLAIM))
    result = cu.override(seam="star-lord", holder="kr-4242", note="   ",
                         ledger=ledger, starts=LIVE)
    assert result.ok is False and result.exit_code == cu.EXIT_REFUSED
    assert "difference between this and a TTL" in result.reason
    assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].state == cu.SEAM_STALE


def test_an_OVERRIDE_over_a_LIVE_HOLDER_is_REFUSED_and_there_is_NO_FORCE(ledger):
    """Not an override — evicting somebody who is working. There is deliberately no
    `--force`: inventing one here would grant an authority nobody ratified."""
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM))
    result = cu.override(seam="star-lord", holder="kr-1", note="I want the seam",
                         ledger=ledger, starts=LIVE)
    assert result.ok is False
    assert result.exit_code == cu.CUSTODY_EXIT_CODES[cu.SEAM_HELD]
    assert "OVERRIDE clears only a STALE claim" in result.reason
    assert "force" not in json.dumps(cu.override.__doc__ or "").lower().replace(
        "no `--force`", ""), "an override force path appeared"


def test_an_OVERRIDE_over_CUSTODY_UNKNOWN_is_REFUSED(ledger):
    """We cannot SHOW the holder dead. An override on a leg we could not read is a lock
    break with extra steps."""
    _seed(ledger, _row("star-lord", "gandalf-session-53631d11", cu.EVENT_CLAIM))
    result = cu.override(seam="star-lord", holder="kr-1", note="probably dead",
                         ledger=ledger, starts=LIVE)
    assert result.ok is False
    assert result.exit_code == cu.CUSTODY_EXIT_CODES[cu.SEAM_UNKNOWN]


def test_an_OVERRIDE_over_a_FREE_seam_is_REFUSED(ledger):
    result = cu.override(seam="star-lord", holder="kr-1", note="tidying",
                         ledger=ledger, starts=LIVE)
    assert result.ok is False
    assert cu.read_ledger(ledger)[0] == []


def test_an_AUTO_FREE_of_a_stale_claim_DOES_NOT_EXIST(ledger):
    """The refusal stated as an absence: nothing in the module frees a seam by time.

    Asserted over the public surface rather than by reading the code, because the claim
    is *there is no such verb*, and a verb is exactly the kind of thing that gets added
    later by somebody who found the override tedious.
    """
    forbidden = [name for name in dir(cu)
                 if any(word in name.lower() for word in ("expire", "ttl", "reap", "gc"))]
    assert forbidden == [], f"a time-based clearing path exists: {forbidden}"

    _seed(ledger, _row("star-lord", "holder-9999", cu.EVENT_CLAIM))
    for _ in range(5):
        assert cu.custody_check("star-lord", ledger=ledger, starts=LIVE)[0].state == cu.SEAM_STALE


# ===========================================================================
# 7 — the CLI contract
# ===========================================================================
def _cli(*argv: str) -> int:
    from factory.cli import main

    return main(list(argv))


def test_the_CLI_exits_with_the_PINNED_per_state_code(ledger, capsys):
    _seed(ledger, _row("star-lord", "holder-9999", cu.EVENT_CLAIM))
    assert _cli("custody", "--ledger", str(ledger), "check", "--seam", "gamora") == 0
    assert _cli("custody", "--ledger", str(ledger), "check", "--seam", "star-lord") == \
        cu.CUSTODY_EXIT_CODES[cu.SEAM_STALE]


def test_the_CLI_safe_to_spawn_flag_collapses_to_ONE_BIT(ledger, capsys):
    _seed(ledger, _row("star-lord", "holder-9999", cu.EVENT_CLAIM))
    assert _cli("custody", "--ledger", str(ledger), "check", "--seam", "star-lord",
                "--safe-to-spawn") == 1
    assert _cli("custody", "--ledger", str(ledger), "check", "--seam", "gamora",
                "--safe-to-spawn") == 0


def test_the_CLI_REFUSES_a_claim_with_no_RELEASE_CONDITION_at_the_ARGPARSE_layer(ledger):
    """Required in both layers: a governance line enforced only by the CLI is one an API
    caller walks past, and a flag that DEFAULTS is a flag that gets left off."""
    with pytest.raises(SystemExit) as exc:
        _cli("custody", "--ledger", str(ledger), "claim", "--seam", "star-lord",
             "--holder", "h-4242", "--intent", "build")
    assert exc.value.code == 2
    assert not ledger.exists()


def test_the_CLI_round_trips_claim_check_release(ledger, capsys):
    assert _cli("custody", "--ledger", str(ledger), "claim", "--seam", "star-lord",
                "--holder", f"star-lord-session-{os.getpid()}", "--intent", "build D-9",
                "--release-on", "the completion-record commit") == 0
    assert _cli("custody", "--ledger", str(ledger), "check", "--seam", "star-lord") == \
        cu.CUSTODY_EXIT_CODES[cu.SEAM_HELD]
    assert _cli("custody", "--ledger", str(ledger), "release", "--seam", "star-lord",
                "--holder", f"star-lord-session-{os.getpid()}",
                "--evidence", "commit abc1234") == 0
    assert _cli("custody", "--ledger", str(ledger), "check", "--seam", "star-lord") == 0

    out = capsys.readouterr().out
    assert "CLAIMED" in out and "RELEASED" in out


def test_the_CLI_json_answer_carries_the_PREDICATE_and_the_CODES(ledger, capsys):
    _seed(ledger, _row("star-lord", "holder-4242", cu.EVENT_CLAIM))
    _cli("custody", "--ledger", str(ledger), "--json", "check", "--seam", "star-lord")
    payload = json.loads(capsys.readouterr().out)
    assert payload["safe_to_spawn_states"] == sorted(cu.SAFE_TO_SPAWN_STATES)
    assert payload["exit_codes"] == cu.CUSTODY_EXIT_CODES
    assert payload["seams"][0]["state"] in cu.CUSTODY_STATES


def test_the_LIVE_process_scan_returns_PID_AND_START_TIME():
    """One real `ps`, no vendor, no agent. The one leg a fake cannot stand in for."""
    starts = cu.scan_process_starts()
    assert os.getpid() in starts, "the checking process is not in its own process table"
    assert starts[os.getpid()].strip(), "a start time came back empty"


def test_scan_process_starts_RAISES_when_ps_FAILS_rather_than_reporting_EMPTY():
    """An empty table and an unanswerable question are different facts.

    Conflating them makes every holder read DEAD at exactly the moment we cannot see —
    and `dead` is the state that unlocks `override`, so the conflation would hand out
    the seam-clearing verb on a broken instrument.
    """
    def _failed(argv):
        return subprocess.CompletedProcess(argv, 1, "", "ps: illegal option")

    with pytest.raises(RuntimeError, match="exited 1"):
        cu.scan_process_starts(runner=_failed)
