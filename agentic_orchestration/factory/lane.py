"""Vendor-lane primitives — THE SERIAL LAW, made structural.

    ONE `codex exec` at a time. One `auth.json`, one job stream.

This is an OpenAI CI/CD-auth precondition ("one machine or serialized job stream"),
not a preference, and this module exists so that violating it is not something a
caller can do by forgetting something.

Four surfaces live here, in the order they matter:

1. `SerialLaneLock` — the mutual exclusion. Held at the `codex exec` INVOCATION
   SITE, never merely at a queue-process boundary.
2. `SeamSlotSemaphore` — the SAME primitive, counted, for a lane whose serial law
   is policy rather than vendor precondition. **The Codex lane never takes it:**
   P-1 cites a verified OpenAI precondition and § 9.5 probed xAI, so the evidence
   that loosened the Grok lane does not travel across vendors. Grok's law is now
   *one job per named agent seam, ceiling N=3 per credential* (§ 9.6 AM-3).
3. `RunLog` — the lane's liveness surface, `_run-log.tsv`. The pre-fire check of
   record is *"last row terminal"*, answerable by `tail -1`, and this module
   generalises the format ADDITIVELY so that check keeps working.
4. `Telemetry` — append-only JSONL, one event per line, emitted from birth.

THE MUTUAL-EXCLUSION PRIMITIVE, NAMED
-------------------------------------
`fcntl.flock(fd, LOCK_EX | LOCK_NB)` on a lock file keyed to the `CODEX_HOME` that
owns the `auth.json` being serialised. Chosen over the three alternatives for
reasons that were MEASURED on this host (Darwin 24.6.0, 2026-08-24), not assumed:

  * **A PID file** (`O_EXCL` + a stale-PID reaper) is the obvious answer and it is
    the wrong one. Its two failure modes are symmetric and both are fatal here: a
    reaper that clears too slowly wedges the lane behind a dead process, and a
    reaper that clears too eagerly runs two jobs against one `auth.json` — which
    is the one thing this module exists to prevent. `flock` has no reaper because
    it needs none: the kernel drops the lock when the holder dies, including on
    SIGKILL, where no userspace cleanup runs at all.
  * **An in-process `threading.Lock`** cannot see a second process, so it is not a
    lock for this problem.
  * **A queue-level "only one drainer" guard** is what Gate-1 explicitly refused:
    one process spawning two children is the same violation as two processes.

The measurement that makes `flock` sufficient for the tightened requirement —
and it is the non-obvious half, because `flock` is often described as
per-PROCESS:

    same process, two separate open() calls on the same path
    -> second flock(LOCK_EX|LOCK_NB) FAILS, errno 35 (EWOULDBLOCK)

`flock` locks are held by the OPEN FILE DESCRIPTION, not by the process, so a
second `open()` in the SAME process conflicts with the first. `acquire()` below
therefore opens a FRESH descriptor every time and never caches one, which is what
turns "two processes cannot both run" into "two `codex exec` invocations cannot
both run, however they were reached" — including two threads, two nested calls,
and one drain loop that got its concurrency wrong.

THE CRASH FAILURE-MODE I ACCEPTED, AND WHY
------------------------------------------
The lock fd is made INHERITABLE and passed to the `codex exec` child, so the child
holds the same open file description and therefore the same lock. Lock lifetime is
consequently `max(queue process, codex exec process)` and never longer.

  * **REFUSED:** a dead process's lock outliving it. There is no lock file whose
    mere existence blocks anything, no PID to go stale, and no reaper to tune. A
    `kill -9` of the queue releases the lane the instant the last holder exits.
  * **ACCEPTED:** a LIVE ORPHANED `codex exec` — one whose parent queue was killed
    while it ran — continues to hold the lane until it exits or is killed. That is
    a real way to wedge the lane, and it is the failure I chose, because that
    process is genuinely using the `auth.json`; releasing the lane for it would be
    the double-fire the serial law forbids. A wedged lane is loud (`ps` shows the
    holder, `_run-log.tsv`'s last row is non-terminal) and fails CLOSED. A
    double-fire is silent and violates a vendor precondition.

There is deliberately NO timeout-based lock breaking and NO `--force` flag. Adding
one converts the refused failure mode back into the accepted one at exactly the
moment an operator is impatient.
"""

from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

#: Bumped when the JSONL event shape changes in a way a reader must notice.
#: DELIBERATELY NOT the U-1 flight-recorder schema: those axes are Matt's F-1…F-8
#: rulings and are not ours to freeze. Every event carries this string and a
#: `passthrough` object, so a recorder can normalise later against axes that do
#: not exist yet.
TELEMETRY_SCHEMA_VERSION = "reincarnated.lane.telemetry/0.1"

#: The `_run-log.tsv` column count this module writes. Columns 1-4 are the proven
#: runner's, byte-for-byte in the same positions; 5 and 6 are additive.
RUNLOG_COLUMN_COUNT = 6

#: Markers in COLUMN 3 that mean "no `codex exec` is running for this job".
#:
#: This is the vocabulary the pre-fire check of record spends — *"last row
#: terminal"* — which the U-4 router's question (3) reads and which knight-rider
#: reads at session start. It fails open in the ADDITION direction: adding a marker
#: here makes some non-idle state read as idle, and nothing downstream can notice,
#: because the row that would catch it must exercise a state nobody has named yet.
#: Pinned by literal in `tests/test_vocabularies.py` for that reason.
#:
#: `rc=N` is matched by PREFIX (the proven runner writes `rc=0`, `rc=1`, …) and is
#: therefore handled in `is_terminal_marker` rather than enumerated here.
TERMINAL_MARKERS = frozenset({
    "SKIP-EXISTS",       # the proven runner's idempotency marker
    "FALLBACK-CLAUDE",   # handed to the named Claude curator's lane; not ours any more
    "AUTH-BLOCKED",      # lane closed on a Matt-only action; nothing is executing
    "ENQUEUE-REFUSED",   # never fired (e.g. no curator named)
})

#: Non-terminal markers. The OTHER HALF of the accept vocabulary `RunLog.append`
#: enforces: a marker in neither set is REFUSED AT WRITE TIME, so the liveness
#: surface cannot gain a state nobody adjudicated. That refusal is what makes this
#: collection load-bearing rather than a label — without it, a caller could write
#: `DONE` and the terminal check would (correctly, and uselessly) call it busy while
#: everyone reading the file assumed otherwise.
#:
#: Fails open in the ADDITION direction, same as its terminal sibling, and is pinned
#: by literal in `tests/test_vocabularies.py` for the same reason.
BUSY_MARKERS = frozenset({
    "ENQUEUED",   # accepted, not yet drained: the lane has work pending
    "START",      # a `codex exec` was launched and no finish row followed it
})

#: The `-s` values `codex exec` accepts, as a CLOSED vocabulary. `read-only` is the
#: posture of record for research jobs; the others exist and must be NAMED by a job
#: class rather than reached by typo. Addition is the fail-open direction — a new
#: member admits a sandbox posture nobody adjudicated — so this is pinned by
#: literal in `tests/test_vocabularies.py`.
SANDBOX_MODES = frozenset({"read-only", "workspace-write", "danger-full-access"})


def utcnow() -> str:
    """`2026-08-24T14:03:40Z` — the exact spelling the proven runner's rows carry."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# 1 — the lock
# ---------------------------------------------------------------------------
class LaneBusy(RuntimeError):
    """A second `codex exec` was attempted while one was running. Fails CLOSED.

    Carries the lock path so the message can say WHICH lane and WHY, rather than
    leaving an operator to guess at a refusal.
    """

    def __init__(self, path: Path):
        self.path = path
        super().__init__(
            f"THE SERIAL LAW: another `codex exec` holds {path}. One `auth.json`, one "
            "job stream — a busy lane means queue behind it or fire the Claude lane, "
            "NEVER parallel. This refusal is the lock working, not a fault to retry "
            "around. If nothing should be running, `ps` will name the live holder: the "
            "kernel releases this lock when its last holder exits, so an occupied lock "
            "means an occupied lane."
        )


#: Where every vendor lane's credential home lives, and the environment variable that
#: relocates it. Keyed by VENDOR because P-3's granularity is per-CREDENTIAL and a
#: credential belongs to exactly one vendor: `~/.codex/auth.json` and
#: `~/.grok/auth.json` are two tokens, two lanes, and — per Amendment B — two blast
#: radii that never cross.
VENDOR_HOMES: dict[str, tuple[str, str]] = {
    # vendor -> (env var that overrides the home, default home relative to ~)
    "codex": ("CODEX_HOME", ".codex"),
    "grok": ("GROK_HOME", ".grok"),
}


def default_lock_path(
    home: str | os.PathLike[str] | None = None,
    vendor: str = "codex",
) -> Path:
    """The lock is keyed to the `auth.json` it serialises, not to a queue directory.

    Two different queue directories sharing one credential home share one auth token
    and MUST share one lock; two different homes are two different tokens and must NOT
    block each other. Keying on the queue directory would have got both of those
    backwards, which is why the key is the resolved credential-home path.

    The lock lives OUTSIDE the credential home (under `~/.reincarnated/lane-locks/`) so
    that nothing we create is ever walked, cached or session-scanned by the vendor CLI
    whose home it names.

    **`vendor` is part of the FILENAME, not merely of the digest**, and that is
    deliberate: an operator running `ls ~/.reincarnated/lane-locks/` must be able to
    see WHICH vendor holds a lane without resolving a sha256 back to a path. The digest
    still keys the credential home, so two `CODEX_HOME`s remain two locks.

    The signature keeps `codex` as the default vendor and the same digest computation,
    so `default_lock_path()` with no arguments returns the same path it always did —
    the fleet board calls it that way (`flight/bin/flight_report::probe_lane_lock`) and
    a rename here would have silently pointed that view at a lock nobody takes.
    """
    if vendor not in VENDOR_HOMES:
        raise ValueError(
            f"lane lock: vendor {vendor!r} has no declared credential home. Known: "
            f"{sorted(VENDOR_HOMES)}. A lane whose credential home nobody named cannot "
            "be serialised per-credential, which is the one granularity P-3 rules."
        )
    env_var, default_dirname = VENDOR_HOMES[vendor]
    home = home or os.environ.get(env_var) or (Path.home() / default_dirname)
    resolved = str(Path(home).expanduser().resolve())
    digest = hashlib.sha256(resolved.encode("utf-8")).hexdigest()[:12]
    root = Path(os.environ.get("REINCARNATED_LANE_LOCK_DIR", Path.home() / ".reincarnated" / "lane-locks"))
    return root / f"{vendor}-{digest}.lock"


class SerialLaneLock:
    """`flock(LOCK_EX | LOCK_NB)` around ONE `codex exec`. See the module docstring.

    Used as a context manager at the invocation site:

        with SerialLaneLock(path) as lock:
            subprocess.run(argv, pass_fds=(lock.fd,), ...)

    `pass_fds` is not optional decoration. It is what makes the lock's lifetime equal
    the CHILD's lifetime rather than the parent's, and it is the whole reason a killed
    queue cannot leave a live `codex exec` running on an unlocked lane.
    """

    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path is not None else default_lock_path()
        self._fd: int | None = None

    @property
    def fd(self) -> int:
        if self._fd is None:
            raise RuntimeError(
                "SerialLaneLock.fd read while the lock is not held. The descriptor IS "
                "the lock; handing out a stale integer would hand out a lock nobody "
                "holds."
            )
        return self._fd

    def acquire(self) -> "SerialLaneLock":
        """Take the lane or raise `LaneBusy`. NEVER blocks, NEVER waits, NEVER breaks.

        A fresh descriptor every time, deliberately: `flock` is held by the open file
        description, so re-opening is what makes a SECOND acquisition inside the SAME
        process fail (measured: errno 35). Caching one fd would make the same process
        able to hold the lane twice, which is Gate-1's exact refused case.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.path, os.O_CREAT | os.O_RDWR, 0o644)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            os.close(fd)
            if exc.errno in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EACCES):
                raise LaneBusy(self.path) from exc
            raise
        # Inheritable ON PURPOSE (see the crash-failure-mode note in the module
        # docstring). Python 3.4+ makes descriptors non-inheritable by default, so
        # this line is the difference between a lock that dies with the queue and a
        # lock that lives as long as the `codex exec` it is protecting.
        os.set_inheritable(fd, True)
        os.write(fd, b"")  # touch; the CONTENT is never read and never trusted
        self._fd = fd
        return self

    def release(self) -> None:
        if self._fd is None:
            return
        fd, self._fd = self._fd, None
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)

    def __enter__(self) -> "SerialLaneLock":
        return self.acquire()

    def __exit__(self, *exc: object) -> None:
        self.release()


# ---------------------------------------------------------------------------
# 1b — the COUNTED semaphore (§ 9.6 AM-3, Amendment N)
# ---------------------------------------------------------------------------
#: **N=3, and what that number is and is not** (Amendment O). CONFIRMED at default
#: reasoning effort, trivial single-line prompts, n=6 across two rounds (§ 9.5's live
#: concurrency probe: 3/3 clean, 4s wall against a 4.3s single-job baseline, no 429, no
#: `leader.sock`). **PROVISIONAL at this lane's own pinned posture** — `grok-4.6 @
#: xhigh` against the ~28,170-token input floor measured at Gate-2 (G2-2) is not the
#: same load on a token-bucket limiter as three trivial default-effort calls, and the
#: probe never ran there.
#:
#: THE RAISE LICENSE, CORRECTED (O.1): this number rises **only on a probe at the
#: proposed level**. Clean in-window rows at 3 confirm 3 — they retire "provisional",
#: they never license 4. The discharge event is a NAMED LANE EVENT, recorded, not
#: noticed in passing: `factory/MIGRATION.md` § 11.3 names it and the row that carries
#: it. The ceiling DROPS to k-1 on the first 429, auth flag, or measurable output
#: degradation observed at k concurrent jobs (O.3) — erring toward do-not-fire is this
#: lane's chosen failure everywhere else, and the ceiling is not the one place it is
#: chosen the other way.
GROK_SLOT_CEILING = 3

#: `extra["lane_state"]` on a `RawResult` whose SEAM already holds a slot. **Amendment
#: R:** this is NOT `"busy"` and NOT a fault. Surfacing it as busy stops the whole drain
#: at 1/3 with two slots idle (head-of-line blocking, inverting AM-3's own purpose);
#: surfacing it as a fault counts an attempt and hands the job PERMANENTLY to
#: FALLBACK-CLAUDE for a condition that clears in minutes — the exact defect
#: `jobqueue.drain`'s standing comment records being made once already. It is its own
#: outcome, and `JobQueue._run_one` skips on it.
LANE_STATE_SEAM_HELD = "per-agent-slot-held"

#: The `detail`-column token that makes a per-agent skip COUNTABLE (R.3), in the shape
#: G-7 gave lane contention: `grep -c "skipped=per-agent-slot-held" _run-log.tsv`. A
#: queue that silently reorders is folklore; one that says why is evidence — and this is
#: a number the job-10 banking verdict will want.
SKIPPED_PER_AGENT = "per-agent-slot-held"


class SeamSlotHeld(RuntimeError):
    """This SEAM already holds a slot on this lane. A JOB-specific refusal, never a lane state.

    Distinct from `LaneBusy` by TYPE and not merely by message, because the two produce
    opposite correct behaviours in a drain (Amendment R.1): `LaneBusy` means *the
    credential's ceiling is full, stop*; this means *this one job cannot go now, take
    the next one*. A caller that cannot tell them apart will get one of them wrong.
    """

    def __init__(self, seam: str, path: Path):
        self.seam = seam
        self.path = path
        super().__init__(
            f"PER-AGENT SLOT: seam {seam!r} already holds a Grok slot ({path.name}). "
            "One in-flight vendor job per named agent seam (§ 9.6 AM-3): the refusal is "
            "at the CLAIM and it is refuse-don't-queue — this agent's second task "
            "enqueues normally and an enqueued job holds nothing. This is NOT a busy "
            "lane (other seams may still fire; the ceiling is the only bound on total "
            "fan-out) and NOT a fault (it is never an attempt, and it never reaches the "
            "Claude fallback). The kernel releases this lock when its last holder exits, "
            "so an agent that crashes mid-job is not locked out of its own lane."
        )


class LaneCeilingReached(LaneBusy):
    """Every slot on the credential is held. THE LANE is busy — the existing break is correct.

    A subclass of `LaneBusy` on purpose: under the serial law "lane busy" meant *the one
    slot is taken*, and under AM-3 it means *all N slots are taken*. Both are the same
    fact to every consumer — the credential cannot take more work right now — so a drain
    that already breaks on `LaneBusy` keeps doing the right thing without being taught a
    new word. What changed is only the ARITY, and arity is not a new disposition.
    """

    def __init__(self, ceiling: int, paths: tuple[Path, ...]):
        self.ceiling = ceiling
        self.paths = paths
        self.path = paths[0] if paths else Path("(no slots declared)")
        RuntimeError.__init__(
            self,
            f"THE CEILING: all {ceiling} slot(s) on this credential are held "
            f"({', '.join(p.name for p in paths)}). The ceiling is the CREDENTIAL's — "
            "one grok.com subscription, one usage window — and the slot is the DISPATCH "
            "grain. Slot 4 ENQUEUES (a P-9 named-condition hold); it does not wait, "
            "does not break a slot, and does not fall back to Claude on backlog alone: "
            "a full lane is OCCUPIED, not CLOSED (Amendment H), so § 10.3 step 4's "
            "Claude branch is NOT reachable from here. There is no timeout, no "
            "`--force`, and no stale-slot reaper — P-2 restated PER SLOT, because three "
            "files is three times the 'just break slot 2' temptation and the law does "
            "not thin out by division."
        )


def seam_lock_path(base: Path, seam: str) -> Path:
    """`<vendor>-<credential digest>-agent-<seam>.lock` — the per-seam lock (N.1(i)).

    Derived from the lane's BASE lock path rather than spelled independently, so the
    credential digest rides along: the lane spec writes this file as
    `grok-agent-<seam>.lock`, and building it that way would key per-agent exclusivity
    to the VENDOR instead of to the CREDENTIAL. Two `GROK_HOME`s are two lanes under
    P-3, and one seam legally holds one slot on each; a digest-less name would have
    merged them into a single semaphore and refused the second, silently narrowing a
    granularity ruling nobody re-opened. The vendor and the seam are both still legible
    in an `ls`, which is the property the spec's spelling was after.
    """
    return base.with_name(f"{base.stem}-agent-{seam}.lock")


def slot_lock_path(base: Path, index: int) -> Path:
    """`<vendor>-<credential digest>-slot-<i>.lock` — one counted slot (N.1(ii))."""
    return base.with_name(f"{base.stem}-slot-{index}.lock")


def slot_lock_paths(base: Path, ceiling: int = GROK_SLOT_CEILING) -> tuple[Path, ...]:
    return tuple(slot_lock_path(base, i) for i in range(ceiling))


@dataclass(frozen=True)
class SlotOccupancy:
    """What the counted semaphore looks like RIGHT NOW. Derived, read-only, emits nothing.

    `tags` are DISPLAY-ONLY (Amendment N.3) and are read only for a slot whose
    `LOCK_NB` probe just FAILED — i.e. a slot proved held by the kernel. No fire/refuse
    decision anywhere reads them. That restriction is the whole of N: enforcing
    exclusivity by reading a tag rebuilds the assert-style lockfile G-1 dissolved (stale
    content outlives the lock, write-after-acquire is a window, scan-then-claim is
    TOCTOU) — so the tag exists to tell a human WHO, and nothing else.

    `unreadable` is counted separately from `held` and is ALSO INCLUDED in `held`
    (Amendment Q.1): a slot that cannot be read counts HELD, so `free` never
    over-reports. Keeping the count beside it is what lets a caller distinguish *the
    lane is full* from *the instrument is broken* — the first is `busy-lock` and the
    second, when it is total, is `busy-unknown`.
    """

    total: int
    held: int
    free: int
    unreadable: int
    tags: tuple[str, ...] = ()

    @property
    def all_held(self) -> bool:
        return self.total > 0 and self.free == 0

    @property
    def all_unreadable(self) -> bool:
        return self.total > 0 and self.unreadable == self.total

    def to_dict(self) -> dict[str, Any]:
        """The `k/3` payload, whose KEY SET is pinned across both derivations (Q.3)."""
        return {
            "total": self.total,
            "held": self.held,
            "free": self.free,
            "unreadable": self.unreadable,
            "tags": list(self.tags),
        }

    def one_line(self) -> str:
        return f"{self.free}/{self.total} free"


def probe_slot(path: Path) -> tuple[str, str]:
    """One slot: `("free"|"held"|"unreadable", tag-or-reason)`. Acquires nothing durable.

    A slot file that does not exist is FREE and is **not created** — `lane_is_free`
    opens with `O_CREAT`, and asking it here would make a read-only status call leave a
    file behind, which is the § 3 emits-nothing discipline broken by the instrument that
    exists to uphold it. A lock file that does not exist cannot be held.

    Any other `OSError` is `unreadable`, never `free`. That is Amendment Q.1 at the
    smallest grain: leg 1 grew from one read to three, and a partial read that resolved
    toward "free" would let one broken permission bit fire a job at a full lane.
    """
    if not path.exists():
        return "free", "no slot file exists — nothing has ever taken this slot"
    try:
        fd = os.open(path, os.O_RDWR)
    except OSError as exc:
        return "unreadable", f"{path.name}: {exc.strerror or exc}"
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            if exc.errno in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EACCES):
                # HELD — proved by the kernel. ONLY NOW may the tag be read, and only
                # for display (N.3).
                try:
                    tag = os.pread(fd, 512, 0).decode("utf-8", "replace").strip()
                except OSError:
                    tag = ""
                return "held", tag or f"{path.name} (held; no tag written yet)"
            return "unreadable", f"{path.name}: {exc.strerror or exc}"
        fcntl.flock(fd, fcntl.LOCK_UN)
        return "free", ""
    finally:
        os.close(fd)


def probe_slots(base: Path, ceiling: int = GROK_SLOT_CEILING) -> SlotOccupancy:
    """Leg 1 for a COUNTED lane: `k/N`, fail-closed PER SLOT (Amendment Q.1).

    Three acquire-and-release probes instead of one, and no writes — G-4 holds
    unchanged: a `k/3` answer is no more a reservation than an `open` answer was.
    """
    held = free = unreadable = 0
    tags: list[str] = []
    for path in slot_lock_paths(base, ceiling):
        state, note = probe_slot(path)
        if state == "free":
            free += 1
        elif state == "held":
            held += 1
            if note:
                tags.append(note)
        else:
            # UNREADABLE COUNTS HELD (Q.1). Counted in both places on purpose: `held`
            # is what the disposition is computed from, `unreadable` is what tells a
            # human the difference between a full lane and a broken instrument.
            held += 1
            unreadable += 1
            tags.append(f"UNREADABLE: {note}")
    return SlotOccupancy(total=ceiling, held=held, free=free,
                         unreadable=unreadable, tags=tuple(tags))


class SeamSlotSemaphore:
    """**AMENDMENT N — TWO NESTED FLOCKS.** Per-seam lock FIRST, then a counted slot.

        with SeamSlotSemaphore(base, seam="star-lord") as sem:
            subprocess.run(argv, pass_fds=sem.fds, ...)

    The ordering is the ruling, and so is the primitive:

      1. **`grok-agent-<seam>.lock`** — its acquisition failing IS the second-claim
         refusal, *by construction*, with no content read and no race. The alternative
         the spec first reached for — tag each slot with its claiming seam and scan the
         tags — is check-then-act over file CONTENT, which is Amendment K's TOCTOU one
         axis over, on top of a stale tag that outlives its lock. jack-ryan named it a
         Gate-2 BLOCK-if-built. The fix costs one more `flock`.
      2. **`grok-slot-{0..N-1}.lock`** — first acquirable wins; all held raises
         `LaneCeilingReached`, which IS a busy lane.

    Released in reverse order. **Both are `LOCK_NB`. Nothing here ever waits**, so the
    nesting cannot deadlock — that property is stated rather than left to be
    rediscovered, because it is the reason a fixed acquisition order is safe here and
    is not safe in general.

    **Both fds are inheritable and both are `pass_fds`'d to the child** (N.2), so both
    lifetimes are `max(queue, grok)` — a killed queue leaves neither an untracked job
    stream nor a phantom seam hold, and a dead holder's per-seam lock is released by
    the kernel, so an agent that crashes mid-job is not locked out of its own lane.

    **Nothing else in this package takes these locks.** Enqueued jobs hold nothing
    (N.5): an agent's backlog must not lock the agent out of its own next fire.
    """

    def __init__(
        self,
        base: Path,
        seam: str,
        ceiling: int = GROK_SLOT_CEILING,
    ):
        self.base = Path(base)
        self.seam = str(seam)
        self.ceiling = int(ceiling)
        self.slot_index: int | None = None
        self._seam_fd: int | None = None
        self._slot_fd: int | None = None

    # -- fds ----------------------------------------------------------------
    @property
    def fds(self) -> tuple[int, ...]:
        if self._seam_fd is None or self._slot_fd is None:
            raise RuntimeError(
                "SeamSlotSemaphore.fds read while the semaphore is not fully held. The "
                "descriptors ARE the locks; handing out stale integers would hand out "
                "locks nobody holds — and `pass_fds` would then close them into the "
                "child's table as ordinary numbers."
            )
        return (self._seam_fd, self._slot_fd)

    @property
    def seam_lock_path(self) -> Path:
        return seam_lock_path(self.base, self.seam)

    def slot_paths(self) -> tuple[Path, ...]:
        return slot_lock_paths(self.base, self.ceiling)

    # -- acquire / release ---------------------------------------------------
    def acquire(self) -> "SeamSlotSemaphore":
        """Take the seam, then a slot. Raises `SeamSlotHeld` or `LaneCeilingReached`.

        A fresh descriptor every time, for the reason `SerialLaneLock.acquire` gives:
        `flock` binds to the open file description, so re-opening is what makes a second
        acquisition inside the SAME process fail (measured, errno 35). That is what
        makes one process's two threads as safely excluded as two processes.
        """
        self.base.parent.mkdir(parents=True, exist_ok=True)
        seam_path = self.seam_lock_path
        seam_fd = os.open(seam_path, os.O_CREAT | os.O_RDWR, 0o644)
        try:
            fcntl.flock(seam_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            os.close(seam_fd)
            if exc.errno in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EACCES):
                raise SeamSlotHeld(self.seam, seam_path) from exc
            raise
        os.set_inheritable(seam_fd, True)

        slot_paths = self.slot_paths()
        for index, path in enumerate(slot_paths):
            try:
                slot_fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o644)
            except OSError:
                # An unopenable slot is not an available slot. Fail-closed here for the
                # same reason `probe_slot` counts it HELD.
                continue
            try:
                fcntl.flock(slot_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                os.close(slot_fd)
                if exc.errno in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EACCES):
                    continue
                self._release_fd(seam_fd)
                raise
            os.set_inheritable(slot_fd, True)
            # TRUNCATE-ON-ACQUIRE (N.3), so a stale tag cannot survive one handover, and
            # a reader who (legitimately, for display) reads a held slot never sees the
            # previous holder's name. Written AFTER the lock, which is why the window
            # between acquisition and tag-write is harmless: the tag is not the claim.
            os.ftruncate(slot_fd, 0)
            os.pwrite(slot_fd, self._tag().encode("utf-8"), 0)
            self._seam_fd, self._slot_fd, self.slot_index = seam_fd, slot_fd, index
            return self

        # Every slot held. Give the seam lock back BEFORE raising: a refused claim that
        # keeps holding something is a refusal that can wedge the lane it declined.
        self._release_fd(seam_fd)
        raise LaneCeilingReached(self.ceiling, slot_paths)

    def _tag(self) -> str:
        """DISPLAY ONLY. Never parsed, never compared, never a fire/refuse input (N.3)."""
        return f"seam={self.seam} pid={os.getpid()} since={utcnow()}"

    @staticmethod
    def _release_fd(fd: int) -> None:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)

    def release(self) -> None:
        """Reverse order (N.1): the slot first, then the seam."""
        slot_fd, self._slot_fd = self._slot_fd, None
        seam_fd, self._seam_fd = self._seam_fd, None
        self.slot_index = None
        if slot_fd is not None:
            self._release_fd(slot_fd)
        if seam_fd is not None:
            self._release_fd(seam_fd)

    def occupancy(self) -> SlotOccupancy:
        """`k/N` as seen from here — INCLUSIVE of this holder's own slot.

        Inclusive because `flock` conflicts across two open file descriptions in one
        process (measured, errno 35), so the probe below genuinely cannot acquire the
        slot this object holds and reports it held. That is the honest reading and it is
        the one `MIGRATION.md` § 11.4 pins: `slots_held=` counts every held slot on the
        lane at the instant of the reading, this job's own included when it holds one.
        """
        return probe_slots(self.base, self.ceiling)

    def __enter__(self) -> "SeamSlotSemaphore":
        return self.acquire()

    def __exit__(self, *exc: object) -> None:
        self.release()


def lane_is_free(path: Path | None = None) -> bool:
    """ADVISORY. True if the lane was free at the instant this was called.

    This is a PROBE, not a reservation, and nothing may treat it as one: it acquires
    and immediately releases, so between its answer and any use of that answer the
    lane can change hands. It exists so `available()` can tell the truth in both
    directions at workflow-load time. The GUARANTEE is `SerialLaneLock` held across
    the `subprocess.run` call, and there is exactly one such call site.
    """
    lock = SerialLaneLock(path)
    try:
        lock.acquire()
    except LaneBusy:
        return False
    lock.release()
    return True


# ---------------------------------------------------------------------------
# 2 — the run log (the liveness surface)
# ---------------------------------------------------------------------------
def is_terminal_marker(marker: str) -> bool:
    """Does COLUMN 3 mean "nothing is executing for this job"?

    `rc=N` by prefix (the proven runner's spelling, any exit code) plus the named
    terminal vocabulary. Anything else — including a marker this build has never
    seen — is NON-terminal, which is the fail-closed direction: an unrecognised
    state reads as "do not fire", never as "idle".
    """
    marker = marker.strip()
    if marker.startswith("rc="):
        return True
    return marker in TERMINAL_MARKERS


def _clean(value: object) -> str:
    """No field may contain a tab or a newline; the TSV is the contract."""
    text = "" if value is None else str(value)
    return text.replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


class RunLog:
    """`_run-log.tsv` — the lane's human-readable liveness surface.

    FORMAT CONTRACT (additive; columns 1-4 are the proven runner's, unmoved):

        1  ts_utc      2026-08-24T14:03:40Z
        2  job_id      30-ma_video_companion
        3  marker      rc=0 | SKIP-EXISTS | ENQUEUED | START | FALLBACK-CLAUDE | ...
        4  detail      free-form `k=v k=v`, as before
        5  curator     curator=<named Claude agent>          [U-4 R-B, enqueue-time]
        6  event       event=enqueue|start|finish

    `tail -1` still shows the marker; `tail -1 | cut -f3` still extracts it; every
    reader that counted on columns 1-4 keeps working. Rows written by the proven
    `run_p2_serial.sh` have four columns and are read here without complaint —
    `curator_of` returns None for them, which is "unknown", not "empty".
    """

    def __init__(self, path: Path):
        self.path = Path(path)

    def append(
        self,
        *,
        job_id: str,
        marker: str,
        detail: str = "-",
        curator: str = "",
        event: str = "",
    ) -> str:
        # A CLOSED MARKER VOCABULARY. Column 3 is the whole liveness contract, and a
        # marker nobody enumerated would be read as non-terminal by `is_terminal_marker`
        # (correct, and fail-closed) while every HUMAN reading `tail -1` would take the
        # word at face value. Refused at write time, where it is cheap.
        if not is_terminal_marker(marker) and _clean(marker) not in BUSY_MARKERS:
            raise ValueError(
                f"lane run-log: marker {marker!r} is in neither TERMINAL_MARKERS nor "
                f"BUSY_MARKERS (known: {sorted(TERMINAL_MARKERS | BUSY_MARKERS)}, plus "
                "`rc=<N>` by prefix). Column 3 is the pre-fire check of record; a state "
                "nobody enumerated cannot be written into it."
            )
        if event == "enqueue" and not _clean(curator):
            # Defence in depth. `JobQueue.enqueue` refuses first and refuses louder;
            # this exists so that no OTHER caller can write a curator-less enqueue row
            # into the surface the governance criterion is queried from.
            raise ValueError(
                "U-4 R-B: an enqueue row with no curator may not be written. Every "
                "vendor-lane job names the Claude agent who owns its output, AT ENQUEUE "
                "TIME — a curator recorded at close is one chosen after seeing the "
                "output, which is not a governance control."
            )
        row = "\t".join([
            utcnow(),
            _clean(job_id),
            _clean(marker),
            _clean(detail) or "-",
            f"curator={_clean(curator)}" if curator else "curator=",
            f"event={_clean(event)}" if event else "event=",
        ])
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Append mode + one write() of a single line: on a local filesystem this is
        # the write the proven runner's `>>` performs, and a crash mid-drain leaves
        # whole rows rather than a half-row nobody can parse.
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(row + "\n")
        return row

    def rows(self) -> Iterator[list[str]]:
        if not self.path.exists():
            return
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                yield line.split("\t")

    def last_row(self) -> list[str] | None:
        last = None
        for row in self.rows():
            last = row
        return last

    def is_idle(self) -> bool:
        """The pre-fire check of record: *last row terminal*.

        An ABSENT or EMPTY log is idle — nothing has ever run. A row with fewer than
        three columns is NOT idle: it is a row this format cannot read, and an
        unreadable liveness surface must not answer "safe".
        """
        row = self.last_row()
        if row is None:
            return True
        if len(row) < 3:
            return False
        return is_terminal_marker(row[2])

    def terminal_job_ids(self) -> set[str]:
        """Jobs whose last row is terminal — the idempotency ledger.

        Last row WINS: a job that went `ENQUEUED -> START -> rc=0` is done, and one
        that went `... -> rc=0` and was then re-enqueued is pending again.
        """
        state: dict[str, bool] = {}
        for row in self.rows():
            if len(row) < 3:
                continue
            state[row[1]] = is_terminal_marker(row[2])
        return {job for job, terminal in state.items() if terminal}

    def curator_of(self, job_id: str) -> str | None:
        """The curator named on ANY row for this job, or None if no row names one.

        None means UNKNOWN (a four-column row from the proven runner). It does not
        mean empty, and a query counting governance leaks must not conflate them.
        """
        for row in self.rows():
            if len(row) >= 5 and row[1] == job_id and row[4].startswith("curator="):
                value = row[4][len("curator="):].strip()
                if value:
                    return value
        return None

    def curator_at_enqueue(self, job_id: str) -> str | None:
        """The curator named on the ENQUEUE row specifically — U-4 R-B's actual claim.

        Distinct from `curator_of` on purpose. R-B is not "a curator appears
        somewhere in this job's rows"; it is "a curator was named BEFORE the job
        fired". A query that accepts a name from a finish row would report a lane with
        zero governance leaks while every name on it was chosen after the output
        existed, which is the exact substitution the amendment was written to close.
        """
        for row in self.rows():
            if len(row) >= 6 and row[1] == job_id and row[5] == "event=enqueue":
                value = row[4][len("curator="):].strip() if row[4].startswith("curator=") else ""
                return value or None
        return None


# ---------------------------------------------------------------------------
# 3 — telemetry (U-1(a) from birth, WITHOUT freezing U-1's schema)
# ---------------------------------------------------------------------------
@dataclass
class Telemetry:
    """Append-only JSONL, one event per line. A recorder READS this; nothing writes back.

    THE LAW, applied pre-emptively: any view over this data is read-only, zero
    authority, and never in the data path. The queue is the data path; a board is a
    projection. Nothing in this module reads lane state back out of the telemetry
    file in order to decide anything — `_run-log.tsv` is the state surface and the
    JSONL is the record.

    DISCIPLINE #73, applied pre-emptively: no event here carries a work-state claim
    sourced from a dispatch `**Status:**` header. That field is measured-defective
    (99 of 197 dispatch files carry none; 14 of the 31 reading open/pending are
    contradicted by a completion record in the same file), so work state is DERIVED
    from a completion record plus git and is never asserted by a field — and it is
    certainly never re-emitted by a lane that has no business knowing it. This module
    does not read `dispatches/` at all, and `tests/test_lane.py` asserts that
    mechanically rather than leaving it to this paragraph.
    """

    path: Path

    def emit(self, event: str, **facts: Any) -> dict[str, Any]:
        """Write one event. Absent facts are OMITTED, never zero-filled.

        Anything a caller observes that the named minimum does not cover goes in
        `passthrough` — a permissive object, present on every record, so that a
        later normaliser has somewhere to have found the fact it needs. Consumers
        must not depend on this top-level shape; that is what `schema_version` is
        for, and the axes are Matt's F-1…F-8 to rule.
        """
        record: dict[str, Any] = {
            "schema_version": TELEMETRY_SCHEMA_VERSION,
            "event": event,
            "ts_utc": utcnow(),
            "ts_epoch": time.time(),
        }
        passthrough = facts.pop("passthrough", None) or {}
        for key, value in facts.items():
            if value is not None:
                record[key] = value
        record["passthrough"] = passthrough
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=False, default=str) + "\n")
        return record

    def events(self) -> list[dict[str, Any]]:
        """Read back. Used by tests and by an operator; never by a decision here."""
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out
