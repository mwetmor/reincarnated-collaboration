"""Falsification tests — every registered gate must RED when its subject is broken.

Spec A § 11 acceptance 3 lives next door (`test_no_stub_gates.py`); this file
enforces the harder companion law, taken from KC2 practice: **strip the thing the
gate checks and the gate must come back red.** A gate that greens on a broken
substrate is worse than no gate, because it launders the substrate.

`test_every_registered_gate_has_a_falsification_case` asserts registry coverage,
so a NEW gate cannot land without a falsification pair. That is the mechanism
that keeps this file honest as the gate set grows.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from factory.envelope import EnvelopeBase
from factory.gates import GateReport, RunContext, available_gates, run_gate

FALSIFIED: set[str] = set()


def _ctx(tmp_path: Path, **kw) -> RunContext:
    return RunContext(
        run_id="test", root=tmp_path, session_dir=tmp_path / "session", **kw
    )


def _env(status: str = "PASS", artifacts: list[str] | None = None) -> EnvelopeBase:
    return EnvelopeBase(
        status=status, summary="under test", artifacts=artifacts or [], notes_for_next_agent=""
    )


def _record(name: str) -> None:
    FALSIFIED.add(name)


# ---------------------------------------------------------------------------
# artifacts_exist
# ---------------------------------------------------------------------------
def test_artifacts_exist(tmp_path: Path):
    (tmp_path / "made.txt").write_text("bytes")
    green = run_gate("artifacts_exist", _env(artifacts=["made.txt"]), _ctx(tmp_path))
    assert green.is_green, green.detail

    broken = run_gate("artifacts_exist", _env(artifacts=["never_written.txt"]), _ctx(tmp_path))
    assert not broken.is_green
    assert broken.evidence["missing"] == ["never_written.txt"]
    _record("artifacts_exist")


def test_artifacts_exist_with_no_claims_is_not_runnable(tmp_path: Path):
    """An empty claim list is not a free pass -- it is a gate that could not run."""
    report = run_gate("artifacts_exist", _env(artifacts=[]), _ctx(tmp_path))
    assert report.status == "NOT_RUNNABLE"
    assert not report.is_green


# ---------------------------------------------------------------------------
# files_non_empty
# ---------------------------------------------------------------------------
def test_files_non_empty(tmp_path: Path):
    (tmp_path / "full.txt").write_text("bytes")
    green = run_gate("files_non_empty", _env(artifacts=["full.txt"]), _ctx(tmp_path))
    assert green.is_green, green.detail

    (tmp_path / "hollow.txt").write_text("")
    broken = run_gate("files_non_empty", _env(artifacts=["hollow.txt"]), _ctx(tmp_path))
    assert not broken.is_green
    assert broken.evidence["empty"] == ["hollow.txt"]
    _record("files_non_empty")


# ---------------------------------------------------------------------------
# json_parses
# ---------------------------------------------------------------------------
def test_json_parses(tmp_path: Path):
    (tmp_path / "good.json").write_text(json.dumps({"a": 1}))
    green = run_gate("json_parses", _env(artifacts=["good.json"]), _ctx(tmp_path))
    assert green.is_green, green.detail

    (tmp_path / "bad.json").write_text('{"a": 1,,}')
    broken = run_gate("json_parses", _env(artifacts=["bad.json"]), _ctx(tmp_path))
    assert not broken.is_green
    assert "bad.json" in broken.evidence["broken"]
    _record("json_parses")


def test_json_parses_reads_jsonl_line_by_line(tmp_path: Path):
    (tmp_path / "log.jsonl").write_text('{"a":1}\n{"b":2}\n')
    assert run_gate("json_parses", _env(artifacts=["log.jsonl"]), _ctx(tmp_path)).is_green
    (tmp_path / "torn.jsonl").write_text('{"a":1}\nnot json\n')
    assert not run_gate("json_parses", _env(artifacts=["torn.jsonl"]), _ctx(tmp_path)).is_green


# ---------------------------------------------------------------------------
# diff_matches_claims
# ---------------------------------------------------------------------------
def test_diff_matches_claims(tmp_path: Path):
    green = run_gate(
        "diff_matches_claims",
        _env(artifacts=["a.txt", "b.txt"]),
        _ctx(tmp_path, changed_paths=["a.txt"]),
    )
    assert green.is_green, green.detail

    broken = run_gate(
        "diff_matches_claims",
        _env(artifacts=["a.txt"]),
        _ctx(tmp_path, changed_paths=["a.txt", "somebody_elses_file.py"]),
    )
    assert not broken.is_green
    assert broken.evidence["unclaimed"] == ["somebody_elses_file.py"]
    _record("diff_matches_claims")


# ---------------------------------------------------------------------------
# verdict_consistent
# ---------------------------------------------------------------------------
def test_verdict_consistent(tmp_path: Path):
    green_prior = [GateReport.passed("artifacts_exist", "fine")]
    green = run_gate(
        "verdict_consistent", _env("PASS"), _ctx(tmp_path, prior_reports=green_prior)
    )
    assert green.is_green, green.detail

    red_prior = [GateReport.failed("files_non_empty", "zero-byte deliverable")]
    broken = run_gate(
        "verdict_consistent", _env("PASS"), _ctx(tmp_path, prior_reports=red_prior)
    )
    assert not broken.is_green
    assert "files_non_empty" in broken.detail
    _record("verdict_consistent")


def test_verdict_consistent_treats_not_runnable_as_red(tmp_path: Path):
    prior = [GateReport.not_runnable("ffprobe_verifies", "ffprobe missing")]
    report = run_gate("verdict_consistent", _env("PASS"), _ctx(tmp_path, prior_reports=prior))
    assert not report.is_green, "NOT_RUNNABLE must not be launderable into a PASS"


def test_verdict_consistent_accepts_an_honest_fail(tmp_path: Path):
    report = run_gate("verdict_consistent", _env("FAIL"), _ctx(tmp_path, prior_reports=[]))
    assert report.is_green, "a self-declared FAIL with no contradicting gate is consistent"


# ---------------------------------------------------------------------------
# tests_pass / command_succeeds  (the exec primitive, two intents)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("gate_name", ["tests_pass", "command_succeeds"])
def test_exec_gates(tmp_path: Path, gate_name: str):
    green = run_gate(
        gate_name, _env(), _ctx(tmp_path), command="python3 -c pass", cwd=str(tmp_path)
    )
    assert green.is_green, green.detail

    broken = run_gate(
        gate_name,
        _env(),
        _ctx(tmp_path),
        command='python3 -c "raise SystemExit(1)"',
        cwd=str(tmp_path),
    )
    assert not broken.is_green
    assert broken.evidence["exit_code"] == 1
    _record(gate_name)


def test_passing_output_does_not_travel(tmp_path: Path):
    """Only-failures-travel: a green run must not carry its stdout into evidence.

    The sentinel is printed BY the script, never named in the command line --
    the command itself is retained as metadata on purpose, and a sentinel hiding
    in the argv would prove nothing about the output.
    """
    script = tmp_path / "chatty.py"
    script.write_text("print('SECRET' + '-PASSING-CHATTER')\n" * 10)
    report = run_gate(
        "tests_pass",
        _env(),
        _ctx(tmp_path),
        command=f"python3 {script}",
        cwd=str(tmp_path),
    )
    assert report.is_green
    assert "SECRET-PASSING-CHATTER" not in json.dumps(report.evidence)
    assert report.evidence["stdout_lines"] == 10, "the output's shape is kept, not its text"


def test_failing_output_does_travel(tmp_path: Path):
    report = run_gate(
        "tests_pass",
        _env(),
        _ctx(tmp_path),
        command='python3 -c "import sys; print(\'FAILED test_x\'); sys.exit(2)"',
        cwd=str(tmp_path),
    )
    assert not report.is_green
    assert any("FAILED test_x" in line for line in report.evidence["failures"])


def test_missing_command_is_not_runnable(tmp_path: Path):
    report = run_gate("tests_pass", _env(), _ctx(tmp_path), command="definitely-not-a-binary-xyz")
    assert report.status == "NOT_RUNNABLE"
    assert not report.is_green


# ---------------------------------------------------------------------------
# sha256_matches
# ---------------------------------------------------------------------------
def test_sha256_matches(tmp_path: Path):
    target = tmp_path / "pinned.json"
    target.write_text('{"pinned": true}')
    import hashlib

    digest = hashlib.sha256(target.read_bytes()).hexdigest()

    green = run_gate(
        "sha256_matches", _env(), _ctx(tmp_path), path="pinned.json", expected=digest,
        size_bytes=target.stat().st_size,
    )
    assert green.is_green, green.detail

    target.write_text('{"pinned": false}')  # the supply moved under the consumer
    broken = run_gate(
        "sha256_matches", _env(), _ctx(tmp_path), path="pinned.json", expected=digest
    )
    assert not broken.is_green
    assert broken.evidence["actual"] != digest
    _record("sha256_matches")


def test_sha256_size_cross_check_can_red_on_its_own(tmp_path: Path):
    target = tmp_path / "pinned.bin"
    target.write_bytes(b"abc")
    import hashlib

    digest = hashlib.sha256(b"abc").hexdigest()
    report = run_gate(
        "sha256_matches", _env(), _ctx(tmp_path), path="pinned.bin", expected=digest,
        size_bytes=999,
    )
    assert not report.is_green


def test_sha256_without_a_pin_is_not_runnable(tmp_path: Path):
    report = run_gate("sha256_matches", _env(), _ctx(tmp_path), path="x")
    assert report.status == "NOT_RUNNABLE"


# ---------------------------------------------------------------------------
# ffprobe_verifies
# ---------------------------------------------------------------------------
def _synthesize_clip(path: Path, seconds: float = 1.0) -> bool:
    if shutil.which("ffmpeg") is None:
        return False
    proc = subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c=black:s=1280x720:d={seconds}",
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono:d={seconds}",
            "-shortest", "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0 and path.exists()


def test_ffprobe_verifies(tmp_path: Path):
    clip = tmp_path / "render.mp4"
    if not _synthesize_clip(clip, seconds=1.0):
        pytest.skip("ffmpeg unavailable on this host — green case NAMED-ABSENT, not assumed")

    green = run_gate(
        "ffprobe_verifies", _env(), _ctx(tmp_path), path="render.mp4",
        min_duration_s=0.5, expect_streams=["video", "audio"], min_width=1280, min_height=720,
    )
    assert green.is_green, green.detail

    # Falsification 1: the render is too short to be the deliverable.
    short = run_gate(
        "ffprobe_verifies", _env(), _ctx(tmp_path), path="render.mp4", min_duration_s=60,
    )
    assert not short.is_green
    assert "duration" in short.detail

    # Falsification 2: a stream the render does not carry.
    missing_stream = run_gate(
        "ffprobe_verifies", _env(), _ctx(tmp_path), path="render.mp4",
        expect_streams=["subtitle"],
    )
    assert not missing_stream.is_green
    _record("ffprobe_verifies")


def test_ffprobe_reds_on_a_file_that_is_not_media(tmp_path: Path):
    fake = tmp_path / "not_really.mp4"
    fake.write_text("this is a text file wearing an mp4 extension")
    report = run_gate("ffprobe_verifies", _env(), _ctx(tmp_path), path="not_really.mp4")
    assert not report.is_green
    _record("ffprobe_verifies")


# ---------------------------------------------------------------------------
# registry coverage — the mechanism that keeps this file honest
# ---------------------------------------------------------------------------
def test_every_registered_gate_has_a_falsification_case():
    registered = set(available_gates())
    uncovered = registered - FALSIFIED
    assert not uncovered, (
        f"gate(s) with no falsification test: {sorted(uncovered)}. "
        "Every gate must be shown to red when its subject is broken."
    )


def test_unknown_gate_name_is_red_not_silent(tmp_path: Path):
    report = run_gate("gate_that_does_not_exist", _env(), _ctx(tmp_path))
    assert report.status == "NOT_RUNNABLE"
    assert not report.is_green


def test_a_gate_that_raises_is_red(tmp_path: Path, monkeypatch):
    """There is no path from an exception to a green verdict."""
    from factory.gates import base

    def explode(envelope, run, **kw):
        raise RuntimeError("gate internals fell over")

    monkeypatch.setitem(base._REGISTRY, "exploding_gate", explode)
    report = run_gate("exploding_gate", _env(), _ctx(tmp_path))
    assert report.status == "NOT_RUNNABLE"
    assert "gate internals fell over" in report.detail
