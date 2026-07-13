# Dispatch — 2026-07-12 — gamora — element `water` → `ice` (Unit 3 / Wave 2, SIMULATION sub-scope)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt ruling 2026-07-12 (elem-prep §6 EL2); relayed via gandalf KR brief
**Pattern:** B (multi-hour; own session memory)
**Serialization:** **BEHIND the rocket LEAD config pivot.** Do NOT start until `rocket/v2.7-water-to-ice-element-1` has landed the `config/elements.yaml` rename + the shared read-compat normalizer contract in `element/MIGRATION.md`. Read that normalizer contract FIRST and mirror it — do not author a divergent normalizer.
**Estimated effort:** half-day
**Acceptance:** live simulation code speaks `ice`; reads the rocket-authored normalizer (`water`→`ice`) at load; historical artifacts untouched; simulation tests green; `simulation/MIGRATION.md` entry. Tag `gamora/v1.6-water-to-ice-simulation-1`.

## Context

Part of the Matt-ruled `water`→`ice` element rename + cold/frost register (EL2). rocket owns the config pivot, the element load-boundary normalizer, and the generation literals. **You own the simulation-seam literals only.** The mechanic is UNCHANGED — `chill` (soft_control slow) already is the cold/frost ailment; this is a string + register pass, zero behavioral change.

## Binding laws

1. **Census-first** — grep `"water"` across `simulation/` before editing.
2. **Historical artifacts immutable** — telemetry/fight-log rows keep `water`; normalize on read, emit `ice` forward. NEVER retro-edit.
3. **MIGRATION.md** (`simulation/MIGRATION.md`).
4. **Gate-2 (jack-ryan)** before tag.
5. **Auto-commit, no push.**
6. **No scope creep:** NO resistance-value change, NO ailment-parameter change. String + register only.

## Path note

All live code is under `src/reincarnated/simulation/...`. A decoy top-level `./simulation` (`output/` only) exists — ignore it.

## ⚠ Discipline #14 layer exclusion (Gate-1 finding)

`water` lives in two layers. You rename the SUBSTRATE-element layer only (the `resistance_matrix` element KEY, combatant/damage_resolver element literals). If any simulation code references the canonical-four slot-routing tokens (`water_slot`/`VALID_SLOTS` — rocket's `element/selector.py`+`schema.py` seam), LEAVE THEM — they are Discipline #14 internal routing keys and structural emitted-kit keys, not the display element. If ambiguous, flag to KR.

## Known surfaces (anchors — verify against census; brief: simulation 8 literals)

- `resistance_matrix` (⚠ rename the KEY string `water`→`ice`; VALUES/coefficients UNCHANGED — Law 6)
- `combatant`
- `damage_resolver.py`
- `spatial_gauntlet/` (spatial resolver element references)
- simulation test files in the census

## ⚠ E4 overlap note

HEAD `785956c` carries live E4 PHASE-2 cast-state work in `spatial_engine.py` with **Gate-2 pending/held**. Touch ONLY `water` string sites; do not disturb E4 cast-state logic. If the `water` sites are entangled with held E4 code, flag to KR before editing rather than risk contaminating the held E4 build.

## Read-compat normalizer

Do NOT author your own. Read the shared contract from `element/MIGRATION.md` (rocket-authored) and consume it. If simulation reads element strings from persisted fight-logs/telemetry, normalize `water`→`ice` at that read boundary using the same rule.

## Required reading before starting

- This dispatch + the rocket LEAD dispatch (`2026-07-12-rocket-water-to-ice-element-LEAD.md`)
- `element/MIGRATION.md` (the shared normalizer contract — MUST exist before you start)
- KR brief §Unit 3

## Math-before-code

N/A — no numeric change. Smoke: run a simulation smoke proving a fight resolves byte-identically pre/post rename (resistance coefficients unchanged; only the element key string differs).

## Cross-seam contract change? (Principle 6 gate)

The `water`→`ice` element key crosses simulation → telemetry/export (star-lord). MIGRATION.md required. Coordinate the key rename so star-lord's telemetry read side normalizes identically. No new schema field.

## Out of scope

- resistance-value / ailment-parameter changes
- E4 cast-state logic
- generation/config/llm/export literals (other seams)

## Completion record
_(append: census result, normalizer-consumption confirmation, E4-overlap resolution, smoke result, MIGRATION.md path, tag, notes for jack-ryan Gate-2)_
