"""The cross-session busy check — three legs, unioned fail-closed, EMITTING NOTHING.

    "Is a vendor agent in use RIGHT NOW?" is a DERIVATION over three independent
    state surfaces — the kernel lock, the process table, and the run-log — unioned
    fail-closed, readable by any session on this host without acquiring anything
    and without writing anything.

Lane spec § 3 (`gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md`),
ratified by jack-ryan 2026-08-24 with Amendments A–I. This module is D-1 + D-2's
derivation; `cli.py` is its command surface.

THE INCIDENT THIS ABOLISHES
---------------------------
*Uptime is not utilization.* The Codex lane sat healthy, authenticated and idle —
and unusable, because nobody could prove it free. A lane held by vibes is the
failure mode this file exists to end.

WHY THREE LEGS AND NOT ONE
--------------------------
Each leg covers a blind spot the others have, and the blind spots are not
hypothetical — each one is a way the lane has actually been mis-read:

  * **Leg 1, the kernel lock.** Sees every lock-taking invocation with zero
    staleness by construction (`flock` binds to the open file description; the
    kernel drops it when the last holder exits, including on SIGKILL). CANNOT see a
    `codex exec` that never took the lock.
  * **Leg 2, the process table.** The ONLY leg that sees an out-of-band invocation —
    a hand-fired script, an agent exercising the CLI in a live session, Matt in his
    own terminal. This is the motivating incident and the one leg the pre-existing
    build did not have. CANNOT see another machine.
  * **Leg 3, the run-log's last row.** Sees an in-flight queue job (`START` with no
    finish row) and the enqueued backlog. CANNOT see a hand-fire that wrote no row,
    which is why leg 3 alone reports idle precisely when the lane is hottest.

**THE UNION IS OVER EXECUTION OCCUPANCY ONLY (Amendment A, BINDING).** A live lock
hold, a live vendor `exec`, an in-flight `START`-without-finish. `ENQUEUED` is NOT
occupancy: a P-9 HELD job is a *deliberately parked* job, and counting it busy would
wedge the lane's answer forever — uptime-is-not-utilization re-created through the
instrument built to abolish it. Backlog answers `queue-pending`, which counts OPEN in
`safe_to_fire`, and the reading is *"free, and the next drain will take it."*

**BLAST RADIUS IS PER-VENDOR, NEVER PER-HOST (Amendment B, BINDING).** Leg 2 cannot
cheaply attribute a raw out-of-band process to a specific credential home, so an
unattributable hit counts busy against every lane OF THAT VENDOR. It does not cross
vendors: a `codex exec` cannot spend the xAI credential, and closing the Grok lane on
a Codex phantom would drive the § 10.3 selection law past spillover into the branch
that spends Claude. `test_lane_status.py` asserts the non-crossing mechanically.

THE LAW: THIS MODULE WRITES NOTHING
-----------------------------------
A probe that writes converts a question into a side effect and walks the checker into
the data path. Two consequences are structural here rather than aspirational:

  * `lane_is_free()` opens its lock file with `O_CREAT`. So leg 1 is only asked when
    the lock file ALREADY EXISTS — a lock file that does not exist cannot be held, and
    that answer is free. Asking anyway would make a read-only status call CREATE a
    file that outlives it.
  * No telemetry event, no run-log row, no `AUTH-BLOCKED.md`. Nothing in this module
    calls `RunLog.append` or `Telemetry.emit`, and a test asserts that over the source.

Flow is one-directional: state surfaces -> (this check reads · the queue records) ->
a recorder derives history -> a board renders. **Liveness-NOW is never answered from
telemetry or from a board** — those are record and view.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

from .lane import default_lock_path, is_terminal_marker, lane_is_free

# ---------------------------------------------------------------------------
# The answer vocabulary (lane spec § 3, + one declared extension)
# ---------------------------------------------------------------------------
#: The lane is free and nothing is queued behind it.
STATE_OPEN = "open"
#: The lane is FREE and an `ENQUEUED` backlog exists. Amendment A: NOT busy.
STATE_QUEUE_PENDING = "queue-pending"
#: Leg 1 — a lock-taking invocation holds the lane. `ps` names the holder.
STATE_BUSY_LOCK = "busy-lock"
#: Leg 2 — a vendor `exec` the lock never saw. The PID is named in the reason.
STATE_BUSY_OUT_OF_BAND = "busy-out-of-band"
#: **DECLARED EXTENSION, not in § 3's six.** A leg was UNREACHABLE and no reachable
#: leg reported occupancy. § 3's vocabulary assumes all three legs answer; when one
#: does not, reporting `open` would be false-open, which is the single direction G-2
#: ruled against. The spelling is drax's, taken deliberately: the fleet board's
#: degraded card (`flight/bin/flight_report`) already renders this label, and two
#: instruments answering one question in two vocabularies is the folklore this check
#: was built to abolish.
STATE_BUSY_UNKNOWN = "busy-unknown"
#: Closed on a MATT-ONLY action. Not a job failure, never retried.
STATE_AUTH_EXPIRED = "auth-expired"
#: The vendor CLI cannot be reached from this process at all.
STATE_CLI_MISSING = "cli-missing"

#: **THE SAFE-TO-FIRE PREDICATE, BY STATE NAME.** Amendment H: consumers — the § 10.3
#: selection law and the router's question (3) included — bind to THIS, never to a
#: leg's raw reading and never to *"last run-log row terminal"*. Pinned by literal in
#: `tests/test_lane_status.py` and in `MIGRATION.md`, because a caller re-deriving it
#: is a caller who will re-derive it differently.
SAFE_TO_FIRE_STATES = frozenset({STATE_OPEN, STATE_QUEUE_PENDING})

#: **CLOSED** for the § 10.3 selection law: the lane cannot take the work AT ALL, so
#: step 4's Claude branch is reachable. Distinct from OCCUPIED, where the lane exists
#: and works and the correct move is to enqueue behind it.
CLOSED_STATES = frozenset({STATE_AUTH_EXPIRED, STATE_CLI_MISSING})

#: **OCCUPIED**: the lane works, something is executing on it. Enqueue.
OCCUPIED_STATES = frozenset({STATE_BUSY_LOCK, STATE_BUSY_OUT_OF_BAND, STATE_BUSY_UNKNOWN})

#: Per-state exit codes, PINNED. `0` is the only value the spec imposes (open =
#: safe-to-fire); the rest are chosen here and pinned in `MIGRATION.md` so that no
#: consumer discovers them by experiment. Banded on purpose — 0/1x = fire, 2x =
#: occupied, 3x = closed — so a shell caller that only wants the band can divide.
#:
#: Amendment A required `open` and `queue-pending` to be SEPARATELY IDENTIFIABLE by
#: exit code, and the spec required `0` = safe-to-fire. Those pull opposite ways, and
#: the resolution is two questions instead of one collapsed answer: the DEFAULT exit
#: code is per-state (so the two are distinguishable), and `--safe-to-fire` collapses
#: to 0/1 for the caller whose question is only *"may I fire?"*.
EXIT_CODES: dict[str, int] = {
    STATE_OPEN: 0,
    STATE_QUEUE_PENDING: 10,
    STATE_BUSY_LOCK: 20,
    STATE_BUSY_OUT_OF_BAND: 21,
    STATE_BUSY_UNKNOWN: 22,
    STATE_AUTH_EXPIRED: 30,
    STATE_CLI_MISSING: 31,
}

#: Fail-closed precedence when legs disagree — and disagreement is COVERAGE, not
#: contradiction (G-1). A running process is a FACT and outranks a credential state;
#: ambiguity outranks `open`, always. Identical ordering to the fleet board's
#: `STATE_PRECEDENCE`, deliberately: one question, one answer, two renderers.
STATE_PRECEDENCE: tuple[str, ...] = (
    STATE_BUSY_LOCK,
    STATE_BUSY_OUT_OF_BAND,
    STATE_BUSY_UNKNOWN,
    STATE_AUTH_EXPIRED,
    STATE_CLI_MISSING,
    STATE_QUEUE_PENDING,
    STATE_OPEN,
)


def safe_to_fire(state: str) -> bool:
    """THE predicate. One name, one place, bound by every consumer (Amendment H)."""
    return state in SAFE_TO_FIRE_STATES


def exit_code_for(state: str) -> int:
    """An UNKNOWN state exits `busy-unknown`, not `open`. Fail-closed at the edge too."""
    return EXIT_CODES.get(state, EXIT_CODES[STATE_BUSY_UNKNOWN])


# ---------------------------------------------------------------------------
# Per-vendor lane configuration
# ---------------------------------------------------------------------------
#: Repository root, derived from this file's own location rather than from a cwd a
#: caller happens to be in — the check must answer the same thing from any directory.
REPO_ROOT = Path(__file__).resolve().parents[2]

#: The Grok lane's queue root of record (D-8). Its `_run-log.tsv` is born WITH the
#: curator column and with enqueue-time rows: this lane has no rows-at-close era,
#: because it has no hand-fire era (P-10 from birth).
GROK_LANE_ROOT = REPO_ROOT / "agentic_orchestration" / "lanes" / "grok"

#: The Codex lane's run-logs, in the order they were created. The VFX dossier log is
#: the PROVEN runner's — 30 four-column rows written at CLOSE — and it is read here
#: without complaint because columns 1-4 never moved. The queue root is where the
#: durable queue writes.
CODEX_RUNLOGS = (
    REPO_ROOT / "agentic_orchestration" / "research" / "vfx-p2-dossiers" / "usage" / "_run-log.tsv",
    REPO_ROOT / "agentic_orchestration" / "lanes" / "codex" / "_run-log.tsv",
)


@dataclass(frozen=True)
class LaneConfig:
    """One vendor lane's state surfaces, named so the check can find all three.

    `exec_re` and `tui_re` are ANCHORED AT ARGV[0]: the process's own executable must
    be the vendor CLI. An unanchored match convicts any shell whose command line
    merely MENTIONS the vendor — including a `grep codex` and including this check's
    own invocation — and a busy answer nobody can act on is noise, not safety. The
    false-busy bargain (G-2) buys safety with delay; a pattern that matches everything
    buys nothing with delay, which is outside the bargain.

    `extra_busy_re` is UNANCHORED on purpose for Grok: a shared-leader backend is a
    concurrency door around the serial lock (§ 9.3), and it counts busy wherever the
    socket appears in a command line.
    """

    key: str
    vendor: str
    exec_re: re.Pattern[str]
    tui_re: re.Pattern[str]
    extra_busy_re: re.Pattern[str] | None
    runlogs: tuple[Path, ...]
    serial_law_grounding: str


LANES: dict[str, LaneConfig] = {
    "codex": LaneConfig(
        key="codex",
        vendor="codex",
        exec_re=re.compile(r"^(?:\S*/)?codex\b.*\bexec\b"),
        tui_re=re.compile(r"^(?:\S*/)?codex\b"),
        extra_busy_re=None,
        runlogs=CODEX_RUNLOGS,
        serial_law_grounding=(
            "VERIFIED VENDOR PRECONDITION — OpenAI CI/CD auth requires one machine or a "
            "serialized job stream. This is a LAW, not our preference."
        ),
    ),
    "grok": LaneConfig(
        key="grok",
        vendor="grok",
        # `-p` (single-turn headless) or the `agent` subcommand. Both spend the
        # credential; both are job streams in the sense the serial policy is about.
        exec_re=re.compile(r"^(?:\S*/)?grok\b.*(?:\s-p\b|\s--single\b|\s--prompt-file\b|\bagent\b)"),
        tui_re=re.compile(r"^(?:\S*/)?grok\b"),
        extra_busy_re=re.compile(r"leader\.sock"),
        runlogs=(GROK_LANE_ROOT / "_run-log.tsv",),
        serial_law_grounding=(
            "SERIAL BY CHOICE — no equivalent xAI precondition has been verified, so this "
            "lane is serialised as a POLICY (G-2's false-busy ruling applied at the policy "
            "level), not as a vendor law. Loosening requires the evidence NAMED, by "
            "amendment to the lane spec. Do not defend this as if it were the Codex law."
        ),
    ),
}

#: The deterministic vendor order of § 10.3(2). NEVER random: Codex has banked
#: statistics (30/30 at the pin), Grok has zero rows, so every early Grok job is ALSO
#: a banking measurement. Re-ranking is a U-5 evidence event, not a preference.
VENDOR_ORDER: tuple[str, ...] = ("codex", "grok")


# ---------------------------------------------------------------------------
# Leg 2 — the process table (D-1)
# ---------------------------------------------------------------------------
def scan_process_table(
    runner: Callable[[list[str]], "subprocess.CompletedProcess[str]"] | None = None,
) -> list[tuple[int, str]]:
    """`ps -axo pid=,args=` -> [(pid, argv-string)]. Read-only; raises if unreachable.

    RAISES rather than returning `[]` when `ps` fails. An empty list and an
    unanswerable question are different facts, and conflating them makes leg 2 report
    "nothing running" at exactly the moment it cannot see. The caller turns the raise
    into `busy-unknown`, which is the fail-closed direction.

    Our OWN pid is excluded — an instrument must not convict itself of being the thing
    it watches.
    """
    argv = ["ps", "-axo", "pid=,args="]
    run = runner or (lambda a: subprocess.run(
        a, capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL,
    ))
    proc = run(argv)
    if proc.returncode != 0:
        raise RuntimeError(
            f"`{' '.join(argv)}` exited {proc.returncode}: "
            f"{(proc.stderr or '').strip()[:200] or 'no stderr'}"
        )
    me = os.getpid()
    out: list[tuple[int, str]] = []
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line:
            continue
        pid_text, _, args = line.partition(" ")
        if not pid_text.isdigit():
            continue
        pid = int(pid_text)
        if pid == me:
            continue
        out.append((pid, args.strip()))
    return out


@dataclass
class ProcessFindings:
    """What leg 2 saw FOR ONE VENDOR. Attribution never crosses vendors (Amendment B)."""

    occupancy: list[tuple[int, str]] = field(default_factory=list)
    interactive: list[tuple[int, str]] = field(default_factory=list)
    leader: list[tuple[int, str]] = field(default_factory=list)


def classify_processes(cfg: LaneConfig, procs: Iterable[tuple[int, str]]) -> ProcessFindings:
    """Sort one vendor's processes into occupancy / advisory / leader-socket.

    The order of the tests is the ruling: an `exec`-shaped argv is OCCUPANCY; a vendor
    CLI without the headless argv shape is the INTERACTIVE TUI, which Matt ruled
    ADVISE-ONLY 2026-08-24 (Q62, verbatim: *"I'm not worried about TUI. I'll simply
    check the fleet-board before ever engaging with the codex or grok TUI."*). The
    advisory is reported and does NOT gate; a drain firing while it is active writes
    the advisory token into its ledger note, so the choice is evidence-generating and
    flips to blocking only by amendment citing observed vendor friction.
    """
    found = ProcessFindings()
    for pid, args in procs:
        if cfg.exec_re.search(args):
            found.occupancy.append((pid, args))
        elif cfg.extra_busy_re is not None and cfg.extra_busy_re.search(args):
            found.leader.append((pid, args))
        elif cfg.tui_re.search(args):
            found.interactive.append((pid, args))
    return found


# ---------------------------------------------------------------------------
# Leg 3 — the run-log's last row
# ---------------------------------------------------------------------------
@dataclass
class RunLogReading:
    path: str
    present: bool
    rows: int = 0
    last_marker: str | None = None
    last_job: str | None = None
    executing: bool = False
    pending: int = 0


def read_runlog(path: Path) -> RunLogReading:
    """Leg 3, restricted to EXECUTION occupancy (Amendment A).

    `executing` is True only for a job whose LAST row is `START` or a marker nobody
    enumerated (fail-closed, G-2 — an unreadable liveness surface must not answer
    "safe"). `ENQUEUED` sets `pending` and NOT `executing`, which is the whole of
    Amendment A in two lines of code.

    An ABSENT log is not an error: it is "this queue has never run", which on a bare
    host is the truth. The check is SUBSTRATE and the queue is a consumer — a busy
    check that only worked once the queue was up would not have unblocked the crawl.
    """
    if not path.exists():
        return RunLogReading(path=str(path), present=False)
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    # LAST ROW WINS, per job. A job that went ENQUEUED -> START -> rc=0 is finished;
    # one that went rc=0 and was re-enqueued is pending again.
    last_by_job: dict[str, str] = {}
    for line in lines:
        row = line.split("\t")
        if len(row) < 3:
            # A row this format cannot read. It cannot be attributed to a job, and it
            # is not silently dropped either: it makes the whole reading fail-closed.
            last_by_job[f"_unreadable:{len(last_by_job)}"] = "_UNREADABLE"
            continue
        last_by_job[row[1]] = row[2].strip()
    executing = any(
        marker == "START" or (marker != "ENQUEUED" and not is_terminal_marker(marker))
        for marker in last_by_job.values()
    )
    pending = sum(1 for marker in last_by_job.values() if marker == "ENQUEUED")
    last_row = lines[-1].split("\t") if lines else []
    return RunLogReading(
        path=str(path),
        present=True,
        rows=len(lines),
        last_marker=last_row[2].strip() if len(last_row) > 2 else None,
        last_job=last_row[1] if len(last_row) > 1 else None,
        executing=executing,
        pending=pending,
    )


# ---------------------------------------------------------------------------
# The composite
# ---------------------------------------------------------------------------
@dataclass
class LaneStatus:
    """One lane's answer. The check reports WHICH state, never a bare bool."""

    lane: str
    vendor: str
    state: str
    reason: str
    advisories: list[str] = field(default_factory=list)
    unreachable: list[str] = field(default_factory=list)
    legs: dict[str, Any] = field(default_factory=dict)

    @property
    def safe_to_fire(self) -> bool:
        return safe_to_fire(self.state)

    @property
    def exit_code(self) -> int:
        return exit_code_for(self.state)

    def one_line(self) -> str:
        head = f"{self.lane:<6} {self.state:<18} {self.reason}"
        if self.advisories:
            head += "  |  " + "; ".join(self.advisories)
        return head

    def to_dict(self) -> dict[str, Any]:
        return {
            "lane": self.lane,
            "vendor": self.vendor,
            "state": self.state,
            "reason": self.reason,
            "safe_to_fire": self.safe_to_fire,
            "exit_code": self.exit_code,
            "advisories": list(self.advisories),
            "unreachable": list(self.unreachable),
            "legs": self.legs,
        }


def _auth_state(vendor: str, auth_probe: Callable[[], Any] | None) -> tuple[str, str]:
    """Auth health via the VENDOR'S OWN check of record, reused and never re-derived.

    The harness already owns the probe (`codex login status`, whose answer is on
    STDERR; `grok models`). Re-implementing it here would be a second derivation of
    one fact, and the two would drift on the first vendor wording change.
    """
    if auth_probe is not None:
        availability = auth_probe()
    elif vendor == "codex":
        from .harness.codex import CodexHarness

        availability = CodexHarness().check_auth()
    elif vendor == "grok":
        from .harness.grok import GrokHarness

        availability = GrokHarness().check_auth()
    else:
        return STATE_CLI_MISSING, f"no auth check of record is declared for vendor {vendor!r}"
    if availability.ok:
        return STATE_OPEN, availability.reason
    mapped = {
        "cli_missing": STATE_CLI_MISSING,
        "auth_expired": STATE_AUTH_EXPIRED,
        "auth_unknown": STATE_BUSY_UNKNOWN,
    }.get(availability.state, STATE_AUTH_EXPIRED)
    return mapped, availability.reason


def lane_status(
    lane: str,
    *,
    procs: Iterable[tuple[int, str]] | None = None,
    procs_error: str | None = None,
    auth_probe: Callable[[], Any] | None = None,
    lock_path: Path | None = None,
    extra_runlogs: Iterable[Path] = (),
    check_auth: bool = True,
) -> LaneStatus:
    """Answer one lane, fail-closed across whichever legs were reachable.

    `procs` is injected rather than scanned here so that the caller scans the process
    table ONCE for `--lane all` and so that a test can hand this function a fake table
    without a fake `ps`. `procs_error` carries an unreachable leg 2 in the same
    argument position, because "I could not look" must travel with the answer.
    """
    cfg = LANES[lane]
    signals: list[tuple[str, str]] = []
    advisories: list[str] = []
    unreachable: list[str] = []
    legs: dict[str, Any] = {}

    # -- leg 1: the kernel lock -------------------------------------------
    path = Path(lock_path) if lock_path is not None else default_lock_path(vendor=cfg.vendor)
    if not path.exists():
        # ANSWERED FREE WITHOUT OPENING ANYTHING. `lane_is_free` opens with `O_CREAT`;
        # asking it here would make a read-only status call create a file that
        # outlives the question. A lock file that does not exist cannot be held.
        legs["lock"] = {"path": str(path), "free": True, "probed": False,
                        "why": "no lock file exists — nothing has ever taken this lane"}
    else:
        free = lane_is_free(path)
        legs["lock"] = {"path": str(path), "free": free, "probed": True}
        if not free:
            signals.append((
                STATE_BUSY_LOCK,
                f"the kernel lock is HELD ({path.name}) — `ps` names the live holder; "
                "the kernel releases this lock when its last holder exits, so an "
                "occupied lock means an occupied lane",
            ))

    # -- leg 2: the process table -----------------------------------------
    if procs is None:
        unreachable.append(f"leg 2 (process table): {procs_error or 'not scanned'}")
        legs["processes"] = {"reachable": False, "error": procs_error}
    else:
        found = classify_processes(cfg, procs)
        legs["processes"] = {
            "reachable": True,
            "occupancy": [{"pid": p, "args": a[:200]} for p, a in found.occupancy],
            "leader": [{"pid": p, "args": a[:200]} for p, a in found.leader],
            "interactive": [{"pid": p, "args": a[:200]} for p, a in found.interactive],
        }
        for pid, args in found.occupancy:
            signals.append((
                STATE_BUSY_OUT_OF_BAND,
                f"PID {pid} is a live `{cfg.vendor}` invocation the lock did not see: "
                f"{args[:120]}",
            ))
        for pid, args in found.leader:
            signals.append((
                STATE_BUSY_OUT_OF_BAND,
                f"PID {pid} holds a shared-leader backend (`leader.sock`) — the "
                f"concurrency door the serial policy forbids: {args[:120]}",
            ))
        for pid, args in found.interactive:
            advisories.append(
                f"interactive-{cfg.vendor}-present (PID {pid}) — ADVISORY ONLY, "
                "NON-BLOCKING (Q62, Matt-ruled 2026-08-24). A drain firing while this "
                "is active writes the advisory token into its ledger note."
            )

    # -- leg 3: the run-logs ----------------------------------------------
    # DEDUPED BY RESOLVED PATH. A caller passing `--queue-dir lanes/grok` names the
    # same file the lane config already names, and reading it twice double-counted the
    # backlog — a lane with one held job reported "2 job(s) enqueued". Wrong in the
    # harmless direction here, but the same bug on the `executing` leg would have
    # doubled nothing and hidden nothing, so it is fixed at the source rather than at
    # the number that happened to show it.
    seen: set[str] = set()
    ordered: list[Path] = []
    for candidate in (*cfg.runlogs, *extra_runlogs):
        key = str(Path(candidate).expanduser().resolve())
        if key not in seen:
            seen.add(key)
            ordered.append(Path(candidate))
    readings = [read_runlog(p) for p in ordered]
    legs["runlogs"] = [r.__dict__ for r in readings]
    for reading in readings:
        if reading.executing:
            # `busy-out-of-band` rather than `busy-lock`, and the distinction is the
            # honest one: leg 1 answers for the lock, and if leg 1 said FREE while a
            # `START` row dangles, then whatever wrote that row is not holding the
            # lock. Two readings fit and both are non-terminal: a job genuinely
            # in flight (the lock leg will usually agree), or a drain that died
            # mid-job and left its row unanswered. Both resolve the same way — a
            # re-drain writes the finishing row — and neither is safe to fire past.
            signals.append((
                STATE_BUSY_OUT_OF_BAND,
                f"{reading.path}: job {reading.last_job!r} has a NON-TERMINAL last row "
                f"({reading.last_marker!r}) — started and never finished. Re-drain to "
                "answer the row; the lane is not free until something does",
            ))
    pending_total = sum(r.pending for r in readings)

    # -- auth --------------------------------------------------------------
    if check_auth:
        auth_state, auth_reason = _auth_state(cfg.vendor, auth_probe)
        legs["auth"] = {"state": auth_state, "reason": auth_reason[:300]}
        if auth_state != STATE_OPEN:
            signals.append((auth_state, auth_reason))
    else:
        legs["auth"] = {"state": "not-checked", "reason": "auth probe skipped by caller"}

    # -- the union, fail-closed -------------------------------------------
    if unreachable and not signals:
        # A leg we could not read, and nothing else reporting occupancy. Reporting
        # `open` here would be false-open, the one direction G-2 ruled against.
        return LaneStatus(
            lane=cfg.key, vendor=cfg.vendor, state=STATE_BUSY_UNKNOWN,
            reason="; ".join(unreachable) + " — reported ambiguous rather than open",
            advisories=advisories, unreachable=unreachable, legs=legs,
        )
    if signals:
        rank = {state: i for i, state in enumerate(STATE_PRECEDENCE)}
        state, reason = min(signals, key=lambda s: rank.get(s[0], 0))
        return LaneStatus(
            lane=cfg.key, vendor=cfg.vendor, state=state, reason=reason,
            advisories=advisories, unreachable=unreachable, legs=legs,
        )
    if pending_total:
        return LaneStatus(
            lane=cfg.key, vendor=cfg.vendor, state=STATE_QUEUE_PENDING,
            reason=(
                f"lane FREE; {pending_total} job(s) enqueued and not yet drained. A "
                "backlog is not occupancy — the next drain will take the lane. This "
                "state is SAFE TO FIRE (Amendment A) and counts OPEN for the "
                "selection law (Amendment H)."
            ),
            advisories=advisories, unreachable=unreachable, legs=legs,
        )
    return LaneStatus(
        lane=cfg.key, vendor=cfg.vendor, state=STATE_OPEN,
        reason="lane free on all three legs; auth healthy",
        advisories=advisories, unreachable=unreachable, legs=legs,
    )


def all_lane_status(
    lanes: Iterable[str] = VENDOR_ORDER,
    *,
    auth_probes: dict[str, Callable[[], Any]] | None = None,
    procs: Iterable[tuple[int, str]] | None = None,
    check_auth: bool = True,
) -> list[LaneStatus]:
    """Every named lane, from ONE process-table scan.

    One scan, not one per lane: two scans a millisecond apart can disagree, and a
    composite assembled from disagreeing snapshots is a composite of two moments.
    """
    scanned: list[tuple[int, str]] | None
    error: str | None = None
    if procs is not None:
        scanned = list(procs)
    else:
        try:
            scanned = scan_process_table()
        except Exception as exc:  # noqa: BLE001 — any failure is "could not look"
            scanned, error = None, f"{type(exc).__name__}: {exc}"
    probes = auth_probes or {}
    return [
        lane_status(
            lane, procs=scanned, procs_error=error,
            auth_probe=probes.get(lane), check_auth=check_auth,
        )
        for lane in lanes
    ]


def select_lane(statuses: Iterable[LaneStatus]) -> LaneStatus | None:
    """§ 10.3's selection law, mechanised: the FIRST safe-to-fire lane in vendor order.

    Matt's ruling, verbatim: *"once a vendor lane is found/mapped then codex/grok
    should be first if the vendor is open, and only claude if both vendors are not
    open for a scoped vendor lane."*

    Returns None when no vendor lane is safe to fire — which is the dispatcher's cue
    to ENQUEUE (the default, cost-preserving, P-9 named-condition hold) or, only under
    the R-A ledger note, to fire Claude. This function does not make that call: it
    answers which vendor lane is available, and the R-A override is a human decision
    that must leave a ledger note behind it.
    """
    ranked = {vendor: i for i, vendor in enumerate(VENDOR_ORDER)}
    for status in sorted(statuses, key=lambda s: ranked.get(s.lane, len(ranked))):
        if status.safe_to_fire:
            return status
    return None


def shell_fallback_doc(lane: str = "codex") -> str:
    """The pure-shell degraded fallback, for a session with no Python environment.

    Documented as a STRING the CLI can print, so the fallback and the real check
    cannot drift into two different recipes living in two different files.
    """
    cfg = LANES[lane]
    # ONE `tail` PER LOG. `tail -1 a b` prints `==> a <==` banners and would feed
    # `cut -f3` a header line, so a two-log lane would answer with a marker that is not
    # a marker. Measured on this host rather than assumed from the flag's shape.
    legs3 = "\n".join(
        f"[ -f {p} ] && tail -1 {p} | cut -f3" for p in cfg.runlogs
    )
    return (
        f"# degraded fallback for the {cfg.key} lane — legs 2 and 3 only, no lock probe\n"
        f"ps -axo pid=,args= | grep -E '{cfg.exec_re.pattern}'   # leg 2: occupancy\n"
        f"{legs3}   # leg 3: last marker, per run-log\n"
        "# leg 3 reads: rc=<N>|SKIP-EXISTS|FALLBACK-CLAUDE|AUTH-BLOCKED|ENQUEUE-REFUSED\n"
        "#              = terminal (nothing executing);  START = executing;\n"
        "#              ENQUEUED = queue-pending, which is SAFE TO FIRE, not busy.\n"
        f"{'codex login status' if cfg.vendor == 'codex' else '~/.grok/bin/grok models'}"
        "                    # auth health\n"
        "# This fallback CANNOT see leg 1 (the kernel lock). It is strictly weaker than\n"
        "# `factory lane` and it says so; use it only where python is unavailable.\n"
    )


def which_cli(vendor: str) -> str | None:
    """Where the vendor CLI actually is. Grok is NOT on PATH; codex is."""
    if vendor == "grok":
        from .harness.grok import resolve_grok_binary

        found = resolve_grok_binary()
        return str(found) if found else None
    return shutil.which(vendor)
