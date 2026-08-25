"""D-5 (per-lane) — the Grok lane, proven without a live vendor call.

The rows this file exists for:

1. **AMENDMENT E.** `--no-leader` is said on EVERY argv, the preflight ASSERTS the
   flag parses, and a failed assertion REFUSES THE FIRE. The flag is accepted but
   undocumented at the top-level surface, so a version bump could remove it with no
   help-diff to signal it, and the failure would be silent re-entry through the
   concurrency door the lock exists to close.
2. **AMENDMENT C.** The resolved model id (`grok-4.6` -> `grok-4.6-build`) is captured
   per call out of the envelope's `modelUsage` keys. A pin whose resolved target is
   chosen by a vendor-side rule is a REQUEST, not a pin.
3. **AMENDMENT D.** `--reasoning-effort xhigh` is argv-said from the FIRST job.
4. **P-3.** The Grok lock is an INDEPENDENT lane. A busy Codex lane does not close it.
5. **The fence.** `bypassPermissions` / `dontAsk` are refused BY NAME.

The fake `grok` below is a real subprocess emitting the real envelope shape, copied
from the live smoke job of 2026-08-24 rather than invented. It is not a mock of the
adapter: the thing under test is what happens at the `subprocess.run` call site, and a
mock replaces exactly that.
"""

from __future__ import annotations

import base64
import json
import subprocess
from pathlib import Path

import pytest

from factory.harness.grok import (
    AUTH_CONFIRM_READINGS,
    FORBIDDEN_PERMISSION_MODES,
    IMAGE_MIME_BY_SUFFIX,
    LANE_STATE_PREFLIGHT_FAILED,
    LANE_STATE_PREFLIGHT_UNKNOWN,
    MAX_PROMPT_ARGV_BYTES,
    MAX_PROMPT_JSON_ARGV_BYTES,
    MODEL_PIN,
    NO_LEADER_FLAG,
    REASONING_EFFORT_PIN,
    REASONING_EFFORTS,
    GrokHarness,
    LaneAvailability,
    argv_exec_cost,
    host_arg_max,
    parse_envelope,
    resolved_model_ids,
)
from factory.jobqueue import JobQueue
from factory.lane import (
    LANE_STATE_SEAM_HELD,
    SKIPPED_PER_AGENT,
    SeamSlotHeld,
    SeamSlotSemaphore,
    SerialLaneLock,
    SlotOccupancy,
    probe_slots,
    seam_lock_path,
    slot_lock_path,
)
from factory.usage import UsageBreakdown

#: The envelope of the LIVE SMOKE JOB, 2026-08-24, copied field-for-field from
#: `lanes/grok/usage/smoke-grok-lane-2026-08-24.jsonl`. Pinned as a literal because it
#: is the only measured sample of this vendor's shape, and paraphrasing it would make
#: every assertion below a test of my paraphrase.
LIVE_SMOKE_ENVELOPE = {
    "text": "SMOKE-OK grok-lane 2026-08-24.",
    "stopReason": "end_turn",
    "sessionId": "smoke-session",
    "requestId": "smoke-request",
    "num_turns": 1,
    "total_cost_usd": 0.00982838,
    "usage": {
        "input_tokens": 28170,
        "cache_read_input_tokens": 2432,
        "cache_creation_input_tokens": 0,
        "output_tokens": 43,
        "reasoning_tokens": 23,
        "total_tokens": 30645,
    },
    "modelUsage": {"grok-4.6-build": {"costUSD": 0.00982838}},
}

_FAKE_GROK = r'''#!/usr/bin/env python3
"""A fake `grok` speaking the real envelope shape. Not a mock of the adapter."""
import json, os, sys, time

argv = sys.argv[1:]
if argv[:1] == ["models"]:
    print("You are logged in with grok.com.")
    sys.exit(0)
if "--version" in argv:
    if os.environ.get("FAKE_GROK_REJECT_NO_LEADER") and "--no-leader" in argv:
        sys.stderr.write("error: unexpected argument '--no-leader' found\n")
        sys.exit(2)
    print("grok 1.0.5 (fake) [stable]")
    sys.exit(0)

with open(os.environ["FAKE_GROK_ARGV"], "w") as fh:
    json.dump(argv, fh)

time.sleep(float(os.environ.get("FAKE_GROK_SLEEP", "0")))
body = os.environ.get("FAKE_GROK_BODY", "x" * 800)
out = os.environ.get("FAKE_GROK_OUTPUT")
if out:
    with open(out, "w") as fh:
        fh.write(body)

rc = int(os.environ.get("FAKE_GROK_RC", "0"))
print(json.dumps({
    "text": body[:40], "stopReason": "end_turn" if rc == 0 else "error",
    "sessionId": "fake-session", "requestId": "fake-request", "num_turns": 1,
    "total_cost_usd": 0.00982838,
    "usage": {"input_tokens": 28170, "cache_read_input_tokens": 2432,
              "cache_creation_input_tokens": 0, "output_tokens": 43,
              "reasoning_tokens": 23, "total_tokens": 30645},
    "modelUsage": {"grok-4.6-build": {"costUSD": 0.00982838}},
}))
sys.exit(rc)
'''


@pytest.fixture
def fake_grok(tmp_path: Path, monkeypatch) -> Path:
    path = tmp_path / "fake-grok"
    path.write_text(_FAKE_GROK, encoding="utf-8")
    path.chmod(0o755)
    monkeypatch.setenv("FAKE_GROK_ARGV", str(tmp_path / "argv.json"))
    return path


@pytest.fixture
def lock_path(tmp_path: Path) -> Path:
    return tmp_path / "grok.lock"


def _harness(fake_grok: Path, lock_path: Path, **kw) -> GrokHarness:
    return GrokHarness(
        executable=str(fake_grok), lock_path=lock_path,
        auth_probe=kw.pop("auth_probe", lambda: LaneAvailability(True, "open", "logged in")),
        # The auth DEBOUNCE sleeps between confirmation readings. A no-op by default so
        # no existing row pays 3 s of real wall for a code path it is not about; the rows
        # that ARE about it inject a recorder and assert the schedule.
        sleep=kw.pop("sleep", lambda _s: None),
        **kw,
    )


def _vanished_binary_harness(lock_path: Path) -> GrokHarness:
    """A harness whose CLI is NOT THERE, with auth pre-answered `open`.

    Built by hand rather than through `_harness` because the executable is the variable
    under test. Auth is injected open so that `availability()` reaches the PREFLIGHT —
    otherwise `check_auth`'s own `cli_missing` (a different, correctly-terminal state)
    answers first and the row would silently stop testing what it names.
    """
    return GrokHarness(
        executable="/nonexistent/grok-binary", lock_path=lock_path,
        auth_probe=lambda: LaneAvailability(True, "open", "logged in"),
        sleep=lambda _s: None,
    )


def _argv(tmp_path: Path) -> list[str]:
    return json.loads((tmp_path / "argv.json").read_text(encoding="utf-8"))


#: The seam every row below fires under, unless it is testing the seam itself.
SEAM = "star-lord"


def _cfg(**kw) -> dict:
    """A job config that NAMES ITS SEAM — required on this lane since § 9.6 AM-3.

    A helper rather than a default inside the harness, deliberately: `run()` REFUSES a
    config with no seam (Amendment M), and a fixture that quietly supplied one would
    make every row below pass through a door the production caller has to open for
    itself. The rows that test the refusal build their config by hand.
    """
    return {"seam": SEAM, **kw}


# ===========================================================================
# 1 — AMENDMENT E: --no-leader, said AND asserted
# ===========================================================================
def test_AMENDMENT_E_no_leader_is_on_EVERY_argv(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    assert result.ok
    assert NO_LEADER_FLAG in _argv(tmp_path), (
        "leader mode multiplexes clients onto ONE backend through `~/.grok/leader.sock` "
        "— a concurrency door AROUND the serial lock. The flag is not optional."
    )


def test_AMENDMENT_E_the_PREFLIGHT_ASSERTS_the_flag_rather_than_assuming_it(fake_grok, lock_path):
    verdict = _harness(fake_grok, lock_path).assert_no_leader_parses()
    assert verdict.ok is True
    assert NO_LEADER_FLAG in verdict.reason


def test_AMENDMENT_E_a_REJECTED_flag_REFUSES_THE_FIRE(fake_grok, lock_path, tmp_path, monkeypatch):
    """The version-bump scenario: the flag stops parsing and the lane must NOT fire.

    Firing anyway would leave leader mode reachable with nothing to signal it — silent
    re-entry through the exact door the lock exists to close, which is why this
    amendment demanded an assertion instead of an argv entry.
    """
    monkeypatch.setenv("FAKE_GROK_REJECT_NO_LEADER", "1")
    harness = _harness(fake_grok, lock_path)
    verdict = harness.assert_no_leader_parses()
    assert verdict.ok is False
    assert "REFUSES TO FIRE" in verdict.reason

    result = harness.run("hello", tmp_path, _cfg())
    assert result.ok is False
    assert "PREFLIGHT REFUSED" in (result.error or "")
    assert (result.extra or {}).get("lane_state") == LANE_STATE_PREFLIGHT_FAILED
    assert not (tmp_path / "argv.json").exists(), (
        "the refused lane still launched the CLI. A refusal that runs the process "
        "anyway is not a refusal."
    )


def test_AMENDMENT_E_the_assertion_checks_rc_AND_the_rejection_sentence(fake_grok, lock_path):
    """rc alone would pass a CLI that warns-and-continues on an unknown flag.

    That is a plausible future behaviour and it is exactly the silent failure the
    amendment exists to prevent, so the assertion does not rest on rc alone.
    """
    warn_and_continue = _harness(
        fake_grok, lock_path,
        preflight_probe=lambda: (False, "rc=0 but stderr said: unexpected argument"),
    )
    assert warn_and_continue.assert_no_leader_parses().ok is False


def test_AMENDMENT_E_a_FAILED_preflight_closes_availability_BEFORE_the_busy_probe(
        fake_grok, lock_path):
    """A caller must never see `open` on a lane the harness will then refuse to fire.

    The injected probe returns a LEGACY 2-TUPLE on purpose: `_as_preflight_verdict`
    coerces it, and it lands on `refuted=False` — the non-terminal side — because a probe
    written before that field existed never claimed a refutation and does not get
    credited with one.
    """
    harness = _harness(fake_grok, lock_path, preflight_probe=lambda: (False, "flag gone"))
    state = harness.availability()
    assert state.ok is False
    assert state.state == LANE_STATE_PREFLIGHT_UNKNOWN
    assert state.terminal is False


# ===========================================================================
# 1b — PREFLIGHT: **REFUTED** vs **UNANSWERABLE**, told apart
#
# The auth defect wearing different clothes. `assert_no_leader_parses` folded "the CLI
# REJECTED the flag" (a positive, permanent finding) and "the assertion could not be
# MADE" (a timeout, a vanished binary) into one `False`, and that `False` minted
# `terminal=True` — P-7's one-way door. The second harm the auth case did not have: the
# escalation named `grok login`, a remedy that CANNOT work for a flag a CLI update
# removed. Matt runs it, it succeeds, the lane stays shut, and the next escalation is
# read with less trust than this one.
# ===========================================================================
def test_PREFLIGHT_an_UNANSWERABLE_assertion_is_NOT_terminal(fake_grok, lock_path):
    """The binary is gone, so `--no-leader` was NEITHER accepted NOR rejected.

    Driven through the REAL subprocess path with a path that does not exist, rather than
    through an injected probe: the thing under test is what the harness concludes from a
    `FileNotFoundError`, and an injected verdict would be me asserting my own answer.

    Fire-unsafe (the drain stops) but NOT ownership-transferring. Identical footing to
    `auth_unknown`: absence of an answer is not an answer.
    """
    harness = _vanished_binary_harness(lock_path)
    verdict = harness.assert_no_leader_parses()
    assert verdict.ok is False
    assert verdict.refuted is False, (
        "no `grok` was reached, so no `grok` rejected anything. Crediting this with a "
        "refutation is how a sick host empties a queue."
    )

    state = harness.availability()
    assert state.state == LANE_STATE_PREFLIGHT_UNKNOWN
    assert state.terminal is False, (
        "an assertion that could not be MADE just minted the one-way door. Stopping a "
        "drain is reversible; a FALLBACK-CLAUDE row is not."
    )


def test_PREFLIGHT_a_REFUTED_flag_IS_terminal_and_carries_its_OWN_remedy(
        fake_grok, lock_path, monkeypatch):
    """The CLI answered and said no. Positive, permanent — and NOT a credential problem."""
    monkeypatch.setenv("FAKE_GROK_REJECT_NO_LEADER", "1")
    harness = _harness(fake_grok, lock_path)
    verdict = harness.assert_no_leader_parses()
    assert verdict.ok is False
    assert verdict.refuted is True

    state = harness.availability()
    assert state.state == LANE_STATE_PREFLIGHT_FAILED
    assert state.terminal is True
    assert NO_LEADER_FLAG in state.remedy, (
        "a terminal non-credential state that names no remedy of its own inherits the "
        "lane's credential remedy, which is the whole defect this row is about"
    )
    assert "WILL NOT FIX IT" in state.remedy, (
        "the remedy names `grok login` exactly once and only to REFUSE it — the reader "
        "reaches for it first, so the refusal has to arrive before he does"
    )
    assert state.matt_only is False, (
        "amending `NO_LEADER_FLAG` and `build_argv` is the seam owner's work. Queueing "
        "it to the one person who cannot perform it is how an escalation surface earns "
        "the right to be ignored."
    )


def test_PREFLIGHT_the_two_branches_are_DISTINGUISHABLE_on_the_run_log(
        fake_grok, lock_path, tmp_path, monkeypatch):
    """`run()` refuses either way — and records WHICH, or nobody can count them apart."""
    monkeypatch.setenv("FAKE_GROK_REJECT_NO_LEADER", "1")
    refuted = _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    assert (refuted.extra or {}).get("lane_state") == LANE_STATE_PREFLIGHT_FAILED

    monkeypatch.delenv("FAKE_GROK_REJECT_NO_LEADER")
    unknown = _vanished_binary_harness(lock_path).run("hello", tmp_path, _cfg())
    assert (unknown.extra or {}).get("lane_state") == LANE_STATE_PREFLIGHT_UNKNOWN
    assert unknown.ok is False, "unverifiable is still fire-unsafe; only the LABEL differs"


def test_PREFLIGHT_the_ESCALATION_ARTIFACT_does_NOT_tell_Matt_to_re_authenticate(
        fake_grok, lock_path, tmp_path, monkeypatch):
    """The second harm, and the one the auth case did not have.

    `AUTH-BLOCKED.md` used to say *"grok lane re-authentication — `~/.grok/bin/grok
    login` on the Mac"* for EVERY terminal state, including a `--no-leader` flag a CLI
    update removed. That remedy SUCCEEDS and changes nothing. The cost is not the wasted
    minute: it is that the escalation surface has now spent its credibility, and the next
    row Matt reads on it is one he has been trained to discount.
    """
    monkeypatch.setenv("FAKE_GROK_REJECT_NO_LEADER", "1")
    root = tmp_path / "queue"
    queue = JobQueue(root, lane="grok")
    queue.enqueue(job_id="01-a", prompt="x", curator="elrond", seam=SEAM, sandbox="n/a")
    report = queue.drain(_harness(fake_grok, lock_path))

    assert report.lane_state == LANE_STATE_PREFLIGHT_FAILED
    note = (root / "AUTH-BLOCKED.md").read_text(encoding="utf-8")
    assert "re-authentication" not in note.lower()
    assert "NOT MATT-ONLY" in note
    assert NO_LEADER_FLAG in note and "star-lord" in note, (
        "the note must name the real remedy and its real owner, or it is an escalation "
        "that tells its reader nothing they can act on"
    )
    blocked = [e for e in queue.telemetry.events() if e["event"] == "lane_blocked"]
    assert blocked[0]["passthrough"]["matt_only_action"] is False


# ===========================================================================
# 2 — AMENDMENT C: the RESOLVED model id
# ===========================================================================
def test_AMENDMENT_C_the_RESOLVED_model_id_is_captured_per_call(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    assert result.extra["resolved_model"] == "grok-4.6-build"
    assert result.extra["resolved_model_ids"] == ["grok-4.6-build"]
    assert result.model == MODEL_PIN, "the DECLARED pin is recorded too — both, not either"


def test_AMENDMENT_C_the_declared_pin_and_the_resolved_id_are_DIFFERENT_FIELDS():
    """The whole force of the amendment: `grok-4.6` is a REQUEST, `grok-4.6-build` is what ran."""
    assert resolved_model_ids(LIVE_SMOKE_ENVELOPE) == ["grok-4.6-build"]
    assert MODEL_PIN == "grok-4.6"
    assert resolved_model_ids(LIVE_SMOKE_ENVELOPE) != [MODEL_PIN], (
        "if these ever match, the vendor changed its resolution rule — which is a LANE "
        "EVENT THAT MUST BE VISIBLE, not a reason to delete this row"
    )


def test_a_MULTI_MODEL_turn_records_ALL_the_ids_not_just_the_first():
    envelope = {"modelUsage": {"grok-4.6-build": {}, "grok-4.5-fast": {}}}
    assert resolved_model_ids(envelope) == ["grok-4.5-fast", "grok-4.6-build"]


def test_a_MISSING_modelUsage_records_ABSENCE_rather_than_a_guess(fake_grok, lock_path, tmp_path):
    harness = _harness(fake_grok, lock_path)
    result = harness.adjudicate(json.dumps({"text": "hi", "stopReason": "end_turn"}),
                                returncode=0)
    assert result.extra["resolved_model_ids"] == []
    assert result.extra["model_resolution_captured"] is False


# ===========================================================================
# 3 — AMENDMENT D + the pin discipline
# ===========================================================================
def test_AMENDMENT_D_the_effort_is_ARGV_SAID_from_the_first_job(fake_grok, lock_path, tmp_path):
    _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    argv = _argv(tmp_path)
    assert "--reasoning-effort" in argv
    assert argv[argv.index("--reasoning-effort") + 1] == REASONING_EFFORT_PIN == "xhigh"
    assert "-m" in argv and argv[argv.index("-m") + 1] == MODEL_PIN


def test_the_pin_is_said_on_the_ARGV_never_left_to_ambient_config(fake_grok, lock_path, tmp_path):
    """H1 on the third vendor. `~/.grok/config.toml` is host state no file here controls."""
    _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    # The fake records `sys.argv[1:]`, so argv[0] (the binary) is not in this list.
    argv = _argv(tmp_path)
    assert argv[:2] == ["-p", "hello"], "single-turn headless, prompt on argv"
    assert "--output-format" in argv and argv[argv.index("--output-format") + 1] == "json"


def test_an_UNANNOUNCED_pin_swap_is_REFUSED(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg(model="grok-4.5"))
    assert result.ok is False
    assert "model_ab_note" in (result.error or "")
    assert "DECLARED, not banked" in (result.error or ""), (
        "the refusal must state the honest reason: an unbanked pin makes an "
        "unannounced swap WORSE, because it corrupts the baseline while it is being "
        "measured"
    )


def test_an_ANNOUNCED_swap_with_an_AB_NOTE_is_permitted(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run(
        "hello", tmp_path, _cfg(model="grok-4.5", model_ab_note="notes/2026-08-24-ab.md"))
    assert result.ok is True
    argv = _argv(tmp_path)
    assert argv[argv.index("-m") + 1] == "grok-4.5"


def test_the_EFFORT_PIN_is_a_MEMBER_of_the_CLIs_own_vocabulary():
    """The vocabulary itself is pinned by equality in `test_vocabularies.py`.

    What this row adds is the composition: the value we PIN must be one the CLI
    accepts. A pin outside its own vocabulary would be refused at `build_argv` on
    every job, and the lane would be closed by its own constant.
    """
    assert REASONING_EFFORT_PIN in REASONING_EFFORTS
    assert REASONING_EFFORT_PIN == "xhigh", (
        "Posture-2 logic: a shallow second opinion launders confidence. Lowering this "
        "is an A/B decision with an evidence note, not an edit."
    )


def test_an_EFFORT_OUTSIDE_the_vocabulary_is_refused_HERE_not_at_the_vendor(
        fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run(
        "hello", tmp_path, _cfg(reasoning_effort="maximum"))
    assert result.ok is False
    assert "xhigh" in (result.error or "")
    assert not (tmp_path / "argv.json").exists()


# ===========================================================================
# 4 — the fence
# ===========================================================================
@pytest.mark.parametrize("mode", sorted(FORBIDDEN_PERMISSION_MODES))
def test_the_FENCE_DISSOLVING_permission_modes_are_refused_BY_NAME(
        mode, fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg(permission_mode=mode))
    assert result.ok is False
    assert "REFUSED BY NAME" in (result.error or "")
    assert not (tmp_path / "argv.json").exists()


def test_WEB_SEARCH_IS_OFF_unless_the_job_class_NAMES_it(fake_grok, lock_path, tmp_path):
    _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    assert "--disable-web-search" in _argv(tmp_path)


def test_WEB_SEARCH_ON_is_a_DECLARATION_not_a_default(fake_grok, lock_path, tmp_path):
    _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg(web_search=True))
    assert "--disable-web-search" not in _argv(tmp_path)


def test_a_TOOLS_declaration_is_REFUSED_with_the_reason_stated(fake_grok, lock_path):
    with pytest.raises(ValueError, match="not been enumerated on this host"):
        GrokHarness.validate_tools(["Read"], "phase-x")


def test_an_OVERSIZE_prompt_is_refused_HERE_not_as_an_E2BIG(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("x" * (300 * 1024), tmp_path, _cfg())
    assert result.ok is False
    assert "ARG_MAX" in (result.error or "")
    assert "--prompt-file" in (result.error or ""), "name the door past the ceiling"


# ===========================================================================
# 5 — P-3: an INDEPENDENT lane
# ===========================================================================
def test_the_GROK_lane_is_INDEPENDENT_of_a_BUSY_CODEX_lane(fake_grok, lock_path, tmp_path):
    """Cross-vendor parallel is LEGAL and intended: two credentials, two lanes."""
    from factory.lane import default_lock_path

    codex_lock = SerialLaneLock(tmp_path / "codex.lock").acquire()
    try:
        result = _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
        assert result.ok is True, "a busy Codex lane closed the Grok lane — it must not"
    finally:
        codex_lock.release()
    assert default_lock_path(vendor="grok") != default_lock_path(vendor="codex")


def test_a_SECOND_grok_job_FOR_THE_SAME_SEAM_is_REFUSED(fake_grok, lock_path, tmp_path):
    """**AM-3 replaced this row's subject and NOT its shape.** It used to hold the single
    lane lock and assert `lane_state == "busy"`. Under § 9.6 AM-3 the lane is not serial:
    what is refused is a second job for the SAME SEAM, and the refusal is `per-agent`,
    not `busy` — because the lane may have two free slots and other seams may be firing
    into them at that instant. The old assertion would now be measuring the ceiling."""
    held = SeamSlotSemaphore(lock_path, SEAM).acquire()
    try:
        result = _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    finally:
        held.release()
    assert result.ok is False
    assert (result.extra or {}).get("lane_state") == LANE_STATE_SEAM_HELD, (
        "a per-agent refusal reported as a BUSY LANE. That stops a whole drain at 1/3 "
        "with two slots idle (Amendment R.2's head-of-line blocking) — the lane is not "
        "busy, this one agent is."
    )
    assert not (tmp_path / "argv.json").exists()


def test_BOTH_lock_fds_are_INHERITED_by_the_child(fake_grok, lock_path, tmp_path, monkeypatch):
    """`pass_fds` is what makes lock lifetime = max(queue, grok) — now for BOTH locks.

    **AMENDMENT N.2.** One fd inherited and the other not would be the worst of the two
    worlds available: a killed queue would release the per-seam hold while the child
    kept running (the agent could double-fire itself), or hold the seam after the child
    died (the agent locked out of its own lane). Both are probed from a THIRD process,
    because a probe inside this one cannot distinguish "the child holds it" from "I hold
    it" — `flock` conflicts across two open file descriptions in one process either way.
    """
    monkeypatch.setenv("FAKE_GROK_SLEEP", "0.5")
    import subprocess as sp
    import threading

    seam_path = seam_lock_path(lock_path, SEAM)
    slot_path = slot_lock_path(lock_path, 0)
    seen: dict[str, str] = {}

    def watch():
        import time

        time.sleep(0.2)
        probe = sp.run(
            [__import__("sys").executable, "-c",
             "import fcntl,os,sys\n"
             "for name, p in ((\"seam\", %r), (\"slot\", %r)):\n"
             "    fd=os.open(p, os.O_CREAT|os.O_RDWR)\n"
             "    try:\n"
             "        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB); print(name+'=FREE')\n"
             "    except OSError: print(name+'=HELD')\n"
             % (str(seam_path), str(slot_path))],
            capture_output=True, text=True,
        )
        seen["out"] = probe.stdout

    thread = threading.Thread(target=watch)
    thread.start()
    _harness(fake_grok, lock_path).run("hello", tmp_path, _cfg())
    thread.join()
    assert "seam=HELD" in seen.get("out", ""), (
        "the PER-SEAM lock did not travel to the child. A killed queue would then leave "
        "a live job with its seam unheld — and the agent could fire a second one."
    )
    assert "slot=HELD" in seen.get("out", ""), (
        "the SLOT lock did not travel to the child — a killed queue would leave a "
        "running job on an uncounted slot, which is the ceiling silently becoming N+1."
    )


# ===========================================================================
# 6 — auth + adjudication + usage
# ===========================================================================
def test_AUTH_uses_grok_models_as_the_check_of_record(fake_grok, lock_path):
    harness = GrokHarness(executable=str(fake_grok), lock_path=lock_path)
    state = harness.check_auth()
    assert state.ok is True
    assert "logged in" in state.reason.lower()


def test_EXPIRED_AUTH_carries_the_MATT_ONLY_discipline_verbatim(fake_grok, lock_path):
    harness = GrokHarness(
        executable=str(fake_grok), lock_path=lock_path,
        auth_probe=lambda: GrokHarness(executable="/nonexistent/grok").check_auth(),
    )
    state = harness.check_auth()
    assert state.ok is False
    assert state.state == "cli_missing"


def test_a_MISSING_BINARY_is_a_STATE_not_a_constructor_explosion(monkeypatch, tmp_path):
    monkeypatch.setenv("REINCARNATED_GROK_BIN", str(tmp_path / "nope"))
    harness = GrokHarness()
    assert harness.executable is None
    assert harness.check_auth().state == "cli_missing"


def test_NO_PARSEABLE_ENVELOPE_is_the_failure_signal(fake_grok, lock_path):
    result = _harness(fake_grok, lock_path).adjudicate("total garbage", returncode=1)
    assert result.ok is False
    assert "no parseable JSON envelope" in (result.error or "")
    assert result.usage.billable_token_total() is None


def test_the_envelope_parser_survives_noise_around_the_object():
    assert parse_envelope('warn: something\n{"text":"hi"}\n')["text"] == "hi"
    assert parse_envelope("") is None
    assert parse_envelope("{not json") is None


def test_the_USAGE_MAPPING_reproduces_the_VENDORS_OWN_TOTAL_EXACTLY():
    """The containment question, settled by arithmetic rather than by inference.

    Sibling reading: 28170 + 2432 + 0 + 43 = 30645 = the envelope's `total_tokens`.
    Subset reading would have given 28213, which matches nothing the vendor reported.
    """
    usage = UsageBreakdown.from_grok_envelope(LIVE_SMOKE_ENVELOPE)
    assert usage.billable_token_total() == LIVE_SMOKE_ENVELOPE["usage"]["total_tokens"]
    assert usage.cache_read_tokens == 2432
    assert usage.input_tokens == 28170, "NOT reduced by the cache read — siblings, not subset"


def test_G2_2_the_PER_JOB_INPUT_FLOOR_is_bound_to_its_MEASUREMENT_OF_RECORD():
    """The named quantity and the envelope it was measured from cannot drift apart.

    G2-2's finding was that the arithmetic survived and the *operational fact* did not:
    28,170 input tokens on a ONE-LINE prompt is a fixed context the CLI injects on every
    call, and Amendment I's banking window must attribute it as overhead rather than as
    per-job model spend. A number written only into prose is a number the next reader
    re-derives or re-types; this row makes the constant answerable to the artifact.

    `LIVE_SMOKE_ENVELOPE` is the real envelope from `smoke-grok-lane-2026-08-24`, so if
    a future re-probe replaces it with a new measurement, the constant must move in the
    same commit — which is what "a CLI version bump requires a re-probe" means when it
    is a mechanism rather than a sentence.
    """
    from factory.harness.grok import GROK_CLI_INPUT_FLOOR_TOKENS

    usage = UsageBreakdown.from_grok_envelope(LIVE_SMOKE_ENVELOPE)
    assert GROK_CLI_INPUT_FLOOR_TOKENS == usage.input_tokens, (
        f"the declared per-job input floor ({GROK_CLI_INPUT_FLOOR_TOKENS:,}) no longer "
        f"matches its measurement of record ({usage.input_tokens:,}). One of the two "
        "moved alone — and the banking window reads the constant."
    )
    # The reading that makes the floor MATTER, asserted rather than left to the prose:
    # this call's cost was overwhelmingly fixed overhead, not model spend.
    marginal = usage.billable_token_total() - GROK_CLI_INPUT_FLOOR_TOKENS - usage.cache_read_tokens
    assert marginal == 43, (
        "the marginal (non-floor, non-cache) token count for the smoke job is not the "
        f"43 output tokens the vendor reported: got {marginal}. That subtraction IS the "
        "per-job figure the Amendment-I window compares against Codex."
    )
    assert marginal / usage.billable_token_total() < 0.01, (
        "the smoke job's marginal share is no longer under 1% — the sentence '$0.00983 "
        "for 43 output tokens is ~99.9% fixed overhead' would now be false in MIGRATION "
        "§ 10.1 while still being written there."
    )


def test_REASONING_TOKENS_are_a_SHARE_OF_OUTPUT_never_a_fifth_addend():
    usage = UsageBreakdown.from_grok_envelope(LIVE_SMOKE_ENVELOPE)
    assert usage.reasoning_tokens == 23
    assert usage.billable_token_total() == 30645, "reasoning must not be summed in"


def test_the_PER_CALL_COST_is_recorded_AND_labelled_as_IMPUTED():
    usage = UsageBreakdown.from_grok_envelope(LIVE_SMOKE_ENVELOPE)
    assert usage.dollars == pytest.approx(0.00982838)
    assert usage.dollars_source == "harness_reported_imputed", (
        "the credential is a grok.com SUBSCRIPTION; recording this as money billed "
        "would let a downstream report claim a spend that did not happen"
    )


def test_the_cost_falls_back_to_summing_modelUsage_when_the_top_level_is_absent():
    envelope = {"usage": {"input_tokens": 1}, "modelUsage": {
        "a": {"costUSD": 0.001}, "b": {"costUSD": 0.002}}}
    assert UsageBreakdown.from_grok_envelope(envelope).dollars == pytest.approx(0.003)


# ===========================================================================
# 7 — D-8: the per-lane run-log, born with the curator column
# ===========================================================================
def test_D8_the_GROK_run_log_is_born_with_the_CURATOR_COLUMN_and_ENQUEUE_ROWS(
        tmp_path, fake_grok, lock_path, monkeypatch):
    """This lane never has a rows-at-close era, because it never has a hand-fire era."""
    queue = JobQueue(tmp_path / "q", lane="grok")
    queue.enqueue(job_id="j1", prompt="p", curator="galadriel", seam=SEAM, sandbox="n/a")

    rows = list(queue.runlog.rows())
    assert len(rows) == 1
    assert len(rows[0]) == 6, "six columns from the FIRST row this lane ever wrote"
    assert rows[0][2] == "ENQUEUED"
    assert rows[0][4] == "curator=galadriel"
    assert rows[0][5] == "event=enqueue"
    assert queue.curator_at_enqueue("j1") == "galadriel"


def test_R_B_is_VENDOR_GENERIC_no_curator_no_fire_on_the_GROK_lane(tmp_path):
    queue = JobQueue(tmp_path / "q", lane="grok")
    with pytest.raises(ValueError, match="REFUSAL TO FIRE"):
        queue.enqueue(job_id="j", prompt="p", curator="", sandbox="n/a")
    assert not (tmp_path / "q" / "_run-log.tsv").exists(), (
        "the refusal must leave NO trace — it fires before any file or row exists"
    )


def test_a_GROK_job_declaring_a_CODEX_SANDBOX_is_REFUSED(tmp_path):
    """A fence this lane cannot hold must not be accepted and ignored."""
    queue = JobQueue(tmp_path / "q", lane="grok")
    with pytest.raises(ValueError, match="holds no sandbox fence"):
        queue.enqueue(job_id="j", prompt="p", curator="galadriel", seam=SEAM, sandbox="read-only")


def test_the_GROK_FENCE_lands_in_the_ENQUEUE_ROW_where_it_can_be_read(tmp_path):
    queue = JobQueue(tmp_path / "q", lane="grok")
    queue.enqueue(job_id="j", prompt="p", curator="galadriel", seam=SEAM, sandbox="n/a",
                  extra={"permission_mode": "plan"})
    assert "permission_mode=plan" in list(queue.runlog.rows())[0][3]


def test_D3_the_ROUTER_TOKEN_rides_the_detail_column_and_is_GREPPABLE(tmp_path):
    """`grep -c "router=Q3-NO"` — lane contention, countable for the first time."""
    from factory.jobqueue import ROUTER_Q3_NO

    queue = JobQueue(tmp_path / "q", lane="codex")
    queue.enqueue(job_id="j", prompt="p", curator="elrond", router=ROUTER_Q3_NO)
    text = (tmp_path / "q" / "_run-log.tsv").read_text(encoding="utf-8")
    assert "router=Q3-NO" in text
    assert text.count("\t") == 5, "no schema change: still six columns"


def test_a_job_with_NO_router_verdict_does_NOT_get_a_fabricated_one(tmp_path):
    queue = JobQueue(tmp_path / "q", lane="codex")
    queue.enqueue(job_id="j", prompt="p", curator="elrond")
    assert "router=" not in (tmp_path / "q" / "_run-log.tsv").read_text(encoding="utf-8")


def test_the_AUTH_BLOCKED_note_names_WHICH_LANE(tmp_path, fake_grok, lock_path):
    queue = JobQueue(tmp_path / "q", lane="grok")
    queue.enqueue(job_id="j", prompt="p", curator="galadriel", seam=SEAM, sandbox="n/a")
    harness = _harness(
        fake_grok, lock_path,
        auth_probe=lambda: LaneAvailability(False, "auth_expired", "expired (injected)"))
    report = queue.drain(harness)
    assert report.lane_state == "auth_expired"
    note = (tmp_path / "q" / "AUTH-BLOCKED.md").read_text(encoding="utf-8")
    assert "grok lane BLOCKED" in note
    assert "grok/bin/grok login" in note
    assert "knight-rider files it" in note


# ===========================================================================
# 8 — the round trip, end to end, with no live call
# ===========================================================================
def test_ROUND_TRIP_enqueue_drain_and_the_row_carries_C_and_I(tmp_path, fake_grok, lock_path):
    """Amendment I's window needs curator + resolved id + effort + cost ON EVERY ROW."""
    queue = JobQueue(tmp_path / "q", lane="grok")
    queue.enqueue(job_id="j1", prompt="do it", curator="galadriel", seam=SEAM, sandbox="n/a")
    report = queue.drain(_harness(fake_grok, lock_path))

    assert report.fired == 1
    finish = [r for r in queue.runlog.rows() if r[2].startswith("rc=")][0]
    assert "resolved_model=grok-4.6-build" in finish[3], "Amendment C, on the row"
    assert "cost_usd=" in finish[3], "Amendment I, on the row"
    # GATE-2 G2-1. This assertion did not exist while the docstring above already
    # claimed the row carried all four: the effort check below reads the TELEMETRY, and
    # the ROW was never asked. The claim and the check were about different surfaces —
    # inside the one test written to hold the row to the claim.
    assert "effort=xhigh" in finish[3], "Amendment D, ON THE ROW (G2-1)"
    assert finish[4] == "curator=galadriel", "R-B, on the row"

    events = [e for e in queue.telemetry.events() if e["event"] == "finish"]
    assert events[0]["reasoning_effort"] == "xhigh", "Amendment D, in the telemetry"
    assert events[0]["usage"]["dollars"] == pytest.approx(0.00982838)


def test_G2_1_a_harness_that_reports_NO_EFFORT_gets_no_FABRICATED_one(
    tmp_path, fake_grok, lock_path
):
    """Absent is absent — the same discipline `cost_usd=` and `router=` already hold.

    The fix for G2-1 reads the effort out of the harness's `extra`, and the tempting
    shorter spelling was to fall back to the module's `REASONING_EFFORT_PIN` when it is
    missing. That would write a value nobody measured onto the surface Amendment I's
    banking window reads — a row asserting an effort level the invocation may never
    have carried, which is the finding G2-1 IS, rebuilt on the other side.

    So a harness whose result declares no effort writes no `effort=` token, and the
    window sees a gap it can ask about rather than a default it cannot detect.
    """
    queue = JobQueue(tmp_path / "q", lane="grok")
    queue.enqueue(job_id="j1", prompt="do it", curator="galadriel", seam=SEAM, sandbox="n/a")

    inner = _harness(fake_grok, lock_path)

    class _SaysNothingAboutEffort:
        def availability(self):
            return inner.availability()

        def run(self, prompt, cwd, config):
            result = inner.run(prompt, cwd, config)
            result.extra.pop("reasoning_effort", None)
            return result

    assert queue.drain(_SaysNothingAboutEffort()).fired == 1
    finish = [r for r in queue.runlog.rows() if r[2].startswith("rc=")][0]
    assert "effort=" not in finish[3], (
        f"a defaulted effort landed on the run-log row: {finish[3]!r}. A banking-window "
        "row that states an effort level nobody measured is worse than one that states "
        "none, because the gap is detectable and the default is not."
    )
    assert "resolved_model=" in finish[3], "the rest of the row is untouched"


# ===========================================================================
# 9 — TRANSIENT vs TERMINAL AUTH: the one-way door is spent only on a finding
# ===========================================================================
"""Occasioned by a MEASURED false positive, 2026-08-25.

jack-ryan ran `factory lane-status --lane grok lanes/grok` at ~17:27 and got
`auth_expired`. Six probes seconds later all returned rc=0 and *"You are logged in with
grok.com."* **The token had auto-refreshed.** So the first real-world occurrence of
`check_auth`'s REASONED-NOT-MEASURED negative branch was not a `grok logout` — it was a
routine refresh, and it produced the identical classification.

Downstream of that reading, on the code as it stood: `jobqueue.drain` ->
`if not state.ok and state.state != "busy"` -> `_stop_on_closed_lane` -> `for job in
pending: self._hand_to_claude(...)`, **every** pending job, with a `FALLBACK-CLAUDE` row
the queue's own comment makes deliberately terminal (a drain after re-auth must NOT pick
it back up), plus an `AUTH-BLOCKED.md` escalating a Matt-only re-authentication that was
never needed. `auth_unknown` — the 60 s CLI timeout — took the identical path.

The defect was INERT only because `pending: 0`. These rows exist because the window in
which it is free to fix closes on the first dispatch that enqueues real work.

Every row below is written to go RED against the pre-fix code, and each names which
assertion does it.
"""


class _SequencedAuth:
    """A probe that answers a SCRIPTED SEQUENCE — the instrument the old code made impossible.

    The pre-fix `check_auth` read the lane ONCE, so no injected probe could express "the
    CLI said one thing and then said another": a sequence and a constant were the same
    input. 69 rows passed against that method and none of them exercised a lane whose
    answer CHANGED, which is precisely the lane jack-ryan measured.
    """

    def __init__(self, *readings: LaneAvailability):
        self._readings = list(readings)
        self.calls = 0

    def __call__(self) -> LaneAvailability:
        self.calls += 1
        # The last reading repeats, so a script is a PREFIX and never a length puzzle.
        return self._readings[min(self.calls - 1, len(self._readings) - 1)]


_EXPIRED = LaneAvailability(False, "auth_expired", "exited 1: not logged in (injected)")
_OPEN = LaneAvailability(True, "open", "You are logged in with grok.com.")
_UNKNOWN = LaneAvailability(
    False, "auth_unknown", "`grok models` did not answer within 60s (injected)")


def _grok_queue(tmp_path: Path, n: int = 3) -> JobQueue:
    queue = JobQueue(tmp_path / "q", lane="grok")
    for i in range(n):
        queue.enqueue(job_id=f"j{i}", prompt="p", curator="galadriel",
                      seam=SEAM, sandbox="n/a")
    return queue


def _handed_off(queue: JobQueue) -> list[str]:
    return sorted(p.name for p in (queue.root / "fallback").glob("*.json"))


# -- the harness half: a reading is not a verdict ---------------------------
def test_a_TRANSIENT_auth_reading_is_ABSORBED_and_does_NOT_close_the_lane(
    fake_grok, lock_path
):
    """THE MEASURED CASE, replayed: one not-authenticated reading, then logged-in.

    RED against the old code at `state.ok is False` — the old `check_auth` returned the
    FIRST reading verbatim, so a lane that had already refreshed read as expired.
    """
    probe = _SequencedAuth(_EXPIRED, _OPEN)
    harness = _harness(fake_grok, lock_path, auth_probe=probe)

    state = harness.check_auth()

    assert state.ok is True, (
        "one transient not-authenticated reading closed the lane. This is jack-ryan's "
        "17:27 measurement: the token was auto-refreshing and the CLI answered logged-in "
        "seconds later."
    )
    assert probe.calls == 2, "the negative branch must RE-PROBE, not conclude"
    assert "TRANSIENT" in state.reason, (
        "the absorbed blip must be SAID. A debounce nobody can see is indistinguishable "
        "from a bug, and an operator needs to know the lane wobbled."
    )


def test_a_CONFIRMED_expiry_takes_THREE_CONSECUTIVE_readings_and_only_then_is_TERMINAL(
    fake_grok, lock_path
):
    """The real-logout path still works, and terminal is minted at exactly ONE site."""
    probe = _SequencedAuth(_EXPIRED)
    harness = _harness(fake_grok, lock_path, auth_probe=probe)

    state = harness.check_auth()

    assert state.ok is False and state.state == "auth_expired"
    assert probe.calls == AUTH_CONFIRM_READINGS == 3
    assert state.terminal is True
    assert "MATT-ONLY" in state.reason, "the Matt-only discipline survives the debounce"
    assert "CONFIRMED by 3 consecutive readings" in state.reason


def test_the_readings_must_be_CONSECUTIVE_a_recovery_at_ANY_point_absorbs(
    fake_grok, lock_path
):
    """expired, expired, logged-in -> OPEN. Two out of three is not a confirmation."""
    probe = _SequencedAuth(_EXPIRED, _EXPIRED, _OPEN)
    harness = _harness(fake_grok, lock_path, auth_probe=probe)

    state = harness.check_auth()

    assert state.ok is True, "a recovery on the LAST reading still absorbs"
    assert probe.calls == 3


def test_AUTH_UNKNOWN_is_NEVER_terminal_and_is_NEVER_re_probed(fake_grok, lock_path):
    """CLAUSE 2. Absence of an answer is FIRE-UNSAFE, never OWNERSHIP-TRANSFERRING.

    RED against the old code at `state.terminal is False` (the attribute did not exist,
    and the queue handed the whole backlog over on this state).

    The `calls == 1` assertion is the other half and is deliberate: no COUNT of timeouts
    is a positive finding, so re-probing one would push a `lane-status` worst case from
    60 s to 180 s to reach a verdict it already had.
    """
    probe = _SequencedAuth(_UNKNOWN)
    harness = _harness(fake_grok, lock_path, auth_probe=probe)

    state = harness.check_auth()

    assert state.ok is False and state.state == "auth_unknown"
    assert state.terminal is False
    assert probe.calls == 1


def test_a_confirmation_that_CANNOT_COMPLETE_does_not_inherit_reading_ONEs_verdict(
    fake_grok, lock_path
):
    """expired, then the CLI stops answering. That is unresolved, NOT a confirmed expiry."""
    probe = _SequencedAuth(_EXPIRED, _UNKNOWN)
    harness = _harness(fake_grok, lock_path, auth_probe=probe)

    state = harness.check_auth()

    assert state.state == "auth_unknown"
    assert state.terminal is False, (
        "one affirmative reading plus a timeout is ONE affirmative reading. Promoting it "
        "would make the debounce bypassable by a slow CLI."
    )


def test_the_RE_PROBE_SCHEDULE_is_exponential_and_bounded(fake_grok, lock_path):
    """The delay is a MEASURED-COST decision, so the schedule is asserted, not assumed."""
    slept: list[float] = []
    harness = _harness(
        fake_grok, lock_path, auth_probe=_SequencedAuth(_EXPIRED), sleep=slept.append)

    harness.check_auth()

    assert slept == [1.0, 2.0], (
        f"re-probe schedule drifted to {slept}. Probe latency is measured on this host "
        "(n=6, 0.74-0.96s); the REFRESH WINDOW is not measurable from here, so the "
        "schedule is chosen on cost asymmetry and pinned rather than tuned by feel."
    )
    assert sum(slept) < 10, "a debounce is not a retry storm"


def test_probe_auth_once_REMAINS_the_undebounced_instrument(fake_grok, lock_path):
    """The raw reading is still reachable — BY NAME, and not by accident."""
    probe = _SequencedAuth(_EXPIRED, _OPEN)
    harness = _harness(fake_grok, lock_path, auth_probe=probe)

    reading = harness.probe_auth_once()

    assert reading.ok is False and probe.calls == 1
    assert reading.terminal is False, "a raw reading may never be a terminal verdict"


def test_a_LIVE_probe_of_the_REAL_lane_confirms_the_positive_branch_is_UNCHANGED():
    """n=6 on this host said rc=0 and 'You are logged in with grok.com.' — one call each.

    Skipped where the binary is absent, so the row is a fact when it can be and never a
    fabrication. The point it holds: the debounce costs the HEALTHY path nothing.
    """
    harness = GrokHarness()
    if harness.executable is None:
        pytest.skip("the grok CLI is not installed on this host")
    state = harness.check_auth()
    if not state.ok:
        pytest.skip(f"the live lane is not open right now: {state.state}")
    assert "logged in" in state.reason.lower()
    assert "TRANSIENT" not in state.reason, "the healthy path must not re-probe at all"


# -- the queue half: D-12's new row -----------------------------------------
def test_D12_a_TRANSIENT_reading_hands_ZERO_JOBS_TO_CLAUDE(tmp_path, fake_grok, lock_path):
    """**THE ROW.** Drain a real queue across the exact reading jack-ryan measured.

    RED against the old code at `_handed_off(queue) == []` — the old drain saw
    `not state.ok`, called `_stop_on_closed_lane`, and wrote a `fallback/` manifest plus a
    terminal `FALLBACK-CLAUDE` row for EVERY pending job, permanently, on one reading.
    """
    queue = _grok_queue(tmp_path)
    harness = _harness(fake_grok, lock_path, auth_probe=_SequencedAuth(_EXPIRED, _OPEN))

    report = queue.drain(harness)

    assert _handed_off(queue) == [], (
        "a transient auth reading moved ownership of pending work to Claude. P-7 makes "
        "that a ONE-WAY DOOR: a drain after recovery must not pick these jobs back up."
    )
    assert not (queue.root / "AUTH-BLOCKED.md").exists(), (
        "a transient reading escalated a MATT-ONLY re-authentication that was not needed"
    )
    assert report.lane_state == "open" and report.fired == 3, (
        "the lane had already refreshed; the work should simply have run"
    )


def test_D12_an_UNCONFIRMED_lane_STOPS_the_drain_and_hands_off_NOTHING(
    tmp_path, fake_grok, lock_path
):
    """CLAUSE 3, both halves at once: the drain stops AND ownership does not move.

    These two outcomes shared one trigger and are not equally undoable — stopping a drain
    is reversible, `FALLBACK-CLAUDE` is not. RED against the old code at
    `_handed_off(queue) == []`.
    """
    queue = _grok_queue(tmp_path)
    harness = _harness(fake_grok, lock_path, auth_probe=_SequencedAuth(_UNKNOWN))

    report = queue.drain(harness)

    assert report.lane_state == "auth_unknown"
    assert report.fired == 0, "the lane was unsafe to fire, so nothing fired"
    assert _handed_off(queue) == [], "'the CLI did not answer' is not a finding about Grok"
    assert not (queue.root / "AUTH-BLOCKED.md").exists()
    assert len(queue.pending()) == 3, "the work stayed on this lane, still ownable"
    assert "NOTHING HANDED OFF" in (report.stopped_reason or "")

    # NOT SILENT — the reporter surface carries it, with the count it did not touch.
    events = [e for e in queue.telemetry.events() if e["event"] == "lane_stopped_unconfirmed"]
    assert len(events) == 1
    assert events[0]["pending_jobs"] == 3
    assert events[0]["passthrough"]["jobs_handed_to_claude"] == 0
    assert events[0]["passthrough"]["matt_only_action"] is False

    # And it did NOT write the per-job ledger: a terminal marker would claim ownership
    # moved, a busy marker would wedge the "last row terminal" liveness check with
    # nothing running. This is a LANE event with no JOB in it.
    assert [r for r in queue.runlog.rows() if r[2] == "AUTH-BLOCKED"] == []


def test_D12_a_CONFIRMED_expiry_STILL_files_and_STILL_hands_off(tmp_path, fake_grok, lock_path):
    """The remedy must not have cost the real path. Three consecutive readings -> handoff."""
    queue = _grok_queue(tmp_path)
    harness = _harness(fake_grok, lock_path, auth_probe=_SequencedAuth(_EXPIRED))

    report = queue.drain(harness)

    assert report.lane_state == "auth_expired"
    assert _handed_off(queue) == ["j0.json", "j1.json", "j2.json"]
    assert (queue.root / "AUTH-BLOCKED.md").exists()
    assert queue.runlog.last_row()[2] == "FALLBACK-CLAUDE"


def test_D12_an_UNREADABLE_SEMAPHORE_stops_the_drain_but_does_not_move_ownership(
    tmp_path, fake_grok, lock_path
):
    """Q.1 fails closed on FIRING — correctly. It must not also fail closed on OWNERSHIP.

    A blind instrument says the queue cannot SEE the lane. It says nothing about whether
    Grok can do the work, so it cannot be the finding that spends the one-way door.
    """
    queue = _grok_queue(tmp_path)
    harness = _harness(fake_grok, lock_path)
    # The instrument going BLIND, expressed directly rather than by breaking a real
    # lock file: `all_unreadable` is the condition Q.1 names, and constructing it is
    # honest about what is under test here (the OWNERSHIP consequence), not the
    # semaphore primitive, which D-12's sibling file already proves with real flocks.
    harness.slot_occupancy = lambda: SlotOccupancy(
        total=3, held=3, free=0, unreadable=3, tags=("unreadable",))

    report = queue.drain(harness)

    assert report.lane_state == "auth_unknown"
    assert _handed_off(queue) == []
    assert not (queue.root / "AUTH-BLOCKED.md").exists()


# ===========================================================================
# 13 — THE IMAGE LANE: `--prompt-json` + inline ACP `image` blocks
#
# `grok` publishes NO `--image` flag, and knight-rider's first ruling read that flag
# surface and concluded the lane had no image door at all. It has one; it is just not a
# flag. The CLI enumerates the door in its own rejection of a wrong guess — *"unknown
# variant `image_url`, expected one of `text`, `image`, `audio`, `resource_link`,
# `resource`"* — and TWO of those five carry an image. Both were probed live. The
# rows below pin the one that was wired and the reasons the other was not.
#
# THE RISK HERE WAS NEVER THAT IMAGES BREAK. It is that adding an image parameter
# perturbs the argv of every job that sends NONE — mid-banking-window, where the
# baseline is being measured. The identity row is the one that actually matters.
# ===========================================================================
def test_NO_IMAGES_leaves_the_grok_argv_BYTE_IDENTICAL_to_the_pre_image_build():
    """The pin. Compared against a LITERAL, not against a re-derivation of the builder.

    A row asserting `build_argv(...) == build_argv(...)` would pass no matter what the
    builder did to every call. This is the argv as it stood before `--prompt-json`
    existed, written out by hand.

    ⚑ **This lane is inside its 10-job banking window** (Amendment I), so an argv
    perturbation here does not merely change future jobs — it corrupts the baseline
    while the baseline is being measured, and the corruption would be invisible.
    """
    expected = [
        "/bin/grok", "-p", "hello", "--output-format", "json",
        NO_LEADER_FLAG,
        "-m", MODEL_PIN,
        "--reasoning-effort", REASONING_EFFORT_PIN,
        "--permission-mode", "default",
        "--disable-web-search",
    ]
    harness = GrokHarness(executable="/bin/grok", lock_path=None)
    assert harness.build_argv("hello", _cfg()) == expected
    assert harness.build_argv("hello", _cfg(images=[])) == expected, (
        "an EMPTY list must be indistinguishable from no key at all, or every caller "
        "that defensively passes `images=[]` gets a different invocation than one that "
        "does not"
    )
    assert "--prompt-json" not in harness.build_argv("hello", _cfg())


def _png(path: Path, payload: bytes = b"\x89PNG\r\n\x1a\n") -> Path:
    path.write_bytes(payload)
    return path


def _blocks_from(argv: list[str]) -> list[dict]:
    return json.loads(argv[argv.index("--prompt-json") + 1])


def test_IMAGES_DISPLACE_the_p_flag_and_travel_as_INLINE_ACP_CONTENT_BLOCKS(tmp_path):
    """`--prompt-json` REPLACES `-p`. That displacement is the whole hazard of this path.

    The prompt stops being its own argv string, so anything bounding the `-p` payload is
    measuring a string that is no longer there.
    """
    one = _png(tmp_path / "a.png")
    two = _png(tmp_path / "b.png", b"\x89PNG-two")
    argv = GrokHarness(executable="/bin/grok", lock_path=None).build_argv(
        "look at these", _cfg(images=[one, str(two)]))

    assert "-p" not in argv, "`-p` survived alongside `--prompt-json`; they are exclusive"
    blocks = _blocks_from(argv)
    assert blocks[0] == {"type": "text", "text": "look at these"}
    assert [b["type"] for b in blocks[1:]] == ["image", "image"]
    assert all(b["mimeType"] == "image/png" for b in blocks[1:])
    # base64 of the real bytes, not a path reference.
    assert base64.b64decode(blocks[1]["data"]) == one.read_bytes()
    assert base64.b64decode(blocks[2]["data"]) == two.read_bytes()
    # Every pin still said, on the path that displaced the prompt.
    assert argv[argv.index("-m") + 1] == MODEL_PIN
    assert NO_LEADER_FLAG in argv


def test_the_IMAGE_LIST_IS_LOAD_BEARING_and_N_crops_all_arrive(tmp_path):
    """*"Here are four crops of the same mark; are they the same effect in four colours?"*

    That is the characteristic job of this lane per the image-lane ruling — premise-checks
    against SEVERAL small crops at once. A door that carried one image would satisfy the
    flag surface and miss the use case.
    """
    crops = [_png(tmp_path / f"crop-{i}.png", b"\x89PNG" + bytes([i])) for i in range(4)]
    argv = GrokHarness(executable="/bin/grok", lock_path=None).build_argv(
        "same effect?", _cfg(images=crops))
    blocks = _blocks_from(argv)
    assert len(blocks) == 5, "one text block plus four images"
    assert [base64.b64decode(b["data"]) for b in blocks[1:]] == [c.read_bytes() for c in crops]


def test_a_NAMED_IMAGE_THAT_DOES_NOT_EXIST_is_REFUSED_at_argv_not_dropped(tmp_path):
    """⚑ **This is the row `resource_link` could not have.**

    Probed live, 2026-08-25: a `resource_link` block naming a nonexistent file returned
    **rc=0**. The CLI never looked at the path; a whole model call was launched and paid
    for ($0.0061, 28 s) and the MODEL discovered at runtime the file was missing. It said
    so only because the probe prompt told it to — absent that instruction it answers
    fluently about nothing, in the exact register of an answer about something.

    Inline blocks are refusable here: free, certain, and before a process exists.
    """
    with pytest.raises(ValueError, match="does not exist"):
        GrokHarness(executable="/bin/grok", lock_path=None).build_argv(
            "x", _cfg(images=[tmp_path / "nope.png"]))


def test_a_BARE_STRING_in_images_is_REFUSED_rather_than_iterated_per_character(tmp_path):
    png = _png(tmp_path / "a.png")
    with pytest.raises(ValueError, match="must be a LIST"):
        GrokHarness(executable="/bin/grok", lock_path=None).build_argv(
            "x", _cfg(images=str(png)))


def test_an_UNPROBED_IMAGE_FORMAT_is_REFUSED_BY_NAME_rather_than_guessed(tmp_path):
    """PNG / JPEG / WEBP were each FIRED AT THE LIVE VENDOR. GIF was not.

    This file already refuses `--tools` and declines to say `--sandbox` on exactly this
    ground: declaring a vocabulary nobody enumerated is how a caller reads as supported
    while not being. A mimeType the vendor mishandles fails on a lane whose entire
    purpose is to look at the picture.
    """
    gif = _png(tmp_path / "a.gif", b"GIF89a")
    with pytest.raises(ValueError, match="CLOSED set"):
        GrokHarness(executable="/bin/grok", lock_path=None).build_argv("x", _cfg(images=[gif]))
    for suffix in (".png", ".jpg", ".jpeg", ".webp"):
        assert suffix in IMAGE_MIME_BY_SUFFIX


def test_the_CEILING_IS_ENFORCED_AGAINST_THE_PAYLOAD_THAT_ACTUALLY_TRAVELS(tmp_path):
    """⚑ **The instrument that returned cleanly after it stopped answering the question.**

    `MAX_PROMPT_ARGV_BYTES` is enforced against the `-p` payload. `--prompt-json`
    DISPLACES `-p`. So on an image job the old ceiling measures a string that is not
    there, and a payload of any size would have sailed past it into an `E2BIG` from the
    OS — which names no file and no reason.

    Both directions are pinned: a payload OVER the `-p` ceiling but under this path's own
    is ACCEPTED (proving the wrong ceiling is not being misapplied to the new path), and
    a payload over this path's ceiling is REFUSED **naming the file, its encoded size and
    the limit**, because the caller's next action is to crop something and they need to
    know which something.
    """
    harness = GrokHarness(executable="/bin/grok", lock_path=None)

    # 300 KB raw -> 400 KB base64: over MAX_PROMPT_ARGV_BYTES (256 KiB), under
    # MAX_PROMPT_JSON_ARGV_BYTES (512 KiB). Accepted.
    big = _png(tmp_path / "big.png", b"\x89PNG" + b"\x00" * 300_000)
    argv = harness.build_argv("x", _cfg(images=[big]))
    payload = argv[argv.index("--prompt-json") + 1]
    assert len(payload.encode()) > MAX_PROMPT_ARGV_BYTES
    assert len(payload.encode()) <= MAX_PROMPT_JSON_ARGV_BYTES

    # A FULL ANALYSIS FRAME. `zoom_ww7_full.png` — the frame galadriel's P-2 ruling rests
    # on — is 1,959,839 bytes raw / 2,613,120 base64: 2.49x this host's ENTIRE ARG_MAX.
    # The frame that fails is the one nobody should be sending.
    frame = _png(tmp_path / "zoom_ww7_full.png", b"\x89PNG" + b"\x00" * 1_959_835)
    with pytest.raises(ValueError) as exc:
        harness.build_argv("x", _cfg(images=[frame]))
    message = str(exc.value)
    assert "zoom_ww7_full.png" in message, "the refusal must NAME THE FILE"
    assert str(MAX_PROMPT_JSON_ARGV_BYTES) in message, "the refusal must name the LIMIT"
    assert "2613120" in message.replace(",", "") or "base64" in message, (
        "the refusal must name the ENCODED size, not the raw one — the encoded size is "
        "what travels")
    assert "NATIVE" in message, (
        "the remedy must say CROP, not downscale: downscaling erases the 1-3 px detail "
        "these jobs exist to look for, and would return a false null")


def test_the_LARGEST_image_is_NAMED_when_several_crops_share_the_blame(tmp_path):
    """Four crops over the ceiling together is not four equal suspects."""
    small = _png(tmp_path / "small.png", b"\x89PNG" + b"\x00" * 1_000)
    huge = _png(tmp_path / "huge.png", b"\x89PNG" + b"\x00" * 500_000)
    with pytest.raises(ValueError, match="LARGEST IMAGE.*huge.png"):
        GrokHarness(executable="/bin/grok", lock_path=None).build_argv(
            "x", _cfg(images=[small, huge, small]))


# ---------------------------------------------------------------------------
# The PHYSICS check — `execve` charges for argv AND environ, together
# ---------------------------------------------------------------------------
def test_the_ARGV_EXEC_COST_FORMULA_IS_EXACT_AGAINST_THIS_HOST():
    """⚑ Asserted against **the operating system**, not against our own arithmetic.

    The declared ceilings are POLICY. `ARG_MAX` is PHYSICS, and it bounds argv and the
    inherited ENVIRONMENT together — so the usable argv budget is not a constant, it
    shrinks by exactly the size of the environment the child inherits.

    This row pins the formula AND the comparison operator at the boundary: an invocation
    costing exactly `ARG_MAX` must EXECUTE, and one costing a single byte more must
    raise `OSError`. If either half flips, `build_argv`'s refusal is off by one in a
    direction that either rejects legal jobs or lets `E2BIG` through.
    """
    limit = host_arg_max()
    assert limit > 0
    env = {"PATH": "/usr/bin"}
    fixed = argv_exec_cost(["/usr/bin/true", ""], env)
    at_limit = "x" * (limit - fixed)

    subprocess.run(["/usr/bin/true", at_limit], env=env, capture_output=True, timeout=30)
    assert argv_exec_cost(["/usr/bin/true", at_limit], env) == limit

    with pytest.raises(OSError):
        subprocess.run(["/usr/bin/true", at_limit + "x"], env=env, capture_output=True,
                       timeout=30)


def test_a_FAT_ENVIRONMENT_SHRINKS_THE_ARGV_BUDGET_and_the_check_SEES_IT(tmp_path, monkeypatch):
    """The half everyone forgets. Measured: a 100 KB variable cost 100,022 argv bytes.

    ⚑ **A payload can clear EVERY declared ceiling and still be `E2BIG`** — and `E2BIG`
    arrives as a bare `OSError` from `subprocess` naming no file, no size and no reason.
    The images below are legal on both policy ceilings; only the environment makes this
    invocation impossible, and only the physics check can see that.

    **This row is matched on the PHYSICS refusal's own words, not on `ARG_MAX`.** An
    earlier draft matched `ARG_MAX` and passed against pre-fix source — because the
    `-p` ceiling's message ALSO contains that token. It was green for the wrong reason,
    which is the defect this whole section is about wearing a test's clothing.
    """
    lean = argv_exec_cost(["/bin/grok", "hello"], {"PATH": "/usr/bin"})
    monkeypatch.setenv("SL_PROBE_PAD", "P" * 100_000)
    fat = argv_exec_cost(["/bin/grok", "hello"])
    assert fat - lean > 100_000

    # ~400 KB base64: under MAX_PROMPT_JSON_ARGV_BYTES, so the policy ceiling passes it.
    crop = _png(tmp_path / "crop.png", b"\x89PNG" + b"\x00" * 300_000)
    harness = GrokHarness(executable="/bin/grok", lock_path=None)
    assert harness.build_argv("x", _cfg(images=[crop])), "legal before the environment grows"

    monkeypatch.setenv("SL_PROBE_PAD2", "P" * (host_arg_max() - 200_000))
    with pytest.raises(ValueError, match="inherited environment"):
        harness.build_argv("x", _cfg(images=[crop]))


def test_the_PHYSICS_CHECK_IS_INERT_on_the_p_path_under_a_normal_environment():
    """It is here anyway, and the docstring says why.

    `MAX_PROMPT_ARGV_BYTES` is 256 KiB and the `-p` path cannot reach `ARG_MAX` under any
    environment this host has had. But *"cannot reach it today"* is a fact about the
    ENVIRONMENT, not about the code — exactly the kind of fact that stops being true
    quietly. A bound that covers one path when there are two is what this whole section
    exists to correct; adding a second uncovered path would repeat it.
    """
    harness = GrokHarness(executable="/bin/grok", lock_path=None)
    argv = harness.build_argv("x" * MAX_PROMPT_ARGV_BYTES, _cfg())
    assert argv_exec_cost(argv) < host_arg_max()


def test_RESOURCE_LINK_IS_NEVER_EMITTED_even_though_it_WORKS(tmp_path):
    """It was probed, it returned correct image comprehension, and it is NOT the door.

    | door | turns | cost, same answer | nonexistent path |
    |---|---|---|---|
    | inline `image` | 1 | $0.0045 | refused here, free |
    | `resource_link` | 2 | $0.0075 - $0.0112 | **rc=0, $0.0061, 28 s** |

    It is a POINTER THE MODEL RESOLVES WITH ITS OWN FILE-READ TOOL, not an attachment:
    `num_turns: 2`, the model's own *"Let me read the image first"*, and a nonexistent
    path that nobody refused. It also does not save context (17.5 K / 31.9 K input tokens
    against 11.5 K inline), so it buys no budget either — and it makes correctness depend
    on the agent's tool fence and `cwd`, surfaces this lane deliberately does not control.
    """
    argv = GrokHarness(executable="/bin/grok", lock_path=None).build_argv(
        "x", _cfg(images=[_png(tmp_path / "a.png")]))
    assert "resource_link" not in json.dumps(_blocks_from(argv))
    assert {b["type"] for b in _blocks_from(argv)} == {"text", "image"}
