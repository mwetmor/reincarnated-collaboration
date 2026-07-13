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
_(append: census result, normalizer-consumption confirmation, gandalf register-review status, DB-migration note if any, smoke result, MIGRATION.md paths, tag, notes for jack-ryan Gate-2)_
