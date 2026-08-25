"""Labor harnesses — the lanes that actually execute a phase.

Spec A § 5. THREE lanes, all subscription-native (strategy § 4: no third-party
harness on the Claude lane -- pi's providers.md is explicit that Claude
subscription use through a third-party harness bills per token):

  - `claude_code` — LIVE. `claude --agent <seam> -p ... --output-format stream-json
    --verbose`. Named seam agents only: the discipline stack loads with the name.
  - `codex` — LIVE since 2026-08-24. `codex exec --json ... -` under THE SERIAL LAW
    (one `codex exec` at a time, one `auth.json`, one job stream), enforced by
    `factory/lane.py`'s `flock` at the invocation site. Was an honest stub blocked
    on Matt action T16; T16 is done, so the stub and its `HONEST_STUB` /
    `BLOCKED_ON` markers are DELETED rather than left beside a working body.
  - `grok` — LIVE since 2026-08-24, build-authorized by jack-ryan's re-ratification
    addendum (D-6). `grok -p "<prompt>" --output-format json --no-leader` against
    `~/.grok/bin/grok`, which is NOT on PATH and is resolved explicitly. Serialised
    with the SAME primitive on a DIFFERENT credential (`~/.grok`), so the two vendor
    lanes never contend: parallel Codex+Grok is LEGAL and intended.

There is NO stub in this package. `tests/test_no_stub_gates.py` asserts that as an
equality against the empty set — it used to carve out the Codex module by name, and
that carve-out is gone with the thing it forgave.

**THE THREE LANES DO NOT HAVE THE SAME FENCE, AND THE DIFFERENCES ARE NOT COSMETIC.**
The Claude lane's pre-hoc containment is a tool allowlist (`--tools`, base names only
— see `claude_code.py` for how little that buys). The Codex lane has no such flag; its
containment is the SANDBOX MODE (`-s read-only` is the posture of record for research
jobs). The Grok lane's is `--permission-mode` plus `--disable-web-search`. Both vendor
harnesses therefore publish a `validate_tools` that REFUSES, rather than one that
accepts a list it cannot enforce — and for two DIFFERENT reasons, each stated in its
own module.

**ONE MORE ASYMMETRY, STATED HERE BECAUSE IT IS THE ONE MOST LIKELY TO BE FLATTENED:**
the Codex serial law is a VERIFIED VENDOR PRECONDITION; the Grok serial policy is OUR
CHOICE, taken because no equivalent xAI constraint has been verified. Same primitive,
two kinds of rule. A reader who cannot tell them apart will defend the policy as if it
were the law, and will never be able to find what it rests on.
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
from . import grok  # noqa: F401,E402

__all__ = [
    "HarnessAdapter",
    "RawResult",
    "available_harnesses",
    "get_harness",
    "register_harness",
]
