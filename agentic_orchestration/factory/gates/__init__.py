"""Claim gates — the per-landing law, compiled.

Spec A § 4. Signature: `gate(envelope, run, **args) -> GateReport`. Gates
adjudicate ARTIFACTS ON DISK, never the envelope's own word.

Three laws hold in this package and are test-enforced:

1. **No stub gates, ever.** A gate that cannot execute returns NOT_RUNNABLE with
   a reason -- never green. `tests/test_no_stub_gates.py` greps this tree for the
   stub signatures (NotImplementedError, `pass  # TODO`, bare `exit 0`) and fails
   on any hit. SSSF's echo-exit-0 stubs are the named anti-pattern.
2. **Only PASS is green.** FAIL and NOT_RUNNABLE are both red.
3. **Every gate is falsifiable.** `tests/test_gates.py` requires a
   (green fixture, broken fixture) pair per registered gate: strip the thing the
   gate checks and the gate must red. A gate with no falsification fixture fails
   the suite -- registry coverage is asserted, not assumed.
"""

from .base import (  # noqa: F401
    GateReport,
    GateStatus,
    RunContext,
    available_gates,
    gate,
    run_gate,
)
from . import core  # noqa: F401,E402  (registers the v1 six)
from . import digest  # noqa: F401,E402
from . import media  # noqa: F401,E402

__all__ = [
    "GateReport",
    "GateStatus",
    "RunContext",
    "available_gates",
    "gate",
    "run_gate",
]
