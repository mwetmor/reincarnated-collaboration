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
    widening. Both flags are passed; `--tools` selects what exists, `--allowedTools`
    selects what may run without a prompt, and neither substitutes for the other.
  * The `result` frame carries `usage` and `total_cost_usd` (O2, see usage.py).
  * SessionStart hooks DO fire in headless mode (hook_started/hook_response frames
    appear in the stream); they are recorded, not suppressed.

No `--model` is ever passed: model policy belongs to the launcher session, not to
a workflow file (Spec A § 9). No `--dangerously-skip-permissions`, ever.
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


class ClaudeCodeHarness:
    name = "claude_code"

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
        tools = config.get("tools")
        if not tools:
            # Gate-2 C3, second half. The loader refuses this at LOAD, but the
            # adapter is callable directly and a guard that exists in only one of
            # two entry points is a guard with a route around it — which is L8's
            # finding, at the harness layer. Fail closed at both.
            raise ValueError(
                "claude_code harness requires a non-empty `tools` allowlist: with no "
                "--tools/--allowedTools the CLI runs its full default tool set, and "
                "this is the agentic lane's only pre-hoc containment"
            )
        argv += ["--tools", ",".join(tools)]
        argv += ["--allowedTools", ",".join(tools)]
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
            result_frame, init_frame, proc.returncode, elapsed_ms, raw_path, len(frames)
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
                else denial_error
                or str(result_frame.get("api_error_status") or "is_error")
            ),
            extra={
                "elapsed_ms": elapsed_ms,
                "num_turns": result_frame.get("num_turns"),
                "stop_reason": result_frame.get("stop_reason"),
                "permission_denials": result_frame.get("permission_denials"),
                "frame_count": frame_count,
            },
        )


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
