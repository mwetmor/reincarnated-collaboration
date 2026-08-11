"""Permissions fingerprinting — Spec A § 8 and § 11 acceptance item 4 (second half).

The centrepiece is `test_planted_write_outside_the_allowlist_aborts_and_rolls_back`:
a phase writes a file it never declared, and the run must ABORT (not retry), the
bytes must be quarantined, and the tree must come back clean.

The rest are the safety rules that keep the containment from becoming its own
accident: pre-existing dirt is never restored over, committed paths are never
unwound, protected paths cannot be opted into by config.
"""

import dataclasses
import os
import json
import subprocess
from pathlib import Path

import pytest

from factory import permissions as perm
from factory.runner import Runner
from factory.workflow import load_workflow


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _write_workflow(tmp_path: Path, repo: Path, phase: dict) -> Path:
    doc = {
        "name": "breachtest",
        "root": str(repo),
        "repos": [str(repo)],
        "phases": [phase],
    }
    path = tmp_path / "wf.json"
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _run(tmp_path: Path, repo: Path, phase: dict):
    wf = load_workflow(_write_workflow(tmp_path, repo, phase))
    runner = Runner(wf, factory_dir=tmp_path / "factory_home", verbose=False)
    try:
        return runner.run()
    finally:
        runner.close()


def _sh(command: str) -> dict:
    return {"gate": "command_succeeds", "args": {"command": f"sh -c '{command}'"}}


# ---------------------------------------------------------------------------
# the acceptance test
# ---------------------------------------------------------------------------
def test_planted_write_outside_the_allowlist_aborts_and_rolls_back(tmp_path, git_repo):
    result = _run(
        tmp_path,
        git_repo,
        {
            "name": "sneaky",
            "writes": ["allowed/**"],
            "retries": 1,  # a breach must NOT consume this
            "artifacts": ["allowed/declared.txt"],
            "gates": [_sh("mkdir -p allowed && echo ok > allowed/declared.txt && "
                          "echo gotcha > not_declared.txt")],
        },
    )

    assert result.status == "ABORTED", f"expected ABORTED, got {result.status}"
    assert "permissions breach" in (result.abort_reason or "")

    # the undeclared write is gone from the tree
    assert not (git_repo / "not_declared.txt").exists(), (
        "the breaching file survived rollback"
    )
    # ...but its bytes were kept as evidence before deletion
    quarantined = list((result.session_dir / "breach").rglob("not_declared.txt"))
    assert quarantined, "breaching bytes were deleted without being quarantined"
    assert quarantined[0].read_text().strip() == "gotcha"

    breach_json = list((result.session_dir / "breach").rglob("BREACH.json"))
    assert breach_json, "no BREACH.json written"
    record = json.loads(breach_json[0].read_text())
    assert record["writes_allowlist"] == ["allowed/**"]
    assert any("not_declared.txt" in b for b in record["breaches"])


def test_a_breach_is_never_retried(tmp_path, git_repo):
    result = _run(
        tmp_path,
        git_repo,
        {
            "name": "sneaky",
            "writes": ["allowed/**"],
            "retries": 3,
            "gates": [_sh("echo gotcha > not_declared.txt")],
        },
    )
    assert result.status == "ABORTED"
    assert result.outcomes[0].attempts == 1, (
        "a permissions breach consumed a retry — a breach is evidence, not a retry"
    )


def test_a_declared_write_does_not_abort(tmp_path, git_repo):
    """The falsification partner: the same machinery must let a legal write through."""
    result = _run(
        tmp_path,
        git_repo,
        {
            "name": "tidy",
            "writes": ["allowed/**"],
            "artifacts": ["allowed/declared.txt"],
            "gates": [
                _sh("mkdir -p allowed && echo ok > allowed/declared.txt"),
                "artifacts_exist",
                "files_non_empty",
            ],
        },
    )
    assert result.status == "PASS", f"legal write was blocked: {result.abort_reason}"
    assert (git_repo / "allowed" / "declared.txt").exists()


# ---------------------------------------------------------------------------
# classify — the rules that cannot be configured away
# ---------------------------------------------------------------------------
def _change(root: Path, path: str, kind: str = "created") -> perm.Change:
    return perm.Change(root=root, path=path, kind=kind, before_status=None, after_status="??")


@pytest.mark.parametrize(
    "path",
    ["agentic_orchestration/factory/gates/core.py", "canonical/00-ground-state.md",
     ".claude/settings.json"],
)
def test_protected_paths_breach_even_when_the_allowlist_names_them(tmp_path, path):
    root = tmp_path
    allowed, breaches = perm.classify([_change(root, path)], writes=["**"], root=root)
    assert not allowed
    assert len(breaches) == 1
    assert "always-protected" in breaches[0].reason


def test_write_inside_a_NESTED_read_only_tree_is_a_breach(tmp_path):
    """Gate-2 re-review G2. Read-only was matched on `change.root`, which is ALWAYS a
    whole repo root — so a read-only tree declared as a subdirectory matched nothing
    and was enforced nowhere, while the loader accepted it without complaint."""
    root = tmp_path / "engine"
    (root / "seasons").mkdir(parents=True)
    allowed, breaches = perm.classify(
        [_change(root, "seasons/001.json")],
        writes=["**"],
        root=root,
        read_only_trees=[root / "seasons"],
    )
    assert not allowed
    assert "read-only tree" in breaches[0].reason


def test_a_write_beside_a_nested_read_only_tree_is_still_allowed(tmp_path):
    """The falsification partner: nesting narrows the fence, it does not close the
    whole repo. Without this, 'everything breaches' would pass the test above."""
    root = tmp_path / "engine"
    (root / "seasons").mkdir(parents=True)
    (root / "src").mkdir()
    allowed, breaches = perm.classify(
        [_change(root, "src/whatever.py")],
        writes=["src/**"],
        root=root,
        read_only_trees=[root / "seasons"],
    )
    assert len(allowed) == 1 and not breaches


def test_a_collapsed_entry_ABOVE_a_read_only_tree_breaches(tmp_path):
    """Git reports a wholly-untracked directory as one line, so a change entry can be
    an ANCESTOR of the read-only tree. Which members moved is unknowable from the
    entry, so it fails closed — otherwise a collapsed ancestor smuggles writes into
    a protected subtree."""
    root = tmp_path / "engine"
    (root / "data" / "protected").mkdir(parents=True)
    allowed, breaches = perm.classify(
        [_change(root, "data/")],
        writes=["**"],
        root=root,
        read_only_trees=[root / "data" / "protected"],
    )
    assert not allowed
    assert "collapsed entry" in breaches[0].reason


def test_write_inside_a_read_only_tree_is_a_breach(tmp_path):
    root = tmp_path / "meta"
    engine = tmp_path / "engine"
    root.mkdir()
    engine.mkdir()
    allowed, breaches = perm.classify(
        [_change(engine, "src/whatever.py")],
        writes=["**"],
        root=root,
        read_only_trees=[engine],
    )
    assert not allowed
    assert "read-only tree" in breaches[0].reason


def test_allowlist_accepts_directory_prefixes_and_globs(tmp_path):
    root = tmp_path
    changes = [
        _change(root, "out/season/001.json"),
        _change(root, "notes/x.md"),
    ]
    allowed, breaches = perm.classify(changes, writes=["out/", "notes/*.md"], root=root)
    assert len(allowed) == 2
    assert not breaches


# ---------------------------------------------------------------------------
# rollback safety
# ---------------------------------------------------------------------------
def test_rollback_never_restores_over_pre_existing_dirt(tmp_path, git_repo):
    """A path already dirty at phase start is baseline, not the phase's doing."""
    (git_repo / "tracked.txt").write_text("edited by the human, before the phase\n")
    before = {str(git_repo): perm.fingerprint(git_repo)}
    assert "tracked.txt" in before[str(git_repo)].entries

    breach = perm.Breach(
        _change(git_repo, "tracked.txt", kind="modified"), "outside the allowlist"
    )
    actions = perm.rollback([breach], before, tmp_path / "q")

    assert actions[0].action == "NOT_ROLLED_BACK"
    assert "already dirty" in actions[0].reason
    assert (git_repo / "tracked.txt").read_text().startswith("edited by the human")
    assert actions[0].quarantined_to, "evidence should still have been quarantined"


def test_rollback_will_not_unwind_a_commit(tmp_path, git_repo):
    before = {str(git_repo): perm.fingerprint(git_repo)}
    breach = perm.Breach(_change(git_repo, "tracked.txt", kind="committed"), "committed")
    actions = perm.rollback([breach], before, tmp_path / "q")
    assert actions[0].action == "NOT_ROLLED_BACK"
    assert "human decision" in actions[0].reason


def test_rollback_deletes_only_what_the_phase_created(tmp_path, git_repo):
    before = {str(git_repo): perm.fingerprint(git_repo)}
    (git_repo / "new.txt").write_text("phase output\n")
    breach = perm.Breach(_change(git_repo, "new.txt", kind="created"), "outside the allowlist")
    actions = perm.rollback([breach], before, tmp_path / "q")
    assert actions[0].action == "deleted"
    assert not (git_repo / "new.txt").exists()
    assert Path(actions[0].quarantined_to).read_text() == "phase output\n"


# ---------------------------------------------------------------------------
# fingerprint mechanics
# ---------------------------------------------------------------------------
def test_fingerprint_sees_a_new_file(git_repo):
    before = perm.fingerprint(git_repo)
    (git_repo / "visible.txt").write_text("x\n")
    after = perm.fingerprint(git_repo)
    assert "visible.txt" in {c.path for c in perm.diff_fingerprints(before, after)}


# ---------------------------------------------------------------------------
# gitignored writes — Gate-2 F1
#
# The v1 build exempted gitignored paths as a CATEGORY in order to stop the
# factory's own sessions/ writes reading as self-breach. That exempted every
# gitignored path in every tree, including the engine's seasons/ (3.3 GB) and
# telemetry.db — inside the tree the workflow declares read-only. The exemption
# is now by NAMED PATH. These tests hold that line from both sides.
# ---------------------------------------------------------------------------
def test_a_gitignored_write_is_a_tree_change(git_repo):
    """The falsification partner of the exemption below. Ignored by git is not the
    same as permitted by the factory — git's opinion about version control says
    nothing about whether a phase was allowed to write there."""
    before = perm.fingerprint(git_repo)
    (git_repo / "ignored").mkdir()
    (git_repo / "ignored" / "noise.txt").write_text("y\n")
    after = perm.fingerprint(git_repo)

    paths = {c.path for c in perm.diff_fingerprints(before, after)}
    assert any(p.startswith("ignored") for p in paths), (
        "a gitignored write escaped the fingerprint — this is the F1 fail-open: "
        "the engine's seasons/ and telemetry.db live behind exactly this rule"
    )


def _with_factory_skeleton(root: Path) -> Path:
    """Mirror the meta-repo's real shape: a TRACKED `agentic_orchestration/factory/`
    with a gitignored `sessions/` inside it.

    The tracked parents matter. Git collapses a wholly-untracked directory to a
    single porcelain line, so without a committed ancestor every one of these tests
    would be measuring git's collapsing behaviour instead of the exemption.
    """
    factory = root / "agentic_orchestration" / "factory"
    (factory / "sessions").mkdir(parents=True)
    (factory / "gates.py").write_text("def real_gate(): ...\n")
    (root / ".gitignore").write_text(
        "ignored/\nagentic_orchestration/factory/sessions/\n"
    )

    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=str(root), check=True, capture_output=True)

    git("add", ".gitignore", "agentic_orchestration/factory/gates.py")
    git("commit", "-q", "-m", "factory skeleton")
    return factory


def test_only_the_factorys_own_runtime_paths_are_exempt(git_repo):
    """The exemption exists so the factory's receipts do not read as self-breach. It
    is scoped to named paths, so it cannot grow to cover anything else."""
    factory = _with_factory_skeleton(git_repo)

    before = perm.fingerprint(git_repo, is_root_repo=True)
    (factory / "sessions" / "run-1.json").write_text("receipt\n")
    (git_repo / "ignored").mkdir(exist_ok=True)
    (git_repo / "ignored" / "noise.txt").write_text("y\n")
    after = perm.fingerprint(git_repo, is_root_repo=True)

    paths = {c.path for c in perm.diff_fingerprints(before, after)}
    assert not any("factory/sessions" in p for p in paths), "the factory's own receipts"
    assert any(p.startswith("ignored") for p in paths), (
        "the exemption is by named path; every other ignored path stays measured"
    )
    assert any("factory/sessions" in e for e in after.exempted), (
        "an exemption taken is an exemption recorded — it is never silent. "
        "(`before` records none: git does not report an empty directory at all.)"
    )


def test_the_factory_exemption_does_not_apply_to_other_repos(git_repo):
    """Only the root repo holds the factory. The same path in a declared read-only
    tree is somebody else's directory and is measured like any other."""
    factory = _with_factory_skeleton(git_repo)

    before = perm.fingerprint(git_repo, is_root_repo=False)
    (factory / "sessions" / "run-1.json").write_text("receipt\n")
    after = perm.fingerprint(git_repo, is_root_repo=False)

    paths = {c.path for c in perm.diff_fingerprints(before, after)}
    assert any("factory/sessions" in p for p in paths)
    assert before.exempted == [], "a non-root repo gets no exemptions at all"


def test_factory_source_is_still_visible_under_the_exempt_directory(git_repo):
    """The exemption covers the factory's runtime writes, not the factory. A phase
    that rewrites the spine is still a breach."""
    factory = _with_factory_skeleton(git_repo)

    before = perm.fingerprint(git_repo, is_root_repo=True)
    (factory / "gates.py").write_text("def always_pass(): return True\n")
    after = perm.fingerprint(git_repo, is_root_repo=True)

    paths = {c.path for c in perm.diff_fingerprints(before, after)}
    assert any(p.endswith("factory/gates.py") for p in paths), "self-modification"


# ---------------------------------------------------------------------------
# the exact/coarse tier — what a containment claim is WORTH
#
# A region too large to stat file-by-file used to stop at the cap and report a
# truncated signature, which made everything past the cap invisible to the diff.
# It now falls back to directory mtimes. That catches less, and says so.
# ---------------------------------------------------------------------------
def _big_region(root: Path, files: int) -> Path:
    region = root / "huge"
    region.mkdir()
    for i in range(files):
        (region / f"f{i}.dat").write_text(str(i))
    return region


def test_a_region_within_the_cap_is_measured_exactly(git_repo):
    _big_region(git_repo, 5)
    sig, mode = perm._walk_signature(git_repo / "huge", cap=100)
    assert mode == perm.EXACT
    assert sig.startswith("dir:5:")


def test_a_region_past_the_cap_falls_back_to_coarse_and_is_labelled(git_repo):
    _big_region(git_repo, 20)
    sig, mode = perm._walk_signature(git_repo / "huge", cap=5)
    assert mode == perm.COARSE
    assert sig.startswith("coarse:"), "the signature itself names the weaker method"


def test_coarse_measurement_still_catches_a_file_created_past_the_cap(git_repo):
    """The point of the fallback. The old truncating sweep saw nothing here."""
    region = _big_region(git_repo, 20)
    before, _ = perm._walk_signature(region, cap=5)
    (region / "planted.txt").write_text("an agent wrote where it was told not to\n")
    after, mode = perm._walk_signature(region, cap=5)
    assert mode == perm.COARSE
    assert before != after


def test_coarse_measurement_catches_a_deletion_past_the_cap(git_repo):
    region = _big_region(git_repo, 20)
    before, _ = perm._walk_signature(region, cap=5)
    (region / "f19.dat").unlink()
    after, _ = perm._walk_signature(region, cap=5)
    assert before != after


def test_coarse_measurement_does_NOT_catch_an_in_place_content_edit(git_repo):
    """The blind spot, pinned deliberately.

    This is the cost of the fallback, and it is asserted rather than hoped about:
    if a future change makes coarse measurement catch content edits, this test goes
    red and the receipts' `containment_coarse` caveat can be weakened on evidence.
    Until then the caveat is accurate, which is the only thing that matters.
    """
    region = _big_region(git_repo, 20)
    target = region / "f3.dat"
    edited = "x" * len(target.read_text())   # same length, same directory entry
    before, _ = perm._walk_signature(region, cap=5)
    target.write_text(edited)                # rewrites the inode, not the dir entry
    after, _ = perm._walk_signature(region, cap=5)
    assert before == after, (
        "coarse measurement is blind to in-place edits — the `containment_coarse` "
        "receipt says exactly this, and it must stay true"
    )


def test_an_oversized_region_is_reported_on_the_fingerprint_as_coarse(git_repo, monkeypatch):
    monkeypatch.setattr(perm, "_IGNORED_SCAN_CAP", 3)
    _big_region(git_repo, 10)
    fp = perm.fingerprint(git_repo)
    assert fp.coarse, "the fingerprint declares which regions got the weaker method"
    assert fp.usable, "coarse is a weaker measurement, NOT a containment failure"


def test_a_collapsed_untracked_directory_is_swept_not_skipped(git_repo):
    """Git reports a wholly-untracked directory as ONE line. The exemption is a
    prefix match on that line, so a collapsed ancestor never matches and the whole
    region is swept — the containment fails CLOSED under collapsing, not open."""
    buried = git_repo / "agentic_orchestration" / "factory" / "sessions"
    buried.mkdir(parents=True)

    before = perm.fingerprint(git_repo, is_root_repo=True)
    (buried / "deep.json").write_text("written inside a collapsed dir\n")
    after = perm.fingerprint(git_repo, is_root_repo=True)

    changes = perm.diff_fingerprints(before, after)
    assert [c.path for c in changes] == ["agentic_orchestration/"], (
        "the write is reported at the collapsed ancestor, and it IS reported"
    )


def test_fingerprinting_a_SUBDIRECTORY_is_a_containment_failure(git_repo):
    """Gate-2 re-review G1, defence in depth. The loader refuses this, but the
    loader is not the only caller. `git status` emits worktree-root-relative paths,
    so a subdirectory fingerprint joins every one against the wrong base and stats
    nothing — it would have come back `usable=True` with every signature empty."""
    sub = git_repo / "sub"
    sub.mkdir()
    (sub / "planted.txt").write_text("a write that must not vanish\n")

    fp = perm.fingerprint(sub)
    assert fp.usable is False, "a subdirectory fingerprint measures nothing"
    assert "not a git worktree root" in (fp.error or "")
    with pytest.raises(perm.ContainmentError):
        perm.diff_fingerprints(fp, fp)


def test_an_unmeasurable_tree_raises_rather_than_reading_as_clean(tmp_path):
    """A non-git directory produces no change-set. The v1 build recorded that
    honestly and then never read it, so the empty diff was indistinguishable from
    innocence — Gate-2 F2. Now it stops the run."""
    fp = perm.fingerprint(tmp_path)
    assert fp.is_git is False
    assert fp.usable is False
    with pytest.raises(perm.ContainmentError, match="not a git worktree"):
        perm.diff_fingerprints(fp, fp)


def test_a_tree_that_errored_mid_run_also_raises(git_repo):
    """Not just non-git: any snapshot that failed to measure. A tree that vanished
    or went unreadable between snapshots must abort, not diff to nothing."""
    good = perm.fingerprint(git_repo)
    broken = dataclasses.replace(good, error="fatal: unable to read index")
    assert broken.usable is False
    with pytest.raises(perm.ContainmentError):
        perm.diff_fingerprints(good, broken)


def test_fingerprint_detects_content_change_in_a_tracked_file(git_repo):
    before = perm.fingerprint(git_repo)
    (git_repo / "tracked.txt").write_text("changed\n")
    after = perm.fingerprint(git_repo)
    changes = perm.diff_fingerprints(before, after)
    assert [c.path for c in changes] == ["tracked.txt"]


def test_fingerprint_detects_a_commit_made_during_the_window(git_repo):
    before = perm.fingerprint(git_repo)
    (git_repo / "sneaky.txt").write_text("committed behind our back\n")
    subprocess.run(["git", "add", "sneaky.txt"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "sneak"], cwd=git_repo, check=True, capture_output=True
    )
    after = perm.fingerprint(git_repo)
    changes = perm.diff_fingerprints(before, after)
    assert any(c.kind == "committed" and c.path == "sneaky.txt" for c in changes)


# ---------------------------------------------------------------------------
# Gate-2 L2 — the status-code classifier, over its WHOLE domain
#
# These are unit tests rather than wall rows, and the reason is a real limit on
# what the wall can do. The wall plants artifacts and asks what containment makes
# of them, so it can only ever reach status codes git actually emits. L2's defect
# lived in the classifier's DEFAULT — the branch taken by codes nobody enumerated
# — and a mutation restoring that default (`return "modified"` as the catch-all)
# changes the answer for 41 two-character codes while leaving all 362 wall rows
# green, because no planted artifact can produce any of them.
#
# A default-fail is a claim about inputs that have not happened yet. It cannot be
# tested by an artifact; it has to be tested by the alphabet.
# ---------------------------------------------------------------------------

#: Every code git's `status --porcelain` can put in front of a NEW entry, and what
#: containment must make of it. Written out rather than computed, so the table is
#: readable as a specification and cannot agree with the code by construction.
_KIND_BY_CODE = {
    "??": "created",   # untracked
    "!!": "created",   # ignored
    "!?": "created",
    "A ": "created",   # staged addition — the disciplined agent (L3)
    "AM": "created",
    "AT": "created",
    "R ": "created",   # rename DESTINATION — the file did not exist before (L2)
    "RM": "created",
    "RT": "created",
    "C ": "created",   # copy destination — likewise
    "CM": "created",
    "CT": "created",
    " M": "modified",
    "M ": "modified",
    "MM": "modified",
    " T": "modified",  # type change
    "T ": "modified",
    "TT": "modified",
    "MT": "modified",
    "TM": "modified",
    " D": "deleted",
    "D ": "deleted",   # staged deletion
    "MD": "deleted",
    "TD": "deleted",
}

#: Staged, then removed from disk. Nothing on disk to undo AND a dirty index: no
#: verb this module owns is right, so these must come back `unknown` rather than
#: send a guess to a destructive verb.
_STAGED_THEN_DELETED = ("AD", "RD", "CD")


def test_L2_every_status_code_git_emits_is_classified_as_the_thing_it_IS():
    """The rename destination is the row this table exists for.

    `R ` contains no `A` and does not begin with `D`, so the first enumeration fell
    through to a `modified` default — and `modified` is restored with
    `git checkout --`, which restored the file FROM THE INDEX THE PHASE HAD JUST
    STAGED and wrote `restored` on the receipt. The artifact survived, unchanged,
    under a receipt saying it had been undone.
    """
    wrong = {
        code: (perm._kind_of_new_entry(code), expected)
        for code, expected in _KIND_BY_CODE.items()
        if perm._kind_of_new_entry(code) != expected
    }
    assert not wrong, (
        "status codes classified as something other than what they are — "
        + "; ".join(f"{c!r}: got {got!r}, want {want!r}" for c, (got, want) in wrong.items())
    )


def test_L2_the_classifier_is_a_CLOSED_enumeration_over_the_whole_alphabet():
    """Everything NOT in the table above must come back `unknown`, which the
    rollback refuses by name. This is the assertion the wall structurally cannot
    make: it fixes the behaviour of inputs no artifact can currently produce, which
    is exactly the population the next git version adds to.
    """
    alphabet = " MTADRCU?!"
    for code in _STAGED_THEN_DELETED:
        assert perm._kind_of_new_entry(code) == "unknown", (
            f"{code!r} means the phase staged a creation and then removed it from "
            "disk. There is nothing on disk to undo and the index is dirty; a "
            "confident kind here sends a guess to a destructive verb"
        )
    leaked = {
        x + y: perm._kind_of_new_entry(x + y)
        for x in alphabet
        for y in alphabet
        if (x + y) not in _KIND_BY_CODE and perm._kind_of_new_entry(x + y) != "unknown"
    }
    assert not leaked, (
        f"{len(leaked)} unenumerated status code(s) were given a confident kind "
        f"instead of `unknown`: {leaked}. A code nobody enumerated is a code nobody "
        "has reasoned about, and the safe answer is to refuse it by name — not to "
        "guess `modified` and hand it to `git checkout --`."
    )


def test_L2_unmerged_codes_are_unknown_rather_than_guessed():
    """A conflicted path is mid-merge. There is no single `before` to restore to,
    so containment must refuse rather than pick one."""
    for code in sorted(perm.UNMERGED_CODES):
        assert perm._kind_of_new_entry(code) == "unknown", (
            f"unmerged code {code!r} was classified confidently; a conflicted path "
            "has no unambiguous prior state to be restored to"
        )


# ---------------------------------------------------------------------------
# Gate-2 L8 — the two states the WALL cannot plant
#
# The wall plants artifacts in a healthy repo, so it can only reach conditions a
# healthy repo produces. Neither of these is one: a repo where git REFUSES the
# question, and a repo with no commits at all. Round seven's mutation table caught
# both as survivors — the guard was correct in each case and nothing was holding it
# there, which is the same "absence reads as a pass" shape one tier down.
# ---------------------------------------------------------------------------
def test_L8_a_question_git_REFUSES_to_answer_is_not_a_no(tmp_path, git_repo, monkeypatch):
    """`git checkout --` ACTS. So an unanswered question cannot be filed as `no`.

    Every other default-fail branch in this module already works this way; the
    staging guard is the newest one, and the newest guard is the one whose
    not-knowing case has never been exercised.
    """
    # The baseline is taken FIRST. Dirtying the file before the snapshot makes it
    # dirty-at-phase-start, and such a path is dropped long before any verb is
    # chosen — the same masking that hid L8 for six rounds.
    before = {str(git_repo): perm.fingerprint(git_repo)}
    (git_repo / "tracked.txt").write_text("the phase rewrote this\n")
    real_git = perm._git

    def failing_diff(root, *args, **kwargs):
        if args[:2] == ("diff", "--cached"):
            return subprocess.CompletedProcess(
                args=list(args), returncode=128, stdout="",
                stderr="fatal: this operation must be run in a work tree",
            )
        return real_git(root, *args, **kwargs)

    monkeypatch.setattr(perm, "_git", failing_diff)
    breach = perm.Breach(
        perm.Change(root=git_repo, path="tracked.txt", kind="modified",
                    before_status=None, after_status=" M"),
        "outside the allowlist",
    )
    actions = perm.rollback([breach], before, tmp_path / "q")
    assert actions[0].action == "NOT_ROLLED_BACK", (
        "git refused to say whether its index differs from HEAD, and containment "
        "ran `git checkout --` anyway. Not-knowing is not a `no` for a verb that "
        f"writes the worktree from the index. Action was {actions[0]!r}"
    )
    assert "could not say" in (actions[0].reason or ""), (
        f"the refusal must name the unanswered question. Reason: {actions[0].reason}"
    )


def test_B3_staging_ELSEWHERE_does_not_stop_the_rollback_acting_HERE(tmp_path, git_repo):
    """The staging guard's falsification partner — the branch where it must say NO.

    Every staged-* row proves the guard REFUSES. None proved it PROCEEDS when the
    staging is somewhere else, so nothing in 410 tests distinguished "the index
    differs from HEAD **under this path**" from "**anywhere in the repo**". Dropping
    the `-- <rel>` pathspec left the suite green while turning the guard repo-wide:
    one staged file anywhere and every rollback refuses, every breach stands, and
    containment reports itself contained (Gate-2 B3).

    A predicate ships with both branches held: one row where it answers yes and the
    verb refuses, one where it answers no and the verb acts.
    """
    before = {str(git_repo): perm.fingerprint(git_repo)}
    (git_repo / "tracked.txt").write_text("the phase rewrote this\n")   # the breach
    (git_repo / ".gitignore").write_text("ignored/\nphase-added-line\n")
    subprocess.run(["git", "add", ".gitignore"], cwd=str(git_repo), check=True,
                   capture_output=True)                                  # staged ELSEWHERE

    breach = perm.Breach(
        perm.Change(root=git_repo, path="tracked.txt", kind="modified",
                    before_status=None, after_status=" M"),
        "outside the allowlist",
    )
    actions = perm.rollback([breach], before, tmp_path / "q")
    assert actions[0].action == "restored", (
        "a file staged ELSEWHERE in the repo made the staging guard refuse to roll "
        "back an unstaged breach HERE. The guard's pathspec is what keeps it a "
        f"question about this path; without it every breach stands. Action was "
        f"{actions[0]!r}"
    )
    assert (git_repo / "tracked.txt").read_text() == "baseline\n", (
        "the rollback reported `restored` without restoring the baseline content"
    )


def test_L8_with_NO_COMMITS_the_index_still_holds_the_phases_own_work(tmp_path):
    """Unborn HEAD is a real answer, not a refusal — and the answer is not `no`.

    With nothing committed, everything the index holds differs from HEAD, so
    `git checkout -- <path>` restores the phase's own staged bytes and calls it
    `restored`. The `rev-parse HEAD` probe returning non-zero is the branch that
    decides this, and it is the branch a repo with commits never reaches.
    """
    root = tmp_path / "unborn"
    root.mkdir()
    for args in (("init", "-q"), ("config", "user.email", "t@example.invalid"),
                 ("config", "user.name", "t")):
        subprocess.run(["git", *args], cwd=str(root), check=True, capture_output=True)
    (root / "staged.txt").write_text("THE PHASE STAGED THIS\n")
    subprocess.run(["git", "add", "staged.txt"], cwd=str(root), check=True,
                   capture_output=True)

    staged = perm._staged_against_head(root, "staged.txt")
    assert staged, (
        "with an unborn HEAD the index holds content HEAD does not, so the staging "
        f"guard must answer yes. It answered {staged!r}"
    )
    assert not staged.unanswered, (
        "an unborn HEAD is the real answer 'nothing is committed yet', not a git "
        f"refusal. Recorded as unanswered: {staged.unanswered!r}"
    )


# ---------------------------------------------------------------------------
# Gate-2 B2 — an assertion that cannot fire is not coverage
# ---------------------------------------------------------------------------
# The phrase scanner that stood here is DELETED, not moved. It regex-matched the
# wall for `if "<phrase>" in reason:` gates and checked the phrase still existed in
# permissions.py. Gate-2 C2 read it as a gate with no power, and the mechanism that
# replaced it settled the question by measurement: the assertion inside that
# scanner's loop had never executed, in any run, because the scanner collected zero
# phrases from the wall. The check written to catch dead assertions was one.
#
# Its invariant is not lost — it is subsumed and widened. An assertion gated on a
# phrase the product can no longer emit is unreachable, so no row reaches it, so
# `tests/test_reach_audit.py` reports it by file and line. That covers the single
# quotes, the aliased variable, the other four test files and the shapes nobody
# thought to write a pattern for, none of which the regex could see.


# ---------------------------------------------------------------------------
# Gate-2 L6 — a refusal the operator never sees is a refusal that did not happen
# ---------------------------------------------------------------------------
def test_L6_paths_the_rollback_REFUSED_to_undo_are_named_in_the_receipts(tmp_path, git_repo):
    """Containment deliberately leaves some artifacts in place — a staged write it
    will not unstage, tracked content it will not delete. Each refusal carries a
    reason, and for five rounds those reasons went into a list that was returned and
    dropped. The abort report said the run was contained; nothing said the tree was
    not clean.

    An artifact left on disk with a stated reason is fine. An artifact left on disk
    with a stated reason NOBODY READS is a fail-open with paperwork.
    """
    result = _run(
        tmp_path,
        git_repo,
        {
            "name": "disciplined-breacher",
            "writes": ["allowed/**"],
            "retries": 1,
            # The phase STAGES its undeclared write. Containment refuses to unstage
            # it — correctly — so this run aborts with the artifact still present.
            "gates": [_sh("echo gotcha > not_declared.txt && git add -- not_declared.txt")],
        },
    )
    assert result.status == "ABORTED", f"expected ABORTED, got {result.status}"

    events = _containment_events(tmp_path, result.run_id)
    kinds = {k for k, _ in events}
    assert "containment_not_undone" in kinds, (
        "the rollback refused to undo a breaching path and the receipts do not say "
        f"so. Event kinds recorded were: {sorted(kinds)}"
    )
    detail = next(d for k, d in events if k == "containment_not_undone")
    assert "not_declared.txt" in detail, (
        "the receipts record that something was not undone without naming WHICH "
        f"path: {detail}"
    )
    assert (git_repo / "not_declared.txt").exists(), (
        "the premise failed — containment DID undo the staged write, so this test is "
        "no longer exercising the not-undone path"
    )


def _containment_events(tmp_path: Path, run_id: str) -> list[tuple[str, str]]:
    """Straight out of the one data path the report is a view of."""
    import sqlite3

    db = tmp_path / "factory_home" / "receipts.db"
    assert db.exists(), f"no receipts db at {db}"
    con = sqlite3.connect(db)
    try:
        return [
            (k, d)
            for k, d in con.execute(
                "SELECT kind, detail FROM events WHERE run_id = ?", (run_id,)
            )
        ]
    finally:
        con.close()


def _assert_counted_claim_is_certified(action, repo, expect_guard: str) -> None:
    """A guard that makes a COUNTED claim carries the counts — always.

    Gate-2 C1. Round nine's P1/P2/P6 dropped or falsified the measurements only when
    `staged_paths == 0`, and 412 tests stayed green. The wall's rows all happen to
    have staged content, so the two states where nothing is staged — an ordinary
    destroyer refusal, and the branch where git REFUSED the question — were reached
    by no assertion at all. The trigger was fixed in round ten (guard identity, not a
    certified value) and these are the rows that make it reachable.
    """
    assert action.guard == expect_guard, (
        f"expected the {expect_guard} guard to refuse {action.path!r}; got "
        f"{action.guard!r}. Reason was: {action.reason}"
    )
    assert action.facts, (
        f"the {expect_guard} guard refused {action.path!r} while telling the operator "
        "how many files git holds, and carried no measurements. Nothing is staged "
        "here, which is exactly the state round nine's mutations exploited."
    )
    held = perm._tracked_under(repo, action.path)
    expected = {
        "head_files": len(held.in_head),
        "index_files": len(held.in_index),
        "staged_paths": len(perm._staged_against_head(repo, action.path).paths),
    }
    assert dict(action.facts) == expected, (
        f"the {expect_guard} refusal carries {dict(action.facts)}; git says {expected}."
    )
    rendered = perm.render_containment_facts(tuple(expected.items()))
    assert rendered, (
        "the renderer produced an empty clause, and an empty string is `in` every "
        "reason ever written. F1: the delivery check has to have something to find."
    )
    assert rendered in (action.reason or ""), (
        f"the {expect_guard} refusal does not state the facts it rests on. "
        f"Reason was: {action.reason}"
    )


def test_C1_the_DESTROYER_guard_carries_its_counts_when_NOTHING_is_staged(tmp_path, git_repo):
    """The ordinary destroyer case: committed content, clean index, `created` claimed.

    `staged_paths` is 0 here, so any check triggered on it certifies nothing — and
    this is the refusal that tells an operator "deleting it would destroy committed
    work". That sentence is the whole reason the guard exists.
    """
    (git_repo / "pkg").mkdir()
    (git_repo / "pkg" / "mod.py").write_text("committed work\n")
    subprocess.run(["git", "add", "pkg"], cwd=str(git_repo), check=True, capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", "pkg"], cwd=str(git_repo), check=True,
                   capture_output=True)
    before = {str(git_repo): perm.fingerprint(git_repo)}

    breach = perm.Breach(
        perm.Change(root=git_repo, path="pkg", kind="created",
                    before_status=None, after_status="??"),
        "outside the allowlist",
    )
    actions = perm.rollback([breach], before, tmp_path / "q")

    assert actions[0].action == "NOT_ROLLED_BACK", (
        "a path reported as `created` holds content git has committed — the "
        f"identification is wrong and deleting it destroys work. Action: {actions[0]!r}"
    )
    assert (git_repo / "pkg" / "mod.py").exists(), "committed work was deleted"
    _assert_counted_claim_is_certified(actions[0], git_repo, "destroyer")
    assert dict(actions[0].facts)["staged_paths"] == 0, (
        "this row exists to cover the staged_paths==0 state; if staging appears here "
        "the row has stopped testing what it was written for"
    )


def test_C1_the_STAGING_guard_carries_its_counts_when_git_REFUSES_the_question(
    tmp_path, git_repo, monkeypatch
):
    """The unanswered branch — `staged_paths` is 0 because git would not answer.

    This is the most consequential refusal the module makes (`git checkout --` ACTS,
    so not-knowing cannot be filed as `no`), and until round ten its measurements
    were checked by nothing.
    """
    before = {str(git_repo): perm.fingerprint(git_repo)}
    (git_repo / "tracked.txt").write_text("the phase rewrote this\n")
    real_git = perm._git

    def failing_diff(root, *args, **kwargs):
        if args[:2] == ("diff", "--cached"):
            return subprocess.CompletedProcess(
                args=list(args), returncode=128, stdout="",
                stderr="fatal: this operation must be run in a work tree",
            )
        return real_git(root, *args, **kwargs)

    monkeypatch.setattr(perm, "_git", failing_diff)
    breach = perm.Breach(
        perm.Change(root=git_repo, path="tracked.txt", kind="modified",
                    before_status=None, after_status=" M"),
        "outside the allowlist",
    )
    actions = perm.rollback([breach], before, tmp_path / "q")

    assert actions[0].action == "NOT_ROLLED_BACK"
    _assert_counted_claim_is_certified(actions[0], git_repo, "staging")
    assert dict(actions[0].facts)["staged_paths"] == 0, (
        "git refused the question, so no staged path can be known; a non-zero count "
        "here means the guard answered from something other than the failed call"
    )


def test_C4_dot_claude_is_protected_in_EVERY_declared_repo_not_only_the_root(tmp_path):
    """The receipt said "never config-overridable"; the check was root-repo-only.

    `.claude/settings.json` executes hooks, so a phase in a sibling repo with a
    permissive `writes` could arrange for code to run in the next session there.
    Reachability needs a broad glob — a human decision in a workflow file — which is
    why this was a WARN and not a BLOCK; but the CLAIM was broader than the
    MEASUREMENT, which is the class this review has been chasing (Gate-2 C4).
    """
    root = tmp_path / "meta"
    sibling = tmp_path / "sibling"
    for d in (root, sibling):
        (d / ".claude").mkdir(parents=True)

    changes = [
        perm.Change(root=root, path=".claude/settings.json", kind="modified",
                    before_status=None, after_status=" M"),
        perm.Change(root=sibling, path=".claude/settings.json", kind="modified",
                    before_status=None, after_status=" M"),
    ]
    allowed, breaches = perm.classify(
        changes, root=root, writes=["**"], protected=perm.PROTECTED_ALWAYS,
    )
    assert not allowed, (
        "a permissive `writes: ['**']` reached a hook-execution surface. Allowed: "
        f"{[c.root.name + '/' + c.path for c in allowed]}"
    )
    assert len(breaches) == 2
    assert all("always-protected" in b.reason for b in breaches), (
        f"reasons were {[b.reason for b in breaches]}"
    )


def test_C4_the_root_only_entries_stay_root_only(tmp_path):
    """The widening is `.claude/` and nothing else, deliberately.

    `canonical/` exists in the meta-repo AND in reincarnated-engine, where it is
    rocket's own library and a legitimately declarable write target for its seam.
    Protecting it everywhere would fence another agent out of its own files, which
    is a different failure from the one C4 named.
    """
    root = tmp_path / "meta"
    sibling = tmp_path / "engine"
    for d in (root, sibling):
        (d / "canonical").mkdir(parents=True)

    changes = [
        perm.Change(root=sibling, path="canonical/00-index.md", kind="modified",
                    before_status=None, after_status=" M"),
    ]
    allowed, breaches = perm.classify(
        changes, root=root, writes=["canonical/**"], protected=perm.PROTECTED_ALWAYS,
    )
    assert allowed and not breaches, (
        "a declared write to a SIBLING repo's canonical/ must remain possible; "
        f"breaches were {[b.reason for b in breaches]}"
    )
    assert ".claude/" in perm.PROTECTED_EVERY_REPO
    assert "canonical/" not in perm.PROTECTED_EVERY_REPO
