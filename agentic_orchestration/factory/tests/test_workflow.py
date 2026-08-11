"""Workflow loading — Spec A § 9. Every refusal happens at LOAD, before anything runs.

A workflow that is wrong should be wrong before a single token is spent. Each
test here is a refusal the loader must make with the file still on disk and the
run not yet started.
"""

import json
import re

import pytest

from factory.harness.claude_code import (
    BUILTIN_TOOLS,
    INVOCATION_ONLY_TOOLS,
    REASONED_ADMISSIONS,
    UNFENCEABLE_TOOLS,
)
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


# --- Gate-2 J7: a name the CLI HAS, whose grant is not its reach --------------------
#
# F4 closed the vocabulary against names the CLI does not have. That is a membership
# question, and it is not the containment question. `Task` is a member in good standing:
# it passes F4, it passes `check_grant` with the granted set EXACTLY equal to the
# declared set, and the child it spawns holds Bash, Edit and Write (measured
# 2026-08-11). The fence is satisfied and bypassed in one call — J1's shape, arriving
# inside the mechanism that replaced J1.
#
# These rows exist because the refusal has to be REACHED, not merely declared. The J7
# fix originally landed as a dict that nothing read: the WIRING axis, which is the
# defect this whole series keeps finding.


#: The refused roster, HARDCODED. Gate-2 JR-13 (jack-ryan, round 19).
#:
#: Every row that adjudicates a refusal is parametrised over `UNFENCEABLE_TOOLS`, so a
#: DELETION from that dict loses a case rather than failing one and the suite stays
#: green — README rule 44, which round 17 wrote and round 18 then walked into inside its
#: own new entry. Measured, at `5a75386d`: deleting `ToolSearch`, `EnterWorktree`,
#: `RemoteTrigger`, `PushNotification`, `CronDelete` or `ScheduleWakeup` left the whole
#: suite green. SIX of nine findings were one dict-entry deletion from evaporating.
#:
#: This literal is the second half of rule 44's "both, not either": the parametrisation
#: keeps the lists from drifting, and this keeps the findings from evaporating. Adding a
#: name here is meant to be a deliberate act, not a convenience — if you are editing
#: this list to make a test pass, that is the review the rule exists to force.
REFUSED_ROSTER = frozenset({
    "Task", "Agent", "ToolSearch", "EnterWorktree", "CronCreate", "CronDelete",
    "ScheduleWakeup", "RemoteTrigger", "PushNotification",
})


def test_JR13_no_refusal_can_be_DELETED_without_a_row_failing():
    """The roster, pinned literally, because deletion is invisible to derivation.

    This is the only row in the file that fails on a REMOVAL from `UNFENCEABLE_TOOLS`.
    Everything else is derived from that dict and therefore cannot see one: the J7
    existence row computes `set(UNFENCEABLE_TOOLS) - known`, and removing an element
    can only SHRINK that difference, so it is structurally incapable of failing on a
    deletion from the dict it guards. Round 18's mutation table named it as the killer
    for exactly that mutation. It was not an unverified attribution; it was an
    impossible one, and the reason it looked verified is in `mutation`-shape rather
    than in the code — round 18 mutated by RENAMING the entry, which leaves an orphan
    the derived row does trip over. A rename is a strictly weaker mutation than a
    deletion here, and the fix under test is one that only deletion can reach.
    """
    assert set(UNFENCEABLE_TOOLS) == set(REFUSED_ROSTER), (
        "the refused roster changed.\n"
        f"  removed: {sorted(REFUSED_ROSTER - set(UNFENCEABLE_TOOLS))}\n"
        f"  added:   {sorted(set(UNFENCEABLE_TOOLS) - REFUSED_ROSTER)}\n"
        "A REMOVAL is a Gate-2 finding being withdrawn, and it needs the evidence that "
        "put the name there to be withdrawn with it. An ADDITION needs a reason in the "
        "dict and a line in this literal. Neither is a test-fixing edit."
    )


#: The admitted roster, HARDCODED. Gate-2 JR-15 (jack-ryan, round 20).
#:
#: Round 19 wrote rule 47 and applied it to `UNFENCEABLE_TOOLS` alone. The dict beside
#: it has the identical shape and had no pin: all four assertions over
#: `REASONED_ADMISSIONS` are derived in the SHRINKING direction (two set differences,
#: one blank-reason scan, and one row that loads `sorted(REASONED_ADMISSIONS)` and so
#: simply tests one fewer name). Measured twice, by jack-ryan and then independently by
#: me: deleting `Skill` or `ExitWorktree` leaves **603 passed** — not 602. Nothing is
#: parametrised over this dict, so the count does not even twitch. That is worse than
#: the JR-13 case, where a careful reader comparing totals had one thread to pull.
#:
#: WHICH collections need a literal, since the answer is not "all of them" and a rule
#: that says so would be noise. The distinction is jack-ryan's; the control measurements
#: below are theirs, re-run by me before this comment claimed them (see notes § 24.5 for
#: the observed lines — writing the sentence first and measuring afterwards is how the
#: last three rounds each produced a false receipt):
#:
#:   - a collection whose members are BEHAVIOUR is protected by the scenario rows that
#:     exercise the behaviour. `GIT_NESTED_GITDIRS`, `GIT_CONTROL_PATHS` and
#:     `PROTECTED_EVERY_REPO` are all KILLED by deletion, because removing a member
#:     stops a real key from being minted and a real row notices. They need no literal.
#:   - a collection whose members are a RECORD needs the literal, because deleting the
#:     record changes no behaviour and therefore no row can see it. `REASONED_ADMISSIONS`
#:     is the only one of that kind here. `Skill` is admitted either way; what evaporates
#:     is the sentence that adjudicated it — *"Distinct from `ToolSearch`, which changes
#:     the callable set rather than the instructions"* — which is the entire reason one
#:     of those two names is refused and the other is not. This dict's own docstring
#:     says an admission with a reason can be argued with and an admission by silence
#:     cannot; a silent deletion converts the first into the second.
ADMITTED_ROSTER = frozenset({"Skill", "TaskOutput", "TaskStop", "ExitWorktree"})


def test_JR15_no_reasoned_admission_can_be_DELETED_without_a_row_failing():
    """`REFUSED_ROSTER`'s partner, for the dict whose members are a record.

    The addition direction was already closed before this row existed: moving a name
    from `UNFENCEABLE_TOOLS` into `REASONED_ADMISSIONS` fails
    `test_JR13_no_refusal_can_be_DELETED_without_a_row_failing` as a missing refusal.
    Only deletion-from-admissions was open, and it was open in its most complete form —
    the suite's verdict was byte-identical before and after.

    The second assertion is not decoration. A roster pin catches the KEY vanishing and
    a blank-reason scan catches the reason being emptied, and between them sits the case
    neither sees: the reason rewritten to something that no longer adjudicates anything.
    `Skill`'s admission is not "it seems fine"; it is a stated contrast against the one
    name in this module refused on reasoning rather than measurement. That contrast is
    the load-bearing clause, so it is pinned rather than described.
    """
    assert set(REASONED_ADMISSIONS) == set(ADMITTED_ROSTER), (
        "the admitted roster changed.\n"
        f"  removed: {sorted(ADMITTED_ROSTER - set(REASONED_ADMISSIONS))}\n"
        f"  added:   {sorted(set(REASONED_ADMISSIONS) - ADMITTED_ROSTER)}\n"
        "A REMOVAL deletes the record that an admission was ADJUDICATED, and the name "
        "goes on being admitted — by silence, which is the one thing this dict exists "
        "to prevent. An ADDITION needs a reason in the dict and a line in this literal."
    )
    assert "ToolSearch" in REASONED_ADMISSIONS["Skill"], (
        "`Skill`'s admission no longer names `ToolSearch`. The two are adjacent — both "
        "reach past the phase's stated tools — and the whole adjudication is the "
        "distinction between them: a skill injects INSTRUCTIONS and every tool it asks "
        "for must still be in `--tools`, while `ToolSearch` changes the CALLABLE SET. "
        "Without that contrast the entry reads as an admission by assertion."
    )


#: Gate-2 JR-19. WHAT EACH ADMISSION STANDS ON. Every entry in `REASONED_ADMISSIONS`
#: is admitted because some OTHER name is refused — that is the actual argument, and
#: until this mapping existed it was load-bearing prose held together by nothing.
#:
#: jack-ryan's measurement: replacing `ExitWorktree`'s or `TaskOutput`'s whole reason
#: with the word `"admitted"` SURVIVED at an unmoved 604. And the failure mode with
#: real reach is not a rewrite at all — it is a legal two-line REGRADE. Move `Task` out
#: of `UNFENCEABLE_TOOLS` and out of `REFUSED_ROSTER`, both of which are ordinary edits
#: a future round might make on good evidence, and three admissions are left standing
#: on a refusal that no longer exists. Nothing in the suite moves, because the coupling
#: lived in two literals that never referred to each other.
ADMISSION_DEPENDS_ON: dict[str, str] = {
    "Skill": "ToolSearch",
    "TaskOutput": "Task",
    "TaskStop": "Task",
    "ExitWorktree": "EnterWorktree",
}

#: The reason TEXT, pinned by digest. This is the one that closes jack-ryan's R21-A,
#: and it is here because their proposed fix does not — I checked before adopting it.
#:
#: Their suggestion was a row requiring each reason to NAME the refusal it depends on.
#: That closes R21-B and R21-C (reason replaced by `"admitted"`) and it closes the
#: regrade case, which is why `ADMISSION_DEPENDS_ON` above exists. It does NOT close
#: R21-A, whose whole point was that the token survives:
#:
#:     Skill's reason -> "is fine; ToolSearch is a different name"     SURVIVED, 604
#:
#: A name-check is a substring test, and R21-A keeps the substring. So is the
#: `"ToolSearch" in …` assert above — which is the finding, and adding a second
#: substring test of the same shape would have been the round-18 error again
#: (a weaker mutation reported as the stronger guard).
#:
#: A digest has no adjacent question to answer. Any rewrite fails it, which is the
#: point: these four sentences are an ADJUDICATION RECORD, and re-writing one is an
#: act that should have to be performed deliberately. Updating a digest is cheap and
#: the failure message prints the new one; what it cannot be is silent.
ADMISSION_REASON_DIGESTS: dict[str, str] = {
    "Skill": "e6571ed111d3f378",
    "TaskOutput": "321600055d095f5e",
    "TaskStop": "3de5b0142c2781ad",
    "ExitWorktree": "e56d9224e97f8aa7",
}


def test_JR19_every_admission_names_a_refusal_that_STILL_EXISTS():
    """The admissions are conditional, and until now nothing asserted the condition.

    `TaskOutput` is admitted because *"`Task` is refused above, and without a creator
    this is inert"*. `ExitWorktree` because *"`EnterWorktree` is refused above"*. Those
    are not decoration; they are the premises. `REFUSED_ROSTER` pinned the refusals in a
    DIFFERENT literal, so the coupling was real and stated nowhere — held by accident.

    This row asserts the link, so a regrade breaks loudly at the admission that depended
    on it rather than quietly at the fence.
    """
    assert set(ADMISSION_DEPENDS_ON) == set(REASONED_ADMISSIONS), (
        "the dependency map and the admissions have drifted apart.\n"
        f"  admissions without a stated dependency: "
        f"{sorted(set(REASONED_ADMISSIONS) - set(ADMISSION_DEPENDS_ON))}\n"
        f"  dependencies for names not admitted:    "
        f"{sorted(set(ADMISSION_DEPENDS_ON) - set(REASONED_ADMISSIONS))}\n"
        "A new admission must say what it stands on. That is the whole argument for "
        "admitting it."
    )
    for name, needed in sorted(ADMISSION_DEPENDS_ON.items()):
        assert needed in UNFENCEABLE_TOOLS, (
            f"`{name}` is admitted on the argument that `{needed}` is refused, and "
            f"`{needed}` is no longer in UNFENCEABLE_TOOLS. The admission is now "
            f"standing on a refusal that does not exist. This is the REGRADE case: "
            f"moving a name out of the refusals is a legal edit, and without this row "
            f"it leaves the reasoning behind, silently, in a different file."
        )
        assert needed in REASONED_ADMISSIONS[name], (
            f"`{name}`'s reason no longer names `{needed}`, which is what it depends "
            f"on. A reader cannot check an argument whose premise has been deleted.\n"
            f"  reason: {REASONED_ADMISSIONS[name]!r}"
        )


def test_JR19_no_admission_REASON_can_be_REWRITTEN_without_a_row_failing():
    """The case no substring assert reaches: the reason rewritten, the token kept.

    See `ADMISSION_REASON_DIGESTS` for why this is a digest and not a third name-check.
    """
    import hashlib

    observed = {
        name: hashlib.sha256(reason.encode()).hexdigest()[:16]
        for name, reason in REASONED_ADMISSIONS.items()
    }
    drifted = {n: (ADMISSION_REASON_DIGESTS.get(n), d) for n, d in observed.items()
               if ADMISSION_REASON_DIGESTS.get(n) != d}
    assert not drifted, (
        "an adjudication record was rewritten without the record of the adjudication "
        "being re-stated.\n"
        + "".join(
            f"  {n}: pinned {was!r} -> observed {now!r}\n     now reads: "
            f"{REASONED_ADMISSIONS[n]!r}\n"
            for n, (was, now) in sorted(drifted.items())
        )
        + "If the rewrite is intended, update the digest in this file — that edit IS "
        "the act of re-adjudicating, and it is the thing that must not happen by "
        "accident. If it is not intended, the reason has been changed underneath the "
        "argument that admitted the tool."
    )


def test_JR13_ToolSearch_is_refused_by_LITERAL_and_says_WHICH_KIND_of_entry_it_is(
    tmp_path, git_repo
):
    """`ToolSearch` hardcoded, and its PROVENANCE LABEL hardcoded with it.

    `Task` has a literal row because it is measured. `Agent` got one in round 18. The
    round's headline addition — four live probe calls, five preserved frame files — had
    neither, and the mutation table said it did.

    The second assertion is the one that earns its place. `ToolSearch` is the single
    entry in `UNFENCEABLE_TOOLS` that is REASONED rather than MEASURED: the probe was
    run four times and refused four times by the model's own safety classifier, while a
    control with identical argv returned cleanly (`jr7-toolsearch-control.jsonl`). That
    asymmetry is the whole disclosure, and it lives in a string. Pinning the label into
    the message a phase author reads means the entry cannot be quietly re-graded from
    reasoned to measured without frames to back it — rule 13, applied to the one entry
    in this module that does not have them.
    """
    phase = dict(AGENTIC_PHASE, tools=["ToolSearch"])
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    with pytest.raises(WorkflowError) as exc:
        load_workflow(path)
    message = str(exc.value)
    assert "this fence cannot hold" in message, (
        f"`ToolSearch` was not refused as unfenceable: {message}"
    )
    assert "REASONED, NOT MEASURED" in message, (
        "the refusal no longer tells its reader that this entry is reasoned rather "
        "than measured. That label is the JR-7 disclosure; without it the entry reads "
        "with the same authority as `Task`, which has frames."
    )


@pytest.mark.parametrize("name", sorted(UNFENCEABLE_TOOLS))
def test_J7_every_unfenceable_name_is_refused_at_LOAD(tmp_path, git_repo, name):
    """Parametrized over the dict itself, so a name added without a reason still fails.

    Hand-listing the names here would let the two lists drift, and the drift would
    show up as a tool that is documented as refused and is not.

    It cannot see a DELETION — rule 44, measured under JR-13. `REFUSED_ROSTER` above is
    the other half; this row and that literal are a pair and neither is sufficient.
    """
    phase = dict(AGENTIC_PHASE, tools=[name])
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    with pytest.raises(WorkflowError) as exc:
        load_workflow(path)
    message = str(exc.value)
    assert UNFENCEABLE_TOOLS[name] in message, "refused without saying what it reaches"
    assert "not in the built-in set" not in message, (
        "refused for the WRONG reason: this CLI does have this tool, and a message "
        "saying otherwise sends the reader to re-probe a vocabulary that is correct"
    )


def test_J7_the_refusal_survives_a_SCOPED_form_and_a_crowd(tmp_path, git_repo):
    """`Task(...)` and a Task buried among honest names.

    The vocabulary adjudicates the BASE name, and J1 established that the scope buys
    nothing — so a scoped `Task` is a bare `Task` wearing a fence's clothes. The crowd
    case is F4's `["Read", "default"]` lesson: the reviewer's eye stops at the first
    recognisable name.
    """
    for tools in (["Task(sub)"], ["Read", "Task"], ["Bash(git log:*)", "CronCreate"]):
        phase = dict(AGENTIC_PHASE, tools=tools)
        path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
        with pytest.raises(WorkflowError, match="this fence cannot hold"):
            load_workflow(path)


def test_J7_the_refused_names_are_names_this_CLI_ACTUALLY_HAS(tmp_path, git_repo):
    """The lists cannot drift apart — but "this CLI has it" has TWO channels.

    A name refused here and existing nowhere would be dead law that reads as diligence:
    the reason text would never be seen, and the force of J7 is that these are tools the
    CLI HAS. Refusing something absent proves nothing.

    Gate-2 JR-6 corrected the predicate rather than the list. This row asserted
    `UNFENCEABLE ⊆ BUILTIN`, on the reasoning that a name outside `BUILTIN_TOOLS` "does
    not exist". `BUILTIN_TOOLS` is what one init frame enumerated, which is the GRANT
    vocabulary; the invocation channel speaks other names, and `Agent` is one — proven
    by a frame in this repo. So the row that existed to keep two lists honest was
    forbidding the fence from refusing a name it had measured to exist. The one-way
    implication, read backwards, inside the check written to stop exactly that.
    """
    known = BUILTIN_TOOLS | set(INVOCATION_ONLY_TOOLS)
    orphans = sorted(set(UNFENCEABLE_TOOLS) - known)
    assert not orphans, (
        f"refused, but named by neither channel this CLI was measured on: {orphans}. "
        "A refusal for a name nothing has observed is dead law."
    )
    unreasoned = sorted(n for n, why in UNFENCEABLE_TOOLS.items() if not str(why).strip())
    assert not unreasoned, f"refused with no reason recorded: {unreasoned}"


def test_JR6_the_INVOCATION_names_are_not_grant_names_or_the_split_is_fiction(
    tmp_path, git_repo
):
    """`INVOCATION_ONLY_TOOLS` earns its name only if its members are not grantable.

    If a name drifts into both, the dict stops recording a two-channel split and starts
    being a second spelling of `BUILTIN_TOOLS` — at which point the JR-6 correction
    above silently widens back into the invariant it replaced, and nothing says so.
    """
    both = sorted(set(INVOCATION_ONLY_TOOLS) & BUILTIN_TOOLS)
    assert not both, (
        f"{both} are in BOTH the grant vocabulary and the invocation-only map. One of "
        "the two is wrong, and while they disagree the subset check above is meaningless."
    )
    unreasoned = sorted(
        n for n, why in INVOCATION_ONLY_TOOLS.items() if not str(why).strip()
    )
    assert not unreasoned, f"invocation-only with no provenance recorded: {unreasoned}"


def test_JR6_an_INVOCATION_name_is_refused_for_the_TRUE_reason(tmp_path, git_repo):
    """`Agent` — the name the frames show, refused without the false sentence.

    This is the row that makes the "refused BEFORE the membership check" ordering
    load-bearing (JR-8). While every refused name was also a `BUILTIN_TOOLS` member the
    ordering was inert by construction: jack-ryan moved the block below the membership
    check and a full 585-row suite stayed green. `Agent` is refused and is not a member,
    so position now decides which message a phase author reads — the true one, or the
    one that sends them to re-probe a vocabulary that is correct.
    """
    phase = dict(AGENTIC_PHASE, tools=["Agent"])
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    with pytest.raises(WorkflowError) as exc:
        load_workflow(path)
    message = str(exc.value)
    assert "this fence cannot hold" in message, (
        f"`Agent` was not refused as unfenceable: {message}"
    )
    assert "not in the built-in set" not in message, (
        "the loader told its reader this CLI does not have `Agent`. The frames in "
        "star-lord/notes/evidence/2026-08-11-tool-fence-probes/ show this CLI invoking "
        "it. That is the false sentence README rule 39 exists to forbid."
    )


def test_JR7_every_QUESTIONED_name_is_either_refused_or_admitted_WITH_A_REASON(
    tmp_path, git_repo
):
    """An admission by silence cannot be argued with; an admission with a reason can.

    `UNFENCEABLE_TOOLS` answers "are these unfenceable?" and `validate_tools` spends it
    as "the rest are fenceable" — the series' own predicate shape, on top of the J7 fix.
    The answer is not a bigger refusal list; it is a record of which admissions were
    adjudicated. This row holds the two maps apart and requires both to be reasoned. It
    does NOT claim the enumeration is complete, and no assertion here should ever be
    read as claiming it.
    """
    overlap = sorted(set(REASONED_ADMISSIONS) & set(UNFENCEABLE_TOOLS))
    assert not overlap, (
        f"{overlap} are recorded as BOTH refused and admitted. The fence cannot hold "
        "two answers to one question, and whichever one loses does so silently."
    )
    unknown = sorted(set(REASONED_ADMISSIONS) - BUILTIN_TOOLS)
    assert not unknown, (
        f"admitted with a reason, but not names this CLI's grant channel enumerated: "
        f"{unknown}. A reasoned admission of a name nothing can declare is noise."
    )
    unreasoned = sorted(
        n for n, why in REASONED_ADMISSIONS.items() if not str(why).strip()
    )
    assert not unreasoned, f"admitted with an EMPTY reason: {unreasoned}"


def test_JR7_the_reasoned_admissions_actually_LOAD(tmp_path, git_repo):
    """The falsification partner: a name recorded as admitted must really be admitted.

    Without this the two maps could agree perfectly with each other and disagree with
    `validate_tools` — the WIRING axis, which is where the J7 fix first landed wrong.
    """
    tools = sorted(REASONED_ADMISSIONS)
    phase = dict(AGENTIC_PHASE, tools=tools)
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    assert load_workflow(path).phases[0].tools == tools


def test_J7_the_MEASURED_name_is_refused_by_LITERAL_not_by_derivation(tmp_path, git_repo):
    """`Task` in this row's own text, because every other J7 row derives its names.

    The parametrized rows above iterate `UNFENCEABLE_TOOLS`. Delete `Task` from that
    dict and they do not fail — the parametrisation quietly loses a case and the suite
    stays green while the one name that was actually MEASURED walks back in. A row that
    derives its expectation from the code under test asserts that the code equals
    itself; here that would erase a finding, not just weaken a check.

    So this row hardcodes what the probe found. The frames are preserved at
    `star-lord/notes/evidence/2026-08-11-tool-fence-probes/j7-task-reach-probe.jsonl`:
    a parent granted `--tools Task` reported `tools: ['Task']` at `init` and spawned a
    child holding `Bash`, `Edit` and `Write`, `is_error: false`,
    `permission_denials: []`. If this row ever has to change, the frames are what it
    must be changed against.
    """
    phase = dict(AGENTIC_PHASE, tools=["Task"])
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    with pytest.raises(WorkflowError) as exc:
        load_workflow(path)
    assert "this fence cannot hold" in str(exc.value), (
        "the MEASURED unfenceable name loaded, or was refused on some other rule: "
        f"{exc.value}"
    )


def test_J7_the_fence_still_admits_the_tools_a_real_phase_needs(tmp_path, git_repo):
    """The refusal is worth nothing if it also refuses the working set.

    Named explicitly rather than derived, because a row that computes its own expected
    value from the code under test asserts that the code equals itself.
    """
    tools = ["Read", "Glob", "Grep", "Bash(git status:*)", "Write", "Edit", "TodoWrite"]
    phase = dict(AGENTIC_PHASE, tools=tools)
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    assert load_workflow(path).phases[0].tools == tools


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
