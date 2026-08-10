"""The default-fail phase primitive — Spec A § 2.

A phase is guilty until a single finish() acquits it. These tests pin the four
ways that can go wrong (never finished · finished twice · raised · gated red)
and the one way it can go right, plus the structural law that there is no
override parameter to find.
"""

import inspect

import pytest

from factory.envelope import EnvelopeBase
from factory.gates.base import GateReport
from factory.phase import FAILED, PARTIAL, PASS, Phase, PhaseProtocolError
from factory.receipts import Receipts


# ---------------------------------------------------------------------------
# the default
# ---------------------------------------------------------------------------
def test_a_phase_enters_failed():
    with Phase(name="p") as phase:
        assert phase.status == FAILED
        assert phase.is_green is False
        phase.finish("PASS", "done")


def test_a_phase_that_never_finishes_stays_failed():
    with Phase(name="p") as phase:
        pass
    assert phase.status == FAILED
    assert "without calling finish()" in phase.error
    assert "assume-success" in phase.error


def test_one_finish_collapses_the_phase():
    with Phase(name="p") as phase:
        env = phase.finish("PASS", "the thing was done", ["out/a.json"], "next: b")
    assert phase.status == PASS
    assert phase.is_green
    assert isinstance(env, EnvelopeBase)
    assert phase.envelope.artifacts == ["out/a.json"]


def test_a_second_finish_is_a_protocol_error_and_re_fails_the_phase():
    with Phase(name="p") as phase:
        phase.finish("PASS", "first")
        with pytest.raises(PhaseProtocolError):
            phase.finish("PASS", "second")
    assert phase.status == FAILED
    assert "more than once" in phase.error


def test_a_raised_exception_fails_the_phase_and_keeps_the_traceback():
    with Phase(name="p") as phase:
        raise RuntimeError("the tool exploded")
    assert phase.status == FAILED
    assert "RuntimeError: the tool exploded" in phase.error
    assert "Traceback" in phase.error


def test_keyboard_interrupt_is_not_swallowed():
    with pytest.raises(KeyboardInterrupt):
        with Phase(name="p"):
            raise KeyboardInterrupt


def test_a_self_declared_fail_maps_to_failed():
    with Phase(name="p") as phase:
        phase.finish("FAIL", "I could not do it")
    assert phase.status == FAILED


def test_partial_is_its_own_status_and_is_not_green():
    with Phase(name="p") as phase:
        phase.finish("PARTIAL", "half of it")
    assert phase.status == PARTIAL
    assert phase.is_green is False


def test_a_status_outside_the_envelope_vocabulary_is_refused():
    with Phase(name="p") as phase:
        with pytest.raises(PhaseProtocolError, match="not one of"):
            phase.finish("GREEN", "looks fine to me")
    assert phase.status == FAILED


# ---------------------------------------------------------------------------
# gates may only downgrade
# ---------------------------------------------------------------------------
def test_a_red_gate_downgrades_a_finished_pass():
    with Phase(name="p") as phase:
        phase.finish("PASS", "I claim success")
        phase.apply_gate_verdicts(
            [GateReport.failed("artifacts_exist", "the file is not there")]
        )
    assert phase.status == FAILED
    assert "artifacts_exist:FAIL" in phase.error


def test_not_runnable_downgrades_too():
    with Phase(name="p") as phase:
        phase.finish("PASS", "I claim success")
        phase.apply_gate_verdicts([GateReport.not_runnable("json_parses", "no JSON declared")])
    assert phase.status == FAILED


def test_green_gates_cannot_upgrade_a_phase_that_never_finished():
    with Phase(name="p") as phase:
        phase.apply_gate_verdicts([GateReport.passed("artifacts_exist", "all present")])
        assert phase.status == FAILED
    assert phase.status == FAILED


def test_apply_gate_verdicts_is_idempotent():
    reports = [GateReport.failed("g", "nope")]
    with Phase(name="p") as phase:
        phase.finish("PASS", "claim")
        first = phase.apply_gate_verdicts(reports)
        second = phase.apply_gate_verdicts(reports)
    assert first == second == FAILED


# ---------------------------------------------------------------------------
# the structural law: no override exists to be found
# ---------------------------------------------------------------------------
FORBIDDEN_PARAMS = ("force", "override", "assume_success", "skip_gates", "allow_fail", "yes")


def test_no_method_on_phase_accepts_an_override_parameter():
    offenders: list[str] = []
    for name, member in inspect.getmembers(Phase, predicate=inspect.isfunction):
        params = inspect.signature(member).parameters
        for forbidden in FORBIDDEN_PARAMS:
            if forbidden in params:
                offenders.append(f"Phase.{name}({forbidden}=...)")
    assert not offenders, (
        f"override path(s) found: {offenders}. The emit wall's no_override posture is "
        "the ancestor and the law — there is no parameter that turns a red green."
    )


def test_nothing_in_the_module_can_raise_a_status():
    """apply_gate_verdicts is the only status-mutating public entry after finish()."""
    source = inspect.getsource(Phase.apply_gate_verdicts)
    assert "self.status = FAILED" in source
    assert "self.status = PASS" not in source


# ---------------------------------------------------------------------------
# receipts integration
# ---------------------------------------------------------------------------
def test_a_phase_records_failed_before_it_records_anything_else(tmp_path):
    """The receipt says FAILED from the moment the phase opens."""
    receipts = Receipts(tmp_path / "r.db")
    receipts.start_session("run1", "wf", tmp_path, tmp_path)
    with Phase(name="p", receipts=receipts, run_id="run1", idx=0) as phase:
        row = receipts.phases("run1")[0]
        assert row["status"] == FAILED, "the open phase must be on record as FAILED"
        phase.finish("PASS", "done")
    assert receipts.phases("run1")[0]["status"] == PASS
    kinds = [e["kind"] for e in receipts.events("run1")]
    assert kinds == ["phase_start", "phase_end"]
    receipts.close()


def test_an_unfinished_phase_lands_in_receipts_as_failed(tmp_path):
    receipts = Receipts(tmp_path / "r.db")
    receipts.start_session("run1", "wf", tmp_path, tmp_path)
    with Phase(name="p", receipts=receipts, run_id="run1", idx=0):
        pass
    row = receipts.phases("run1")[0]
    assert row["status"] == FAILED
    assert "without calling finish()" in row["error"]
    receipts.close()
