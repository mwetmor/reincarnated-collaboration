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

---

## Completion record — rocket — 2026-06-20

**Status:** COMPLETE. Both guards held; neither tripped; no escalation required. Recompose-first PORT; no new mechanic; the two DEFERRED economies stayed deferred.

**Tag:** `rocket/v-phaseR-reference-economy-hardening-1` (engine repo).

**Math-note (Discipline #1, authored BEFORE code):**
`reincarnated-engine/src/reincarnated/generation/math/2026-06-20-phaseR-reference-economy-hardening-math.md`

**The population→kit-type KEY (GUARD #1 — design-side):**
The population is built bottom-up on BC cells (`class_archetype=element`; NO doc-48 class field). The KEY = doc-48's own `(bc_attribute, bc_range, bc_tempo, bc_amplitude)` signature, which is **COLLISION-FREE within doc-48** (proven: collisions exist only at coarser keys — `(attr,range,tempo)` collides DEX-melee-high charge-stack-vs-stamina = Assassin vs Wildhunter — and are resolved by `amplitude`, doc-48's OWN discriminator). Off-grid population cells (only 3/18 exactly match a doc-48 class coordinate) fall back to doc-48's within-attribute discriminator: STR by range (melee→rage / mid→stamina / ranged→combo); DEX by range then melee-amplitude (ranged→combo / mid→rage / melee&spiky→charge-stack / melee&flat→stamina / melee-other→mana); INT→mana; WIS→mana. Single-valued, zero per-cell ambiguity → **DESIGN TRIP-WIRE did NOT trip** (no two economies in one population bucket); no gandalf escalation. Implemented as `_assign_doc48_economy()` + the `_DOC48_ECONOMY_BY_BC` exact-signature table in `season_generation_pipeline.py`.

**bc_target round-trip guard result (GUARD #2 — technical-side): HOLDS.**
The harness path (`season_generation_pipeline.py`) does NOT call `bc_target_from_generation_params` — verified zero `bc_target`/`econ_bin`/`cost_type` references in the harness pipeline. The `energy_type→bc_target` binding (`bc_target_source.py:105-197`) lives in a SEPARATE seam (production season_orchestrator/class_generator). My edit is confined to the harness `resource_model` source (4 call sites) + touches no shared bc_target code → the production round-trip is untouched and holds by construction. Emitted vocab `{rage,combo,stamina-as-resource,charge-stack,mana}` is fully kernel `_ENERGY_CONFIGS`-consumable. (One note: `charge-stack` ∈ kernel configs but ∉ `bc_target_source._ENERGY_ECON`; no current population cell emits it — requires a DEX-melee-spiky cell, absent from the 18-cell catalog — so inert for the harness; flagged in MIGRATION for the production seam owner.) **No round-trip failure → no KR re-escalation.**

**By-class population-verification artifact (first-hand, affirmative):**
Generated the real 54-kit harness population (`w5r1_generate_kit_candidates(seed_base=14001)`) and inspected each kit's `resource_model` AND the `_build_real_player_class(kit).energy_type` round-trip:
- **STR: {rage: 9, combo: 3}** — all 9 STR-melee kits carry `energy_type=rage` (physical element). **The Barbarian-rage lever materializes on the population** (Phase-6 hinge satisfied).
- **DEX: {stamina-as-resource: 3, combo: 6, rage: 3}** — multi-economy (G3b distinguishability satisfied).
- **INT: {mana: 15}; WIS: {mana: 15}** (Magus overflow→mana; Crusader HP-economy DEFER→mana).
- Full 54-kit distribution: **rage:12 / combo:9 / stamina-as-resource:3 / mana:30** (matches math-note §3 prediction exactly).
- PlayerClass round-trip: **0/54 mismatches** — energy_type faithfully carried to the kernel-consumed `PlayerClass`.
- Smoke: `scripts/rocket_phaseR_economy_smoke_2026_06_20.py` — ALL PASS.

**Semantic-shift declaration (Discipline #12):** the population's economy composition changes from **100% mana-default** → rage:12/combo:9/stamina:3/mana:30. Every KPM/DPS field on this population now reflects the kit's real economy rhythm, not uniform mana-default. Pre-Phase-R and post-Phase-R KPM are DIFFERENT instruments — Phase 5's ONE band refit fits the post-Phase-R composed instrument.

**MIGRATION status:** WRITTEN — `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` [2026-06-20] Phase R entry. Value/vocabulary shift on existing `energy_type`/`resource_model` (NO new field). Consumers: gamora (selector + kernel already branch on energy_type — **NO gamora code change required**; the contract is the value, which now matches the kernel `_ENERGY_CONFIGS` it already expects); star-lord (verbatim passthrough; value set widens). bc_target round-trip note + standing-drift non-entanglement documented.

**Notes for jack-ryan Gate-2:**
1. **Mechanism correctness:** `_assign_doc48_economy` PORTs the LOCKED G1 table (doc 48 §3.1); collision-free key proven in math-note §1; the DEFERRED economies stay deferred (→mana). Exact-match precedence + within-attr fallback are both single-valued.
2. **bc_target round-trip:** harness path does not feed bc_target; production seam untouched. Verify the grep claim (zero bc_target refs in `season_generation_pipeline.py`) if desired.
3. **Cross-seam contract:** the emitted energy_type vocabulary matches kernel `_ENERGY_CONFIGS` + gamora's selector; G1 table is the contract; MIGRATION written.
4. **Semantic-shift continuity:** declared at the population boundary (Discipline #12).
5. **Seed hygiene:** verification used seed_base=14001 (the Cycle-14 Wave-5 production seed); no fresh-seed requirement for a population-composition change (no sim run in Phase R).
6. **Standing test drift:** full suite 60 failed / 4755 passed = the documented 60 (foundation 5-vs-7 `season_emit`; cycle13 gauntlet; LLM auth). ZERO economy/resource/energy failures — not entangled. Verified.
7. **No production-gate / band touch:** Phase R changes the POPULATION only; ENCOUNTER_COHORT_KPM_BAND + the production gate UNTOUCHED (band refit is Phase 5).

**NOT pushed** (Matt-gated, ADR-006). Files committed under tag `rocket/v-phaseR-reference-economy-hardening-1`.
