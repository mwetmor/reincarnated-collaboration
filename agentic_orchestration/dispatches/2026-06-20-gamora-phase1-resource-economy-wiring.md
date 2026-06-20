# Dispatch — 2026-06-20 — gamora — Phase 1: Resource-economy wiring (instrument-validity workstream)

**From:** knight-rider
**To:** gamora (simulation seam)
**Approved by:** Matt 2026-06-20 (autonomous instrument-validity workstream authorization)
**Estimated effort:** half-day (WIRE, not BUILD — recompose-first)
**Acceptance:** energy pool gates + decrements per `energy_type`-branched config; measure-isolated harness shows the resource-shift delta against the CURRENT (untouched) bands; math-note-first; jack-ryan Gate-2 clean.

## Authoritative spec
This is **Phase 1** of the gandalf-authored instrument-validity workstream. Read it IN FULL first — it is the binding spec, including the pre-registered gates:
`agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (§2 spine, §3 Phase-1 detail + GATES G1/G2, §5 cautions).

## Context
Every band-fit to date was measured on a contaminated instrument. The resource economy is **modeled-but-not-wired** (Phase-0 verdict, brief §1): the entity carries `energy / max_energy / energy_regen / skill_energy_costs`, skills carry rolled `energy_cost`, the regen tick runs — BUT the selector/fire-gate only check cooldown + range, the pool is never decremented, and `energy_cost` is read only to emit a `resource_spent` telemetry event. The adapter even neutralizes the kernel gate (`spatial_resolver_adapter.py:192` `mana=1e9`). A complete consuming economy with 5 energy configs exists in the kernel (`combatant.py:347-385` `can_use_skill` + `_ENERGY_CONFIGS`; `ai_strategies.py:423-518` build-vs-spend) — retired-not-migrated when spatial took over. **Fix size: WIRE, not BUILD.**

This is the head of the offense-side dependency chain (1→2→3). Phase 2 (rotation selector) **falls out of** the `energy_type` branch you build here, so build the branch cleanly.

## Math-before-code (Discipline #1 — REQUIRED FIRST)
Author `simulation/math/<...>-phase1-resource-economy-2026-06-20.md` BEFORE wiring:
- Per-economy expected spend/regen balance (rage build-on-hit/starts-empty; focus full/decays; combo discrete 0–N; charge-stack hold; stamina fast-regen; mana-default spam→empty→throttle).
- Sanity-check that **no economy starves a kit to silence** (the old structural-mana-bug shape — escalate if any config would flatline a kit to ~0 KPM). This is the G2 escalation falsifier; pre-compute it.
- Cite code locations for every claim (Discipline #1.2 math-note code-citation).

## GATE G1 (BEFORE build) — PRE-RATIFIED in the brief (§3)
The doc-48 class-economy → kernel-config mapping is **already ratified** by gandalf: port the **5 configs + mana-default** → covers **8/10 classes including BOTH STR classes** (Barbarian-rage, Hoplite-steady). The two gaps (Skirmisher damage-taken-converts, Crusader HP-economy) **DEFER** — intentional scope-hold, neither is STR, neither blocks the Phase-6 STR read.
- **Do NOT re-litigate the mapping.** Proceed on the pre-ratification.
- **Escalate to KR ONLY IF:** (a) your math-note finds the 5-config port is materially more than "wire + branch" (scope surprise), OR (b) you find the kernel ALREADY implements damage-taken-converts / HP-as-resource (port them too — cheap; confirm scope with KR before expanding).

## The work (recompose-first — PORT, do not invent)
Port the kernel `_ENERGY_CONFIGS` into the spatial loop:
- **(a)** Wire an energy term into `skill_ready()`/the selector so a cast gates on `energy >= effective_cost` (selector at `spatial_engine.py:1023-1030`, `:1043-1057`, `:1580`).
- **(b)** Decrement at the cast site (`:1610-1620`, alongside the existing cooldown set + `resource_spent` event at `:1585`, `:1641-1648`).
- **(c)** `energy_type`-branched pool behavior (the generic 100/regen-10 is not faithful — see math-note). The regen tick (`:1719`) already exists.
- Remove/correct the `spatial_resolver_adapter.py:192` `mana=1e9` neutralizer so the gate it claims actually exists.
- **Invent no new mechanic.** The kernel holds the working reference. This is a port + a branch.

## Measure-ISOLATED (Discipline — load-bearing, brief §5)
- **Do NOT touch** `ENCOUNTER_COHORT_KPM_BAND` or the production gate. Bands stay as-is so the resource-shift is visible against the CURRENT bands. The refit is Phase 5 only.
- Run the measure-isolated harness on a **fresh disjoint seed base** (Discipline #3; known-USED bases to avoid: `[700000,766703]`, `[619000,684303]`). Fix the intra-run seed-stride overflow (DoT brief §11.1) before any harness re-use.
- **Semantic-shift declaration (Discipline #12):** resource-gating changes the meaning of every KPM/DPS field. Declare the boundary explicitly in the math-note/results, as the DPS field was declared.

## GATE G2 (AFTER measure) — report against this pre-registration
Expected direction: KPM **flat-or-DOWN** vs the un-gated baseline (the gate THROTTLES free-spammers); build-spend kits show a burst→lull rhythm. **Report your result against this table** — KR auto-resolves if the shift is in-direction.
- **Flag to KR ONLY IF:** KPM *rises* (gate not binding → wiring failed), OR any kit flatlines to ~0 KPM (cost-vs-pool mis-scale starving a kit silent).

## Cross-seam contract change? (Principle 6 gate)
Resource-gating is INTERNAL to the simulation seam (selector/cast-site/pool behavior). The `resource_spent` telemetry event already exists. If you add/rename/remove any telemetry field or fight_log key crossing the gamora→star-lord boundary, write `simulation/MIGRATION.md` per ADR-004. If no schema field changes, note that explicitly.

## Out of scope (do NOT do)
- No band refit (Phase 5 only).
- No magnitude re-tune of energy costs/regen beyond the faithful per-economy branch.
- No rotation-selector tier logic yet (that is Phase 2 — but build the `energy_type` branch so Phase 2 falls out of it cleanly).
- No DoT work (Phase 3). No mitigation work (Phase 4 — separate parallel dispatch).
- The two DEFERRED economies (Skirmisher, Crusader HP).

## Hand-back
Append a completion record: tag (`gamora/...` seam-prefixed), math-note path, harness results path, G2 self-assessment vs the table, MIGRATION.md status, notes for jack-ryan Gate-2. KR runs jack-ryan Gate-2 (mechanism correctness, V-gates, semantic-shift declaration, seed hygiene, no production-gate regression) on hand-back.
