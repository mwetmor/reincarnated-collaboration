# Dispatch — 2026-07-12 — rocket — geometry rename `chain_lightning` → `chain` (Unit 1 / Wave 1)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt ruling 2026-07-12 (geo-prep §5 G0); relayed via gandalf KR brief `agentic_orchestration/gandalf/briefs/2026-07-12-kr-engine-renames-and-ice-element.md`
**Pattern:** B (multi-hour; own session memory; census + read-compat + registry regen)
**Estimated effort:** half-day
**Acceptance:** grep for `chain_lightning` in LIVE code paths returns only the read-compat alias + historical-artifact references; tests green; registry sidecar regenerated. Tag `rocket/v2.6-chain-geometry-rename-1` (seam-prefixed, intermediate).

## Context

The geometry type `chain_lightning` predates the 8-element layer. Its name wrongly welds a geometry to one element — under the free-axis law a corpus `chain` kit can be ANY element. Matt ruled (verbatim): *"For chain, we can map to chain_lightning, but we will need to change the engine's type name to chain as we go."* This is a hygiene rename: the geometry identity becomes `chain`; the old string `chain_lightning` survives only as a read-compat alias for historical artifacts.

## Binding laws (from the KR brief — non-negotiable)

1. **Census-first.** Open with a full-repo grep census of `chain_lightning` (src + config + tests + data artifacts) BEFORE any edit. The surfaces below are anchors, not an exhaustive list — the census is authoritative.
2. **Historical artifacts immutable.** Emitted kits (`data/kit_space/kits/*.json`), telemetry rows, `output/` bundles, past-season data keep `chain_lightning` as provenance. The rename lands at **load boundaries** (read-compat normalizer: `chain_lightning` accepted on read → normalized to `chain`) + **emit paths** (write `chain` going forward). Regen-able artifacts regen at next emission; NEVER retro-edit kit files.
3. **MIGRATION.md entry** (ADR-004 / Discipline #12 semantic-shift documentation) — document the alias, the load-boundary normalization point, and the emit-path change.
4. **Gate-2 (jack-ryan)** before tag.
5. **Auto-commit, no push** (Matt-gated per CLAUDE.md team discipline).
6. **No scope creep:** rename only. No new geometry types, no palette re-ordering beyond the string swap, no derivation-logic change. Design questions that surface route back to gandalf via KR.

## Path note

All live code is under `src/reincarnated/` (e.g. `src/reincarnated/generation/geometry_constants.py`). There is a decoy top-level `./simulation` (an `output/` dir only) — ignore it. Target `src/reincarnated/...` exclusively.

## Known surfaces (anchors — verify against census)

- **generation:** `geometry_constants.py` (16-type palette tuple, ~line 26) · `geometry_derivation.py` · consumers: `bc_target_source`, `gear_instance_generator`, `proxy_vocabulary_bridge`, `bc_target_composer`, `weapon_envelope_composer`, `per_skill_emitter`, `ability_grammar`
- **simulation:** `damage_resolver.py` · `spatial_gauntlet/spatial_engine.py` + `spatial_resolver_adapter.py` (⚠ E4 overlap — Gate-1-VERIFIED BENIGN: the two `chain_lightning` sites in `spatial_engine.py` are **lines 131 and 434, static geometry→shape lookup-dict entries — NOT E4 cast-state logic**. E4 PHASE-2 is live-but-Gate-2-held at HEAD `785956c`; these dict-literal sites are provably non-entangled. Confirm those two lines are still dict entries, edit only them, do not touch E4 cast-state code. If the census surfaces a `chain_lightning` site OUTSIDE lines 131/434 that sits inside cast-state logic, flag to KR before editing.)
- **canonical sidecar:** `canonical/sidecars/emit_substrate_registry.py` → **regen** `atomic_substrate_registry_v1.json`
- **config:** `substrate_identities/lightning.yaml` (PREFER list) + `holy.yaml` (AVOID list)
- **tests:** 3 test files (per brief) — verify count against census
- **persisted (do NOT rewrite):** `data/kit_space/kits/*.json` carry `chain_lightning` → read-compat normalizer handles these on load

## Read-compat normalizer

Place the alias at the geometry-load boundary (wherever a persisted geometry string enters live code). One normalization point preferred; document it in MIGRATION.md. `chain_lightning` → `chain` on read. Emit `chain` forward.

## Required reading before starting

- This dispatch + the KR brief §Unit 1
- `generation/geometry_constants.py` (current palette tuple)
- `canonical/sidecars/emit_substrate_registry.py` (registry regen procedure)
- Discipline #12 (semantic-shift documentation) at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

## Math-before-code

N/A — pure identifier rename, no numeric/behavioral change. Smoke-test discipline still applies: run the generation smoke after the rename to prove zero behavioral drift (a `chain` kit must generate/resolve byte-identically to a pre-rename `chain_lightning` kit of the same seed, modulo the string).

## Cross-seam contract change? (Principle 6 gate)

**YES — geometry-string identity crosses generation → simulation → registry sidecar.** MIGRATION.md required. The read-compat normalizer means simulation and the registry read the same normalized `chain`; no schema field is added/removed. Flag the `spatial_engine.py` E4 overlap to KR if the string sites are entangled with held E4 code.

## Out of scope

- Any change to the other 15 geometry types
- Any derivation-logic or palette-weight change
- Rewriting persisted kit files (Law 2)
- Element-pool or free-axis rebalancing

## Completion record

**Completed:** 2026-07-12 by rocket. **Commit:** `5a6e0c4`. **Tag:** `rocket/v2.6-chain-geometry-rename-1` (created, NOT pushed — KR owns wave push). **Engine repo HEAD before:** `785956c` (E4 PHASE-2 held).

### Census result (full-repo grep, authoritative)

- **Persisted kits** `data/kit_space/kits/*.json`: ~200 files carrying `geometry_type: "chain_lightning"` — **UNTOUCHED (Law 2)**; read-compat normalizer handles on load.
- **Persisted data** `data/synergy_priors/v1_co_occurrence_priors.json`: 1 methodology-string occurrence — **UNTOUCHED** (provenance).
- **Live code renamed to `chain`:** 22 files (generation 9, simulation 3, config 2, canonical/registry 2, foundation 1, tests 3, + MIGRATION.md + AGENT_STATE.md). Full emit-path + canonical-vocab-set list in `generation/MIGRATION.md` [2026-07-12].
- **Correctly EXCLUDED (distinct identifiers):** `gear_instance_generator.py chain_lightning_on_hit` (legendary gear-affix capability, NOT the geometry — has concrete "Chains lightning to nearest enemy" flavor); registry skill-tree `chain_architecture`/`chain_position`/`chain_role` family (kit skill-chains, a wholly different concept).
- **Remaining `chain_lightning` occurrences in live code (all intentional):** the 2 alias-map definitions (`geometry_derivation.py`, `spatial_engine.py` local mirror) + documenting comments/docstrings/registry-notes. Verified via re-census.

### E4 overlap confirmation (Gate-1-verified BENIGN — held)

`spatial_engine.py` lines 131 & 434 confirmed still **static geometry-string → shape lookup-dict entries** (dict keys mapping to `"line"`), NOT E4 cast-state logic. Edited ONLY those two dict keys. **No `chain_lightning` site was found outside 131/434 inside cast-state logic.** No E4 PHASE-2 code touched; held build unentangled.

### Read-compat normalizer location (single source of truth)

`src/reincarnated/generation/geometry_derivation.py` — `_GEOMETRY_ALIASES = {"chain_lightning": "chain"}` + `normalize_geometry_type(s) -> str | None` (idempotent; `None`→`None`). Applied at 3 load boundaries: `spatial_resolver_adapter._resolver_skill_from_dict` (sim damage path), `spatial_engine._determine_geometry_type` (local import-free mirror, hot-path discipline), `court_persistence._row_to_court_form` (foundation seam). Emit paths write canonical `chain` directly.

### Registry regen confirmation

`python3 -m reincarnated.canonical.sidecars.emit_substrate_registry` → **EMIT PASS** (schema_version 1.0.0, family_count 20, all acceptance criteria pass). `src/reincarnated/canonical/sidecars/atomic_substrate_registry_v1.json` regenerated; primitive_id now `chain` (line 244). NOTE: emitter stamps a fresh `emission_timestamp` (non-deterministic) — expected in the diff alongside the primitive rename.

### Smoke result (Discipline #2, LLM-free, zero behavioral drift)

- `scripts/rocket_geometry_axis_e1_smoke_2026_07_08.py` → **VERDICT PASS**. int/wis kits now emit **`chain`** (was `chain_lightning`); same distinct-geometry counts (12/11/11/12, min 11 ≥ N=6); same B11 multipliers fire (fork 2.2, multi_projectile 2.6, ricochet_bounce 2.533, leap_strike 1.3, ring 1.2). Emitted geometry → `_RICH_TO_SPATIAL` → spatial class → B11 fires. No sim contract change.
- Inline zero-drift harness: normalizer idempotent + `None`-passthrough; `derive_geometry_type(area_damage, lightning) == "chain"`; **read-compat** persisted `chain_lightning` → `chain` mult **2.533× == fresh `chain` mult**; **drift-guard** bare un-normalized `chain_lightning` → 1.0 (proves the load-boundary normalizer is load-bearing).
- Tests: `test_b11_geometry_mechanics` + `test_b11_geometry_palette` + `test_substrate_identity_loader` → **283 passed**. 2 fails are PRE-EXISTING and UNRELATED (`TestFoundationIntegration` asserts 4 rotating / 5 total elements; config now has 7/8 from the 8-element layer — RED identically on clean tree; not caused by this work).
- All 12 touched modules import clean (no circular import from the new foundation→geometry_derivation edge).

### MIGRATION.md path

`src/reincarnated/generation/MIGRATION.md` — entry `[2026-07-12] GEOMETRY RENAME chain_lightning → chain`. Documents the alias, the 3-site load-boundary inventory, the emit-path swap, Law-2 immutables, and the downstream-consumer reader-update note.

### Notes for jack-ryan Gate-2

1. **CROSS-SEAM reader dependency (drax's `reincarnated-demo/`).** The demo has `chain_lightning` VFX/HUD consumers: `src/abilities/vfx.ts` switch cases on `'chain_lightning'`; `src/ui/combatHud.ts:131` ALREADY forward-compat (handles both `'chain'` and `'chain_lightning'`); `src/main.ts:980` + `src/types/engine.ts` type union. **Exported season JSON now emits `chain`**; persisted kits still carry `chain_lightning` until regenerated. This is NOT rocket's seam to edit — flagged in MIGRATION downstream note as a drax/KR coordination item. Gate-2 should route this to drax so the demo VFX switch accepts `chain` (or normalizes on read).
2. **Config affinity keys renamed but currently unconsumed.** `geometry_affinities` in `lightning.yaml`/`holy.yaml` is validated by the substrate-identity loader but has NO live consumer that looks it up by canonical geometry name (grep-proven: zero `.geometry_affinities` lookups outside loader + test). Renaming `chain_lightning`→`chain` there is forward-consistency with zero behavioral effect; the asserting test was updated.
3. **Spine untouched.** No balance constant / distribution weight / scaling factor changed (math-before-code N/A per dispatch — pure rename). Damage-multiplier fan-out math byte-identical (proven: 2.533× before == after).
4. **`bc_target_source.py:172`** `geo_bin = "chain"` was ALREADY the BC-axis damage-geometry bin name `chain` (a separate namespace from geometry_type); left as-is, only the adjacent comment updated. Not a rename site.
