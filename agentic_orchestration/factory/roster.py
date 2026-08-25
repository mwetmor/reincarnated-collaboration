"""The agent roster — ONE spelling of the fleet's seam names, for every mechanism.

**Why this is its own module and not a constant inside `custody.py` or `jobqueue.py`.**

Two independent axes now speak the word *seam*:

  * **agent-level custody** (lane spec § 11) — `_custody.tsv`'s `seam` column, the grain
    at which a dispatcher asks *"is somebody mid-flight in this seam?"*;
  * **the Grok lane's per-agent slot** (§ 9.6 AM-3, Amendment M) — the grain at which a
    vendor fire asks *"does this agent already hold a slot?"*

**Amendment M.4 is explicit that these two share a VOCABULARY and must not share a
MECHANISM:** a vendor fire that consulted the custody ledger would acquire a second
truth source, and a missing or stale CLAIM row would then block a legal fire. Putting
the roster in `custody.py` and importing it from the harness path would make that
coupling one edit away and would read, to a later author, as permission for it. Putting
a second copy beside the harness would make `star-lord` and `star-lord` two different
constants the day one of them gains a name. A module that owns exactly the NAMES —
and knows nothing about ledgers, locks or lanes — is the only shape with neither
defect.

**Amendment M.3 — the roster is CLOSED, and that is the whole point.** A free-text seam
field makes `star-lord` and `starlord` two agents, and per-agent exclusivity then fails
**silently**: both spellings acquire their own per-seam lock, both fire, and every
instrument reports compliance. Silence is the one failure direction the lane spec
refuses everywhere else, so the field is validated by MEMBERSHIP and a name outside the
roster is **refused, never normalised** — normalising a typo is guessing which agent was
meant, at exactly the moment being wrong is undetectable.

SOURCE OF RECORD: `agentic_orchestration/AGENTS.md` § 2, *"The team (12 entities)"* —
eleven Mac-resident agents plus Matt, who is **not** on this roster: he is a human whose
sessions custody explicitly does not gate (§ 11.5) and who does not hold vendor slots.
Read off that table on 2026-08-25 rather than from memory; the retired PC-resident team
(David-H, Radagast, Sam, Mantis) is deliberately absent, and `legolas-crawler` is
deliberately PRESENT and distinct from `legolas` — they are two agents on two models
(Matt ruling 2026-07-24), and collapsing them would let a crawler fan-out and a research
job collide on one slot.
"""

from __future__ import annotations

#: The eleven Mac-resident agent seams. PINNED BY EQUALITY in
#: `tests/test_vocabularies.py`: ADDITION is the fail-open direction — a name added here
#: is an agent nobody adjudicated getting its own concurrent Grok slot, which raises the
#: fleet's real parallelism against one credential without anyone deciding to.
AGENT_ROSTER: frozenset[str] = frozenset({
    "knight-rider",
    "jack-ryan",
    "gandalf",
    "rocket",
    "gamora",
    "star-lord",
    "drax",
    "legolas",
    "legolas-crawler",
    "elrond",
    "galadriel",
})


def validate_seam(seam: object, *, where: str) -> str:
    """Return the seam name, or RAISE. Never defaults, never normalises, never guesses.

    `where` names the call site in the refusal, because a governance refusal that cannot
    say which surface refused gets fixed by whoever guesses first — the same reason
    `_validate_fence` carries its lane name.

    Case is NOT folded and whitespace is NOT stripped from the middle: a name that needs
    normalising to match is a name whose author did not type the roster's spelling, and
    the cheapest moment to say so is before anything is written. Surrounding whitespace
    IS stripped, because that is an artifact of shell quoting rather than of a typo, and
    refusing it would only teach callers to `.strip()` before calling — which moves the
    refusal one frame away from where it can be understood.
    """
    text = "" if seam is None else str(seam).strip()
    if not text:
        raise ValueError(
            f"{where}: REFUSAL TO FIRE — no seam named. **Amendment M:** `seam` is a "
            "REQUIRED field on this lane, never defaulted and never inferred from "
            "`curator` (the curator owns the OUTPUT; the seam is the agent whose "
            "process makes the INVOCATION, and they legitimately differ). The per-agent "
            "slot is keyed on this name, so an unnamed seam is not a job with a missing "
            "label — it is a job that cannot be excluded against. Pass "
            f"`seam=\"<agent>\"` from {sorted(AGENT_ROSTER)}."
        )
    if text not in AGENT_ROSTER:
        raise ValueError(
            f"{where}: seam {text!r} is not on the agent roster. Known seams: "
            f"{sorted(AGENT_ROSTER)}. **Amendment M.3:** this vocabulary is CLOSED "
            "because a free-text seam makes two spellings of one agent into two agents "
            "— both acquire their own per-seam lock, both fire, and per-agent "
            "exclusivity fails with every instrument reporting compliance. A near miss "
            "is refused rather than corrected: guessing which agent was meant is only "
            "safe when being wrong is visible, and here it is not."
        )
    return text
