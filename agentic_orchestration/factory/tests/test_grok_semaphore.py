"""D-12 — the Grok lane's PER-AGENT SEMAPHORE, proven without a live vendor call.

§ 9.6 AM-3 (Matt: *"agreed on (b) per agent seam"*), ratified by jack-ryan as ADDENDUM 3
with binding Amendments M–R. The rows below are organised by amendment, because that is
the unit a Gate-2 reader adjudicates:

  **M** — `seam` is a REQUIRED, roster-validated job field: refused, never defaulted,
          never inferred from `curator`, and never read from the custody LEDGER.
  **N** — TWO NESTED FLOCKS. The per-seam lock is the second-claim refusal *by
          construction*; the slot tag is DISPLAY-ONLY and is never an exclusion input.
          Nothing blocks, so nothing can deadlock. Both fds outlive the queue.
  **O** — N=3, and the ceiling is the credential's.
  **P** — the run-log rows carry the concurrency interval and the wait's REASON.
  **Q** — the busy check answers `k/3`, writes nothing, and fails closed PER SLOT.
  **R** — a per-agent refusal is neither a busy lane nor a failed job: the drain SKIPS
          and keeps going, and the skip is never an attempt.

**Why real flocks and real threads rather than mocks.** The thing under test is a kernel
primitive's behaviour across open file descriptions; a mock of `SeamSlotSemaphore`
replaces precisely the part that could be wrong. Same choice `test_custody.py` made for
Amendment K, and for the same reason: `flock` binds to the open file description rather
than to the PID (measured, errno 35), so threads in one process are a faithful stand-in
for two sessions — and that property is itself load-bearing here, since one drain
process is exactly where a second acquisition would otherwise slip through.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from factory.harness.grok import GrokHarness, LaneAvailability
from factory.jobqueue import JobQueue
from factory.lane import (
    GROK_SLOT_CEILING,
    LANE_STATE_SEAM_HELD,
    SKIPPED_PER_AGENT,
    LaneCeilingReached,
    SeamSlotHeld,
    SeamSlotSemaphore,
    probe_slots,
    seam_lock_path,
    slot_lock_path,
)
from factory.roster import AGENT_ROSTER

# The fake vendor CLI is the one the sibling file already proves against — imported
# rather than re-typed, so the two suites cannot disagree about what `grok` does.
from test_grok_harness import _FAKE_GROK  # noqa: E402

SEAMS = ("star-lord", "elrond", "galadriel")


@pytest.fixture
def base(tmp_path: Path) -> Path:
    """The lane's BASE lock path. Seam locks and slots are derived from it."""
    return tmp_path / "grok.lock"


@pytest.fixture
def fake_grok(tmp_path: Path, monkeypatch) -> Path:
    path = tmp_path / "fake-grok"
    path.write_text(_FAKE_GROK, encoding="utf-8")
    path.chmod(0o755)
    monkeypatch.setenv("FAKE_GROK_ARGV", str(tmp_path / "argv.json"))
    return path


def _harness(fake_grok: Path, base: Path, ceiling: int = GROK_SLOT_CEILING) -> GrokHarness:
    return GrokHarness(
        executable=str(fake_grok), lock_path=base, ceiling=ceiling,
        auth_probe=lambda: LaneAvailability(True, "open", "logged in"),
    )


def _enqueue(queue: JobQueue, job_id: str, seam: str, curator: str = "galadriel"):
    return queue.enqueue(
        job_id=job_id, prompt=f"prompt for {job_id}", curator=curator,
        seam=seam, sandbox="n/a",
    )


# ===========================================================================
# AMENDMENT M — the seam is a DECLARED, ROSTER-VALIDATED field
# ===========================================================================
def test_M_a_GROK_job_with_NO_SEAM_does_not_enqueue(tmp_path):
    """REFUSED, and it leaves no trace — the P-8 curator-law shape, one axis over.

    A job with no seam is not a job with a missing label. The per-agent flock is keyed
    on this name, so an unnamed seam is a job **nothing can exclude against** — and the
    refusal has to fire before any file or row exists, or a later reader finds a job
    record that looks enqueued and an exclusivity rule that never applied to it.
    """
    queue = JobQueue(tmp_path / "q", lane="grok")
    with pytest.raises(ValueError, match="AMENDMENT M: REFUSAL TO FIRE"):
        queue.enqueue(job_id="j", prompt="p", curator="galadriel", sandbox="n/a")
    assert not (tmp_path / "q" / "_run-log.tsv").exists()
    assert not (tmp_path / "q" / "jobs").exists()


def test_M_the_seam_is_NEVER_INFERRED_FROM_THE_CURATOR(tmp_path):
    """The conflation M.2 forbids, exhibited in both directions rather than described.

    A curator is the named Claude owner of the OUTPUT (R-B/P-8); a seam is the agent
    whose PROCESS makes the invocation. Defaulting one to the other breaks exclusivity
    BOTH ways, and both ways are legal shapes that the fleet actually runs:

      * two DIFFERENT agents running jobs curated by one agent would collide on one
        slot — a refusal where the law permits two concurrent fires;
      * one agent running three DIFFERENTLY-curated jobs would take three slots — three
        concurrent fires where the law permits one.
    """
    queue = JobQueue(tmp_path / "q", lane="grok")
    # A curator is named and is a perfectly good roster name — and it is still not a
    # seam. The refusal fires anyway, which is the whole content of "never inferred".
    with pytest.raises(ValueError, match="AMENDMENT M: REFUSAL TO FIRE"):
        queue.enqueue(job_id="j", prompt="p", curator="galadriel", sandbox="n/a")

    job = _enqueue(queue, "j", seam="star-lord", curator="galadriel")
    assert job.seam == "star-lord" and job.curator == "galadriel", (
        "the two fields collapsed into one. They are recorded BESIDE each other, never "
        "on top of each other."
    )
    row = list(queue.runlog.rows())[0]
    assert "seam=star-lord" in row[3] and row[4] == "curator=galadriel"


def test_M_a_seam_OFF_THE_ROSTER_is_refused_and_NOT_normalised(tmp_path):
    """`starlord` is not `star-lord`, and guessing is only safe when being wrong shows.

    A free-text seam makes two spellings of one agent into two agents: both acquire
    their own per-seam lock, both fire, and every instrument reports compliance. That
    is the SILENT failure direction, and it is the one this whole spec refuses — so the
    near miss is REFUSED rather than corrected.
    """
    queue = JobQueue(tmp_path / "q", lane="grok")
    with pytest.raises(ValueError, match="not on the agent roster"):
        _enqueue(queue, "j", seam="starlord")
    assert "star-lord" in AGENT_ROSTER and "starlord" not in AGENT_ROSTER


def test_M_the_CODEX_lane_does_not_DEMAND_a_seam_but_VALIDATES_ONE_GIVEN(tmp_path):
    """The per-lane required set, and why the asymmetry is not laziness.

    Codex is hard serial by VENDOR LAW (N=1) — there is no per-agent grain there and
    none coming, so a required seam would be a mandatory declaration that refuses jobs
    while enforcing nothing: a governance line with no mechanism behind it, which is the
    "label, not a vocabulary" state R-B's own first version was in.

    But a seam that IS given is roster-validated even there, because a recorded typo is
    worse than an absent field: it reads as an answer.
    """
    queue = JobQueue(tmp_path / "q", lane="codex")
    assert queue.enqueue(job_id="a", prompt="p", curator="elrond").seam == ""
    assert queue.enqueue(job_id="b", prompt="p", curator="elrond", seam="rocket").seam == "rocket"
    with pytest.raises(ValueError, match="not on the agent roster"):
        queue.enqueue(job_id="c", prompt="p", curator="elrond", seam="rockett")


def test_M4_the_vendor_fire_NEVER_READS_THE_CUSTODY_LEDGER():
    """M.4's scope guard, asserted over the SOURCE rather than left to a paragraph.

    The Grok slot borrows custody's GRAIN and must not acquire its MECHANISM: a vendor
    fire that consulted `_custody.tsv` would take on a second truth source, and a
    missing or stale CLAIM row could then block a legal fire. Two axes, one vocabulary,
    no coupling — which means the fire path must not import `custody` at all.
    """
    import ast

    for module in ("harness/grok.py", "jobqueue.py", "lane.py", "roster.py"):
        tree = ast.parse(
            (Path(__file__).resolve().parents[1] / module).read_text(encoding="utf-8"))
        # By AST, and over CODE only. Read as raw text this row reds on the comments
        # that EXPLAIN the prohibition — which would teach the next author to delete
        # the explanation rather than keep the property, and the comment is where the
        # reason lives. Docstrings are `Expr(Constant(str))` statements and are
        # excluded on the same grounds; a real path reference is never one.
        prose = {
            id(node.value) for node in ast.walk(tree)
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
        }
        imports, literals = set(), set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
                imports.update(f"{node.module or ''}.{a.name}" for a in node.names)
            elif (isinstance(node, ast.Constant) and isinstance(node.value, str)
                    and id(node) not in prose):
                literals.add(node.value)
        assert not any("custody" in name for name in imports), (
            f"`{module}` imports the custody ledger's module. The vendor lane borrows "
            "the seam VOCABULARY and must never depend on the agent LEDGER — a vendor "
            "fire gated on a hand-appended row is a fire that a forgotten CLAIM blocks."
        )
        assert not any("custody" in text for text in literals), (
            f"`{module}` names a custody path in code. Same finding, reached by opening "
            "the file instead of importing the module."
        )


# ===========================================================================
# AMENDMENT N — two nested flocks; the tag is DIAGNOSTIC, never enforcement
# ===========================================================================
def test_N_a_SECOND_CLAIM_BY_THE_SAME_SEAM_IS_REFUSED_and_names_the_holder(base):
    """The refusal is the per-seam `flock` FAILING — no content read, no race.

    And the loser is told WHICH SEAM holds it, for the reason Amendment K gave one axis
    over: a refusal that says only "busy" sends the caller back to look for whom to talk
    to, and here the answer is already in the exception.
    """
    first = SeamSlotSemaphore(base, "star-lord").acquire()
    try:
        with pytest.raises(SeamSlotHeld) as caught:
            SeamSlotSemaphore(base, "star-lord").acquire()
    finally:
        first.release()
    assert caught.value.seam == "star-lord"
    assert "star-lord" in str(caught.value)
    assert not isinstance(caught.value, LaneCeilingReached), (
        "a per-agent refusal is a `LaneBusy`. That is Amendment R's whole finding: a "
        "drain cannot then tell 'this agent is busy' from 'the credential is full', and "
        "will stop the lane at 1/3 with two slots idle."
    )
    # ... and the seam is free the instant the holder releases.
    SeamSlotSemaphore(base, "star-lord").acquire().release()


def test_N_THREE_DISTINCT_SEAMS_HOLD_THREE_SLOTS_AT_ONCE(base):
    """**The capacity AM-3 exists to unlock**, exercised with real concurrent flocks.

    Eight threads at a barrier across three seams rather than three tidy sequential
    acquisitions: with three, a scheduler could run each to completion before the next
    starts and the row would pass without the locks ever being contended. The assertion
    is the same either way — exactly one holder per SEAM, and never more than the
    ceiling in total.
    """
    ceiling = 3
    barrier = threading.Barrier(len(SEAMS) * 2)
    held: list[SeamSlotSemaphore] = []
    refused: list[BaseException] = []
    guard = threading.Lock()

    def race(seam: str) -> None:
        barrier.wait()
        semaphore = SeamSlotSemaphore(base, seam, ceiling=ceiling)
        try:
            semaphore.acquire()
        except BaseException as exc:  # noqa: BLE001 — the refusal IS the measurement
            with guard:
                refused.append(exc)
            return
        with guard:
            held.append(semaphore)

    threads = [threading.Thread(target=race, args=(seam,))
               for seam in SEAMS for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    try:
        assert len(held) == 3, (
            f"{len(held)} of 3 seams got a slot. Three DISTINCT seams firing at once is "
            "the capacity the amendment exists to unlock; if this is 1, the lane is "
            "still serial and the ruling did not land."
        )
        assert sorted(s.seam for s in held) == sorted(SEAMS)
        assert sorted(s.slot_index for s in held) == [0, 1, 2], (
            "two holders got the same slot index, or a slot was skipped. The counted "
            "half of the semaphore is what bounds the CREDENTIAL, and it must allocate "
            "each slot exactly once."
        )
        assert len(refused) == 3 and all(isinstance(e, SeamSlotHeld) for e in refused), (
            "the second claimant for each seam was refused for the wrong reason: at "
            "1/3, 2/3 and 3/3 the lane had capacity for SOMEBODY, so the refusal is "
            "per-agent, never the ceiling."
        )
        assert probe_slots(base, ceiling).free == 0
    finally:
        for semaphore in held:
            semaphore.release()


def test_N_THE_TAG_IS_DISPLAY_ONLY_and_TRUNCATED_ON_ACQUIRE(base):
    """The Gate-2-BLOCK-if-built defect, closed and then proven closed.

    § 9.6 first reached for *"each held slot TAGGED with its claiming agent seam"* as
    the EXCLUSION mechanism. Reading content to decide a fire rebuilds the assert-style
    lockfile G-1 dissolved: stale content outlives the lock, the window between acquire
    and tag-write is untagged, and scan-then-claim is TOCTOU. So the tag is written, and
    it is *diagnostic*: a stale tag must not survive one handover, and — the load-bearing
    half — a slot whose tag says `star-lord` while nobody holds it must not refuse
    star-lord.
    """
    first = SeamSlotSemaphore(base, "star-lord", ceiling=1).acquire()
    slot = slot_lock_path(base, 0)
    assert "seam=star-lord" in slot.read_text(encoding="utf-8")
    first.release()

    # THE LOCK IS GONE; THE TEXT REMAINS. Anything that read this file to decide would
    # now refuse star-lord on the word of a dead holder.
    assert "seam=star-lord" in slot.read_text(encoding="utf-8")
    assert probe_slots(base, 1).free == 1, (
        "a released slot read as HELD because its tag still names a seam. That is the "
        "lockfile-whose-contents-are-the-claim primitive, rebuilt."
    )

    second = SeamSlotSemaphore(base, "elrond", ceiling=1).acquire()
    try:
        text = slot.read_text(encoding="utf-8")
        assert "seam=elrond" in text and "star-lord" not in text, (
            "the previous holder's tag survived a handover. Truncate-on-acquire is what "
            "keeps the human-readable half honest."
        )
    finally:
        second.release()


def test_N_NOTHING_EVER_BLOCKS_so_the_nesting_CANNOT_DEADLOCK(base):
    """`LOCK_NB` everywhere — stated as a property, measured as a duration.

    A fixed acquisition order (seam, then slot) is only safe because no step waits. If
    either flock ever became blocking, this row would hang rather than fail, so the
    assertion is a WALL-CLOCK bound: a refused claim returns in milliseconds, not when
    somebody else finishes.
    """
    holder = SeamSlotSemaphore(base, "star-lord", ceiling=1).acquire()
    try:
        started = time.monotonic()
        with pytest.raises(SeamSlotHeld):
            SeamSlotSemaphore(base, "star-lord", ceiling=1).acquire()
        with pytest.raises(LaneCeilingReached):
            SeamSlotSemaphore(base, "elrond", ceiling=1).acquire()
        assert time.monotonic() - started < 2.0, (
            "a refused acquisition took seconds — something WAITED. Every lock here is "
            "LOCK_NB precisely so that the nesting has no cycle to close."
        )
    finally:
        holder.release()


def test_N_A_REFUSED_CEILING_CLAIM_GIVES_THE_SEAM_LOCK_BACK(base):
    """A refusal that keeps holding something can wedge the lane it just declined.

    The ceiling check happens AFTER the per-seam lock is taken, so the failure path has
    to unwind it. If it did not, an agent refused once at a full lane could never fire
    again — its own seam lock would be held by nobody, forever.
    """
    others = [SeamSlotSemaphore(base, seam, ceiling=1).acquire() for seam in ("elrond",)]
    try:
        with pytest.raises(LaneCeilingReached):
            SeamSlotSemaphore(base, "star-lord", ceiling=1).acquire()
    finally:
        for semaphore in others:
            semaphore.release()
    # The seam lock is free: star-lord can fire the moment a slot opens.
    again = SeamSlotSemaphore(base, "star-lord", ceiling=1).acquire()
    again.release()


# ===========================================================================
# AMENDMENT O — the ceiling is the CREDENTIAL's; slot 4 enqueues
# ===========================================================================
def test_O_SLOT_FOUR_ENQUEUES_and_a_FULL_LANE_IS_OCCUPIED_NOT_CLOSED(base, fake_grok, tmp_path):
    """The fourth claimant does not wait, does not break a slot, and does not go Claude.

    § 10.3's composition, checked specifically: a Grok lane at 3/3 answers in the
    `busy-*` band = **OCCUPIED**, and step 4's Claude branch requires both vendors
    CLOSED. Matt's floor — Claude takes vendor-scoped work only when both vendors are
    closed — is not eroded by the ceiling, and this row is where that stays true.
    """
    from factory import lane_status as ls

    held = [SeamSlotSemaphore(base, seam).acquire() for seam in SEAMS]
    try:
        harness = _harness(fake_grok, base)
        state = harness.availability()
        assert state.ok is False and state.state == "busy"
        assert "ceiling" in state.reason.lower()

        # A fourth seam's job is REFUSED AT THE CLAIM — not queued inside the harness,
        # not retried, and with no vendor process launched.
        result = harness.run("hello", tmp_path, {"seam": "drax"})
        assert result.ok is False
        assert (result.extra or {}).get("lane_state") == "busy"
        assert not (tmp_path / "argv.json").exists()

        status = ls.lane_status(
            "grok", procs=[], lock_path=base,
            auth_probe=lambda: LaneAvailability(True, "open", "ok"),
        )
        assert status.state == ls.STATE_BUSY_LOCK
        assert status.state in ls.OCCUPIED_STATES and status.state not in ls.CLOSED_STATES, (
            "a full lane read CLOSED. That routes vendor-scoped work to Claude on "
            "CAPACITY alone, which inverts Matt's verbatim floor through a state that "
            "means 'the lane works and is busy'."
        )
    finally:
        for semaphore in held:
            semaphore.release()


def test_O_the_CEILING_IS_A_VALUE_so_a_DROP_TO_K_MINUS_1_is_not_a_code_change(base):
    """O.3: first 429 or degradation at k concurrent drops the operating ceiling to k-1.

    That has to be reachable without editing this package — otherwise the mechanical
    response to observed friction is a commit, and the response that actually happens
    at 22:00 is nothing.
    """
    assert GROK_SLOT_CEILING == 3
    two = SeamSlotSemaphore(base, "star-lord", ceiling=2).acquire()
    other = SeamSlotSemaphore(base, "elrond", ceiling=2).acquire()
    try:
        with pytest.raises(LaneCeilingReached):
            SeamSlotSemaphore(base, "drax", ceiling=2).acquire()
    finally:
        two.release()
        other.release()


# ===========================================================================
# SLOT RELEASE ON CHILD EXIT — including SIGKILL, PER SLOT
# ===========================================================================
_HOLD_SCRIPT = """
import sys, time
sys.path.insert(0, {parent!r})
from factory.lane import SeamSlotSemaphore
sem = SeamSlotSemaphore({base!r}, {seam!r}).acquire()
print("HELD", sem.slot_index, flush=True)
time.sleep(120)
"""


@pytest.mark.parametrize("slot_target", [0, 1, 2])
def test_a_SIGKILLED_HOLDER_RELEASES_ITS_SLOT_AND_ITS_SEAM(base, slot_target):
    """**PER SLOT**, because the ceiling is only as honest as its worst slot.

    `flock` was chosen over a PID file precisely so that there is no reaper to tune and
    no stale entry to clear: the kernel drops the lock when the last holder exits,
    including under SIGKILL where no userspace cleanup runs at all. Amendment N.2
    extends that to the per-seam lock — an agent that crashes mid-job must not be locked
    out of its own lane, which is a failure mode a hand-rolled registry would have.

    Parametrised over each slot index rather than testing slot 0 three times: the slots
    are separate files with separate descriptors, and "it works for the first one" is
    exactly the reading that lets slot 2 wedge quietly.
    """
    parent = str(Path(__file__).resolve().parents[2])
    # Fill the slots below the target so the child is forced onto `slot_target`.
    fillers = [SeamSlotSemaphore(base, seam).acquire()
               for seam in SEAMS[:slot_target]]
    try:
        script = _HOLD_SCRIPT.format(parent=parent, base=str(base), seam="drax")
        proc = subprocess.Popen(
            [sys.executable, "-c", script], start_new_session=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
        )
        try:
            line = proc.stdout.readline().strip()
            assert line == f"HELD {slot_target}", f"the child took {line!r}"
            assert probe_slots(base, GROK_SLOT_CEILING).free == GROK_SLOT_CEILING - slot_target - 1
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait(timeout=30)
        finally:
            if proc.poll() is None:  # pragma: no cover — only on an unexpected hang
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)

        deadline = time.time() + 30
        while probe_slots(base, GROK_SLOT_CEILING).free <= slot_target and time.time() < deadline:
            time.sleep(0.05)
        assert probe_slots(base, GROK_SLOT_CEILING).free == GROK_SLOT_CEILING - slot_target, (
            f"slot {slot_target} stayed HELD after its holder was SIGKILLed. That is the "
            "stale-lock failure `flock` was chosen to make impossible, and at the "
            "ceiling it silently narrows the lane by one for good."
        )
        # AND the seam: a crashed agent is not locked out of its own lane.
        recovered = SeamSlotSemaphore(base, "drax").acquire()
        recovered.release()
    finally:
        for semaphore in fillers:
            semaphore.release()


# ===========================================================================
# AMENDMENT Q — the busy check answers k/3, fails closed per slot, WRITES NOTHING
# ===========================================================================
def _status(base: Path, **kw):
    from factory import lane_status as ls

    return ls.lane_status(
        "grok", procs=kw.pop("procs", []), lock_path=base,
        auth_probe=lambda: LaneAvailability(True, "open", "ok"), **kw,
    )


def test_Q_the_check_reports_K_OVER_3_and_open_stays_SAFE_TO_FIRE(base):
    from factory import lane_status as ls

    answer = _status(base)
    assert answer.state == ls.STATE_OPEN
    assert answer.slots.to_dict() == {
        "total": 3, "held": 0, "free": 3, "unreadable": 0, "tags": [],
    }
    assert answer.safe_to_fire is True

    held = SeamSlotSemaphore(base, "star-lord").acquire()
    try:
        answer = _status(base)
        assert (answer.slots.held, answer.slots.free) == (1, 2)
        assert answer.state == ls.STATE_OPEN and answer.safe_to_fire is True, (
            "a lane with 2 free slots read as not-fire-safe. Under AM-3 partial "
            "occupancy is CAPACITY, not busyness."
        )
        # The `k/3` reaches a HUMAN too, on the one line the CLI prints — not only the
        # `--json` payload. § 11.3 sends a dispatcher to a screen before it sends them
        # to a parser.
        assert "2/3 free" in answer.one_line()
        assert answer.to_dict()["slots"]["held"] == 1
        assert answer.to_dict()["legs"]["lock"]["counted"] is True
    finally:
        held.release()


def test_Q4_OPEN_WITH_ZERO_FREE_SLOTS_IS_NOT_AN_EXPRESSIBLE_ANSWER(base):
    """Q.4, stated as an impossibility rather than as a convention.

    `SAFE_TO_FIRE_STATES` is unchanged, so if the shape could ever produce `open` with
    k=0 the predicate would say *fire* at a full credential — and the shape would be
    wrong, in jack-ryan's words. Swept over every occupancy the lane can reach.
    """
    from factory import lane_status as ls

    held: list[SeamSlotSemaphore] = []
    try:
        for n, seam in enumerate(SEAMS, start=1):
            held.append(SeamSlotSemaphore(base, seam).acquire())
            answer = _status(base)
            assert answer.slots.held == n
            if answer.slots.free == 0:
                assert answer.state == ls.STATE_BUSY_LOCK and not answer.safe_to_fire
            else:
                assert answer.safe_to_fire
        assert answer.state == ls.STATE_BUSY_LOCK
    finally:
        for semaphore in held:
            semaphore.release()


def test_Q1_AN_UNREADABLE_SLOT_COUNTS_HELD(base):
    """Fail-closed PER SLOT — leg 1 grew from one read to three and the union did not say.

    A slot that cannot be read is not a slot that is free. A partial read resolving
    toward free is the direction that fires a job at a lane nobody can see, and it is
    reachable by one wrong permission bit rather than by anything exotic.
    """
    slot = slot_lock_path(base, 1)
    slot.parent.mkdir(parents=True, exist_ok=True)
    slot.touch()
    slot.chmod(0o000)
    try:
        occupancy = probe_slots(base, 3)
        assert (occupancy.held, occupancy.free, occupancy.unreadable) == (1, 2, 1)
        assert any("UNREADABLE" in tag for tag in occupancy.tags), (
            "an unreadable slot counted held but said nothing about WHY. A full lane "
            "and a broken instrument want different responses from an operator."
        )
    finally:
        slot.chmod(0o644)


def test_Q1_NO_SLOT_READABLE_ANSWERS_BUSY_UNKNOWN_NOT_BUSY_LOCK(base):
    """Ambiguity, not capacity — and they are different INSTRUCTIONS.

    `busy-lock` says *enqueue behind it* (amber). `busy-unknown` says *somebody must
    fix the instrument* (red, exit 22). Reporting a blind leg as a full lane would tell
    an operator to wait for something that is never going to finish.
    """
    from factory import lane_status as ls

    base.parent.mkdir(parents=True, exist_ok=True)
    for index in range(3):
        path = slot_lock_path(base, index)
        path.touch()
        path.chmod(0o000)
    try:
        assert probe_slots(base, 3).all_unreadable is True
        answer = _status(base)
        assert answer.state == ls.STATE_BUSY_UNKNOWN
        assert answer.exit_code == 22 and not answer.safe_to_fire
    finally:
        for index in range(3):
            slot_lock_path(base, index).chmod(0o644)


def test_Q_the_check_WRITES_NOTHING_not_even_a_SLOT_FILE(base):
    """G-4 holds at three probes exactly as it held at one.

    `lane_is_free` opens with `O_CREAT`, so asking it three times would leave three
    files behind — a read-only status call creating state that outlives the question,
    which is THE LAW's failure mode arriving through the instrument built to uphold it.
    A slot file that does not exist cannot be held, and that answer is free.
    """
    before = sorted(p.name for p in base.parent.iterdir()) if base.parent.exists() else []
    answer = _status(base)
    after = sorted(p.name for p in base.parent.iterdir()) if base.parent.exists() else []
    assert answer.slots.free == 3
    assert before == after, (
        f"the busy check created files: {sorted(set(after) - set(before))}. A probe "
        "that writes converts a question into a side effect."
    )


def test_Q_the_CODEX_lane_grew_NO_SLOTS(base):
    """P-1 is a VENDOR LAW and § 9.5 probed xAI. Evidence does not travel across vendors."""
    from factory import lane_status as ls

    assert ls.LANES["codex"].slot_ceiling == 0
    assert ls.LANES["grok"].slot_ceiling == GROK_SLOT_CEILING
    answer = ls.lane_status(
        "codex", procs=[], lock_path=base,
        auth_probe=lambda: LaneAvailability(True, "open", "ok"),
    )
    assert answer.slots is None
    assert answer.to_dict()["slots"] is None


# ===========================================================================
# AMENDMENT R — the drain SKIPS and keeps going; a skip is NEVER an attempt
# ===========================================================================
def test_R_the_DRAIN_SKIPS_A_HELD_SEAM_AND_COMPLETES_THE_REST_OF_THE_QUEUE(
    base, fake_grok, tmp_path,
):
    """**R.2 — the head-of-line block, refused.** The head job's seam is busy; the queue
    still drains.

    Under the serial law a busy answer meant *the other drainer is doing this work*, so
    breaking was right. Under AM-3 a per-agent refusal is JOB-specific: breaking here
    would sit the lane at 1/3 with a full queue and two free slots, which inverts the
    amendment's own purpose. The job is not lost — its marker is `ENQUEUED`, which is
    non-terminal, so the next drain takes it.
    """
    queue = JobQueue(tmp_path / "q", lane="grok")
    _enqueue(queue, "a-head", seam="star-lord")
    _enqueue(queue, "b-second", seam="elrond")
    _enqueue(queue, "c-third", seam="galadriel")

    blocker = SeamSlotSemaphore(base, "star-lord").acquire()
    try:
        report = queue.drain(_harness(fake_grok, base))
    finally:
        blocker.release()

    assert report.fired == 2, (
        f"the drain fired {report.fired} job(s). One agent's in-flight job stopped the "
        "whole queue — head-of-line blocking, which R.2 refuses by name."
    )
    assert report.skipped_per_agent == 1
    assert report.handed_to_claude == 0
    assert [o.job_id for o in report.outcomes if o.skipped_reason] == ["a-head"]
    assert {o.job_id for o in report.outcomes if o.ok} == {"b-second", "c-third"}

    # FIFO is otherwise preserved, and the skipped job is still PENDING.
    assert [job.job_id for job in queue.pending()] == ["a-head"]

    # R.3 — countable from the surface that already exists, in G-7's shape.
    text = (tmp_path / "q" / "_run-log.tsv").read_text(encoding="utf-8")
    assert text.count(f"skipped={SKIPPED_PER_AGENT}") == 1, (
        "a queue that silently reorders is folklore; one that says why is evidence — "
        f'and `grep -c "skipped={SKIPPED_PER_AGENT}"` is the number the job-10 verdict '
        "conditions on."
    )
    assert all(len(row) == 6 for row in queue.runlog.rows()), "no schema change"


def test_R_A_SKIPPED_JOB_IS_NOT_AN_ATTEMPT_AND_NEVER_GOES_FALLBACK_CLAUDE(
    base, fake_grok, tmp_path,
):
    """**R.1 — the defect this file exists to keep closed, arriving through a new door.**

    `jobqueue.drain`'s standing comment records it being made once already: a transient
    lane condition reached `_run_one`, was counted as an ATTEMPT, and the job was handed
    PERMANENTLY to its Claude curator for something that clears by itself. Ownership
    moves once (P-7) — it does not come back. A per-agent refusal is the same shape with
    a different name, and this row is what stops it being re-made.

    Drained TWICE with the seam held and `max_attempts` exhausted-if-counted, because
    "not an attempt" is only meaningful if repetition cannot accumulate into one.
    """
    queue = JobQueue(tmp_path / "q", lane="grok")
    queue.enqueue(job_id="j", prompt="p", curator="galadriel", seam="star-lord",
                  sandbox="n/a", max_attempts=1)

    blocker = SeamSlotSemaphore(base, "star-lord").acquire()
    try:
        for _ in range(3):
            report = queue.drain(_harness(fake_grok, base))
            outcome = report.outcomes[0]
            assert outcome.skipped_reason == SKIPPED_PER_AGENT
            assert outcome.attempts == 0, (
                "the skip was counted as an attempt. With `max_attempts=1` that is one "
                "drain away from FALLBACK-CLAUDE, permanently, for a condition that "
                "clears when the agent's other job finishes."
            )
    finally:
        blocker.release()

    assert report.handed_to_claude == 0
    assert not (tmp_path / "q" / "fallback").exists(), (
        "a fallback manifest was written for a transient per-agent refusal. That spends "
        "the Claude lane on a condition that resolves in minutes AND moves ownership "
        "away from the vendor lane for good."
    )
    text = (tmp_path / "q" / "_run-log.tsv").read_text(encoding="utf-8")
    assert "FALLBACK-CLAUDE" not in text
    assert queue.is_done(queue.load("j")) is None, "a skipped job stopped being pending"

    # The seam is free now, so the SAME queue drains it — no re-enqueue, no manual step.
    assert queue.drain(_harness(fake_grok, base)).fired == 1


def test_R5_availability_STAYS_LANE_GLOBAL(base, fake_grok):
    """R.5 — `availability()` answers about the LANE, never about a job.

    Folding per-agent eligibility into the lane state is exactly what creates R.1: one
    agent's job would make the lane read busy to every other agent, and the drain's
    existing `break` would then do the wrong thing correctly.
    """
    harness = _harness(fake_grok, base)
    held = SeamSlotSemaphore(base, "star-lord").acquire()
    try:
        state = harness.availability()
        assert state.ok is True, (
            "one held seam closed the lane. Per-agent eligibility is evaluated per JOB "
            "at claim time; the lane is busy only when the CEILING is exhausted."
        )
        assert "2/3 free" in state.reason
    finally:
        held.release()


# ===========================================================================
# AMENDMENT P — the rows carry the interval, and the wait carries its reason
# ===========================================================================
def test_P_the_rows_carry_SLOTS_HELD_at_START_and_FINISH_plus_SLOT_INDEX(
    base, fake_grok, tmp_path,
):
    """P.1. `slots_held=` is a point sample at each end; the VERDICT joins the timestamps.

    Both ends are recorded because a job that starts alone and spends 90% of its life
    beside two others would otherwise be read as a solo row. The inclusivity differs by
    design and is pinned in MIGRATION § 11.4: at START this job holds nothing, at FINISH
    it holds its own slot, and each row states the literal truth about the lane at the
    instant it was written.
    """
    queue = JobQueue(tmp_path / "q", lane="grok")
    _enqueue(queue, "j", seam="star-lord")
    other = SeamSlotSemaphore(base, "elrond").acquire()
    try:
        assert queue.drain(_harness(fake_grok, base)).fired == 1
    finally:
        other.release()

    rows = {row[2]: row[3] for row in queue.runlog.rows()}
    assert "slots_held=1/3" in rows["START"], (
        f"the START row carries no ambient concurrency: {rows['START']!r}"
    )
    finish = next(detail for marker, detail in rows.items() if marker.startswith("rc="))
    assert "slots_held=2/3" in finish, (
        f"the finish row's `slots_held` is not inclusive of this job's own slot: "
        f"{finish!r}"
    )
    assert "slot_index=" in finish
    assert "seam=star-lord" in rows["START"]


def test_P2_the_WAIT_carries_its_REASON_and_the_two_causes_never_share_one_number(
    base, fake_grok, tmp_path,
):
    """P.2. § 9.5's banked countable measured ONE thing; under AM-3 it measures TWO.

    An ENQUEUED->START gap now means *the ceiling was full* or *this agent already had a
    job in flight* — different questions with different answers about whether N=3 is the
    right number. The reason is DERIVED from the job's own prior rows rather than
    carried in memory, because the drain that skipped a job is usually not the drain
    that runs it, and a number whose cause lived in a dead process is unattributable.
    """
    from factory.jobqueue import WAIT_REASONS

    queue = JobQueue(tmp_path / "q", lane="grok")
    _enqueue(queue, "j", seam="star-lord")

    blocker = SeamSlotSemaphore(base, "star-lord").acquire()
    try:
        queue.drain(_harness(fake_grok, base))     # skipped: per-agent
    finally:
        blocker.release()
    assert queue.drain(_harness(fake_grok, base)).fired == 1

    starts = [row[3] for row in queue.runlog.rows() if row[2] == "START"]
    assert len(starts) == 2
    assert "waited_reason=none" in starts[0], (
        f"the FIRST start claimed a cause before one existed: {starts[0]!r}"
    )
    assert "waited_reason=per-agent" in starts[1], (
        f"the second start did not attribute its wait: {starts[1]!r}. Attributing a "
        "per-agent skip to the ceiling would make the banking window's own evidence "
        "argue for changing N."
    )
    assert all("waited_ms=" in start for start in starts)
    for start in starts:
        reason = start.split("waited_reason=")[1].split()[0]
        assert reason in WAIT_REASONS, f"{reason!r} is outside the closed vocabulary"
