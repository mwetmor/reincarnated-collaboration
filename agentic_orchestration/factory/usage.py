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
        return "usage: " + " ".join(parts)
