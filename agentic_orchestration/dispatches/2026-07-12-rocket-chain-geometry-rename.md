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
_(append on completion: census result, normalizer location, registry regen confirmation, smoke result, MIGRATION.md path, tag, notes for jack-ryan Gate-2)_
