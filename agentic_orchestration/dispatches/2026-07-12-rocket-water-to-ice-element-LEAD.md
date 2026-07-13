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
