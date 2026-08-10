"""Token accounting — Spec A § 6, and the two standing rules it enforces.

Rule 1: reasoning tokens are a SHARE of output, never a fifth addend.
Rule 2: absent is absent — a number nobody reported is NULL with a reason,
        never a zero.

The `from_claude_result_frame` tests run against a RECORDED frame from the live
probe (fixtures/claude_stream_probe.jsonl, claude 2.1.119, 2026-08-10), not a
hand-written imitation of one. Discipline #9: assertions come from the spec
source, and here the harness's own output is the spec source.
"""

import json
from pathlib import Path

from factory.usage import DOLLARS_HARNESS_IMPUTED, UsageBreakdown

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "claude_stream_probe.jsonl"


def _recorded_result_frame() -> dict:
    frames = [json.loads(ln) for ln in FIXTURE.read_text().splitlines() if ln.strip()]
    return next(f for f in reversed(frames) if f.get("type") == "result")


# ---------------------------------------------------------------------------
# rule 1 — reasoning is never a fifth addend
# ---------------------------------------------------------------------------
def test_billable_total_sums_exactly_four_addends():
    u = UsageBreakdown(
        input_tokens=100,
        output_tokens=200,
        cache_read_tokens=300,
        cache_write_tokens=400,
        reasoning_tokens=150,
    )
    assert u.billable_token_total() == 1000


def test_reasoning_tokens_do_not_move_the_total():
    without = UsageBreakdown(input_tokens=1, output_tokens=2, cache_read_tokens=3,
                             cache_write_tokens=4)
    with_reasoning = UsageBreakdown(input_tokens=1, output_tokens=2, cache_read_tokens=3,
                                    cache_write_tokens=4, reasoning_tokens=999)
    assert without.billable_token_total() == with_reasoning.billable_token_total()


def test_reasoning_never_exceeds_output_in_the_one_line_framing():
    """The rendering says what reasoning IS, so no reader can add it themselves."""
    u = UsageBreakdown(input_tokens=1, output_tokens=10, reasoning_tokens=6)
    line = u.one_line()
    assert "reasoning=6" in line
    assert "share of out" in line


# ---------------------------------------------------------------------------
# rule 2 — absent is absent
# ---------------------------------------------------------------------------
def test_absent_carries_a_reason_and_no_numbers():
    u = UsageBreakdown.absent("mechanical phase — no model invoked")
    assert u.billable_token_total() is None
    assert u.input_tokens is None
    assert u.dollars is None
    assert u.absent_reason == "mechanical phase — no model invoked"


def test_absent_renders_as_null_with_the_reason_visible():
    line = UsageBreakdown.absent("harness killed on timeout").one_line()
    assert line.startswith("usage: NULL")
    assert "harness killed on timeout" in line


def test_a_frame_without_usage_becomes_absent_not_zero():
    u = UsageBreakdown.from_claude_result_frame({"type": "result", "result": "hi"})
    assert u.billable_token_total() is None
    assert "no usage object" in u.absent_reason


def test_partial_reporting_sums_only_what_was_reported():
    u = UsageBreakdown(input_tokens=5, output_tokens=None, cache_read_tokens=7)
    assert u.billable_token_total() == 12


# ---------------------------------------------------------------------------
# the recorded live frame (O2 / O4)
# ---------------------------------------------------------------------------
def test_parses_the_recorded_probe_frame():
    u = UsageBreakdown.from_claude_result_frame(_recorded_result_frame())
    assert u.input_tokens == 2
    assert u.output_tokens == 4
    assert u.cache_read_tokens == 15628
    assert u.cache_write_tokens == 9486
    assert u.billable_token_total() == 2 + 4 + 15628 + 9486


def test_the_probe_frame_reports_no_reasoning_so_reasoning_stays_null():
    frame = _recorded_result_frame()
    assert "reasoning_tokens" not in frame["usage"], (
        "the fixture changed — if the harness now reports reasoning_tokens, usage.py's "
        "O2 finding needs re-probing, not a quiet test edit"
    )
    u = UsageBreakdown.from_claude_result_frame(frame)
    assert u.reasoning_tokens is None
    assert "no reasoning_tokens field" in u.absent_reason


def test_dollars_are_recorded_but_labelled_as_an_imputation():
    """O4 delta: the subscription lane DOES report total_cost_usd. It is list price."""
    u = UsageBreakdown.from_claude_result_frame(_recorded_result_frame())
    assert u.dollars is not None and u.dollars > 0
    assert u.dollars_source == DOLLARS_HARNESS_IMPUTED
    assert "imputed" in u.dollars_source, (
        "any dollars figure must carry a source label, or a downstream report will "
        "claim a flat-rate subscription spent money it did not spend"
    )


def test_no_dollars_means_no_source_label():
    u = UsageBreakdown.from_claude_result_frame({"usage": {"input_tokens": 1}})
    assert u.dollars is None
    assert u.dollars_source is None


# ---------------------------------------------------------------------------
# merge across retry attempts
# ---------------------------------------------------------------------------
def test_merge_accumulates_across_attempts():
    a = UsageBreakdown(input_tokens=10, output_tokens=1, dollars=0.5,
                       dollars_source=DOLLARS_HARNESS_IMPUTED)
    b = UsageBreakdown(input_tokens=20, output_tokens=2, dollars=0.25,
                       dollars_source=DOLLARS_HARNESS_IMPUTED)
    merged = a.merge(b)
    assert merged.input_tokens == 30
    assert merged.output_tokens == 3
    assert merged.dollars == 0.75
    assert merged.billable_token_total() == 33


def test_absent_merged_with_present_yields_present():
    merged = UsageBreakdown.absent("attempt 1 never launched").merge(
        UsageBreakdown(input_tokens=7, output_tokens=1)
    )
    assert merged.billable_token_total() == 8


def test_absent_merged_with_absent_stays_null():
    merged = UsageBreakdown.absent("a").merge(UsageBreakdown.absent("b"))
    assert merged.billable_token_total() is None
    assert merged.absent_reason == "a"


def test_to_dict_round_trips_every_field():
    u = UsageBreakdown(input_tokens=1, reasoning_tokens=2, dollars=3.0,
                       dollars_source=DOLLARS_HARNESS_IMPUTED, absent_reason=None)
    d = u.to_dict()
    assert set(d) == {
        "input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens",
        "reasoning_tokens", "dollars", "dollars_source", "absent_reason",
    }
    assert UsageBreakdown(**d) == u
