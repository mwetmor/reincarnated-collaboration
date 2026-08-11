"""The containment falsification wall — Gate-2 verdict (jack-ryan, 2026-08-10).

Four rounds of review found four defects in this module, one per round, all the
same shape: a containment predicate that answers a slightly different question
than the one asked, whose wrong answer is always `clean`.

    F1  the wrong CATEGORY   — gitignored regions were not measured at all
    G1  the wrong BASE       — a subdirectory measured against the worktree root
    G2  the wrong GRANULARITY— read-only matched on the repo root, not the path
    H1  the wrong TARGET     — `.resolve()` answered about a symlink's target

Three of the four were pinned in place by a passing test that asserted the
reduced behaviour was the requirement. Instance-by-instance review stopped
converging, so this file replaces the fifth patch with a wall: one parametrised
table over the artifact kinds a phase can actually produce, each one planted
inside a fenced tree and required to be *detected*, *fenced*, and *undone*.

Every kind carries a falsification partner in `test_the_wall_can_go_green`: the
same artifact planted in an allowlisted directory must be ALLOWED. Without it,
a `classify` that breached unconditionally would pass the whole wall.

Adding a new artifact kind means adding a row. That is the point — the next
containment question of this shape should be answerable by a row rather than by
a fourth reviewer finding it live.
"""

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

from factory import permissions as perm


# ---------------------------------------------------------------------------
# the artifact kinds
#
# Each planter creates ONE artifact under `where` and returns the repo-relative
# path a human would name. What git reports for it may be that path, an ancestor
# of it, or a collapsed directory entry — which is exactly the variation the wall
# exists to cover, so no planter asserts what the change entry will look like.
# ---------------------------------------------------------------------------
def _plant_regular_file(where: Path) -> str:
    (where / "planted.txt").write_text("planted\n", encoding="utf-8")
    return "planted.txt"


def _plant_symlink_pointing_out(where: Path, tmp: Path) -> str:
    """H1, live. The link RESOLVES outside the fence; the link IS inside it."""
    outside = tmp / "far-away"
    outside.mkdir(exist_ok=True)
    (where / "escape").symlink_to(outside)
    return "escape"


def _plant_broken_symlink(where: Path) -> str:
    """H3, live. `exists()` is False for a broken link, so the artifact is
    invisible to any check that asks whether the path exists."""
    (where / "dangling").symlink_to(where / "nothing-here")
    return "dangling"


def _plant_nested_dir(where: Path) -> str:
    (where / "a" / "b" / "c").mkdir(parents=True)
    (where / "a" / "b" / "c" / "deep.txt").write_text("deep\n", encoding="utf-8")
    return "a/b/c/deep.txt"


def _plant_collapsed_untracked_member(where: Path) -> str:
    """git reports a wholly-untracked directory as ONE porcelain line, so the
    change entry is the directory, not this file."""
    d = where / "wholly-new"
    d.mkdir()
    for i in range(3):
        (d / f"m{i}.txt").write_text(f"{i}\n", encoding="utf-8")
    return "wholly-new/m1.txt"


def _plant_gitignored_file(where: Path) -> str:
    """F1's original shape: git never reports this in plain porcelain."""
    d = where / "ignored"
    d.mkdir(exist_ok=True)
    (d / "invisible.txt").write_text("invisible\n", encoding="utf-8")
    return "ignored/invisible.txt"


def _plant_nested_git_repo(where: Path) -> str:
    """A phase that runs `git init` (or clones) inside a fenced tree. git reports
    the whole thing as a single untracked entry and looks no further."""
    d = where / "inner-repo"
    d.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=str(d), check=True, capture_output=True)
    (d / "inner.txt").write_text("inner\n", encoding="utf-8")
    return "inner-repo"


def _plant_quoted_path_with_rename_delimiter(where: Path) -> str:
    """J1(b)+(c), live. Porcelain v1 C-quotes this name AND it contains v1's rename
    separator, so the old parser produced `src` — a real path at the repo root that
    the rollback then deleted. A filename may legally contain the delimiter; a
    delimiter a filename can contain is not a delimiter."""
    (where / "junk -> src").write_text("harmless\n", encoding="utf-8")
    return "junk -> src"


def _plant_path_with_a_newline(where: Path) -> str:
    """The other half of J1(b): v1 quotes and escapes this, so any line-oriented
    parse of the status output sees two records where there is one."""
    (where / "two\nlines.txt").write_text("x\n", encoding="utf-8")
    return "two\nlines.txt"


def _plant_hard_link(where: Path) -> str:
    """Content arrives without a write to this path's inode. Nothing in the fence
    should care, but nothing in the suite established that it doesn't."""
    os.link(where.parent / "tracked.txt", where / "hardlink.txt")
    return "hardlink.txt"


def _plant_mode_only_change(where: Path) -> str:
    """No byte of content changes. git reports the mode; a content-hash-only view
    would not."""
    f = where / "movable.md"
    os.chmod(f, 0o755)
    return "movable.md"


def _plant_dir_replacing_a_file(where: Path) -> str:
    """A tracked FILE becomes a DIRECTORY. Every `is_dir()` branch in rollback and
    quarantine flips meaning for this path between the two snapshots."""
    f = where / "swappable.md"
    f.unlink()
    f.mkdir()
    (f / "inner.txt").write_text("inner\n", encoding="utf-8")
    return "swappable.md"


def _plant_empty_directory_tree(where: Path) -> str:
    """K1. The one artifact git cannot see at any porcelain setting, so it is the one
    the structure sweep exists for — and the sweep shipped WITHOUT a row here, which
    is exactly why its rollback path went unmeasured and reverted a whole repository.
    A new measurement surface gets a row before it ships."""
    (where / "empty_pkg" / "nested").mkdir(parents=True)
    return "empty_pkg"


def _plant_unreadable_subtree(where: Path) -> str:
    """A directory the sweep cannot descend into. The temptation is to skip what
    cannot be read; skipping it makes it read as clean (G6)."""
    d = where / "sealed"
    d.mkdir()
    (d / "secret.txt").write_text("secret\n", encoding="utf-8")
    os.chmod(d, 0o000)
    return "sealed"


#: name -> planter. Signature is uniform except the symlink kind, which needs a
#: destination outside the tree; `_plant` adapts it.
ARTIFACT_KINDS: dict[str, object] = {
    "regular_file": _plant_regular_file,
    "symlink_pointing_out_of_the_tree": _plant_symlink_pointing_out,
    "broken_symlink": _plant_broken_symlink,
    "nested_dir": _plant_nested_dir,
    "collapsed_untracked_member": _plant_collapsed_untracked_member,
    "gitignored_file": _plant_gitignored_file,
    "nested_git_repo": _plant_nested_git_repo,
    "unreadable_subtree": _plant_unreadable_subtree,
    # added closing J1 (Gate-2 wall audit) — the kinds the first eight rows missed
    "quoted_path_with_rename_delimiter": _plant_quoted_path_with_rename_delimiter,
    "path_with_a_newline": _plant_path_with_a_newline,
    "hard_link": _plant_hard_link,
    "mode_only_change": _plant_mode_only_change,
    "dir_replacing_a_file": _plant_dir_replacing_a_file,
    # added closing K1 (Gate-2 round five) — the measurement surface added in round
    # four, which was tested for DETECTION only and therefore never reached rounds
    # three or four, where its defect lived
    "empty_directory_tree": _plant_empty_directory_tree,
}


def _plant(kind: str, where: Path, tmp: Path) -> str:
    planter = ARTIFACT_KINDS[kind]
    if kind == "symlink_pointing_out_of_the_tree":
        return planter(where, tmp)
    return planter(where)


@pytest.fixture(autouse=True)
def _restore_permissions(tmp_path: Path):
    """`unreadable_subtree` chmods a directory to 000; pytest cannot clean up
    tmp_path without it back."""
    yield
    for p in tmp_path.rglob("*"):
        try:
            if p.is_dir() and not p.is_symlink():
                os.chmod(p, 0o755)
        except OSError:
            pass


@pytest.fixture
def fenced(git_repo: Path):
    """A git repo with a read-only subtree inside it and one writable subtree
    beside it. This is the shipped shape: whole-worktree `repos:` entry, narrower
    `read_only_trees:` inside it."""
    protected = git_repo / "protected"
    workspace = git_repo / "workspace"
    for d in (protected, workspace):
        d.mkdir()
        # Tracked content in BOTH trees: the mode-only, type-change and rename kinds
        # need something git already knows about, and the falsification partner needs
        # the identical starting shape on the writable side.
        (d / "movable.md").write_text("movable\n", encoding="utf-8")
        (d / "swappable.md").write_text("swappable\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=str(git_repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "fence"], cwd=str(git_repo), check=True,
        capture_output=True,
    )
    return git_repo, protected, workspace


def _snapshot(repo: Path, plant) -> tuple[perm.TreeFingerprint, list[perm.Change]]:
    """Both subtrees are MEASURED; only one is fenced.

    Measurement scope and fence scope are different questions, and giving the wall
    both subtrees as `structure_roots` is what lets the `empty_directory_tree` row
    have a real falsification partner: the same empty tree planted in the writable
    subtree is seen, and must still come back ALLOWED.
    """
    roots = [repo / "protected", repo / "workspace"]
    before = perm.fingerprint(repo, structure_roots=roots)
    assert before.usable, f"baseline unusable: {before.error}"
    plant()
    after = perm.fingerprint(repo, structure_roots=roots)
    assert after.usable, f"post-plant fingerprint unusable: {after.error}"
    return before, perm.diff_fingerprints(before, after)


def _changes(repo: Path, plant) -> list[perm.Change]:
    return _snapshot(repo, plant)[1]


# ---------------------------------------------------------------------------
# the wall
# ---------------------------------------------------------------------------
def _at_or_below(ancestor: str, path: str) -> bool:
    a, p = ancestor.rstrip("/"), path.rstrip("/")
    return a == p or p.startswith(a + "/")


def _unaccounted(residue: list[perm.Change], named: set[str]) -> list[str]:
    """Round four's accounting predicate — ONE definition, used by the round and by
    the test that falsifies it. Two copies of a predicate is one copy that can drift
    out from under its own falsifier."""
    return [c.path for c in residue if not any(_at_or_below(n, c.path) for n in named)]


def _assert_contents_match(
    before: perm.TreeFingerprint, repo: Path, rel: str, kind: str
) -> None:
    """A `restored` path must be back at its phase-start fingerprint, contents included."""
    roots = [repo / "protected", repo / "workspace"]
    now = perm.fingerprint(repo, structure_roots=roots)
    assert now.usable, f"post-rollback fingerprint unusable: {now.error}"
    still_moved = [
        c.path for c in perm.diff_fingerprints(before, now) if _at_or_below(rel, c.path)
    ]
    assert not still_moved, (
        f"the receipt claims `restored` for {rel!r} after a {kind}, and these paths "
        f"under it are still not back at their phase-start state: {still_moved}. "
        "`restored` is a claim about contents; a path that merely still EXISTS "
        "satisfies nothing — that is what `git checkout -- .` scored while it was "
        "reverting an entire repository (K1)."
    )


def _names(changes: list[perm.Change], rel: str, prefix: str = "protected") -> bool:
    """Is `prefix/rel` actually NAMED by the change-set?

    Either exactly, or by an ancestor — git collapses a wholly-untracked directory
    to one entry, so the ancestor is the only record that exists and it is a true
    record of the artifact. Deliberately NOT the other direction: a change *below*
    the artifact does not name it, and accepting that is how a fabricated path
    satisfies the check (J1).
    """
    want = f"{prefix}/{rel}".rstrip("/")
    for c in changes:
        got = c.path.rstrip("/")
        if got == want or want.startswith(got + "/"):
            return True
    return False


@pytest.mark.parametrize("kind", sorted(ARTIFACT_KINDS))
def test_the_wall_NAMES_every_artifact_kind(kind, fenced, tmp_path):
    """Round one: the change-set must name the artifact — not merely be non-empty.

    The first draft of this round asserted `assert changes`, and the Gate-2 wall
    audit found the wall had the module's own disease in the one assertion meant to
    cure it: a predicate answering a slightly different question than the one asked,
    whose wrong answer is green. Both faces of J1 satisfy "non-empty" — a rename
    produced a change-set holding only the DESTINATION while the source silently
    left the fence, and a quoted path produced a change naming a fabricated path
    that never existed. Non-emptiness is not detection.
    """
    repo, protected, _ = fenced
    planted: list[str] = []
    changes = _changes(repo, lambda: planted.append(_plant(kind, protected, tmp_path)))
    assert changes, (
        f"a {kind} was planted inside the tree and the fingerprint diff was EMPTY. "
        "An empty diff is indistinguishable from innocence."
    )
    assert _names(changes, planted[0]), (
        f"a {kind} was planted at protected/{planted[0]!r} and the change-set names "
        f"{[c.path for c in changes]} — none of which is that path or an ancestor of "
        "it. A change-set that is non-empty but names the wrong thing is worse than "
        "an empty one: it looks like detection, and whatever it names is what the "
        "rollback will act on."
    )


@pytest.mark.parametrize("kind", sorted(ARTIFACT_KINDS))
def test_the_wall_fences_every_artifact_kind(kind, fenced, tmp_path):
    """Round two: detection is not enforcement. `writes: ["**"]` is deliberate —
    the read-only tree must hold even when the allowlist is maximally permissive,
    because that is the configuration H1 escaped from."""
    repo, protected, _ = fenced
    changes = _changes(repo, lambda: _plant(kind, protected, tmp_path))
    allowed, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    assert breaches, f"a {kind} inside the read-only tree was not a breach"
    assert any("read-only tree" in b.reason for b in breaches), (
        f"a {kind} breached for some other reason ({[b.reason for b in breaches]}); "
        "the read-only fence itself must be what caught it, or the fence is "
        "passing on the strength of an unrelated rule"
    )
    assert not allowed, f"a {kind} was BOTH breached and allowed: {allowed}"


@pytest.mark.parametrize("kind", sorted(ARTIFACT_KINDS))
def test_the_wall_reports_the_undo_honestly_for_every_artifact_kind(kind, fenced, tmp_path):
    """Round three: the receipt and the disk must agree.

    NOT "the artifact is always removed" — that is not the contract and should not
    be. The module's standing safety rule is that nothing is deleted unquarantined,
    so an artifact the rollback cannot safely quarantine is deliberately LEFT as
    evidence (the unreadable subtree is exactly this case). The run aborts either
    way. What must never happen is the third state: the artifact survives and the
    receipt says `deleted`, so the abort report reads as if the tree came back
    clean. That is a fail-open wearing a rollback.

    `lstat` throughout, never `exists()` — `exists()` follows symlinks and reports
    False for a broken link that is very much still on disk (H3).
    """
    repo, protected, _ = fenced
    before, changes = _snapshot(repo, lambda: _plant(kind, protected, tmp_path))
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    actions = perm.rollback(
        breaches, {}, tmp_path / "quarantine", declared_trees=[repo, protected]
    )
    assert actions, f"a {kind} breached and the rollback recorded nothing at all"

    for a in actions:
        target = repo / a.path
        if a.action == "deleted":
            assert not _lexists(target), (
                f"the receipt claims `deleted` for {a.path!r} after a {kind}, and it "
                "is still on disk. A receipt that disagrees with the disk is worse "
                "than no rollback: the abort report reads as if the tree came back "
                "clean."
            )
        elif a.action == "restored":
            assert _lexists(target), (
                f"the receipt claims `restored` for {a.path!r} after a {kind}, and "
                "there is nothing there. A restore that removed the path is a "
                "rollback that destroyed work."
            )
            # Mere existence is what K1 satisfied: `git checkout -- .` reverted an
            # entire repository, left the artifact standing, and reported `restored`
            # — and the path it named (a directory) trivially still existed. A
            # restore is a claim about CONTENTS, so the contents are what is checked.
            _assert_contents_match(before, repo, a.path, kind)
        else:
            assert a.action == "NOT_ROLLED_BACK", f"unknown action {a.action!r}"
            assert a.reason, (
                f"{a.path!r} was left in place after a {kind} with no stated reason. "
                "Evidence left deliberately is fine; evidence left silently is not."
            )


@pytest.mark.parametrize("kind", sorted(ARTIFACT_KINDS))
def test_the_wall_accounts_for_every_residue_of_every_artifact_kind(kind, fenced, tmp_path):
    """Round four — the second clause the Gate-2 wall audit required.

    "The receipt and the disk agree" is the right floor and the wrong ceiling: it is
    satisfiable by a *consistent falsehood*, because a rollback that silently misses
    a path emits no action for it and therefore contradicts nothing. The stronger
    promise is closure over the tree, not over the receipt —

        after rollback, the fenced tree is back to its phase-start fingerprint,
        or every path that is not is NAMED.

    Anything still moved and unnamed is residue nobody decided to leave.

    An action accounts only for residue AT OR BELOW the path it names. The first
    draft accepted the relation in both directions, which made this round satisfiable
    by an over-broad name: an action naming `.` or `protected` accounted for every
    path in the tree. K1 — a rollback that reverted an entire repository and left the
    artifact standing — passed this round with an empty unaccounted list. Being named
    by something enormous is not being accounted for.
    """
    repo, protected, _ = fenced
    before, changes = _snapshot(repo, lambda: _plant(kind, protected, tmp_path))
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    actions = perm.rollback(
        breaches, {}, tmp_path / "quarantine", declared_trees=[repo, protected]
    )

    after = perm.fingerprint(repo, structure_roots=[protected, repo / "workspace"])
    assert after.usable, f"post-rollback fingerprint unusable: {after.error}"
    residue = perm.diff_fingerprints(before, after)
    named = {a.path.rstrip("/") for a in actions}
    unaccounted = _unaccounted(residue, named)
    assert not unaccounted, (
        f"after rolling back a {kind}, the tree has not returned to its phase-start "
        f"fingerprint and these paths are named by no rollback action: {unaccounted}. "
        f"Actions were {[(a.path, a.action) for a in actions]}. Residue nobody "
        "decided to leave is the failure this round exists to catch."
    )


@pytest.mark.parametrize("kind", sorted(ARTIFACT_KINDS))
def test_the_wall_can_go_green(kind, fenced, tmp_path):
    """The falsification partner for all three rounds above.

    The identical artifact, planted in a declared, allowlisted, NON-fenced
    directory, must come back ALLOWED. Without this, a `classify` that breached
    on everything would pass the entire wall and the wall would be measuring
    nothing — which is the failure mode the wall was built to end."""
    repo, _, workspace = fenced
    changes = _changes(repo, lambda: _plant(kind, workspace, tmp_path))
    allowed, breaches = perm.classify(
        changes, writes=["workspace/**", "workspace"], root=repo,
        read_only_trees=[repo / "protected"],
    )
    assert allowed and not breaches, (
        f"a {kind} in a declared writable directory was refused: "
        f"{[(b.change.path, b.reason) for b in breaches]}. The fence is over-wide, "
        "which makes every green above meaningless."
    )


# ---------------------------------------------------------------------------
# J1 — the rename escape and the induced deletion
#
# These do not fit the uniform planter signature (they need a destination OUTSIDE
# the fence), so they get their own names — the regression a reviewer will grep for.
# ---------------------------------------------------------------------------
def test_J1a_a_git_mv_OUT_of_the_fence_names_the_SOURCE(fenced):
    """The old parser kept `split(" -> ")[-1]`, the DESTINATION, and dropped the
    source. So `git mv` out of a read-only tree into the phase's own allowlist
    produced a change-set naming only a legal path — the fenced file was gone and
    the run passed. Using the *more* disciplined command was the difference between
    caught and clean."""
    repo, _, _ = fenced

    def do_move():
        subprocess.run(
            ["git", "mv", "protected/movable.md", "workspace/exfiltrated.md"],
            cwd=str(repo), check=True, capture_output=True,
        )

    changes = _changes(repo, do_move)
    assert _names(changes, "movable.md"), (
        f"a git mv out of the fence produced {[c.path for c in changes]} — the source "
        "protected/movable.md is not among them, so the fence never sees the file leave"
    )
    _, breaches = perm.classify(
        changes, writes=["workspace/**", "protected/**"], root=repo,
        read_only_trees=[repo / "protected"],
    )
    assert any("read-only tree" in b.reason for b in breaches), (
        f"moving a file OUT of a read-only tree was not a breach: {breaches}"
    )


def test_J1a_partner_a_rename_entirely_inside_the_allowlist_is_allowed(fenced):
    """Falsification partner: renames are not breaches, renames ACROSS the fence are."""
    repo, _, _ = fenced

    def do_move():
        subprocess.run(
            ["git", "mv", "workspace/movable.md", "workspace/renamed.md"],
            cwd=str(repo), check=True, capture_output=True,
        )

    changes = _changes(repo, do_move)
    allowed, breaches = perm.classify(
        changes, writes=["workspace/**"], root=repo,
        read_only_trees=[repo / "protected"],
    )
    assert allowed and not breaches, f"a legal rename was refused: {breaches}"


def test_J1c_the_rollback_never_deletes_tracked_content(fenced, tmp_path):
    """The third face, and the worst: the fabricated path the old parser produced was
    a REAL path at the repo root, and the rollback acted on it — deleting the very
    read-only tree it was fencing, from a file the phase was ALLOWED to write.

    The parser fix removes the cause. This asserts the structural guard, which does
    not depend on knowing which parse bug produced the bad path: a `created` path
    cannot contain anything git already tracks, so if it does, our identification is
    wrong and the deletion is refused. Containment must never destroy work."""
    repo, protected, _ = fenced
    misidentified = perm.Change(
        root=repo, path="protected", kind="created", before_status=None, after_status="??"
    )
    actions = perm.rollback(
        [perm.Breach(misidentified, "misidentified")], {}, tmp_path / "quarantine"
    )
    assert (protected / "movable.md").exists(), (
        "the rollback DELETED a tree full of committed files because a change entry "
        "claimed the phase had created it. This is the J1(c) live failure."
    )
    assert actions and actions[0].action == "NOT_ROLLED_BACK"
    assert "tracks" in actions[0].reason, (
        f"the refusal did not say why: {actions[0].reason!r}"
    )


def test_J1c_partner_the_guard_still_deletes_a_genuine_creation(fenced, tmp_path):
    """Without this, a rollback that refused everything would pass the test above and
    the containment would quietly stop rolling anything back."""
    repo, protected, _ = fenced
    (protected / "genuinely-new.txt").write_text("new\n", encoding="utf-8")
    change = perm.Change(
        root=repo, path="protected/genuinely-new.txt", kind="created",
        before_status=None, after_status="??",
    )
    actions = perm.rollback([perm.Breach(change, "planted")], {}, tmp_path / "quarantine")
    assert actions[0].action == "deleted", f"a real creation was not undone: {actions}"
    assert not (protected / "genuinely-new.txt").exists()


# ---------------------------------------------------------------------------
# the declared blind spot
# ---------------------------------------------------------------------------
def test_a_WHOLLY_EMPTY_directory_tree_is_STILL_invisible_to_git_itself(fenced):
    """The premise, pinned. If git ever starts reporting these, the structure sweep
    below becomes redundant and someone should know to delete it."""
    repo, protected, _ = fenced
    before = perm.fingerprint(repo)
    (protected / "a" / "b" / "c").mkdir(parents=True)
    after = perm.fingerprint(repo)
    assert not perm.diff_fingerprints(before, after), (
        "git now reports empty directory trees; the structure sweep is redundant"
    )


def test_an_empty_directory_tree_in_a_READ_ONLY_tree_is_caught_by_the_structure_sweep(fenced):
    """The blind spot, CLOSED rather than reworded.

    It was first declared as bounded — no bytes cross the fence — and the Gate-2 wall
    audit refused the reassurance on two grounds. First, the affordability argument
    conflated the *exact* sweep (one stat per file, genuinely expensive) with a
    *structure-only* sweep (no stats at all), measured at 0.21 s for the engine and
    1.69 s for godot. Second, "bounded to directory structure" is not inert on the two
    trees actually fenced: a bare directory is a PEP-420 namespace package, so an
    empty `src/reincarnated/<name>/` turns an ImportError into a successful import of
    nothing; and a new directory under `res://` is picked up by Godot's import scan.
    It was also invisible to the rollback, so it accumulated across runs.

    "Bounded and low-harm" has been the wrong answer three times in this module. The
    sweep is scoped to the read-only trees, which is where it is both cheap and
    load-bearing.
    """
    repo, protected, _ = fenced
    before = perm.fingerprint(repo, structure_roots=[protected])
    (protected / "a" / "b" / "c").mkdir(parents=True)
    after = perm.fingerprint(repo, structure_roots=[protected])
    changes = perm.diff_fingerprints(before, after)
    assert changes, "an empty directory tree inside a read-only tree was not detected"
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    assert any("read-only tree" in b.reason for b in breaches), (
        f"detected but not fenced: {[(c.path, c.kind) for c in changes]}"
    )


def test_the_structure_sweep_does_not_fire_on_an_unchanged_tree(fenced):
    """Falsification partner. A sweep that reported a delta every time would pass the
    test above and abort every run — the M7 failure mode, one layer down."""
    repo, protected, _ = fenced
    before = perm.fingerprint(repo, structure_roots=[protected])
    after = perm.fingerprint(repo, structure_roots=[protected])
    assert not perm.diff_fingerprints(before, after), (
        "the structure sweep is not stable across two reads of an untouched tree"
    )


def test_the_structure_sweep_is_scoped_to_the_trees_it_is_given(fenced):
    """It is affordable BECAUSE it is scoped. A fingerprint taken without
    `structure_roots` must not walk anything."""
    repo, _, _ = fenced
    assert perm.fingerprint(repo).structure == {}


# ---------------------------------------------------------------------------
# K1-K4 — Gate-2 round five. The defect was in round four's own fix.
# ---------------------------------------------------------------------------
def test_K1_a_structure_change_is_reported_at_the_DIRECTORY_not_at_the_tree(fenced):
    """The whole of K1 in one assertion.

    The first structure sweep returned `dirs:<n>:<hash>`. A hash can say that
    something moved and nothing about what, so the diff reported the change at the
    TREE ROOT — and the rollback handed that to `git checkout --` as a pathspec,
    reverting every uncommitted change in the repository over one empty directory,
    while the directory itself survived. The receipt word was `restored`.

    A measurement that cannot NAME what moved must not be wired to a verb that acts
    on what it names.
    """
    repo, protected, _ = fenced
    roots = [protected]
    before = perm.fingerprint(repo, structure_roots=roots)
    (protected / "empty_pkg").mkdir()
    changes = perm.diff_fingerprints(before, perm.fingerprint(repo, structure_roots=roots))
    assert [c.path for c in changes] == ["protected/empty_pkg"], (
        f"the structure sweep reported {[(c.path, c.kind) for c in changes]}. It must "
        "name the directory that moved — reporting the tree is K1, and the tree's "
        "path is a pathspec that reverts the tree."
    )
    assert changes[0].kind == "created", (
        f"a new directory typed {changes[0].kind!r}; `created` is what lets the "
        "rollback remove it instead of running a restore over its parent"
    )


def test_K1_the_rollback_REFUSES_a_pathspec_that_names_a_whole_tree(fenced, tmp_path):
    """The structural guard, independent of what produced the coarse path.

    This is the destroyer guard's principle applied to the other destructive verb.
    `git checkout -- .` is not a smaller act than `rm -rf` — it silently discards
    every uncommitted modification in the repository — and no measurement in this
    module is ever entitled to trigger it.
    """
    repo, protected, _ = fenced
    (protected / "movable.md").write_text("EDITED IN FLIGHT\n", encoding="utf-8")
    for pathspec in (".", "", "protected"):
        change = perm.Change(repo, pathspec, "modified", " M", " M")
        actions = perm.rollback(
            [perm.Breach(change, "coarse")], {}, tmp_path / "q",
            declared_trees=[repo, protected],
        )
        assert actions[0].action == "NOT_ROLLED_BACK", (
            f"the rollback ran `git checkout -- {pathspec!r}`, which reverts a whole "
            "tree. That is K1."
        )
        assert "REFUSED" in actions[0].reason and "human decision" in actions[0].reason
    assert (protected / "movable.md").read_text() == "EDITED IN FLIGHT\n", (
        "the in-flight edit was destroyed by a rollback aimed at a tree"
    )


def test_K1_partner_the_rollback_still_restores_a_named_file(fenced, tmp_path):
    """Falsification partner: a guard that refused every restore would pass the test
    above and quietly stop rolling anything back."""
    repo, protected, _ = fenced
    (protected / "movable.md").write_text("PHASE WROTE THIS\n", encoding="utf-8")
    change = perm.Change(repo, "protected/movable.md", "modified", None, " M")
    actions = perm.rollback(
        [perm.Breach(change, "planted")], {}, tmp_path / "q",
        declared_trees=[repo, protected],
    )
    assert actions[0].action == "restored", f"a named file was not restored: {actions}"
    assert (protected / "movable.md").read_text() == "movable\n"


def test_K2_a_clean_tracked_file_modified_by_a_phase_is_MODIFIED_not_created(fenced, tmp_path):
    """A tracked file nobody has touched is absent from `git status`, and absence was
    read as newness. So the most likely agentic breach there is — an agent edits a
    committed source file — was typed `created`, hit the destroyer guard, and came
    back NOT_ROLLED_BACK with a reason asserting a misidentification that had not
    occurred. The edit stayed in the read-only tree after the abort."""
    repo, protected, _ = fenced
    changes = _changes(
        repo, lambda: (protected / "movable.md").write_text("AGENT EDIT\n", encoding="utf-8")
    )
    edit = [c for c in changes if c.path == "protected/movable.md"]
    assert edit and edit[0].kind == "modified", (
        f"a modified tracked file typed {[(c.path, c.kind) for c in changes]}. "
        "`created` sends it to the delete branch, where the guard correctly refuses "
        "and the edit therefore survives inside the fence."
    )
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    actions = perm.rollback(
        breaches, {}, tmp_path / "q", declared_trees=[repo, protected]
    )
    assert [a.action for a in actions] == ["restored"], f"not restored: {actions}"
    assert (protected / "movable.md").read_text() == "movable\n", (
        "the agent's edit survived inside a read-only tree after the abort"
    )


def test_K3_the_destroyer_guard_asks_HEAD_as_well_as_the_index(fenced, tmp_path):
    """`git ls-files` reads the index, and the index can be silenced while the content
    is still committed and still on disk. A phase that runs `git rm --cached` leaves
    the path CLEAN at phase start, so the pre-existing-dirt guard correctly does not
    fire and the destroyer guard is the only thing standing between the rollback and
    committed work. Asking one question got the answer `no tracked content` for a
    directory full of it."""
    repo, protected, _ = fenced
    subprocess.run(
        ["git", "rm", "--cached", "-q", "-r", "protected"],
        cwd=str(repo), check=True, capture_output=True,
    )
    assert not subprocess.run(
        ["git", "ls-files", "--", "protected"],
        cwd=str(repo), capture_output=True, text=True,
    ).stdout.strip(), "the premise failed: the index still reports this path"
    assert perm._tracks_content(repo, "protected") == 2, (
        "HEAD still holds two files under protected/ and the guard must see them"
    )
    change = perm.Change(repo, "protected", "created", None, "??")
    actions = perm.rollback(
        [perm.Breach(change, "misidentified")], {}, tmp_path / "q",
        declared_trees=[repo],
    )
    assert (protected / "movable.md").exists() and (protected / "swappable.md").exists(), (
        "the rollback deleted committed content because the index had been silenced"
    )
    assert actions[0].action == "NOT_ROLLED_BACK" and "tracks" in actions[0].reason


def test_K4_a_collapsed_ignored_dir_dirty_at_phase_start_is_refused_BY_THAT_REASON(
    fenced, tmp_path
):
    """The row the Gate-2 round-five audit asked for by name.

    The trailing-slash normalisation of the pre-existing-dirt guard landed in round
    four with no falsifying test — reverting it turned nothing red, which makes a
    safety fix a comment. git reports a collapsed ignored directory WITH a trailing
    slash and the change path arrives without one, so an exact-string membership test
    misses on the punctuation alone, for exactly the entries most likely to be huge
    (the engine's 3.3 GB `seasons/`). What must be asserted is not merely that the
    path survives, but that it survives FOR THE RIGHT REASON: the refusal has to be
    the dirt guard, or the protection is passing on the strength of an accident.
    """
    repo, protected, _ = fenced
    big = protected / "ignored"
    big.mkdir()
    (big / "existing.dat").write_text("pre-existing uncommitted work\n", encoding="utf-8")
    before = perm.fingerprint(repo)
    assert any(e.rstrip("/") == "protected/ignored" for e in before.entries), (
        f"premise failed: git did not report the ignored dir at all ({before.entries})"
    )
    (big / "added-by-the-phase.dat").write_text("phase\n", encoding="utf-8")
    changes = perm.diff_fingerprints(before, perm.fingerprint(repo))
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    assert breaches, "a write into an ignored dir inside the fence was not a breach"
    actions = perm.rollback(
        breaches, before={str(repo): before}, quarantine_dir=tmp_path / "q",
        declared_trees=[repo, protected],
    )
    assert [a.action for a in actions] == ["NOT_ROLLED_BACK"], f"acted on it: {actions}"
    assert "already dirty at phase start" in actions[0].reason, (
        f"the path survived, but for the wrong reason: {actions[0].reason!r}. The "
        "dirt guard must be what refused; anything else means the guard missed and "
        "something downstream happened to fail."
    )
    assert (big / "existing.dat").exists()


def test_K1_ordinary_git_activity_does_not_move_the_structure(fenced):
    """K1's TRIGGER, which is separate from its consequence.

    `.git` is 281 of the engine's 968 directories and 276 of godot's 5,240, and its
    object fanout gains a directory on a plain `git add`. With `.git` in the walk,
    the most disciplined thing an agent can do in a read-only tree — stage its work
    rather than leave it loose — was itself the breach that triggered the repo-wide
    revert. Nothing the sweep exists to catch lives under `.git`: a PEP-420 namespace
    package and a Godot `res://` import target are both worktree facts.
    """
    repo, protected, _ = fenced
    # Swept at the REPO ROOT, because that is the shipped shape: both declared
    # read-only trees (`~/Games/reincarnated-engine`, `~/Games/reincarnated-godot`)
    # are worktree roots, so `.git` is inside the fence. Sweeping a subdirectory
    # would never meet `.git` and would prove nothing.
    (protected / "ignored").mkdir(exist_ok=True)
    (protected / "ignored" / "blob.dat").write_text("x" * 4096, encoding="utf-8")
    before = perm.structure_dirs(repo)
    subprocess.run(
        ["git", "add", "-f", "protected/ignored/blob.dat"],
        cwd=str(repo), check=True, capture_output=True,
    )
    assert (repo / ".git" / "objects").exists(), "premise failed: no object store"
    assert perm.structure_dirs(repo) == before, (
        "a plain `git add` moved the directory-structure signature. Ordinary git use "
        "inside a read-only tree must not read as a structural write — that is what "
        "made K1 fire on disciplined behaviour."
    )
    assert not any(d == ".git" or d.startswith(".git/") for d in before), (
        f"the sweep descended into .git: {sorted(d for d in before if '.git' in d)[:5]}"
    )


def test_K1_partner_the_sweep_still_sees_a_directory_outside_dot_git(fenced):
    """Falsification partner: a sweep that skipped everything would pass the test
    above and see nothing at all."""
    repo, protected, _ = fenced
    before = perm.structure_dirs(repo)
    (protected / "empty_pkg").mkdir()
    assert perm.structure_dirs(repo) - before == {"protected/empty_pkg"}


def test_K5_round_four_does_not_accept_an_OVER_BROAD_name(fenced, tmp_path):
    """Round four's accounting predicate, falsified directly.

    The round is only as strong as the relation it accepts. With the relation read in
    both directions, an action naming `.` or `protected` accounted for every path in
    the tree — so K1, a rollback that reverted an entire repository and left the
    artifact standing, produced an EMPTY unaccounted list and passed. Being named by
    something enormous is not being accounted for, and this asserts the direction
    rather than trusting the sentence in the docstring.
    """
    # An ancestor genuinely does account for what is under it: git collapses a
    # wholly-untracked directory to one entry, so the ancestor is often the only
    # record that exists. That direction is kept.
    assert _at_or_below("protected/ignored", "protected/ignored/blob.dat")

    # The other direction is the one that was wrong. Here the rollback undid ONE FILE
    # and the residue is the whole collapsed directory, still differing — the action
    # names strictly less than what is still moved, and the old predicate called that
    # accounted for.
    assert not _at_or_below("protected/ignored/blob.dat", "protected/ignored"), (
        "the accounting relation is being read in both directions. A rollback that "
        "touched one file inside a directory does not account for the directory "
        "still being changed — accepting that is how a receipt that named something "
        "small, or something enormous, closed the round without closing the tree."
    )

    # And live: a rollback naming only the deepest path must leave the broader
    # residue UNACCOUNTED, so round four reds instead of passing on the name.
    repo, protected, _ = fenced
    before, _ = _snapshot(
        repo,
        lambda: [
            (protected / "ignored").mkdir(),
            (protected / "ignored" / "blob.dat").write_text("x\n", encoding="utf-8"),
            (protected / "empty_pkg").mkdir(),
        ],
    )
    after = perm.fingerprint(repo, structure_roots=[protected, repo / "workspace"])
    partial = {"protected/ignored/blob.dat"}     # a receipt that undid one file only
    unaccounted = _unaccounted(perm.diff_fingerprints(before, after), partial)
    # `protected/ignored/` is the discriminating one: git collapses the directory to
    # a single entry, so the residue is the DIRECTORY while the receipt names a file
    # inside it. Reading the relation both ways calls that accounted for, and the
    # directory is still changed.
    assert "protected/ignored/" in unaccounted, (
        f"a receipt naming one file inside a collapsed directory accounted for the "
        f"directory itself ({unaccounted}); round four is passing on a name rather "
        "than on the disk"
    )
    assert "protected/empty_pkg" in unaccounted


def test_K9_the_filesystem_refuses_a_non_UTF8_filename(git_repo: Path):
    """Pinned as a HOST property, not a code property.

    `_git` decodes strictly, so a non-UTF-8 byte in a filename would raise rather
    than fabricate a path — the right failure. That branch is unreachable here only
    because APFS rejects the name outright. A network mount or a different volume
    could change the answer, and this test is what notices.
    """
    with pytest.raises(OSError):
        os.close(os.open(bytes(git_repo) + b"/inv\xffalid.txt", os.O_CREAT | os.O_WRONLY))


def _lexists(p: Path) -> bool:
    try:
        os.lstat(p)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# the specific escape that opened the wall — kept as its own named test so the
# regression has a name a reviewer can grep for
# ---------------------------------------------------------------------------
def test_H1_a_symlink_out_of_a_read_only_tree_is_judged_where_the_LINK_is(tmp_path):
    """`_read_only_hit` called `.resolve()`, which follows symlinks — so for a link
    planted inside the fence it answered a question about the target's location.
    A link to /tmp resolved clean out of the tree entirely. The artifact that
    appeared inside the read-only tree was the LINK, so the link's own location is
    the one that decides."""
    root = tmp_path / "engine"
    (root / "seasons").mkdir(parents=True)
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    (root / "seasons" / "escape").symlink_to(outside)

    allowed, breaches = perm.classify(
        [perm.Change(root=root, path="seasons/escape", kind="created",
                     before_status=None, after_status="??")],
        writes=["**"],
        root=root,
        read_only_trees=[root / "seasons"],
    )
    assert not allowed
    assert "read-only tree" in breaches[0].reason


def test_H1_partner_a_symlink_reached_THROUGH_a_link_still_hits(tmp_path):
    """The resolved form is kept, not replaced. A read-only tree reached through a
    symlinked parent is equally a hit, so the fix matches on either form."""
    real = tmp_path / "real-engine"
    (real / "seasons").mkdir(parents=True)
    link = tmp_path / "engine"
    link.symlink_to(real)

    allowed, breaches = perm.classify(
        [perm.Change(root=link, path="seasons/x.json", kind="created",
                     before_status=None, after_status="??")],
        writes=["**"],
        root=link,
        read_only_trees=[real / "seasons"],
    )
    assert not allowed, "the read-only tree was declared by its real path and missed"
    assert "read-only tree" in breaches[0].reason
