"""Vendor-lane primitives — THE SERIAL LAW, made structural.

    ONE `codex exec` at a time. One `auth.json`, one job stream.

This is an OpenAI CI/CD-auth precondition ("one machine or serialized job stream"),
not a preference, and this module exists so that violating it is not something a
caller can do by forgetting something.

Three surfaces live here, in the order they matter:

1. `SerialLaneLock` — the mutual exclusion. Held at the `codex exec` INVOCATION
   SITE, never merely at a queue-process boundary.
2. `RunLog` — the lane's liveness surface, `_run-log.tsv`. The pre-fire check of
   record is *"last row terminal"*, answerable by `tail -1`, and this module
   generalises the format ADDITIVELY so that check keeps working.
3. `Telemetry` — append-only JSONL, one event per line, emitted from birth.

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
