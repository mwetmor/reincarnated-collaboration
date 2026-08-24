"""Labor harnesses — the lanes that actually execute a phase.

Spec A § 5. Two lanes, both subscription-native (strategy § 4: no third-party
harness on the Claude lane -- pi's providers.md is explicit that Claude
subscription use through a third-party harness bills per token):

  - `claude_code` — LIVE. `claude --agent <seam> -p ... --output-format stream-json
    --verbose`. Named seam agents only: the discipline stack loads with the name.
  - `codex` — LIVE since 2026-08-24. `codex exec --json ... -` under THE SERIAL LAW
    (one `codex exec` at a time, one `auth.json`, one job stream), enforced by
    `factory/lane.py`'s `flock` at the invocation site. Was an honest stub blocked
    on Matt action T16; T16 is done, so the stub and its `HONEST_STUB` /
    `BLOCKED_ON` markers are DELETED rather than left beside a working body.

There is now NO stub in this package. `tests/test_no_stub_gates.py` asserts that as
an equality against the empty set — it used to carve out this one module by name, and
that carve-out is gone with the thing it forgave.

The two lanes do not have the same fence, and the difference is not cosmetic. The
Claude lane's pre-hoc containment is a tool allowlist (`--tools`, base names only —
see `claude_code.py` for how little that buys). The Codex lane has no such flag; its
containment is the SANDBOX MODE (`-s read-only` is the posture of record for research
jobs). `CodexHarness` therefore publishes a `validate_tools` that REFUSES, rather
than one that accepts a list it cannot enforce.
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
