"""Labor harnesses — the lanes that actually execute a phase.

Spec A § 5. Two lanes, both subscription-native (strategy § 4: no third-party
harness on the Claude lane -- pi's providers.md is explicit that Claude
subscription use through a third-party harness bills per token):

  - `claude_code` — LIVE. `claude --agent <seam> -p ... --output-format stream-json
    --verbose`. Named seam agents only: the discipline stack loads with the name.
  - `codex` — HONEST STUB. Interface pinned, body raises NotImplementedError,
    blocked on Matt action T16.

An honest stub in an ADAPTER is legal; a stub in a GATE is not. The distinction
is load-bearing and `tests/test_no_stub_gates.py` enforces which side of the line
each lives on.
"""

from .base import (  # noqa: F401
    HarnessAdapter,
    RawResult,
    available_harnesses,
    get_harness,
    register_harness,
)
from . import claude_code  # noqa: F401,E402
from . import codex  # noqa: F401,E402

__all__ = [
    "HarnessAdapter",
    "RawResult",
    "available_harnesses",
    "get_harness",
    "register_harness",
]
