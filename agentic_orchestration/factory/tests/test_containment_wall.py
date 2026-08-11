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
    before = perm.fingerprint(repo)
    assert before.usable, f"baseline unusable: {before.error}"
    plant()
    after = perm.fingerprint(repo)
    assert after.usable, f"post-plant fingerprint unusable: {after.error}"
    return before, perm.diff_fingerprints(before, after)


def _changes(repo: Path, plant) -> list[perm.Change]:
    return _snapshot(repo, plant)[1]


# ---------------------------------------------------------------------------
# the wall
# ---------------------------------------------------------------------------
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
    changes = _changes(repo, lambda: _plant(kind, protected, tmp_path))
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    actions = perm.rollback(breaches, {}, tmp_path / "quarantine")
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
    """
    repo, protected, _ = fenced
    before, changes = _snapshot(repo, lambda: _plant(kind, protected, tmp_path))
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    actions = perm.rollback(breaches, {}, tmp_path / "quarantine")

    after = perm.fingerprint(repo)
    assert after.usable, f"post-rollback fingerprint unusable: {after.error}"
    residue = perm.diff_fingerprints(before, after)
    named = {a.path.rstrip("/") for a in actions}
    unaccounted = [
        c.path for c in residue
        if not any(
            c.path.rstrip("/") == n or c.path.rstrip("/").startswith(n + "/")
            or n.startswith(c.path.rstrip("/") + "/")
            for n in named
        )
    ]
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
