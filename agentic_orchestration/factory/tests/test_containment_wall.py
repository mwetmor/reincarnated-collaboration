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
    protected.mkdir()
    (protected / ".keep").write_text("", encoding="utf-8")
    workspace = git_repo / "workspace"
    workspace.mkdir()
    subprocess.run(["git", "add", "-A"], cwd=str(git_repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "fence"], cwd=str(git_repo), check=True,
        capture_output=True,
    )
    return git_repo, protected, workspace


def _changes(repo: Path, plant) -> list[perm.Change]:
    before = perm.fingerprint(repo)
    assert before.usable, f"baseline unusable: {before.error}"
    plant()
    after = perm.fingerprint(repo)
    assert after.usable, f"post-plant fingerprint unusable: {after.error}"
    return perm.diff_fingerprints(before, after)


# ---------------------------------------------------------------------------
# the wall
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("kind", sorted(ARTIFACT_KINDS))
def test_the_wall_detects_every_artifact_kind(kind, fenced, tmp_path):
    """Round one of the wall: the tree must not measure clean.

    This is the assertion every one of F1/G1/G2/H1 would have failed. Each of
    those defects ended with an empty change-set over a tree that had just been
    written to."""
    repo, protected, _ = fenced
    changes = _changes(repo, lambda: _plant(kind, protected, tmp_path))
    assert changes, (
        f"a {kind} was planted inside the tree and the fingerprint diff was EMPTY. "
        "An empty diff is indistinguishable from innocence, so this reads as proof "
        "that nothing happened."
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
    planted: list[str] = []
    changes = _changes(repo, lambda: planted.append(_plant(kind, protected, tmp_path)))
    rel = planted[0]
    _, breaches = perm.classify(
        changes, writes=["**"], root=repo, read_only_trees=[protected]
    )
    actions = perm.rollback(breaches, {}, tmp_path / "quarantine")
    assert actions, f"a {kind} breached and the rollback recorded nothing at all"

    survived = _lexists(protected / rel)
    deleted = [a for a in actions if a.action == "deleted"]
    left = [a for a in actions if a.action == "NOT_ROLLED_BACK"]
    if survived:
        assert not deleted, (
            f"a {kind} survived rollback while the receipt claimed {deleted} — the "
            "receipt disagrees with the disk, so the abort report reads as if the "
            "tree came back clean"
        )
        assert left and all(a.reason for a in left), (
            f"a {kind} was left on disk with no stated reason: {actions}. Evidence "
            "left deliberately is fine; evidence left silently is not."
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
# the declared blind spot
# ---------------------------------------------------------------------------
def test_a_WHOLLY_EMPTY_directory_tree_is_INVISIBLE_to_the_porcelain_channel(fenced, tmp_path):
    """A pinned limitation, not a passing gate. Declared here rather than left to be
    found, the same way the COARSE tier's in-place-edit blind spot is declared.

    git has no concept of an empty directory — it tracks content, so a directory
    tree containing no files is reported by nothing, at any porcelain setting. The
    stat sweep cannot rescue it either: the sweep only descends into paths git
    already reported, which is the design that keeps the engine's 3.3 GB affordable.

    Scope of the residual risk: bounded to directory structure. The moment any FILE
    lands anywhere inside such a tree, git reports the collapsed entry and the fence
    catches it — `test_the_wall_fences_every_artifact_kind[collapsed_untracked_member]`
    is that case. So a phase can leave stray empty directories inside a read-only
    tree and the run will still pass. No bytes cross the fence.

    This test asserts the limitation so that a future fix breaks it loudly and the
    author knows to delete this test rather than wonder why the wall disagrees.
    """
    repo, protected, _ = fenced
    changes = _changes(repo, lambda: (protected / "a" / "b" / "c").mkdir(parents=True))
    assert not changes, (
        "empty directory trees became visible — the blind spot documented here is "
        "closed. Delete this test and add `empty_dir_tree` as a row in ARTIFACT_KINDS."
    )


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
