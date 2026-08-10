"""Claude Code headless adapter — the live lane.

Flag surface VERIFIED at claude 2.1.119 on this host (star-lord probe 2026-08-10,
Spec A § 13 item O1):

    claude --agent <seam> -p '<prompt>' --output-format stream-json --verbose

  * `--agent`, `-p`, `--output-format stream-json` co-support: CONFIRMED.
  * `--verbose` is REQUIRED alongside stream-json in print mode. Without it the
    CLI exits 1 with "When using --print, --output-format=stream-json requires
    --verbose" -- before any API call. We pass it unconditionally.
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
        if tools:
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

        usage = UsageBreakdown.from_claude_result_frame(result_frame)
        is_error = bool(result_frame.get("is_error")) or proc.returncode != 0
        return RawResult(
            ok=not is_error,
            text=result_frame.get("result") or "",
            usage=usage,
            harness=self.name,
            harness_session_id=result_frame.get("session_id"),
            model=(init_frame or {}).get("model")
            or next(iter(result_frame.get("modelUsage", {}) or {}), None),
            exit_code=proc.returncode,
            raw_output_path=raw_path,
            error=None if not is_error else str(result_frame.get("api_error_status") or "is_error"),
            extra={
                "elapsed_ms": elapsed_ms,
                "num_turns": result_frame.get("num_turns"),
                "stop_reason": result_frame.get("stop_reason"),
                "permission_denials": result_frame.get("permission_denials"),
                "frame_count": len(frames),
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
