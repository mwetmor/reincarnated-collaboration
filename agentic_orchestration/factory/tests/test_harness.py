"""Harness adapters — Spec A § 5, and the O1 flag surface it was probed against.

The argv tests are the load-bearing ones. `--verbose` is not a preference: the
CLI exits 1 before any API call without it when stream-json is requested in
print mode, so an adapter that forgets it burns a phase for nothing. And no
`--model` may ever appear, because model policy belongs to the launcher session.

The parse tests run against the RECORDED probe stream, not a hand-built
imitation of one.
"""

from pathlib import Path

import pytest

from factory.harness import available_harnesses, get_harness
from factory.harness.claude_code import (
    PINNED_PERMISSION_MODE,
    ClaudeCodeHarness,
    check_grant,
    parse_frames,
)
from factory.harness.codex import (
    MODEL_PIN,
    MODEL_REASONING_EFFORT_PIN,
    CodexHarness,
    LaneAvailability,
)

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "claude_stream_probe.jsonl"


@pytest.fixture
def h() -> ClaudeCodeHarness:
    return ClaudeCodeHarness()


# ---------------------------------------------------------------------------
# argv — the O1 flag surface, pinned
# ---------------------------------------------------------------------------
def test_argv_carries_the_probed_flag_surface(h):
    argv = h.build_argv("do the thing", {"agent": "star-lord", "tools": ["Read"]})
    assert argv[0] == "claude"
    assert argv[1:3] == ["--agent", "star-lord"]
    assert "-p" in argv and argv[argv.index("-p") + 1] == "do the thing"
    assert argv[argv.index("--output-format") + 1] == "stream-json"


def test_verbose_is_always_present(h):
    """Without it the CLI exits 1 before any API call (probed 2026-08-10)."""
    for config in ({"agent": "a", "tools": ["Bash"]}, {"agent": "a", "tools": ["Read"]}):
        assert "--verbose" in h.build_argv("x", config)


def test_no_model_flag_is_ever_emitted(h):
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read"], "add_dirs": ["/tmp"]})
    assert not any(a.startswith("--model") for a in argv)


def test_a_model_key_in_the_config_is_refused_loudly(h):
    with pytest.raises(ValueError, match="model policy"):
        h.build_argv("x", {"agent": "a", "model": "claude-opus-4"})


def test_a_phase_without_an_agent_is_refused(h):
    with pytest.raises(ValueError, match="requires a named seam"):
        h.build_argv("x", {})


def test_no_permission_skipping_flag_appears_anywhere(h):
    """H1 amended this row, and the amendment is the finding.

    It used to assert `--permission-mode` was ABSENT, on the reading that any
    mention of permission modes was a step toward skipping them. Absent is not
    safe: with no flag the mode comes from `~/.claude/settings.json`, and on this
    host that file carries `defaultMode: bypassPermissions` — so the row certifying
    that we never skip permissions was passing on a lane that skipped all of them.
    The safe state is the mode PINNED, not unmentioned.
    """
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read", "Bash"]})
    joined = " ".join(argv)
    assert "--dangerously-skip-permissions" not in joined
    assert argv[argv.index("--permission-mode") + 1] == PINNED_PERMISSION_MODE
    assert PINNED_PERMISSION_MODE not in ("bypassPermissions", "acceptEdits", "plan"), (
        "the pin itself was moved to a mode that does not enforce. In "
        "`bypassPermissions` the `permission_denials` list cannot fire, so every "
        "denial-based assertion on this lane would pass by being structurally silent."
    )


def test_the_tool_allowlist_reaches_both_flags(h):
    """H2: the two flags no longer receive the same string, and that is measured.

    `--tools` rejects the scoped form — `Bash(git status:*)` is dropped on the floor,
    silently — so it receives base names; `--allowedTools` is where the scoping has
    to survive. Sending one string to both was the bug: the scope was either lost or
    the flag was.
    """
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read", "Grep"]})
    assert argv[argv.index("--tools") + 1] == "Grep,Read"
    assert argv[argv.index("--allowedTools") + 1] == "Read,Grep"


def test_H2_the_SCOPED_form_survives_on_allowedTools_and_is_stripped_for_tools(h):
    """One declaration, two shapes, because the flags do not accept the same one."""
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read", "Bash(git status:*)"]})
    assert argv[argv.index("--tools") + 1] == "Bash,Read", (
        "a scoped form reached `--tools`, which drops it silently — the phase would "
        "run without the tool it declared"
    )
    assert argv[argv.index("--allowedTools") + 1] == "Read,Bash(git status:*)", (
        "the scope was stripped from `--allowedTools` too, which is where it is the "
        "whole point: `Bash` unscoped is a different fence from `Bash(git status:*)`"
    )


def test_extra_directories_are_passed_one_flag_each(h):
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read"], "add_dirs": ["/one", "/two"]})
    assert argv.count("--add-dir") == 2


def test_an_absent_binary_is_a_failed_result_not_an_exception(tmp_path):
    result = ClaudeCodeHarness(executable="claude-that-does-not-exist").run(
        "x", tmp_path, {"agent": "a", "tools": ["Read"]}
    )
    assert result.ok is False
    assert "not found on PATH" in result.error
    assert result.usage.billable_token_total() is None


# ---------------------------------------------------------------------------
# stream parsing — against the recording
# ---------------------------------------------------------------------------
def test_parses_the_recorded_stream():
    frames = parse_frames(FIXTURE.read_text())
    assert frames, "the recorded probe stream parsed to nothing"
    assert any(f.get("type") == "result" for f in frames)


def test_unparseable_lines_are_skipped_not_guessed_at():
    stream = '{"type":"system"}\nthis is not json\n{"type":"result","result":"ok"}\n'
    frames = parse_frames(stream)
    assert len(frames) == 2
    assert frames[-1]["result"] == "ok"


def test_an_empty_stream_parses_to_nothing():
    assert parse_frames("") == []
    assert parse_frames("\n\n  \n") == []


def test_the_result_frame_carries_what_the_spine_needs():
    frames = parse_frames(FIXTURE.read_text())
    result = next(f for f in reversed(frames) if f.get("type") == "result")
    for key in ("result", "session_id", "usage", "is_error"):
        assert key in result, f"the recorded result frame lost `{key}` — re-probe, don't patch"


# ---------------------------------------------------------------------------
# the registry and the vendor lanes
# ---------------------------------------------------------------------------
def test_all_THREE_lanes_are_registered():
    """Renamed from `test_both_lanes_are_registered` when the third lane landed.

    The NAME is part of the assertion here. A row called *both* asserting a set of
    three is a row whose title stopped being true, and the next lane would arrive
    against a header nobody trusts. Grok registers 2026-08-24 under D-6.
    """
    assert set(available_harnesses()) == {"claude_code", "codex", "grok"}


def test_an_unknown_harness_name_raises_at_lookup():
    with pytest.raises(KeyError, match="no harness registered"):
        get_harness("telepathy")


def _codex(tmp_path, *, auth_ok=True, state="open", reason="Logged in using ChatGPT"):
    return CodexHarness(
        executable="codex",
        lock_path=tmp_path / "lane.lock",
        auth_probe=lambda: LaneAvailability(auth_ok, state, reason),
    )


def test_available_TELLS_THE_TRUTH_IN_BOTH_DIRECTIONS(tmp_path):
    """This row replaced `assert CodexHarness().available() is False`.

    That assertion was CORRECT while the lane was a stub and would have gone RED the
    moment the body was filled — which is exactly why the instruction was to UPDATE it
    rather than delete it. A deleted test is how `available()` stops telling the
    truth: the one-directional version could not distinguish a lane that is open from
    a lane whose `available()` had been quietly hardcoded, and neither can an absent
    one.

    So both directions are asserted here, and the reason is asserted with them —
    because a bare `False` cannot tell an operator whether to wait (busy) or to fetch
    Matt (auth).
    """
    open_lane = _codex(tmp_path)
    assert open_lane.available() is True
    assert open_lane.unavailable_reason() == ""

    expired = _codex(tmp_path, auth_ok=False, state="auth_expired", reason="token gone")
    assert expired.available() is False
    assert "auth_expired" in expired.unavailable_reason()


def test_the_REAL_auth_check_reads_the_CLI_and_fails_closed(tmp_path):
    """`check_auth` itself, not an injected stand-in.

    The row above injects an `auth_probe`, which is what makes the AVAILABILITY
    contract testable — and which means it never exercises the production auth path.
    Two probes with the same shape, one of which tests nothing, is how a green suite
    ends up saying nothing about the thing under review, so this row runs the real
    method against a real `codex` binary.

    THE POSITIVE FIXTURE WRITES TO **STDERR**, AND THAT IS THE POINT OF THIS ROW.
    Measured on this host, `codex login status` returns rc=0 with **stdout empty** and
    `Logged in using ChatGPT` on **stderr**. `check_auth` shipped reading `proc.stdout`
    — so it reported `auth_expired` unconditionally, and the queue would never have
    drained a single job. The earlier version of this fixture `echo`-ed to stdout,
    which meant the test was written against the same wrong belief as the code and
    agreed with it. A fake that shares the bug's premise cannot find the bug.

    The stdout-only fixture is kept BESIDE it, because a fix that reads only stderr
    would be the same defect mirrored, and nothing here should pass by luck.

    HONESTY ABOUT WHAT THIS MEASURES. The NEGATIVE branch is still REASONED, NOT
    MEASURED — verifying the vendor's actual not-logged-in text requires
    `codex logout`, a Matt-only action on a live lane. So it asserts the CONTRACT (a
    non-zero exit or an unrecognised answer reads as closed, and the reason names the
    Matt-only response), not the vendor's wording.
    """
    on_stderr = tmp_path / "codex-in-stderr"
    on_stderr.write_text(
        "#!/bin/sh\n>&2 echo 'Logged in using ChatGPT'\nexit 0\n", encoding="utf-8"
    )
    on_stderr.chmod(0o755)
    state = CodexHarness(executable=str(on_stderr)).check_auth()
    assert state.ok is True, (
        "the vendor answers on STDERR with an EMPTY stdout. A check that reads one "
        "stream reports a healthy lane as expired, forever, and every job is handed to "
        "the Claude lane with a matt_to_do row for an auth that never expired."
    )
    assert state.state == "open"

    on_stdout = tmp_path / "codex-in-stdout"
    on_stdout.write_text("#!/bin/sh\necho 'Logged in using ChatGPT'\nexit 0\n", encoding="utf-8")
    on_stdout.chmod(0o755)
    assert CodexHarness(executable=str(on_stdout)).check_auth().ok is True

    logged_out = tmp_path / "codex-out"
    logged_out.write_text("#!/bin/sh\n>&2 echo 'Not logged in'\nexit 1\n", encoding="utf-8")
    logged_out.chmod(0o755)
    state = CodexHarness(executable=str(logged_out)).check_auth()
    assert state.ok is False
    assert state.state == "auth_expired"
    # The RESPONSE is part of the contract, not just the verdict: re-auth is Matt-only
    # and this must never read as a retryable job failure.
    assert "MATT-ONLY" in state.reason.upper()
    assert "MUST NOT BE RETRIED" in state.reason.upper()

    # A CLI that answers rc=0 with something unrecognisable is ALSO closed. Absence of
    # a recognised answer is not a pass.
    ambiguous = tmp_path / "codex-huh"
    ambiguous.write_text("#!/bin/sh\n>&2 echo 'shrug'\nexit 0\n", encoding="utf-8")
    ambiguous.chmod(0o755)
    assert CodexHarness(executable=str(ambiguous)).check_auth().ok is False

    missing = CodexHarness(executable=str(tmp_path / "no-such-binary"))
    assert missing.check_auth().state == "cli_missing"


def test_available_reports_BUSY_when_the_serial_lane_is_held(tmp_path):
    """The second direction of "busy", which the stub could not have had.

    A lane that is authenticated and OCCUPIED is not an open lane, and reporting it as
    one is how two `codex exec` processes end up on one `auth.json`.
    """
    from factory.lane import SerialLaneLock

    harness = _codex(tmp_path)
    holder = SerialLaneLock(tmp_path / "lane.lock").acquire()
    try:
        assert harness.available() is False
        state = harness.availability()
        assert state.state == "busy"
        assert "NEVER parallel" in state.reason
    finally:
        holder.release()
    assert harness.available() is True


def test_the_codex_lane_RETURNS_A_RESULT_rather_than_raising(tmp_path):
    """It used to raise `NotImplementedError`. A live adapter must not raise at all.

    The spine records a `RawResult`; it cannot record an exception. So every
    operational condition — missing binary included — comes back as `ok=False` with an
    error that says which.
    """
    harness = CodexHarness(
        executable="codex-does-not-exist-xyz",
        lock_path=tmp_path / "lane.lock",
        auth_probe=lambda: LaneAvailability(True, "open", "stubbed ok"),
    )
    result = harness.run("x", tmp_path, {})
    assert result.ok is False
    assert "not found on PATH" in (result.error or "")
    assert result.usage.billable_token_total() is None
    assert result.usage.absent_reason


def test_the_model_pin_is_ON_THE_ARGV_not_left_to_ambient_config():
    """It lived only in `~/.codex/config.toml` — host state no file here controls.

    Every banked lane statistic was measured at this config, so where the pin is SAID
    is the difference between a reproducible baseline and a coincidence.
    """
    argv = CodexHarness().build_argv({"web_search": True, "output_path": "/tmp/x.md"})
    assert argv[:3] == ["codex", "exec", "--json"]
    assert argv[argv.index("-m") + 1] == MODEL_PIN
    assert f'model_reasoning_effort="{MODEL_REASONING_EFFORT_PIN}"' in argv
    assert argv[argv.index("-s") + 1] == "read-only"
    assert "tools.web_search=true" in argv
    assert argv[-1] == "-", "the prompt arrives on stdin, never on argv"


def test_a_silent_model_swap_is_REFUSED_and_an_evidenced_one_is_not():
    """Drift is loud at the call site, per U-4's A/B requirement.

    The refusal is not "you may not change the model". It is "you may not change it
    without naming the evidence", which is the difference between an experiment and a
    baseline that quietly stopped meaning anything.
    """
    h = CodexHarness()
    with pytest.raises(ValueError, match="A/B evidence"):
        h.build_argv({"model": "gpt-4o-mini"})
    argv = h.build_argv({"model": "gpt-4o-mini", "model_ab_note": "notes/ab-2026-09-01.md"})
    assert argv[argv.index("-m") + 1] == "gpt-4o-mini"


def test_an_unenumerated_sandbox_is_REFUSED():
    with pytest.raises(ValueError, match="not one of"):
        CodexHarness().build_argv({"sandbox": "read_only"})  # underscore, not hyphen


def test_the_codex_lane_REFUSES_a_tool_allowlist_it_cannot_enforce():
    """`codex exec` has no `--tools`. Accepting a list would be the fail-open."""
    with pytest.raises(ValueError, match="no tool allowlist"):
        CodexHarness.validate_tools(["Read"], "a phase")


def test_ABSENT_turn_completed_IS_the_failure_signal():
    """Measured with a bad `-m`: rc=1, a `turn.failed`, and NO `turn.completed`."""
    result = CodexHarness().adjudicate(
        [
            {"type": "thread.started", "thread_id": "t-1"},
            {"type": "turn.started"},
            {"type": "turn.failed", "error": {"message": "model not supported"}},
        ],
        returncode=1,
    )
    assert result.ok is False
    assert "no `turn.completed`" in (result.error or "")
    assert "model not supported" in (result.error or "")
    assert result.harness_session_id == "t-1"
    assert result.usage.billable_token_total() is None


def test_a_fallback_metadata_run_FAILS_rather_than_warns():
    """A run at fallback metadata is not a run at the pin, and the stats are ABOUT the pin."""
    result = CodexHarness().adjudicate(
        [
            {"type": "thread.started", "thread_id": "t-2"},
            {"type": "item.completed", "item": {
                "type": "error",
                "message": "Model metadata for `nope` not found. Defaulting to fallback metadata; "
                           "this can degrade performance and cause issues.",
            }},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "done"}},
            {"type": "turn.completed", "usage": {
                "input_tokens": 100, "cached_input_tokens": 40,
                "cache_write_input_tokens": 0, "output_tokens": 5,
                "reasoning_output_tokens": 2}},
        ],
        returncode=0,
    )
    assert result.ok is False
    assert "fallback metadata" in (result.error or "")
    # The usage is still recorded — the tokens were really spent.
    assert result.usage.billable_token_total() == 105


def test_a_clean_turn_carries_what_the_spine_needs():
    result = CodexHarness().adjudicate(
        [
            {"type": "thread.started", "thread_id": "t-3"},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "OK"}},
            {"type": "turn.completed", "usage": {
                "input_tokens": 17422, "cached_input_tokens": 9984,
                "cache_write_input_tokens": 0, "output_tokens": 5,
                "reasoning_output_tokens": 0}},
        ],
        returncode=0,
        model=MODEL_PIN,
    )
    assert result.ok is True
    assert result.text == "OK"
    assert result.model == MODEL_PIN
    assert result.exit_code == 0
    assert result.harness == "codex"
    # in(uncached) 7438 + out 5 + cache_read 9984 + cache_write 0
    assert result.usage.billable_token_total() == 7438 + 5 + 9984


def test_C3_an_agentic_phase_without_a_tools_allowlist_is_REFUSED():
    """The one allowlist in this spine that failed OPEN.

    `claude --help`: `--tools ... Use "" to disable all tools, "default" to use all
    tools`. So omitting the flag is not a neutral default — it is the full built-in
    set, chosen by no one. Every sibling allowlist here fails closed: an empty
    `writes` breaches everything, an empty `gates` is a load error. This one was
    proven to RESTRICT when declared and never proven to REFUSE when absent, which
    is Gate-2 B3's shape at the harness layer (Gate-2 C3).
    """
    h = ClaudeCodeHarness()
    for config in ({"agent": "a"}, {"agent": "a", "tools": []}):
        with pytest.raises(ValueError, match="tools"):
            h.build_argv("x", config)


def test_C3_a_denied_tool_call_is_not_a_passing_phase():
    """`permission_denials` was recorded and adjudicated by nothing.

    A phase that spent its turns being refused tools returned ok=True with a
    cheerful result string. A denial is the pre-hoc analogue of a breach — the phase
    reached outside its declared tools — and this spine does not treat a breach as
    noise. Weakened only on live evidence, the way the COARSE caveat is.
    """
    frame = {
        "type": "result", "subtype": "success", "is_error": False,
        "result": "all done!", "session_id": "s1", "num_turns": 3,
        "permission_denials": [{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}],
        "usage": {"input_tokens": 1, "output_tokens": 1},
    }
    # H1/H2: a clean grant, so the DENIAL is the only thing under test here. With
    # `init_frame=None` this row passed on the fail-closed grant check instead —
    # the right verdict for the wrong reason, which is the review's whole subject.
    init = {"type": "system", "subtype": "init",
            "permissionMode": PINNED_PERMISSION_MODE, "tools": ["Bash"]}
    declared = ["Bash"]
    ok_frame = {**frame, "permission_denials": []}
    clean = ClaudeCodeHarness().adjudicate(ok_frame, init, 0, 1, declared_tools=declared)
    assert clean.ok, f"a clean phase must still pass; error was {clean.error!r}"
    denied = ClaudeCodeHarness().adjudicate(frame, init, 0, 1, declared_tools=declared)
    assert not denied.ok, (
        "a phase whose tool calls were denied by its own allowlist came back ok=True. "
        "The denial is the only signal that the phase tried to leave its fence."
    )
    assert "denied" in (denied.error or ""), (
        f"the failure must say what happened; error was {denied.error!r}"
    )


def test_C3_both_tool_flags_are_emitted_because_neither_substitutes_for_the_other():
    """`--tools` selects what EXISTS; `--allowedTools` selects what may run unprompted.

    Passing only the second leaves the full built-in set present and merely
    prompting — and a headless run has nobody to prompt, so the phase stalls or the
    tool is denied. Passing only the first leaves declared tools asking permission
    nobody can grant. The refusal test above proves the flags are demanded; this
    proves they are DELIVERED, which is the other half of B3's shape.
    """
    argv = ClaudeCodeHarness().build_argv("x", {"agent": "star-lord", "tools": ["Read", "Grep"]})
    assert "--tools" in argv, "the phase would run with the CLI's full built-in set"
    assert "--allowedTools" in argv, "declared tools would still stop to ask permission"
    assert argv[argv.index("--tools") + 1] == "Grep,Read"
    assert argv[argv.index("--allowedTools") + 1] == "Read,Grep"
    assert "--dangerously-skip-permissions" not in argv, "never, on any lane"


# ---------------------------------------------------------------------------
# H1/H2 — the GRANT, which is not the argv.
#
# Every other row on this lane certifies what we SEND. jack-ryan's H1 is that the
# flags are not what the process receives: `~/.claude/settings.json` on this host
# carries `defaultMode: bypassPermissions`, which overrode everything, and in that
# mode `permission_denials` cannot fire — so the denial row above was asserting on
# a list that was structurally incapable of being non-empty. The `init` frame is
# the CLI reporting what it actually did, and it is the only evidence there is.
#
# Each row below isolates ONE of the four refusals. `check_grant` returning
# non-None is too weak an assertion — four mechanisms satisfy it — so every row
# asserts on what the message SAYS.
# ---------------------------------------------------------------------------
_GOOD_INIT = {"type": "system", "subtype": "init",
              "permissionMode": PINNED_PERMISSION_MODE, "tools": ["Read", "Bash"]}
_DECLARED = ["Read", "Bash(git status:*)"]


def test_H2_the_ambient_MCP_servers_are_refused_on_the_ARGV_too(h):
    """A SURVIVOR from the round-fourteen mutation set, and the H1 lesson repeating.

    Dropping `--strict-mcp-config` killed nothing: `check_grant` refuses MCP tools
    when they ARRIVE, so the detection was covered and the prevention was not. That
    is the same split H1 is about — the argv and the grant are two claims, and a row
    on one is not a row on the other. Detection alone means every agentic phase on a
    host with MCP servers configured fails at adjudication instead of running
    correctly, and a check that fires on every correct run gets removed.
    """
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read"]})
    assert "--strict-mcp-config" in argv, (
        "the ambient `~/.claude.json` MCP servers are loaded. Measured on this host: "
        "two `mcp__` tools were granted under an explicit `--allowedTools`, so the "
        "fence's contents varied by machine."
    )


def test_H1_a_matching_grant_is_accepted():
    """The control. Without it, every row below is satisfied by refusing always."""
    assert check_grant(_GOOD_INIT, _DECLARED) is None


def test_H1_a_mode_the_workflow_did_not_pin_is_refused():
    """The finding itself: the mode came from ambient settings, not from our argv."""
    frame = {**_GOOD_INIT, "permissionMode": "bypassPermissions"}
    error = check_grant(frame, _DECLARED) or ""
    assert "permission mode" in error and "bypassPermissions" in error, error
    assert "permission_denials" in error, (
        "the refusal should say WHY this mode is disqualifying — that the denial "
        "list cannot fire in it, so the fence reports silence rather than safety"
    )


def test_H1_a_MISSING_init_frame_is_refused_not_assumed_clean():
    """No evidence about the grant must not read as no problem."""
    error = check_grant(None, _DECLARED) or ""
    assert "no `init` frame" in error and "Absence of evidence is not a pass" in error, error


def test_H2_MCP_tools_nobody_declared_are_refused():
    """Measured on the live probe: two arrived under an explicit allowlist."""
    frame = {**_GOOD_INIT, "tools": ["Read", "Bash", "mcp__vercel__deploy"]}
    error = check_grant(frame, _DECLARED) or ""
    assert "MCP tool" in error and "mcp__vercel__deploy" in error, error


def test_H2_a_grant_WIDER_than_the_declaration_is_refused():
    frame = {**_GOOD_INIT, "tools": ["Read", "Bash", "Write"]}
    error = check_grant(frame, _DECLARED) or ""
    assert "granted but NOT declared: Write" in error, error


def test_H2_a_grant_NARROWER_than_the_declaration_is_refused():
    """The direction that is not a safety problem, and is still a defect.

    A phase holding less than it declared fails in a way that reads as the agent's
    fault. Refusing only the wide direction would leave that misattribution live.
    """
    frame = {**_GOOD_INIT, "tools": ["Read"]}
    error = check_grant(frame, _DECLARED) or ""
    assert "declared but NOT granted: Bash" in error, error


def test_H2_the_SCOPED_declaration_is_compared_by_BASE_NAME():
    """`Bash(git status:*)` is granted as `Bash`; comparing raw strings refuses always.

    This is the row that stops the adjudicator from being disabled the next time it
    fires on a correct workflow — a check that refuses everything gets removed.

    Gate-2 J1 called this "a row certifying the hole", and the charge is half right —
    which is the half worth writing down. The COMPARISON is correct and must stay:
    the init frame reports base names, so a raw-string comparison would refuse every
    scoped declaration and the adjudicator would be deleted within a week. What was
    wrong is what a reader could take from the green. Passing here means "the
    adjudicator did not false-positive." It does NOT mean the declared scope was
    honoured — measured 2026-08-11, `--allowedTools` does not restrict in headless
    `default` mode, so this declaration buys the full reach of `Bash`.

    So the row now asserts the second fact too, and can no longer be read as the
    stronger claim: the grant is accepted, AND `Bash` is what was actually granted.
    """
    declared = ["Read", "Bash(git status:*)"]
    assert check_grant({**_GOOD_INIT, "tools": ["Read", "Bash"]}, declared) is None
    # The scope bought nothing. If a future CLI starts enforcing `--allowedTools`,
    # THIS is the line that should be revisited — the declaration would then be
    # narrower than the grant, and `check_grant` treating them as equal would be
    # under-reporting rather than the accurate reading it is today.
    assert check_grant({**_GOOD_INIT, "tools": ["Read"]}, declared) is not None, (
        "a declaration of Bash(git status:*) against a grant WITHOUT Bash was "
        "accepted. The scope is not a fence, but the base name still is, and it is "
        "the only pre-hoc containment this lane has."
    )


def test_H3_the_WIRING_of_declared_tools_fails_CLOSED():
    """The H3 axis applied to this check: a call site that passes nothing.

    `declared_tools` defaults to None so that `adjudicate` can be called from the
    tests, and a default that compares against the empty set would make every
    declaration look like an over-grant — or, worse for a defaulted argument, be
    made to compare against nothing at all and pass. It fails closed and says the
    wiring is what failed, not the grant.
    """
    error = check_grant(_GOOD_INIT, None) or ""
    assert "no declared tool set reached the adjudicator" in error, error
    assert "WIRING" in error, error


def _fake_claude(tmp_path, granted, mode=PINNED_PERMISSION_MODE):
    """A `claude` that ignores its argv and reports a grant of our choosing.

    The point is the WIRING, so the stream has to come from a real subprocess that
    `run()` launched and parsed — not from a hand-built frame handed to
    `adjudicate`, which is the call `run()`'s wiring sits between.
    """
    import json
    import stat

    stream = "\n".join(
        json.dumps(f)
        for f in (
            {"type": "system", "subtype": "init", "permissionMode": mode, "tools": granted},
            {"type": "result", "subtype": "success", "is_error": False, "result": "done",
             "session_id": "s", "num_turns": 1, "permission_denials": [],
             "usage": {"input_tokens": 1, "output_tokens": 1}},
        )
    )
    path = tmp_path / "fake-claude"
    path.write_text(f"#!/bin/sh\ncat <<'JSONL'\n{stream}\nJSONL\n", encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return ClaudeCodeHarness(executable=str(path))


def test_H3_the_RUN_call_site_passes_the_ACTUAL_declared_tools(tmp_path):
    """The wiring row. `check_grant` failing closed is worth nothing unwired.

    Same shape as the post-gate call site that took no `agentic` argument while
    every row on the function stayed green — so this goes through `run()`, with a
    subprocess whose grant MATCHES. If `run()` stopped passing `declared_tools`,
    the adjudicator would see None and refuse for the WIRING reason, and this row
    would go red on a phase that did nothing wrong.
    """
    harness = _fake_claude(tmp_path, ["Read", "Bash"])
    result = harness.run("x", tmp_path, {"agent": "a", "tools": ["Read", "Bash(git status:*)"]})
    assert result.ok, f"a matching grant was refused through run(): {result.error!r}"
    assert result.extra.get("granted_tools") == ["Read", "Bash"], result.extra


def test_H3_the_RUN_call_site_passes_the_DECLARATION_and_not_a_placeholder(tmp_path):
    """The row above passes if `run()` hands over the GRANTED set instead.

    Comparing the grant against itself is the tightest-looking check that certifies
    nothing, and it is one plausible edit away. Here the declaration and the grant
    disagree, and the refusal has to name the declared tool BY NAME — which only
    the workflow's own list can supply.
    """
    harness = _fake_claude(tmp_path, ["Read"])
    result = harness.run("x", tmp_path, {"agent": "a", "tools": ["Read", "Write"]})
    assert not result.ok, "a phase granted less than it declared was passed"
    assert "declared but NOT granted: Write" in (result.error or ""), result.error


def test_H1_the_MODE_is_adjudicated_through_run_not_merely_sent(tmp_path):
    """The finding end to end: argv pins it, the host overrides it, the run stops."""
    harness = _fake_claude(tmp_path, ["Read"], mode="bypassPermissions")
    result = harness.run("x", tmp_path, {"agent": "a", "tools": ["Read"]})
    assert not result.ok, (
        "a phase that reported running in bypassPermissions was accepted. The argv "
        "pins the mode; only the init frame says whether the pin held."
    )
    assert "bypassPermissions" in (result.error or ""), result.error
    assert result.extra.get("permission_mode") == "bypassPermissions", result.extra
