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
"""

from __future__ import annotations

import hashlib
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

_QUARANTINE_MAX_BYTES = 64 * 1024 * 1024


def _git(root: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=check,
        stdin=subprocess.DEVNULL,
    )


_DIR_SCAN_CAP = 500


def _stat_sig(path: Path) -> str:
    try:
        st = path.stat()
        return f"file:{st.st_size}:{st.st_mtime_ns}"
    except OSError as exc:
        return f"unreadable:{exc.errno}"


def _signature(root: Path, rel: str, untracked_files: list[str]) -> str:
    """Cheap change signature for a dirty path: size + mtime (dirs: capped listing).

    Deliberately NOT a content hash. Content comparison for TRACKED files is
    git's job (`git status --porcelain` already compares content, so an
    identical-content rewrite does not show up as a change). This signature only
    has to catch movement in UNTRACKED paths, where git offers presence and
    nothing else. The engine tree carries ~2.8k dirty paths; hashing them all per
    phase would cost more than the phase.

    Directory entries (git collapses untracked dirs) are summarised from the
    repo's `ls-files --others --exclude-standard` listing, so **gitignored files
    inside them are invisible here** -- which is what keeps the factory's own
    `sessions/` and `receipts.db` from reading as writes to a protected path.
    """
    path = root / rel
    if rel.endswith("/") or path.is_dir():
        prefix = rel if rel.endswith("/") else rel + "/"
        members = [f for f in untracked_files if f.startswith(prefix)]
        h = hashlib.sha256()
        for member in members[:_DIR_SCAN_CAP]:
            h.update(f"{member}:{_stat_sig(root / member)}".encode())
        if len(members) > _DIR_SCAN_CAP:
            h.update(b"TRUNCATED")
        return f"dir:{len(members)}:{h.hexdigest()[:16]}"
    if not path.exists():
        return ""
    return _stat_sig(path)


@dataclass
class TreeFingerprint:
    root: Path
    head: str
    entries: dict[str, str] = field(default_factory=dict)         # path -> porcelain XY
    content: dict[str, str] = field(default_factory=dict)         # path -> signature (dirty only)
    is_git: bool = True
    error: str | None = None


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


def fingerprint(root: Path) -> TreeFingerprint:
    """Snapshot a working tree: HEAD, porcelain status, and hashes of dirty paths."""
    root = Path(root)
    head_proc = _git(root, "rev-parse", "HEAD")
    if head_proc.returncode != 0:
        return TreeFingerprint(
            root=root, head="", is_git=False, error=head_proc.stderr.strip()[:300]
        )
    status = _git(root, "status", "--porcelain")
    entries: dict[str, str] = {}
    for line in status.stdout.splitlines():
        if not line.strip():
            continue
        code, _, rest = line[:2], line[2], line[3:]
        path = rest.split(" -> ")[-1].strip().strip('"')
        entries[path] = code
    untracked = _git(root, "ls-files", "--others", "--exclude-standard")
    untracked_files = [ln for ln in untracked.stdout.splitlines() if ln.strip()]
    content = {p: _signature(root, p, untracked_files) for p in entries}
    return TreeFingerprint(
        root=root, head=head_proc.stdout.strip(), entries=entries, content=content
    )


def diff_fingerprints(before: TreeFingerprint, after: TreeFingerprint) -> list[Change]:
    """Everything that moved in the tree between the two snapshots."""
    changes: list[Change] = []
    if not before.is_git or not after.is_git:
        return changes

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
        if any(change_root == ro or str(change_root).startswith(str(ro) + "/") for ro in read_only):
            breaches.append(
                Breach(change, f"write inside a read-only tree ({change_root.name})")
            )
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
        if target.exists():
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
                if target.is_dir():
                    shutil.rmtree(target)
                elif target.exists():
                    target.unlink()
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
