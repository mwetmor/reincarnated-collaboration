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
import re
import shutil
import stat
import subprocess
from dataclasses import dataclass
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


def _plant_hard_link(where: Path, repo: Path) -> str:
    """Content arrives without a write to this path's inode. Nothing in the fence
    should care, but nothing in the suite established that it doesn't."""
    os.link(repo / "tracked.txt", where / "hardlink.txt")
    return "hardlink.txt"


def _plant_pathspec_magic_name(where: Path) -> str:
    """Gate-2 L1, live. A perfectly legal filename that git reads as a PATHSPEC.

    `:(top)` is pathspec magic meaning *from the repository root*, so handing this
    name to `git checkout --` reverted an ENTIRE repository over one edited file and
    wrote `restored` on the receipt — K1's outcome, produced by K1's own guard. The
    same name handed to `ls-files` / `ls-tree` returns rc=0 and empty output while
    the content is in both the index and HEAD, and empty is what authorises `rmtree`.

    Magic is POSITIONAL, so this row only bites where the change path has no
    directory prefix — i.e. in the `read_only_worktree_root` fixture shape, which is
    the shape both shipped read-only trees actually have. In the subtree shape the
    `protected/` prefix neutralises it, and that is precisely why the wall now runs
    every round against both shapes.

    The artifact is a MODIFICATION of a file seeded into the baseline commit, not a
    creation. A created `:(top)` is rolled back with `unlink` and never reaches git,
    which is how the first version of this row passed while blind — see `_seed_tree`.
    """
    target = where / ":(top)"
    target.write_text(
        target.read_text(encoding="utf-8") + "THE PHASE TOUCHED THIS\n", encoding="utf-8"
    )
    return ":(top)"


def _plant_staged_artifact(where: Path, repo: Path) -> str:
    """Gate-2 L3. The DISCIPLINED agent: it creates a file and stages it.

    `A ` contains no `?`, so absence-from-baseline typed it `created` and the
    destroyer guard refused it — with a reason whose both clauses were false, since
    HEAD had never heard of the path and the identification was exactly right. Third
    round running in which the more disciplined git command is handled worst.
    """
    (where / "staged.txt").write_text("staged by the phase\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "--", str(where / "staged.txt")],
        cwd=str(repo), check=True, capture_output=True,
    )
    return "staged.txt"


def _plant_staged_modification(where: Path, repo: Path) -> str:
    """Gate-2 L2, general. The most ordinary thing a disciplined agent does.

    `git checkout -- <path>` restores from the INDEX. L2 was closed by re-typing the
    one status code the reviewer's `git mv` produced, but the property is not about
    renames: it holds for every code whose X column is non-space. A phase that edits
    a tracked file and stages it puts its own content where containment reads the
    baseline, so `checkout` rewrote the file with exactly the bytes being removed and
    the receipt said `restored`. Verified live before this row existed.

    The falsification partner matters more than usual here: the UNSTAGED edit must
    still come back genuinely restored, or the fix is just a blanket refusal.
    """
    target = where / "staged_edit.md"
    target.write_text("THE PHASE REWROTE THIS\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "--", str(target)], cwd=str(repo), check=True, capture_output=True
    )
    return "staged_edit.md"


def _plant_unstaged_modification(where: Path) -> str:
    """The staging guard's discrimination partner, and the reason it is a guard
    rather than a blanket refusal.

    Same file, same edit, no `git add`. Here the index still holds the baseline, so
    `git checkout -- <path>` really is a restore and round three's `restored` branch
    checks the CONTENTS against the phase-start fingerprint. If a future fix closes
    the staged case by refusing everything, this row goes red.
    """
    (where / "staged_edit.md").write_text("THE PHASE REWROTE THIS\n", encoding="utf-8")
    return "staged_edit.md"


def _plant_staged_dir_removal(where: Path, repo: Path) -> str:
    """Gate-2 L8. The row that proves a guard keyed on a LABEL is keyed on nothing.

    The phase edits a tracked file, stages it, then removes the whole directory. git
    names the file (`MD`), and the structure sweep separately names the DIRECTORY —
    with `after_status="structure"`, a label this module invents. The code-based
    staging guard measured that string, found it was not two characters, answered
    "not staged", and handed `protected/pkg` to `git checkout --`, which restored the
    directory FROM THE INDEX. The phase's own bytes landed back inside the fenced
    tree under a receipt reading `restored`, on the row beside an honest refusal for
    the same file.

    Two rows, same breach, opposite answers — and the wrong one was the one that
    acted. Reproduced against the shipped module before this row existed.

    The directory must be CLEAN at phase start. Dirt under it sets `was_dirty_before`
    and the change is dropped long before any verb is chosen, which is precisely why
    six rounds of wall rows never touched this path.
    """
    subprocess.run(
        ["git", "add", "--", str(where / "pkg" / "mod.py")],
        cwd=str(repo), check=True, capture_output=True,
    )
    (where / "pkg" / "mod.py").write_text("THE PHASE STAGED THIS\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "--", str(where / "pkg" / "mod.py")],
        cwd=str(repo), check=True, capture_output=True,
    )
    shutil.rmtree(where / "pkg")
    return "pkg"


def _plant_staged_rename(where: Path, repo: Path) -> str:
    """Gate-2 L2. `git mv` — the command round four's J1 was about.

    The destination carries `R `, which contains no `A` and does not start with `D`,
    so the first enumeration defaulted it to `modified`; `git checkout --` then
    restored it FROM THE INDEX THE PHASE HAD JUST STAGED, leaving the file exactly as
    the phase wrote it under a receipt reading `restored`. Pre-fix the same artifact
    came back with an honest refusal, so the fix converted a refusal into a lie.
    """
    subprocess.run(
        ["git", "mv", str(where / "movable.md"), str(where / "renamed.md")],
        cwd=str(repo), check=True, capture_output=True,
    )
    return "renamed.md"


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
    # added closing L1/L2/L3 (Gate-2 round six) — the four predicates added in round
    # five shipped without rows, so the round-five rule ("a new measurement surface
    # gets its row before it ships") was written down and then applied to measurement
    # surfaces only. A new PREDICATE gets one too.
    "pathspec_magic_name": _plant_pathspec_magic_name,
    "staged_artifact": _plant_staged_artifact,
    "staged_modification": _plant_staged_modification,
    "staged_rename": _plant_staged_rename,
    "unstaged_modification": _plant_unstaged_modification,
    # added closing L8 (Gate-2 round seven) — round six's staging guard read a status
    # STRING, so the one change carrying a string this module wrote itself walked
    # straight past it. The rule grows again: a new predicate gets a row that reaches
    # it by EVERY route a change can arrive on, not just the route git labels.
    "staged_dir_removal": _plant_staged_dir_removal,
}

#: Planters needing the repo root as well as the plant directory. In the
#: `read_only_worktree_root` shape these are the same path, which is exactly the
#: coincidence the old `where.parent` idiom was silently relying on.
_NEEDS_REPO = frozenset(
    {
        "hard_link", "staged_artifact", "staged_modification", "staged_rename",
        "staged_dir_removal",
    }
)


def _plant(kind: str, where: Path, tmp: Path, repo: Path) -> str:
    planter = ARTIFACT_KINDS[kind]
    if kind == "symlink_pointing_out_of_the_tree":
        return planter(where, tmp)
    if kind in _NEEDS_REPO:
        return planter(where, repo)
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


#: The uncommitted work every fenced tree carries at phase start. K1's damage was
#: "a rollback destroying uncommitted modifications to tracked files", and for four
#: rounds no wall row had any such work to destroy — every fixture committed
#: everything, so the entire damage class was unobservable and L1(a) shipped green
#: under 262 tests. One tracked file, dirty before the phase runs, that no artifact
#: kind touches. Asserting it survives is a single line that catches K1, L1(a) and
#: whatever comes next in the family (Gate-2 L4(ii)).
CANARY_TEXT = "COMMITTED BASELINE\nPRECIOUS UNCOMMITTED WORK IN FLIGHT\n"

#: Committed content for the file the staged/unstaged modification rows edit.
BASELINE_EDIT_TEXT = "ORIGINAL COMMITTED CONTENT\n"


@dataclass
class Fence:
    """One fenced-tree SHAPE, with the writable place its falsification partner uses.

    The wall ran for four rounds against a single shape — a read-only SUBDIRECTORY of
    a repo — under a docstring claiming it was the shipped shape. It is not. Both
    shipped `read_only_trees` (`~/Games/reincarnated-engine`, `~/Games/reincarnated-godot`)
    are worktree ROOTS that are also `repos:` entries, so their change paths carry no
    directory prefix. That missing prefix is the whole of L1's reachability: pathspec
    magic is positional. An identical row is green in the subtree shape and red in the
    shipped one (Gate-2 L4(i)).
    """

    shape: str
    repo: Path                  # the repo artifacts are planted in and measured against
    fenced_dir: Path            # where artifacts are planted
    prefix: str                 # repo-relative prefix of fenced_dir; "" at a worktree root
    read_only_trees: list[Path]
    declared_trees: list[Path]
    structure_roots: list[Path]
    free_repo: Path             # the falsification partner's repo
    free_dir: Path              # ...and its allowlisted directory
    free_prefix: str
    free_structure_roots: list[Path]
    free_writes: list[str]
    canary: Path

    def __iter__(self):
        """`repo, protected, workspace = fence` — the shape the named regressions
        below were written against, kept so a reproduction reads as its own story
        rather than as a fixture-plumbing exercise."""
        return iter((self.repo, self.fenced_dir, self.free_dir))


def _seed_tree(d: Path) -> None:
    """Tracked content the mode-only, type-change, rename and pathspec-magic kinds
    need to exist BEFORE the baseline commit.

    `:(top)` is seeded rather than planted because the artifact kind that needs it
    is a MODIFICATION. Round six shipped the magic row as a planter that CREATED
    `:(top)`, and a created file is rolled back with `unlink` — which never hands
    the name to git at all. The row was green under a mutation that removed the fix
    it was written to hold, because it exercised the wrong verb. Tracked-and-dirty
    is the only state in which `git checkout -- ':(top)'` is ever reached.
    """
    d.mkdir(parents=True, exist_ok=True)
    (d / "movable.md").write_text("movable\n", encoding="utf-8")
    (d / "swappable.md").write_text("swappable\n", encoding="utf-8")
    (d / ":(top)").write_text("a legally-named file\n", encoding="utf-8")
    (d / "staged_edit.md").write_text(BASELINE_EDIT_TEXT, encoding="utf-8")
    # Gate-2 L8 needs a CLEAN tracked subdirectory to delete. It has to be clean:
    # any dirt under it at phase start sets `was_dirty_before` and the change never
    # reaches the rollback verb at all, which is how the case stayed invisible.
    (d / "pkg").mkdir(exist_ok=True)
    (d / "pkg" / "mod.py").write_text(BASELINE_EDIT_TEXT, encoding="utf-8")


def _git_init(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for args in (
        ("init", "-q"),
        ("config", "user.email", "factory-test@example.invalid"),
        ("config", "user.name", "factory test"),
    ):
        subprocess.run(["git", *args], cwd=str(root), check=True, capture_output=True)
    (root / "tracked.txt").write_text("baseline\n", encoding="utf-8")
    (root / ".gitignore").write_text("ignored/\n", encoding="utf-8")


def _commit_all(root: Path, msg: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=str(root), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", msg], cwd=str(root), check=True, capture_output=True
    )


def _build_fence(shape: str, git_repo: Path, tmp_path: Path) -> Fence:
    workspace = git_repo / "workspace"
    _seed_tree(git_repo / "protected")
    _seed_tree(workspace)

    if shape == "read_only_subtree":
        protected = git_repo / "protected"
        (protected / "canary.md").write_text("COMMITTED BASELINE\n", encoding="utf-8")
        _commit_all(git_repo, "fence")
        fence = Fence(
            shape=shape,
            repo=git_repo,
            fenced_dir=protected,
            prefix="protected",
            read_only_trees=[protected],
            declared_trees=[git_repo, protected],
            structure_roots=[protected, workspace],
            free_repo=git_repo,
            free_dir=workspace,
            free_prefix="workspace",
            free_structure_roots=[protected, workspace],
            free_writes=["workspace/**", "workspace"],
            canary=protected / "canary.md",
        )
    else:
        # The shipped shape: the read-only tree IS a worktree root, and is also the
        # `repos:` entry. Change paths therefore have no directory prefix.
        sibling = tmp_path / "fenced-root"
        _git_init(sibling)
        _seed_tree(sibling)
        (sibling / "canary.md").write_text("COMMITTED BASELINE\n", encoding="utf-8")
        _commit_all(sibling, "fence")
        _commit_all(git_repo, "hub")
        fence = Fence(
            shape=shape,
            repo=sibling,
            fenced_dir=sibling,
            prefix="",
            read_only_trees=[sibling],
            declared_trees=[sibling],
            structure_roots=[sibling],
            free_repo=git_repo,
            free_dir=workspace,
            free_prefix="workspace",
            free_structure_roots=[git_repo / "protected", workspace],
            free_writes=["workspace/**", "workspace"],
            canary=sibling / "canary.md",
        )

    # The canary goes dirty AFTER the commit and BEFORE any baseline is taken, so it
    # is uncommitted work in flight for the whole of every phase.
    fence.canary.write_text(CANARY_TEXT, encoding="utf-8")
    return fence


@pytest.fixture(params=["read_only_subtree", "read_only_worktree_root"])
def fenced(request, git_repo: Path, tmp_path: Path) -> Fence:
    """The wall's fixture. Every round runs against BOTH shapes. See `Fence`."""
    return _build_fence(request.param, git_repo, tmp_path)


@pytest.fixture
def fenced_subtree(git_repo: Path, tmp_path: Path):
    """The named regressions below reproduce SPECIFIC historical defects, each of
    which occurred in the subtree shape, and several hardcode `protected/…` paths.
    Running a reproduction against a shape it never occurred in tests nothing.

    The distinction is deliberate: the WALL is the thing that must cover both shapes,
    because the wall is what has to catch the next defect. These are the receipts for
    defects already caught.
    """
    return _build_fence("read_only_subtree", git_repo, tmp_path)


def _assert_canary_survived(f: Fence, kind: str, actions) -> None:
    """The one assertion that catches the whole K1/L1 damage class."""
    assert f.canary.exists(), (
        f"rolling back a {kind} in the {f.shape} shape DELETED {f.canary.name}, a "
        "tracked file no artifact touched."
    )
    assert f.canary.read_text(encoding="utf-8") == CANARY_TEXT, (
        f"rolling back a {kind} in the {f.shape} shape destroyed uncommitted work on "
        f"{f.canary.name}, a tracked file NO ARTIFACT TOUCHED. Actions were "
        f"{[(a.path, a.action) for a in actions]}. This is the K1/L1 shape: a "
        "pathspec that named more than the artifact, handed to a verb that acts on "
        "what it names. Containment must never be the thing that destroys work."
    )


def _assert_refusal_claims_are_true(f: Fence, action, kind: str) -> None:
    """A refusal states FACTS about the tree, and the facts must hold.

    Round three asked only that a NOT_ROLLED_BACK action carry a non-empty reason.
    That is the weaker question: Gate-2 L3 was a refusal with a perfectly good
    non-empty reason whose *both clauses were false* — it claimed HEAD held content
    it had never heard of, and claimed a misidentification that had not occurred.
    A reason nobody checks is a comment, and the mutation that collapsed the
    three-way branch back to one left every row green.

    So the numeric claims are re-derived from git and compared. Nothing here parses
    prose for its own sake: these are the load-bearing sentences an operator reads
    off an abort report and acts on.
    """
    reason = action.reason or ""
    truth = perm._tracked_under(f.repo, action.path)
    for pattern, actual, what in (
        (r"HEAD (?:still )?holds (\d+) file\(s\)", len(truth.in_head), "HEAD"),
        (r"index holds (\d+) file\(s\)", len(truth.in_index), "the index"),
    ):
        for claimed in re.findall(pattern, reason):
            assert int(claimed) == actual, (
                f"the refusal for a {kind} claims {what} holds {claimed} file(s) "
                f"under {action.path!r}; it holds {actual}. Reason was: {reason}"
            )
    #: A count is not a claim on its own. `elif True:` collapsing the three-way
    #: branch produced "HEAD holds 0 file(s) under it — the path identification is
    #: wrong", which is NUMERICALLY TRUE and completely false: HEAD holds nothing,
    #: the identification was right, and the real reason (the phase staged it) went
    #: unsaid. Checking the arithmetic passed that mutation; checking that the
    #: sentence is the one the facts support does not.
    #: Gate-2 B1/B2. The two assertions that stood here were gated on literal phrases
    #: — "HEAD still holds", "index no longer" — and round seven deleted BOTH from the
    #: product in the same commit that made the wall require them. They read as
    #: coverage and could not fire: 2 of 365 assertions in the suite never executed,
    #: and one of them was the fix reported as closing L9. A test keyed on a phrase is
    #: keyed on a label, which is the exact disease this review has been chasing
    #: through the product code, transplanted into the thing that certifies it.
    #:
    #: So the measurements TRAVEL on the action, the sentence is RENDERED from them by
    #: the product, and the wall derives the same numbers from git independently and
    #: asserts the rendered clause is present. There is nowhere left for a wording to
    #: disagree with the tree, and no literal for a later commit to orphan.
    #: ...and the first version of THAT fix was `if action.facts:` — a check the
    #: product switches off simply by sending nothing. Mutation N6 dropped the
    #: measurements at the constructor and the suite stayed green: the third instance
    #: of this round's own defect, living inside the fix for the first one. Whether a
    #: refusal OWES the operator numbers is a question about the TREE, so it is asked
    #: of git. If the index differs from HEAD here, the refusal that stopped the run
    #: carries the measurements or this row is red.
    expected = {
        "head_files": len(truth.in_head),
        "index_files": len(truth.in_index),
        "staged_paths": len(perm._staged_against_head(f.repo, action.path).paths),
    }
    if expected["staged_paths"]:
        assert action.facts, (
            f"git says {expected['staged_paths']} path(s) under {action.path!r} have "
            f"an index differing from HEAD, and containment refused to undo a {kind} "
            "there — but the refusal carries no measurements at all, so the operator "
            f"is being asked to act on prose. Reason was: {reason}"
        )
    if action.facts:
        assert dict(action.facts) == expected, (
            f"the refusal for a {kind} carries measurements {dict(action.facts)} for "
            f"{action.path!r}; git says {expected}. These are the numbers an operator "
            "reads off an abort report and acts on."
        )
        rendered = perm.render_containment_facts(tuple(expected.items()))
        assert rendered in reason, (
            f"the refusal for a {kind} does not state the facts it rests on. Expected "
            f"{rendered!r} to appear in the reason, which was: {reason}"
        )
    if truth.in_index and not truth.in_head:
        assert "index" in reason, (
            f"the only thing holding {action.path!r} is the phase's own INDEX — "
            "nothing is committed, nothing is at risk, and the identification is "
            "right. A refusal that does not say `index` here is telling the operator "
            f"the wrong story about why their run stopped. Reason was: {reason}"
        )
    #: A THIRD dead gate lived here — `if "HEAD holds none" in reason:` — which the
    #: B2 standing check found on its first run, one more than the Gate-2 line-trace
    #: audit reported. Same cause: the phrase had been reworded in the product and
    #: the gate was left behind holding nothing. The structured-facts assertion above
    #: covers what it was for, and covers it by number rather than by wording.


def _snapshot(f: Fence, plant) -> tuple[perm.TreeFingerprint, list[perm.Change]]:
    """The fenced tree is measured; the writable place is measured separately.

    Measurement scope and fence scope are different questions, and measuring the
    writable side too is what lets the `empty_directory_tree` row have a real
    falsification partner: the same empty tree planted in an allowlisted directory is
    seen, and must still come back ALLOWED.
    """
    before = perm.fingerprint(f.repo, structure_roots=f.structure_roots)
    assert before.usable, f"baseline unusable: {before.error}"
    plant()
    after = perm.fingerprint(f.repo, structure_roots=f.structure_roots)
    assert after.usable, f"post-plant fingerprint unusable: {after.error}"
    return before, perm.diff_fingerprints(before, after)


def _changes(f: Fence, plant) -> list[perm.Change]:
    return _snapshot(f, plant)[1]


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
    before: perm.TreeFingerprint, f: "Fence", rel: str, kind: str
) -> None:
    """A `restored` path must be back at its phase-start fingerprint, contents included."""
    now = perm.fingerprint(f.repo, structure_roots=f.structure_roots)
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


def _names(changes: list[perm.Change], rel: str, prefix: str) -> bool:
    """Is `prefix/rel` actually NAMED by the change-set?

    Either exactly, or by an ancestor — git collapses a wholly-untracked directory
    to one entry, so the ancestor is the only record that exists and it is a true
    record of the artifact. Deliberately NOT the other direction: a change *below*
    the artifact does not name it, and accepting that is how a fabricated path
    satisfies the check (J1).
    """
    want = (f"{prefix}/{rel}" if prefix else rel).rstrip("/")
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
    f = fenced
    planted: list[str] = []
    changes = _changes(
        f, lambda: planted.append(_plant(kind, f.fenced_dir, tmp_path, f.repo))
    )
    assert changes, (
        f"a {kind} was planted inside the tree ({f.shape}) and the fingerprint diff "
        "was EMPTY. An empty diff is indistinguishable from innocence."
    )
    assert _names(changes, planted[0], f.prefix), (
        f"a {kind} was planted at {f.prefix}/{planted[0]!r} and the change-set names "
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
    f = fenced
    changes = _changes(f, lambda: _plant(kind, f.fenced_dir, tmp_path, f.repo))
    allowed, breaches = perm.classify(
        changes, writes=["**"], root=f.repo, read_only_trees=f.read_only_trees
    )
    assert breaches, f"a {kind} inside the read-only tree ({f.shape}) was not a breach"
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
    f = fenced
    before, changes = _snapshot(f, lambda: _plant(kind, f.fenced_dir, tmp_path, f.repo))
    _, breaches = perm.classify(
        changes, writes=["**"], root=f.repo, read_only_trees=f.read_only_trees
    )
    # The REAL phase-start fingerprint, not `{}`. Passing an empty map left
    # `was_dirty_before` False in all fifty-six parametrized runs, so the
    # pre-existing-dirt guard — landed twice, by K1(3) and K4 — was exercised by one
    # dedicated test and by no row of the wall (Gate-2 L4(ii)).
    actions = perm.rollback(
        breaches, {str(f.repo): before}, tmp_path / "quarantine",
        declared_trees=f.declared_trees,
    )
    assert actions, f"a {kind} breached and the rollback recorded nothing at all"
    _assert_canary_survived(f, kind, actions)

    for a in actions:
        target = f.repo / a.path
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
            _assert_contents_match(before, f, a.path, kind)
        else:
            assert a.action == "NOT_ROLLED_BACK", f"unknown action {a.action!r}"
            assert a.reason, (
                f"{a.path!r} was left in place after a {kind} with no stated reason. "
                "Evidence left deliberately is fine; evidence left silently is not."
            )
            _assert_refusal_claims_are_true(f, a, kind)


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
    f = fenced
    before, changes = _snapshot(f, lambda: _plant(kind, f.fenced_dir, tmp_path, f.repo))
    _, breaches = perm.classify(
        changes, writes=["**"], root=f.repo, read_only_trees=f.read_only_trees
    )
    actions = perm.rollback(
        breaches, {str(f.repo): before}, tmp_path / "quarantine",
        declared_trees=f.declared_trees,
    )
    _assert_canary_survived(f, kind, actions)

    after = perm.fingerprint(f.repo, structure_roots=f.structure_roots)
    assert after.usable, f"post-rollback fingerprint unusable: {after.error}"
    residue = perm.diff_fingerprints(before, after)
    named = {a.path.rstrip("/") for a in actions}
    unaccounted = _unaccounted(residue, named)
    assert not unaccounted, (
        f"after rolling back a {kind} ({f.shape}), the tree has not returned to its "
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
    f = fenced
    free = Fence(
        shape=f.shape,
        repo=f.free_repo,
        fenced_dir=f.free_dir,
        prefix=f.free_prefix,
        read_only_trees=[],
        declared_trees=[f.free_repo],
        structure_roots=f.free_structure_roots,
        free_repo=f.free_repo,
        free_dir=f.free_dir,
        free_prefix=f.free_prefix,
        free_structure_roots=f.free_structure_roots,
        free_writes=f.free_writes,
        canary=f.canary,
    )
    changes = _changes(free, lambda: _plant(kind, f.free_dir, tmp_path, f.free_repo))
    allowed, breaches = perm.classify(
        changes, writes=f.free_writes, root=f.free_repo,
        read_only_trees=[f.free_repo / "protected"],
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
def test_J1a_a_git_mv_OUT_of_the_fence_names_the_SOURCE(fenced_subtree):
    """The old parser kept `split(" -> ")[-1]`, the DESTINATION, and dropped the
    source. So `git mv` out of a read-only tree into the phase's own allowlist
    produced a change-set naming only a legal path — the fenced file was gone and
    the run passed. Using the *more* disciplined command was the difference between
    caught and clean."""
    f = fenced_subtree
    repo = f.repo

    def do_move():
        subprocess.run(
            ["git", "mv", "protected/movable.md", "workspace/exfiltrated.md"],
            cwd=str(repo), check=True, capture_output=True,
        )

    changes = _changes(f, do_move)
    assert _names(changes, "movable.md", f.prefix), (
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


def test_J1a_partner_a_rename_entirely_inside_the_allowlist_is_allowed(fenced_subtree):
    """Falsification partner: renames are not breaches, renames ACROSS the fence are."""
    f = fenced_subtree
    repo = f.repo

    def do_move():
        subprocess.run(
            ["git", "mv", "workspace/movable.md", "workspace/renamed.md"],
            cwd=str(repo), check=True, capture_output=True,
        )

    changes = _changes(f, do_move)
    allowed, breaches = perm.classify(
        changes, writes=["workspace/**"], root=repo,
        read_only_trees=[repo / "protected"],
    )
    assert allowed and not breaches, f"a legal rename was refused: {breaches}"


def test_J1c_the_rollback_never_deletes_tracked_content(fenced_subtree, tmp_path):
    """The third face, and the worst: the fabricated path the old parser produced was
    a REAL path at the repo root, and the rollback acted on it — deleting the very
    read-only tree it was fencing, from a file the phase was ALLOWED to write.

    The parser fix removes the cause. This asserts the structural guard, which does
    not depend on knowing which parse bug produced the bad path: a `created` path
    cannot contain anything git already tracks, so if it does, our identification is
    wrong and the deletion is refused. Containment must never destroy work."""
    repo, protected, _ = fenced_subtree
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
    # The reason must name HEAD, because HEAD is what makes this unsurvivable. A
    # refusal citing the index alone would be true of the phase's own staged writes
    # too, and those are a different decision (Gate-2 L3).
    assert "HEAD holds" in actions[0].reason, (
        f"the refusal did not say WHICH question answered yes: {actions[0].reason!r}"
    )


def test_J1c_partner_the_guard_still_deletes_a_genuine_creation(fenced_subtree, tmp_path):
    """Without this, a rollback that refused everything would pass the test above and
    the containment would quietly stop rolling anything back."""
    repo, protected, _ = fenced_subtree
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
def test_a_WHOLLY_EMPTY_directory_tree_is_STILL_invisible_to_git_itself(fenced_subtree):
    """The premise, pinned. If git ever starts reporting these, the structure sweep
    below becomes redundant and someone should know to delete it."""
    repo, protected, _ = fenced_subtree
    before = perm.fingerprint(repo)
    (protected / "a" / "b" / "c").mkdir(parents=True)
    after = perm.fingerprint(repo)
    assert not perm.diff_fingerprints(before, after), (
        "git now reports empty directory trees; the structure sweep is redundant"
    )


def test_an_empty_directory_tree_in_a_READ_ONLY_tree_is_caught_by_the_structure_sweep(fenced_subtree):
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
    repo, protected, _ = fenced_subtree
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


def test_the_structure_sweep_does_not_fire_on_an_unchanged_tree(fenced_subtree):
    """Falsification partner. A sweep that reported a delta every time would pass the
    test above and abort every run — the M7 failure mode, one layer down."""
    repo, protected, _ = fenced_subtree
    before = perm.fingerprint(repo, structure_roots=[protected])
    after = perm.fingerprint(repo, structure_roots=[protected])
    assert not perm.diff_fingerprints(before, after), (
        "the structure sweep is not stable across two reads of an untouched tree"
    )


def test_the_structure_sweep_is_scoped_to_the_trees_it_is_given(fenced_subtree):
    """It is affordable BECAUSE it is scoped. A fingerprint taken without
    `structure_roots` must not walk anything."""
    repo, _, _ = fenced_subtree
    assert perm.fingerprint(repo).structure == {}


# ---------------------------------------------------------------------------
# K1-K4 — Gate-2 round five. The defect was in round four's own fix.
# ---------------------------------------------------------------------------
def test_K1_a_structure_change_is_reported_at_the_DIRECTORY_not_at_the_tree(fenced_subtree):
    """The whole of K1 in one assertion.

    The first structure sweep returned `dirs:<n>:<hash>`. A hash can say that
    something moved and nothing about what, so the diff reported the change at the
    TREE ROOT — and the rollback handed that to `git checkout --` as a pathspec,
    reverting every uncommitted change in the repository over one empty directory,
    while the directory itself survived. The receipt word was `restored`.

    A measurement that cannot NAME what moved must not be wired to a verb that acts
    on what it names.
    """
    repo, protected, _ = fenced_subtree
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


def test_K1_the_rollback_REFUSES_a_pathspec_that_names_a_whole_tree(fenced_subtree, tmp_path):
    """The structural guard, independent of what produced the coarse path.

    This is the destroyer guard's principle applied to the other destructive verb.
    `git checkout -- .` is not a smaller act than `rm -rf` — it silently discards
    every uncommitted modification in the repository — and no measurement in this
    module is ever entitled to trigger it.
    """
    repo, protected, _ = fenced_subtree
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


def test_K1_partner_the_rollback_still_restores_a_named_file(fenced_subtree, tmp_path):
    """Falsification partner: a guard that refused every restore would pass the test
    above and quietly stop rolling anything back."""
    repo, protected, _ = fenced_subtree
    (protected / "movable.md").write_text("PHASE WROTE THIS\n", encoding="utf-8")
    change = perm.Change(repo, "protected/movable.md", "modified", None, " M")
    actions = perm.rollback(
        [perm.Breach(change, "planted")], {}, tmp_path / "q",
        declared_trees=[repo, protected],
    )
    assert actions[0].action == "restored", f"a named file was not restored: {actions}"
    assert (protected / "movable.md").read_text() == "movable\n"


def test_K2_a_clean_tracked_file_modified_by_a_phase_is_MODIFIED_not_created(fenced_subtree, tmp_path):
    """A tracked file nobody has touched is absent from `git status`, and absence was
    read as newness. So the most likely agentic breach there is — an agent edits a
    committed source file — was typed `created`, hit the destroyer guard, and came
    back NOT_ROLLED_BACK with a reason asserting a misidentification that had not
    occurred. The edit stayed in the read-only tree after the abort."""
    f = fenced_subtree
    repo, protected, _ = f
    changes = _changes(
        f, lambda: (protected / "movable.md").write_text("AGENT EDIT\n", encoding="utf-8")
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


def test_K3_the_destroyer_guard_asks_HEAD_as_well_as_the_index(fenced_subtree, tmp_path):
    """`git ls-files` reads the index, and the index can be silenced while the content
    is still committed and still on disk. A phase that runs `git rm --cached` leaves
    the path CLEAN at phase start, so the pre-existing-dirt guard correctly does not
    fire and the destroyer guard is the only thing standing between the rollback and
    committed work. Asking one question got the answer `no tracked content` for a
    directory full of it."""
    repo, protected, _ = fenced_subtree
    subprocess.run(
        ["git", "rm", "--cached", "-q", "-r", "protected"],
        cwd=str(repo), check=True, capture_output=True,
    )
    assert not subprocess.run(
        ["git", "ls-files", "--", "protected"],
        cwd=str(repo), capture_output=True, text=True,
    ).stdout.strip(), "the premise failed: the index still reports this path"
    tracked = perm._tracked_under(repo, "protected")
    #: Named, not counted. A bare count here has had to be edited every time the
    #: fixture seeded another file, and each edit was a chance to quietly accept a
    #: SMALLER answer — which is the failure this row exists to catch.
    seeded = {
        "protected/:(top)",
        "protected/canary.md",
        "protected/movable.md",
        "protected/pkg/mod.py",
        "protected/staged_edit.md",
        "protected/swappable.md",
    }
    assert set(tracked.in_head) == seeded, (
        "HEAD still holds every file seeded under protected/ and the guard must see "
        f"all of them — missing {sorted(seeded - set(tracked.in_head))} from {tracked}"
    )
    assert tracked.count == len(seeded), f"the union miscounted — {tracked}"
    assert not tracked.in_index, (
        "the guard must keep the two answers APART: this is the case where HEAD says "
        f"yes and the index says no, and they mean different things — {tracked}"
    )
    change = perm.Change(repo, "protected", "created", None, "??")
    actions = perm.rollback(
        [perm.Breach(change, "misidentified")], {}, tmp_path / "q",
        declared_trees=[repo],
    )
    assert (protected / "movable.md").exists() and (protected / "swappable.md").exists(), (
        "the rollback deleted committed content because the index had been silenced"
    )
    assert actions[0].action == "NOT_ROLLED_BACK" and "HEAD holds" in actions[0].reason


def test_K4_a_collapsed_ignored_dir_dirty_at_phase_start_is_refused_BY_THAT_REASON(
    fenced_subtree, tmp_path
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
    repo, protected, _ = fenced_subtree
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


def test_K1_ordinary_git_activity_does_not_move_the_structure(fenced_subtree):
    """K1's TRIGGER, which is separate from its consequence.

    `.git` is 281 of the engine's 968 directories and 276 of godot's 5,240, and its
    object fanout gains a directory on a plain `git add`. With `.git` in the walk,
    the most disciplined thing an agent can do in a read-only tree — stage its work
    rather than leave it loose — was itself the breach that triggered the repo-wide
    revert. Nothing the sweep exists to catch lives under `.git`: a PEP-420 namespace
    package and a Godot `res://` import target are both worktree facts.
    """
    repo, protected, _ = fenced_subtree
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


def test_K1_partner_the_sweep_still_sees_a_directory_outside_dot_git(fenced_subtree):
    """Falsification partner: a sweep that skipped everything would pass the test
    above and see nothing at all."""
    repo, protected, _ = fenced_subtree
    before = perm.structure_dirs(repo)
    (protected / "empty_pkg").mkdir()
    assert perm.structure_dirs(repo) - before == {"protected/empty_pkg"}


def test_K5_round_four_does_not_accept_an_OVER_BROAD_name(fenced_subtree, tmp_path):
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
    f = fenced_subtree
    repo, protected, _ = f
    before, _ = _snapshot(
        f,
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
