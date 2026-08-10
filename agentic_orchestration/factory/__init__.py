"""factory — the thin run spine.

Compiles the mechanical fraction of a run (phase sequencing, envelopes, claim
gates, receipts, permissions fingerprinting) into code. It ORCHESTRATES; the
labor harnesses EXECUTE; the charter GOVERNS.

Governing docs:
  - agentic_orchestration/operating-procedures/software-factory.md  (strategy, D1-D5)
  - agentic_orchestration/gandalf/notes/2026-08-10-factory-spine-spec.md  (Spec A)
  - agentic_orchestration/operating-procedures/desirable-run-pattern.md  (charter layer)

Standing laws compiled here:
  - A phase is FAILED until exactly one finish() collapses it. No override path.
  - Gates adjudicate ARTIFACTS ON DISK, never the envelope's own word.
  - No stub gates, ever. A gate that cannot run returns NOT_RUNNABLE (red).
  - Reasoning tokens are a SHARE of output tokens, never a fifth addend.
  - A permissions breach is evidence: roll back the excess and ABORT, never retry.
"""

__version__ = "1.0.0"

SPEC = "gandalf/notes/2026-08-10-factory-spine-spec.md"
