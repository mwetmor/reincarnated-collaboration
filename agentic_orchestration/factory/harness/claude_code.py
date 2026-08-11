"""Claude Code headless adapter — the live lane.

Flag surface VERIFIED at claude 2.1.119 on this host (star-lord probe 2026-08-10,
Spec A § 13 item O1):

    claude --agent <seam> -p '<prompt>' --output-format stream-json --verbose

  * `--agent`, `-p`, `--output-format stream-json` co-support: CONFIRMED.
  * `--verbose` is REQUIRED alongside stream-json in print mode. Without it the
    CLI exits 1 with "When using --print, --output-format=stream-json requires
    --verbose" -- before any API call. We pass it unconditionally.
  * `--tools` and `--allowedTools` VERIFIED present (star-lord probe 2026-08-11,
    Gate-2 C3 — they shipped on this lane without ever appearing in the O1 list).
    `claude --help` states: `--tools <tools...>  Specify the list of available tools
    from the built-in set. Use "" to disable all tools, "default" to use all tools`.
    So OMITTING the flag is not a neutral default — it is the full built-in set,
    which is why an undeclared allowlist is now a LOAD error rather than a silent
    widening.
  * `--allowedTools` DOES NOT RESTRICT in headless `default` mode (Gate-2 J1;
    measured star-lord 2026-08-11, `/tmp/sl_probe/p1.jsonl`). Given
    `--tools Bash --allowedTools 'Bash(git status:*)'`, the model ran
    `echo SCOPE_ESCAPED` and the run returned `is_error=False`,
    `stop_reason=end_turn`, `permission_denials=[]`. In headless nothing prompts, so
    "may run without a prompt" is a distinction with no consequence here. `--tools`
    is the fence; the scope inside `--allowedTools` is decorative. It is still sent —
    it costs nothing and a future CLI may honour it — but NOTHING in this module may
    treat it as narrowing, and an empty `permission_denials` is therefore not
    evidence of anything. Pre-hoc containment on this lane is TOOL BASE NAMES ONLY;
    everything finer is post-hoc, through the fingerprint wall.
  * The `result` frame carries `usage` and `total_cost_usd` (O2, see usage.py).
  * SessionStart hooks DO fire in headless mode (hook_started/hook_response frames
    appear in the stream); they are recorded, not suppressed.

No `--model` is ever passed: model policy belongs to the launcher session, not to
a workflow file (Spec A § 9). No `--dangerously-skip-permissions`, ever.

Gate-2 H1/H2 — the flags are not the grant
------------------------------------------
"No `--dangerously-skip-permissions`, ever" is a claim about a FLAG, and the flag was
never the thing that mattered. Measured on this host with the exact argv above:

    INIT permissionMode: bypassPermissions
    INIT tools: ['Bash', 'Read', 'mcp__…authenticate', 'mcp__…complete_authentication']

`~/.claude/settings.json` carries `permissions.defaultMode: "bypassPermissions"`, so the
ambient config decided the mode and the argv never spoke. Two consequences, both of them
the shape this review keeps finding — the wrong answer is the safe-looking one:

  * `--allowedTools` (the "may run without a prompt" half) was decorative, because a
    mode that approves everything already approves everything;
  * `permission_denials` — the guard that turns a phase reaching outside its fence into
    EVIDENCE — could not fire at all. Its silence was structural, not a measurement.

And the two MCP tools were GRANTED under an explicit two-name allowlist: F4 excluded
`mcp__` names from the vocabulary for the right reason and drew the wrong conclusion,
because refusing to NAME them does not REMOVE them.

So the mode is pinned on the argv AND re-read off the `init` frame and asserted equal
(`PINNED_PERMISSION_MODE`); `--strict-mcp-config` removes the ambient MCP servers; and
the granted tool set is adjudicated against the declared one, because the init frame is
the only truth about what the process actually got.

One more measured fact, which is why the two flags no longer receive the same string:

    --tools 'Bash(git *),Read'   ->  INIT tools: ['Read']

`--tools` takes BASE names and silently discards what it does not recognise. That fails
closed, but a workflow declaring scoped Bash would have believed it had scoped Bash and
had NO Bash. Base names go to `--tools`; the full scoped forms go to `--allowedTools`,
which is the flag whose grammar accepts them.
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Any

from ..usage import UsageBreakdown
from .base import RawResult, register_harness

DEFAULT_TIMEOUT_S = 3600

#: The permission mode every agentic phase runs in, pinned on the argv and then
#: RE-READ off the `init` frame and asserted equal (Gate-2 H1). `default` is the mode
#: in which a tool outside the allowlist produces a denial rather than an approval —
#: which is what makes `permission_denials` a measurement instead of a silence.
PINNED_PERMISSION_MODE = "default"

#: The built-in tool set, read off the `init` frame of a live stream-json run on this
#: host (claude 2.1.119, star-lord probe 2026-08-11, Gate-2 F4). Not copied from
#: documentation and not guessed: the CLI enumerates its own tools, so that is the
#: source. Host-specific MCP tools appeared in the same frame and are deliberately
#: NOT here — their availability depends on local config, so a workflow naming one
#: would be declaring a fence whose contents vary by machine.
BUILTIN_TOOLS = frozenset({
    "Task", "AskUserQuestion", "Bash", "CronCreate", "CronDelete", "CronList", "Edit",
    "EnterPlanMode", "EnterWorktree", "ExitPlanMode", "ExitWorktree", "Glob", "Grep",
    "Monitor", "NotebookEdit", "PushNotification", "Read", "RemoteTrigger",
    "ScheduleWakeup", "Skill", "TaskOutput", "TaskStop", "TodoWrite", "ToolSearch",
    "WebFetch", "WebSearch", "Write",
})

#: Names this CLI speaks in `tool_use` frames that its GRANT channel does not speak.
#: Gate-2 JR-6 (jack-ryan, round 17), read off the preserved frames rather than off a
#: summary of them — which is how it was found, and how the error it corrects was made.
#:
#: `j7-task-reach-probe.jsonl` advertises `tools: ['Task']` in its init frame and
#: carries exactly one `tool_use`, whose name is `Agent`. Delegation therefore has TWO
#: names on claude 2.1.119: `Task` on the GRANT channel (`--tools`, the init frame,
#: `check_grant`) and `Agent` on the INVOCATION channel. The split is measured, not
#: assumed general — `j1-allowedtools-does-not-restrict.jsonl` grants `Bash` and
#: invokes `Bash`, so the two channels agree for that name, and this dict has exactly
#: one entry until a frame says otherwise.
#:
#: Two consequences, both live:
#:
#:   * `BUILTIN_TOOLS` is what ONE init frame enumerated, which is the grant vocabulary
#:     and nothing wider. Reading membership in it as "this CLI has that tool" is a
#:     one-way implication read backwards, and `Agent` is the counterexample — it was
#:     sitting in the evidence folder while the loader told its reader that this CLI
#:     does not have it. That is the false sentence rule 39 exists to forbid, produced
#:     by the fix for rule 39, one layer down.
#:   * nothing in this module reads `tool_use` names today — `check_grant` compares
#:     init-frame names to declared names, both grant-channel. If anything ever does,
#:     the two namespaces must be translated between and not compared.
INVOCATION_ONLY_TOOLS: dict[str, str] = {
    "Agent": (
        "is what `tool_use` frames call delegation on this CLI, while `--tools` and the "
        "init frame call the same thing `Task`. It is a real name this CLI speaks and "
        "it is not a name the grant channel accepts, so declaring it fences nothing"
    ),
}

#: Names whose GRANT IS NOT THEIR REACH. Gate-2 J7 (jack-ryan, round 16), MEASURED by
#: star-lord probe 2026-08-11; extended by JR-6 (round 17) to delegation's second name.
#:
#: `BUILTIN_TOOLS` answers "what does this CLI have?" — probed off a live init frame,
#: which is why it is trustworthy. It never answered "what does each one reach?", and
#: those are two questions. J1 established that after `--allowedTools` proved inert,
#: the base-name vocabulary is the agentic lane's ONLY pre-hoc fence. A fence whose
#: vocabulary contains a name that reaches past the fence is not a fence.
#:
#: The `Task` entry is not reasoned. Measured, argv identical to what `build_argv`
#: emits (`--tools Task --allowedTools Task --permission-mode default
#: --strict-mcp-config`):
#:
#:   * the parent's own init frame reported `tools: ['Task']` — the fence HELD for the
#:     parent, which is what makes this finding sharp rather than sloppy;
#:   * the parent delegated — the one `tool_use` frame in the run is named `Agent`, not
#:     `Task` (JR-6; this line used to say `Task`, and the frame beside it said
#:     otherwise); the child reported having `Bash, Glob, Grep, Read,
#:     Edit, Write, NotebookEdit, WebFetch, WebSearch, TodoWrite, BashOutput,
#:     KillShell, ExitPlanMode, Task, SlashCommand, Skill, AskUserQuestion, …`;
#:   * `is_error: False`, `permission_denials: []`.
#:
#: So a phase declaring `tools: ["Task"]` passes `validate_tools`, passes
#: `check_grant` (granted set == declared set, exactly), and runs `Bash`. The fence is
#: SATISFIED while being BYPASSED — J1's shape, arriving inside the mechanism that
#: replaced J1. The child's set is not even a subset of `BUILTIN_TOOLS` (`BashOutput`,
#: `KillShell`, `SlashCommand` are not names this vocabulary knows), so the child is
#: not fenced by this module at all.
#:
#: The rest are refused on the TIME axis, which no amount of hashing closes. The wall
#: is `fingerprint(before) -> execute -> fingerprint(after)`. Anything scheduled,
#: triggered or delegated to fire later fires after the after-fingerprint, in a window
#: the run has already reported on. F3's shape — a channel that structurally cannot
#: carry the counterexample — with time as the axis instead of path.
#:
#: These are REFUSED, not deleted from `BUILTIN_TOOLS`. Deleting them would make the
#: loader say "not a tool on this CLI", which is false, and would lose the measurement
#: that put them there (rule 13). The vocabulary stays honest; the fence gets smaller.
UNFENCEABLE_TOOLS: dict[str, str] = {
    "Task": (
        "delegates to a sub-agent whose grant is NOT this phase's grant. Measured "
        "2026-08-11: a run granted only `Task` produced a child holding Bash, Edit and "
        "Write, with no denial and no error. Declaring it satisfies the fence and "
        "bypasses it in the same call"
    ),
    "Agent": INVOCATION_ONLY_TOOLS["Agent"] + (
        ", and what it names is `Task`, which is refused above. Refused rather than "
        "left to the membership branch, whose message would say this CLI does not "
        "have it — the false sentence, about the one name the frames prove exists"
    ),
    "ToolSearch": (
        "exists to fetch schemas for DEFERRED tools and make them callable, which is "
        "the one documented mechanism whose whole purpose is to change the answer to "
        "'what can this phase call?' after the grant is fixed. REASONED, NOT MEASURED "
        "— and the failure to measure is itself recorded (JR-7): four probe framings "
        "were refused by the model's own safety classifier, while a control run with "
        "the same argv and an innocuous prompt returned cleanly, so the configuration "
        "is fine and the QUESTION is what could not be asked. Refused in the "
        "fail-closed direction, and this entry says which kind of entry it is"
    ),
    "EnterWorktree": (
        "creates a git worktree, which can land OUTSIDE every declared tree — and a "
        "write the fingerprint never covers is not a write this factory can report on"
    ),
    "CronCreate": (
        "schedules work that fires AFTER the after-fingerprint, in a window the run has "
        "already declared clean"
    ),
    "CronDelete": (
        "mutates host-level scheduled state that no fingerprint covers and no rollback "
        "can restore"
    ),
    "ScheduleWakeup": (
        "schedules a future turn, which is reach past the run's own time boundary"
    ),
    "RemoteTrigger": "reaches OFF this host entirely; nothing here can measure or undo it",
    "PushNotification": "reaches off-host; the effect outlives the run and is not recallable",
}

#: Names a reviewer has ASKED ABOUT and this fence nevertheless admits, each with the
#: reason it is admitted. Gate-2 JR-7 (jack-ryan, round 17).
#:
#: `UNFENCEABLE_TOOLS` answers "are these unfenceable?"; `validate_tools` spends the
#: answer as "the rest are fenceable". That is the series' own predicate shape sitting
#: on top of the J7 fix, and the honest response is not a bigger refusal list — it is a
#: record of which admissions were ADJUDICATED and which were merely never raised.
#: An admission with a reason can be argued with. An admission by silence cannot.
#:
#: This does not close the enumeration and does not claim to. It closes the QUESTIONS
#: ASKED SO FAR, which is a smaller and true claim.
REASONED_ADMISSIONS: dict[str, str] = {
    "Skill": (
        "injects a skill file's instructions into the conversation; it does not grant "
        "a tool. Its reach is the phase's own reach, and every tool a skill asks for "
        "still has to be in `--tools`. Distinct from `ToolSearch`, which changes the "
        "callable set rather than the instructions"
    ),
    "TaskOutput": (
        "reads the output of a background task that already exists. It cannot start "
        "one — `Task` is refused above, and without a creator this is inert"
    ),
    "TaskStop": (
        "stops a background task that already exists. Inert because `Task` is refused "
        "above and there is nothing to stop, and stopping is the fail-closed direction "
        "anyway"
    ),
    "ExitWorktree": (
        "leaves a worktree; it cannot create one. `EnterWorktree` is refused above, so "
        "a phase that cannot enter has nothing to exit"
    ),
}


def validate_tools(tools: object, where: str) -> list[str]:
    """Refuse an allowlist that does not restrict. Returns the validated list.

    Gate-2 C3 made an absent `tools` a refusal at both entry points. Gate-2 F4 showed
    that closed only the EMPTY case: the guard tested declaration, not restriction, so
    the exact state C3 exists to prevent — the full built-in set, chosen by nobody —
    was reachable by writing one word, `default`, and it read as diligence. A test for
    emptiness is not a test for restriction.

    So this is rule 13 applied to the allowlist: a CLOSED VOCABULARY. `default` is
    refused by name, a non-list is refused (YAML `tools: Read` is a string, and
    `list("Read")` is `['R','e','a','d']` — an allowlist of four tools that do not
    exist, which the CLI would accept and which restricts by accident), and a name
    nobody enumerated is refused rather than passed through. A default that admits
    every string is how this class recurs.

    Gate-2 J7 adds the second question. `BUILTIN_TOOLS` answers "does this CLI have
    that tool?"; it never answered "does the grant equal the reach?". `UNFENCEABLE_TOOLS`
    holds the measured and reasoned NOs, and they are refused BEFORE the membership
    check — because the membership message would say the one thing that is not true
    about them.

    That ordering was recorded as load-bearing in round 17 and was INERT (Gate-2 JR-8):
    every refused name was also a `BUILTIN_TOOLS` member, so the membership branch
    could not fire for one at any position, and jack-ryan's mutation moving the block
    below it survived a full green suite. The mechanism named was not the mechanism
    working — the subset invariant was. JR-6 makes it real: `Agent` is refused and is
    NOT a `BUILTIN_TOOLS` member, because `BUILTIN_TOOLS` is the grant vocabulary and
    `Agent` is an invocation name. Put the block second and `Agent` gets told this CLI
    does not have it, with the frames that disprove that sitting in the repo.

    Scoped forms are kept and the BASE name is what must be in the vocabulary. This
    used to read "`Bash(git *)` … is strictly narrower than `Bash`", which measured
    FALSE at the only place it is spent (Gate-2 J1): `--allowedTools` does not
    restrict in headless `default` mode, so a declaration of `Bash(git status:*)`
    buys exactly the reach of `Bash` and nothing less. The scope is retained as
    author INTENT — it says what the phase means to do, it reads well in a receipt,
    and a future CLI may enforce it — but it is not a fence and no caller may treat
    it as one.
    """
    if tools is None:
        raise ValueError(
            f"{where}: declares no `tools` allowlist. An agentic phase with no tool "
            "allowlist runs with the CLI's full default tool set, which is the one "
            "allowlist in this spine that would fail OPEN. Name the tools the phase "
            "needs."
        )
    if isinstance(tools, str) or not isinstance(tools, (list, tuple)):
        raise ValueError(
            f"{where}: `tools` must be a LIST of tool names, got {type(tools).__name__} "
            f"{tools!r}. A YAML scalar (`tools: Read`) becomes the characters of the "
            "word, which is an allowlist of four tools that do not exist — it restricts "
            "by accident and reads as a declaration."
        )
    names = [str(t) for t in tools]
    if not names:
        raise ValueError(
            f"{where}: `tools` is empty. With no --tools/--allowedTools the CLI runs "
            "its full default tool set, and this is the agentic lane's only pre-hoc "
            "containment."
        )
    for name in names:
        base = name.split("(", 1)[0].strip()
        if base == "default":
            raise ValueError(
                f"{where}: `tools` names 'default', which `claude --help` defines as "
                "\"use all tools\". That is the exact state this allowlist exists to "
                "prevent, reached by declaring it — a fence naming everything. Name the "
                "tools the phase needs."
            )
        if base.startswith("mcp__"):
            raise ValueError(
                f"{where}: `tools` names the MCP tool {name!r}. MCP availability depends "
                "on local config, so this fence would mean different things on different "
                "machines. Not admitted to the vocabulary."
            )
        if base in UNFENCEABLE_TOOLS:
            raise ValueError(
                f"{where}: `tools` names {name!r}, which this CLI HAS but which this "
                f"fence cannot hold: it {UNFENCEABLE_TOOLS[base]}. Declaring it would "
                "produce a run whose granted set equals its declared set and whose "
                "reach exceeds both — the fence satisfied and bypassed in one call. "
                "Refused at load, where the refusal is cheap, rather than adjudicated "
                "after the fact, where there is nothing left to adjudicate."
            )
        if base not in BUILTIN_TOOLS:
            raise ValueError(
                f"{where}: `tools` names {name!r}, which is not in the built-in set "
                f"probed from this CLI. Known: {', '.join(sorted(BUILTIN_TOOLS))}. If the "
                "CLI has gained a tool, re-probe the init frame and extend BUILTIN_TOOLS "
                "deliberately — an allowlist that passes through unknown strings is not "
                "closed."
            )
    return names


class ClaudeCodeHarness:
    name = "claude_code"

    #: Published on the ADAPTER so the loader can validate a phase's allowlist without
    #: owning an opinion about what a tool name is (Gate-2 F4). The loader refuses any
    #: harness that does not publish it — otherwise a second lane would be a way around
    #: the vocabulary, which is how this class recurs.
    validate_tools = staticmethod(validate_tools)

    def __init__(self, executable: str = "claude"):
        self.executable = executable

    # -- argv ---------------------------------------------------------------
    def build_argv(self, prompt: str, config: dict[str, Any]) -> list[str]:
        agent = config.get("agent")
        if not agent:
            raise ValueError("claude_code harness requires a named seam `agent`")
        if "model" in config:
            raise ValueError(
                "workflow phases must not pin a `model` -- model policy belongs to the "
                "launcher session (Spec A § 9)"
            )
        argv = [
            self.executable,
            "--agent",
            str(agent),
            "-p",
            prompt,
            "--output-format",
            "stream-json",
            "--verbose",
        ]
        # Gate-2 C3, second half. The loader refuses this at LOAD, but the adapter is
        # callable directly and a guard that exists in only one of two entry points is
        # a guard with a route around it — which is L8's finding, at the harness layer.
        # Fail closed at both, and against the same vocabulary (F4).
        tools = validate_tools(config.get("tools"), "claude_code harness")
        # H2: different grammars. `--tools` takes BASE names and silently DROPS what it
        # does not recognise (measured: `--tools 'Bash(git *),Read'` grants only Read),
        # so sending it a scoped form is how a phase ends up with less than it declared
        # and no error. `--allowedTools` is the flag that accepts the scoped form, and
        # the scoped form is strictly narrower, so it belongs there.
        argv += ["--tools", ",".join(sorted({t.split("(", 1)[0].strip() for t in tools}))]
        argv += ["--allowedTools", ",".join(tools)]
        # H1: the mode is a GRANT, and until it is pinned the ambient config decides it.
        argv += ["--permission-mode", PINNED_PERMISSION_MODE]
        # H2: the ambient MCP servers are granted even under an explicit allowlist.
        argv += ["--strict-mcp-config"]
        for extra_dir in config.get("add_dirs", []) or []:
            argv += ["--add-dir", str(extra_dir)]
        return argv

    # -- run ----------------------------------------------------------------
    def run(self, prompt: str, cwd: Path, config: dict[str, Any]) -> RawResult:
        raw_path = config.get("raw_output_path")
        timeout_s = int(config.get("timeout_s", DEFAULT_TIMEOUT_S))
        try:
            argv = self.build_argv(prompt, config)
        except ValueError as exc:
            return RawResult(ok=False, harness=self.name, error=str(exc))

        started = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=timeout_s,
                stdin=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            return RawResult(
                ok=False,
                harness=self.name,
                error=f"{self.executable} not found on PATH",
                usage=UsageBreakdown.absent("harness never launched"),
            )
        except subprocess.TimeoutExpired:
            return RawResult(
                ok=False,
                harness=self.name,
                error=f"claude headless exceeded {timeout_s}s and was killed",
                usage=UsageBreakdown.absent("harness killed on timeout; no result frame"),
            )
        elapsed_ms = int((time.monotonic() - started) * 1000)

        if raw_path:
            Path(raw_path).parent.mkdir(parents=True, exist_ok=True)
            Path(raw_path).write_text(proc.stdout, encoding="utf-8")
            if proc.stderr.strip():
                Path(str(raw_path) + ".stderr").write_text(proc.stderr, encoding="utf-8")

        frames = parse_frames(proc.stdout)
        result_frame = next((f for f in reversed(frames) if f.get("type") == "result"), None)
        init_frame = next((f for f in frames if f.get("subtype") == "init"), None)

        if result_frame is None:
            return RawResult(
                ok=False,
                harness=self.name,
                exit_code=proc.returncode,
                raw_output_path=raw_path,
                error=(
                    f"no result frame in stream (exit {proc.returncode}): "
                    f"{proc.stderr.strip()[:300] or 'no stderr'}"
                ),
                usage=UsageBreakdown.absent("stream carried no result frame"),
                extra={"elapsed_ms": elapsed_ms, "frame_count": len(frames)},
            )

        return self.adjudicate(
            result_frame, init_frame, proc.returncode, elapsed_ms, raw_path, len(frames),
            declared_tools=validate_tools(config.get("tools"), "claude_code harness"),
        )

    # -- adjudication -------------------------------------------------------
    def adjudicate(
        self,
        result_frame: dict[str, Any],
        init_frame: dict[str, Any] | None,
        returncode: int,
        elapsed_ms: int,
        raw_path: str | None = None,
        frame_count: int = 0,
        declared_tools: list[str] | None = None,
    ) -> RawResult:
        """Turn a result frame into a verdict. Separated from `run` so it is TESTABLE.

        Gate-2 C3: this logic lived inside `run()` behind a live subprocess, so the
        only way to exercise it was to invoke a model — which meant nothing exercised
        it, on the lane under review. A verdict that can only be checked by spending
        money is a verdict nobody checks.
        """
        usage = UsageBreakdown.from_claude_result_frame(result_frame)
        is_error = bool(result_frame.get("is_error")) or returncode != 0
        # `permission_denials` was recorded into `extra` and adjudicated by nothing,
        # so a phase that spent its turns being refused tools returned ok=True with a
        # cheerful result string. A denial is the pre-hoc analogue of a breach: the
        # phase asked for something its allowlist forbids. This spine's rule for a
        # breach is that it is evidence, never noise and never a retry — so it fails
        # the phase and says how many. If live data later shows benign probing is
        # common this is weakened ON EVIDENCE, the way the COARSE caveat is; it is
        # not weakened because it is inconvenient.
        # H1/H2: adjudicated BEFORE the denial check, because the denial check's
        # meaning depends on it — in `bypassPermissions` an empty `permission_denials`
        # is not a clean phase, it is a fence that was never enforced. A guard whose
        # silence is produced by the condition above it has to be ordered under it.
        grant_error = check_grant(init_frame, declared_tools)
        if grant_error:
            is_error = True
        denials = result_frame.get("permission_denials") or []
        denial_error = None
        if denials:
            denial_error = (
                f"{len(denials)} tool call(s) were denied by the phase's allowlist. "
                "A phase reaching outside its declared tools is evidence, not noise — "
                f"first denial: {str(denials[0])[:200]}"
            )
            is_error = True
        return RawResult(
            ok=not is_error,
            text=result_frame.get("result") or "",
            usage=usage,
            harness=self.name,
            harness_session_id=result_frame.get("session_id"),
            model=(init_frame or {}).get("model")
            or next(iter(result_frame.get("modelUsage", {}) or {}), None),
            exit_code=returncode,
            raw_output_path=raw_path,
            error=(
                None if not is_error
                else grant_error
                or denial_error
                or str(result_frame.get("api_error_status") or "is_error")
            ),
            extra={
                "elapsed_ms": elapsed_ms,
                "num_turns": result_frame.get("num_turns"),
                "stop_reason": result_frame.get("stop_reason"),
                "permission_denials": result_frame.get("permission_denials"),
                "permission_mode": (init_frame or {}).get("permissionMode"),
                "granted_tools": (init_frame or {}).get("tools"),
                "frame_count": frame_count,
            },
        )


def check_grant(
    init_frame: dict[str, Any] | None, declared_tools: list[str] | None
) -> str | None:
    """Adjudicate what the process was GRANTED against what the workflow DECLARED.

    Gate-2 H1/H2. Everything else on this lane certifies the argv — the flags we send.
    The `init` frame is the CLI reporting what it actually did with them, and on this
    host those two disagreed in three ways at once: the mode came from
    `~/.claude/settings.json` rather than from us, two MCP tools arrived that no
    allowlist named, and a scoped form sent to `--tools` was dropped on the floor.

    Returns an error string, or None. Fails CLOSED on a missing frame: with no init
    frame there is no evidence about the grant, and "no evidence" must not read as
    "no problem" — that is the exact substitution this review exists to refuse.
    """
    if declared_tools is None:
        return (
            "no declared tool set reached the adjudicator, so the grant cannot be "
            "compared to anything. This is the WIRING failing rather than the check: "
            "H3's finding was a gate disarmed at its call site with every row still "
            "green, so this argument fails closed rather than defaulting to a "
            "comparison against the empty set."
        )
    if init_frame is None:
        return (
            "the stream carried no `init` frame, so what this process was GRANTED — its "
            "permission mode and its tool set — cannot be established. The phase may "
            "have run wide open. Absence of evidence is not a pass."
        )
    mode = init_frame.get("permissionMode")
    if mode != PINNED_PERMISSION_MODE:
        return (
            f"the phase ran in permission mode {mode!r}, not the pinned "
            f"{PINNED_PERMISSION_MODE!r}. The argv pins it, so a disagreement means "
            "something outside this workflow — ambient settings, a hook, a newer CLI "
            "honouring the flag differently — decided how this process was allowed to "
            "act. In `bypassPermissions` in particular, `permission_denials` cannot "
            "fire, so the phase's fence would be reporting silence rather than safety."
        )
    granted = set(init_frame.get("tools") or [])
    mcp = sorted(t for t in granted if t.startswith("mcp__"))
    if mcp:
        return (
            f"the phase was granted {len(mcp)} MCP tool(s) that no allowlist named: "
            f"{', '.join(mcp)}. MCP availability is per-machine, so this fence's "
            "contents would vary by host. `--strict-mcp-config` is passed to prevent "
            "exactly this; its presence on the argv is evidently not sufficient here."
        )
    expected = {t.split("(", 1)[0].strip() for t in declared_tools}
    extra = sorted(granted - expected)
    missing = sorted(expected - granted)
    if extra or missing:
        return (
            "the granted tool set is not the declared one"
            + (f"; granted but NOT declared: {', '.join(extra)}" if extra else "")
            + (f"; declared but NOT granted: {', '.join(missing)}" if missing else "")
            + ". The declared set is the fence; a process holding more than it has "
            "reaches further than the workflow says it can, and one holding less will "
            "fail in a way that looks like the agent's fault."
        )
    return None


def parse_frames(stdout: str) -> list[dict[str, Any]]:
    """Parse stream-json output. Unparseable lines are skipped, not guessed at."""
    frames: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            frames.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return frames


HARNESS = register_harness(ClaudeCodeHarness())
