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
from factory.harness.claude_code import ClaudeCodeHarness, parse_frames
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
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read", "Bash"]})
    joined = " ".join(argv)
    assert "--dangerously-skip-permissions" not in joined
    assert "--permission-mode" not in joined


def test_the_tool_allowlist_reaches_both_flags(h):
    argv = h.build_argv("x", {"agent": "a", "tools": ["Read", "Grep"]})
    assert argv[argv.index("--tools") + 1] == "Read,Grep"
    assert argv[argv.index("--allowedTools") + 1] == "Read,Grep"


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
    ok_frame = {**frame, "permission_denials": []}
    assert ClaudeCodeHarness().adjudicate(ok_frame, None, 0, 1).ok, "a clean phase must still pass"
    denied = ClaudeCodeHarness().adjudicate(frame, None, 0, 1)
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
    assert argv[argv.index("--tools") + 1] == "Read,Grep"
    assert argv[argv.index("--allowedTools") + 1] == "Read,Grep"
    assert "--dangerously-skip-permissions" not in argv, "never, on any lane"
