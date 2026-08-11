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

PROTECTED_EVERY_REPO: tuple[str, ...] = (
    ".claude/",
    ".git/",
)
"""Protected in EVERY declared repo, not only the root one (Gate-2 C4, F3).

`.claude/settings.json` executes hooks. A phase that can write it in
`reincarnated-demo` or `reincarnated-loadout` can arrange for code to run in the
next session there — so scoping the check to the meta-repo made the receipt's
"never config-overridable" true only where it was already hardest to reach.

`.git/` is the same surface with a shorter fuse (Gate-2 F3). C4 closed the
next-CLAUDE-session hijack; `.git/hooks/pre-commit` arranges for code to run on the
next git operation any HUMAN performs in that repo, and `.git/config` reaches the
same place by moving `core.hooksPath`. Nothing under `.git/` is ever a legitimate
phase write, and — the reason this is not merely belt-and-braces — `git status`
NEVER reports these paths, at any porcelain setting. Before F3 the fingerprint could
not see the write at all, so containment measured a clean tree and said so. See
`_git_control_entries`.

The other `PROTECTED_ALWAYS` entries name paths that exist only in the meta-repo,
so widening them would protect nothing and would collide with rocket's engine-side
`canonical/`, which is a legitimately declarable write target for its own seam.
"""

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


def coarse_key(repo: "Path | str", region: str) -> str:
    """The ONE spelling of a coarse-region acknowledgement. Loader and runner both
    call it, so they cannot disagree about what a workflow acknowledged.

    Keyed on the RESOLVED path, not the basename (Gate-2 F6). `repo.name` collides:
    two declared repos at `~/a/engine` and `~/b/engine` share the key `engine:X`, so
    one acknowledgement silently waived a region in a tree nobody looked at — a
    predicate answering a slightly different question, whose wrong answer is the
    quiet one. Absolute and host-specific is the honest form anyway: a coarse
    acknowledgement is a waiver about how well THIS machine can measure THIS tree.
    """
    return f"{Path(repo).resolve()}:{region}"


#: Every pathspec this module hands to git is built from a filesystem PATH — a name
#: read off the fingerprint, never a pattern a human wrote. A path is not a pathspec.
#: Pathspecs are a language: a leading `:` is magic, so `:(top)` and `:/` mean THE
#: WHOLE REPOSITORY, and `*`, `?`, `[` glob. A file legally named `:(top)` at a tree
#: root therefore turned `git checkout -- <that file>` into a repo-wide revert, and
#: turned `ls-files -- <that dir>` into "git knows nothing here" — rc=0, empty output,
#: silently wrong, and zero is the answer that authorises rmtree (Gate-2 L1).
#:
#: This makes git read what we mean. No call site in this module wants globbing or
#: magic — every one of them names one concrete path — so turning the language off is
#: not a restriction, it is the removal of an interpretation nobody asked for.
_GIT_ENV = {**os.environ, "GIT_LITERAL_PATHSPECS": "1"}


def _git(root: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=check,
        stdin=subprocess.DEVNULL,
        env=_GIT_ENV,
    )


def _stat_sig(path: Path) -> str:
    try:
        st = path.stat()
        return f"file:{st.st_size}:{st.st_mtime_ns}"
    except OSError as exc:
        return f"unreadable:{exc.errno}"


#: Gate-2 H7. Bytes read per control surface before falling back to stat. A hook is a
#: script and a config is an ini file; anything past this is not one of those, and the
#: cap is what keeps "hash it" from becoming an unbounded read of an attacker-chosen
#: file. Exceeding it is RECORDED in the signature, never silently truncated.
_CONTROL_HASH_MAX_BYTES = 1 << 20      # 1 MiB


def _content_sig(path: Path) -> str:
    """Content hash, for the handful of paths where stat is not good enough.

    Gate-2 H7. `_stat_sig` is size + mtime. Both are SETTABLE by the phase being
    measured: an equal-length rewrite of `.git/hooks/pre-commit` followed by
    `touch -t` restores the pair exactly, and the fingerprint reads unchanged. That was
    an acceptable deferral while the threat was theoretical. J1 fired the trigger —
    `--allowedTools` does not restrict in headless `default` mode, so a phase declaring
    `Bash(git status:*)` has unrestricted `Bash`, and `touch` is in it.

    Applied ONLY to the F3/H4 control surfaces, which is the whole reason it is
    affordable. The general fingerprint's cost argument — the engine tree carries ~2.8k
    dirty paths, hashing them per phase would cost more than the phase — is imported
    from a different population and does not cover three small files that change only
    when somebody decides to change them.

    A directory is NOT hashed here: the only directory-valued control keys are the
    synthetic nested-gitdir markers, which name nothing on disk by design (K1).
    """
    try:
        if path.is_dir():
            return _stat_sig(path)
        st = path.stat()
        if st.st_size > _CONTROL_HASH_MAX_BYTES:
            # Say so rather than hash a prefix: a prefix hash reads exactly like a
            # whole-file hash and would be defeated by appending. Falling back to stat
            # is weaker, so the signature carries the word.
            return f"oversize:{st.st_size}:{_stat_sig(path)}"
        h = hashlib.sha256()
        with path.open("rb") as fh:
            h.update(fh.read(_CONTROL_HASH_MAX_BYTES))
        # Mode is part of the surface: a hook that becomes executable has changed what
        # git does with it without changing one byte of its content.
        return f"content:{st.st_size}:{st.st_mode & 0o7777:o}:{h.hexdigest()[:32]}"
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
    # Gate-2 J4/H7. This function no longer sees the git control surfaces at all —
    # `fingerprint` routes them to `_content_sig` with the REAL path, because for a
    # worktree or submodule the key (`.git/…`, so it classifies as protected) and the
    # file (outside the worktree entirely) are different paths. J4 first solved that
    # with a `real_path` parameter here; H7 then made those entries content-hashed
    # rather than stat-signed, which left the parameter unreachable. It is removed
    # rather than kept "in case": an argument no call site passes is a branch no test
    # can reach, which is the ROUTE axis this review series keeps finding.
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
    kind: str            # created | modified | deleted | committed | unknown
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
    #: The MEASUREMENTS a refusal rests on, carried as numbers rather than living
    #: only inside the sentence. Gate-2 B1: the wall checked the PROSE, and prose is
    #: a label — replacing the whole clause with "HEAD holds nothing here; the index
    #: is empty here" left all 410 tests green while the receipt told the operator a
    #: double falsehood about a file git held in both HEAD and the index. Numbers
    #: travel; the sentence is RENDERED from them, so there is exactly one place the
    #: figures come from and no wording can disagree with the tree.
    facts: tuple[tuple[str, int], ...] = ()
    #: WHICH refusal fired, as a closed vocabulary. Gate-2 C1: round eight made the
    #: measurements travel and then triggered the wall's check on
    #: `if expected["staged_paths"]:` — one of the three values the check certifies.
    #: A refusal where nothing was staged (the destroyer guard's ordinary case, and
    #: the branch where git REFUSED the question) therefore certified nothing, and a
    #: receipt reading "HEAD holds 6 file(s) ... Measured here: head_files=0" passed
    #: 412 tests. A trigger that can be switched off by anything it is measuring is a
    #: comment. Identity is not a measurement, so it is the one thing safe to key on.
    guard: str | None = None


#: Closed, because a default that catches every case nobody enumerated is how this
#: class recurs (rule 13, applied to the refusal vocabulary rather than to git's
#: status codes). Every NOT_ROLLED_BACK names one of these or the wall reds.
REFUSAL_GUARDS = frozenset({
    "whole_tree", "quarantine_failed", "committed", "dirty_before", "destroyer",
    "delete_failed", "nothing_at_path", "unknown_status", "staging", "checkout_failed",
    "git_internal",
})

#: The two that make COUNTED claims about what git holds. These owe the operator
#: numbers unconditionally — not when something happens to be staged.
GUARDS_OWING_FACTS = frozenset({"destroyer", "staging"})


def render_containment_facts(facts: tuple[tuple[str, int], ...]) -> str:
    """The ONE place a refusal's measured clause is worded.

    Product and wall both call this. The wall passes numbers it derived from git
    itself and asserts the result appears in the reason, so the assertion is anchored
    to the tree and to a single wording — not to a literal phrase copied into the
    test. Gate-2 B2 found two such copies had gone dead: the wall was gated on
    "HEAD still holds", a string round seven deleted from the product in the very
    commit that narrowed the regex to require it, and on three "index no longer"
    variants that no longer existed either. Both assertions read as coverage and
    could not fire.
    """
    return "; ".join(f"{name}={value}" for name, value in facts)


def _is_factory_runtime(rel: str, is_root_repo: bool) -> bool:
    """The six named exemptions — root repo only, prefix match, nothing wider."""
    if not is_root_repo:
        return False
    return any(rel.startswith(p) or rel == p.rstrip("/") for p in FACTORY_RUNTIME_PATHS)


#: Synthetic code for the SOURCE half of a rename. git names both endpoints; the
#: source has left the worktree, so it resolves to a `deleted` change.
RENAME_SOURCE = "R<"

#: The porcelain v1 conflict codes. A path in one of these states exists in SEVERAL
#: index stages at once, so none of this module's three verbs (delete, checkout,
#: refuse-with-a-reason) can act on it without arbitrarily picking a stage. They
#: classify to `unknown`, which the rollback refuses by name (Gate-2 L2).
UNMERGED_CODES = frozenset({"DD", "AU", "UD", "UA", "DU", "AA", "UU"})


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

#: The separator between a fingerprint key's PATH and the synthetic marker that says
#: why the ordinary reading of that path failed — `\t<unreadable: …>`,
#: `\t<gitdir pointer unparseable…>`, `\t<commondir unreadable…>`, and the rest.
MARKER_SEP = "\t"


def marker_path(key: str) -> str:
    """The real path a fingerprint key names, with any synthetic marker removed.

    Gate-2 JR-5. The markers exist so that "we could not read this" never renders as
    "this did not change" — the absent-is-absent law, applied to the filesystem. But
    they are glued onto the key, and every downstream predicate that reasons about the
    key's PATH was reading the glue as part of the path.

    The cost was exact and asymmetric. `_gitdir_control_entries(common, ".git/\\t<common>")`
    puts the tab AFTER the slash, so those keys begin `.git/` and `PROTECTED_EVERY_REPO`
    catches them. The five keys minted directly by `_resolve_gitdir_pointer` and
    `_resolve_commondir` put the tab BEFORE it — `.git\\t<gitdir pointer unreadable: …>` —
    and `.git` alone is neither `.git/`-prefixed nor equal to the bare `.git`, so they
    were protected by nothing and refused by the rollback's `git_internal` guard for
    nothing. The paths that mint them are precisely the paths where git's own control
    plane has been made unreadable, which is the last place a blind spot belongs.

    Comparable normalisation already existed at ONE site (`diff_fingerprints`, which
    splits so an unreadable marker still names its directory). Living in one place and
    being needed in four is the WIRING axis; this is that split, named and shared.

    Splitting on the FIRST separator only. A marker's own text can contain anything —
    `exc.strerror`, a path, a filename — and taking the last field would let the
    message decide what the path is.
    """
    return key.split(MARKER_SEP, 1)[0]


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


#: Synthetic status code for a path under `.git/`. Not a porcelain code — git has
#: none for these, which is the whole finding. Maps to `git_internal` in `_ENTRY_KIND`,
#: which the rollback refuses by name rather than acting on.
GIT_CONTROL = "G!"

#: The control surfaces under `.git/`, as a CLOSED list (rule 13 again). Each either
#: executes code or decides what git reports:
#:
#:   hooks/         every hook git runs — `pre-commit`, `post-checkout`, `pre-push`…
#:                  Enumerated as its direct children so a planted hook is NAMED, not
#:                  summarised. git only ever executes direct children, so a flat
#:                  listing is the exact set, not a sample of it.
#:   config         reaches hooks/ from the side via `core.hooksPath`, and reaches the
#:                  network via `url.*.insteadOf` and `remote.*.url`.
#:   info/exclude   an untracked ignore list — a phase that appends to it makes its own
#:                  later writes invisible to every OTHER measurement in this module.
#:
#: NOT the object store, refs, or the index: those move on ordinary disciplined git
#: use, which is exactly the mistake K1 made with STRUCTURE_SKIP_DIRS. This list is
#: the paths that change ONLY when somebody decides to change them.
#:   config.worktree  the per-worktree config, live whenever `extensions.worktreeConfig`
#:                  is set. It reaches `core.hooksPath` exactly like `config` does, and
#:                  it is the file `git config --worktree` writes.
GIT_CONTROL_PATHS: tuple[str, ...] = ("hooks/", "config", "config.worktree", "info/exclude")

#: Gate-2 H4. The two directories under a gitdir that contain FURTHER GITDIRS.
#:
#: `.git/modules/<sub>` is a submodule's complete gitdir — its own `hooks/`, its own
#: `config`. `.git/worktrees/<wt>` is a linked worktree's gitdir, which carries
#: `config.worktree`. Both were entirely outside F3's closed list, so the one write
#: F3 exists to catch — planting `pre-commit` — was still invisible if it landed one
#: directory deeper. F3 named the surface and then measured a single instance of it;
#: a repo has as many gitdirs as it has submodules and worktrees, and every one of
#: them runs hooks on the next git operation a human performs.
#:
#: Measured on BOTH axes, because either alone leaves a live path:
#:   - the ENTRY NAMES of these directories, so a gitdir that did not exist before
#:     appearing is itself the change (the `git worktree add` / `submodule add` route,
#:     which H5 notes the `EnterWorktree` builtin reaches without invoking git at all);
#:   - the closed control list INSIDE each one, because planting a hook in a gitdir
#:     that already exists moves no entry name.
#:
#: Ordinary disciplined git use does not move either — `add`, `commit`, `gc` never
#: write here — which is the K1 test this list has to pass and `refs/`, `index` and
#: the object store do not.
GIT_NESTED_GITDIRS: tuple[str, ...] = ("worktrees/", "modules/")

#: Submodules nest, so gitdirs nest. Bounded rather than unbounded because this walk
#: runs on every fingerprint, and because a cycle here (a symlink pointing upward)
#: would otherwise not terminate. Exceeding it is RECORDED, not skipped silently:
#: "we stopped looking" must never be stored as "there was nothing there".
_MAX_GITDIR_DEPTH = 4


def _gitdir_control_entries(
    dot: Path,
    prefix: str,
    depth: int,
    out: dict[str, str],
    real: dict[str, Path] | None = None,
) -> None:
    """The closed control list for ONE gitdir, then recurse into the gitdirs it holds.

    `dot` is the DIRECTORY ON DISK; `prefix` is the KEY the entry is filed under. They
    are already separate because nested gitdirs key relative to the outer repo. Gate-2
    J4 makes the separation load-bearing: for a worktree or submodule the real gitdir
    lives outside the worktree entirely, so the key must stay under `.git/` (that is
    what `PROTECTED_EVERY_REPO` matches) while the stat must follow the real path.

    `real` collects key -> the actual filesystem path the entry was read from, so
    `_signature` can sign the file that exists rather than the one the key names. When
    the two coincide — the ordinary in-repo case — the map is redundant and harmless.
    """
    if depth > _MAX_GITDIR_DEPTH:
        out[f"{prefix}\t<nested deeper than {_MAX_GITDIR_DEPTH} gitdirs: not measured>"] = (
            GIT_CONTROL
        )
        return
    for rel in GIT_CONTROL_PATHS:
        target = dot / rel.rstrip("/")
        if rel.endswith("/"):
            if not target.is_dir():
                continue
            try:
                # Sorted so the entry set is deterministic; direct children only,
                # because that is the exact set git executes.
                for child in sorted(target.iterdir()):
                    key = f"{prefix}/{rel}{child.name}"
                    out[key] = GIT_CONTROL
                    if real is not None:
                        real[key] = child
            except OSError as exc:
                # Unreadable must never read as unchanged — same rule as everywhere
                # else in this module.
                out[f"{prefix}/{rel}\t<unreadable: {exc.strerror}>"] = GIT_CONTROL
        elif target.exists():
            out[f"{prefix}/{rel}"] = GIT_CONTROL
            if real is not None:
                real[f"{prefix}/{rel}"] = target

    for nested in GIT_NESTED_GITDIRS:
        container = dot / nested.rstrip("/")
        if not container.is_dir():
            continue
        try:
            children = sorted(container.iterdir())
        except OSError as exc:
            out[f"{prefix}/{nested}\t<unreadable: {exc.strerror}>"] = GIT_CONTROL
            continue
        for child in children:
            # The name itself is an entry: a gitdir appearing is the change, before
            # anything inside it has been written.
            #
            # SYNTHETIC key, not the real path, and the tab is what makes it one.
            # `_signature` stat-sweeps any key that resolves to a directory, and a
            # gitdir's contents are `index`, `HEAD`, `ORIG_HEAD`, `refs/`, `logs/`
            # and the object store — every one of which moves on an ordinary
            # `commit`. Keying on the real path would therefore report a breach
            # every time a submodule was used correctly, which is precisely the K1
            # mistake this module has already made once. A synthetic key resolves
            # to nothing, signs as "", and carries its signal by EXISTING.
            out[f"{prefix}/{nested}\t<gitdir: {child.name}>"] = GIT_CONTROL
            if child.is_dir():
                _gitdir_control_entries(
                    child, f"{prefix}/{nested}{child.name}", depth + 1, out, real
                )


def _resolve_gitdir_pointer(
    root: Path, dot: Path, out: dict[str, str], real: dict[str, Path] | None
) -> Path | None:
    """Read `gitdir: <path>` out of a `.git` FILE. Unreadable is RECORDED, never skipped.

    Gate-2 J4. Every failure to resolve files an entry saying so, because the whole
    point of this pass is that "we could not look" must not be stored as "there was
    nothing there" — the same rule `_MAX_GITDIR_DEPTH` follows one function up.
    """
    try:
        text = dot.read_text(encoding="utf-8", errors="replace").strip()
    except OSError as exc:
        out[".git\t<gitdir pointer unreadable: %s>" % exc.strerror] = GIT_CONTROL
        return None
    if not text.startswith("gitdir:"):
        out[".git\t<gitdir pointer unparseable: no 'gitdir:' prefix>"] = GIT_CONTROL
        return None
    target = Path(text[len("gitdir:"):].strip())
    if not target.is_absolute():
        target = (root / target).resolve()
    if not target.is_dir():
        out[f".git\t<gitdir points at a non-directory: {target}>"] = GIT_CONTROL
        return None
    return target


def _resolve_commondir(
    gitdir: Path, out: dict[str, str], real: dict[str, Path] | None
) -> Path | None:
    """The shared gitdir a linked worktree runs its hooks out of. Absent = it IS the one."""
    marker = gitdir / "commondir"
    if not marker.is_file():
        return gitdir
    try:
        text = marker.read_text(encoding="utf-8", errors="replace").strip()
    except OSError as exc:
        out[f".git\t<commondir unreadable: {exc.strerror}>"] = GIT_CONTROL
        return None
    common = Path(text)
    if not common.is_absolute():
        common = (gitdir / common).resolve()
    if not common.is_dir():
        out[f".git\t<commondir points at a non-directory: {common}>"] = GIT_CONTROL
        return None
    return common


def _git_control_entries(root: Path, real: dict[str, Path] | None = None) -> dict[str, str]:
    """Measure `.git/`'s control surfaces, because `git status` never will.

    Gate-2 F3. Every other path in this module arrives from `git status`; these cannot,
    at any porcelain setting, because git does not consider its own directory part of
    the worktree. So the one write that most directly defeats containment — planting
    `.git/hooks/pre-commit` — was invisible to the fingerprint, produced an empty
    change-set, and the run reported a clean tree. That is the B1 class at its worst:
    the claim ("no writes outside the allowlist") was measured against a channel that
    structurally could not carry the counterexample.

    Returned as ordinary entries keyed on repo-relative paths (`.git/config`), so they
    flow through `diff_fingerprints` and `classify` with everything else and need no
    parallel comparison path. `.git/` is in PROTECTED_EVERY_REPO, so any of them
    changing is a breach in every declared repo regardless of `writes`.

    A worktree/submodule `.git` is a FILE pointing elsewhere.

    Gate-2 J4. The first version stopped there, filed the pointer file as the single
    entry, and justified it: "its content is what would have to change to redirect
    anything." That reasoning answers a question nobody asked. REDIRECTING the gitdir
    is one route to a hook; PLANTING one in the gitdir the pointer already names is the
    other, and it moves no byte of the pointer file. So in every worktree and every
    submodule — the two places this repo's own workflows create on purpose — the exact
    write F3 exists to catch was reported as a clean tree. The recurring shape: a
    containment predicate that answers a slightly different question than the one
    asked, whose wrong answer is the safe-looking one.

    Both routes are now measured. The pointer file stays an entry (redirection), and
    the gitdir it names is enumerated (planting), keyed under `.git/` so it classifies
    as the protected surface it is while `real` carries where to actually stat.

    `commondir` matters and is not optional. A linked worktree's gitdir does NOT hold
    the hooks git runs in it — `hooks/`, `config` and `info/exclude` resolve through the
    COMMON dir, the main repo's `.git`. Enumerating only the per-worktree gitdir would
    have measured `config.worktree` and missed `pre-commit`, which is to say it would
    have missed the one file the whole mechanism is named after.
    """
    dot = root / ".git"
    out: dict[str, str] = {}
    if not dot.exists():
        return out
    if not dot.is_dir():
        # The pointer itself: content signature, because redirection is a real route.
        out[".git"] = GIT_CONTROL
        if real is not None:
            real[".git"] = dot
        gitdir = _resolve_gitdir_pointer(root, dot, out, real)
        if gitdir is None:
            return out
        _gitdir_control_entries(gitdir, ".git", 1, out, real)
        common = _resolve_commondir(gitdir, out, real)
        if common is not None and common != gitdir:
            # The tab goes AFTER the slash, and that is load-bearing rather than
            # cosmetic. `PROTECTED_EVERY_REPO` matches by literal `.git/` prefix
            # (`_matches` -> `path.startswith(bare + "/")`), so the first version of
            # this key — `.git\t<common>` — was NOT protected in any repo. The
            # docstring claimed it classified "as the protected surface it is" while
            # the only rows checking it compared fingerprint CONTENT, which moves
            # whether or not the key is protected. A claim no assertion reaches, one
            # layer beneath a fix for a claim no assertion reached.
            _gitdir_control_entries(common, ".git/\t<common>", 1, out, real)
        return out
    _gitdir_control_entries(dot, ".git", 1, out, real)
    return out


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
    # Gate-2 F3. The only entries in this function that do NOT come from git, because
    # for these git has no answer to give. Folded in here rather than compared
    # separately so they inherit the diff, the classifier and the receipt unchanged.
    git_real: dict[str, Path] = {}
    git_entries = _git_control_entries(root, git_real)
    entries.update(git_entries)

    content: dict[str, str] = {}
    coarse: list[str] = []
    for p in entries:
        if p in git_entries:
            # Gate-2 H7. The control surfaces get a CONTENT hash, not size+mtime.
            # Both halves of the stat signature are settable by the phase being
            # measured (`touch -t` after an equal-length rewrite), and J1 established
            # that a phase declaring `Bash(git status:*)` in fact holds unrestricted
            # `Bash`. Affordable only because this set is tiny and closed — which is
            # also why the general fingerprint's cost objection does not reach it.
            content[p] = _content_sig(git_real[p]) if p in git_real else ""
            continue
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

    git's own status code answers the question that was actually being asked. But the
    first version of THIS fix enumerated part of the code space and defaulted the rest
    to `modified` — so a rename DESTINATION (`R `, no `A` in it) was typed `modified`,
    the rollback ran `git checkout --` on it, and git restored it FROM THE INDEX THE
    PHASE HAD JUST STAGED. The file was left exactly as the phase wrote it and the
    receipt said `restored`. Pre-fix the same artifact came back with an honest
    refusal, so the fix converted a refusal into a false restore (Gate-2 L2).

    The code space is therefore enumerated CLOSED, and an unrecognised code returns
    `unknown` — which the rollback refuses. A default that catches every code nobody
    listed is how this class recurs; the whole architecture is default-fail, and that
    has to include the classifier, not just the callers.

    And the SECOND version of the fix — the closed enumeration — was written as
    character-class tests (`x in "ARC"`, `x == "D" or y == "D"`) under a docstring
    claiming closure. Those are prefix tests, not an enumeration: they hand a
    confident answer to 29 codes nobody listed, and they order `A` ahead of `D` so
    `AD` — staged, then removed from disk — came back `created`. A table that only
    LOOKS closed is the same defect with better documentation, so the enumeration
    is now a literal mapping and closure is a property of the data structure.

    `unknown` is not a failure state. It is the answer that routes a path to a
    refusal naming it, which is what containment owes a case it cannot reason about.
    """
    return _ENTRY_KIND.get(code, "unknown")


#: The CLOSED table. Keys are the porcelain-v1 XY codes reachable for a path that
#: was ABSENT from the baseline (i.e. clean at phase start), plus this module's
#: synthetic rename-source marker. Anything not a key here is `unknown`.
#:
#: Written as data because the three previous versions were written as control
#: flow, and each time the control flow admitted codes its author had not thought
#: about. A dict cannot silently widen.
_ENTRY_KIND: dict[str, str] = {
    # A control surface under `.git/` (Gate-2 F3). Its own kind, because none of the
    # three verbs is right for it: `git checkout --` cannot restore a path git has
    # never tracked, and `created` would send `.git/config` to the destroyer guard,
    # which — finding nothing tracked underneath, correctly, since git tracks nothing
    # in there — would authorise deleting it. Containment must not be the thing that
    # breaks the repository.
    GIT_CONTROL: "git_internal",
    # nothing was here before the phase ran
    "??": "created",
    "!!": "created",
    "!?": "created",
    # ...nor here: staged creations, and the DESTINATION of a staged rename/copy.
    # `created` sends these to the destroyer guard, which refuses them because the
    # phase's own index holds them — the honest answer, and the one L2 restored.
    "A ": "created",
    "AM": "created",
    "AT": "created",
    "R ": "created",
    "RM": "created",
    "RT": "created",
    "C ": "created",
    "CM": "created",
    "CT": "created",
    # git knew this path before the phase ran, and it is still on disk
    " M": "modified",
    " T": "modified",
    "M ": "modified",
    "MM": "modified",
    "MT": "modified",
    "T ": "modified",
    "TM": "modified",
    "TT": "modified",
    # the path has left the worktree
    " D": "deleted",
    "D ": "deleted",
    "MD": "deleted",
    "TD": "deleted",
    RENAME_SOURCE: "deleted",   # the far end of a rename (Gate-2 J1)
    #
    # DELIBERATELY ABSENT, so they resolve to `unknown` and are refused by name:
    #   AD RD CD — the phase staged a creation and then removed it from disk. There
    #     is nothing on disk to undo and the index is dirty; no verb this module
    #     owns is right, and picking one would be a guess.
    #   DD AU UD UA DU AA UU — unmerged; the path is in several index stages at
    #     once and every verb would arbitrarily pick one.
}


@dataclass(frozen=True)
class StagedAgainstHead:
    """Paths under a pathspec where the INDEX differs from HEAD, or why unknown."""

    paths: tuple[str, ...]
    unanswered: tuple[str, ...]

    def __bool__(self) -> bool:
        """True when `git checkout --` might write the phase's own bytes back.

        Not-knowing counts as true. `checkout` ACTS; an unanswered question is not
        a `no`, and the safe-looking answer here is the one that lets it run.
        """
        return bool(self.paths or self.unanswered)


def _staged_against_head(root: Path, rel: str) -> StagedAgainstHead:
    """Does git's index hold something other than HEAD under this path?

    This is the predicate that makes `git checkout -- <path>` safe to use at all.
    That command restores from the INDEX — so if the phase staged its own work, the
    index IS the phase's work, and `checkout` rewrites the file with exactly the
    content containment is supposed to be removing, then reports `restored`.

    Gate-2 L2 found this on a rename destination and was closed by re-typing `R `.
    That closed one cell of a column. Gate-2 L2-general found the column is every
    code whose X is non-space — `M `, a staged modification, being the most ordinary
    thing a disciplined agent does — and closed it by reading the porcelain code.

    Gate-2 L8 found that reading the CODE is still the wrong question, because not
    every change carries one git wrote. `diff_fingerprints` emits structure-sweep
    rows with `after_status="structure"`, a label THIS MODULE invents; the code-based
    predicate measured `len("structure") == 2`, answered "not staged", and handed a
    DIRECTORY pathspec to `git checkout --`. Reproduced: `git add` a fenced file,
    `rm -rf` its directory, and the phase's own bytes come back under a `restored`
    receipt — on the row beside an honest refusal for the same file.

    So the question is asked of GIT, about the TREE, and never of a label:

        git diff --cached --name-only HEAD -- <rel>

    which is a property of the repository rather than of a string, and is therefore
    immune to `after_status` being synthetic, `None`, or something added later. It
    is also why the rename pair needs no hand-placed exemption any more — `git mv`
    stages both ends, so git itself reports both.

    Fourth round running in which the more disciplined git command is handled worst,
    and the reason is structural: staging moves work into the place containment reads
    as its baseline. So containment does not restore staged work — it refuses and
    names the index, exactly as the destroyer guard already does for staged
    creations. Editing the index of a fenced tree is a human decision.
    """
    if _git(root, "rev-parse", "--quiet", "--verify", "HEAD").returncode != 0:
        # Unborn HEAD is a real answer, not a refusal: HEAD holds nothing, so
        # everything the index holds here differs from it.
        proc = _git(root, "ls-files", "--", rel)
        unborn = () if proc.returncode == 0 else (
            f"git ls-files failed: {proc.stderr.strip()[:120]}",
        )
        return StagedAgainstHead(
            tuple(l for l in proc.stdout.splitlines() if l.strip()), unborn
        )

    proc = _git(root, "diff", "--cached", "--name-only", "HEAD", "--", rel)
    if proc.returncode != 0:
        return StagedAgainstHead(
            (), (f"git diff --cached failed: {proc.stderr.strip()[:120]}",)
        )
    return StagedAgainstHead(
        tuple(l for l in proc.stdout.splitlines() if l.strip()), ()
    )


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
                d = marker_path(d)  # an unreadable marker still names its directory
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
    # The marker comes off FIRST (JR-5). Every caller below is asking a question about
    # the path, and `fnmatch` would happily let a trailing `\t<…>` decide the answer —
    # in the permissive direction for the protected lists, which is the direction that
    # does not announce itself.
    path = marker_path(path).rstrip("/")
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
    rel = marker_path(rel)  # JR-5: `<unreadable: …>` is not a path component
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
        # Gate-2 C4. This check was gated on the ROOT repo while its receipt said
        # "never config-overridable" — true in the meta-repo, false in every other
        # declared repo, where a permissive `writes` reaches it. The claim was
        # broader than the measurement, which is the B1 class at the classifier.
        # `.claude/` is a HOOK-EXECUTION surface: a phase in reincarnated-demo or
        # reincarnated-loadout could plant a hook that fires on the next session
        # there. It is protected in every declared repo. The other two entries name
        # paths that exist only in the meta-repo, so they stay root-scoped and the
        # receipt now says which rule it is.
        if any(_matches(change.path, p) for p in PROTECTED_EVERY_REPO):
            breaches.append(
                Breach(change, "write inside an always-protected path in ANY declared "
                               "repo (never config-overridable)")
            )
            continue
        if change_root == Path(root).resolve() and any(
            _matches(change.path, p) for p in protected
        ):
            breaches.append(
                Breach(change, "write inside an always-protected path in the root repo "
                               "(never config-overridable)")
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


@dataclass(frozen=True)
class TrackedUnder:
    """What git knows under a path, kept as TWO answers rather than one total.

    The previous version unioned the index and HEAD and returned `len(seen)`. The
    union is right; collapsing it to an integer is not, because the caller then
    cannot tell WHICH question said yes — and the two say different things:

      HEAD knows it   -> deleting destroys COMMITTED work. Refuse, always.
      only the index  -> this is the phase's OWN staged write (`git add`, `git mv`).
                         Nothing committed is at risk, and the identification was
                         never wrong. Refuse, but say THAT.

    Shipped, the single count produced a refusal whose BOTH clauses were false —
    "the path identification is wrong and deleting it would destroy committed work"
    over a file the phase had just `git add`-ed, which HEAD had never heard of. K4
    fixed one instance of the false-reason class; this fixes the class in this guard
    (Gate-2 L3). A refusal that asserts a misidentification which did not occur sends
    the reader hunting a parse bug that isn't there.
    """

    in_head: tuple[str, ...]
    in_index: tuple[str, ...]
    unanswered: tuple[str, ...]

    def __bool__(self) -> bool:
        """True when there is any reason not to delete — including not knowing."""
        return bool(self.in_head or self.in_index or self.unanswered)

    @property
    def count(self) -> int:
        return len(set(self.in_head) | set(self.in_index))


def _tracked_under(root: Path, rel: str) -> TrackedUnder:
    """Ask BOTH questions git can answer about a path, and keep them apart.

    `git ls-files` reads the INDEX, and the index can be silenced while the content
    is still committed and still on disk: `git rm --cached` and `assume-unchanged`
    both do it. A guard that asks only the index answers "no tracked content" for a
    path whose deletion destroys committed work — the exact outcome the guard exists
    to refuse (Gate-2 K3). `ls-tree HEAD` is the second question.

    Both questions are asked in git's pathspec language, which is why `_GIT_ENV` is
    load-bearing here: under default pathspecs a directory named `:magic` made BOTH
    halves return rc=0 with empty output, and zero is the answer that authorises
    `rmtree` (Gate-2 L1b).

    A question git REFUSES to answer is recorded as unanswered, not as `no`. An
    unborn HEAD is not a refusal — it is the real answer "nothing is committed yet".
    """
    index_proc = _git(root, "ls-files", "--", rel)
    in_index = tuple(l for l in index_proc.stdout.splitlines() if l.strip())
    unanswered: list[str] = []
    if index_proc.returncode != 0:
        unanswered.append(f"git ls-files failed: {index_proc.stderr.strip()[:120]}")

    in_head: tuple[str, ...] = ()
    if _git(root, "rev-parse", "--quiet", "--verify", "HEAD").returncode == 0:
        head_proc = _git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", rel)
        in_head = tuple(l for l in head_proc.stdout.splitlines() if l.strip())
        if head_proc.returncode != 0:
            unanswered.append(f"git ls-tree HEAD failed: {head_proc.stderr.strip()[:120]}")
    return TrackedUnder(in_head, in_index, tuple(unanswered))


def _is_whole_tree_pathspec(rel: str, root: Path, fenced: list[Path]) -> str | None:
    """Reason this pathspec names a TREE rather than an artifact, or None.

    A rollback that cannot name a file has not identified an artifact; it has
    identified a tree, and acting on a tree is a human decision. `git checkout -- .`
    restores every tracked file in the repository from the index — it destroyed a
    fenced repo's uncommitted work over a single empty directory, and recorded the
    word `restored` (Gate-2 K1). This is the destroyer guard's principle applied to
    the other destructive verb: the refusal does not depend on knowing which
    measurement produced the coarse path.

    COMPLETENESS, and what it rests on. Under `GIT_LITERAL_PATHSPECS=1` (set for
    every call in this module, see `_GIT_ENV`) the whole-tree forms are exactly
    three: the empty pathspec, `.`, and a path that resolves to a declared tree's
    own root. That is an enumeration of a closed set, and it is why the environment
    variable is load-bearing rather than defensive. Without it this function is a
    partial enumeration of an OPEN set — the magic prefixes — and a partial
    enumeration whose miss returns "proceed" is the family defect (Gate-2 L1a).

    `*` and `**` are kept in the refusal list even though literal pathspecs strip
    them of meaning. They are then merely unusual filenames, so refusing them costs
    one un-undone artifact and buys independence from the environment variable
    staying set. Refusal is the safe direction; that is the whole reason it is
    permitted to be over-broad here.
    """
    norm = rel.strip().rstrip("/")
    if norm in ("", ".", "*", "**", "./"):
        return f"the pathspec {rel!r} names the whole of {root}"
    # `..`-prefixed: this also refuses a legal filename that merely BEGINS with two
    # dots. Deliberate, and not to be "fixed" — an escape from the root and a file
    # named `..config` are indistinguishable by prefix, and only one of them is
    # survivable. The cost is an artifact left standing inside the fence (L7).
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
                    guard="whole_tree",
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
                        guard="quarantine_failed",
                    )
                )
                continue

        # Gate-2 F3. Keyed on the PATH, not on `change.kind`: the kind is a measurement,
        # and C1's fourth clause is that a check must not be switchable off by anything
        # it certifies. `.git/config` being modified, a hook being planted, and a hook
        # being deleted arrive as three different kinds, and all three must refuse.
        # Refuse, do not act: git never reports these paths, so `git checkout --` cannot
        # restore one, and the created-path branch would find nothing tracked underneath
        # — correctly, git tracks nothing in there — and authorise `rmtree` on
        # `.git/config`. The breach is detected, quarantined and named; a human decides.
        # JR-5: on the marker-bearing keys (`.git\t<gitdir pointer unreadable: …>`)
        # neither arm matched, so the ONE class of change where git's control plane is
        # provably unreadable fell through to the ordinary rollback verbs below.
        git_path = marker_path(change.path)
        if git_path == ".git" or git_path.startswith(".git/"):
            actions.append(
                RollbackAction(
                    change.path,
                    "NOT_ROLLED_BACK",
                    "REFUSED: this is git's own control surface — a hook, its config, or "
                    "its exclude list. Nothing here is ever a phase write, and git "
                    "tracks none of it, so every rollback verb available would either "
                    "no-op or destroy the repository. Quarantined and reported; undoing "
                    "it is a human decision",
                    quarantined,
                    guard="git_internal",
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
                    guard="committed",
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
                    guard="dirty_before",
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
            tracked = _tracked_under(root, change.path)
            if tracked:
                # Say which question answered yes. The three cases are genuinely
                # different and the reader acts on them differently (Gate-2 L3).
                if tracked.unanswered:
                    why = (
                        "git could not say whether it tracks content here "
                        f"({'; '.join(tracked.unanswered)}) — an unanswered question "
                        "is not a `no`, and deleting on `we do not know` is the one "
                        "thing containment must never do"
                    )
                elif tracked.in_head:
                    why = (
                        f"reported as created by the phase, but HEAD holds "
                        f"{len(tracked.in_head)} file(s) under it — the path "
                        "identification is wrong and deleting it would destroy "
                        "committed work"
                    )
                else:
                    why = (
                        f"the phase staged this itself — git's index holds "
                        f"{len(tracked.in_index)} file(s) under it and HEAD holds "
                        "none. Nothing committed is at risk, and the identification "
                        "is right; but undoing a staged write means editing the "
                        "index of a fenced tree, which is a human decision"
                    )
                # The destroyer guard's numbers were written into English here while
                # the staging guard's travelled as data — so the wall could check one
                # and only read the other. The tightened wall check found this site
                # the moment it stopped asking the ACTION whether measurements were
                # owed and started asking git (Gate-2 B1, second call site). One
                # extra git call, on a path that has already decided to refuse.
                measured = (
                    ("head_files", len(tracked.in_head)),
                    ("index_files", len(tracked.in_index)),
                    ("staged_paths", len(_staged_against_head(root, change.path).paths)),
                )
                actions.append(
                    RollbackAction(
                        change.path,
                        "NOT_ROLLED_BACK",
                        f"REFUSED: {why}. Measured here: "
                        f"{render_containment_facts(measured)}",
                        quarantined,
                        measured,
                        guard="destroyer",
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
                            guard="nothing_at_path",
                        )
                    )
                    continue
                actions.append(
                    RollbackAction(change.path, "deleted", "created by the phase", quarantined)
                )
            except OSError as exc:
                actions.append(
                    RollbackAction(
                        change.path, "NOT_ROLLED_BACK", f"delete failed: {exc}",
                        quarantined, guard="delete_failed",
                    )
                )
            continue

        if change.kind == "unknown":
            # The classifier could not name what happened here. Every remaining verb
            # acts — `git checkout --` writes the worktree from the index — and a verb
            # chosen on an unclassified change is a verb chosen at random. Default-fail
            # has to reach the classifier too, not just its callers (Gate-2 L2).
            actions.append(
                RollbackAction(
                    change.path,
                    "NOT_ROLLED_BACK",
                    f"REFUSED: git reported status {change.after_status!r}, which this "
                    "classifier does not recognise. An unrecognised state is not a "
                    "modification, and undoing it would be a guess",
                    quarantined,
                    guard="unknown_status",
                )
            )
            continue

        # THE STAGING GUARD. `git checkout -- <path>` restores from the INDEX, so it
        # is only a restore while the index still holds the baseline. The moment the
        # phase runs `git add`, the index holds the PHASE's content and the same
        # command rewrites the file with the very bytes containment exists to remove
        # — then reports `restored`. Gate-2 L2 found this on a rename destination;
        # the property is the whole X≠' ' column, `M ` included (Gate-2 L2, general).
        #
        # So: containment does not restore staged work. It refuses and names the
        # index — the same answer the destroyer guard already gives staged creations,
        # for the same reason. Nothing here edits the index of a fenced tree; that is
        # a human decision, and the recovery command is printed so it is a cheap one.
        staged = _staged_against_head(root, change.path)
        if staged:
            held = _tracked_under(root, change.path)
            if staged.unanswered:
                what = (
                    "git could not say whether its index here differs from HEAD "
                    f"({'; '.join(staged.unanswered)}). `git checkout --` writes the "
                    "worktree FROM the index, so an unanswered question is not a `no`"
                )
            else:
                what = (
                    f"git's index differs from HEAD at {len(staged.paths)} path(s) "
                    "here, which is the phase's own staged content — `git checkout --` "
                    "reads the INDEX, not HEAD, so it would write back exactly what "
                    "containment is removing, under a receipt saying `restored`"
                )
            # Every clause below is MEASURED, and the measurements TRAVEL. Round
            # seven made the numbers true and left them inside a sentence; the wall
            # could then only check the sentence, so rewriting the sentence as a flat
            # falsehood passed (Gate-2 B1). The numbers now ride on the action and the
            # sentence is rendered from them.
            measured = (
                ("head_files", len(held.in_head)),
                ("index_files", len(held.in_index)),
                ("staged_paths", len(staged.paths)),
            )
            actions.append(
                RollbackAction(
                    change.path,
                    "NOT_ROLLED_BACK",
                    f"REFUSED: {what}. Measured here: "
                    f"{render_containment_facts(measured)}. Editing the index of a "
                    f"fenced tree is a human decision (status {change.after_status!r}; "
                    f"recover from the commit with: "
                    f"git checkout HEAD -- {change.path!r})",
                    quarantined,
                    measured,
                    guard="staging",
                )
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
                    guard="checkout_failed",
                )
            )
    return actions
