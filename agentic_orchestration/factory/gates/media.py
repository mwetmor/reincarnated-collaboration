"""ffprobe_verifies — R-BR-56 compiled: promote no render unverified.

The law (BR-2, Addendum 23): a re-render writes to a TEMPORARY name and is
promoted to the deliverable name only after ffprobe verifies duration and stream
inventory. This gate is the verification half. The promotion half is a separate
phase in the workflow (`command_succeeds`), so that the promotion write passes
through permissions fingerprinting like any other write -- a gate that mutated
the tree would slip its own writes past the fingerprint.

The gate is PURE: it reads, it reports, it changes nothing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

from .base import GateReport, RunContext, gate


def _ffprobe(path: str, timeout_s: int) -> dict[str, Any]:
    proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            path,
        ],
        capture_output=True,
        text=True,
        timeout=timeout_s,
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe exited {proc.returncode}: {proc.stderr.strip()[:400]}")
    return json.loads(proc.stdout)


@gate("ffprobe_verifies")
def ffprobe_verifies(
    envelope: Any,
    run: RunContext,
    path: str | None = None,
    min_duration_s: float | None = None,
    max_duration_s: float | None = None,
    expect_streams: list[str] | None = None,
    min_width: int | None = None,
    min_height: int | None = None,
    timeout_s: int = 120,
) -> GateReport:
    """Verify a render's duration and stream inventory before anyone promotes it."""
    if not path:
        return GateReport.not_runnable("ffprobe_verifies", "no `path` argument supplied")
    if shutil.which("ffprobe") is None:
        return GateReport.not_runnable(
            "ffprobe_verifies",
            "ffprobe is not installed on this host -- the render is UNVERIFIED, which is red, "
            "not green",
        )
    resolved = run.resolve(path)
    if not resolved.exists():
        return GateReport.failed(
            "ffprobe_verifies", f"render does not exist: {resolved}", path=str(resolved)
        )

    try:
        probe = _ffprobe(str(resolved), timeout_s)
    except subprocess.TimeoutExpired:
        return GateReport.not_runnable(
            "ffprobe_verifies", f"ffprobe exceeded {timeout_s}s on {resolved}"
        )
    except (RuntimeError, json.JSONDecodeError) as exc:
        return GateReport.failed(
            "ffprobe_verifies",
            f"ffprobe could not read {resolved.name} as media: {exc}",
            path=str(resolved),
        )

    fmt = probe.get("format", {})
    streams = probe.get("streams", [])
    inventory = [s.get("codec_type") for s in streams]
    try:
        duration = float(fmt.get("duration"))
    except (TypeError, ValueError):
        duration = None

    evidence: dict[str, Any] = {
        "path": str(resolved),
        "duration_s": duration,
        "stream_inventory": inventory,
        "size_bytes": resolved.stat().st_size,
        "format_name": fmt.get("format_name"),
    }

    problems: list[str] = []
    if duration is None:
        problems.append("no duration reported by ffprobe")
    else:
        if min_duration_s is not None and duration < min_duration_s:
            problems.append(f"duration {duration:.2f}s < required {min_duration_s}s")
        if max_duration_s is not None and duration > max_duration_s:
            problems.append(f"duration {duration:.2f}s > allowed {max_duration_s}s")

    for wanted in expect_streams or []:
        if wanted not in inventory:
            problems.append(f"expected a {wanted} stream; inventory is {inventory}")

    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if video is not None:
        evidence["width"] = video.get("width")
        evidence["height"] = video.get("height")
        evidence["video_codec"] = video.get("codec_name")
        evidence["nb_frames"] = video.get("nb_frames")
        if min_width is not None and (video.get("width") or 0) < min_width:
            problems.append(f"width {video.get('width')} < required {min_width}")
        if min_height is not None and (video.get("height") or 0) < min_height:
            problems.append(f"height {video.get('height')} < required {min_height}")
    elif min_width is not None or min_height is not None:
        problems.append("dimension check requested but the file carries no video stream")

    if problems:
        return GateReport.failed(
            "ffprobe_verifies",
            f"{resolved.name} is NOT promotable: " + "; ".join(problems),
            problems=problems,
            **evidence,
        )
    summary = f"{resolved.name} verified"
    if duration is not None:
        summary += f": {duration:.2f}s"
    summary += f", streams {inventory}"
    return GateReport.passed("ffprobe_verifies", summary, **evidence)
