"""THE SERIAL LAW, the curator field, and the queue's durability — proven, not asserted.

Five things this file exists to make mechanical, in the order the dispatch ranks them:

1. **A second `codex exec` under the lock exits non-zero.** Including the tightened
   case Gate-1 named: ONE process spawning TWO children is the same violation as two
   processes, so a same-process second acquisition must fail too.
2. **Crash-and-resume is safe**, and the accepted failure mode is exhibited rather
   than described — a killed queue does NOT leave a lock that blocks a live lane, and
   a live orphaned child DOES hold it, which is the trade this build chose.
3. **Idempotent re-entry does not redo work.**
4. **The auth-expired path stops cleanly and surfaces**, without retrying a
   Matt-only condition and without writing into `canonical/matt_to_do/`.
5. **U-4 R-B: a job with no curator does not enqueue**, and the curator lands in
   `_run-log.tsv` at ENQUEUE time.

The fake `codex` executable below is a real subprocess emitting the real event
vocabulary. It is not a mock of the adapter: the thing under test is what happens at
the `subprocess.run` call site, and a mock replaces exactly that.
"""

from __future__ import annotations

import ast
import json
import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

from factory.harness.codex import CodexHarness, LaneAvailability
from factory.jobqueue import JobQueue
from factory.lane import (
    BUSY_MARKERS,
    TERMINAL_MARKERS,
    LaneBusy,
    RunLog,
    SerialLaneLock,
    is_terminal_marker,
    lane_is_free,
)

FACTORY_DIR = Path(__file__).resolve().parents[1]

#: A row from the PROVEN runner's `_run-log.tsv`, copied byte-for-byte
#: (`research/vfx-p2-dossiers/usage/_run-log.tsv`, last row of the 30-job VFX run).
#: This is the format contract that must not break while it is generalised, so it is
#: pinned as a literal rather than described.
PROVEN_TERMINAL_ROW = (
    "2026-08-24T14:03:40Z\t30-ma_video_companion\trc=0\t"
    "start=2026-08-24T13:59:39Z end=2026-08-24T14:03:40Z dossier_bytes=    3612"
)

_FAKE_CODEX = r'''#!/usr/bin/env python3
"""A fake `codex` that speaks the real event vocabulary. Not a mock of the adapter."""
import json, os, sys, time

argv = sys.argv[1:]
if argv[:2] == ["login", "status"]:
    print("Logged in using ChatGPT")
    sys.exit(0)

marker = os.environ.get("FAKE_CODEX_MARKER")
if marker:
    with open(marker, "a") as fh:
        fh.write("ran\n")

sys.stdin.read()
time.sleep(float(os.environ.get("FAKE_CODEX_SLEEP", "0")))

out = None
if "-o" in argv:
    out = argv[argv.index("-o") + 1]
body = os.environ.get("FAKE_CODEX_BODY", "x" * 800)
if out:
    with open(out, "w") as fh:
        fh.write(body)

rc = int(os.environ.get("FAKE_CODEX_RC", "0"))
print(json.dumps({"type": "thread.started", "thread_id": "fake-thread"}))
print(json.dumps({"type": "turn.started"}))
if rc == 0:
    print(json.dumps({"type": "item.completed",
                      "item": {"type": "agent_message", "text": body[:40]}}))
    print(json.dumps({"type": "turn.completed", "usage": {
        "input_tokens": 1000, "cached_input_tokens": 600,
        "cache_write_input_tokens": 0, "output_tokens": 50,
        "reasoning_output_tokens": 20}}))
else:
    print(json.dumps({"type": "turn.failed", "error": {"message": "fake failure"}}))
sys.stderr.write("ERROR codex_models_manager: failed to load models cache\n")
sys.exit(rc)
'''


@pytest.fixture
def fake_codex(tmp_path: Path) -> Path:
    path = tmp_path / "fake-codex"
    path.write_text(_FAKE_CODEX, encoding="utf-8")
    path.chmod(0o755)
    return path


@pytest.fixture
def lock_path(tmp_path: Path) -> Path:
    return tmp_path / "lane.lock"


def _harness(fake_codex: Path, lock_path: Path) -> CodexHarness:
    return CodexHarness(
        executable=str(fake_codex),
        lock_path=lock_path,
        auth_probe=lambda: LaneAvailability(True, "open", "Logged in using ChatGPT"),
    )


def _enqueue(queue: JobQueue, job_id: str, curator: str = "elrond", **kw) -> None:
    queue.enqueue(
        job_id=job_id,
        prompt=f"do {job_id}",
        curator=curator,
        output_path=str(queue.root / "out" / f"{job_id}.md"),
        min_output_bytes=kw.pop("min_output_bytes", 500),
        **kw,
    )


# ===========================================================================
# 1 — THE SERIAL LAW
# ===========================================================================
def test_a_SECOND_codex_exec_under_the_lock_EXITS_NONZERO(lock_path):
    """The row Gate-2 asked for by name.

    A real second process, a real `flock` attempt, a real non-zero exit, and a
    refusal that SAYS WHY. Not `assert lock.locked()` — the question is what a second
    launcher observes, and the only honest way to observe it is to be one.
    """
    holder = SerialLaneLock(lock_path).acquire()
    try:
        proc = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(f"""
                import sys
                sys.path.insert(0, {str(FACTORY_DIR.parent)!r})
                from factory.lane import SerialLaneLock, LaneBusy
                try:
                    SerialLaneLock({str(lock_path)!r}).acquire()
                except LaneBusy as exc:
                    sys.stderr.write(str(exc))
                    sys.exit(3)
                sys.exit(0)
            """)],
            capture_output=True, text=True, timeout=60,
        )
    finally:
        holder.release()
    assert proc.returncode != 0, (
        "a second launcher took the lane. THE SERIAL LAW is an OpenAI CI/CD-auth "
        "precondition, not a preference: one auth.json, one job stream."
    )
    assert proc.returncode == 3
    assert "SERIAL LAW" in proc.stderr
    assert "NEVER parallel" in proc.stderr


def test_ONE_PROCESS_cannot_hold_the_lane_TWICE(lock_path):
    """Gate-1's tightening, and the measured fact the whole design rests on.

    `flock` is widely described as per-PROCESS, which would make this pass by
    accident and make a single drain loop able to spawn two children legally. It is
    not: the lock is held by the OPEN FILE DESCRIPTION, so a second `open()` in the
    same process conflicts (errno 35, measured on Darwin 24.6.0, 2026-08-24). That is
    why `acquire()` opens a fresh descriptor every time and never caches one.

    If this row ever reds, the exclusion has silently degraded from "one `codex exec`"
    to "one queue process", which is precisely the weaker guarantee Gate-1 refused.
    """
    first = SerialLaneLock(lock_path).acquire()
    try:
        with pytest.raises(LaneBusy):
            SerialLaneLock(lock_path).acquire()
    finally:
        first.release()
    assert lane_is_free(lock_path)


def test_the_harness_DOES_NOT_LAUNCH_codex_when_the_lane_is_held(
    fake_codex, lock_path, tmp_path, monkeypatch
):
    """The exclusion is at the INVOCATION SITE, proven by the absence of an invocation.

    A refusal that still ran the vendor CLI would be a log line, not a lock. The fake
    `codex` appends to a marker file the instant it starts, so this row asserts the
    marker was never written — the strongest available statement that nothing ran.
    """
    marker = tmp_path / "ran.txt"
    monkeypatch.setenv("FAKE_CODEX_MARKER", str(marker))
    harness = _harness(fake_codex, lock_path)

    holder = SerialLaneLock(lock_path).acquire()
    try:
        result = harness.run("prompt", tmp_path, {})
    finally:
        holder.release()

    assert result.ok is False
    assert "SERIAL LAW" in (result.error or "")
    assert not marker.exists(), (
        "the vendor CLI was launched while the lane was held. The refusal fired after "
        "the violation, which is a report and not a lock."
    )
    assert result.usage.absent_reason == "harness never launched: lane busy"


def test_the_lock_fd_is_INHERITED_by_the_child(fake_codex, lock_path, tmp_path):
    """The crash-safety line, asserted rather than trusted to a comment.

    `pass_fds` is what makes the lock's lifetime equal the CHILD's rather than the
    parent's. Without it, a killed queue whose `codex exec` survives leaves the lane
    UNLOCKED while a job is still running against `auth.json` — the double-fire the
    serial law forbids, arriving through the crash path instead of the happy one.
    """
    import inspect

    source = inspect.getsource(CodexHarness.run)
    assert "pass_fds=(lock.fd,)" in source, (
        "the lock descriptor is no longer passed to the child. See the module "
        "docstring's crash-failure-mode note: removing this converts the ACCEPTED "
        "failure (a live orphan holds the lane) into the REFUSED one (a live orphan "
        "runs on an unlocked lane)."
    )
    # And the mechanism itself works on this host.
    lock = SerialLaneLock(lock_path).acquire()
    try:
        proc = subprocess.run(
            [sys.executable, "-c", f"import os; os.fstat({lock.fd}); print('visible')"],
            pass_fds=(lock.fd,), capture_output=True, text=True, timeout=60,
        )
    finally:
        lock.release()
    assert proc.stdout.strip() == "visible"


# ===========================================================================
# 2 — CRASH AND RESUME
# ===========================================================================
def _drain_script(root: Path, fake_codex: Path, lock_path: Path) -> str:
    return textwrap.dedent(f"""
        import sys
        sys.path.insert(0, {str(FACTORY_DIR.parent)!r})
        from factory.jobqueue import JobQueue
        from factory.harness.codex import CodexHarness, LaneAvailability
        h = CodexHarness(
            executable={str(fake_codex)!r},
            lock_path={str(lock_path)!r},
            auth_probe=lambda: LaneAvailability(True, "open", "ok"),
        )
        JobQueue({str(root)!r}).drain(h)
    """)


def test_a_KILLED_queue_leaves_NO_STALE_LOCK(tmp_path, fake_codex, lock_path, monkeypatch):
    """The failure mode I REFUSED: a dead process's lock outliving it.

    The whole reason `flock` was chosen over a PID file. Kill the queue AND its child
    (the process group) and the lane is free the instant the last holder exits — with
    no reaper to tune, no PID to go stale, and no `--force` for an impatient operator
    to reach for.
    """
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-slow")

    env = {**os.environ, "FAKE_CODEX_SLEEP": "30"}
    proc = subprocess.Popen(
        [sys.executable, "-c", _drain_script(root, fake_codex, lock_path)],
        env=env, start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 30
        while lane_is_free(lock_path) and time.time() < deadline:
            time.sleep(0.05)
        assert not lane_is_free(lock_path), "the drain never took the lane"
        # SIGKILL: no userspace cleanup runs at all, which is the point.
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        proc.wait(timeout=30)
    finally:
        if proc.poll() is None:  # pragma: no cover - only on an unexpected hang
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)

    deadline = time.time() + 30
    while not lane_is_free(lock_path) and time.time() < deadline:
        time.sleep(0.05)
    assert lane_is_free(lock_path), (
        "a SIGKILLed queue left the lane locked. That is the stale-lock failure this "
        "design refused; a lock file that outlives its holder wedges the lane forever."
    )
    # And the crash is VISIBLE: the last row is START, not terminal, so the pre-fire
    # check reads "do not fire" rather than "idle".
    assert queue.runlog.is_idle() is False
    assert queue.runlog.last_row()[2] == "START"


def test_a_LIVE_ORPHANED_child_STILL_HOLDS_the_lane(tmp_path, fake_codex, lock_path):
    """The failure mode I ACCEPTED, exhibited rather than described.

    Kill ONLY the queue and leave its `codex exec` running: the lane stays held. That
    is deliberate — that process is genuinely using `auth.json`, and releasing the lane
    for it would be the double-fire. A wedged lane is loud (`ps` names the holder, the
    run log's last row is non-terminal) and fails CLOSED. The alternative fails open
    and silently.
    """
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-slow")

    env = {**os.environ, "FAKE_CODEX_SLEEP": "30"}
    proc = subprocess.Popen(
        [sys.executable, "-c", _drain_script(root, fake_codex, lock_path)],
        env=env, start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    pgid = os.getpgid(proc.pid)
    try:
        deadline = time.time() + 30
        while lane_is_free(lock_path) and time.time() < deadline:
            time.sleep(0.05)
        assert not lane_is_free(lock_path)
        proc.kill()          # the QUEUE only; the child is orphaned and keeps running
        proc.wait(timeout=30)
        time.sleep(0.5)
        assert not lane_is_free(lock_path), (
            "the lane was released while an orphaned `codex exec` was still running "
            "against auth.json. This is the ACCEPTED trade going the wrong way."
        )
    finally:
        os.killpg(pgid, signal.SIGKILL)


def test_RESUME_after_a_crash_completes_the_job(tmp_path, fake_codex, lock_path):
    """Re-entry after a crash is SAFE and it FINISHES THE WORK.

    An interrupted job has a `START` row and no terminal row, so `is_done` says no and
    the next drain runs it. State lives on disk; nothing was held in the dead
    process's memory.
    """
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-slow")

    env = {**os.environ, "FAKE_CODEX_SLEEP": "30"}
    proc = subprocess.Popen(
        [sys.executable, "-c", _drain_script(root, fake_codex, lock_path)],
        env=env, start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 30
        while lane_is_free(lock_path) and time.time() < deadline:
            time.sleep(0.05)
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        proc.wait(timeout=30)
    finally:
        if proc.poll() is None:  # pragma: no cover
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    deadline = time.time() + 30
    while not lane_is_free(lock_path) and time.time() < deadline:
        time.sleep(0.05)

    assert [j.job_id for j in queue.pending()] == ["01-slow"]
    report = JobQueue(root).drain(_harness(fake_codex, lock_path))
    assert report.fired == 1
    assert queue.runlog.is_idle() is True
    assert queue.pending() == []


# ===========================================================================
# 3 — IDEMPOTENT RE-ENTRY
# ===========================================================================
def test_a_REFIRED_queue_does_not_redo_completed_work(tmp_path, fake_codex, lock_path, monkeypatch):
    marker = tmp_path / "ran.txt"
    monkeypatch.setenv("FAKE_CODEX_MARKER", str(marker))
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a")
    _enqueue(queue, "02-b")

    first = queue.drain(_harness(fake_codex, lock_path))
    assert first.fired == 2
    assert marker.read_text().count("ran") == 2

    second = queue.drain(_harness(fake_codex, lock_path))
    assert second.fired == 0
    assert marker.read_text().count("ran") == 2, (
        "a re-fired queue re-ran completed jobs. The proven runner's idempotency is "
        "the reason a 30-job wave could be resumed at all."
    )


def test_re_ENQUEUEING_the_same_job_does_not_duplicate_the_liveness_row(tmp_path):
    queue = JobQueue(tmp_path / "q")
    _enqueue(queue, "01-a")
    rows_before = len(list(queue.runlog.rows()))
    _enqueue(queue, "01-a")
    assert len(list(queue.runlog.rows())) == rows_before, (
        "a re-fired enqueue script grew the run log. Duplicate rows make the "
        "terminal-row liveness check answer for the wrong firing."
    )
    with pytest.raises(ValueError, match="DIFFERENT terms"):
        queue.enqueue(job_id="01-a", prompt="something else", curator="elrond")


def test_output_that_already_exists_is_SKIPPED_the_proven_runners_way(
    tmp_path, fake_codex, lock_path, monkeypatch
):
    """The runner's `dossier exists and > 500 bytes` test, generalised and kept.

    Kept alongside the stronger run-log test because it is the one that makes a
    Claude-lane fallback safe: if the curator's agent does the work by hand, a later
    Codex drain must not produce the artifact a second time.
    """
    marker = tmp_path / "ran.txt"
    monkeypatch.setenv("FAKE_CODEX_MARKER", str(marker))
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a")
    out = root / "out" / "01-a.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("y" * 900, encoding="utf-8")

    report = queue.drain(_harness(fake_codex, lock_path))
    assert report.skipped == 1
    assert report.fired == 0
    assert not marker.exists()
    assert queue.runlog.last_row()[2] == "SKIP-EXISTS"


# ===========================================================================
# 4 — AUTH HEALTH AS A FIRST-CLASS QUEUE STATE
# ===========================================================================
def test_EXPIRED_AUTH_stops_the_queue_surfaces_it_and_does_NOT_retry(
    tmp_path, fake_codex, lock_path, monkeypatch
):
    marker = tmp_path / "ran.txt"
    monkeypatch.setenv("FAKE_CODEX_MARKER", str(marker))
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", curator="elrond")
    _enqueue(queue, "02-b", curator="galadriel")

    expired = CodexHarness(
        executable=str(fake_codex), lock_path=lock_path,
        auth_probe=lambda: LaneAvailability(
            False, "auth_expired",
            "re-authentication is a MATT-ONLY action and must not be retried",
        ),
    )
    report = queue.drain(expired)

    assert report.lane_state == "auth_expired"
    assert not marker.exists(), "the queue fired jobs against a closed lane"

    # It SURFACES: run log, telemetry, and a ready-to-file row.
    assert queue.runlog.last_row()[2] in TERMINAL_MARKERS
    blocked = [e for e in queue.telemetry.events() if e["event"] == "lane_blocked"]
    assert len(blocked) == 1
    assert blocked[0]["outcome"] == "auth_blocked"
    assert blocked[0]["passthrough"]["matt_only_action"] is True
    note = root / "AUTH-BLOCKED.md"
    assert note.exists() and "matt_to_do" in note.read_text()

    # THE CHOICE, ASSERTED: the queue writes a DRAFT, it does not file it.
    assert "NOT filed" in note.read_text()
    assert not (Path(__file__).resolve().parents[3] / "canonical" / "matt_to_do"
                / "AUTH-BLOCKED.md").exists()

    # And work is not idled: both jobs are handed to their NAMED curators.
    handoffs = {p.stem: json.loads(p.read_text()) for p in (root / "fallback").glob("*.json")}
    assert set(handoffs) == {"01-a", "02-b"}
    assert handoffs["01-a"]["job"]["curator"] == "elrond"
    assert handoffs["02-b"]["job"]["curator"] == "galadriel"


def test_a_FAILED_job_is_handed_to_the_named_curator_not_retried_forever(
    tmp_path, fake_codex, lock_path, monkeypatch
):
    monkeypatch.setenv("FAKE_CODEX_RC", "1")
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", curator="legolas")
    report = queue.drain(_harness(fake_codex, lock_path))

    assert report.handed_to_claude == 1
    assert queue.runlog.last_row()[2] == "FALLBACK-CLAUDE"
    manifest = json.loads((root / "fallback" / "01-a.json").read_text())
    assert manifest["job"]["curator"] == "legolas"
    assert "no re-litigating" in manifest["posture"]
    # Terminal: ownership moves ONCE. A later drain must not produce the artifact twice.
    assert queue.pending() == []


def test_a_BUSY_lane_DEFERS_and_NEVER_hands_the_job_to_claude(
    tmp_path, fake_codex, lock_path, monkeypatch
):
    """A busy lane is transient. Spending Claude tokens on it is the wrong answer.

    Written the other way first, and the LIVE round-trip is what surfaced it: `drain`
    proceeded on `busy`, `harness.run` refused with `LaneBusy`, and that refusal was
    counted as a failed ATTEMPT — so a job whose only problem was that another drainer
    held the lane for ten seconds got a terminal `FALLBACK-CLAUDE` row and a handoff
    manifest. The serial law says "queue behind it or fire the Claude lane"; a
    DRAINER's answer is the first, because the other drainer is already doing the work.

    Both paths are exercised: the pre-check (lane busy before the loop reaches the job)
    and the race window (busy only by the time the harness launched).
    """
    marker = tmp_path / "ran.txt"
    monkeypatch.setenv("FAKE_CODEX_MARKER", str(marker))
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", curator="elrond")

    holder = SerialLaneLock(lock_path).acquire()
    try:
        report = queue.drain(_harness(fake_codex, lock_path))
    finally:
        holder.release()

    assert report.lane_state == "busy"
    assert report.handed_to_claude == 0, (
        "a transient busy lane produced a permanent Claude-lane handoff"
    )
    assert not (root / "fallback").exists()
    assert not marker.exists()
    # The job is STILL PENDING, and the next drain finishes it.
    assert [j.job_id for j in queue.pending()] == ["01-a"]
    assert queue.drain(_harness(fake_codex, lock_path)).fired == 1


def test_the_RACE_WINDOW_between_the_precheck_and_the_launch_also_DEFERS(
    tmp_path, fake_codex, lock_path
):
    """Free when asked, taken by the time we launched — the window a probe cannot close.

    `availability()` is advisory by construction. This row drives the path where it
    said yes and the lock said no, and asserts the job returns to PENDING with its
    START row answered rather than dangling as a job that began and never ended.
    """
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", curator="elrond")

    harness = _harness(fake_codex, lock_path)
    holder: list[SerialLaneLock] = []

    class _TakesTheLaneAfterTheProbe:
        """Reports the lane free, then takes it before `run` can."""

        def availability(self):
            return harness.availability()

        def run(self, prompt, cwd, config):
            if not holder:
                holder.append(SerialLaneLock(lock_path).acquire())
            return harness.run(prompt, cwd, config)

    try:
        report = queue.drain(_TakesTheLaneAfterTheProbe())
    finally:
        for lock in holder:
            lock.release()

    assert report.deferred == 1
    assert report.handed_to_claude == 0
    rows = [r for r in queue.runlog.rows() if r[1] == "01-a"]
    assert [r[2] for r in rows] == ["ENQUEUED", "START", "ENQUEUED"]
    assert rows[-1][5] == "event=defer"
    assert queue.runlog.is_idle() is False, "a pending job means the lane has work"
    assert [j.job_id for j in queue.pending()] == ["01-a"]


def test_JUNK_OUTPUT_is_judged_by_the_job_class_criterion(
    tmp_path, fake_codex, lock_path, monkeypatch
):
    monkeypatch.setenv("FAKE_CODEX_BODY", "tiny")
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", min_output_bytes=500)
    report = queue.drain(_harness(fake_codex, lock_path))
    assert report.handed_to_claude == 1
    assert "below the job class's declared floor" in (report.outcomes[0].error or "")


# ===========================================================================
# 5 — U-4 R-B: THE CURATOR IS ENQUEUE-TIME SCHEMA
# ===========================================================================
def test_RB_a_job_with_no_curator_does_not_enqueue(tmp_path):
    """The governance line, made a refusal instead of an assertion.

    R-B, verbatim: *"A job whose curator field is empty is a REFUSAL TO FIRE, not a
    job to be reconciled later."* So this asserts more than the exception: it asserts
    that NOTHING was written. A refusal that leaves a job record behind is a job
    someone will find and fire.

    NOTE FOR `tests/test_vocabularies.py`: this row is the covering row for
    `jobqueue.REQUIRED_JOB_FIELDS`. Deleting `"curator"` from that set reds it.
    """
    queue = JobQueue(tmp_path / "q")
    for empty in ("", "   ", None):
        with pytest.raises(ValueError, match="REFUSAL TO FIRE"):
            queue.enqueue(job_id="01-a", prompt="do it", curator=empty)
    assert not queue.job_path("01-a").exists()
    assert not queue.prompt_path("01-a").exists()
    assert list(queue.runlog.rows()) == [], (
        "a curator-less job left a row in the surface the governance criterion is "
        "queried from. The query would then count a leak as a job."
    )


def test_the_OTHER_required_fields_are_refused_from_the_same_closed_set(tmp_path):
    """`REQUIRED_JOB_FIELDS` DRIVES the refusal; it does not merely describe it.

    Its first version named the requirement in an error message while three hardcoded
    conditions did the enforcing — a constant that could be edited without changing
    behaviour, which is the shape `test_vocabularies.py` calls a label. These rows are
    what make deleting a member of that set red something.
    """
    queue = JobQueue(tmp_path / "q")
    with pytest.raises(ValueError, match="empty job_id"):
        queue.enqueue(job_id="", prompt="do it", curator="elrond")
    with pytest.raises(ValueError, match="empty prompt"):
        queue.enqueue(job_id="01-a", prompt="   ", curator="elrond")
    assert list(queue.runlog.rows()) == []


def test_RB_the_curator_lands_in_the_run_log_AT_ENQUEUE_not_at_close(tmp_path, fake_codex, lock_path):
    """Enqueue-time, not close-time, is the whole point.

    A curator recorded at close is one chosen AFTER seeing the output, which is an
    endorsement rather than a control. So the assertion is about WHICH ROW carries the
    name, not merely that some row does.
    """
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", curator="elrond")

    first = list(queue.runlog.rows())[0]
    assert first[2] == "ENQUEUED"
    assert first[5] == "event=enqueue"
    assert first[4] == "curator=elrond", (
        "the curator is not on the ENQUEUE row. R-B is enqueue-time schema, not a "
        "later add — this is the difference between a commitment and a signature."
    )
    assert queue.curator_at_enqueue("01-a") == "elrond"

    queue.drain(_harness(fake_codex, lock_path))
    # Every row for this job names the same curator; the query is answerable by cut.
    for row in queue.runlog.rows():
        if row[1] == "01-a":
            assert row[4] == "curator=elrond"


def test_RB_the_run_log_cannot_be_given_a_curatorless_enqueue_row_by_ANY_caller(tmp_path):
    """Defence in depth: the refusal is not only in `enqueue`.

    `_run-log.tsv` is the surface R-B's empirical criterion is queried from ("zero
    governance leaks", falsifiable by query rather than by memory). A second writer
    able to append a curator-less enqueue row would make that query answer for a
    corpus it does not cover.
    """
    log = RunLog(tmp_path / "_run-log.tsv")
    with pytest.raises(ValueError, match="R-B"):
        log.append(job_id="x", marker="ENQUEUED", event="enqueue", curator="")


# ===========================================================================
# 6 — THE LIVENESS SURFACE (do not break `tail -1`)
# ===========================================================================
def test_the_PROVEN_runners_row_still_reads_as_TERMINAL(tmp_path):
    """The generalised format must not break the check KR and the U-4 router read."""
    path = tmp_path / "_run-log.tsv"
    path.write_text(PROVEN_TERMINAL_ROW + "\n", encoding="utf-8")
    log = RunLog(path)
    assert log.is_idle() is True
    row = log.last_row()
    assert len(row) == 4, "the proven runner's rows are four columns; they are read as-is"
    assert row[2] == "rc=0"
    assert log.curator_of("30-ma_video_companion") is None, (
        "a four-column row has an UNKNOWN curator, not an empty one. A leak query "
        "that conflates the two miscounts the pre-R-B corpus."
    )


def test_the_terminal_check_is_answerable_by_TAIL_MINUS_1_AND_CUT(tmp_path, fake_codex, lock_path):
    """`tail -1 | cut -f3` — the human path, run as a shell pipeline, not simulated."""
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a")
    queue.drain(_harness(fake_codex, lock_path))

    out = subprocess.run(
        f"tail -1 {queue.runlog.path} | cut -f3",
        shell=True, capture_output=True, text=True,
    ).stdout.strip()
    assert out == "rc=0"
    assert is_terminal_marker(out)

    curator = subprocess.run(
        f"tail -1 {queue.runlog.path} | cut -f5",
        shell=True, capture_output=True, text=True,
    ).stdout.strip()
    assert curator == "curator=elrond"


def test_an_UNKNOWN_marker_is_NOT_terminal(tmp_path):
    """Fail CLOSED. An unrecognised state reads as "do not fire", never as "idle"."""
    assert is_terminal_marker("SOMETHING-NOBODY-ENUMERATED") is False
    for marker in BUSY_MARKERS:
        assert is_terminal_marker(marker) is False
    for marker in TERMINAL_MARKERS:
        assert is_terminal_marker(marker) is True

    path = tmp_path / "_run-log.tsv"
    path.write_text("a truncated line with no tabs\n", encoding="utf-8")
    assert RunLog(path).is_idle() is False, (
        "an unreadable liveness surface answered 'safe'. Absence of evidence is not a "
        "pass — that is the substitution this whole package exists to refuse."
    )


def test_an_EMPTY_or_ABSENT_log_is_idle(tmp_path):
    assert RunLog(tmp_path / "nope.tsv").is_idle() is True
    (tmp_path / "empty.tsv").write_text("", encoding="utf-8")
    assert RunLog(tmp_path / "empty.tsv").is_idle() is True


def test_no_field_may_smuggle_a_TAB_into_the_liveness_surface(tmp_path):
    log = RunLog(tmp_path / "_run-log.tsv")
    log.append(job_id="a\tb", marker="rc=0", detail="x\ty\nz", curator="c\td", event="finish")
    row = log.last_row()
    assert len(row) == 6, "a field with a tab in it silently added a column"


def test_a_marker_NOBODY_ENUMERATED_cannot_be_WRITTEN(tmp_path):
    """Column 3 is a CLOSED vocabulary at write time, not only at read time.

    `is_terminal_marker` already reads an unknown marker as non-terminal, which is
    fail-closed and is not enough: a human running `tail -1` and seeing `DONE` reads
    it as done. The refusal is what keeps the file's words and its semantics the same
    words.
    """
    log = RunLog(tmp_path / "_run-log.tsv")
    with pytest.raises(ValueError, match="neither TERMINAL_MARKERS nor BUSY_MARKERS"):
        log.append(job_id="x", marker="DONE", event="finish", curator="elrond")
    for marker in ("rc=0", "rc=137", *TERMINAL_MARKERS, *BUSY_MARKERS):
        log.append(job_id="x", marker=marker, event="finish", curator="elrond")


# ===========================================================================
# 7 — TELEMETRY: U-1(a) FROM BIRTH, WITHOUT FREEZING U-1's SCHEMA
# ===========================================================================
def test_the_minimum_grain_is_PRESENT_across_the_lifecycle(tmp_path, fake_codex, lock_path):
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", curator="elrond")
    queue.drain(_harness(fake_codex, lock_path))
    events = queue.telemetry.events()

    assert [e["event"] for e in events] == ["enqueue", "start", "finish"]
    for event in events:
        assert event["schema_version"].startswith("reincarnated.lane.telemetry/")
        assert "passthrough" in event, (
            "a record with no passthrough freezes the shape. The U-1 axes are Matt's "
            "F-1…F-8 to rule; this file's job is to make the facts FINDABLE later."
        )
        assert event["job_id"] == "01-a"
        assert event["curator"] == "elrond"
        assert event["ts_utc"].endswith("Z")

    finish = events[-1]
    assert finish["exit_code"] == 0
    assert finish["model"]
    assert finish["reasoning_effort"] == "xhigh"
    assert finish["outcome"] == "ok"
    assert finish["usage"]["cache_read_tokens"] == 600
    assert finish["usage"]["input_tokens"] == 400, (
        "cached_input_tokens is a SUBSET of input_tokens; passing the vendor's number "
        "through unchanged double-counts the cache (93% over-report on the VFX run)"
    )


def test_ABSENT_facts_are_OMITTED_never_zero_filled(tmp_path):
    from factory.lane import Telemetry

    tel = Telemetry(tmp_path / "t.jsonl")
    record = tel.emit("start", lane="codex", job_id="a", curator="b", exit_code=None)
    assert "exit_code" not in record, "absent is absent; a None became a field"


def test_DISCIPLINE_73_no_lane_module_reads_a_dispatch_Status_header():
    """Work state is DERIVED from a completion record plus git. Never asserted by a field.

    Measured defect (jack-ryan, 2026-08-24): across 197 dispatch files, 99 carry no
    `Status:` header at all, and of the 31 reading open/pending, 14 are contradicted by
    a substantive completion record in the SAME file. A lane that read that field would
    republish a corpus-wide stale claim into a data path — THE LAW's failure mode
    arriving through the front door.

    Checked over non-docstring string constants, because the modules DESCRIBE the rule
    in prose and a scan that cannot tell a law from its violation would force the law
    to go unwritten.
    """
    forbidden = ("dispatches/", "**Status:**", "Status:")
    offenders: list[str] = []
    for rel in ("lane.py", "jobqueue.py", "harness/codex.py"):
        tree = ast.parse((FACTORY_DIR / rel).read_text(encoding="utf-8"))
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                body = getattr(node, "body", None) or []
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                        and isinstance(body[0].value.value, str):
                    docstrings.add(id(body[0].value))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                    and id(node) not in docstrings:
                for needle in forbidden:
                    if needle in node.value:
                        offenders.append(f"{rel}:{node.lineno}: {node.value[:80]!r}")
    assert not offenders, (
        "a lane module carries a dispatch-status reference in executable code:\n"
        + "\n".join(offenders)
    )


def test_the_lane_speaks_only_about_LANE_state_never_about_WORK_state():
    """The other half of Discipline #73, on the emission side.

    A marker vocabulary containing `COMPLETE` or `SEALED` would let a board render a
    work-state claim off lane data — which is the same projection through a different
    door. Every marker this lane can write is a statement about a JOB ON A LANE.
    """
    work_state_terms = {"SEALED", "COMPLETE", "CLOSED", "IN-PROGRESS", "PENDING", "OPEN", "BLOCKED"}
    assert not (TERMINAL_MARKERS | BUSY_MARKERS) & work_state_terms


# ===========================================================================
# 8 — THE ROUND-TRIP, on the fake lane
# ===========================================================================
def test_ROUND_TRIP_enqueue_drain_RawResult_receipts_and_liveness(
    tmp_path, fake_codex, lock_path
):
    """enqueue -> serial drain -> RawResult -> usage recorded -> terminal row.

    The field-presence check the Principle-6 gate asks for, on RawResult's `usage`,
    `model` and `exit_code`, plus the `_run-log.tsv` terminal-row check.
    """
    root = tmp_path / "queue"
    queue = JobQueue(root)
    _enqueue(queue, "01-a", curator="elrond")
    _enqueue(queue, "02-b", curator="elrond")

    report = queue.drain(_harness(fake_codex, lock_path))
    assert report.fired == 2
    assert all(o.ok for o in report.outcomes)

    for outcome in report.outcomes:
        assert outcome.exit_code == 0
        assert outcome.usage["cache_read_tokens"] == 600
        assert outcome.usage["reasoning_tokens"] == 20

    assert queue.runlog.is_idle() is True
    assert (root / "usage" / "01-a.jsonl").exists()
    assert (root / "usage" / "01-a.jsonl.stderr").exists(), (
        "stderr must be captured per job — and it must NEVER be adjudicated: all 30 "
        "jobs of the proven run wrote to it while returning rc=0"
    )
    assert (root / "out" / "01-a.md").exists()
    assert (root / "prompts" / "01-a.md").read_text() == "do 01-a"
