# Dispatch — 2026-07-12 — rocket (LEAD) — element `water` → `ice` + cold/frost register (Unit 3 / Wave 2)

**From:** knight-rider
**To:** rocket (LEAD); gamora + star-lord sub-dispatches (same date, this directory) serialize behind the rocket config pivot
**Approved by:** Matt ruling 2026-07-12 (elem-prep §6 EL2; corpus-rekey-spec-v1.md §2 + §5 rows 1c/1d); relayed via gandalf KR brief
**Pattern:** B (multi-hour, multi-seam; own session memory)
**Estimated effort:** 1–2 days across three seams
**Acceptance (rocket half):** live generation/element/anchor/foundation/canonical/config code + config speak `ice` (SUBSTRATE-element layer ONLY — see ⚠ Discipline #14 exclusion below); read-compat normalizer RULE at the element load boundary (`water` → `ice`); historical artifacts untouched; rocket-owned tests green (count is an estimate — don't gate on it); MIGRATION.md documents the semantic shift + INT-pool reading + the #14 layer distinction. Tag `rocket/v2.7-water-to-ice-element-1`.

## Path note

All live code is under `src/reincarnated/` (e.g. `src/reincarnated/config/elements.yaml`, `src/reincarnated/element/selector.py`). A decoy top-level `./simulation` (`output/` only) exists — ignore it. Target `src/reincarnated/...` exclusively.

## ⚠⚠ BLOCK-CLASS — Discipline #14 layer exclusion (Gate-1 finding — READ BEFORE ANY EDIT)

`water` lives in TWO distinct layers that share the bare token. The census MUST classify each hit into one of these before editing:

- **SUBSTRATE-ELEMENT (display) layer — RENAME to `ice`:** `config/elements.yaml name: water`, `STAT_ELEMENT_POOLS`, `_ALL_8_ELEMENTS`, `resistance_matrix` element KEY (value/coefficients unchanged), telemetry/export element VALUE, generation element literals, substrate-identity file.
- **CANONICAL-FOUR SLOT-ROUTING layer — DO NOT RENAME:** `element/selector.py` `VALID_SLOTS = ("fire","wind","water","earth")`, the `water_slot` / `water_sel` JSON protocol keys (~13 bare `water` tokens in `selector.py` alone), `element/schema.py water_slot`. Per **Discipline #14** these are internal routing keys, deliberately decoupled from the generative/display layer, and `water_slot` is a **structural key in emitted kits** — renaming it violates Law 2 (historical immutability) AND breaks live schema.

**Rule:** rename the substrate-element (display) `water` ONLY. The census MUST tag each hit substrate-layer (rename) vs canonical-four-slot (leave). If a hit is ambiguous, route it to gandalf via KR — do NOT guess.

## Context — this is a DESIGN change, not hygiene

Matt ruled (verbatim): *"let's change our water element to Ice and adopt the cold/frost ailment. The genre's corpus has spoken."* Corpus evidence (legolas mega-probe): **38 cold/frost kits, zero "water" kits** — RDR's "water" was the genre-outlier name. The locked-8 amends substrate-led to: **fire · ice · earth · wind · lightning · holy · shadow · physical**.

The mechanic does NOT change: `chill` (soft_control slow, 20–50%) already IS the genre's cold/frost ailment. EL2's "adoption" lands as a **register confirmation**, not a new mechanic. No freeze-as-hard-control here (that routes to gandalf's ailment-layer queue — OUT of scope).

## Binding laws (from the KR brief — non-negotiable)

1. **Census-first.** Full-repo grep census of `"water"` (src + config + tests + data) BEFORE any edit. Brief estimates ~114 src literals + 58 test files + config; the census is authoritative, not these counts.
2. **Historical artifacts immutable.** Emitted kits, telemetry rows, `output/` bundles, past-season data keep `water` as provenance. Rename lands at **load boundaries** (read-compat normalizer: `water` → `ice` on read) + **emit paths** (write `ice` forward). NEVER retro-edit persisted artifacts. (Matt's free-axis aside: *"if we run enough iterations across time, we will see these kits in their Ice Elemental version"* — regen, don't retro-pin.)
3. **MIGRATION.md** per seam (ADR-004 / Discipline #12).
4. **Gate-2 (jack-ryan)** on the unit before tag. **gandalf reviews the register surfaces** (elements.yaml prose, theme_tags, substrate-identity content) BEFORE Gate-2 — route those surfaces back through KR to gandalf.
5. **Auto-commit, no push.**
6. **No scope creep:** no ailment-parameter change, no resistance-value change, no pool-probability change, no freeze-mechanic design. Rename + register pass only.

## rocket scope (LEAD — owns the pivot + normalizer)

**The config pivot is the serialization anchor — land it first; gamora/star-lord sub-dispatches read from it.**

1. **`config/elements.yaml`** water entry → `name: ice`, `display: Ice`. **`ailment: chill` UNCHANGED.** Description / `theme_tags` re-register: propose `[cold, preservation, stillness]` (preservation carries over from water; `flow`/`depth` retire). `color_range [560000, 700000]` (blue band) **KEEPS** — ice-coherent. ⚑ These prose/tag surfaces are gandalf-review-before-Gate-2 — draft them, then hold for gandalf via KR.
2. **`config/substrate_identities/water.yaml` → `ice.yaml`** — file rename + identity-declaration content pass; PREFER/AVOID lists re-read under the ice register. ⚑ gandalf-review surface.
3. **`config/ailments.yaml`** chill entry: **description pass only** — re-register as the cold/frost ailment ("chill/freeze register"). **Parameters untouched.**
4. **`generation/season_generation_pipeline.py::STAT_ELEMENT_POOLS`:** INT pool → `["fire", "ice", "lightning", "shadow"]` (the classic mage quartet — Matt-noted). DEX 8-pool + `_ALL_8_ELEMENTS` likewise get `water`→`ice`.
5. **generation / element / anchor / foundation / canonical** literals: `water` → `ice` per census (brief: generation 23 · foundation 3 · element 2 · canonical 1). `element/schema.py` + `element/selector.py` included.
6. **Read-compat normalizer — ONE RULE, N boundaries.** Author a single normalization RULE (`water` → `ice` on read) in `element/MIGRATION.md` as the shared contract. The three seams have genuinely different load boundaries (element-load / fight-log+telemetry read / export-bundle read) and will each APPLY the rule at their own boundary — this is not necessarily one shared imported function. Document the rule precisely so gamora/star-lord apply it identically. `element/MIGRATION.md` already exists as the shared-contract home.
7. **rocket-owned tests** in the census that touch generation/element SUBSTRATE literals — update to `ice`. Do NOT touch tests that assert on the canonical-four `water_slot`/`VALID_SLOTS` layer (#14).

## Element-name vocab pools (data-side, small, NON-blocking)

D1 pools carry `element=water` rows → re-register to `ice`. **Queue for the report, do not block:** `rime` re-promotion — demoted vocab-obscure 2026-05-12 under the *water* register; under an *ice* register `rime` is register-coherent. This is a **Matt one-word call** — flag it in the completion record; do NOT self-decide.

## Cross-seam coordination

- **gamora sub-dispatch** (`2026-07-12-gamora-water-to-ice-simulation.md`): simulation literals (resistance_matrix, combatant, damage_resolver, spatial). Serializes behind the rocket config pivot + normalizer contract.
- **star-lord sub-dispatch** (`2026-07-12-starlord-water-to-ice-pipeline.md`): llm (naming, cosmological_vocabulary, spirit_guide_voice, phase5), telemetry, export. Serializes behind the pivot.
- All three seams read the SAME normalizer contract from `element/MIGRATION.md`. Do NOT let two seams author divergent normalizers.
- **drax follow-on** (loadout/demo/godot element labels+colors) is a POST-engine-landing pass — KR queues it; NOT in this dispatch's critical path.
- **elrond** schema note already filed separately (`elem_raw` provenance-only) — no action here.

## Required reading before starting

- This dispatch + KR brief §Unit 3
- `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` §5 rows 1c/1d + §2 (enum of record)
- `agentic_orchestration/gandalf/views/rekey-prep/elem-prep.md` §6 (EL2 ruling)
- `config/elements.yaml`, `config/substrate_identities/water.yaml`, `config/ailments.yaml`
- `generation/season_generation_pipeline.py` (STAT_ELEMENT_POOLS)
- Discipline #12

## Math-before-code

N/A for numerics (no resistance/pool-probability change — Law 6). But the INT-pool composition IS a design reading of record: document in MIGRATION.md that INT = `["fire","ice","lightning","shadow"]` is the classic mage quartet per Matt, and that DEX/`_ALL_8` are pure string swaps.

## Out of scope

- Freeze-as-hard-control escalation (→ gandalf ailment-layer queue)
- Retro-pinning corpus cold kits to Ice (→ regen naturally, Law 2)
- Any resistance-value / ailment-parameter / pool-probability change
- **The canonical-four slot-routing layer (`VALID_SLOTS`, `water_slot`/`water_sel` JSON keys, `element/selector.py` + `element/schema.py` internal role-slots) — Discipline #14, structural emitted-kit keys. LEAVE UNTOUCHED.**
- drax presentation-layer relabel (separate follow-on)

## Completion record
_(append: census result, normalizer location + contract, gandalf-review surfaces held/cleared, `rime` flag, INT-pool note, smoke result, MIGRATION.md path, tag, notes for jack-ryan Gate-2)_

### rocket completion — 2026-07-12

**Commit:** `2ae665b` (50 files) · **Tag:** `rocket/v2.7-water-to-ice-element-1` · **Auto-committed, NOT pushed** (KR owns wave push).
**Path correction:** config lives at repo-root `config/` (NOT `src/reincarnated/config/`); the dispatch's `src/reincarnated/config/` path is wrong — `config/` is authoritative (verified via `foundation/config_loader.py`).

#### Census result (substrate-vs-slot classification)
Full-repo `grep -w water` census of my seams (generation/element/anchor/foundation/canonical): **109 `.py` hits + config + data + tests.** Classified:
- **RENAMED → `ice` (SUBSTRATE-ELEMENT display layer):** config/elements.yaml, config/substrate_identities/water.yaml→ice.yaml (+ fire/holy/shadow reciprocal refs), config/ailments.yaml (chill desc + comment); `foundation.py CANONICAL_SUBSTRATES`, `color_spectrum.ELEMENT_COLOR_RANGES` key, `substrate_identity_loader` comments; `season_generation_pipeline STAT_ELEMENT_POOLS/_ALL_8`; `element_biases` (2 dict keys), `element_application_binder`, `geometry_derivation` (branches + `_water_geometry`→`_ice_geometry`), `bc_target_source` (`_FIRE_ICE..` const+branch), `bc_target_player_class`/`typed_monster_skills`/`kit_space_schema` (canonical-8 lists), `substrate_templates`(10)/`endgame_encounter_catalog`(6)/`companion_generation` (`element=`/`preferred_element=`/`dominant_element` literals), `mechanic_alteration`(2), `gear_generation`/`gear_catalog`/`keystone_loadout_materializer` (name-flavor + resistance-vector keys), `bc_target_substrate_engine`/`substrate_weapon_binding`/`phase5_skill_naming`/`phase5_t4_narration` (naming-vocab dict KEYS), `phase5_pm1_multimodal_clustering._ELEMENT_MAP` (ordinal key, value 0.143 kept), `kit_architecture` (merged redundant water key into ice; value refs), canonical `library_generator`/`emit_substrate_registry` (doc strings). anchor/ = **0 hits.**
- **LEFT `water` (CANONICAL-FOUR SLOT-ROUTING, Discipline #14):** `element/selector.py` ENTIRELY (VALID_SLOTS, ~18 water_slot/water_sel JSON keys, _SLOT_TO_GROUPING, Q7 audit refs) · `element/schema.py` ENTIRELY (water_slot structural emitted-kit field) · `data/seasonal_elements/pool.json` (41 primary_slot + 14 substrate_native — provenance mirroring primary_slot, zero display consumer) · `bc_target_composer.py:858` (slot-layer comment "slots from selector.py").
- **LEFT `water` (read-compat legacy detection nets — documented):** regex/keyword superset bags in `bc_target_substrate_engine` (element regex), `synergy_scan_layer7` (element_seeds), `substrate_weapon_binding`/`phase5_skill_naming` (keyword bags) — so historical water-named text still classifies to `ice`.
- **No ambiguous hits required KR escalation** — every hit classified cleanly against the two-layer rule.

#### Normalizer RULE + location
`src/reincarnated/element/MIGRATION.md` [2026-07-12] entry. RULE `elem_rekey_water_to_ice`: on reading a persisted **substrate-element display VALUE** = `"water"` from any historical artifact, normalize → `"ice"` before canonical-set comparison / forward emit. Scope guards: NEVER normalize slot-routing keys (water_slot/primary_slot/slots-dict-keys); NEVER rewrite the on-disk artifact; leave read-side detection-net water tokens. **One RULE, applied at three genuinely-different boundaries** (rocket element-load / gamora fight-log+telemetry read / star-lord export-bundle+telemetry read) — documented so all three apply it identically; not forced into one shared function.

#### gandalf-review register surfaces (DRAFTED, HELD — route via KR before Gate-2)
1. `config/elements.yaml` ice entry: `theme_tags: [cold, preservation, stillness]` (flow/depth retired; preservation carried); `display: Ice`; `color_range [560000,700000]` KEPT.
2. `config/substrate_identities/ice.yaml`: identity content pass (cosmological_commitment → state-change-by-cold/preservation/stillness; court_resonance → Frostbinders; iconic_verbs submerges→encases; telegraph/dodge comment prose). Mechanical identity UNCHANGED (suffusion grouping, chill ailment, SUSTAINED_PRESENCE pillar, geometry/role affinities, windup/i-frame params).
3. `config/ailments.yaml` chill: description → "the cold/freeze register". **Params UNTOUCHED (Law 6).**
4. `config/substrate_identities/fire.yaml`: `forbidden_hybrid_with: [ice]` (functional-required for cross-declaration validation) + i-frame comment. holy/shadow prose comments.
5. `canonical/library_generator.py`: "Tide Shroud"→"Frost Shroud" example; ELEMENT_COLOR_HINTS blue/cyan kept.

#### INT-pool note (design reading of record)
`STAT_ELEMENT_POOLS["INT"] = ["fire", "ice", "lightning", "shadow"]` — the classic mage quartet (Matt-noted). Documented in MIGRATION as a design reading, not a numeric change. DEX 8-pool + `_ALL_8_ELEMENTS` are pure string swaps.

#### `rime` flag (Matt one-word call — NOT self-decided, NOT blocking)
`rime` (D1 vocab pool, demoted allow-list→eligible 2026-05-12 under *water* register) is register-coherent under *ice*. Re-promotion is a Matt call. Flagged in MIGRATION §"Open Matt-decision item". Did not touch pool.json.

#### Smoke result
- Config loads clean: ice element (display Ice, ailment chill, theme [cold,preservation,stillness], grouping suffusion).
- **Zero-numeric-drift PROVEN:** ice inherits water's exact numerics (color band 560000–700000, ailment chill, scaling intelligence, resistance_type percentage, dodge_iframes 0.35, windup 0.7); chill params byte-unchanged (slow 0.2–0.5, duration 2.0–5.0). Only the element key string differs.
- **leg2 primary-T4 route smoke: 14/14 GREEN, `S2_non_summoner_byte_identical: true`** — including the `ice` corpus row (byte-identical off the route).
- My-seam tests (per-file isolated): green except **7 PRE-EXISTING failures** in test_foundation(4)/test_substrate_identity_loader(2)/test_d2_substrate_coupling(1) — all canonical-7-config-vs-stale-canonical-4-count assertions, **PROVEN identical on HEAD via git-stash** (NOT this rename; predate this wave). Updated substrate-element `water`→`ice` in ~14 test files; LEFT slot-layer (VALID_SLOTS/water_slot) test assertions untouched.

#### MIGRATION path + tag
`src/reincarnated/element/MIGRATION.md` [2026-07-12] · tag `rocket/v2.7-water-to-ice-element-1`.

#### Notes for jack-ryan Gate-2 (scrutinize)
1. **star-lord export normalizer is REQUIRED and surfaced:** `tests/test_one_realm_bundle_assembler.py::test_season_000001_generates_nonzero_pool` now FAILS with `KeyError: Unknown element: water` — a HISTORICAL season_000001 catalog is read by `export/one_realm_bundle_assembler.py::generate_gear_pool_from_catalog` (STAR-LORD's seam) and hits the ice-only pipeline. This is the intended serialization — star-lord must apply `elem_rekey_water_to_ice` at that catalog read. NOT patched by rocket (export/ is not my seam). Flag to star-lord via KR.
2. **gamora-lockstep smoke:** `generation/notes/typed_resistance_roundtrip_smoke_2026_06_21.py` asserts on the resistance_matrix `water` key (gamora's rename target) — LEFT `water` deliberately; must be rekeyed IN LOCKSTEP with gamora's `resistance_matrix` element-KEY rename to avoid breaking mid-serialize.
3. **elrond CHECK constraint:** `kit_space_schema.CANONICAL_ELEMENTS_LOWERCASE` now emits `ice` — verify elrond's shadow-table element CHECK constraint accepts `ice` (elrond `elem_raw` note already filed provenance-only).
4. **Pre-existing test debt (NOT mine):** the 7 canonical-count failures + the grouping-layer-vocabulary.md doc-path RuntimeError (any test importing `llm.naming` fails on a missing collaboration-repo doc; star-lord/env issue) both pre-date this wave — proven on HEAD.
5. Register surfaces (item list above) are gandalf-review-BEFORE-Gate-2 per dispatch Law 4.
