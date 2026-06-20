# Finding — 2026-06-20 — gamora-phase1-resource-economy-wiring

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no BLOCK, no WARN)
**Target:** tag `gamora/v-resource-economy-phase1-1` (commit `c28d027`)
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam), 4 (decisions-log/spec), 6 (cross-seam round-trip); Disciplines #1, #2, #3, #12; Principle 6 / V-gate empirical inspection

## What I found

Gamora's Phase-1 resource-economy wiring is a faithful recompose-first port: the kernel `_ENERGY_CONFIGS` energy_type branch is read (not rebuilt) from the production `CombatantState`, a selector gate (`energy >= effective_cost`) and a cast-site decrement are added behind the `WIRE_RESOURCE_ECONOMY` flag, and the harness seed-stride overflow is fixed. I verified every Gate-2 focus item first-hand on disk rather than on report (Principle 6). The smoke runs ALL PASS for me locally; the gate binds in isolation (energy=0/cost=40 → `None`) and is genuinely inert when the flag is OFF (energy=0 → still fires, byte-identical legacy). The G2 self-assessment "KPM FLAT (gate ON==OFF)" is correct and is NOT a wiring defect — the gate is unit-verified and only lacks an occasion to bind because the rotation still collapses to the regen-positive T1 skill (the SESSION-31 T1-only-firing defect Phase 2 addresses). No mechanism, discipline, or regression issue found.

### First-hand evidence per focus item

- **Mechanism correctness (gate + decrement + kernel-pool port):** Diff at `spatial_engine.py:1046-1052` adds the energy gate inside `skill_ready` behind the flag; decrement present at both cast sites (`:1657` player, `:1755` mob); kernel pool mirrored at the entity builders (`:2078+`, `:2197+`) reading `combatant_state.mana/max_mana/mana_regen/energy_type`. Kernel `_ENERGY_CONFIGS` confirmed = exactly the 5 economies the brief names (`rage, combo, focus, stamina-as-resource, charge-stack`). Recompose-first held — no new mechanic; the branch lives in the kernel, the entity now READS it.
- **No-regression guard / V-gate (flag OFF == byte-identical legacy):** Verified directly. With `WIRE_RESOURCE_ECONOMY=False`, an entity at energy=0 against a cost-40 skill STILL fires (selector index 0) — the pool is never consulted, identical to pre-Phase-1. With the flag ON the same case gates to `None`. Projection/smoke path (no `player_class`) keeps legacy `100/100/10/"mana"`; production path reads the kernel pool (130/130/5.2). Both confirmed.
- **Semantic-shift declaration (Discipline #12):** Declared in math-note §7 and MIGRATION v1.78 §"Semantic shift" — KPM moves from "throughput under unlimited resources" to "throughput under a resource budget," with the Phase-1 caveat that the measured magnitude is mana-throttle-only (population scope). Routed to me for the cross-boundary continuity record.
- **Seed hygiene (Discipline #3):** Overflow genuinely fixed. Old `kit*1000 + enc*100` collides at enc≥10 (enc 10 = 1000 = kit stride); new `kit*100_000 + enc*1_000 + cohort` has enc max 17000 < 100000 — disjoint. Fresh base `820000` is disjoint from used `[700000,766703]` and `[619000,684303]`; span recorded (7,337,003), Phase-2 reserved ≥8,000,000.
- **No production-gate regression (measure-isolated):** `ENCOUNTER_COHORT_KPM_BAND` and `SPATIAL_ENCOUNTER_KPM_BAND` live in `gauntlet_sim.py:206/371` — that file is NOT in the commit's file list. Bands untouched. Measure-isolated discipline held.
- **Cross-seam (Principle 6 / ADR-004):** All 7 touched files are within the gamora simulation seam. No telemetry/export/recorder file touched. The `energy_type` already persisted in `recorder.py` is the pre-existing `PlayerClass.energy_type`, distinct from the new engine-internal `SpatialEntity.energy_type` (unpersisted, additive-defaulted). No gamora→star-lord schema change; no MIGRATION hand-off required. Round-trip: not applicable because the change is internal-to-seam with no inter-seam dict/schema field added.
- **Smoke-gate (Principle 2):** Commit message carries the smoke-line (path + ALL PASS + 586/586 regression). Verified the line and re-ran the smoke first-hand.

## Rationale

Principle 1 satisfied (math-note `resource-economy-wiring-phase1-2026-06-20.md` precedes code, code-cited per Discipline #1.2). Principle 2 satisfied (smoke-line present; re-run PASS). Principle 3 / Principle 6 satisfied (internal-to-seam; cross-seam null-status explicitly noted per dispatch). Principle 4 satisfied (wiring conforms to the brief's recompose-first/port mandate; G1 pre-ratified mapping not re-litigated). Discipline #3 (seed hygiene) and #12 (semantic-shift) both met. No principle or discipline is at risk. The "KPM FLAT" outcome falls inside the pre-registered G2 auto-resolve branch (flat-not-rising + no starvation), which is gandalf/KR's gate, not mine — my gate is the wiring mechanics, which are correct.

## INFO items (for the record; non-blocking)

- **INFO-1 (Phase-3 dependency surfaced, not a Phase-1 defect):** The G1 population scope-surprise gamora documented (math-note §3) is real and correctly routed — the measure-isolated population carries BC-tempo-inferred `{cooldown, energy, mana}`, all resolving to mana-default, so no kernel/doc-48 build-spend economy (incl. Barbarian-rage) reaches the spatial layer. This is a rocket generation-seam matter and a Matt scope call per the workstream, NOT a gamora wiring matter. Recording it here only so the Phase-5 composed re-baseline (my structural Gate-6) inherits the note: if the population still lacks the doc-48 economies at Phase 5, the composed instrument measures mana-default-only for the resource axis, and the band refit must declare that scope.
- **INFO-2 (mob decrement is harmless-but-untested in-fight):** The mob cast-site decrement (`:1755`) is symmetric and flag-gated, correct for loop uniformity. The smoke unit-tests the player gate, not the mob gate; mobs carry the flat pool on the projection path so this is benign. No action — noted only so a future phase that gates mob economies knows the mob path has no dedicated assertion yet.

## Action

- [x] Developer (gamora): none required — Phase 1 wiring PASSES Gate-2. Proceed to Phase 2 (rotation selector) per the brief's 1→2 dependency; the `energy_type` branch is built cleanly so the gate will bind once expensive tiers fire.
- [ ] Matt: no decision needed for THIS gate. (The G1 population scope-surprise + the "KPM-flat auto-resolve" are gandalf+Matt/KR routing per the brief's pre-registration, independent of this structural Gate-2.)

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (gate `:1046-1052`; decrement `:1657`/`:1755`; entity-builder kernel-pool mirror `:2078+`/`:2197+`; flag `WIRE_RESOURCE_ECONOMY`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_resolver_adapter.py:192` (adapter comment correction; `mana=1e9` retained)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/str_9pass_floor_all18_harness_2026_06_19.py` (seed-stride fix; base 820000)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/resource-economy-wiring-phase1-2026-06-20.md` (math-note, the gate)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.78 (cross-seam null-status + semantic-shift)
- `~/Games/reincarnated-engine/scripts/gamora_phase1_resource_economy_smoke_2026_06_20.py` (smoke; re-run ALL PASS first-hand)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:206/371` (bands — confirmed UNTOUCHED)
- Brief: `agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` §3 (G1/G2)
- Dispatch: `agentic_orchestration/dispatches/2026-06-20-gamora-phase1-resource-economy-wiring.md`
