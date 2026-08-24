"""UsageBreakdown — token accounting that refuses to lie.

Spec A § 6. Two standing rules are enforced here, not merely documented:

1. **Reasoning tokens are a SHARE of output tokens, never a fifth addend.**
   `billable_token_total()` sums input + output + cache_read + cache_write and
   excludes reasoning. A test asserts it.
2. **Absent is absent.** If the harness does not report a number, the column is
   NULL and `absent_reason` says why. Tokens are never invented, never zero-filled.

O2/O4 field survey (star-lord probe, claude 2.1.119, 2026-08-10) -- the `result`
frame of `--output-format stream-json` carries:
    usage.input_tokens, usage.output_tokens,
    usage.cache_read_input_tokens, usage.cache_creation_input_tokens,
    total_cost_usd, modelUsage{...}
No `reasoning_tokens` key was present in the probe sample -> reasoning stays NULL
with a reason rather than being folded into output.

O4 finding (spec expected NULL): `total_cost_usd` IS populated on the
subscription lane ($0.0672 for a 4-output-token call). It is a harness-computed
LIST-PRICE imputation, not a billed amount -- the Max subscription is flat. So we
record it AND record `dollars_source` so no downstream report can claim it was
money spent.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

DOLLARS_HARNESS_IMPUTED = "harness_reported_imputed"
"""Harness-computed list-price estimate. NOT an amount billed on a subscription lane."""

DOLLARS_NONE = None


@dataclass
class UsageBreakdown:
    input_tokens: int | None = None
    output_tokens: int | None = None
    cache_read_tokens: int | None = None
    cache_write_tokens: int | None = None
    reasoning_tokens: int | None = None  # share of output_tokens; never a fifth addend
    dollars: float | None = None
    dollars_source: str | None = None
    absent_reason: str | None = None

    # -- construction ------------------------------------------------------
    @classmethod
    def absent(cls, reason: str) -> "UsageBreakdown":
        """No model was invoked, or the harness reported nothing. Say which."""
        return cls(absent_reason=reason)

    @classmethod
    def from_claude_result_frame(cls, frame: dict[str, Any]) -> "UsageBreakdown":
        """Parse the `result` frame of `claude -p --output-format stream-json --verbose`."""
        usage = frame.get("usage") or {}
        if not usage:
            return cls.absent("claude result frame carried no usage object")

        def _int(value: Any) -> int | None:
            return int(value) if isinstance(value, (int, float)) else None

        reasoning = _int(usage.get("reasoning_tokens"))
        dollars = frame.get("total_cost_usd")
        dollars = float(dollars) if isinstance(dollars, (int, float)) else None
        return cls(
            input_tokens=_int(usage.get("input_tokens")),
            output_tokens=_int(usage.get("output_tokens")),
            cache_read_tokens=_int(usage.get("cache_read_input_tokens")),
            cache_write_tokens=_int(usage.get("cache_creation_input_tokens")),
            reasoning_tokens=reasoning,
            dollars=dollars,
            dollars_source=DOLLARS_HARNESS_IMPUTED if dollars is not None else None,
            absent_reason=None
            if reasoning is not None
            else "harness reported no reasoning_tokens field",
        )

    @classmethod
    def from_codex_turn_completed(cls, frame: dict[str, Any]) -> "UsageBreakdown":
        """Parse the `turn.completed` frame of `codex exec --json`.

        The frame's own vocabulary, measured on codex-cli 0.147.0::

            {"type": "turn.completed", "usage": {
                "input_tokens": 1581825, "cached_input_tokens": 1449472,
                "cache_write_input_tokens": 0, "output_tokens": 7148,
                "reasoning_output_tokens": 4084}}

        **`cached_input_tokens` IS A SUBSET OF `input_tokens`, NOT A SIBLING OF IT.**
        This is the one thing in this mapping that could silently corrupt every
        number downstream, so it is established rather than assumed. Over the VFX
        run's 30 jobs the totals are `input 72,375,471` and `cached 67,431,424`;
        `cached / input = 0.9317`, and the banked lane statistic -- carried in
        `workflow-upgrades.md` and in the flight-recorder spec -- is
        **93.2 % cache-hit**, described there as "the cache absorbed 93.2 % OF
        them". The disjoint reading gives `cached / (cached + input) = 0.4823`,
        which matches nothing anyone recorded. So the containment direction is
        settled by the record, and:

          * `input_tokens` here = `input_tokens - cached_input_tokens`, the UNCACHED
            share. Passing the vendor's `input_tokens` through unchanged would make
            `billable_token_total()` count 67 M tokens twice on a 72 M-token run --
            a 93 % over-report, produced by a mapping that looked like a rename.
          * `cache_read_tokens` = `cached_input_tokens`.

        `reasoning_output_tokens` maps to `reasoning_tokens`, which this module
        already defines as a SHARE OF OUTPUT and never a fifth addend. That is the
        vendor's own framing too (`reasoning_OUTPUT_tokens`), so the two agree.

        Codex reports NO cost figure at all -- unlike the Claude lane, where
        `total_cost_usd` is present as a list-price imputation. Absent is absent:
        `dollars` stays NULL and `absent_reason` says why, so `one_line()` prints
        `[INCOMPLETE: ...]` rather than presenting a complete-looking row whose
        money column was never reported.
        """
        usage = frame.get("usage") or {}
        if not usage:
            return cls.absent("codex turn.completed frame carried no usage object")

        def _int(value: Any) -> int | None:
            return int(value) if isinstance(value, (int, float)) else None

        raw_input = _int(usage.get("input_tokens"))
        cached = _int(usage.get("cached_input_tokens"))
        uncached: int | None
        if raw_input is None:
            uncached = None
        elif cached is None:
            uncached = raw_input
        else:
            # `max(0, ...)` because a negative token count is not a number this
            # module will publish. If the vendor ever reports cached > input the
            # containment assumption above has broken, and the floor keeps the
            # arithmetic sane while `absent_reason` below says the split is suspect.
            uncached = max(0, raw_input - cached)
        contradiction = (
            raw_input is not None and cached is not None and cached > raw_input
        )
        return cls(
            input_tokens=uncached,
            output_tokens=_int(usage.get("output_tokens")),
            cache_read_tokens=cached,
            cache_write_tokens=_int(usage.get("cache_write_input_tokens")),
            reasoning_tokens=_int(usage.get("reasoning_output_tokens")),
            dollars=None,
            dollars_source=DOLLARS_NONE,
            absent_reason=(
                "codex reported cached_input_tokens > input_tokens, contradicting the "
                "subset relation this mapping is built on; the split is not trustworthy"
                if contradiction
                else "codex exec reports no cost figure; the ChatGPT subscription lane "
                "is flat-rate and no list-price imputation is emitted"
            ),
        )

    # -- arithmetic --------------------------------------------------------
    def billable_token_total(self) -> int | None:
        """input + output + cache_read + cache_write.

        Reasoning is deliberately NOT summed here: it is a share of output, and
        adding it double-counts. Returns None if every addend is absent.
        """
        addends = [
            self.input_tokens,
            self.output_tokens,
            self.cache_read_tokens,
            self.cache_write_tokens,
        ]
        present = [a for a in addends if a is not None]
        if not present:
            return None
        return sum(present)

    def merge(self, other: "UsageBreakdown") -> "UsageBreakdown":
        """Accumulate across retry attempts. Absent + present = present."""

        def _add(a: int | None, b: int | None) -> int | None:
            if a is None and b is None:
                return None
            return (a or 0) + (b or 0)

        dollars: float | None
        if self.dollars is None and other.dollars is None:
            dollars = None
        else:
            dollars = (self.dollars or 0.0) + (other.dollars or 0.0)
        return UsageBreakdown(
            input_tokens=_add(self.input_tokens, other.input_tokens),
            output_tokens=_add(self.output_tokens, other.output_tokens),
            cache_read_tokens=_add(self.cache_read_tokens, other.cache_read_tokens),
            cache_write_tokens=_add(self.cache_write_tokens, other.cache_write_tokens),
            reasoning_tokens=_add(self.reasoning_tokens, other.reasoning_tokens),
            dollars=dollars,
            dollars_source=self.dollars_source or other.dollars_source,
            absent_reason=self.absent_reason or other.absent_reason,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def one_line(self) -> str:
        if self.billable_token_total() is None:
            return f"usage: NULL ({self.absent_reason or 'no reason recorded'})"
        parts = [
            f"in={self.input_tokens}",
            f"out={self.output_tokens}",
            f"cache_r={self.cache_read_tokens}",
            f"cache_w={self.cache_write_tokens}",
            f"total={self.billable_token_total()}",
        ]
        if self.reasoning_tokens is not None:
            parts.append(f"(reasoning={self.reasoning_tokens}, share of out)")
        if self.dollars is not None:
            parts.append(f"${self.dollars:.4f} [{self.dollars_source}]")
        line = "usage: " + " ".join(parts)
        # Gate-2 J3. A breakdown can be PARTLY known — real tokens from a completed
        # attempt plus an attempt whose cost the harness never reported. This method
        # used to drop `absent_reason` the moment any number was present, so the
        # partial case printed as if it were the whole, which is the under-reporting
        # this module's opening law exists to forbid. Numbers alone are not a claim
        # of completeness unless nothing is missing.
        if self.absent_reason:
            line += f"  [INCOMPLETE: {self.absent_reason}]"
        return line
