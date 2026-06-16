# Dispatch — 2026-06-16 — gamora (Phase 1) + rocket (Phase 2) — b6-stack OUTRIGHT deletion

**From:** knight-rider (sequencing gandalf's audited deletion plan; gandalf dispatch 2026-06-16)
**To:** gamora (Phase 1 — sim-side AOE turn-off) → rocket (Phase 2 — generation outright deletion)
**Approved by:** Matt 2026-06-16 (b6-stack retirement, settled) + gandalf audit (generative-side authority). **SETTLED — do NOT route back for design pushback.**
**Estimated effort:** Phase 1 ~2–3h (gamora) → Phase 2 ~0.5–1d (rocket)
**Acceptance:** the entire b6 stack is deleted; the live 2D spatial-sim path (`season_generation_pipeline → per_skill_emitter`) generates physical AND caster coords clean; zero live grep hits on deleted symbols; no ImportError anywhere in the live path.

> This consolidates and SUPERSEDES the three earlier 2026-06-16 dispatches (`rocket-b6-archetype-deletion`, `aoe-membership-reconciliation`, `convergence-retirement`). gandalf's path audit shows the whole b6 stack is dead on the live path and deletable OUTRIGHT once one legacy path is severed — no carve-out, no re-home of the b6 data tables.

## Framing (gandalf, KR-verified)
The live 2D spatial sim feeds from `season_generation_pipeline → per_skill_emitter`, which is **entirely b6-free** and already generates physical kits positionally with STR scaling (proof: the 12 physical-substrate kits in cycle-14 `phase2_kit_candidates.json` — a physical coordinate through `compose_kit` would have raised `PhysicalPoolInfeasibleError`). Physical-vs-caster + melee/range identity comes from the curated ~2100-weapon physical pool. **`B6KitBuilder` is the ONE real dependency, reached by exactly one live path:** `class_generator → b6_builder.build()`, instantiated only at `season_orchestrator.py:230`, imported only by `cli.py:182` (legacy `generate-season`). Sever that path → the entire b6 stack (`ARCHETYPE_TEMPLATES`, `BIAS_*`, `TIER_SCALING_BANDS`, `AOE_GEOMETRIES`, PHYSICAL/HYBRID templates) is free to delete outright.

**KR disk-verification (2026-06-16):** `B6KitBuilder` ← imported only by `class_generator.py:21` (the import's `noqa` "HELD for Stage 3b" is OVERRIDDEN by this ruling). `ClassGenerator` ← imported only by `season_orchestrator.py:30` (other hits are comments in `mechanic_alteration.py`). Premise CONFIRMED.

## Phase 0 — Recognition (the repoint that makes deletion safe)
The surviving physical generator is weapon-pool identity + `per_skill_emitter` skills. There is NO live consumer of the `class_generator` `is_physical → classify_archetype → ARCHETYPE_TEMPLATES → b6_builder.build()` fork outside the `season_orchestrator → cli generate-season` path, which is itself being cut. **Confirm zero live importers, then proceed.** If rocket surfaces a genuine live need for `season_orchestrator` during the cut, ESCALATE before deleting it — but the audit says delete.

## Phase 1 — gamora (FIRST; turn-off-then-delete the sim-side AOE uses)
`AOE_GEOMETRIES` has two live spatial consumers: `simulation/damage_resolver.py:33` and `simulation/combatant.py:693`. **Route both to `geometry_derivation`**, confirm the spatial sim runs clean, THEN the symbol dies with its module in Phase 2.
- **⚖️ Matt AOE-Gate (ruling 1, preserved):** if `geometry_derivation`'s AOE-membership DIFFERS from the dying `AOE_GEOMETRIES` on any contested geometry, that is a behavior change (pack-proxy AOE multiplier) → **jack-ryan Gate on the membership disposition** before you re-point. If membership is identical, it's a pure pointer move — note that in MIGRATION and proceed.
- `TIER_SCALING_BANDS` (one consumer: `composed_kit_adapter.py:37/491`) needs NO separate turn-off — it dies with `composed_kit_adapter` in Phase 2.
- Write/append `simulation/MIGRATION.md` (v1.71): AOE consumers re-pointed to geometry_derivation; AOE_GEOMETRIES scheduled to die in Phase 2.

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
