"""Host facts the factory can read but cannot control — recorded, not assumed.

Gate-2 H6. Two admissions belong on every receipt, and neither of them is a
measurement of the phase. They are measurements of *the measurement*.

**One — the host's own permission default.** H1's root cause was not in this tree.
This host's `~/.claude/settings.json` carries `permissions.defaultMode`, and on the
machine that built the factory it reads `bypassPermissions`. Every containment claim
the wall makes was made underneath that setting. A receipt that records the phase's
`--allowedTools` argv and says nothing about the host's default has recorded the
fence and omitted the ground it stands on — and J1 already established that the argv
is not evidence of the grant in headless `default` mode.

**Two — the trees that were actually fingerprinted.** `fingerprint` measures the
declared `repos`. Writes anywhere else on the disk are not detected, not classified,
and not rolled back. A green containment verdict therefore means "no unauthorised
writes *in these trees*". It does not mean "no unauthorised writes". That sentence
has to appear on the GREEN path, because green is the only path where a reader is
inclined to stop asking.

What this module deliberately does NOT do
-----------------------------------------
It does not resolve the effective permission mode. Claude Code layers enterprise
policy, CLI flags, environment, project `.claude/settings.json`,
`.claude/settings.local.json`, and the user file — and this reads exactly one of
them. Reporting a single layer as though it were the answer is the same defect this
whole review series keeps finding: a predicate that answers a slightly different
question than the one asked. So the recorded mode always travels with a `source`
sentence naming which file it came from and which layers were not consulted.

And an unstated mode is recorded as **NULL**, never as `"default"`. Claude Code's
own fallback is `default`, so filling it in would be *correct on this host and
unfalsifiable everywhere* — the exact shape `usage.py` refuses when it declines to
zero-fill an absent token count. Absent is absent.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

#: Named once so the layering caveat cannot drift apart from the value it qualifies.
_LAYERS_NOT_RESOLVED = (
    "enterprise policy, CLI flags, environment, and project-level "
    ".claude/settings{,.local}.json are NOT resolved here"
)


@dataclass(frozen=True)
class HostPermissions:
    """One layer of the host's permission configuration, and what it is worth.

    `mode` is None whenever the file did not state one — absent, unreadable,
    unparseable, or present-and-silent. `source` is never None: it is the sentence a
    later reader needs in order to know what the mode does and does not mean.
    """

    mode: str | None
    source: str


def default_settings_path() -> Path:
    """The user-level settings file, resolved at CALL time.

    A module-level constant would be computed at import and would make the
    production route untestable — which is the ROUTE axis this review series keeps
    landing on. Resolved here, a row can move `Path.home()` and watch the real
    default follow it.
    """
    return Path.home() / ".claude" / "settings.json"


def read_host_permission_mode(path: Path | None = None) -> HostPermissions:
    """Read `permissions.defaultMode` from the user settings file.

    Read-only, and failure-tolerant by design: this is an observation about the
    host, and a run must not abort because the host is configured in a shape this
    function did not expect. Every failure mode gets its OWN source sentence, so
    "we looked and it was silent" is never confusable with "we never looked".
    """
    target = path if path is not None else default_settings_path()
    try:
        raw = target.read_text(encoding="utf-8")
    except OSError as exc:
        return HostPermissions(
            None,
            f"UNREAD — {target} could not be read (errno {exc.errno}); the host's "
            f"permission default is UNKNOWN, not permissive and not restrictive. "
            f"{_LAYERS_NOT_RESOLVED}.",
        )
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return HostPermissions(
            None,
            f"UNPARSEABLE — {target} is not valid JSON ({exc.msg} at line "
            f"{exc.lineno}); the host's permission default is UNKNOWN. "
            f"{_LAYERS_NOT_RESOLVED}.",
        )
    permissions = data.get("permissions") if isinstance(data, dict) else None
    mode = permissions.get("defaultMode") if isinstance(permissions, dict) else None
    if not isinstance(mode, str) or not mode:
        return HostPermissions(
            None,
            f"UNSTATED — {target} was read and states no permissions.defaultMode. "
            f"Recorded as UNKNOWN rather than as Claude Code's fallback, which "
            f"would be a guess dressed as a measurement. {_LAYERS_NOT_RESOLVED}.",
        )
    return HostPermissions(
        mode,
        f"read from {target} (permissions.defaultMode). This is ONE layer: "
        f"{_LAYERS_NOT_RESOLVED}.",
    )


def describe_measurement_limit(trees: list[Path] | list[str]) -> str:
    """The sentence that keeps a green containment verdict from over-claiming.

    Rendered on every run, green ones included. The wall fingerprints the declared
    trees and nothing else; a phase with unrestricted `Bash` reaches the whole
    filesystem. Both facts are true at once, and only the first one shows up in the
    verdict, so the second one has to be written down next to it.
    """
    if not trees:
        return (
            "NO tree was fingerprinted for this run. There is no containment "
            "evidence here at all — the absence of a reported breach means only "
            "that nothing was looked at."
        )
    listed = ", ".join(str(t) for t in trees)
    return (
        f"Containment was measured in these trees ONLY: {listed}. Writes elsewhere "
        f"on this host were not detected, not classified, and not rolled back. A "
        f"green verdict means 'no unauthorised writes HERE', not 'no unauthorised "
        f"writes'."
    )
