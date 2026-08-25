"""D-9 — AGENT-LEVEL SEAM CUSTODY. The second axis, and it EMITS NOTHING when asked.

    "Is a sub-agent already mid-flight in this seam?" is a DERIVATION over two
    independent surfaces — an append-only ledger of past events, and the holder
    session's own liveness in the kernel's process table — readable by any dispatcher
    on this host without writing anything.

Lane spec § 11 (`gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md`),
ratified by jack-ryan 2026-08-24 with Amendments **K** (atomic claim) and **L** (a claim
names the condition that ends it). This module is D-9's derivation and its three write
verbs; `cli.py` is their command surface.

THE INCIDENT THIS ABOLISHES
---------------------------
The vendor lane's lock serialises **vendor invocations**. It does not serialise
**agents**. On the day the busy check shipped, a RUN-CONDUCTOR session dispatched a
star-lord sub-agent to build the Grok lane; twenty-eight minutes later knight-rider —
whose knowledge was true when formed and false by mtime — dispatched a second star-lord
sub-agent for the same build. Neither dispatcher could see the other. KR stood his down.
The lane lock did its job perfectly and was never the problem.

Two agents colliding is duplicated work, contended files, and a corrupted verification
run. This module is Matt's original question — *is an agent in use, across all
sessions?* — asked one level up from the CLI.

WHY TWO LEGS
------------
  * **Leg 1, the ledger.** `last CLAIM without RELEASE, per seam`. Sees every dispatch
    that wrote a row. CANNOT see a spawn nobody recorded, and cannot tell a live holder
    from a crashed one.
  * **Leg 2, holder liveness.** Sessions ARE host processes, so `ps` is the kernel's
    answer and nobody writes it — the same grounding `flock` has, applied one level up.
    Sees a holder that died mid-flight. CANNOT see anything on another machine.

**A CLAIM ROW IS AN EVENT, NOT A STATUS (#73).** *At time T, dispatcher D spawned into
seam S* is a statement about the past, and a past event cannot become false by the
passage of time — which is precisely the defect a status header has and the founding
incident was made of. Occupancy is never read off a row; it is derived, every time.

STALE IS NOT FREE, AND THERE IS NO TTL — EVER
---------------------------------------------
A CLAIM whose holder is dead is **STALE**, and clearing it takes an explicit `override`
with a note. It does not auto-expire, because a TTL is a timeout-based lock break
wearing a different word: it would silently free a claim whose holder is alive and
mid-flight, which is the FALSE-OPEN direction G-2 forbids. Loud and manual beats quiet
and automatic when the quiet failure spends a seam.

WHAT THE LEDGER BUYS, STATED HONESTLY (AMENDMENT K)
---------------------------------------------------
In the hand-append era the ledger buys **VISIBILITY, NOT MUTUAL EXCLUSION**, and the
exclusion is a dispatcher DISCIPLINE resting on it. Visibility alone would have stopped
the founding incident — KR would have seen the row and stood down twenty-eight minutes
earlier, without a conversation — and that is a real and sufficient win. What must not
happen is this axis spending `flock`'s authority on a mechanism that does not have it.

`claim()` **does** have it: check-and-append happens under an `flock` on the ledger file
itself, reusing `lane.SerialLaneLock`. Two dispatchers can no longer both read *free*
and both append.

**The one difference from the vendor lane, and why it is not a lock break.** The vendor
lock NEVER waits: it is held across a model call, so waiting on it is unbounded. The
ledger lock is held across a read and one appended line of a small TSV — microseconds,
never a spawn, never a subprocess — so its wait is bounded BY CONSTRUCTION. `claim()`
retries for a bounded budget and then REFUSES; it never breaks the lock and never
blocks forever.

THE LAW: `custody_check()` WRITES NOTHING
-----------------------------------------
Same discipline as `factory lane`, for the same reason. Structurally:

  * the ledger is read with `read_text` and only when it EXISTS. Asking does not create
    it — the `O_CREAT` trap `lane_status` already met at leg 1.
  * `check` never takes the ledger lock. Taking it would create the file, and it would
    make a question contend with a write.
  * `ps` is not run at all when no seam has an open claim: a claim nobody made cannot be
    held by anybody, and that answer is free.
  * no telemetry, no run-log row. `test_custody.py` asserts it behaviourally AND over
    the call graph reachable from `custody_check`.
"""

from __future__ import annotations

import re
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence

from .lane import LaneBusy, SerialLaneLock

# ---------------------------------------------------------------------------
# The ledger's shape
# ---------------------------------------------------------------------------
#: The 6-column format family, in order. The ledger is read POSITIONALLY, so this
#: tuple is the whole schema: a reordered column silently re-reads every historical
#: row (holders become events, intents become holders) and nothing about the file
#: would look wrong. Hand-appended by humans in the interim era, which is exactly why
#: the column count is asserted per row rather than assumed.
LEDGER_COLUMNS: tuple[str, ...] = ("ts", "seam", "holder", "event", "intent", "detail")

#: The events a ledger row may carry. A CLOSED accept vocabulary: ADDITION is the
#: fail-open direction, because a new event name that `open_claims` does not know
#: falls through the CLAIM/RELEASE fold and a seam's occupancy is then decided by an
#: event nobody adjudicated. Anything outside this set reds the row as MALFORMED.
CUSTODY_EVENTS: frozenset[str] = frozenset({"CLAIM", "RELEASE", "OVERRIDE"})

EVENT_CLAIM = "CLAIM"
EVENT_RELEASE = "RELEASE"
EVENT_OVERRIDE = "OVERRIDE"

#: The ledger of record. A Path, resolved from this file's own location rather than
#: from a cwd, so the answer does not depend on where the dispatcher happened to be.
DEFAULT_LEDGER = Path(__file__).resolve().parents[2] / "agentic_orchestration" / "lanes" / "agents" / "_custody.tsv"

# ---------------------------------------------------------------------------
# The answer vocabulary (§ 11.2, banded like § 3)
# ---------------------------------------------------------------------------
#: No open CLAIM. Nobody is mid-flight here; this is the ONLY safe-to-spawn answer.
SEAM_FREE = "free"
#: An open CLAIM whose holder session is ALIVE. Do not spawn — coordinate, wait, or
#: escalate. Standing down is the honourable path and gets a ledger row, not a shrug.
SEAM_HELD = "held"
#: An open CLAIM whose holder is DEAD. **NOT free.** Clearing it takes `override` with
#: a note; there is no TTL and there will not be one.
SEAM_STALE = "stale"
#: Leg 2 could not be read, or the holder id names no PID to read it about. Ambiguity
#: outranks every other answer, exactly as `busy-unknown` does at the vendor lane: a
#: seam whose liveness could not be determined rendering `free` is the false-open
#: direction, and false-open is how a second sub-agent gets spawned into a live build.
SEAM_UNKNOWN = "custody-unknown"

#: The whole vocabulary. The three dispositions below PARTITION it, and a test asserts
#: that, so a state added to one and not the other reds a row instead of falling out of
#: the denominator.
CUSTODY_STATES: frozenset[str] = frozenset({SEAM_FREE, SEAM_HELD, SEAM_STALE, SEAM_UNKNOWN})

#: **THE PREDICATE, BY STATE NAME.** § 11.3's rule — *occupied seam → DO NOT SPAWN* —
#: is this set and nothing else. Named separately from the vendor lane's
#: `SAFE_TO_FIRE_STATES` on purpose: these are two different questions (may I spend this
#: CREDENTIAL / may I spawn into this SEAM), and one name for two questions is how a
#: consumer binds to the wrong one. Amendment J is what happens when a predicate has two
#: derivations; a shared name for two predicates is the same defect wearing the opposite
#: mask.
SAFE_TO_SPAWN_STATES: frozenset[str] = frozenset({SEAM_FREE})

#: OCCUPIED — someone or something is mid-flight, or we cannot prove otherwise. Every
#: member is a DO-NOT-SPAWN answer; they differ in what CLEARS them, which is why they
#: are three states and not one. `held` clears by the holder finishing; `stale` clears
#: by an override with a note; `custody-unknown` clears by making leg 2 answerable.
OCCUPIED_SEAM_STATES: frozenset[str] = frozenset({SEAM_HELD, SEAM_STALE, SEAM_UNKNOWN})

#: Per-state exit codes, BANDED exactly like § 3's so a shell caller can bind to the
#: predicate without knowing the vocabulary: **`[ $? -lt 20 ]` is safe-to-spawn.** A
#: future fifth state cannot be handed a number that reads spawn-safe to a band-checker,
#: and `custody_exit_code()` returns the ambiguity code for any state nobody named.
CUSTODY_EXIT_CODES: dict[str, int] = {
    SEAM_FREE: 0,
    SEAM_HELD: 20,
    SEAM_STALE: 21,
    SEAM_UNKNOWN: 22,
}

#: A WRITE was refused on its ARGUMENTS — an unstated release condition (Amendment L),
#: a wildcard seam, a missing note or evidence. Distinct from the state codes, which
#: refuse on the seam's CONDITION, and inside the occupied band so no refusal ever
#: reads spawn-safe to a caller who only checks `$? -lt 20`.
EXIT_REFUSED = 40

#: `claim` could not take the ledger lock within its bounded budget. Not a state and
#: not an argument error: another writer held the ledger for longer than a small TSV
#: append can explain. In the occupied band, because the one thing we know is that we
#: did NOT establish custody.
EXIT_LEDGER_CONTENDED = 41

#: Fail-closed precedence when several seams are summarised into one exit code.
#: Ambiguity first, then the state needing a human, then ordinary occupancy, then free.
CUSTODY_STATE_PRECEDENCE: tuple[str, ...] = (SEAM_UNKNOWN, SEAM_STALE, SEAM_HELD, SEAM_FREE)

#: Release conditions that ASSERT NOTHING. Amendment L requires a claim to name the
#: condition whose satisfaction produces the RELEASE; a condition nobody can evaluate is
#: the unbounded claim L exists to close, with a word in front of it. Compared
#: case-folded and stripped of trailing punctuation.
#:
#: DELETION is the fail-open direction — remove a spelling and a vacuous claim is
#: admitted. Addition is fail-CLOSED: it refuses more claims, loudly, at the moment of
#: writing, when the author is present to say something better. The set is deliberately
#: SMALL: it catches the null answer, not the vague one. Refusing "when the work is
#: done" would be this module having an opinion about English, which it is not equipped
#: to have and would fail at in the direction that annoys people into working around it.
VACUOUS_RELEASE_CONDITIONS: frozenset[str] = frozenset({
    "", "-", "?", "??", "tbd", "n/a", "na", "none", "nothing", "unknown", "unclear",
})

#: The ledger lock's bounded wait. ~2s ceiling at 20ms granularity, and the ceiling is
#: what makes waiting legitimate here: the critical section is a read plus one appended
#: line of a small TSV, so a wait longer than this is not contention, it is something
#: wrong. `claim` then REFUSES rather than breaking the lock or waiting forever.
LEDGER_LOCK_ATTEMPTS = 100
LEDGER_LOCK_DELAY_S = 0.02


class LedgerContended(RuntimeError):
    """The ledger lock could not be taken within its bounded budget."""


class MalformedLedger(RuntimeError):
    """A ledger row is not readable, so the derivation over it is not trustworthy."""


def custody_exit_code(state: str) -> int:
    """An UNKNOWN state exits `custody-unknown`, never `free`. Fail-closed at the edge.

    The vocabulary can grow wrong without the exit code going spawn-safe, which is the
    property that matters most: the failure this whole axis exists to prevent is a
    dispatcher being told *nobody is here* when somebody is.
    """
    return CUSTODY_EXIT_CODES.get(state, CUSTODY_EXIT_CODES[SEAM_UNKNOWN])


def safe_to_spawn(state: str) -> bool:
    """THE predicate. One name, one place, bound by every consumer — including the
    eventual SEAMS board card, which is a VIEW and re-derives nothing (Amendment J)."""
    return state in SAFE_TO_SPAWN_STATES


# ---------------------------------------------------------------------------
# 1 — the ledger (leg 1). READ ONLY.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CustodyRow:
    """One ledger event. Frozen, because a row is a record of the past."""

    ts: str
    seam: str
    holder: str
    event: str
    intent: str
    detail: str
    lineno: int = 0

    @property
    def tokens(self) -> dict[str, str]:
        """The detail column's free-form `k=v` pairs, parsed. Unknown keys survive."""
        out: dict[str, str] = {}
        for part in self.detail.split(";"):
            key, sep, value = part.strip().partition("=")
            if sep and key and " " not in key:
                out[key] = value.strip()
        return out

    def to_line(self) -> str:
        return "\t".join(
            (self.ts, self.seam, self.holder, self.event, self.intent, self.detail))


def read_ledger(path: Path | str | None = None) -> tuple[list[CustodyRow], list[str]]:
    """`(rows, malformed)` from the ledger. An ABSENT ledger is empty, not an error.

    Never creates the file, never locks it, never writes. A ledger that does not exist
    holds no claims, and that answer is free — the same reasoning that keeps leg 1 of
    the vendor busy check from creating a lock file by asking about it.

    Malformed rows are RETURNED, not skipped. A row this parser cannot read is a row
    whose seam might be occupied, and silently dropping it is the false-open direction.
    The caller turns the list into `custody-unknown`.
    """
    ledger = Path(path) if path is not None else DEFAULT_LEDGER
    if not ledger.exists():
        return [], []

    rows: list[CustodyRow] = []
    malformed: list[str] = []
    for lineno, raw in enumerate(ledger.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != len(LEDGER_COLUMNS):
            malformed.append(
                f"line {lineno}: {len(parts)} columns, expected {len(LEDGER_COLUMNS)} "
                f"({', '.join(LEDGER_COLUMNS)})")
            continue
        row = CustodyRow(*[p.strip() for p in parts], lineno=lineno)  # type: ignore[arg-type]
        if row.event not in CUSTODY_EVENTS:
            malformed.append(
                f"line {lineno}: event {row.event!r} is not one of "
                f"{sorted(CUSTODY_EVENTS)}")
            continue
        if not row.seam:
            malformed.append(f"line {lineno}: no seam named")
            continue
        rows.append(row)
    return rows, malformed


def open_claims(rows: Iterable[CustodyRow]) -> dict[str, CustodyRow]:
    """`{seam: the CLAIM row that is still open}` — the fold, in file order.

    CLAIM opens; RELEASE and OVERRIDE close. Last write per seam wins, so a seam
    re-claimed after a release is open again, and a partial release of a multi-seam
    charter is expressible because each seam carries its OWN row (Amendment L: no
    wildcards, no blanket rows).
    """
    out: dict[str, CustodyRow] = {}
    for row in rows:
        if row.event == EVENT_CLAIM:
            out[row.seam] = row
        elif row.event in (EVENT_RELEASE, EVENT_OVERRIDE):
            out.pop(row.seam, None)
    return out


# ---------------------------------------------------------------------------
# 2 — holder liveness (leg 2). READ ONLY.
# ---------------------------------------------------------------------------
#: A holder id ends with its PID when it has one: `gandalf-session-85515` -> 85515.
#: ANCHORED at a separator so a hex session id like `gandalf-session-53631d11` does not
#: yield `11` — convicting an unrelated process of being the holder is worse than
#: admitting we cannot tell, because the wrong answer is confidently `held` and the
#: honest one is `custody-unknown`.
_HOLDER_PID_RE = re.compile(r"(?:^|[-_.:])(\d+)$")


def holder_pid(holder: str) -> int | None:
    """The holder id's PID, or None when it names none."""
    match = _HOLDER_PID_RE.search(holder.strip())
    return int(match.group(1)) if match else None


def scan_process_starts(
    runner: Callable[[list[str]], "subprocess.CompletedProcess[str]"] | None = None,
) -> dict[int, str]:
    """`ps -axo pid=,lstart=` -> `{pid: start-time string}`. RAISES if `ps` fails.

    The whole table, not `ps -p <pid>`, and the reason is a trap worth naming: `ps -p`
    exits NON-ZERO when no listed pid matches, so "the holder is dead" and "`ps` is
    broken" would arrive as the same signal. Conflating them would report
    `custody-unknown` for every dead holder — and `stale` is the state that unlocks
    `override`, so the operator would be denied the one verb that clears the seam, at
    exactly the moment they need it. The full table exits 0 whenever `ps` works.

    Our OWN pid is NOT excluded, unlike the vendor check's process scan. There the
    instrument must not convict itself of being the thing it watches; here a claim held
    by the very session asking is genuinely held, and hiding it would answer `stale` to
    the one process that can prove otherwise.
    """
    argv = ["ps", "-axo", "pid=,lstart="]
    run = runner or (lambda a: subprocess.run(
        a, capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL,
    ))
    proc = run(argv)
    if proc.returncode != 0:
        raise RuntimeError(
            f"`{' '.join(argv)}` exited {proc.returncode}: "
            f"{(proc.stderr or '').strip()[:200] or 'no stderr'}")
    out: dict[int, str] = {}
    for line in (proc.stdout or "").splitlines():
        pid_text, _, started = line.strip().partition(" ")
        if pid_text.isdigit():
            out[int(pid_text)] = started.strip()
    return out


#: What leg 2 can say about a holder, and the seam state each answer produces. Three
#: answers, never two: `unknown` is a REAL answer, and collapsing it into `dead` would
#: let an unreadable leg unlock `override` — handing out the seam-clearing verb on a
#: broken instrument.
#:
#: Spent as `LIVENESS_TO_SEAM_STATE[answer]` in the derivation, so a fourth liveness
#: answer raises a `KeyError` at the mapping rather than silently choosing a state.
LIVENESS_TO_SEAM_STATE: dict[str, str] = {
    "alive": SEAM_HELD,
    "dead": SEAM_STALE,
    "unknown": SEAM_UNKNOWN,
}


def holder_liveness(
    holder: str, recorded_start: str | None, starts: dict[int, str] | None,
) -> tuple[str, str]:
    """`(answer, reason)` for one holder. `starts=None` means `ps` was unreadable.

    **PID AND START TIME, per jack-ryan's Gate-2 INFO.** PIDs recycle. A dead session
    whose PID was reassigned reads *alive*, which fails in the FALSE-BUSY direction and
    is therefore safe — but an `override` refused by a recycled PID looks wrong to the
    operator at the moment they most need the ledger to make sense. Comparing the
    process START TIME as well costs one extra column of `ps` output and removes that
    confusion entirely.

    A claim written before start times were recorded gets PID-only liveness and SAYS SO
    in its reason. Degrading loudly is the whole difference between a weaker answer and
    a wrong one.
    """
    pid = holder_pid(holder)
    if pid is None:
        return "unknown", (
            f"holder {holder!r} names no PID, so leg 2 cannot be asked about it. "
            "Liveness is unanswerable, not negative — the seam reads occupied.")
    if starts is None:
        return "unknown", (
            f"the process table could not be read, so PID {pid} can be neither "
            "confirmed alive nor shown dead.")
    if pid not in starts:
        return "dead", (
            f"PID {pid} is not in the process table — the holder session is gone.")
    if not recorded_start:
        return "alive", (
            f"PID {pid} is alive. NO start time was recorded at claim time, so this is "
            "PID-only liveness: a recycled PID would read alive here. That is the "
            "false-BUSY direction, which is the safe one.")
    if starts[pid] != recorded_start:
        return "dead", (
            f"PID {pid} is alive but started {starts[pid]!r}, not {recorded_start!r} as "
            "recorded at claim time. The PID was RECYCLED; this holder is gone.")
    return "alive", f"PID {pid} alive since {starts[pid]}, matching the claim."


# ---------------------------------------------------------------------------
# 3 — the derivation. READ ONLY. THIS IS THE WHOLE CHECK.
# ---------------------------------------------------------------------------
@dataclass
class CustodyAnswer:
    """One seam's answer. WHICH state, never a bare bool."""

    seam: str
    state: str
    reason: str
    holder: str | None = None
    since: str | None = None
    intent: str | None = None
    claim_line: int | None = None
    legs: dict[str, Any] = field(default_factory=dict)

    @property
    def safe_to_spawn(self) -> bool:
        return safe_to_spawn(self.state)

    @property
    def exit_code(self) -> int:
        return custody_exit_code(self.state)

    def one_line(self) -> str:
        who = f" holder={self.holder}" if self.holder else ""
        return f"{self.seam:<12} {self.state:<15}{who}  — {self.reason}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "seam": self.seam, "state": self.state, "reason": self.reason,
            "holder": self.holder, "since": self.since, "intent": self.intent,
            "claim_line": self.claim_line, "safe_to_spawn": self.safe_to_spawn,
            "exit_code": self.exit_code, "legs": self.legs,
        }


def custody_check(
    seam: str | None = None,
    *,
    ledger: Path | str | None = None,
    starts: dict[int, str] | None = None,
    scan: Callable[[], dict[int, str]] | None = None,
) -> list[CustodyAnswer]:
    """**THE CHECK.** Read-only, locks nothing, creates nothing, emits nothing.

    `seam=None` answers for every seam with an open claim; naming a seam answers for
    that seam even when it is free, which is the question a dispatcher actually asks.

    `ps` is consulted only when at least one claim is open. A seam nobody claimed cannot
    be held by anybody, and that answer costs no subprocess — the same shape as leg 1 of
    the vendor check declining to probe a lock file that does not exist.
    """
    rows, malformed = read_ledger(ledger)
    claims = open_claims(rows)
    seams = sorted(claims) if seam is None else [seam]

    if malformed:
        # Fail-closed over the WHOLE ledger, not per row. A row this parser could not
        # read may be the CLAIM that closes the seam being asked about, and there is no
        # honest way to answer a question over a record that is partly unreadable. Loud,
        # and it is fixed by editing one line of a TSV.
        detail = "; ".join(malformed[:5])
        return [
            CustodyAnswer(
                s, SEAM_UNKNOWN,
                f"the ledger has {len(malformed)} unreadable row(s) — {detail}. "
                "The derivation over a partly unreadable record is not trustworthy, so "
                "every seam reads occupied until the row is fixed.",
                legs={"ledger": {"malformed": malformed}},
            )
            for s in (seams or ["(all)"])
        ]

    if not claims:
        # No subprocess. A seam nobody claimed cannot be held by anybody. With no seam
        # named and no open claims, the honest answer is an EMPTY list — "nothing is
        # held" — rather than a fabricated roster of every seam that ever existed.
        return [
            CustodyAnswer(s, SEAM_FREE, "no open CLAIM in the ledger.",
                          legs={"ledger": {"open_claims": 0}})
            for s in seams
        ]

    if starts is None:
        try:
            starts = (scan or scan_process_starts)()
        except Exception as exc:  # noqa: BLE001 — any failure is "could not look"
            starts = None
            scan_error = f"{type(exc).__name__}: {exc}"
        else:
            scan_error = None
    else:
        scan_error = None

    answers: list[CustodyAnswer] = []
    for name in seams:
        claim = claims.get(name)
        if claim is None:
            answers.append(CustodyAnswer(
                name, SEAM_FREE, "no open CLAIM for this seam.",
                legs={"ledger": {"open_claims": len(claims)}}))
            continue

        recorded_start = claim.tokens.get("holder_started")
        answer, why = holder_liveness(claim.holder, recorded_start, starts)
        if scan_error and answer == "unknown":
            why = f"{why} ({scan_error})"
        state = LIVENESS_TO_SEAM_STATE[answer]
        if state == SEAM_STALE:
            why = (
                f"{why} STALE IS NOT FREE: clearing it takes `factory custody override "
                f"--seam {name} --note ...`. There is no TTL and there will not be one.")
        answers.append(CustodyAnswer(
            name, state, why,
            holder=claim.holder, since=claim.ts, intent=claim.intent,
            claim_line=claim.lineno,
            legs={
                "ledger": {"claim_line": claim.lineno, "open_claims": len(claims)},
                "liveness": {"answer": answer, "pid": holder_pid(claim.holder),
                             "recorded_start": recorded_start,
                             "readable": starts is not None},
            }))
    return answers


def worst_exit_code(answers: Sequence[CustodyAnswer]) -> int:
    """Fail-closed across seams: the worst answer's code wins.

    A caller reading only the exit code is never told *free* while a seam is occupied.
    An EMPTY answer list is `free` — nothing was claimed, so nothing is held.
    """
    if not answers:
        return CUSTODY_EXIT_CODES[SEAM_FREE]
    rank = {state: i for i, state in enumerate(CUSTODY_STATE_PRECEDENCE)}
    return min(answers, key=lambda a: rank.get(a.state, 0)).exit_code


# ---------------------------------------------------------------------------
# 4 — the writes. AMENDMENT K: check-and-append is ATOMIC.
# ---------------------------------------------------------------------------
@dataclass
class CustodyWrite:
    """The outcome of a write verb. Refusals carry the reason and the exit code."""

    ok: bool
    exit_code: int
    reason: str
    row: CustodyRow | None = None
    state: str | None = None
    holder: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok, "exit_code": self.exit_code, "reason": self.reason,
            "state": self.state, "holder": self.holder,
            "row": self.row.to_line() if self.row else None,
        }


@contextmanager
def ledger_lock(
    path: Path,
    *,
    attempts: int = LEDGER_LOCK_ATTEMPTS,
    delay_s: float = LEDGER_LOCK_DELAY_S,
    sleep: Callable[[float], None] = time.sleep,
) -> Iterator[SerialLaneLock]:
    """`flock` on the LEDGER FILE ITSELF (Amendment K), with a BOUNDED wait.

    `SerialLaneLock` is reused unchanged — G-1's grounding carries over exactly: derived
    kernel state, content never trusted, released by the kernel when the holder exits,
    including on SIGKILL. It is `LOCK_NB`, so the wait is this loop and not the kernel's.

    Waiting here is not the thing the vendor lane refuses. That lock is held across a
    model call, so a wait on it is unbounded and a "short" wait is a guess. This one is
    held across a read and one appended line — no subprocess, no spawn — so the budget
    above is a ceiling on something whose true duration is microseconds. Exhausting it
    means something is wrong, and the answer is to REFUSE, never to break the lock.
    """
    lock = SerialLaneLock(path)
    for attempt in range(attempts):
        try:
            lock.acquire()
        except LaneBusy:
            sleep(delay_s)
            continue
        try:
            yield lock
        finally:
            lock.release()
        return
    raise LedgerContended(
        f"the custody ledger lock at {path} was held by another writer for longer than "
        f"{attempts * delay_s:.1f}s. The critical section is a read plus one appended "
        "line, so this is not ordinary contention. NOT breaking the lock; refusing.")


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append_row(path: Path, row: CustodyRow) -> None:
    """One line, appended. Called ONLY with the ledger lock held."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(row.to_line() + "\n")


def _process_table_before_the_lock(
    starts: dict[int, str] | None,
    scan: Callable[[], dict[int, str]] | None,
) -> dict[int, str] | None:
    """Take the `ps` reading BEFORE acquiring the ledger lock. `None` if unreadable.

    This is not a micro-optimisation, it is the thing that makes the bounded wait in
    `ledger_lock` legitimate. That wait is defended by the claim *the critical section
    is a read and one appended line — no subprocess, no spawn*; running `ps` inside the
    lock would falsify it, and a `ps` under contention is tens of milliseconds during
    which every other claimant burns its retry budget.

    Freshness costs nothing here: the reading is taken microseconds before the lock, and
    the failure mode it could theoretically introduce — a holder that died in that
    window reading `alive` — is the false-BUSY direction, which is the safe one. The
    opposite arrangement trades a real property for an imaginary one.
    """
    if starts is not None:
        return starts
    try:
        return (scan or scan_process_starts)()
    except Exception:  # noqa: BLE001 — any failure is "could not look"; the check says so
        return None


def normalise_release_condition(condition: str) -> str:
    return condition.strip().strip(".!?").casefold()


def refuse_reason_for_claim_arguments(seam: str, intent: str, release_on: str) -> str | None:
    """Amendment L, and the one-row-per-seam rule. `None` means the arguments are sound.

    Evaluated BEFORE the lock is taken, so a refused claim never holds the ledger — the
    same shape as the Grok harness's Amendment-E preflight, which refuses and does not
    take the lane. A refusal that first acquires something is a refusal that can fail
    while cleaning up.

    **Why `release_on` is a separate argument and not a phrase inside `intent`.** Nothing
    here can read English, and a claim naming its release condition in prose could only
    be checked by looking for a magic word — which the next author satisfies by typing
    the magic word. Making the field STRUCTURAL means the requirement cannot be met
    accidentally, and it is the same lesson as U-4 R-B's curator: a governance line
    enforced by whoever remembers to type it is the state R-B exists to replace.
    """
    if not seam or seam != seam.strip():
        return "the seam name is empty or carries surrounding whitespace."
    if any(ch in seam for ch in "*?,\t "):
        return (
            f"seam {seam!r} looks like a wildcard or a list. **Amendment L: one row per "
            "seam, never a blanket row** — a dispatcher checking seam X must find a row "
            "ABOUT seam X, and a partial release has to be expressible. A run-scoped "
            "charter claims its seams one row at a time.")
    if not intent.strip():
        return "a claim with no stated intent is a claim nobody can evaluate."
    if normalise_release_condition(release_on) in VACUOUS_RELEASE_CONDITIONS:
        return (
            f"the release condition {release_on!r} states nothing. **Amendment L: every "
            "CLAIM names the condition whose satisfaction produces the RELEASE** — a "
            "claim whose release condition cannot be stated is a claim that should not "
            "be written. Composed with *no TTL* and *occupied means do not spawn*, an "
            "unbounded live claim is indistinguishable from owning the seam, which is "
            "the thing § 11.5 promises custody is not. This refuses rather than "
            "defaulting, the same way the Grok harness refuses an undeclared vendor.")
    return None


def claim(
    *,
    seam: str,
    holder: str,
    intent: str,
    release_on: str,
    detail: str = "",
    ledger: Path | str | None = None,
    now: str | None = None,
    starts: dict[int, str] | None = None,
    scan: Callable[[], dict[int, str]] | None = None,
    lock_attempts: int = LEDGER_LOCK_ATTEMPTS,
    lock_delay_s: float = LEDGER_LOCK_DELAY_S,
) -> CustodyWrite:
    """**ATOMIC check-and-append** (Amendment K). Exactly one concurrent claim wins.

    The race Amendment K names is real: *check, then claim* lets two dispatchers both
    read free, both append, and both spawn — the founding incident, unprevented by the
    mechanism built to prevent it. The exclusion is NOT "whoever got the lock first":
    both claimants serialise through the lock and **re-derive the answer under it**, so
    the second one sees the first one's row and is told WHO holds the seam. That is a
    test-and-set, and it is why the loser gets a name rather than a retry.
    """
    path = Path(ledger) if ledger is not None else DEFAULT_LEDGER

    refusal = refuse_reason_for_claim_arguments(seam, intent, release_on)
    if refusal is not None:
        return CustodyWrite(False, EXIT_REFUSED, refusal)

    # BEFORE the lock, deliberately — see `_process_table_before_the_lock`. The critical
    # section below must stay a read plus one appended line, because that is the entire
    # justification for `ledger_lock` being allowed to wait at all.
    table = _process_table_before_the_lock(starts, scan)

    try:
        with ledger_lock(path, attempts=lock_attempts, delay_s=lock_delay_s):
            answers = custody_check(seam, ledger=path, starts=table, scan=scan)
            current = answers[0]
            if not current.safe_to_spawn:
                # The loser of a concurrent claim is TOLD WHO HOLDS THE SEAM (Amendment
                # K's D-10 row). A refusal that says only "busy" sends a dispatcher back
                # to the ledger to work out who to talk to, and the whole point of the
                # axis is that two live routers can see each other without a
                # conversation.
                who = (
                    f"held by {current.holder} since {current.since} for: "
                    f"{current.intent}. " if current.holder else "")
                return CustodyWrite(
                    False, current.exit_code,
                    f"seam {seam!r} is {current.state.upper()} — {who}"
                    f"{current.reason} DO NOT SPAWN: coordinate with the holder, wait, "
                    "or escalate. Standing down is the honourable path and it gets a "
                    "ledger row, not a shrug.",
                    state=current.state, holder=current.holder)

            tokens = [t for t in (detail.strip(),) if t]
            pid = holder_pid(holder)
            if pid is not None and table and pid in table:
                # jack-ryan's PID-recycling INFO, recorded at the ONE moment it can be:
                # claim time. Without it, leg 2 is PID-only for the life of the claim.
                tokens.append(f"holder_started={table[pid]}")
            # One `k=v` token, not a token plus a trailing phrase: the detail column is
            # split on `;` and a bare clause parses as nothing, which is how free-form
            # columns quietly accumulate text no reader can use.
            tokens.append(
                "spec=§ 11.3 claim-before-spawn (Amendment L release condition named)")

            row = CustodyRow(
                ts=now or _utc_now(), seam=seam, holder=holder, event=EVENT_CLAIM,
                intent=f"{intent.strip()}; RELEASE on {release_on.strip()}",
                detail="; ".join(tokens))
            _append_row(path, row)
            return CustodyWrite(
                True, CUSTODY_EXIT_CODES[SEAM_FREE],
                f"CLAIMED seam {seam!r} for {holder}.", row=row, state=SEAM_HELD,
                holder=holder)
    except LedgerContended as exc:
        return CustodyWrite(False, EXIT_LEDGER_CONTENDED, str(exc))


def release(
    *,
    seam: str,
    holder: str,
    evidence: str,
    ledger: Path | str | None = None,
    now: str | None = None,
    lock_attempts: int = LEDGER_LOCK_ATTEMPTS,
    lock_delay_s: float = LEDGER_LOCK_DELAY_S,
) -> CustodyWrite:
    """Close a claim, CITING the completion evidence. Refuses over a seam nobody holds.

    **Who may write it.** The holder column names the SESSION THAT MUST BE ALIVE, not the
    agent — so the dispatcher normally writes the RELEASE when its sub-agent's completion
    lands, and that is not the same string as the sub-agent. A release by a different
    session is therefore ACCEPTED and RECORDED (`claimed_by=`) rather than refused:
    refusing would strand every claim whose sub-agent wrote the completion, and stranded
    claims are what `override` exists for and what it should stay rare for.

    A RELEASE against no open claim is refused. A row that closes nothing teaches a false
    history to everyone who reads the ledger afterwards, and the ledger's whole value is
    that its rows are events that happened.
    """
    path = Path(ledger) if ledger is not None else DEFAULT_LEDGER
    if not evidence.strip():
        return CustodyWrite(False, EXIT_REFUSED, (
            "a RELEASE cites its completion evidence. The claim was written before the "
            "work existed; the release is the half that says the work is done, and an "
            "uncited release is an assertion with nothing behind it."))
    try:
        with ledger_lock(path, attempts=lock_attempts, delay_s=lock_delay_s):
            rows, malformed = read_ledger(path)
            if malformed:
                return CustodyWrite(False, EXIT_REFUSED, (
                    f"the ledger has {len(malformed)} unreadable row(s): "
                    f"{'; '.join(malformed[:3])}. Fix the row before appending to it."))
            claim_row = open_claims(rows).get(seam)
            if claim_row is None:
                return CustodyWrite(False, EXIT_REFUSED, (
                    f"seam {seam!r} has no open CLAIM, so there is nothing to release. A "
                    "RELEASE row that closes nothing teaches a false history."),
                    state=SEAM_FREE)

            tokens = [f"completion={evidence.strip()}"]
            if claim_row.holder != holder:
                tokens.append(f"claimed_by={claim_row.holder}")
                tokens.append("released_by_a_different_session (holder = the session "
                              "that must be alive, not the agent)")
            row = CustodyRow(
                ts=now or _utc_now(), seam=seam, holder=holder, event=EVENT_RELEASE,
                intent=claim_row.intent, detail="; ".join(tokens))
            _append_row(path, row)
            return CustodyWrite(
                True, CUSTODY_EXIT_CODES[SEAM_FREE],
                f"RELEASED seam {seam!r}.", row=row, state=SEAM_FREE, holder=holder)
    except LedgerContended as exc:
        return CustodyWrite(False, EXIT_LEDGER_CONTENDED, str(exc))


def override(
    *,
    seam: str,
    holder: str,
    note: str,
    ledger: Path | str | None = None,
    now: str | None = None,
    starts: dict[int, str] | None = None,
    scan: Callable[[], dict[int, str]] | None = None,
    lock_attempts: int = LEDGER_LOCK_ATTEMPTS,
    lock_delay_s: float = LEDGER_LOCK_DELAY_S,
) -> CustodyWrite:
    """Clear a STALE claim — **loud, manual, and only over a holder shown to be dead.**

    This is the G-2 FALSE-BUSY choice at the agent level. The alternative is a TTL, and a
    TTL is a timeout-based lock break wearing a different word: it frees a claim whose
    holder is alive and mid-flight, silently, at the moment the seam is hottest.

    Three refusals, and each is a different mistake:
      * over a **live** holder — that is not an override, it is evicting somebody who is
        working. Coordinate, or let them release. There is no `--force`, deliberately:
        inventing one here would grant an authority nobody ratified.
      * over `custody-unknown` — we cannot SHOW the holder dead, and an override on a
        leg we could not read is a lock break with extra steps. Make leg 2 answerable
        (record a PID, fix `ps`) and ask again.
      * over a **free** seam — there is nothing to override.
    """
    path = Path(ledger) if ledger is not None else DEFAULT_LEDGER
    if not note.strip():
        return CustodyWrite(False, EXIT_REFUSED, (
            "an OVERRIDE requires a NOTE. The note is the entire difference between "
            "this and a TTL: a human said why, in the record, at the time."))
    # BEFORE the lock, for the same reason `claim` does it: no subprocess under the flock.
    table = _process_table_before_the_lock(starts, scan)
    try:
        with ledger_lock(path, attempts=lock_attempts, delay_s=lock_delay_s):
            answers = custody_check(seam, ledger=path, starts=table, scan=scan)
            current = answers[0]
            if current.state != SEAM_STALE:
                return CustodyWrite(False, current.exit_code, (
                    f"seam {seam!r} is {current.state.upper()}, and OVERRIDE clears only "
                    f"a STALE claim. {current.reason}"),
                    state=current.state, holder=current.holder)
            rows, _ = read_ledger(path)
            claim_row = open_claims(rows)[seam]
            row = CustodyRow(
                ts=now or _utc_now(), seam=seam, holder=holder, event=EVENT_OVERRIDE,
                intent=claim_row.intent,
                detail=f"note={note.strip()}; cleared_holder={claim_row.holder}; "
                       f"claimed_at={claim_row.ts}; liveness={current.reason}")
            _append_row(path, row)
            return CustodyWrite(
                True, CUSTODY_EXIT_CODES[SEAM_FREE],
                f"OVERRODE the stale claim on seam {seam!r} (held by "
                f"{claim_row.holder}).", row=row, state=SEAM_FREE, holder=holder)
    except LedgerContended as exc:
        return CustodyWrite(False, EXIT_LEDGER_CONTENDED, str(exc))
