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
