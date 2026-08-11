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
from factory.harness.codex import BLOCKED_ON, HONEST_STUB, CodexHarness

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
# the registry and the honest stub
# ---------------------------------------------------------------------------
def test_both_lanes_are_registered():
    assert set(available_harnesses()) == {"claude_code", "codex"}


def test_an_unknown_harness_name_raises_at_lookup():
    with pytest.raises(KeyError, match="no harness registered"):
        get_harness("telepathy")


def test_the_codex_lane_declares_itself_closed():
    assert HONEST_STUB is True
    assert "T16" in BLOCKED_ON
    assert CodexHarness().available() is False


def test_the_codex_lane_raises_rather_than_returning_a_result(tmp_path):
    with pytest.raises(NotImplementedError, match="T16"):
        CodexHarness().run("x", tmp_path, {"agent": "a"})


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
    """
    assert check_grant({**_GOOD_INIT, "tools": ["Read", "Bash"]}, ["Read", "Bash(git status:*)"]) is None


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
