# Dispatch — 2026-06-16 — gamora (Phase 1) + rocket (Phase 2) — b6-stack OUTRIGHT deletion

**From:** knight-rider (sequencing gandalf's audited deletion plan; gandalf dispatch 2026-06-16)
**To:** gamora (Phase 1 — sim-side AOE turn-off) → rocket (Phase 2 — generation outright deletion)
**Approved by:** Matt 2026-06-16 (b6-stack retirement, settled) + gandalf audit (generative-side authority). **SETTLED — do NOT route back for design pushback.**
**Estimated effort:** Phase 1 ~2–3h (gamora) → Phase 2 ~0.5–1d (rocket)
**Acceptance:** the entire b6 stack is deleted; the live 2D spatial-sim path (`season_generation_pipeline → per_skill_emitter`) generates physical AND caster coords clean; zero live grep hits on deleted symbols; no ImportError anywhere in the live path.

> This consolidates and SUPERSEDES the three earlier 2026-06-16 dispatches (`rocket-b6-archetype-deletion`, `aoe-membership-reconciliation`, `convergence-retirement`). gandalf's path audit shows the whole b6 stack is dead on the live path and deletable OUTRIGHT once one legacy path is severed — **with ONE exception: `AOE_GEOMETRIES` has 2 live sim-side survivor consumers and gets a verbatim re-home (Matt ruling A, 2026-06-16) before its module dies.** All other b6 data tables delete with no re-home.

## Framing (gandalf, KR-verified)
The live 2D spatial sim feeds from `season_generation_pipeline → per_skill_emitter`, which is **entirely b6-free** and already generates physical kits positionally with STR scaling (proof: the 12 physical-substrate kits in cycle-14 `phase2_kit_candidates.json` — a physical coordinate through `compose_kit` would have raised `PhysicalPoolInfeasibleError`). Physical-vs-caster + melee/range identity comes from the curated ~2100-weapon physical pool. **`B6KitBuilder` is the ONE real dependency, reached by exactly one live path:** `class_generator → b6_builder.build()`, instantiated only at `season_orchestrator.py:230`, imported only by `cli.py:182` (legacy `generate-season`). Sever that path → the entire b6 stack (`ARCHETYPE_TEMPLATES`, `BIAS_*`, `TIER_SCALING_BANDS`, `AOE_GEOMETRIES`, PHYSICAL/HYBRID templates) is free to delete outright.

**KR disk-verification (2026-06-16):** `B6KitBuilder` ← imported only by `class_generator.py:21` (the import's `noqa` "HELD for Stage 3b" is OVERRIDDEN by this ruling). `ClassGenerator` ← imported only by `season_orchestrator.py:30` (other hits are comments in `mechanic_alteration.py`). Premise CONFIRMED.

## Phase 0 — Recognition (the repoint that makes deletion safe)
The surviving physical generator is weapon-pool identity + `per_skill_emitter` skills. There is NO live consumer of the `class_generator` `is_physical → classify_archetype → ARCHETYPE_TEMPLATES → b6_builder.build()` fork outside the `season_orchestrator → cli generate-season` path, which is itself being cut. **Confirm zero live importers, then proceed.** If rocket surfaces a genuine live need for `season_orchestrator` during the cut, ESCALATE before deleting it — but the audit says delete.

## Phase 1 — VERBATIM RE-HOME (Matt ruling A, 2026-06-16; supersedes the original "route to geometry_derivation")

**Gate outcome (gamora 2026-06-16, engine `8ec4f8c`):** the original instruction assumed `geometry_derivation` already held a canonical AOE-membership — it does NOT. The closest spatial-derived membership DIFFERS from `AOE_GEOMETRIES` on 5 geometries (loses `dash_attack`/`ground_slam`/`leap_strike`/`multi_projectile` from the pack-proxy mult; gains `aura`). That is a deliberate B10/B11 pack-proxy classification, not a coarse spatial set. **Matt ruled (A): verbatim re-home, ZERO behavior change.** Tightening membership would be a separate deliberate balance decision (out of scope here).

`AOE_GEOMETRIES` is the SOLE survivor-consumed frozenset in `b6_archetype_templates.py` — the siblings (`GAP_CLOSER_/CLEAVE_/ESCAPE_MOBILITY_GEOMETRIES`, `ROTATING_ELEMENTS`) are consumed only by `b6_kit_builder.py` and die clean with it. Re-home scope = exactly one 16-entry frozenset.

**Phase 1a — rocket (FIRST):** create a surviving non-b6 home (e.g. `generation/geometry_constants.py`); move the **exact 16-entry `AOE_GEOMETRIES` frozenset intact** (no membership change); update the gen-side interim importer `b6_kit_builder.py:24` to the new home (keeps the engine runnable until Phase 2 deletes b6_kit_builder). Commit; write `generation/MIGRATION.md` noting the new home path.

**Phase 1b — gamora (SECOND):** re-point `simulation/damage_resolver.py:33` and `simulation/combatant.py:693` imports to the new home (read rocket's MIGRATION for the path). Confirm spatial sim green (27/27 baseline). Write `simulation/MIGRATION.md` **v1.72** (NOT v1.71 — that number is already taken by the Telegraph emit-contract entry): AOE consumers re-pointed to `<new home>`; membership IDENTICAL → zero behavior change; `AOE_GEOMETRIES` def now scheduled to die with `b6_archetype_templates.py` in Phase 2.

- `TIER_SCALING_BANDS` (one consumer: `composed_kit_adapter.py:37/491`) needs NO turn-off — it dies with `composed_kit_adapter` in Phase 2.

**Gate (Matt ruling): jack-ryan Gate-2 on the re-home commits** — two-witness: clean import + spatial-sim-green; membership identical (zero behavior change) confirmed by diff. This Gate clears BEFORE Phase 2 fires.

## Phase 2 — rocket (outright deletion)
**DELETE (whole modules):**
- `generation/b6_kit_builder.py` (B6KitBuilder)
- `generation/b6_archetype_templates.py` (ARCHETYPE_TEMPLATES, all BIAS_*, TIER_SCALING_BANDS, AOE_GEOMETRIES, PHYSICAL + HYBRID templates)
- `generation/legacy_archetype_shim.py` (G9 — zero live importers; gandalf resolves BC R-1: DELETE)
- `generation/class_generator.py` (physical fork + module; only instantiation was season_orchestrator:230)
- `generation/season_orchestrator.py` + `cli.py:182` generate-season wiring
- `generation/archetype_classifier.py` (classify_archetype:38, _derive_archetype_tag:84)
- `generation/archetype_composer.py`, `generation/stat_allocator.py`, `generation/composed_kit_adapter.py` (zero importers outside the legacy world once class_generator is gone)
- `simulation/balance_loop.py` convergence stack — **SUB-SYMBOLS ONLY (see guard below)**

**⚠️ KR SNAG — `SeasonOutput` cross-seam break (gandalf audit missed; MUST resolve before deleting season_orchestrator):**
`output/season_writer.py:16` and `output/summary_formatter.py:2` import `SeasonOutput` FROM `season_orchestrator`. These are **star-lord's LIVE output seam** — deleting `season_orchestrator.py` wholesale breaks them at import. Before deleting season_orchestrator: either **re-home `SeasonOutput`** (+ any sibling output types) to a surviving output/schema module and re-point the two star-lord imports, OR confirm with star-lord those two consumers are legacy-dying-too. **Cross-seam → coordinate with star-lord; do not leave a dangling import in star-lord's live path.**

## Guards — modules STAY, only dead sub-symbols go
- `generation/mechanic_alteration.py` — LIVE via `gauntlet_sim.py:1960` (`select_primary_t4`). Keep module; delete only G3 dead sub-symbols (`_geo_map`, `_bc_view_from_generation_params`).
- `generation/skill_tree.py` — LIVE via `season_generation_pipeline:968` (+ substrate_templates, t4_wireup, converge). Keep module; delete only the dead `_ARCHETYPE_TEMPLATES` dict (G10).
- **`simulation/balance_loop.py` — MODULE STAYS (KR add).** It has LIVE spatial importers: `spatial_gauntlet/gauntlet_archive.py`, `spatial_gauntlet/spatial_engine.py`, plus `validation_report.py`, `telemetry/recorder.py`. Delete ONLY the convergence/recompose sub-symbols (the `:2426` ARCHETYPE_TEMPLATES/BIAS/TIER_SCALING consumers + recompose machinery). The verification gate MUST prove these spatial importers don't reference the deleted convergence symbols — that empirical check is the arbiter of the gamora-"changes-convergence-for-every-class" vs gandalf-"vestigial" tension (both hold if the recompose loop only ever drove the legacy season_orchestrator path).

## Verification gate (jack-ryan or rocket self-check before close)
1. Run `gauntlet_sim` / `season_generation_pipeline` on a physical coord AND a caster coord → clean generation.
2. `grep` every deleted symbol name → zero live hits.
3. No `ImportError` anywhere in the live spatial-sim path (incl. star-lord output imports — see SeasonOutput snag).
4. **(KR add)** Confirm balance_loop's surviving spatial importers don't reference any deleted convergence symbol.
5. Stale `noqa` at `class_generator.py:21-22` disappears with the file — no follow-up.

## BC-cutover Stage-3 reconciliation (KR → Matt)
This deletion SUBSUMES BC-Stage-3's `legacy_archetype_shim` (R-1) + `ARCHETYPE_TEMPLATES` removal. BC-Stage-3's other targets (`ARCHETYPE_ROLE_PRIORITY`, `_PLAYER_CONTROLLER_ARCHETYPES`, V-D1..V-D6) should be checked against this surface — likely subsumed or made trivial. **BC-Stage-3 dispatch to be reconciled against this consolidated deletion (not run as a separate parallel delete).**

## Discipline
Turn off the use → confirm zero importers → delete. Never leave a dangling import in the live sim.

## Gate
Verification gate above → jack-ryan Gate-2 across the Phase 1 + Phase 2 commits (two-witness: clean physical+caster generation + spatial-sim-green). gandalf design-endorse NOT required for the deletion (settled); the audit IS the design witness.

---

## Completion record — Phase 1 (gamora, 2026-06-16)

**Status:** ⚖️ Matt AOE-Gate STOP — NO re-point performed. Surfaced to knight-rider for jack-ryan Gate on the membership disposition (per dispatch step 2: "If they DIFFER on any geometry … STOP and surface … this needs a jack-ryan Gate before you re-point. Do NOT silently absorb a membership change").

**Membership diff result — DIFFER (the key decision point):**
- `geometry_derivation.py` defines NO AOE-membership frozenset over the rich 24-type vocab. It owns `VALID_GEOMETRY_TYPES` (rich vocab) and `_RICH_TO_SPATIAL` (24→6 spatial enum) only. The dispatch's premise — that geometry_derivation is already a canonical AOE-membership source — does not hold on disk.
- Both sim consumers test `skill.geometry in AOE_GEOMETRIES` over the RICH vocab. The closest derivable membership (spatial in {circle,cone,line} = `layer2_dimensions.BURST_AOE_SPATIAL_GEOMETRIES`) **DIFFERS on 5 geometries:** LOSE pack-proxy mult + GEOMETRY_COLLAPSE = `dash_attack, ground_slam, leap_strike, multi_projectile`; GAIN = `aura`. (The looser {circle,cone} derivation differs on 10.) Dying `AOE_GEOMETRIES` = 16 entries.
- This is a behavior change to the B10.2 Model C pack-proxy AOE multiplier (`damage_resolver.py:459/:502`) and GEOMETRY_COLLAPSE ×1.5 (`combatant.py:697`) → affects win-rate vs `pack_proxy_size>0` defenders → feeds the convergence balance modifier. NOT a pure pointer move.

**Re-pointed:** NOTHING. The two consumers (`damage_resolver.py:33`, `combatant.py:693`) remain on `b6_archetype_templates.AOE_GEOMETRIES`, unchanged, pending Gate disposition.

**Recommendation carried to Gate:** verbatim re-home of the exact 16-entry frozenset to a surviving non-b6 module (`generation/geometry_constants.py` or `foundation/` — rocket's seam) = ZERO behavior change, b6 still dies in Phase 2. Re-confirms the v1.70 BLOCKING contract (`AOE_GEOMETRIES` must survive the b6 deletion). The spatial re-derivation is a SEPARATE deliberate balance change, out of scope for turn-off-then-delete.

**Spatial smoke (unchanged baseline):** `tests/test_spatial_gauntlet_scenarios.py` → 27 passed in 0.23s. Pack-proxy / AOE membership path intact (no change made).

**Artifacts:**
- Math note: `reincarnated-engine/src/reincarnated/simulation/math/b6stack-phase1-aoe-membership-gate-2026-06-16.md`
- MIGRATION: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.72 (NB: dispatch named v1.71, but v1.71 was already consumed by the Telegraph emit-contract entry; took next free number v1.72 — flagged to KR).
- Tag: `gamora/v1.1-b6stack-phase1-aoe-turnoff`

**Phase-2 (rocket) is BLOCKED on this Gate:** do NOT delete `b6_archetype_templates.py` until `AOE_GEOMETRIES` is re-homed per the Gate disposition and the two sim imports re-pointed.

---

## Completion record — Phase 1a (rocket, 2026-06-16)

**Status:** ✅ DONE — verbatim re-home complete. Engine fully runnable in the interim. Phase 1b (gamora sim re-point) is now unblocked.

**New home module:** `reincarnated-engine/src/reincarnated/generation/geometry_constants.py` (new, NON-b6, NOT slated for Phase-2 deletion).

**Frozenset moved — BYTE-IDENTICAL (16 entries, verbatim):** confirmed by smoke. All four import paths (`geometry_constants`, the `b6_archetype_templates` re-export, the `b6_kit_builder` gen importer, the `damage_resolver` sim consumer) resolve to the SAME frozenset OBJECT (`is`-identical, not merely `==`). Membership unchanged: `{cone, circle, line, melee_arc, ground_slam, ground_targeted_circle, beam_channel, whirlwind, dash_attack, leap_strike, chain_lightning, ricochet_bounce, vortex_pull, ring, multi_projectile, fork}`.

**Interim re-export approach chosen:** canonical definition lives in ONE place (`geometry_constants.py`); `b6_archetype_templates.py:385` does `from .geometry_constants import AOE_GEOMETRIES` (re-export, NOT a duplicated literal — drift is impossible). The OLD import path `b6_archetype_templates.AOE_GEOMETRIES` therefore keeps resolving until Phase 2 deletes the module. The two sim consumers were NOT touched — they stay green via the re-export until gamora re-points them in Phase 1b.

**Gen-side importer updated:** `b6_kit_builder.py:24` re-pointed to `from .geometry_constants import AOE_GEOMETRIES` (b6_kit_builder itself dies in Phase 2 but imports clean until then). Sibling frozensets (`GAP_CLOSER_/CLEAVE_/ESCAPE_MOBILITY_/PERSISTENT_GEOMETRIES`, `ROTATING_ELEMENTS`, `TIER_SCALING_BANDS`) NOT touched — they die clean with b6_kit_builder.

**Smoke:** import-path identity check (all 16, `is`-identical) PASS; `tests/test_spatial_gauntlet_scenarios.py` → 27 passed in 0.23s (matches gamora's pre-move baseline exactly — pack-proxy / AOE path intact).

**MIGRATION:** `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — entry `[2026-06-16] b6-stack deletion Phase 1a`.

**Commit / tag:** `b4a1c14` / `rocket/v1.1-b6stack-phase1a-aoe-rehome` (NOT pushed — Matt-gated).

**One thing the dispatch didn't list (surfaced, not a stop):** there is a THIRD `AOE_GEOMETRIES` importer the Phase-1a scope didn't name — `simulation/balance_loop.py:2426`, a function-local import inside `_lever_geometry_mix` (alongside `ARCHETYPE_TEMPLATES`, `BIAS_PREFERRED`, `BIAS_PENALIZED`). This is NOT a surviving path: it is exactly the convergence/recompose machinery the Phase-2 guard marks for deletion (`balance_loop.py:2426` is named in the guard). It resolves fine via the interim re-export and dies with the convergence sub-symbols in Phase 2. No re-point needed in Phase 1a/1b; flagging so gamora/jack-ryan are aware it exists. No genuine SURVIVING consumer beyond the two named sim imports was found.

---

## Completion record — Phase 1b (gamora, 2026-06-16)

**Status:** ✅ DONE — verbatim re-point complete. Pure pointer move, ZERO behavior change. Phase 1 (re-home) is now CLOSED pending jack-ryan Gate-2. Phase 2 (rocket outright deletion) is unblocked on the re-home contract.

**The two sim consumers re-pointed `b6_archetype_templates` → `generation/geometry_constants`:**
- `simulation/damage_resolver.py:33` (module-level import; used at :459, :502 — B10.2 Model-C pack-proxy AOE multiplier).
- `simulation/combatant.py:693` (function-local import; used at :697 — GEOMETRY_COLLAPSE ×1.5). Stale comment at `:692` updated to name the new home.

**Membership-identity check (the load-bearing proof — ZERO behavior change):**
- new home (`geometry_constants.AOE_GEOMETRIES`) has exactly **16 entries**; `==` the known 16-entry set; symmetric-diff vs the known set is **empty**.
- the object `damage_resolver` now binds is **`is`-identical** to `geometry_constants.AOE_GEOMETRIES`.
- `geometry_constants.AOE_GEOMETRIES is b6_archetype_templates.AOE_GEOMETRIES` (rocket's re-export → SAME object), so the `combatant` function-local binding is identical by construction.
- The pack-proxy AOE multiplier + GEOMETRY_COLLAPSE ×1.5 paths are byte-for-byte unchanged.

**NOT touched (per dispatch step 3):** `balance_loop.py:2426` convergence/recompose import — out of Phase-1b scope; dies in Phase 2; resolves via the interim shim until then. Confirmed it still imports from `b6_archetype_templates` (intended).

**Spatial smoke:** `tests/test_spatial_gauntlet_scenarios.py` → **27 passed** (matches the established baseline exactly; pack-proxy / AOE-membership path intact).

**Artifacts:**
- MIGRATION: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.72 (Phase-1b resolution section appended; header updated Gate-STOP → ruling-A → re-point-done).
- Commit / tag: `6128e50` / `gamora/v1.1-b6stack-phase1b-aoe-repoint` (NOT pushed — Matt-gated).

**Phase 1 CLOSE:** both sim imports point at `geometry_constants`; membership identical; spatial-green. Ready for jack-ryan Gate-2 (clean import + spatial-green + membership-identical) → then rocket fires Phase 2. The `AOE_GEOMETRIES` def + its re-export shim at `b6_archetype_templates.py` die with the module in Phase 2.
