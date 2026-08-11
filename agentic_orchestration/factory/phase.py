"""The phase primitive — default-fail, with no override path.

Spec A § 2. A phase ENTERS as FAILED and stays FAILED unless exactly one
`finish()` collapses it. Unhandled exception -> FAILED with the traceback in
receipts. Two `finish()` calls -> FAILED, because a phase that reports twice does
not know what it did.

There is deliberately **no `force`, no `assume_success`, no override parameter**.
The KC2 emit wall's posture (`no_override`) is the ancestor and the law.

Gate verdicts can only ever DOWNGRADE a phase (`apply_gate_verdicts`). Nothing in
this module can turn a red into a green.
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass, field
from typing import Any

from .envelope import ENVELOPE_STATUSES, EnvelopeBase
from .usage import UsageBreakdown

FAILED = "FAILED"
PASS = "PASS"
PARTIAL = "PARTIAL"


class PhaseProtocolError(RuntimeError):
    """finish() called twice, or with a status outside the envelope vocabulary."""


@dataclass
class Phase:
    """Context manager. Enters FAILED; only a single finish() can collapse it."""

    name: str
    agent: str | None = None
    harness: str | None = None
    receipts: Any = None
    run_id: str | None = None
    idx: int = 0

    status: str = FAILED
    envelope: EnvelopeBase | None = None
    error: str | None = None
    attempts: int = 0
    #: H8. This default used to read `"mechanical phase — no model invoked"`, which
    #: is a positive claim about the world — that nothing was spent — asserted by a
    #: dataclass default that cannot know it. `usage.py`'s own law is "absent is
    #: absent … never invented": inventing the REASON breaks it exactly as surely as
    #: inventing a token count, and worse, because the invented reason is the
    #: reassuring one. An agentic phase whose harness raised never reaches the
    #: assignment in `runner._run_phase`, so this default is what `finish_phase`
    #: writes to the durable `usage_absent_reason` column — the ledger would say no
    #: model was invoked for a phase that named an agent and called a harness. The
    #: default now claims nothing beyond its own ignorance; the runner passes the
    #: lane-aware reason at construction.
    usage: UsageBreakdown = field(
        default_factory=lambda: UsageBreakdown.absent(
            "no usage recorded — the phase never reached the accounting point"
        )
    )
    phase_id: int | None = None
    _finished: bool = False
    _entered: bool = False

    # -- context management -------------------------------------------------
    def __enter__(self) -> "Phase":
        self._entered = True
        self.status = FAILED  # the default, restated where it is easy to read
        if self.receipts is not None and self.run_id is not None:
            self.phase_id = self.receipts.start_phase(
                self.run_id, self.idx, self.name, self.agent, self.harness
            )
            self.receipts.event(
                self.run_id, "phase_start", f"{self.name} (agent={self.agent})", self.phase_id
            )
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is not None:
            self.status = FAILED
            self.error = "".join(traceback.format_exception(exc_type, exc, tb))[:8000]
            self._record_end()
            # Suppress: a phase blowing up is a FAILED phase, recorded, not a crashed run.
            return not issubclass(exc_type, (KeyboardInterrupt, SystemExit))
        if not self._finished:
            self.status = FAILED
            unfinished = (
                "phase exited without calling finish() — default-fail stands "
                "(there is no assume-success path)"
            )
            self.error = f"{self.error} | {unfinished}" if self.error else unfinished
        self._record_end()
        return False

    # -- the single collapse ------------------------------------------------
    def finish(
        self,
        status: str,
        summary: str,
        artifacts: list[str] | None = None,
        notes_for_next_agent: str = "",
    ) -> EnvelopeBase:
        if self._finished:
            self.status = FAILED
            self.error = "finish() called more than once — the phase does not know what it did"
            raise PhaseProtocolError(self.error)
        if status not in ENVELOPE_STATUSES:
            self.status = FAILED
            self.error = f"finish() got status {status!r}, not one of {ENVELOPE_STATUSES}"
            raise PhaseProtocolError(self.error)
        self._finished = True
        self.envelope = EnvelopeBase(
            status=status,
            summary=summary,
            artifacts=list(artifacts or []),
            notes_for_next_agent=notes_for_next_agent,
        )
        self.status = {"PASS": PASS, "PARTIAL": PARTIAL, "FAIL": FAILED}[status]
        return self.envelope

    def finish_with_envelope(self, envelope: EnvelopeBase) -> EnvelopeBase:
        return self.finish(
            envelope.status,
            envelope.summary,
            envelope.artifacts,
            envelope.notes_for_next_agent,
        )

    # -- gates may only downgrade -------------------------------------------
    def apply_gate_verdicts(self, reports: list[Any]) -> str:
        reds = [r for r in reports if not getattr(r, "is_green", False)]
        if reds:
            self.status = FAILED
            names = ", ".join(f"{r.gate}:{r.status}" for r in reds)
            self.error = (self.error + " | " if self.error else "") + f"red gate(s): {names}"
        return self.status

    @property
    def is_green(self) -> bool:
        return self.status == PASS

    @property
    def finished(self) -> bool:
        """True once the single permitted finish() has landed."""
        return self._finished

    # -- receipts -----------------------------------------------------------
    def _record_end(self) -> None:
        if self.receipts is not None and self.phase_id is not None:
            self.receipts.finish_phase(
                self.phase_id, self.status, self.attempts, self.usage, self.error
            )
            self.receipts.event(
                self.run_id, "phase_end", f"{self.name} -> {self.status}", self.phase_id
            )
