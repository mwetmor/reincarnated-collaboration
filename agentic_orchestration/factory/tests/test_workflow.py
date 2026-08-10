"""Workflow loading — Spec A § 9. Every refusal happens at LOAD, before anything runs.

A workflow that is wrong should be wrong before a single token is spent. Each
test here is a refusal the loader must make with the file still on disk and the
run not yet started.
"""

import json

import pytest

from factory.workflow import MAX_RETRIES, WorkflowError, load_workflow

MINIMAL_PHASE = {"name": "p", "gates": ["artifacts_exist"], "artifacts": ["x.txt"]}


def _wf(tmp_path, **overrides):
    doc = {"name": "t", "root": str(tmp_path), "phases": [dict(MINIMAL_PHASE)]}
    doc.update(overrides)
    path = tmp_path / "wf.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def _phase_wf(tmp_path, phase: dict):
    return _wf(tmp_path, phases=[phase])


# ---------------------------------------------------------------------------
# it loads
# ---------------------------------------------------------------------------
def test_a_minimal_workflow_loads(tmp_path):
    wf = load_workflow(_wf(tmp_path))
    assert wf.name == "t"
    assert len(wf.phases) == 1
    assert wf.phases[0].is_mechanical, "a phase with no agent is a mechanical cell"
    assert wf.sha256, "the workflow file's digest is pinned into the receipt"


def test_the_shipped_kc2_workflow_loads():
    """The workflow the spine was built against must survive every loader rule."""
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "workflows" / "kc2-baton-mechanical.yaml"
    wf = load_workflow(path)
    assert wf.phases, "the shipped workflow declares no phases"
    for phase in wf.phases:
        assert phase.gates, f"{phase.name} would run unadjudicated"
        assert phase.retries <= MAX_RETRIES


# ---------------------------------------------------------------------------
# it refuses
# ---------------------------------------------------------------------------
def test_a_model_key_is_refused(tmp_path):
    path = _phase_wf(tmp_path, {**MINIMAL_PHASE, "model": "claude-opus-4"})
    with pytest.raises(WorkflowError, match="model"):
        load_workflow(path)


def test_an_unknown_gate_is_refused_at_load_not_at_run(tmp_path):
    path = _phase_wf(tmp_path, {"name": "p", "gates": ["looks_good_to_me"]})
    with pytest.raises(WorkflowError, match="not registered"):
        load_workflow(path)


def test_a_phase_with_no_gates_is_refused(tmp_path):
    path = _phase_wf(tmp_path, {"name": "p"})
    with pytest.raises(WorkflowError, match="no gates"):
        load_workflow(path)


@pytest.mark.parametrize("retries", [MAX_RETRIES + 1, 10, -1])
def test_retries_beyond_the_bound_are_refused(tmp_path, retries):
    path = _phase_wf(tmp_path, {**MINIMAL_PHASE, "retries": retries})
    with pytest.raises(WorkflowError, match="retries"):
        load_workflow(path)


def test_the_retry_bound_itself_is_three():
    assert MAX_RETRIES == 3, (
        "the standing rule on every call site is 3 attempts with exponential backoff, "
        "then stop and report"
    )


def test_an_agent_without_a_prompt_is_refused(tmp_path):
    path = _phase_wf(tmp_path, {**MINIMAL_PHASE, "agent": "rocket"})
    with pytest.raises(WorkflowError, match="no `prompt`"):
        load_workflow(path)


def test_a_prompt_without_an_agent_is_refused(tmp_path):
    path = _phase_wf(tmp_path, {**MINIMAL_PHASE, "prompt": "do the thing"})
    with pytest.raises(WorkflowError, match="no agent"):
        load_workflow(path)


def test_duplicate_phase_names_are_refused(tmp_path):
    path = _wf(tmp_path, phases=[dict(MINIMAL_PHASE), dict(MINIMAL_PHASE)])
    with pytest.raises(WorkflowError, match="duplicate phase name"):
        load_workflow(path)


def test_a_missing_root_is_refused(tmp_path):
    path = _wf(tmp_path, root=str(tmp_path / "nowhere"))
    with pytest.raises(WorkflowError, match="root does not exist"):
        load_workflow(path)


def test_an_empty_phase_list_is_refused(tmp_path):
    path = _wf(tmp_path, phases=[])
    with pytest.raises(WorkflowError, match="no phases"):
        load_workflow(path)


def test_a_bad_on_fail_value_is_refused(tmp_path):
    path = _wf(tmp_path, on_fail="carry on regardless")
    with pytest.raises(WorkflowError, match="on_fail"):
        load_workflow(path)


def test_a_missing_file_is_refused(tmp_path):
    with pytest.raises(WorkflowError, match="not found"):
        load_workflow(tmp_path / "nope.yaml")


def test_an_unsupported_extension_is_refused(tmp_path):
    path = tmp_path / "wf.toml"
    path.write_text("name = 't'", encoding="utf-8")
    with pytest.raises(WorkflowError, match="unsupported workflow extension"):
        load_workflow(path)


# ---------------------------------------------------------------------------
# gate argument shapes
# ---------------------------------------------------------------------------
def test_gates_accept_both_bare_names_and_name_plus_args(tmp_path):
    path = _phase_wf(
        tmp_path,
        {
            "name": "p",
            "artifacts": ["x.txt"],
            "gates": [
                "artifacts_exist",
                {"gate": "sha256_matches", "args": {"path": "x.txt", "expected": "ab"}},
            ],
        },
    )
    wf = load_workflow(path)
    gates = wf.phases[0].gates
    assert gates[0].gate == "artifacts_exist" and gates[0].args == {}
    assert gates[1].args["expected"] == "ab"


def test_a_malformed_gate_entry_is_refused(tmp_path):
    path = _phase_wf(tmp_path, {"name": "p", "gates": [{"name": "artifacts_exist"}]})
    with pytest.raises(WorkflowError, match="each gate is either"):
        load_workflow(path)
