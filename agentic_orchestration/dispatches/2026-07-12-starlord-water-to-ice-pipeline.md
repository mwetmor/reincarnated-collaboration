# Dispatch — 2026-07-12 — star-lord — element `water` → `ice` (Unit 3 / Wave 2, LLM/TELEMETRY/EXPORT sub-scope)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt ruling 2026-07-12 (elem-prep §6 EL2); relayed via gandalf KR brief
**Pattern:** B (multi-hour; own session memory)
**Serialization:** **BEHIND the rocket LEAD config pivot.** Do NOT start until `rocket/v2.7-water-to-ice-element-1` has landed the config rename + the shared read-compat normalizer contract in `element/MIGRATION.md`. Read that contract FIRST and mirror it.
**Estimated effort:** half-day
**Acceptance:** live llm/telemetry/export code speaks `ice`; reads the rocket normalizer (`water`→`ice`) at load; historical telemetry rows / export bundles untouched (provenance); pipeline tests green; MIGRATION.md entries. Tag `star-lord/v-water-to-ice-pipeline-1`.

## Context

Part of the Matt-ruled `water`→`ice` element rename + cold/frost register (EL2). rocket owns the config pivot + element load-boundary normalizer + generation literals; gamora owns simulation. **You own llm, telemetry, and export literals.** The register shift matters MOST in the llm surfaces — element-naming vocabulary, cosmological vocabulary, and spirit-guide voice must speak the cold/frost/ice register, not water.

## Binding laws

1. **Census-first** — grep `"water"` across `llm/`, `telemetry/`, `export/`, `output/` code (NOT emitted bundles) before editing.
2. **Historical artifacts immutable** — persisted telemetry rows, past `output/` season bundles keep `water` as provenance. Normalize on read; emit `ice` forward. NEVER retro-edit emitted bundles or telemetry rows.
3. **MIGRATION.md** per touched seam (telemetry, export).
4. **Gate-2 (jack-ryan)** before tag. **gandalf reviews the llm register surfaces** (naming/cosmological/spirit-guide-voice cold-frost register) BEFORE Gate-2 — route those back through KR to gandalf.
5. **Auto-commit, no push.**
6. **No scope creep:** no schema-value change beyond the string; no telemetry-column add/remove for this unit. Rename + register only.

## Path note

All live code is under `src/reincarnated/{llm,telemetry,export}/...`. A decoy top-level `./simulation` (`output/` only) exists — ignore it.

## ⚠ Discipline #14 layer exclusion (Gate-1 finding — llm/naming is the leak surface)

`water` lives in two layers. Rename the SUBSTRATE-element (display) VALUE only. The **canonical-four slot-routing layer** (`water_slot`/`water_sel`/`VALID_SLOTS`, rocket's `element/selector.py`+`schema.py`) MUST NOT rename — it is Discipline #14 internal routing + a structural emitted-kit key. **Your highest-risk leak point is llm `naming`/prompt sites that may reference `water_slot` or the four-slot protocol** — classify each `water` hit substrate-display (rename) vs canonical-four-slot (leave). If ambiguous, route to gandalf via KR.

## Known surfaces (anchors — verify against census; brief: telemetry 5 · export 5 · llm 4)

- **llm:** `naming` (element-name vocabulary → ice/cold/frost register) · `cosmological_vocabulary` · `spirit_guide_voice` · `phase5` — ⚑ these are gandalf-review register surfaces (voice/register, not just string swap)
- **telemetry:** element-column value literals (rename the emitted value `water`→`ice`; normalize `water` on read for historical rows). NO schema-field add/remove.
- **export:** season-writer / bundle element labels → `ice` on emit; historical bundles keep `water`.
- pipeline test files in the census

## ⚠ Telemetry-DB note (do NOT apply migrations)

Production telemetry DB migration is Matt-gated (ADR-006). This unit changes emitted VALUE strings, not schema. If any value-normalization touches the DB, document the apply-command in `telemetry/MIGRATION.md` and leave it UNAPPLIED for Matt. Do not run migrations against production.

## Read-compat normalizer

Do NOT author your own. Consume the shared contract from `element/MIGRATION.md` (rocket-authored). Telemetry/export read sides that ingest persisted element strings normalize `water`→`ice` using the same rule.

## Required reading before starting

- This dispatch + the rocket LEAD dispatch (`2026-07-12-rocket-water-to-ice-element-LEAD.md`)
- `element/MIGRATION.md` (shared normalizer contract — MUST exist before you start)
- KR brief §Unit 3

## Math-before-code

N/A. Smoke: run the export/round-trip smoke proving a season emits `ice` element labels and a historical `water` bundle still loads clean through the normalizer.

## Cross-seam contract change? (Principle 6 gate)

The emitted element VALUE crosses simulation → telemetry → export. MIGRATION.md required (telemetry + export). No schema-field add/remove for this unit. Coordinate value-normalization with gamora's simulation read side so the boundary is consistent.

## Out of scope

- Telemetry-DB migration application (Matt-gated)
- Schema-column add/remove
- generation/simulation/config literals (other seams)
- resistance/ailment/pool changes

## Completion record

**Completed:** 2026-07-12
**Commit:** `1038e28`
**Tag:** `star-lord/v-water-to-ice-pipeline-1`

### Census result (substrate-vs-slot classification)

Total `water` hits across `llm/`, `telemetry/`, `export/`: ~40 lines across 17 files.

**Classification summary:**

| Category | Count | Action |
|---|---|---|
| SUBSTRATE-DISPLAY (code literals — element sets, dicts, variables) | 22 | RENAMED → `ice` |
| SUBSTRATE-DISPLAY (comments/docstrings) | 12 | UPDATED |
| GANDALF-REVIEW (prompt/register surfaces) | 5 surface sites | DRAFTED + flagged |
| SLOT-ROUTING (Discipline #14 — kept `water`) | 4 | LEFT UNTOUCHED |
| Historical artifact comments (read-normalizer docs) | references | LEFT (`water` kept as provenance token) |

**Slot-routing tokens left as `water` (Discipline #14 exclusion):**
- `recorder.py` lines 165 + 1190: fallback tuple `("fire", "wind", "water", "earth")` — pre-Coupling-#1 named-field path
- `cycle13_normal_season_export.py` line 630: `"canonical_slot": "water"` — slot-routing key in emitted manifest
- `selector.py` `VALID_SLOTS` (`"water"`) — not in star-lord seam, rocket-owned

**No ambiguous `water_slot` / `water_sel` / four-slot-protocol references found in llm/telemetry/export seam.**

### Normalizer consumption confirmation

Consumed `element/MIGRATION.md` RULE `elem_rekey_water_to_ice` (rocket-authored). Applied at:
- **Export read boundary:** `one_realm_bundle_assembler._normalize_catalog_element_water_to_ice()` normalizes `effect_pool[].element` in `GearCatalog` raw JSON before `model_validate()`. Applied in `generate_gear_pool_from_catalog()`.
- **LLM/telemetry:** no historical artifact read boundaries required in-session (forward-only emitters updated; DB normalization is on-read via gamora or via DB UPDATE documented in telemetry MIGRATION.md).

Did NOT author a divergent normalizer — consumed the RULE pattern directly in the normalizer helper function.

### Export KeyError fix

`test_one_realm_bundle_assembler::test_season_000001_generates_nonzero_pool` was failing with
`WARNING: Gear pool generation failed: 'Unknown element: water' — gear pool will be empty`.

Root cause: `season_000001/gear/catalog.json` has `element: "water"` in `effect_pool` entries. After rocket's `ELEMENT_COLOR_RANGES` rename (`water`→`ice`), `sample_color_in_range("water")` raised `KeyError`.

Fix: Added `_normalize_catalog_element_water_to_ice(raw_dict)` helper. Applied at the read boundary in `generate_gear_pool_from_catalog()` — normalizes in-memory before `GearCatalog.model_validate()`. Historical catalog.json untouched on disk.

Smoke verification: 150-record pool generated, 0 with `dominant_element="water"`, 12 with `dominant_element="ice"`. All 93 bundle assembler tests pass.

### DRAFTED LLM register surfaces — GANDALF-REVIEW REQUIRED before Gate-2

Routed via KR to gandalf:

1. **`llm/ws1a4_lite_flavor_judgment.py`** — `Q18_FLAVOR_POOL` key `"water"` → `"ice"`; pool entries UNCHANGED (same cold/frost/ice vocabulary). `_CANONICAL_NAMING_PATTERNS["water"]` → `"ice"` with example "Ice Spear" replacing "Water Spear". ROTATING_PRIMARIES auto-updates from pool keys. `test_ws1a4_lite_flavor_judgment.py` test expectations updated to `"ice"`. Flagged with DRAFT comment.
2. **`llm/cosmological_vocabulary.py`** — ANTI-BIAS prompt line: `water` kept in list + `ice` added explicitly. Both blocked. Flagged with DRAFT comment.
3. **`llm/spirit_guide_voice.py`** — ANTI-REFERENCE RULES `fire, water, earth, wind...` → `fire, ice, earth, wind...`. Flagged with DRAFT comment.
4. **`export/w3_batch1_flavor_writer.py`** — element register line `water=chill/tide/pressure` → `ice=chill/cold/frost`. Flagged with DRAFT comment.
5. **`llm/phase5_orchestrator.py`** — element pair sets `{"fire","water"}` → `{"fire","ice"}` and `{"water","wind"}` → `{"ice","wind"}`. These are substrate identity pairs (NOT voice/prose) — no gandalf register review needed; standard substrate-display rename. Included here for completeness.

Gandalf review scope: items 1-4 above. Item 5 is clean substrate-display rename.

### DB migration note

No production DB migrations applied. Documented in `telemetry/MIGRATION.md`:
- `UPDATE seasonal_elements SET element_id = 'ice' WHERE element_id = 'water'`
- `UPDATE aoe_cast_events SET skill_substrate = 'ice' WHERE skill_substrate = 'water'`
- NOTE: `role_slot = 'water'` rows are SLOT-ROUTING — must NOT be updated without full slot-layer migration (Discipline #14 exclusion).
All UNAPPLIED; Matt authorization required per ADR-006.

### Smoke result

- `test_one_realm_bundle_assembler` (93 tests): PASS — includes `test_season_000001_generates_nonzero_pool` which was previously failing
- `test_ws1a4_lite_flavor_judgment` (34 tests): PASS
- `test_d2_substrate_coupling` (43 tests): PASS — `test_get_valid_slots_with_foundation_returns_registry` updated to use registry-driven assertion (foundation now returns `ice` not `water` after rocket config pivot)
- Broader smoke (595 tests across 9 test files): PASS
- Export round-trip: 150-gear pool from historical `water`-catalog emits `ice` forward. PASS.

### MIGRATION.md paths

- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — new entry [2026-07-12]
- `reincarnated-engine/src/reincarnated/telemetry/MIGRATION.md` — new entry [2026-07-12]
- `reincarnated-engine/src/reincarnated/element/MIGRATION.md` — source RULE (rocket-authored, consumed not modified)

### Notes for jack-ryan Gate-2

1. **Elrond shadow-table CHECK constraint** — `element/MIGRATION.md` flags: "verify elrond's shadow-table element CHECK constraint accepts `ice`." Not in star-lord seam. Route to elrond for verification.
2. **GANDALF-REVIEW surfaces** — 4 prompt/register surfaces drafted (ws1a4 Q18 pool key, cosmological ANTI-BIAS, spirit_guide ANTI-REFERENCE, w3_batch1 element register). These carry DRAFT comments. Must be reviewed by gandalf before Gate-2 closes. Route via KR.
3. **Slot-routing layer (`VALID_SLOTS` still `water`)** — `selector.py` `VALID_SLOTS = ("fire", "wind", "water", "earth")` and `schema.py` `water_slot` remain as `water` per Discipline #14. Gate-2 should confirm this is intentional and does not regress any selector/schema tests.
4. **`test_d2_substrate_coupling.py` assertion update** — `test_get_valid_slots_with_foundation_returns_registry` was updated from hardcoded `{"fire","wind","water","earth"}` to `set(slots) == registry_names` (dynamic). Rationale: the foundation now returns 7 rotating substrates (fire/ice/earth/wind/lightning/holy/shadow) after rocket's config pivot. The test was testing a stale assumption. Gate-2 should verify this change is correct.
5. **DB migration** — UNAPPLIED per ADR-006. Gate-2 should note this for Matt authorization queue.
