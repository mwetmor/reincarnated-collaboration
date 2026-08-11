"""Workflow loading — Spec A § 9. Every refusal happens at LOAD, before anything runs.

A workflow that is wrong should be wrong before a single token is spent. Each
test here is a refusal the loader must make with the file still on disk and the
run not yet started.
"""

import json
import re

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
    path = _phase_wf(
        tmp_path, {**MINIMAL_PHASE, "agent": "rocket", "tools": ["Read"]}
    )
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


# ---------------------------------------------------------------------------
# C5 — the COARSE tier is a lane condition, enforced at LOAD
# ---------------------------------------------------------------------------
AGENTIC_PHASE = {
    "name": "p",
    "agent": "star-lord",
    "prompt": "do the thing",
    "tools": ["Read"],
    "gates": ["artifacts_exist"],
    "artifacts": ["x.txt"],
}


def _ack(repo, region: str) -> str:
    """The acknowledgement key, built the way the product builds it (Gate-2 F6).

    These were literals — `"repo:ignored/"` — which is a second, independent spelling
    of a format the product owns, and the two agree only until one changes. Worse,
    the literal encoded the BASENAME keying that F6 is the fix for, so the tests
    would have gone red on the fix rather than on a defect.
    """
    from factory import permissions as perm

    return perm.coarse_key(repo, region)


@pytest.fixture
def coarse_repo(git_repo, monkeypatch):
    """A repo with one region that measures COARSE.

    The cap is lowered rather than 50,000 files being written: the branch under test
    is `files > cap`, and which side of it a region falls on is the only thing that
    differs between this fixture and the godot tree. `ignored/` is in the fixture's
    .gitignore, so it reproduces the compounding case — coarse AND unrecoverable
    from git.
    """
    from factory import permissions as perm

    monkeypatch.setattr(perm, "_IGNORED_SCAN_CAP", 1)
    region = git_repo / "ignored"
    region.mkdir()
    (region / "a").write_text("1\n")
    (region / "b").write_text("2\n")
    return git_repo


def test_C5_an_agentic_phase_over_an_unacknowledged_COARSE_region_is_refused(
    tmp_path, coarse_repo
):
    """Gate-2 C5. README rule 3 discharged this with a caveat printed on the receipt.
    A caveat is a claim to a reader, not a gate — and the agentic lane is defined by a
    model choosing its own paths, which is precisely the case the caveat does not
    cover. An in-place rewrite inside a coarse gitignored region is neither detected
    nor recoverable."""
    path = _wf(tmp_path, root=str(coarse_repo), repos=[str(coarse_repo)],
               phases=[dict(AGENTIC_PHASE)])
    with pytest.raises(WorkflowError, match="measure COARSE"):
        load_workflow(path)


def test_C5_the_refusal_names_the_region_so_the_author_can_act_on_it(
    tmp_path, coarse_repo
):
    path = _wf(tmp_path, root=str(coarse_repo), repos=[str(coarse_repo)],
               phases=[dict(AGENTIC_PHASE)])
    with pytest.raises(WorkflowError, match=re.escape(_ack(coarse_repo, "ignored/"))):
        load_workflow(path)


def test_C5_a_named_acknowledgement_lets_the_agentic_workflow_load(
    tmp_path, coarse_repo
):
    """The escape hatch is real, and it is per-region and by name — not a boolean."""
    path = _wf(tmp_path, root=str(coarse_repo), repos=[str(coarse_repo)],
               phases=[dict(AGENTIC_PHASE)],
               coarse_acknowledged=[_ack(coarse_repo, "ignored/")])
    wf = load_workflow(path)
    assert wf.coarse_acknowledged == [_ack(coarse_repo, "ignored/")]


def test_C5_an_acknowledgement_that_does_not_match_the_tree_is_refused(
    tmp_path, coarse_repo
):
    """Naming the wrong region is refused even though it is strictly MORE cautious
    than naming none. An acknowledgement that has drifted from the tree reads as
    diligence and certifies nothing — the class this spine keeps finding."""
    path = _wf(tmp_path, root=str(coarse_repo), repos=[str(coarse_repo)],
               phases=[dict(AGENTIC_PHASE)],
               coarse_acknowledged=[_ack(coarse_repo, "ignored/"),
                                    _ack(coarse_repo, "Assets/Synty/")])
    with pytest.raises(WorkflowError, match="do not measure COARSE"):
        load_workflow(path)


def test_C5_a_MECHANICAL_workflow_over_the_same_region_still_loads(
    tmp_path, coarse_repo
):
    """The trigger is the lane, and it is falsifiable: same tree, same region, no
    agent — and the loader says yes. Without this row the C5 refusal could be a blanket
    ban on coarse regions wearing a lane condition's error message."""
    wf = load_workflow(
        _wf(tmp_path, root=str(coarse_repo), repos=[str(coarse_repo)])
    )
    assert wf.phases[0].is_mechanical
    assert wf.coarse_acknowledged == []


def test_C5_acknowledging_ONE_region_does_not_clear_a_second_one(tmp_path, coarse_repo):
    """The acknowledgement is per-region, and only a SECOND region can prove it.

    Round-ten mutation R6 (`unacknowledged = set() if acknowledged else measured`)
    survived the first C5 set: with one coarse region in the fixture, a per-region
    check and a boolean flag are observationally identical. The escape hatch has to
    cost one line per region or it is a checkbox — which is this spine's recurring
    defect wearing an allowlist's clothes.
    """
    second = coarse_repo / "extra"
    second.mkdir()
    (second / "a").write_text("1\n")
    (second / "b").write_text("2\n")
    path = _wf(tmp_path, root=str(coarse_repo), repos=[str(coarse_repo)],
               phases=[dict(AGENTIC_PHASE)],
               coarse_acknowledged=[_ack(coarse_repo, "ignored/")])
    with pytest.raises(WorkflowError, match=re.escape(_ack(coarse_repo, "extra/"))):
        load_workflow(path)


def test_C3_the_loader_refuses_an_agentic_phase_that_declares_no_tools(tmp_path, git_repo):
    """The same refusal as the harness's, at the earlier boundary (Gate-2 C3).

    The harness guard alone would let a workflow author walk a run to the point of
    spending tokens before learning its containment was never declared. And a guard
    present in only one of two entry points is a guard with a route around it —
    which is L8's finding. Both fail closed; this is the LOAD half.
    """
    phase = {k: v for k, v in AGENTIC_PHASE.items() if k != "tools"}
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    with pytest.raises(WorkflowError, match="fail OPEN"):
        load_workflow(path)


# --- Gate-2 F4: the allowlist must RESTRICT, not merely be present ------------------
#
# C3 proved the guard refuses when `tools` is ABSENT and stopped there. That is a test
# of declaration. The state C3 exists to prevent — the full built-in set, chosen by
# nobody — was still reachable, by writing one word, and it read as diligence. Each
# arm of the closed vocabulary gets a row here, because a vocabulary with an untested
# arm is a vocabulary with a hole, and the hole is always the one that looks fine.


@pytest.mark.parametrize(
    "tools, expect",
    [
        (["default"], "use all tools"),
        (["Read", "default"], "use all tools"),          # buried among real names
        ("Read", "must be a LIST"),                       # YAML scalar -> ['R','e','a','d']
        ([], "is empty"),
        (["Reed"], "not in the built-in set"),            # a typo is not an allowlist
        (["Bash(git *)", "Nope"], "not in the built-in set"),
        (["mcp__plugin_vercel_vercel__authenticate"], "MCP"),
    ],
)
def test_F4_the_loader_refuses_an_allowlist_that_does_not_restrict(
    tmp_path, git_repo, tools, expect
):
    phase = dict(AGENTIC_PHASE, tools=tools)
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    with pytest.raises(WorkflowError, match=expect):
        load_workflow(path)


@pytest.mark.parametrize("tools", [["Read"], ["Bash(git *)"], ["Read", "Bash(git log:*)"]])
def test_F4_a_genuinely_narrow_allowlist_still_loads(tmp_path, git_repo, tools):
    """The refusals above are worth nothing if they also refuse the correct input.

    Scoped forms are the vendor's own idiom and are strictly narrower than the bare
    tool, so the BASE name is what the vocabulary adjudicates.
    """
    phase = dict(AGENTIC_PHASE, tools=tools)
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    assert load_workflow(path).phases[0].tools == tools


def test_F4_the_loader_and_the_harness_share_ONE_vocabulary(tmp_path, git_repo):
    """Not two lists that agree today.

    L8's finding was a guard with a route around it. Two vocabularies is that shape
    with a delay on it: they agree until one is extended, and the disagreement shows
    up as a phase that loads and then dies in argv — or worse, the reverse. So the
    loader calls the ADAPTER's validator, and this row fails if it ever stops.
    """
    from factory.harness import get_harness

    adapter = get_harness("claude_code")
    calls: list[object] = []
    original = type(adapter).validate_tools

    def spy(tools, where):
        calls.append(tools)
        return original(tools, where)

    type(adapter).validate_tools = staticmethod(spy)
    try:
        path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)],
                   phases=[dict(AGENTIC_PHASE)])
        load_workflow(path)
    finally:
        type(adapter).validate_tools = staticmethod(original)
    assert calls == [["Read"]], "the loader validated the allowlist somewhere else"


def test_F4_a_harness_that_publishes_no_vocabulary_cannot_be_given_an_allowlist(
    tmp_path, git_repo
):
    """The fail-closed default for a lane the vocabulary has never met.

    A second harness is the obvious route around a validator that lives on the first
    one. If it cannot say which tool names it accepts, it does not get to receive an
    allowlist — silently passing the list through is precisely the fail-open.
    """
    from factory.harness.base import _HARNESSES

    class Mute:
        name = "mute"

        def run(self, prompt, cwd, config):  # pragma: no cover - never reached
            raise AssertionError("load should have refused")

    _HARNESSES["mute"] = Mute()
    try:
        phase = dict(AGENTIC_PHASE, harness="mute")
        path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
        with pytest.raises(WorkflowError, match="publishes no `validate_tools`"):
            load_workflow(path)
    finally:
        _HARNESSES.pop("mute", None)


def test_F6_two_repos_with_the_SAME_BASENAME_do_not_share_an_acknowledgement(
    tmp_path, coarse_repo, git_repo_factory
):
    """Gate-2 F6. The key was `repo.name`, so `~/a/engine` and `~/b/engine` collided.

    One acknowledgement then cleared a coarse region in a tree nobody had looked at,
    and the receipt read as though both had been considered. A key that is not unique
    over its domain is not a key — and this is the recurring shape again: a predicate
    answering a slightly different question ("is a repo with this NAME acknowledged?"),
    whose wrong answer is the quiet one.
    """
    twin = git_repo_factory(tmp_path / "elsewhere" / coarse_repo.name)
    region = twin / "ignored"
    region.mkdir()
    (region / "a").write_text("1\n")
    (region / "b").write_text("2\n")
    assert twin.name == coarse_repo.name, "premise failed: the basenames must collide"

    path = _wf(tmp_path, root=str(coarse_repo),
               repos=[str(coarse_repo), str(twin)],
               phases=[dict(AGENTIC_PHASE)],
               coarse_acknowledged=[_ack(coarse_repo, "ignored/")])
    with pytest.raises(WorkflowError, match=re.escape(_ack(twin, "ignored/"))):
        load_workflow(path)
