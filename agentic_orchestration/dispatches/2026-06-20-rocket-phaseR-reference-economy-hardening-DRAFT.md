# Dispatch — 2026-06-20 — rocket — Phase R: Reference-economy hardening (AUTHORIZED)

> **AUTHORIZED 2026-06-20** — gandalf design ruling (`gandalf/notes/2026-06-20-instrument-validity-G1-rocket-economy-prerequisite-RULING.md`) + Matt scope authorization. Phase R was NOT in the original instrument-validity spine; it is a gandalf-ruled scope addition that Matt has now authorized as a hard-prerequisite to Phase 5. **FIRE.** See the LOCKED-TABLE / KEY-DERIVATION amendment below (§ "Gandalf design-constraint amendment") — it is binding and must be read before any code.

**From:** knight-rider
**To:** rocket (generation seam)
**Approved by:** Matt 2026-06-20 (scope authorization) + gandalf 2026-06-20 (design ruling)
**Estimated effort:** half-day (PORT not BUILD — recompose-first; doc-48 spec + kernel machinery both exist)
**Acceptance:** the generated harness population carries the doc-48 per-class economies (rage/combo/charge-stack/steady/mana etc.) as the authoritative `energy_type`, replacing the BC-tempo-inferred collapse-to-mana-default; the Barbarian-rage economy materializes on STR Barbarian entities; recompose-first held (no new mechanic); the bc_target round-trip guard passes; jack-ryan Gate-2 clean.

## Gandalf design-constraint amendment (BINDING — read before any code)

The doc-48 economy-by-kit-type assignment (G1 table) is LOCKED. It is NOT rocket's to re-decide, "improve," or collapse for convenience while wiring (recompose-first: PORT the assignment, do not author a new one). What IS rocket's room: the population→kit-type KEY — which population feature(s) (BC-cell / cohort / element / role / attribute-primary) deterministically recover the doc-48 kit-type, since the population carries NO doc-48 class field (it is built bottom-up; class_archetype=element, not a doc-48 class roster). Derive that key in the math-note FIRST (Discipline #1), before code. DESIGN TRIP-WIRE: if the population's features do NOT cleanly partition into the doc-48 economies — two economies fall into the same feature bucket — that is a design ambiguity, not an implementation choice. STOP and escalate to gandalf (fire gandalf-subagent) as a design call. Do NOT resolve it by expedient choice. This is the design-side twin of the bc_target round-trip guard the dispatch already carries: round-trip failure → KR; key-ambiguity → gandalf.

## Why this exists (the scope surprise)
Phase 1 (resource wiring) is correct and Gate-2'd — but gamora + gandalf found the *generated population* never carries the doc-48 economies. Generation infers a resource type from BC-tempo (`season_generation_pipeline.py:213-218` `_BC_TEMPO_TO_RESOURCE` → `{cooldown, energy, mana}`, all resolving to the SAME mana-default pool). The doc-48 per-class economies (doc 48 §3.1) never reach the spatial layer. So the **Barbarian-rage build-spend lever — the entire hinge of the Phase-6 STR (A)-vs-(B) read — is absent from the population.** Phase 6 on this population would be "a null instrument reporting a confident number" (gandalf). Phase 2 already corroborated this empirically: STR is throttled (2.2× KPM vs casters' 16-40×) purely because it borrows the wrong (mana-default) economy.

## Read these IN FULL first
1. gandalf's ruling (binding design spec for this phase): `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-20-instrument-validity-G1-rocket-economy-prerequisite-RULING.md`.
2. The workstream brief: `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (§1 Phase-0 canonical design-state; §3 Phase-1 G1 pre-ratified mapping table — the doc-48→kernel-config mapping you implement here).
3. doc 48 §3.1 (per-class economy assignment for all 10 Cycle-14 classes); doc 42 §2.2 / doc 40 §6 (the 8-model catalog, gear-roll-gated by class resource model).

## The work (recompose-first — PORT the doc-48 assignment onto generation; invent NOTHING)
Make the generation seam author the doc-48 per-class economy as the entity's authoritative `energy_type`, so the consuming spatial economy (Phase 1) + the branching selector (Phase 2, full branch set already built) see the real economies instead of mana-default.
- The G1 mapping is **pre-ratified** (brief §3): port the assignment for the **8/10 covered classes** — Barbarian→rage, Hoplite/Wildhunter→steady, Siege-Master→combo, Assassin→charge-stack, Duelist→rage-on-event/combo, Gunslinger→combo, Magus/Crusader-Banner→mana-default.
- The **two DEFERRED economies STAY DEFERRED** (Skirmisher damage-taken-converts, Crusader HP-economy) — the kernel doesn't implement them; building them is NOT recompose-first and is out of scope (gandalf).
- Likely touch points (verify first-hand): `season_generation_pipeline.py:213-218` (`_BC_TEMPO_TO_RESOURCE`), `bc_target_source.py:105-189` (energy_type→bc_target binding), `gear_generation.py` (carries the doc-48 vocabulary but does not author the authoritative energy_type today).

## Math-before-code (Discipline #1 — REQUIRED FIRST) + THE GUARD
Author a generation-seam math-note BEFORE the change. **Load-bearing guard (gandalf):** verify the **bc_target round-trip holds** when you swap the energy_type source from tempo-inferred → doc-48-assigned. The energy_type currently feeds `bc_target_source.py`'s energy_type→bc_target binding; changing the source must not break that binding. **If it cannot thread cleanly, STOP and re-escalate to KR** — do not force it.

## Cross-seam contract (Principle 6 / ADR-004)
Changing the authoritative `energy_type` source is a generation-side change that the simulation seam (gamora, Phases 1-2) CONSUMES. Coordinate: gamora's selector already branches on `energy_type` (full branch set built Phase 2) — confirm the value/vocabulary you emit matches what the selector + kernel `_ENERGY_CONFIGS` expect (the G1 mapping table is the contract). Write generation `MIGRATION.md` if any field/vocabulary crossing rocket→gamora/star-lord changes. Note the standing rocket-seam test drift (60 pre-existing failures: 5-element vs 7-substrate `season_emit`) — verify your change doesn't entangle with it; flag if it does.

## Measure / verify
- This phase changes the POPULATION, not the bands. Do NOT touch ENCOUNTER_COHORT_KPM_BAND or the production gate (the band refit is Phase 5, gamora+jack-ryan).
- Verify first-hand that the regenerated population carries the doc-48 economies (e.g., STR Barbarian configs now carry `energy_type=rage`, not mana-default) — affirmative + by-class, mirroring the rigor of the signature-ailment regen verification.
- Semantic-shift declaration (Discipline #12): the population's economy composition changes — declare it.

## Out of scope
- No new economy mechanic (the two DEFERRED economies stay deferred).
- No band refit (Phase 5).
- No magnitude re-tune.
- No simulation-seam edits (gamora owns the selector/pool; you own only the generation-side energy_type assignment).

## Hand-back chain after Phase R
1. rocket regenerates the population with doc-48 economies → jack-ryan Gate-2 (generation correctness + the bc_target round-trip guard + cross-seam contract).
2. **gamora re-arms G3b** (the deferred Phase-2 falsifier): verify the BUILT rage branch MATERIALIZES on a real rage entity — rage builds on swarm, spends on anchor — and distinct economies produce distinguishable tier-firing.
3. **Phase 5** composed re-baseline now refits against the FULL-economy population (the honest instrument) → Matt band approval.
4. **Phase 6** STR fires its real rage economy + bleed-spender lever against honest bands → gandalf rules O1-O4.

## Hand-back record
Append: tag, math-note path + the bc_target round-trip guard result, population-verification artifact (by-class economy emit), MIGRATION status, notes for jack-ryan Gate-2.
