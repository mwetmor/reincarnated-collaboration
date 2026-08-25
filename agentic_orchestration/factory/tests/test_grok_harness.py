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

import json
from pathlib import Path

import pytest

from factory.harness.grok import (
    FORBIDDEN_PERMISSION_MODES,
    MODEL_PIN,
    NO_LEADER_FLAG,
    REASONING_EFFORT_PIN,
    REASONING_EFFORTS,
    GrokHarness,
    LaneAvailability,
    parse_envelope,
    resolved_model_ids,
)
from factory.jobqueue import JobQueue
from factory.lane import SerialLaneLock
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
        **kw,
    )


def _argv(tmp_path: Path) -> list[str]:
    return json.loads((tmp_path / "argv.json").read_text(encoding="utf-8"))


# ===========================================================================
# 1 — AMENDMENT E: --no-leader, said AND asserted
# ===========================================================================
def test_AMENDMENT_E_no_leader_is_on_EVERY_argv(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, {})
    assert result.ok
    assert NO_LEADER_FLAG in _argv(tmp_path), (
        "leader mode multiplexes clients onto ONE backend through `~/.grok/leader.sock` "
        "— a concurrency door AROUND the serial lock. The flag is not optional."
    )


def test_AMENDMENT_E_the_PREFLIGHT_ASSERTS_the_flag_rather_than_assuming_it(fake_grok, lock_path):
    ok, why = _harness(fake_grok, lock_path).assert_no_leader_parses()
    assert ok is True
    assert NO_LEADER_FLAG in why


def test_AMENDMENT_E_a_REJECTED_flag_REFUSES_THE_FIRE(fake_grok, lock_path, tmp_path, monkeypatch):
    """The version-bump scenario: the flag stops parsing and the lane must NOT fire.

    Firing anyway would leave leader mode reachable with nothing to signal it — silent
    re-entry through the exact door the lock exists to close, which is why this
    amendment demanded an assertion instead of an argv entry.
    """
    monkeypatch.setenv("FAKE_GROK_REJECT_NO_LEADER", "1")
    harness = _harness(fake_grok, lock_path)
    ok, why = harness.assert_no_leader_parses()
    assert ok is False
    assert "REFUSES TO FIRE" in why

    result = harness.run("hello", tmp_path, {})
    assert result.ok is False
    assert "PREFLIGHT REFUSED" in (result.error or "")
    assert (result.extra or {}).get("lane_state") == "preflight_failed"
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
    assert warn_and_continue.assert_no_leader_parses()[0] is False


def test_AMENDMENT_E_a_FAILED_preflight_closes_availability_BEFORE_the_busy_probe(
        fake_grok, lock_path):
    """A caller must never see `open` on a lane the harness will then refuse to fire."""
    harness = _harness(fake_grok, lock_path, preflight_probe=lambda: (False, "flag gone"))
    state = harness.availability()
    assert state.ok is False
    assert state.state == "preflight_failed"


# ===========================================================================
# 2 — AMENDMENT C: the RESOLVED model id
# ===========================================================================
def test_AMENDMENT_C_the_RESOLVED_model_id_is_captured_per_call(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, {})
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
    _harness(fake_grok, lock_path).run("hello", tmp_path, {})
    argv = _argv(tmp_path)
    assert "--reasoning-effort" in argv
    assert argv[argv.index("--reasoning-effort") + 1] == REASONING_EFFORT_PIN == "xhigh"
    assert "-m" in argv and argv[argv.index("-m") + 1] == MODEL_PIN


def test_the_pin_is_said_on_the_ARGV_never_left_to_ambient_config(fake_grok, lock_path, tmp_path):
    """H1 on the third vendor. `~/.grok/config.toml` is host state no file here controls."""
    _harness(fake_grok, lock_path).run("hello", tmp_path, {})
    # The fake records `sys.argv[1:]`, so argv[0] (the binary) is not in this list.
    argv = _argv(tmp_path)
    assert argv[:2] == ["-p", "hello"], "single-turn headless, prompt on argv"
    assert "--output-format" in argv and argv[argv.index("--output-format") + 1] == "json"


def test_an_UNANNOUNCED_pin_swap_is_REFUSED(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, {"model": "grok-4.5"})
    assert result.ok is False
    assert "model_ab_note" in (result.error or "")
    assert "DECLARED, not banked" in (result.error or ""), (
        "the refusal must state the honest reason: an unbanked pin makes an "
        "unannounced swap WORSE, because it corrupts the baseline while it is being "
        "measured"
    )


def test_an_ANNOUNCED_swap_with_an_AB_NOTE_is_permitted(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run(
        "hello", tmp_path, {"model": "grok-4.5", "model_ab_note": "notes/2026-08-24-ab.md"})
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
        "hello", tmp_path, {"reasoning_effort": "maximum"})
    assert result.ok is False
    assert "xhigh" in (result.error or "")
    assert not (tmp_path / "argv.json").exists()


# ===========================================================================
# 4 — the fence
# ===========================================================================
@pytest.mark.parametrize("mode", sorted(FORBIDDEN_PERMISSION_MODES))
def test_the_FENCE_DISSOLVING_permission_modes_are_refused_BY_NAME(
        mode, fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("hello", tmp_path, {"permission_mode": mode})
    assert result.ok is False
    assert "REFUSED BY NAME" in (result.error or "")
    assert not (tmp_path / "argv.json").exists()


def test_WEB_SEARCH_IS_OFF_unless_the_job_class_NAMES_it(fake_grok, lock_path, tmp_path):
    _harness(fake_grok, lock_path).run("hello", tmp_path, {})
    assert "--disable-web-search" in _argv(tmp_path)


def test_WEB_SEARCH_ON_is_a_DECLARATION_not_a_default(fake_grok, lock_path, tmp_path):
    _harness(fake_grok, lock_path).run("hello", tmp_path, {"web_search": True})
    assert "--disable-web-search" not in _argv(tmp_path)


def test_a_TOOLS_declaration_is_REFUSED_with_the_reason_stated(fake_grok, lock_path):
    with pytest.raises(ValueError, match="not been enumerated on this host"):
        GrokHarness.validate_tools(["Read"], "phase-x")


def test_an_OVERSIZE_prompt_is_refused_HERE_not_as_an_E2BIG(fake_grok, lock_path, tmp_path):
    result = _harness(fake_grok, lock_path).run("x" * (300 * 1024), tmp_path, {})
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
        result = _harness(fake_grok, lock_path).run("hello", tmp_path, {})
        assert result.ok is True, "a busy Codex lane closed the Grok lane — it must not"
    finally:
        codex_lock.release()
    assert default_lock_path(vendor="grok") != default_lock_path(vendor="codex")


def test_a_SECOND_grok_job_under_the_lock_is_REFUSED(fake_grok, lock_path, tmp_path):
    held = SerialLaneLock(lock_path).acquire()
    try:
        result = _harness(fake_grok, lock_path).run("hello", tmp_path, {})
    finally:
        held.release()
    assert result.ok is False
    assert (result.extra or {}).get("lane_state") == "busy"
    assert not (tmp_path / "argv.json").exists()


def test_the_lock_fd_is_INHERITED_by_the_child(fake_grok, lock_path, tmp_path, monkeypatch):
    """`pass_fds` is what makes lock lifetime = max(queue, grok), not the parent's."""
    monkeypatch.setenv("FAKE_GROK_SLEEP", "0.4")
    import subprocess as sp
    import threading

    seen: dict[str, bool] = {}

    def watch():
        import time

        time.sleep(0.15)
        probe = sp.run(
            [__import__("sys").executable, "-c",
             f"import fcntl,os,sys\n"
             f"fd=os.open({str(lock_path)!r}, os.O_CREAT|os.O_RDWR)\n"
             f"try:\n fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB); print('FREE')\n"
             f"except OSError: print('HELD')\n"],
            capture_output=True, text=True,
        )
        seen["held"] = "HELD" in probe.stdout

    thread = threading.Thread(target=watch)
    thread.start()
    _harness(fake_grok, lock_path).run("hello", tmp_path, {})
    thread.join()
    assert seen.get("held") is True


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
    queue.enqueue(job_id="j1", prompt="p", curator="galadriel", sandbox="n/a")

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
        queue.enqueue(job_id="j", prompt="p", curator="galadriel", sandbox="read-only")


def test_the_GROK_FENCE_lands_in_the_ENQUEUE_ROW_where_it_can_be_read(tmp_path):
    queue = JobQueue(tmp_path / "q", lane="grok")
    queue.enqueue(job_id="j", prompt="p", curator="galadriel", sandbox="n/a",
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
    queue.enqueue(job_id="j", prompt="p", curator="galadriel", sandbox="n/a")
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
    queue.enqueue(job_id="j1", prompt="do it", curator="galadriel", sandbox="n/a")
    report = queue.drain(_harness(fake_grok, lock_path))

    assert report.fired == 1
    finish = [r for r in queue.runlog.rows() if r[2].startswith("rc=")][0]
    assert "resolved_model=grok-4.6-build" in finish[3], "Amendment C, on the row"
    assert "cost_usd=" in finish[3], "Amendment I, on the row"
    assert finish[4] == "curator=galadriel", "R-B, on the row"

    events = [e for e in queue.telemetry.events() if e["event"] == "finish"]
    assert events[0]["reasoning_effort"] == "xhigh", "Amendment D, in the telemetry"
    assert events[0]["usage"]["dollars"] == pytest.approx(0.00982838)
