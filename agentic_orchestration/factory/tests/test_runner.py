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
