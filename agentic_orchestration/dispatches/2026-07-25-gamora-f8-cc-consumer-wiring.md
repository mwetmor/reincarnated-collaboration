# DISPATCH — gamora: F8 hard-CC consumer wiring (BUILD) + blast-radius A/B

**From:** gandalf (SPEC-AUTHOR), under Matt ruling 2026-07-25
**To:** gamora
**Type:** PRODUCTION CODE — simulation seam. **Gate 2 (jack-ryan) REQUIRED before merge-close.**
**Authorization (Matt, verbatim, 2026-07-25):**
> *"We ARE building our all mechanics needed into our engine. If we don't yet have CC in the
> sim, then we build it in — we don't work around it."*

This ruling reframes goal 1 of the GD program as a **build program**: the G1-A register's
BLOCKED families are a build queue, not a gap ledger. F8 goes first — Matt's named example,
and your audit's highest coverage-per-line item.

---

## 1. What to build (your own audit's § 4 F8 row is the spec seed)

Wire the **consumption half** of the hard-CC stack into the live loop
(`run_spatial_fight` path — the one with 20 production importers, audit § 1):

1. **Action lock** — `_select_skill_for_entity` (`spatial_engine.py:1931`): a mob whose
   `combatant_state` carries live `stun` / `freeze` (and `silence` for skill-gating per its
   existing semantics) selects NO action.
2. **Movement lock + slow composition** — `_navigate_entity` (`spatial_engine.py:1836`):
   live `root`/`freeze`/`stun` ⇒ zero displacement; live `chill` ⇒ `slow_factor` applied.
   **Composition with curse:decrepify is a Discipline #1 item** — the decrepify docstring
   already declares *"NOT additive with chill/root"*; author the composition rule (multiplicative
   vs floor vs min) in a math note BEFORE code:
   `reincarnated-engine/src/reincarnated/simulation/math/` (KF-2 note is the format precedent).
3. **Symmetric-side verification** — your audit probed mob-side consumption. VERIFY the
   player-side consumer status for the same effects (does the player loop consume stun/root/
   chill?) and wire or report per what you find. If player-side is also unwired, that is in
   scope for this dispatch — Matt's ruling is "build it in," not "build the mob half in."

**In scope:** the effects with existing application machinery (registry `damage_resolver.py:62`,
DR windows, boss tiers). **NOT in scope:** `Paralyze`/`Trapped`/`KnockedDown`/`Confused` as new
mechanisms (F8's ABSENT members need design specs — gandalf owes those; knockback additionally
sits on the F6 shared displacement prerequisite your audit isolated). Do not green-field here.

## 2. Blast-radius A/B (the empirical answer to the balance-integrity question)

After wiring, answer the routed question — *did historical balance verdicts for control kits
depend on CC landing?* — **empirically, not by inference**: run a control-oriented kit (and one
damage-baseline kit as control arm) through the balance loop **pre-wiring vs post-wiring**
(smoke-test mode first per Discipline #2; same seeds, no parallel regens of the same seed).
The delta IS the blast radius. Report magnitude + which historical verdict classes need an
asterisk, if any. If the delta is large, that finding routes to Matt via gandalf — do not
re-derive historical seasons yourself.

## 3. Disciplines in force

Math-before-code (#1, the composition rule) · smoke-test before full (#2) · your own probe
(`/tmp/gamora_cc_probe.py` spec, audit § 6) becomes the acceptance test skeleton — all five
CC arms must flip from `0 / 0.5000 m` to `None / 0.0000 m` (chill arm: `0.05 m` at
slow_factor 0.10, pending your composition rule) with positive controls unchanged · DR/boss-tier
behavior must be covered by tests at the consumer (immunity window ⇒ no lock) · tag intermediate
state `gamora/v-f8-cc-1` · **Gate 2 pre-registered: jack-ryan reviews before this closes.**

## 4. Output

- Code + tests in `reincarnated-engine` (working branch `main`), tagged.
- Math note (composition rule).
- Report: `agentic_orchestration/gamora/notes/2026-07-25-f8-cc-wiring-and-blast-radius.md` —
  wiring summary (file:line), acceptance-probe table (before/after), A/B blast-radius numbers,
  player-side verdict, Gate-2 request filed at `agentic_orchestration/qa/pending/`.
- **Ladder consequence to state in the report:** the L0 no-CC character constraint retires
  when this clears Gate 2.

**Signed:** gandalf, 2026-07-25. Build it in; don't work around it.
