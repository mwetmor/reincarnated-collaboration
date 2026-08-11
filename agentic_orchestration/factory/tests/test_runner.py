"""Runner-level carry-forward — what one phase is allowed to tell the next.

`only-failures-travel` governs OUTPUT: a passing phase's product never enters a
later prompt, only its shape. `notes_for_next_agent` is the deliberate exception —
it travels either way, because a handoff note is the point. That exception has a
sharp edge (DRIFT-CRITIC D-7): notes written by a phase that FAILED read exactly
like notes written by one that passed. Same field, same confident prose. The next
agent would inherit a red phase's conclusions as established fact.

So the notes travel; the verdict travels with them.
"""

from factory.envelope import EnvelopeBase
from factory.phase import FAILED, PASS
from factory.runner import PhaseOutcome, Runner


def _outcome(status: str, notes: str) -> PhaseOutcome:
    env = EnvelopeBase(status=status, summary="whatever the agent claimed")
    env.notes_for_next_agent = notes
    return PhaseOutcome(name="build", status=status, envelope=env)


def test_notes_from_a_passing_phase_travel_verbatim():
    notes = "the digest is pinned at d7ecd866; the next phase should re-point it"
    assert Runner._label_notes(_outcome(PASS, notes)) == notes


def test_notes_from_a_failed_phase_carry_their_verdict():
    notes = "the digest is pinned at d7ecd866; the next phase should re-point it"
    labelled = Runner._label_notes(_outcome(FAILED, notes))
    assert notes in labelled, "the notes still travel — this is a label, not a filter"
    assert labelled.startswith("[carried from phase `build`, which ended")
    assert FAILED in labelled
    assert "did not pass its gates" in labelled


def test_the_label_names_the_phase_it_came_from():
    """A run with several phases carries several notes. An unattributed warning is
    one the next agent cannot act on."""
    outcome = _outcome(FAILED, "something")
    outcome.name = "render_scene"
    assert "`render_scene`" in Runner._label_notes(outcome)


def test_empty_notes_from_a_failed_phase_stay_empty():
    """No notes is not the same as a warning about no notes. A label attached to
    nothing is noise in the next agent's prompt."""
    assert Runner._label_notes(_outcome(FAILED, "")) == ""
    assert Runner._label_notes(_outcome(FAILED, "   \n ")).strip() == ""


# ---------------------------------------------------------------------------
# Gate-2 F5 — the coarse acknowledgement is re-asserted DURING the run
# ---------------------------------------------------------------------------
#
# C5 put the check at LOAD, which is where it belongs and is not the only place it
# belongs. The load measurement is a snapshot, and G4's own observation — written into
# `_note_coarse`'s docstring — is that a region can cross the scan cap DURING a phase,
# including because the phase wrote enough files to push it over. That is precisely the
# case where the acknowledgement matters most, and it was the one case nobody re-asked.
#
# `_note_coarse` is called with a stub rather than through a whole agentic run: the
# agentic lane costs tokens, and the product function is the thing under test. The stub
# carries exactly the attributes the method reads, so it cannot pass by supplying
# something the real Runner does not.

import types

import pytest

from factory import permissions as perm


def _coarse_stub(acknowledged):
    said: dict = {}
    return types.SimpleNamespace(
        wf=types.SimpleNamespace(coarse_acknowledged=list(acknowledged)),
        _coarse_said=said,
        run_id=1,
        receipts=types.SimpleNamespace(event=lambda *a, **k: None),
        _say=lambda *a, **k: None,
    )


def _coarse_fp(root, region="ignored/"):
    return {str(root): perm.TreeFingerprint(root=root, head="abc", coarse=[region])}


def test_F5_an_UNACKNOWLEDGED_coarse_region_stops_an_agentic_phase_mid_run(tmp_path):
    stub = _coarse_stub([])
    with pytest.raises(perm.ContainmentError, match="does not acknowledge"):
        Runner._note_coarse(
            stub, _coarse_fp(tmp_path), phase_id=1, when="post-execution", agentic=True
        )


def test_F5_the_refusal_names_the_key_the_author_must_write(tmp_path):
    stub = _coarse_stub([])
    with pytest.raises(perm.ContainmentError) as exc:
        Runner._note_coarse(
            stub, _coarse_fp(tmp_path), phase_id=1, when="post-execution", agentic=True
        )
    assert perm.coarse_key(tmp_path, "ignored/") in str(exc.value), (
        "the refusal must hand over the exact string to acknowledge; a refusal that "
        "describes the problem without naming the fix costs a round-trip"
    )


def test_F5_an_ACKNOWLEDGED_region_passes_through(tmp_path):
    """The escape hatch is the same one C5 established, honoured at the same key."""
    stub = _coarse_stub([perm.coarse_key(tmp_path, "ignored/")])
    Runner._note_coarse(
        stub, _coarse_fp(tmp_path), phase_id=1, when="post-execution", agentic=True
    )


def test_F5_the_MECHANICAL_lane_is_untouched(tmp_path):
    """The trigger is the lane, and it is falsifiable in both directions.

    Without this row the F5 gate could be a blanket ban on coarse regions wearing a
    lane condition's error message — and the founding run, which is entirely
    mechanical over a godot tree with two coarse regions, would stop dead.
    """
    stub = _coarse_stub([])
    Runner._note_coarse(
        stub, _coarse_fp(tmp_path), phase_id=1, when="phase start", agentic=False
    )


def test_F5_a_BASENAME_acknowledgement_does_not_satisfy_the_runtime_check(tmp_path):
    """F6's key, enforced on F5's path too — one spelling, both callers."""
    stub = _coarse_stub([f"{tmp_path.name}:ignored/"])
    with pytest.raises(perm.ContainmentError):
        Runner._note_coarse(
            stub, _coarse_fp(tmp_path), phase_id=1, when="post-execution", agentic=True
        )


# ---------------------------------------------------------------------------
# Gate-2 H3 — the CALL SITES pass the trigger
#
# Every F5 row above calls `Runner._note_coarse(..., agentic=True|False)` directly:
# the TEST supplies the trigger, so the rows certify the function and say nothing
# about the wiring. jack-ryan disarmed the whole gate by rewriting
# `agentic=not spec.is_mechanical` to `agentic=False` at both call sites and the
# suite stayed green at 471 — and found a THIRD call site, post-gate, that never
# passed the argument at all, which is the last measurement of the phase and of the
# run for the final phase.
#
# So these rows go through `Runner.run()`. The trigger is not an argument they
# control; it comes from the phase's own lane, which is the point.
#
# The scenario is F5's reason for existing, made cheap: the region crosses the scan
# cap DURING the run. `_IGNORED_SCAN_CAP` is patched after LOAD, so the loader's C5
# check sees an exact region and the runtime check sees a coarse one — no fixture
# needs 50,000 files to prove the mechanism.
# ---------------------------------------------------------------------------
import json as _json
from pathlib import Path as _Path

from factory import permissions as _perm
from factory.harness.base import RawResult as _RawResult, _HARNESSES
from factory.runner import Runner as _Runner
from factory.usage import UsageBreakdown
from factory.workflow import load_workflow as _load_workflow


class _FreeHarness:
    """An agentic lane that costs nothing.

    `agentic` is `not spec.is_mechanical`, i.e. the phase names an agent — so proving
    the wiring needs a phase with an agent, and spending money to prove a containment
    trigger is how a row stops being run.
    """

    name = "free"
    validate_tools = staticmethod(lambda tools, where: [str(t) for t in (tools or [])])
    #: What the "agent" does to the tree while it runs. Set per-test so the
    #: POST-EXECUTION call site can be isolated from the other two.
    side_effect = None

    def available(self):
        return True

    def run(self, prompt, cwd, config):
        if type(self).side_effect is not None:
            type(self).side_effect(_Path(cwd))
        return _RawResult(
            ok=True,
            text=_json.dumps({"status": "PASS", "summary": "did nothing, cheaply",
                              "artifacts": [], "notes_for_next_agent": ""}),
            harness=self.name,
        )


def _h3_run(tmp_path, repo, phase, patch_cap_to=1, side_effect=None):
    """Load with the cap at its real value, run with it lowered. Returns the result."""
    _HARNESSES.setdefault("free", _FreeHarness())
    _FreeHarness.side_effect = side_effect
    doc = {"name": "h3", "root": str(repo), "repos": [str(repo)], "phases": [phase]}
    path = tmp_path / "wf.json"
    path.write_text(_json.dumps(doc, indent=2), encoding="utf-8")
    wf = _load_workflow(path)          # cap is 50_000 here: nothing is coarse yet
    original = _perm._IGNORED_SCAN_CAP
    _perm._IGNORED_SCAN_CAP = patch_cap_to
    runner = _Runner(wf, factory_dir=tmp_path / "fh", verbose=False)
    try:
        return runner.run()
    finally:
        runner.close()
        _perm._IGNORED_SCAN_CAP = original
        _FreeHarness.side_effect = None


def _coarse_abort_reason(result):
    """The abort reason, ONLY if the run stopped for the coarse-region gate.

    `status == "ABORTED"` was the first version of this assertion and it was too weak
    to mean anything: the same tree ALSO breaches (an ignored directory appearing is
    a path outside `writes`), so the row passed with the gate under test disarmed —
    aborting for a reason that had nothing to do with what the row claimed. Two
    mechanisms satisfying one assertion is the wall's own disease, in a row written
    to cure it. Returns "" when the abort was something else.
    """
    reason = str(getattr(result, "abort_reason", "") or "")
    if result.status != "ABORTED" or "COARSE" not in reason:
        return ""
    return reason


def _ignored_dir(repo, n=4):
    """An IGNORED directory with enough entries to go coarse under a lowered cap."""
    (repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    d = repo / "ignored"
    d.mkdir(exist_ok=True)
    for i in range(n):
        (d / f"f{i}").write_text(str(i), encoding="utf-8")


AGENTIC = {"name": "a", "agent": "star-lord", "harness": "free", "tools": ["Read"],
           "prompt": "do nothing", "writes": ["out/**"], "artifacts": [],
           "gates": [{"gate": "command_succeeds", "args": {"command": "true"}}]}


def test_H3_the_PHASE_START_call_site_passes_the_trigger(tmp_path, git_repo):
    """Disarming the wiring must cost a row, not nothing.

    jack-ryan's mutation (`agentic=False` at every call site) leaves the function's
    own rows green because they pass the trigger themselves. This one cannot: it
    never mentions `agentic`.
    """
    _ignored_dir(git_repo)
    reason = _coarse_abort_reason(_h3_run(tmp_path, git_repo, dict(AGENTIC)))
    assert "phase start" in reason, (
        "an agentic phase was not stopped at PHASE START by a coarse region no author "
        f"acknowledged. Abort reason was: {reason or '(not a coarse abort at all)'}"
    )


def test_H3_CONTROL_the_same_tree_on_the_MECHANICAL_lane_is_untouched(tmp_path, git_repo):
    """The trigger is the LANE, and it must be falsifiable in both directions.

    Same tree, same coarse region, no agent — and the run is not aborted by this
    check. Without this row, `agentic=True` hardcoded at every call site would pass
    the row above while being just as wrong.
    """
    _ignored_dir(git_repo)
    mech = {"name": "m", "writes": ["out/**"], "artifacts": [], "claim": "nothing",
            "gates": [{"gate": "command_succeeds", "args": {"command": "true"}}]}
    result = _h3_run(tmp_path, git_repo, mech)
    assert result.status != "ABORTED", (
        f"the mechanical lane was aborted by the agentic-lane coarse gate "
        f"({result.status}). The gate's trigger is not the lane."
    )


def test_H3_the_POST_GATE_call_site_passes_the_trigger(tmp_path, git_repo):
    """The call site that had no argument at all.

    The region does not exist at phase start or post-execution — the GATE COMMAND
    creates it, which is precisely why the post-gate snapshot exists (gates write).
    So only the third call site can catch this, and before H3 it was the one call
    site that never passed the trigger.
    """
    (git_repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    phase = dict(
        AGENTIC,
        gates=[{"gate": "command_succeeds",
                "args": {"command": "sh -c 'mkdir -p ignored && "
                                    "for i in 1 2 3 4; do echo $i > ignored/f$i; done'"}}],
    )
    reason = _coarse_abort_reason(_h3_run(tmp_path, git_repo, phase))
    assert "post-gate" in reason, (
        "a region that first went coarse DURING the gate was not caught at the "
        "post-gate snapshot — the last measurement of the phase, and of the run for "
        f"the final phase. Abort reason was: {reason or '(not a coarse abort at all)'}"
    )


def test_H3_the_POST_EXECUTION_call_site_passes_the_trigger(tmp_path, git_repo):
    """The middle call site, isolated.

    The region is created by the AGENT — the harness's own side effect — so it does
    not exist at phase start, and the post-gate snapshot would catch it only after
    post-execution had already been asked. Requiring the reason to name
    `post-execution` is what makes this row about one call site rather than about
    "some call site somewhere".
    """
    (git_repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    reason = _coarse_abort_reason(
        _h3_run(tmp_path, git_repo, dict(AGENTIC), side_effect=_ignored_dir)
    )
    assert "post-execution" in reason, (
        "a region the agent itself pushed over the cap was not caught at the "
        "post-execution snapshot — the case F5 exists for, stated in its own "
        f"docstring. Abort reason was: {reason or '(not a coarse abort at all)'}"
    )


def test_H3_the_TRIGGER_cannot_be_OMITTED_by_a_future_call_site():
    """`agentic` has no default, and until now nothing proved it.

    Round fourteen's mutation set gave the parameter a default of `True` and all 500
    rows stayed green — correctly, since all three call sites pass it explicitly, so
    the default is unreachable today. That is what makes the survivor worth a row
    rather than a shrug. `_note_coarse`'s own docstring states the rule it would have
    lost ("A required argument turns that omission into a TypeError at the call site
    rather than a gate that quietly does not apply"), and the rule was enforced by
    nothing except the fact that nobody had yet written a fourth call site. That call
    site would inherit "coarse-tier scans are agentic unless someone remembers to say
    otherwise" — the H3 finding re-entering through the door H3 closed.

    So this row is not about any existing caller. It calls the function the way a
    future caller would get it wrong. Unbound, so `self` is never touched and the
    only thing under test is the signature.
    """
    with pytest.raises(TypeError) as excinfo:
        _Runner._note_coarse(object(), {}, None, "post-gate")   # no `agentic`
    assert "agentic" in str(excinfo.value), (
        "omitting the coarse-tier trigger raised TypeError for some OTHER reason than "
        "the missing argument, so this row would keep passing if `agentic` regained a "
        f"default and would be testing nothing. TypeError was: {excinfo.value}"
    )


# ---------------------------------------------------------------------------
# H8 — what the LEDGER says a crashed agentic attempt cost.
#
# Found while debugging the H3 post-execution row, which failed for a reason that
# had nothing to do with H3: the fake harness raised, and the run's own report
# read `usage: NULL (mechanical phase — no model invoked)` for a phase whose very
# next word on the same line was `[star-lord]`. `Phase.usage`'s dataclass default
# asserted the most reassuring fact available — that nothing was spent — and the
# only code path that ever READ that default was the path where the harness died
# mid-flight, i.e. exactly where spend is least accounted for. The reason lands in
# the durable `phases.usage_absent_reason` column, so these rows read the DB and
# not the in-memory outcome: the ledger is the artifact, and the assertion should
# be made against the artifact.
#
# The rows assert the SPECIFIC reason, not merely that usage is absent. "Absent"
# is satisfied by every mechanism here at once — which is the wall's own disease,
# and the H3 post-gate row is the local precedent for refusing it.
# ---------------------------------------------------------------------------
def _ledger_absent_reason(tmp_path, phase_name="a"):
    """`usage_absent_reason` as it was WRITTEN, for the named phase."""
    import sqlite3

    conn = sqlite3.connect(str(tmp_path / "fh" / "receipts.db"))
    try:
        rows = conn.execute(
            "SELECT usage_absent_reason FROM phases WHERE name = ?", (phase_name,)
        ).fetchall()
    finally:
        conn.close()
    assert len(rows) == 1, f"expected exactly one phase row named {phase_name!r}, got {rows}"
    return rows[0][0] or ""


def _raises(_repo):
    raise RuntimeError("the harness died with the model in flight")


def test_H8_a_crashed_AGENTIC_attempt_is_not_billed_as_no_model_invoked(tmp_path, git_repo):
    """The ledger may not claim nothing was spent when it cannot know."""
    result = _h3_run(tmp_path, git_repo, dict(AGENTIC), patch_cap_to=50_000,
                     side_effect=_raises)
    assert result.status == "FAIL", f"the crash should fail the phase, got {result.status}"
    reason = _ledger_absent_reason(tmp_path)
    assert "no model invoked" not in reason, (
        "an agentic phase whose harness raised was recorded in the receipts DB as "
        f"having invoked no model. Durable ledger says: {reason!r}"
    )
    assert "UNKNOWN" in reason and "in flight" in reason, (
        "the ledger should say the cost of a crashed attempt is unknown — unknown "
        f"is not zero, and a ledger that rounds it down under-reports. Says: {reason!r}"
    )


def test_H8_CONTROL_a_MECHANICAL_phase_still_says_no_model_invoked(tmp_path, git_repo):
    """The claim is not deleted — it is moved to the one lane that can support it.

    Without this row, H8 is satisfied by dropping the phrase everywhere, and the
    ledger loses the one thing it can state as structurally true: a phase with no
    agent returns from `_execute` before `harness.run` is reached.
    """
    mech = {"name": "a", "writes": ["out/**"], "artifacts": [], "claim": "nothing",
            "gates": [{"gate": "command_succeeds", "args": {"command": "true"}}]}
    _h3_run(tmp_path, git_repo, mech, patch_cap_to=50_000)
    reason = _ledger_absent_reason(tmp_path)
    assert reason == "mechanical phase — no model invoked", (
        f"the mechanical lane's honest absent-reason was lost. Says: {reason!r}"
    )


class _RetryHarness(_FreeHarness):
    """Attempt 1 spends real tokens and returns; attempt 2 dies with the model up.

    The shape J3 is about. A first attempt can cost real money and still fail the
    gates — a refused grant, a policy refusal, a malformed envelope all carry usage.
    """

    name = "retry"
    calls = 0

    def run(self, prompt, cwd, config):
        type(self).calls += 1
        if type(self).calls == 1:
            return _RawResult(
                ok=True,
                text=_json.dumps({"status": "PASS", "summary": "spent money, failed",
                                  "artifacts": [], "notes_for_next_agent": ""}),
                usage=UsageBreakdown(input_tokens=1000, output_tokens=500),
                harness=self.name,
            )
        raise RuntimeError("the harness died on attempt 2 with the model in flight")


def _ledger_tokens(tmp_path, phase_name="a"):
    """`input_tokens` / `output_tokens` as WRITTEN, for the named phase."""
    import sqlite3

    conn = sqlite3.connect(str(tmp_path / "fh" / "receipts.db"))
    try:
        return conn.execute(
            "SELECT input_tokens, output_tokens FROM phases WHERE name = ?", (phase_name,)
        ).fetchone()
    finally:
        conn.close()


def test_J3_a_retry_does_not_DISCARD_what_the_first_attempt_provably_spent(tmp_path, git_repo):
    """H8 inverted: KNOWN cost recorded as absent.

    H8 made the runner stop claiming zero where cost is unknown. The same statement
    then did the opposite at the top of every attempt — it ASSIGNED the in-flight
    absent-reason to `phase.usage`, discarding the running total. Attempt 1 here
    returns 1500 real tokens and fails its gate; attempt 2 raises. Before the fix the
    durable ledger read NULL for a phase that provably spent 1500 tokens, which
    breaks `usage.py`'s opening law from the other side: tokens are never invented,
    and they are not to be un-invented either.

    None of the five H8 rows used `retries > 0`, so the whole retry path was outside
    what they measured — the SCOPE axis. `merge` already existed and was unused.
    """
    _HARNESSES.setdefault("retry", _RetryHarness())
    _RetryHarness.calls = 0
    phase = dict(AGENTIC)
    phase["harness"] = "retry"
    phase["retries"] = 1
    phase["gates"] = [{"gate": "command_succeeds", "args": {"command": "false"}}]
    _h3_run(tmp_path, git_repo, phase, patch_cap_to=50_000)

    tokens = _ledger_tokens(tmp_path)
    assert tokens == (1000, 500), (
        "the ledger discarded what attempt 1 provably spent when attempt 2 crashed. "
        f"A phase that cost 1500 tokens is recorded as {tokens}. Unknown is not "
        "zero (H8) and known is not unknown (J3)."
    )
    reason = _ledger_absent_reason(tmp_path)
    assert "UNKNOWN" in reason and "attempt 2" in reason, (
        "the ledger kept the numbers but stopped saying that attempt 2's cost is "
        f"missing, so the total reads as complete when it is not. Says: {reason!r}"
    )
    assert "NOT the phase total" in reason, (
        "the reason does not warn that the recorded tokens are a PARTIAL sum. A "
        f"reader would take 1500 as what the phase cost. Says: {reason!r}"
    )


def test_J3_a_PARTLY_known_usage_does_not_print_as_if_it_were_complete():
    """`one_line` dropped the caveat the moment any number was present.

    Found while fixing J3 rather than reported: the ledger can hold tokens AND an
    absent-reason, but the human-readable line could not express that pair. It
    printed the numbers and discarded the reason, so a partial sum rendered
    identically to a complete one on the operator's screen — the same
    under-reporting the column beneath it had just been fixed to avoid.
    """
    partial = UsageBreakdown.absent("attempt 2 in flight — ITS cost is UNKNOWN").merge(
        UsageBreakdown(input_tokens=1000, output_tokens=500)
    )
    line = partial.one_line()
    assert "1000" in line, f"the known tokens vanished from the line: {line!r}"
    assert "INCOMPLETE" in line and "UNKNOWN" in line, (
        "a partly-known usage printed as though it were the whole phase's cost. "
        f"Line was: {line!r}"
    )


def test_H8_a_crashed_MECHANICAL_phase_is_not_billed_as_UNKNOWN(tmp_path, git_repo, monkeypatch):
    """The mirror of H8, and the third survivor of the round-fourteen set.

    H8 was the ledger claiming ZERO where cost is unknown. Firing the in-flight
    reason on the mechanical lane too is the same falsehood pointed the other way:
    claiming UNKNOWN where zero is provable. A mechanical phase has `agent: null`,
    `_execute` returns before `harness.run` is reached and no harness is ever
    constructed — so "no model invoked" is not a hopeful default on this lane, it is
    the one absent-reason in this file that is structurally true. Inventing doubt
    about it would put phantom unaccounted spend in the cost ledger on the only lane
    that cannot spend.

    The `if not spec.is_mechanical:` guard is what keeps it true, and nothing tested
    the guard: on the happy path the in-flight string is overwritten two statements
    later, so removing the guard is invisible unless the mechanical execution
    CRASHES. Nothing in the suite crashes a mechanical phase, so the branch was
    reachable only by construction — the ROUTE axis again. Hence the monkeypatch,
    which raises from exactly where the real crash would.
    """
    def _boom(*_a, **_k):
        raise RuntimeError("a mechanical cell died before it could return its claim")

    monkeypatch.setattr(_Runner, "_execute", _boom)
    mech = {"name": "a", "writes": ["out/**"], "artifacts": [], "claim": "nothing",
            "gates": [{"gate": "command_succeeds", "args": {"command": "true"}}]}
    result = _h3_run(tmp_path, git_repo, mech, patch_cap_to=50_000)
    assert result.status == "FAIL", f"the crash should fail the phase, got {result.status}"
    reason = _ledger_absent_reason(tmp_path)
    assert "UNKNOWN" not in reason, (
        "a crashed MECHANICAL phase was billed as cost-unknown. No harness is "
        "constructed on this lane, so zero is provable, and inventing uncertainty "
        f"about it is the H8 falsehood inverted. Ledger says: {reason!r}"
    )
    assert reason == "mechanical phase — no model invoked", (
        "the crashed mechanical phase lost the one absent-reason that is "
        f"structurally true on its lane. Ledger says: {reason!r}"
    )


def test_H8_a_phase_ABORTED_BEFORE_the_attempt_says_so(tmp_path, git_repo):
    """The third H8 edit, and the only path that reads the CONSTRUCTION value.

    An agentic phase stopped by the phase-start containment check never reaches the
    in-flight assignment, so what lands in the ledger is whatever the Phase was
    built with. Handing the runner's lane-aware `total_usage` to the constructor is
    what makes that value the honest one; without it the Phase falls back to its own
    default, which knows nothing about the lane. Three distinct absent-reasons for
    three distinct states — no attempt, attempt in flight, no model — and each is
    refutable on its own path.
    """
    _ignored_dir(git_repo)
    result = _h3_run(tmp_path, git_repo, dict(AGENTIC))
    assert result.status == "ABORTED", f"expected the phase-start abort, got {result.status}"
    reason = _ledger_absent_reason(tmp_path)
    assert reason == "no attempt recorded", (
        "a phase aborted before its attempt should say exactly that. Says: "
        f"{reason!r} — which is what the Phase was CONSTRUCTED with, so the "
        "runner's lane-aware reason is not reaching the constructor."
    )


def test_H8_the_Phase_DEFAULT_claims_nothing_about_model_invocation(tmp_path):
    """The guard for the next call site, asserted directly because nothing else can.

    Every `Phase(...)` in the runner now passes `usage`, so the default is
    unreachable from production — which is precisely why it needs a row of its own
    rather than a comment. A default is inherited by callers that do not exist yet,
    and the one this replaced was wrong in the only direction that matters: it
    under-reported. Asserting the class default is not a reachability claim and is
    not offered as one.
    """
    from factory.phase import Phase

    reason = Phase(name="p", agent="star-lord").usage.absent_reason or ""
    assert "no model invoked" not in reason, (
        "the Phase default asserts that no model was invoked — a fact about the "
        f"world that a dataclass default cannot know. Default says: {reason!r}"
    )
    assert reason, "a default that records no reason at all fails `usage.py`'s own law"


class _GrantingHarness(_FreeHarness):
    """A lane that reports a grant, the way `claude_code` does from its init frame."""

    name = "granting"

    def run(self, prompt, cwd, config):
        return _RawResult(
            ok=True,
            text=_json.dumps({"status": "PASS", "summary": "ran fenced",
                              "artifacts": [], "notes_for_next_agent": ""}),
            harness=self.name,
            extra={
                "permission_mode": "bypassPermissions",
                "granted_tools": ["Read", "Bash"],
                "permission_denials": [],
                "num_turns": 2,
                "stop_reason": "end_turn",
            },
        )


def test_J5_the_runner_CARRIES_the_grant_to_the_ledger(tmp_path, git_repo):
    """Mutation J5-a SURVIVED the first pass, and this row is why it now does not.

    J5 is a finding about WIRING: the grant was adjudicated and then dropped on the way
    to the receipt. The first three rows written for it exercised
    `Receipts.record_agent_session` directly — proving the column accepts a value nobody
    was passing it. Deleting `result.extra` from the runner's call site left all of them
    green, so the fix for a wiring defect was itself unwired and the suite said nothing.

    Fifth axis, on the finding named after it. The receipts rows test the STORE; this
    one tests that a phase which actually ran puts something in it.
    """
    _HARNESSES.setdefault("granting", _GrantingHarness())
    phase = dict(AGENTIC)
    phase["harness"] = "granting"
    result = _h3_run(tmp_path, git_repo, phase, patch_cap_to=50_000)
    assert result.status == "PASS", f"premise failed: the phase did not pass ({result.status})"
    import sqlite3
    conn = sqlite3.connect(str(tmp_path / "fh" / "receipts.db"))
    try:
        row = conn.execute(
            "SELECT permission_mode, granted_tools, denial_count, num_turns "
            "FROM agent_sessions"
        ).fetchone()
    finally:
        conn.close()
    assert row is not None, "the phase ran an agent and no agent_session was recorded at all"
    assert row[0] == "bypassPermissions", (
        "a phase PASSED and the receipt cannot say what permission mode it ran under. "
        f"Got {row[0]!r}. That is the sentence J1 makes load-bearing: the argv is not "
        "evidence of the grant, so if the init frame does not reach the ledger nothing does."
    )
    assert _json.loads(row[1]) == ["Read", "Bash"], (
        f"the granted tool set did not survive the trip from harness to ledger: {row[1]!r}"
    )
    assert row[2] == 0 and row[3] == 2
