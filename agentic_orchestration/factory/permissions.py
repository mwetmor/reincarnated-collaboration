"""Permissions fingerprinting — Spec A § 8, the v1 containment (D5: sandboxes deferred).

Fingerprint the working tree before and after each phase. Any write outside the
phase's `writes` allowlist is a BREACH: quarantine the evidence, roll back what
can be rolled back safely, and ABORT the run. A breach is evidence, never noise,
and never a retry.

Two safety rules the rollback obeys, because a containment mechanism that
destroys work is worse than the breach it contains:

1. **Only phase-window deltas are touched.** A path that was already dirty when
   the phase started is baseline; the rollback never restores over it. It is
   reported as NOT_ROLLED_BACK with the reason.
2. **Bytes are quarantined before they are removed.** Every breaching file is
   copied into `sessions/{run_id}/breach/` first. Nothing is deleted unquarantined.

**Gitignored paths are fingerprinted too** (Gate-2 F1 / DRIFT-CRITIC D-1, both
reviewers independently, 2026-08-10). The v1 build scoped the whole world-model to
`git status --porcelain`, which never reports ignored paths -- so every gitignored
region of every declared tree was silently unfenced, including the engine's 3.3 GB
`seasons/` and its 450 MB untracked `telemetry.db`. The original reason was sound
(the factory's own `sessions/` writes were reading as self-breaches on a PROTECTED
path) but the remedy was a CATEGORY exemption for a NAMED-PATH problem. The
exemption is now the named list `FACTORY_RUNTIME_PATHS`, and everything else that
git ignores is measured like anything else.

Where a region is too large to stat file-by-file within `_IGNORED_SCAN_CAP`, it
falls back to a directory-mtime sweep, is recorded on the fingerprint as `coarse`,
and is surfaced to receipts on every phase. A weaker measurement is declared as a
weaker measurement; nothing is ever assumed clean.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

PROTECTED_ALWAYS: tuple[str, ...] = (
    "agentic_orchestration/factory/",  # no self-modification
    "canonical/",
    ".claude/",
)

FACTORY_RUNTIME_PATHS: tuple[str, ...] = (
    "agentic_orchestration/factory/sessions/",
    "agentic_orchestration/factory/receipts.db",
    "agentic_orchestration/factory/receipts.db-wal",
    "agentic_orchestration/factory/receipts.db-shm",
    "agentic_orchestration/factory/__pycache__/",
    "agentic_orchestration/factory/.pytest_cache/",
)
"""The factory's OWN runtime writes, exempted BY NAME in the root repo only.

This is the whole exemption. It is a list of six paths rather than the category
"anything git ignores", because the category version is what let a write to the
engine's telemetry DB pass as a green read-only proof. Factory *source* under the
same directory stays visible AND protected -- self-modification is still a breach.
"""

_QUARANTINE_MAX_BYTES = 64 * 1024 * 1024
_IGNORED_SCAN_CAP = 50_000

EXACT = "exact"      # every file stat'd: catches creation, deletion, in-place edits
COARSE = "coarse"    # directory mtimes + entry counts: catches structural change only
"""How thoroughly a region was measured. The receipt records this per region.

Measured on this host: the godot tree's `.godot/` + `Assets/Synty/` hold 259,000
files and stat-sweep in ~12 s -- times nine fingerprints per run, that is longer
than the run. The same regions have 905 directories and sweep in 0.12 s.

So an oversized region falls back to COARSE rather than going unmeasured. A
directory's mtime moves when an entry is added, removed, or renamed inside it, so
COARSE catches a phase creating or deleting files anywhere in the region. It does
NOT catch an in-place rewrite of an existing file's contents.

That is a weaker claim, and it is recorded as a weaker claim. The failure this
guards against is not "we measured imperfectly" -- it is "we measured nothing and
reported clean."
"""


def _git(root: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=check,
        stdin=subprocess.DEVNULL,
    )


def _stat_sig(path: Path) -> str:
    try:
        st = path.stat()
        return f"file:{st.st_size}:{st.st_mtime_ns}"
    except OSError as exc:
        return f"unreadable:{exc.errno}"


def _record_walk_error(h: "hashlib._Hash"):
    """os.walk error handler that folds the failure INTO the signature.

    The earlier handler was `lambda _: None` — an unreadable subtree was skipped in
    silence, so a directory that became unreadable between two snapshots produced
    identical signatures and the region read as unchanged (Gate-2 re-review G6).
    Permission is not the same as absence.

    Folding the error in means readability itself is part of what is measured: if a
    subtree stops being walkable mid-run, the signature moves and the change is
    caught. Fail closed.
    """

    def handler(exc: OSError) -> None:
        h.update(f"UNREADABLE:{exc.filename}:{exc.errno}".encode())

    return handler


def _coarse_signature(path: Path) -> tuple[str, int]:
    """Directory mtimes + entry counts. Returns (signature, total files seen).

    Cheap, and blind to in-place content edits. A directory's mtime moves when an
    entry is added, removed, or renamed inside it -- which is what an agent writing
    where it was told not to actually does. `os.walk` hands back the filename lists
    without stat-ing them, so the file count comes free with the sweep, and that
    count is what decides whether an exact sweep is affordable.
    """
    h = hashlib.sha256()
    dirs = 0
    files = 0
    for dirpath, dirnames, filenames in os.walk(path, onerror=_record_walk_error(h)):
        dirnames.sort()
        here = Path(dirpath)
        rel = "." if here == path else str(here.relative_to(path))
        h.update(f"{rel}:{_stat_sig(here)}:{len(filenames)}:{len(dirnames)}".encode())
        dirs += 1
        files += len(filenames)
    return f"coarse:{dirs}:{h.hexdigest()[:16]}", files


def _exact_signature(path: Path) -> str:
    """Stat every file in the tree. Catches in-place edits; costs one stat per file."""
    h = hashlib.sha256()
    count = 0
    for dirpath, dirnames, filenames in os.walk(path, onerror=_record_walk_error(h)):
        dirnames.sort()
        for name in sorted(filenames):
            member = Path(dirpath) / name
            h.update(f"{member.relative_to(path)}:{_stat_sig(member)}".encode())
            count += 1
    return f"dir:{count}:{h.hexdigest()[:16]}"


def _walk_signature(path: Path, cap: int) -> tuple[str, str]:
    """Measure a directory region as exactly as it can afford. Returns (sig, mode).

    Coarse first, ALWAYS -- it is the cheap pass and it yields the file count that
    decides the rest. Under `cap`, the region is re-swept exactly; over it, the
    coarse signature already in hand is the answer.

    Measured on this host: the engine's largest ignored region (`cache/`, 14,224
    files) sweeps exactly in 0.29 s -- affordable, so it is paid on every
    fingerprint. The godot tree's `.godot/` + `Assets/Synty/` hold 259,000 files:
    ~12 s exact against 0.12 s coarse, nine times per run.

    The first version of this fallback ran the exact sweep until it hit the cap and
    only THEN went coarse, which spent 50,000 stats per oversized region to learn
    something the cheap pass answers for free. That cost 2m36s of a 2m50s run.
    """
    coarse_sig, files = _coarse_signature(path)
    if files > cap:
        return coarse_sig, COARSE
    return _exact_signature(path), EXACT


def _signature(root: Path, rel: str) -> tuple[str, str]:
    """Change signature for a dirty path: size + mtime. Returns (sig, EXACT | COARSE).

    Deliberately NOT a content hash. Content comparison for TRACKED files is
    git's job (`git status --porcelain` already compares content, so an
    identical-content rewrite does not show up as a change). This signature has
    to catch movement in UNTRACKED and IGNORED paths, where git offers presence
    and nothing else. The engine tree carries ~2.8k dirty paths; hashing their
    contents per phase would cost more than the phase.

    Directory entries (git collapses both untracked and ignored dirs into one
    line) are stat-swept recursively. The earlier version summarised them from
    `ls-files --others --exclude-standard`, which excluded ignored members and
    was therefore blind to exactly the writes this mechanism exists to catch.
    """
    path = root / rel
    if rel.endswith("/") or path.is_dir():
        return _walk_signature(path, _IGNORED_SCAN_CAP)
    if not path.exists():
        return "", EXACT
    return _stat_sig(path), EXACT


@dataclass
class TreeFingerprint:
    root: Path
    head: str
    entries: dict[str, str] = field(default_factory=dict)         # path -> porcelain XY
    content: dict[str, str] = field(default_factory=dict)         # path -> signature (dirty only)
    is_git: bool = True
    error: str | None = None
    coarse: list[str] = field(default_factory=list)      # regions past the sweep cap
    exempted: list[str] = field(default_factory=list)    # factory runtime paths, by name
    #: repo-relative tree -> the set of directory paths inside it, tree-relative.
    #: Populated only for the read-only trees, which is the only place the cost is
    #: worth paying. Stored as the SET, not as a hash of it: a hash can only say
    #: "something moved", and a change the rollback cannot NAME is a change it must
    #: not act on (Gate-2 K1).
    structure: dict[str, set[str]] = field(default_factory=dict)

    @property
    def usable(self) -> bool:
        """False when this tree could not be measured at all.

        A fingerprint that failed is a containment FAILURE, not an empty diff.
        The v1 build recorded `is_git=False` honestly and then never read it, so
        a typo'd `repos:` entry silently disarmed the fence for that tree
        (Gate-2 F2). Callers must consult this before trusting a diff.
        """
        return self.is_git and self.error is None


@dataclass
class Change:
    root: Path
    path: str            # repo-relative
    kind: str            # created | modified | deleted | committed
    before_status: str | None
    after_status: str | None

    @property
    def key(self) -> str:
        return f"{self.root.name}:{self.path}"


@dataclass
class Breach:
    change: Change
    reason: str


@dataclass
class RollbackAction:
    path: str
    action: str          # deleted | restored | NOT_ROLLED_BACK
    reason: str = ""
    quarantined_to: str | None = None


def _is_factory_runtime(rel: str, is_root_repo: bool) -> bool:
    """The six named exemptions — root repo only, prefix match, nothing wider."""
    if not is_root_repo:
        return False
    return any(rel.startswith(p) or rel == p.rstrip("/") for p in FACTORY_RUNTIME_PATHS)


#: Synthetic code for the SOURCE half of a rename. git names both endpoints; the
#: source has left the worktree, so it resolves to a `deleted` change.
RENAME_SOURCE = "R<"


def _parse_porcelain_z(out: str) -> list[tuple[str, str]]:
    """`git status --porcelain -z` records as (code, path) pairs — BOTH ends of a rename.

    Gate-2 J1, three consequences of one line. The previous parser was
    `rest.split(" -> ")[-1].strip().strip('"')` against porcelain v1, and:

    1. It kept only the LAST field of a rename, discarding the SOURCE. `git mv` out of
       a fenced tree therefore produced a change-set that named only the destination,
       and a destination inside the phase's allowlist read as entirely legal — the
       fenced file was gone and the run passed. Using the *more* disciplined command
       was the difference between caught and clean.
    2. `strip('"')` is not unquoting. Porcelain v1 C-quotes any path with a special
       character, so a filename could carry the rename delimiter itself: an entry for
       `protected/'a -> b.txt'` parsed to `b.txt` at the repo root.
    3. That fabricated path is a REAL path, and the rollback acts on it. A phase
       writing one harmless file named `junk -> src` inside its own allowlist induced
       the rollback to delete `src/` — the read-only tree it was fencing. Containment
       became the destroyer, from a write the phase was permitted to make.

    `-z` has none of this: NUL-separated, never quoted, rename origin as its own
    record. The origin is emitted here as a separate (RENAME_SOURCE, path) pair so
    that both ends of a rename are fenced independently.
    """
    out = out.rstrip("\0")
    if not out:
        return []
    records = out.split("\0")
    pairs: list[tuple[str, str]] = []
    i = 0
    while i < len(records):
        rec = records[i]
        i += 1
        if not rec:
            continue
        code, path = rec[:2], rec[3:]
        if not path:
            continue
        pairs.append((code, path))
        # A rename/copy record is followed by exactly one record holding the origin.
        if "R" in code or "C" in code:
            if i < len(records):
                origin = records[i]
                i += 1
                if origin:
                    pairs.append((RENAME_SOURCE, origin))
    return pairs


_UNREADABLE_WARNING = "could not open directory '"


def _unreadable_paths(stderr: str) -> list[str]:
    """Repo-relative paths `git status` warned it could not descend into.

    git reports these on stderr and still exits 0 with a clean stdout, so a caller
    that reads only stdout concludes the tree is untouched. The warning is the only
    evidence that part of the tree was never looked at.
    """
    out: list[str] = []
    for line in stderr.splitlines():
        idx = line.find(_UNREADABLE_WARNING)
        if idx == -1:
            continue
        rest = line[idx + len(_UNREADABLE_WARNING):]
        end = rest.rfind("'")
        if end > 0:
            out.append(rest[:end].rstrip("/"))
    return out


#: Directories the structure sweep never descends into, by name, at any depth.
#: `.git` is git's own storage: 281 of the engine's 968 directories and 276 of
#: godot's 5,240 live under it, and its object fanout gains a directory on an
#: ordinary `git add`. Nothing the sweep exists to catch lives there — a PEP-420
#: namespace package and a Godot `res://` import target are both worktree facts —
#: so including it converted routine, DISCIPLINED git use into a breach (Gate-2 K1).
STRUCTURE_SKIP_DIRS = frozenset({".git"})


def structure_dirs(path: Path) -> set[str]:
    """Tree-relative directory PATHS — no stats, no file listing, no content.

    git tracks content, so a wholly-empty directory tree is invisible to every
    porcelain setting there is, and the stat sweep cannot rescue it because the sweep
    only descends into paths git already reported. That was declared as a bounded
    blind spot; the Gate-2 wall audit measured the cost of closing it (0.21 s for the
    engine, 1.69 s for godot) and established that "bounded to directory structure"
    does not mean inert on the two trees actually fenced:

    * a bare directory is a PEP-420 namespace package, so an empty
      `src/reincarnated/<name>/` turns an ImportError into a successful import of
      nothing — and the engine is a read-only tree;
    * a new directory under `res://` is picked up by Godot's import scan — and the
      godot tree is the other one;
    * being invisible to the fingerprint made it invisible to the rollback too, so it
      accumulated across runs.

    Returns the SET rather than a hash of it. The first version returned
    `dirs:<n>:<hash>` and the diff, having nothing else to name, reported the change
    at the TREE ROOT — which the rollback then handed to `git checkout --` as a
    pathspec, reverting an entire repository over one empty directory (Gate-2 K1). A
    measurement that can only say "something moved" must not be wired to a verb that
    acts on what it names.

    Cheap because it stats nothing: `os.walk` yields directory names from the same
    `scandir` it already performs. Walk errors are recorded as members, for the same
    reason they are everywhere else — unreadable must not read as unchanged.
    """
    found: set[str] = set()

    def onerror(exc: OSError) -> None:
        try:
            rel = str(Path(str(exc.filename)).relative_to(path))
        except ValueError:
            rel = str(exc.filename)
        found.add(f"{rel}\t<unreadable: {exc.strerror}>")

    for dirpath, dirnames, _ in os.walk(path, onerror=onerror):
        dirnames[:] = [d for d in sorted(dirnames) if d not in STRUCTURE_SKIP_DIRS]
        here = Path(dirpath)
        if here != path:
            found.add(str(here.relative_to(path)))
    return found


def fingerprint(
    root: Path, is_root_repo: bool = True, structure_roots: list[Path] | None = None
) -> TreeFingerprint:
    """Snapshot a working tree: HEAD, porcelain status (INCLUDING ignored), signatures.

    `is_root_repo` gates the factory's own runtime exemptions: they apply to the
    meta-repo only, so a sibling repo that happens to share the path shape gets
    no free pass.
    """
    root = Path(root).resolve()
    head_proc = _git(root, "rev-parse", "HEAD")
    if head_proc.returncode != 0:
        return TreeFingerprint(
            root=root, head="", is_git=False, error=head_proc.stderr.strip()[:300]
        )
    # `git status` emits WORKTREE-ROOT-relative paths. Fingerprinting a subdirectory
    # would join every one of them against the wrong base, stat nothing, and report a
    # clean tree (Gate-2 re-review G1). The loader refuses this, but the loader is not
    # the only caller -- a fingerprint that cannot be trusted must say so at the source.
    top_proc = _git(root, "rev-parse", "--show-toplevel")
    top = Path(top_proc.stdout.strip()).resolve() if top_proc.stdout.strip() else None
    if top != root:
        return TreeFingerprint(
            root=root,
            head=head_proc.stdout.strip(),
            error=(
                f"{root} is not a git worktree root (the worktree is {top}); every "
                "signature would be computed against the wrong base"
            ),
        )
    # `--ignored=traditional` collapses ignored DIRECTORIES to one line each, so the
    # listing stays small (118 entries on the engine) while the recursive stat sweep
    # below is what actually sees inside them.
    # `-z` is not a formatting preference, it is the only parseable form (Gate-2 J1).
    # Porcelain v1 C-QUOTES any path with a special character and uses ` -> ` as its
    # rename separator, so a filename may contain both. `-z` emits raw NUL-separated
    # records: no quoting, and the rename origin arrives as its own record instead of
    # being packed into a string that has to be split on a delimiter a filename can
    # legally contain.
    status = _git(root, "status", "--porcelain", "-z", "--ignored=traditional")
    if status.returncode != 0:
        return TreeFingerprint(
            root=root,
            head=head_proc.stdout.strip(),
            error=f"git status failed: {status.stderr.strip()[:300]}",
        )
    entries: dict[str, str] = {}
    exempted: list[str] = []
    # The truth about an unreadable directory arrives on STDERR, with returncode 0 and
    # nothing on stdout (containment wall, 2026-08-10 — found by the wall, not by a
    # reviewer). A phase that creates a directory and chmods it 000 is therefore
    # invisible to the change-set: git warns, exits clean, prints nothing, and the tree
    # measures as untouched. Same defect shape as the previous four, on a new axis --
    # the wrong CHANNEL. Fold the warned paths in as entries so the diff can see them:
    # unreadable at BOTH ends is unchanged (no false breach from a pre-existing
    # condition), unreadable at only one end is a change, which is the truth.
    for path in _unreadable_paths(status.stderr):
        if not _is_factory_runtime(path, is_root_repo):
            entries[path] = "!?"
    for code, path in _parse_porcelain_z(status.stdout):
        if _is_factory_runtime(path, is_root_repo):
            exempted.append(path)
            continue
        entries[path] = code

    content: dict[str, str] = {}
    coarse: list[str] = []
    for p in entries:
        sig, mode = _signature(root, p)
        content[p] = sig
        if mode == COARSE:
            coarse.append(p)
    structure: dict[str, set[str]] = {}
    for tree in structure_roots or []:
        tree = Path(tree).resolve()
        if tree == root or root in tree.parents:
            rel = "." if tree == root else str(tree.relative_to(root))
            structure[rel] = structure_dirs(tree)

    return TreeFingerprint(
        root=root,
        head=head_proc.stdout.strip(),
        entries=entries,
        content=content,
        structure=structure,
        coarse=coarse,
        exempted=exempted,
    )


class ContainmentError(RuntimeError):
    """A tree could not be measured, so nothing about it can be claimed.

    Raised rather than returning an empty diff. An empty diff means "nothing
    moved"; an unmeasurable tree means "we do not know", and in a default-fail
    architecture those must not share a return value (Gate-2 F2).
    """


def _kind_of_new_entry(code: str) -> str:
    """Classify a porcelain entry that was ABSENT from the baseline.

    Absent from the baseline means only "clean at phase start" — a tracked file that
    nobody had touched yet is not in `git status` output. The first version read
    absence as newness and typed every such path `created`, so a phase editing a
    committed source file — the single most likely agentic breach there is — got the
    `created` branch, hit the destroyer guard, and came back NOT_ROLLED_BACK with a
    reason that asserted a misidentification which had not occurred. The edit survived
    inside a read-only tree (Gate-2 K2).

    git's own status code answers the question that was actually being asked. Only
    `??` (untracked) and `!!` (ignored) mean the worktree had nothing here; `A` means
    the phase created it AND staged it, which is still a creation. Everything else is
    a path git knew about before the phase ran, so it is `modified` and the rollback's
    `git checkout --` branch restores it.
    """
    if code == RENAME_SOURCE or code.strip() == "D" or code.startswith("D"):
        # The far end of a rename, or a deletion. NOT a creation: `created` is the one
        # kind the rollback DELETES, and deleting the path a rename emptied would be
        # the rollback acting on the wrong end of the move (Gate-2 J1).
        return "deleted"
    if code in ("??", "!!", "!?") or "A" in code:
        return "created"
    return "modified"


def diff_fingerprints(before: TreeFingerprint, after: TreeFingerprint) -> list[Change]:
    """Everything that moved in the tree between the two snapshots.

    Raises ContainmentError if either snapshot is unusable.
    """
    changes: list[Change] = []
    for label, fp in (("before", before), ("after", after)):
        if not fp.usable:
            raise ContainmentError(
                f"{label} fingerprint of {fp.root} is unusable "
                f"({'not a git worktree' if not fp.is_git else fp.error}) — "
                "containment cannot be proved for this tree, so the run stops"
            )

    if before.head != after.head:
        names = _git(after.root, "diff", "--name-only", f"{before.head}..{after.head}")
        for path in names.stdout.splitlines():
            if path.strip():
                changes.append(
                    Change(after.root, path.strip(), "committed", None, None)
                )

    for path, code in after.entries.items():
        before_code = before.entries.get(path)
        if before_code is None:
            changes.append(Change(after.root, path, _kind_of_new_entry(code), None, code))
        elif before.content.get(path) != after.content.get(path) or before_code != code:
            changes.append(Change(after.root, path, "modified", before_code, code))

    for path, code in before.entries.items():
        if path not in after.entries:
            changes.append(Change(after.root, path, "modified", code, None))

    # Directory structure of the read-only trees. This is the only signal that exists
    # for a wholly-empty directory tree, which git cannot see at any porcelain setting.
    #
    # Every structure change is reported at the path of the DIRECTORY that moved, never
    # at the tree it moved inside. Reporting the tree was Gate-2 K1: the rollback took
    # the tree's path as a `git checkout --` pathspec and reverted the whole repository
    # over one empty directory, while leaving the directory standing.
    already = {c.path.rstrip("/") for c in changes}
    for rel_tree, dirs_after in after.structure.items():
        dirs_before = before.structure.get(rel_tree)
        if dirs_before is None or dirs_before == dirs_after:
            continue
        base = "" if rel_tree == "." else rel_tree.rstrip("/")
        for kind, moved in (
            ("created", dirs_after - dirs_before),
            ("deleted", dirs_before - dirs_after),
        ):
            for d in sorted(moved):
                d = d.split("\t")[0]  # an unreadable marker still names its directory
                path = f"{base}/{d}" if base else d
                # git already named this one (a directory with a file in it is a
                # collapsed porcelain entry). One breach, one row.
                if any(path == a or path.startswith(a + "/") for a in already):
                    continue
                already.add(path)
                changes.append(Change(after.root, path, kind, None, "structure"))

    seen: set[tuple[str, str]] = set()
    unique: list[Change] = []
    for c in changes:
        key = (str(c.root), c.path)
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def _matches(path: str, pattern: str) -> bool:
    path = path.rstrip("/")
    pattern = pattern.strip()
    if not pattern:
        return False
    if fnmatch(path, pattern):
        return True
    bare = pattern.rstrip("/").removesuffix("/**").removesuffix("/*")
    return path == bare or path.startswith(bare + "/")


def _read_only_hit(change_root: Path, rel: str, read_only: list[Path]) -> str | None:
    """Which read-only tree this change lands in, by PATH — or None.

    The earlier version compared only `change.root`, which is always a whole repo
    root. A read-only tree declared as a subdirectory therefore matched nothing and
    was enforced nowhere, while the loader happily accepted it (Gate-2 re-review G2).

    Matching runs both ways on purpose. A change reported at a COLLAPSED directory
    entry (git reports one line for a wholly-untracked directory) may be an ancestor
    of the read-only tree rather than a descendant of it. We cannot tell from the
    entry alone which members moved, so an overlap in either direction is a breach.
    Fail closed: the alternative is letting a collapsed ancestor smuggle writes into
    a protected subtree.

    Matching also runs on BOTH the lexical and the resolved path (Gate-2 verdict H1).
    `.resolve()` follows symlinks, so for a link planted inside a read-only tree it
    answers a question about where the link POINTS instead of where the link IS --
    and a link to /tmp resolved out of the protected tree entirely and came back
    clean. The file that appeared in the read-only tree was the link itself, so the
    link's own location is the location that matters. We keep the resolved form too,
    because a read-only tree reached THROUGH a symlinked parent is equally a hit.
    Either form matching is a breach; that is the fail-closed direction.
    """
    if rel:
        lexical = Path(os.path.normpath(change_root / rel.rstrip("/")))
    else:
        lexical = change_root
    for full in _dedupe_paths(lexical, lexical.resolve()):
        for ro in read_only:
            if full == ro or ro in full.parents:
                return str(ro)
            if full in ro.parents:
                return f"{ro} — reached via the collapsed entry {rel!r}"
    return None


def _dedupe_paths(*paths: Path) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p not in out:
            out.append(p)
    return out


def classify(
    changes: list[Change],
    writes: list[str],
    root: Path,
    read_only_trees: list[Path] | None = None,
    protected: tuple[str, ...] = PROTECTED_ALWAYS,
) -> tuple[list[Change], list[Breach]]:
    """Split measured changes into allowed writes and breaches."""
    allowed: list[Change] = []
    breaches: list[Breach] = []
    read_only = [Path(p).resolve() for p in (read_only_trees or [])]
    for change in changes:
        change_root = Path(change.root).resolve()
        hit = _read_only_hit(change_root, change.path, read_only)
        if hit is not None:
            breaches.append(Breach(change, f"write inside a read-only tree ({hit})"))
            continue
        if change_root == Path(root).resolve() and any(
            _matches(change.path, p) for p in protected
        ):
            breaches.append(
                Breach(change, "write inside an always-protected path (never config-overridable)")
            )
            continue
        if any(_matches(change.path, w) for w in writes):
            allowed.append(change)
        else:
            breaches.append(Breach(change, "path is outside the phase's writes allowlist"))
    return allowed, breaches


def _covers(ancestor: str, path: str) -> bool:
    """True when `ancestor` is `path` or contains it. Purely lexical, on normal form."""
    a, p = ancestor.rstrip("/"), path.rstrip("/")
    return a == p or (a != "" and p.startswith(a + "/"))


def _tracks_content(root: Path, rel: str) -> int:
    """How many files git knows under `rel` — asking BOTH questions, not one.

    `git ls-files` reads the INDEX, and the index can be silenced while the content
    is still committed and still on disk: `git rm --cached` and `assume-unchanged`
    both do it. A guard that asks only the index answers "no tracked content" for a
    path whose deletion destroys committed work — the exact outcome the guard exists
    to refuse (Gate-2 K3). `ls-tree HEAD` is the second question; either one alone is
    answerable `no` while work is present, both together are not.
    """
    seen: set[str] = set()
    for args in (("ls-files", "--", rel), ("ls-tree", "-r", "--name-only", "HEAD", "--", rel)):
        proc = _git(root, *args)
        if proc.returncode == 0:
            seen.update(line for line in proc.stdout.splitlines() if line.strip())
    return len(seen)


def _is_whole_tree_pathspec(rel: str, root: Path, fenced: list[Path]) -> str | None:
    """Reason this pathspec names a TREE rather than an artifact, or None.

    A rollback that cannot name a file has not identified an artifact; it has
    identified a tree, and acting on a tree is a human decision. `git checkout -- .`
    restores every tracked file in the repository from the index — it destroyed a
    fenced repo's uncommitted work over a single empty directory, and recorded the
    word `restored` (Gate-2 K1). This is the destroyer guard's principle applied to
    the other destructive verb: the refusal does not depend on knowing which
    measurement produced the coarse path.
    """
    norm = rel.strip().rstrip("/")
    if norm in ("", ".", "*", "**", "./"):
        return f"the pathspec {rel!r} names the whole of {root}"
    if norm.startswith("..") or Path(norm).is_absolute():
        return f"the pathspec {rel!r} does not resolve inside {root}"
    target = Path(os.path.normpath(root / norm))
    for tree in [root, *fenced]:
        if target == Path(tree).resolve():
            return f"the pathspec {rel!r} names the declared tree {tree} itself"
    return None


def rollback(
    breaches: list[Breach],
    before: dict[str, TreeFingerprint],
    quarantine_dir: Path,
    declared_trees: list[Path] | None = None,
) -> list[RollbackAction]:
    """Quarantine then undo the excess. Never restores over pre-existing dirt.

    `declared_trees` are the workflow's repos and read-only trees. They are the one
    thing the rollback must never act on wholesale, so it is given their names rather
    than left to infer them.
    """
    actions: list[RollbackAction] = []
    fenced = [Path(t).resolve() for t in (declared_trees or [])]
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    for breach in breaches:
        change = breach.change
        root = Path(change.root)
        target = root / change.path
        before_fp = before.get(str(root))
        # Compare on the normalised form: git reports a collapsed directory with a
        # trailing slash in some records and without in others, and an exact-string
        # membership test misses on that alone — which would drop the pre-existing-dirt
        # protection for exactly the entries most likely to be big (Gate-2 J1 WARN).
        # ...and on the ANCESTOR relation, not on equality. A change reported at `X`
        # covers everything under `X`, so restoring it destroys uncommitted work at
        # `X/a/b` that the exact-string test could not see — which is precisely the
        # shape most in need of the protection (Gate-2 K1).
        rel_norm = change.path.rstrip("/")
        was_dirty_before = bool(
            before_fp
            and any(
                _covers(rel_norm, e.rstrip("/")) or _covers(e.rstrip("/"), rel_norm)
                for e in before_fp.entries
            )
        )

        # Asked BEFORE the quarantine copy: for a change reported at a tree root the
        # copy is a multi-gigabyte walk of the very tree we have already decided not
        # to touch.
        whole_tree = _is_whole_tree_pathspec(change.path, root, fenced)
        if whole_tree:
            actions.append(
                RollbackAction(
                    change.path,
                    "NOT_ROLLED_BACK",
                    f"REFUSED: {whole_tree}. A rollback that cannot name an artifact "
                    "has identified a tree, and undoing a tree is a human decision — "
                    "the breach is detected, fenced and reported instead",
                    None,
                )
            )
            continue

        quarantined: str | None = None
        # `exists()` follows symlinks, so a BROKEN link is invisible to it -- and an
        # invisible artifact would be skipped here and then reported `deleted` below
        # while still sitting on disk (Gate-2 verdict H3). `is_symlink()` asks about
        # the link itself, which is the thing that was planted.
        if target.is_symlink():
            dest = quarantine_dir / root.name / f"{change.path}.symlink.txt"
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Never copytree through a link: the bytes on the far side are not what
            # the phase wrote, and following one into a read-only tree would copy the
            # very tree we are protecting. The evidence IS the link and its target.
            dest.write_text(
                f"{target} was a symlink -> {os.readlink(target)}\n"
                "(the link itself was the artifact; its target was not copied)\n",
                encoding="utf-8",
            )
            quarantined = str(dest)
        elif target.exists():
            dest = quarantine_dir / root.name / change.path
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                if target.is_dir():
                    size = sum(f.stat().st_size for f in target.rglob("*") if f.is_file())
                    if size <= _QUARANTINE_MAX_BYTES:
                        shutil.copytree(target, dest, dirs_exist_ok=True)
                        quarantined = str(dest)
                    else:
                        manifest = "\n".join(
                            str(f.relative_to(target)) for f in sorted(target.rglob("*"))
                        )
                        dest.with_suffix(".manifest.txt").write_text(manifest)
                        quarantined = str(dest.with_suffix(".manifest.txt"))
                elif target.stat().st_size <= _QUARANTINE_MAX_BYTES:
                    shutil.copy2(target, dest)
                    quarantined = str(dest)
                else:
                    dest.with_suffix(".toolarge.txt").write_text(
                        f"{target} was {target.stat().st_size} B -- left in place, not copied"
                    )
                    quarantined = str(dest.with_suffix(".toolarge.txt"))
            except OSError as exc:
                actions.append(
                    RollbackAction(
                        change.path,
                        "NOT_ROLLED_BACK",
                        f"could not quarantine ({exc}); left untouched as evidence",
                    )
                )
                continue

        if change.kind == "committed":
            actions.append(
                RollbackAction(
                    change.path,
                    "NOT_ROLLED_BACK",
                    "the phase committed this path; unwinding history is a human decision",
                    quarantined,
                )
            )
            continue
        if was_dirty_before:
            actions.append(
                RollbackAction(
                    change.path,
                    "NOT_ROLLED_BACK",
                    "path was already dirty at phase start; restoring would destroy "
                    "pre-existing uncommitted work",
                    quarantined,
                )
            )
            continue
        if change.kind == "created":
            # THE DESTROYER GUARD (Gate-2 J1, third face). A `created` path is by
            # definition something the phase brought into being, so it cannot contain
            # anything git already tracks. If it does, our *identification* of the path
            # is wrong — and acting on a misidentified path is how the rollback was
            # induced to delete the read-only tree it was fencing. This does not depend
            # on knowing which parse bug produced the bad path; it refuses to delete
            # tracked content whatever the reason, which is the property we actually
            # want. Containment must never be the thing that destroys work.
            n = _tracks_content(root, change.path)
            if n:
                actions.append(
                    RollbackAction(
                        change.path,
                        "NOT_ROLLED_BACK",
                        f"REFUSED: reported as created by the phase, but git tracks "
                        f"{n} file(s) under it — the path identification is wrong and "
                        "deleting it would destroy committed work",
                        quarantined,
                    )
                )
                continue
            try:
                if target.is_symlink():
                    # `is_dir()` is TRUE for a link to a directory and `rmtree` then
                    # refuses it outright; `exists()` is FALSE for a broken link and
                    # the unlink never fired. Either way the receipt said `deleted`
                    # over a surviving artifact (Gate-2 verdict H3). Unlink the link.
                    target.unlink()
                elif target.is_dir():
                    shutil.rmtree(target)
                elif target.exists():
                    target.unlink()
                elif not quarantined:
                    # Nothing on disk and nothing quarantined: we cannot claim a
                    # deletion we did not perform.
                    actions.append(
                        RollbackAction(
                            change.path,
                            "NOT_ROLLED_BACK",
                            "nothing at this path by rollback time; another process may "
                            "have removed it, so the deletion is not ours to claim",
                            quarantined,
                        )
                    )
                    continue
                actions.append(
                    RollbackAction(change.path, "deleted", "created by the phase", quarantined)
                )
            except OSError as exc:
                actions.append(
                    RollbackAction(change.path, "NOT_ROLLED_BACK", f"delete failed: {exc}", quarantined)
                )
            continue

        proc = _git(root, "checkout", "--", change.path)
        if proc.returncode == 0:
            actions.append(
                RollbackAction(change.path, "restored", "git checkout -- <path>", quarantined)
            )
        else:
            actions.append(
                RollbackAction(
                    change.path,
                    "NOT_ROLLED_BACK",
                    f"git checkout failed: {proc.stderr.strip()[:200]}",
                    quarantined,
                )
            )
    return actions
