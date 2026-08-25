"""D-5 — the cross-session busy check, made mechanical.

The rows this file exists for, in the order the ratification ranks them:

1. **THE LAW: a status call WRITES NOTHING.** No file under a queue root changes, no
   telemetry event is emitted, and no lock file is created by asking. jack-ryan:
   *"Do not let this test be dropped as trivial — it is the only mechanical guard
   against a busy check becoming the authoritative-feeling second truth source."*
2. **AMENDMENT A / the P-9 × leg-3 composition.** One HELD (`ENQUEUED`) job with
   nothing executing answers `queue-pending`, and that answer is SAFE TO FIRE. The
   pre-Amendment build returned "do not fire" here, and composed with P-9 it would
   have wedged the lane's answer for as long as the hold lasted.
3. **AMENDMENT B / blast radius.** An out-of-band `codex exec` does NOT close the
   Grok lane. Attribution fails at *which credential home*, never at *which vendor*.
4. **AMENDMENT H / one named predicate.** `SAFE_TO_FIRE_STATES` is pinned by literal
   and the exit-code table is pinned by literal, because every consumer binds to them
   and a silent edit here is a silent re-ruling of the selection law.
5. **Q62.** An interactive vendor TUI is ADVISORY and NON-BLOCKING.

No live vendor call is made anywhere in this file. The process table is a list of
tuples, the auth probe is a lambda, and the lock is a real `flock` on a tmp path —
because the lock is the one thing a fake cannot stand in for.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

from factory import lane_status as ls
from factory.harness.codex import LaneAvailability
from factory.jobqueue import JobQueue
from factory.lane import SerialLaneLock, default_lock_path

FACTORY_DIR = Path(__file__).resolve().parents[1]

#: A healthy auth answer, injected so no test reaches a vendor CLI.
OK_AUTH = lambda: LaneAvailability(True, "open", "logged in (injected)")  # noqa: E731
EXPIRED_AUTH = lambda: LaneAvailability(  # noqa: E731
    False, "auth_expired", "not logged in (injected)")
MISSING_CLI = lambda: LaneAvailability(  # noqa: E731
    False, "cli_missing", "no binary (injected)")


@pytest.fixture
def lock_path(tmp_path: Path) -> Path:
    return tmp_path / "lane.lock"


def _status(lane="codex", *, procs=(), auth=OK_AUTH, lock=None, logs=(), **kw):
    return ls.lane_status(
        lane, procs=list(procs), auth_probe=auth, lock_path=lock,
        extra_runlogs=list(logs), **kw,
    )


# ===========================================================================
# 1 — THE LAW: the check emits nothing
# ===========================================================================
def _tree_fingerprint(root: Path) -> dict[str, str]:
    """Every file under `root`, by content digest AND mtime.

    Content alone would miss a rewrite-with-identical-bytes; mtime alone would miss
    nothing on a fast machine but is cheap to add. Both, because the claim under test
    is *nothing changed*, not *nothing changed much*.
    """
    out: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            out[str(path.relative_to(root))] = f"{digest}:{path.stat().st_mtime_ns}"
    return out


def test_THE_LAW_a_status_call_changes_NOTHING_under_the_queue_root(tmp_path, lock_path):
    queue = JobQueue(tmp_path / "q", lane="codex")
    queue.enqueue(job_id="held", prompt="p", curator="galadriel")
    before = _tree_fingerprint(queue.root)
    telemetry_before = len(queue.telemetry.events())

    for _ in range(3):
        _status(procs=[], lock=lock_path, logs=[queue.runlog.path])

    assert _tree_fingerprint(queue.root) == before, (
        "a READ-ONLY status call modified the queue root. A probe that writes converts "
        "a question into a side effect and walks the checker into the data path — THE "
        "LAW's failure mode arriving through the instrument built to enforce it."
    )
    assert len(queue.telemetry.events()) == telemetry_before, (
        "the busy check emitted a telemetry event. The check READS state surfaces; the "
        "QUEUE records. A check that emits events others trust is a second truth source."
    )


def test_THE_LAW_asking_does_not_CREATE_the_lock_file(tmp_path):
    """`lane_is_free()` opens with `O_CREAT`, so leg 1 must not be asked blindly."""
    absent = tmp_path / "never-existed.lock"
    status = _status(lock=absent, procs=[])
    assert not absent.exists(), (
        "the status call CREATED a lock file that outlives the question. A lock file "
        "that does not exist cannot be held, and that answer is free."
    )
    assert status.legs["lock"]["probed"] is False
    assert status.state == ls.STATE_OPEN


def test_THE_LAW_the_module_can_reach_NO_WRITE_MECHANISM_at_all():
    """Mechanical over the source, so the claim cannot rot into a paragraph.

    Written the coarse way first — *"no call named `append`"* — and it failed on
    `signals.append`, a local list. That failure is worth keeping in the record
    because the coarse version was ALSO the useless version: it would have gone green
    the moment somebody renamed the write, and it flagged the one construct in the
    file that touches nothing. So the test names the two write MECHANISMS this package
    actually has (`RunLog.append`, `Telemetry.emit`) by refusing their IMPORT, and
    names filesystem mutation by refusing the calls that perform it.
    """
    source = (FACTORY_DIR / "lane_status.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    imported = {
        alias.name for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) for alias in node.names
    }
    assert not (imported & {"RunLog", "Telemetry"}), (
        f"lane_status.py imports {sorted(imported & {'RunLog', 'Telemetry'})} — the two "
        "write mechanisms in this package. The check READS state surfaces; the QUEUE "
        "records. A check that can emit is a check that will."
    )

    mutating = {"write_text", "write_bytes", "mkdir", "touch", "unlink", "emit", "replace"}
    called = {
        node.func.attr for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert not (called & mutating), (
        f"lane_status.py calls {sorted(called & mutating)} — no surviving file touch is "
        "permitted by a status call."
    )

    opened_for_write = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        and node.func.id == "open"
        and any(
            isinstance(arg, ast.Constant) and isinstance(arg.value, str)
            and set(arg.value) & set("wax+")
            for arg in [*node.args[1:], *(kw.value for kw in node.keywords if kw.arg == "mode")]
        )
    ]
    assert opened_for_write == [], "lane_status.py opens a file for writing"


# ===========================================================================
# 2 — the named states
# ===========================================================================
def test_an_IDLE_lane_answers_open(lock_path):
    status = _status(procs=[], lock=lock_path)
    assert status.state == ls.STATE_OPEN
    assert status.safe_to_fire is True
    assert status.exit_code == 0


def test_a_HELD_LOCK_answers_busy_lock(lock_path):
    with SerialLaneLock(lock_path):
        status = _status(procs=[], lock=lock_path)
    assert status.state == ls.STATE_BUSY_LOCK
    assert status.safe_to_fire is False
    assert status.exit_code == ls.EXIT_CODES[ls.STATE_BUSY_LOCK]


def test_an_OUT_OF_BAND_exec_answers_busy_out_of_band_AND_NAMES_THE_PID(lock_path):
    """The motivating incident: a `codex exec` the lock never saw."""
    status = _status(
        procs=[(4242, "/opt/homebrew/bin/codex exec --json -s read-only -")],
        lock=lock_path,
    )
    assert status.state == ls.STATE_BUSY_OUT_OF_BAND
    assert "4242" in status.reason, "the PID must be NAMED — a busy answer nobody can act on is noise"
    assert status.safe_to_fire is False


def test_AUTH_EXPIRED_is_its_own_state_not_a_busy_one(lock_path):
    status = _status(procs=[], auth=EXPIRED_AUTH, lock=lock_path)
    assert status.state == ls.STATE_AUTH_EXPIRED
    assert status.state in ls.CLOSED_STATES, (
        "auth-expired is CLOSED for the selection law — the lane cannot take the work "
        "at all — which is a different disposition from OCCUPIED (enqueue behind it)."
    )


def test_CLI_MISSING_is_its_own_state(lock_path):
    status = _status(procs=[], auth=MISSING_CLI, lock=lock_path)
    assert status.state == ls.STATE_CLI_MISSING
    assert status.state in ls.CLOSED_STATES


def test_an_UNREACHABLE_leg_answers_busy_unknown_NEVER_open(lock_path):
    """G-2 applied to the render: ambiguity outranks `open`, always."""
    status = ls.lane_status(
        "codex", procs=None, procs_error="ps exited 1", auth_probe=OK_AUTH,
        lock_path=lock_path,
    )
    assert status.state == ls.STATE_BUSY_UNKNOWN
    assert status.safe_to_fire is False
    assert "ps exited 1" in status.reason


# ===========================================================================
# 3 — AMENDMENT A and the P-9 × leg-3 composition
# ===========================================================================
def test_AMENDMENT_A_a_HELD_job_answers_queue_pending_and_is_SAFE_TO_FIRE(tmp_path, lock_path):
    """The headline row. One P-9 HELD job, nothing executing -> `queue-pending`, fire-safe.

    This is the composition the pre-Amendment build got wrong: `ENQUEUED` is a member
    of `BUSY_MARKERS`, so `RunLog.is_idle()` reads False on backlog and the old
    `lane-status` returned exit 1 — *"do not fire"* — for a lane on which nothing was
    executing. Compose that with P-9 (*ENQUEUED-but-not-drained IS the held state*, and
    a hold persists as long as its named condition does) and one deliberately held job
    renders the lane permanently unusable to every other job and every other session.
    """
    queue = JobQueue(tmp_path / "q", lane="codex")
    queue.enqueue(job_id="crawl-2012-blizzard", prompt="p", curator="galadriel")
    assert queue.runlog.is_idle() is False, (
        "precondition: the raw leg-3 reading really does say not-idle on backlog — if "
        "this ever flips, this test is no longer exercising the composition it names"
    )

    status = _status(procs=[], lock=lock_path, logs=[queue.runlog.path])

    assert status.state == ls.STATE_QUEUE_PENDING
    assert status.safe_to_fire is True, (
        "a HELD job wedged the lane's answer. Counting backlog as busy re-creates "
        "uptime-is-not-utilization through the instrument built to abolish it."
    )
    assert status.exit_code == 10


def test_a_START_row_with_no_finish_DOES_count_as_occupancy(tmp_path, lock_path):
    """Leg 3's OTHER half, unchanged by Amendment A: `START`-without-finish is busy."""
    queue = JobQueue(tmp_path / "q", lane="codex")
    queue.enqueue(job_id="j", prompt="p", curator="elrond")
    queue.runlog.append(job_id="j", marker="START", detail="attempt=1", curator="elrond",
                        event="start")
    status = _status(procs=[], lock=lock_path, logs=[queue.runlog.path])
    assert status.state == ls.STATE_BUSY_OUT_OF_BAND
    assert status.safe_to_fire is False


def test_an_UNRECOGNISED_marker_reads_NON_terminal(tmp_path, lock_path):
    log = tmp_path / "_run-log.tsv"
    log.write_text("2026-08-24T00:00:00Z\tj\tSOMETHING-NOBODY-NAMED\t-\tcurator=x\tevent=finish\n",
                   encoding="utf-8")
    status = _status(procs=[], lock=lock_path, logs=[log])
    assert status.safe_to_fire is False, "fail-closed: an unnamed state is never `idle`"


def test_an_ABSENT_run_log_is_NOT_an_error(tmp_path, lock_path):
    """G-5: the check is SUBSTRATE and the queue is a consumer. It answers on a bare host."""
    status = _status(procs=[], lock=lock_path, logs=[tmp_path / "nope" / "_run-log.tsv"])
    assert status.state == ls.STATE_OPEN


def test_a_run_log_is_read_ONCE_even_when_named_twice(tmp_path, lock_path):
    queue = JobQueue(tmp_path / "q", lane="codex")
    queue.enqueue(job_id="j", prompt="p", curator="elrond")
    status = _status(procs=[], lock=lock_path,
                     logs=[queue.runlog.path, queue.runlog.path])
    assert status.state == ls.STATE_QUEUE_PENDING
    assert "1 job(s) enqueued" in status.reason, (
        "the same run-log was counted twice; a backlog of one read as a backlog of two"
    )


# ===========================================================================
# 4 — AMENDMENT B: blast radius is PER-VENDOR
# ===========================================================================
def test_AMENDMENT_B_a_codex_exec_does_NOT_close_the_GROK_lane(lock_path):
    """The routing defect this amendment closes, stated as a row.

    On the unamended per-host reading, an unattributable out-of-band `codex exec`
    would close the Grok lane too — driving § 10.3's selection law past step 3
    (spillover) into step 4, the branch that spends Claude. A `codex exec` cannot
    spend the xAI credential; false-busy that buys no safety is outside G-2's bargain.
    """
    procs = [(999, "/opt/homebrew/bin/codex exec --json -")]
    codex = _status("codex", procs=procs, lock=lock_path)
    grok = _status("grok", procs=procs, lock=lock_path)
    assert codex.state == ls.STATE_BUSY_OUT_OF_BAND
    assert grok.state == ls.STATE_OPEN
    assert grok.safe_to_fire is True


def test_AMENDMENT_B_a_grok_exec_does_NOT_close_the_CODEX_lane(lock_path):
    procs = [(1001, "/Users/x/.grok/bin/grok -p hello --output-format json")]
    assert _status("grok", procs=procs, lock=lock_path).state == ls.STATE_BUSY_OUT_OF_BAND
    assert _status("codex", procs=procs, lock=lock_path).state == ls.STATE_OPEN


def test_a_live_leader_socket_reads_busy_on_the_GROK_lane(lock_path):
    """Leader mode is the concurrency door around the serial lock (§ 9.3)."""
    procs = [(555, "/Users/x/.grok/bin/grok agent leader --socket /Users/x/.grok/leader.sock")]
    status = _status("grok", procs=procs, lock=lock_path)
    assert status.state == ls.STATE_BUSY_OUT_OF_BAND
    assert "leader.sock" in status.reason


def test_the_argv_patterns_are_ANCHORED_and_do_not_convict_a_MENTION(lock_path):
    """An unanchored match convicts any shell whose command line mentions the vendor."""
    innocent = [
        (1, "grep -rn codex exec /Users/x/notes"),
        (2, "vim /Users/x/notes/codex-exec-design.md"),
        (3, "python3 -m factory lane --lane grok"),
        (4, "/bin/zsh -c 'echo grok -p'"),
    ]
    assert _status("codex", procs=innocent, lock=lock_path).state == ls.STATE_OPEN
    assert _status("grok", procs=innocent, lock=lock_path).state == ls.STATE_OPEN


# ===========================================================================
# 5 — Q62: the interactive TUI advisory
# ===========================================================================
def test_Q62_an_interactive_TUI_is_ADVISORY_and_NON_BLOCKING(lock_path):
    """Matt-ruled 2026-08-24: *"I'm not worried about TUI."* Advise, never gate."""
    status = _status("grok", procs=[(3131, "/Users/x/.grok/bin/grok")], lock=lock_path)
    assert status.state == ls.STATE_OPEN
    assert status.safe_to_fire is True, "the TUI advisory must NOT gate the lane"
    assert len(status.advisories) == 1
    assert "interactive-grok-present" in status.advisories[0]
    assert "3131" in status.advisories[0]


def test_an_exec_shaped_argv_is_OCCUPANCY_not_an_advisory(lock_path):
    status = _status("grok", procs=[(3131, "/Users/x/.grok/bin/grok -p 'do the thing'")],
                     lock=lock_path)
    assert status.state == ls.STATE_BUSY_OUT_OF_BAND
    assert status.advisories == []


# ===========================================================================
# 6 — AMENDMENT H: the predicate and the exit codes, PINNED BY LITERAL
# ===========================================================================
def test_AMENDMENT_H_the_three_dispositions_PARTITION_the_answer_vocabulary():
    """The STRUCTURAL claim. The membership literals are pinned in `test_vocabularies.py`.

    Deliberately not duplicated: that file's `VOCABULARY_PINS` compares each set by
    EQUALITY and its own doctrine is that a collection resting on two pins has one
    that goes unmaintained. What lives here instead is the claim that file cannot
    make — that the three dispositions PARTITION the seven answer states, so a state
    deleted from one set and not added to another reds a row rather than quietly
    falling out of every routing decision.

    `queue-pending` landing in the SAFE half is Matt's floor operating: with it in the
    closed half, one P-9 HELD job on each vendor lane makes both read closed, § 10.3
    step 4 fires, and Claude takes vendor-scoped work on BACKLOG ALONE.
    """
    everything = ls.SAFE_TO_FIRE_STATES | ls.CLOSED_STATES | ls.OCCUPIED_STATES
    assert everything == set(ls.EXIT_CODES), "a state routes nowhere, or routes from nowhere"
    assert len(everything) == (
        len(ls.SAFE_TO_FIRE_STATES) + len(ls.CLOSED_STATES) + len(ls.OCCUPIED_STATES)
    ), "a state is in two dispositions at once; routing would depend on lookup order"
    assert ls.STATE_QUEUE_PENDING in ls.SAFE_TO_FIRE_STATES


def test_the_EXIT_CODES_are_BANDED_so_a_new_state_cannot_read_fire_safe():
    """A shell caller that checks only the band must never be told "fire" wrongly.

    The band is the contract a `[ $? -lt 20 ]` gets to rely on; the numbers themselves
    are pinned by equality in `test_vocabularies.py`.
    """
    assert ls.EXIT_CODES["open"] == 0, "the one value the lane spec imposes"
    for state in ls.SAFE_TO_FIRE_STATES:
        assert ls.EXIT_CODES[state] < 20
    for state in ls.OCCUPIED_STATES | ls.CLOSED_STATES:
        assert ls.EXIT_CODES[state] >= 20


def test_an_UNKNOWN_state_exits_busy_unknown_not_open():
    assert ls.exit_code_for("a-state-nobody-named") == ls.EXIT_CODES[ls.STATE_BUSY_UNKNOWN]
    assert ls.safe_to_fire("a-state-nobody-named") is False


def test_the_STATE_PRECEDENCE_puts_a_RUNNING_PROCESS_above_a_CREDENTIAL_STATE(lock_path):
    """A running process is a FACT; ambiguity outranks `open`, always."""
    status = _status(
        procs=[(7, "/opt/homebrew/bin/codex exec -")], auth=EXPIRED_AUTH, lock=lock_path)
    assert status.state == ls.STATE_BUSY_OUT_OF_BAND
    assert ls.STATE_PRECEDENCE.index("busy-lock") < ls.STATE_PRECEDENCE.index("auth-expired")
    assert ls.STATE_PRECEDENCE.index("busy-unknown") < ls.STATE_PRECEDENCE.index("open")


# ===========================================================================
# 7 — the selection law (§ 10.3), mechanised
# ===========================================================================
def _fake(lane, state):
    return ls.LaneStatus(lane=lane, vendor=lane, state=state, reason="fixture")


def test_SELECTION_codex_is_FIRST_when_both_lanes_are_open():
    chosen = ls.select_lane([_fake("grok", "open"), _fake("codex", "open")])
    assert chosen.lane == "codex", "deterministic Codex -> Grok, NEVER random"


def test_SELECTION_grok_takes_the_task_when_codex_is_OCCUPIED():
    chosen = ls.select_lane([_fake("codex", "busy-lock"), _fake("grok", "open")])
    assert chosen.lane == "grok", "spillover BY LAW — cross-vendor parallel is legal"


def test_SELECTION_queue_pending_counts_as_OPEN_for_the_selection_law():
    """Amendment H's headline harm, as a row: backlog must not fire the Claude branch."""
    chosen = ls.select_lane([_fake("codex", "queue-pending"), _fake("grok", "queue-pending")])
    assert chosen is not None and chosen.lane == "codex"


def test_SELECTION_returns_NONE_only_when_no_vendor_lane_is_fire_safe():
    assert ls.select_lane([_fake("codex", "auth-expired"), _fake("grok", "cli-missing")]) is None
    assert ls.select_lane([_fake("codex", "busy-lock"), _fake("grok", "busy-out-of-band")]) is None


# ===========================================================================
# 8 — the CLI surface
# ===========================================================================
def test_the_CLI_exits_with_the_PINNED_per_state_code(tmp_path, capsys, monkeypatch):
    from factory.cli import main

    monkeypatch.setenv("REINCARNATED_LANE_LOCK_DIR", str(tmp_path / "locks"))
    monkeypatch.setattr(ls, "scan_process_table", lambda *a, **k: [])
    rc = main(["lane", "--lane", "codex", "--no-auth", "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["lanes"]["codex"]["state"] in ls.EXIT_CODES
    assert rc == payload["lanes"]["codex"]["exit_code"]
    assert payload["safe_to_fire_states"] == sorted(ls.SAFE_TO_FIRE_STATES)


def test_the_CLI_safe_to_fire_flag_collapses_to_one_bit(tmp_path, capsys, monkeypatch):
    from factory.cli import main

    monkeypatch.setenv("REINCARNATED_LANE_LOCK_DIR", str(tmp_path / "locks"))
    monkeypatch.setattr(ls, "scan_process_table", lambda *a, **k: [])
    rc = main(["lane", "--lane", "codex", "--no-auth", "--safe-to-fire"])
    capsys.readouterr()
    assert rc in (0, 1), "the one-bit answer is 0 = fire, 1 = do not; nothing else"


def test_the_lock_paths_of_the_two_VENDORS_are_DIFFERENT_FILES():
    """P-3: per-credential. A shared lock would make the lanes contend illegally."""
    codex = default_lock_path(vendor="codex")
    grok = default_lock_path(vendor="grok")
    assert codex != grok
    assert codex.name.startswith("codex-") and grok.name.startswith("grok-"), (
        "the vendor belongs in the FILENAME so `ls` names the holder without a "
        "sha256 lookup"
    )


def test_default_lock_path_with_NO_ARGUMENTS_is_unchanged():
    """The fleet board calls it that way; a rename would point a view at a dead lock."""
    assert default_lock_path() == default_lock_path(vendor="codex")


def test_an_UNDECLARED_vendor_is_REFUSED_not_defaulted():
    with pytest.raises(ValueError, match="no declared credential home"):
        default_lock_path(vendor="anthropic")
