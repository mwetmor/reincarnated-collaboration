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


def fingerprint(root: Path, is_root_repo: bool = True) -> TreeFingerprint:
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
    status = _git(root, "status", "--porcelain", "--ignored=traditional")
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
    for line in status.stdout.splitlines():
        if not line.strip():
            continue
        code, rest = line[:2], line[3:]
        path = rest.split(" -> ")[-1].strip().strip('"')
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
    return TreeFingerprint(
        root=root,
        head=head_proc.stdout.strip(),
        entries=entries,
        content=content,
        coarse=coarse,
        exempted=exempted,
    )


class ContainmentError(RuntimeError):
    """A tree could not be measured, so nothing about it can be claimed.

    Raised rather than returning an empty diff. An empty diff means "nothing
    moved"; an unmeasurable tree means "we do not know", and in a default-fail
    architecture those must not share a return value (Gate-2 F2).
    """


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
            kind = "deleted" if code.strip() == "D" else "created"
            changes.append(Change(after.root, path, kind, None, code))
        elif before.content.get(path) != after.content.get(path) or before_code != code:
            changes.append(Change(after.root, path, "modified", before_code, code))

    for path, code in before.entries.items():
        if path not in after.entries:
            changes.append(Change(after.root, path, "modified", code, None))

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


def rollback(
    breaches: list[Breach], before: dict[str, TreeFingerprint], quarantine_dir: Path
) -> list[RollbackAction]:
    """Quarantine then undo the excess. Never restores over pre-existing dirt."""
    actions: list[RollbackAction] = []
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    for breach in breaches:
        change = breach.change
        root = Path(change.root)
        target = root / change.path
        before_fp = before.get(str(root))
        was_dirty_before = bool(before_fp and change.path in before_fp.entries)

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
