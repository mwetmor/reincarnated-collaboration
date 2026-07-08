# Discipline #2 Amendment Proposal — the Full-Fire Rider

**Proposer:** gandalf ⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier — engineering-disciplines
is his seam per `canonical-doc-format.md §6.7`; I propose, he ratifies and homes the text).
**Date:** 2026-07-08
**Evidence base:** `2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md` (same date).
**Target doc:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md`,
Discipline #2 (smoke-test vs full-regen) — extension, not a new number (numbering is jack-ryan's call).

---

## The gap the incident exposed

Discipline #2 says *prefer* smoke-scale validation before full-regen. It is silent on the
**authorization artifact** — what a transmission/dispatch must CONTAIN before a full-population
run is fireable. The 2026-07-08 incident: a rider carrying a verdict criterion but **no instrument
identity** and **no pilot citation** authorized a ~50 h run on the wrong gauntlet while the right
gauntlet's pilot verdicts sat open/failed. The executor ran it faithfully — nothing in the rider
was violated, because the rider demanded nothing. The discipline gap is rider-completeness.

## Proposed amendment text (jack-ryan to edit/home)

> **#2-FF — Full-fire rider (rider-completeness gate).** Any transmission/dispatch authorizing a
> **population-scale run** must carry BOTH clauses; absent either, the run is **un-authorizable
> and the executor HALTS and asks** (halt-loud, not best-effort):
>
> **(a) Instrument identity + verification.** Name the verdict-rendering instrument (which
> gate/gauntlet/band set judges the run) AND include a pre-fire verification — one command, one
> grep, or one expected first-N-log-lines signature — proving the *executable path* runs that
> instrument. A verdict criterion without instrument identity is half a rider.
>
> **(b) Pilot citation — non-waivable by silence.** Cite the pilot/smoke result the full fire
> stands on (path or verdict line), OR carry an explicit Matt-visible waiver with reason.
> Silence is not a waiver. "The pilots did not pass" is a STOP, not a footnote.
>
> **Trigger threshold (proposed, jack-ryan tunes):** projected wall-clock > 1 h OR > 20% of a
> population, whichever fires first. Projection from measured per-unit pace when available;
> from unit-count arithmetic otherwise.

## Rationale

1. **Cost asymmetry.** The two clauses cost minutes at authoring (the incident's clause-(a)
   check was one grep). The miss cost 88 min of burned compute, a Matt-kill, and — absent
   Matt's own sizing instinct — ~50 h plus a mis-stamped survivor population flowing toward
   One-Realm bundle assembly.
2. **Executor-enforceable.** Rider-completeness is checkable by the receiving agent without
   design judgment: does the rider name an instrument + verification? does it cite a pilot or
   waiver? This puts a second pair of eyes on exactly the two fields the author is most likely
   to assume away — the author's blind spot is structural (they *believe* the instrument is
   right; that belief is why they didn't check).
3. **The composing disciplines were each individually insufficient.** #2 (prefer smoke)
   was skippable by omission; #11 (empirical inspection) binds the executor's findings, not the
   authorization; framing-audit (gandalf OP §4.1) was habitually applied to design verdicts,
   not run authorizations. #2-FF closes the seam between them at the artifact level.

## Non-goals / scope guards

- Does NOT slow small runs, pilots, or smokes — they are below threshold by construction.
- Does NOT add a jack-ryan review leg per fire — enforcement is executor-side rider inspection.
- Does NOT amend the four-family architecture or any band/criterion (no design surface moves).
- Companion hardening (OPTIONAL, star-lord's call, not part of the discipline): drivers print a
  start-banner with instrument identity + projected fight count + wall-clock projection. The
  incident's log would have self-indicted in its first line.

## Ratification ask (jack-ryan)

Ratify #2-FF as written or amended; home it under Discipline #2; rule the trigger threshold.
If ratified, KR folds the rider fields into the dispatch template so completeness is structural
rather than remembered.

---

**Sign-off:** gandalf (proposer), 2026-07-08. Evidence: same-date post-mortem;
`w3_emission_driver.py:505`; `gauntlet_sim.py:264-269`; measured pace 1.674 min/candidate.
