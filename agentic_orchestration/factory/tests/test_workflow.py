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
    """A workflow file on disk. `root` defaults to tmp_path, which is NOT a git tree —
    fine for the refusal tests, which must fail before containment is ever reached. Any
    test that expects a successful load passes `root=str(git_repo)`, because a workflow
    that loads is a workflow whose containment claims are measurable (F2)."""
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
def test_a_minimal_workflow_loads(tmp_path, git_repo):
    wf = load_workflow(_wf(tmp_path, root=str(git_repo)))
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
def test_gates_accept_both_bare_names_and_name_plus_args(tmp_path, git_repo):
    path = _wf(
        tmp_path,
        root=str(git_repo),
        phases=[{
            "name": "p",
            "artifacts": ["x.txt"],
            "gates": [
                "artifacts_exist",
                {"gate": "sha256_matches", "args": {"path": "x.txt", "expected": "ab"}},
            ],
        }],
    )
    wf = load_workflow(path)
    gates = wf.phases[0].gates
    assert gates[0].gate == "artifacts_exist" and gates[0].args == {}
    assert gates[1].args["expected"] == "ab"


def test_a_malformed_gate_entry_is_refused(tmp_path):
    path = _phase_wf(tmp_path, {"name": "p", "gates": [{"name": "artifacts_exist"}]})
    with pytest.raises(WorkflowError, match="each gate is either"):
        load_workflow(path)


# ---------------------------------------------------------------------------
# containment is measurable — Gate-2 F2
#
# Containment is fingerprint-based, and a fingerprint is a git change-set. A tree
# that git cannot describe produces an empty diff, and an empty diff reads exactly
# like innocence. These are the refusals that keep an unmeasurable tree from being
# mistaken for a clean one.
# ---------------------------------------------------------------------------
def test_a_non_git_repo_is_refused_at_load(tmp_path, git_repo):
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo), str(plain)])
    with pytest.raises(WorkflowError, match="not a git worktree"):
        load_workflow(path)


def test_a_missing_repo_is_refused_at_load(tmp_path, git_repo):
    path = _wf(
        tmp_path, root=str(git_repo), repos=[str(git_repo), str(tmp_path / "gone")]
    )
    with pytest.raises(WorkflowError, match="does not exist"):
        load_workflow(path)


def test_a_read_only_tree_no_repo_covers_is_refused(tmp_path, git_repo):
    """Declaring a tree read-only does not fingerprint it. If no `repos` entry covers
    it, nothing measures it and the read-only promise is decorative."""
    other = tmp_path / "elsewhere"
    other.mkdir()
    path = _wf(
        tmp_path, root=str(git_repo), repos=[str(git_repo)], read_only_trees=[str(other)]
    )
    with pytest.raises(WorkflowError, match="not covered by any `repos` entry"):
        load_workflow(path)


def test_a_subdirectory_declared_as_a_repo_is_refused_at_load(tmp_path, git_repo):
    """Gate-2 re-review G1. `git rev-parse` SUCCEEDS from any depth inside a
    worktree, so a returncode check accepts a subdirectory — and `git status` then
    reports worktree-root-relative paths that get joined against the wrong base,
    so every signature comes back empty and the tree measures as permanently clean.
    A guard that passes while measuring nothing is worse than no guard."""
    sub = git_repo / "sub"
    sub.mkdir()
    path = _wf(tmp_path, root=str(git_repo), repos=[str(sub)])
    with pytest.raises(WorkflowError, match="SUBDIRECTORY of the git worktree"):
        load_workflow(path)


def test_the_subdirectory_refusal_names_the_worktree_root_to_declare_instead(
    tmp_path, git_repo
):
    """The error an author acts on. The previous version of the read-only rule said
    'declare it in `repos` as well', which walked the author straight into G1."""
    sub = git_repo / "sub"
    sub.mkdir()
    with pytest.raises(WorkflowError, match=str(git_repo.resolve())):
        load_workflow(_wf(tmp_path, root=str(git_repo), repos=[str(sub)]))


def test_a_read_only_tree_that_does_not_exist_is_refused(tmp_path, git_repo):
    """Gate-2 verdict H2. F2's own sentence, applied to the half that never got the
    existence check: a read-only tree that is not there protects nothing, and it
    loads CLEAN — the shape of every defect this validation exists to refuse. The
    likely cause is a typo, which is the dangerous case: the author walks away
    believing the tree they meant is fenced."""
    path = _wf(
        tmp_path,
        root=str(git_repo),
        repos=[str(git_repo)],
        read_only_trees=[str(git_repo / "seasnos")],  # sic
    )
    with pytest.raises(WorkflowError, match="does not exist"):
        load_workflow(path)


def test_a_read_only_tree_that_is_a_file_is_refused(tmp_path, git_repo):
    """Read-only is a claim about a TREE. A file declared as one would be fenced by
    the ancestor rule alone, which reads as protection but covers only that path."""
    path = _wf(
        tmp_path,
        root=str(git_repo),
        repos=[str(git_repo)],
        read_only_trees=[str(git_repo / "tracked.txt")],
    )
    with pytest.raises(WorkflowError, match="not a directory"):
        load_workflow(path)


def test_a_read_only_tree_nested_inside_a_declared_repo_is_accepted(tmp_path, git_repo):
    """Coverage is by containment, not by string equality — a subdirectory of a
    fingerprinted repo is fingerprinted with it.

    Acceptance alone proves nothing (that was the G2 defect: this test asserted the
    loader said yes, while `classify` enforced nothing). The enforcement half is
    `test_write_inside_a_NESTED_read_only_tree_is_a_breach` in test_permissions.py.
    """
    nested = git_repo / "sub"
    nested.mkdir()
    wf = load_workflow(
        _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)],
            read_only_trees=[str(nested)])
    )
    assert wf.read_only_trees == [nested.resolve()]


def test_the_shipped_kc2_workflow_declares_every_read_only_tree_as_a_repo():
    """The real workflow, not a fixture: the engine and godot trees are the ones the
    run promises not to write to, so they are the ones that must be measured."""
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "workflows" / "kc2-baton-mechanical.yaml"
    wf = load_workflow(path)
    assert wf.read_only_trees, "the shipped workflow makes no read-only claim to check"
    for ro in wf.read_only_trees:
        assert any(ro == r or r in ro.parents for r in wf.repos), f"{ro} is unmeasured"
