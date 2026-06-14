# Dispatch — 2026-06-14 — star-lord + gamora — A4: v2.15 `ALTER TABLE` (BC-coordinate cutover dependency)

**From:** knight-rider
**To:** star-lord (schema owner — authors the migration) + gamora (provides `recompose_energy_calibration_applied` spec)
**Approved by:** Matt 2026-06-14 (BC-coordinate cutover program authorized; gandalf §7 ratified)
**Estimated effort:** bounded — single `ALTER TABLE` migration + two field specs
**Acceptance:** `class_fight_loadouts` carries `archetype_label` + `recompose_energy_calibration_applied` columns at schema v2.15; round-trip verified through the export/telemetry boundary.

## Context

This is the **A4 cross-seam dependency** of the BC-coordinate-identity cutover program (gandalf §7 ruling, Matt-authorized 2026-06-14). It is W0.2's deferred co-migration obligation (W0.2 math note §8.4 / `:775`), now activated because rocket's Stage-1 generation cutover will emit an `archetype_label` derived from the `bc_target` coordinate (the internal legacy-format bridge, §7.6) that needs a persistence home.

This dispatch runs **in parallel with rocket's Stage-1 math note** — it does NOT gate the math note, but it MAY gate Stage-1 persistence (rocket cannot emit `archetype_label` to telemetry until the column exists). Route it promptly so it is not the long pole.

`archetype_label` here is the **internal coordinate-derived bridge label** (`synthesize_archetype_label` output, e.g. `"ranged-slow/large-AOE/damage-pure/glass/overflow_damage_mana"`) — an internal structural identifier for telemetry/keying during the transition, NEVER player-facing. It is NOT the legacy `{element}_{role}` disease label (deleted in Stage 3) and NOT the player-facing `PlayerClass.name` LLM label.

## Required reading before starting

- `agentic_orchestration/gandalf/notes/2026-06-14-class-generator-bc-target-cutover-ruling.md` — §0, §5–§6, §7.6 (program shape); §7.9 (which label this is — the transitional coordinate-string identifier, NOT the disease label)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md` §8.4 / `:775` — the A4 spec as originally deferred
- `agentic_orchestration/rocket/notes/2026-06-14-compose-kit-cutover-readiness-probe.md` §4 — A4 status (open; gates W0.2.6 MIGRATION.md)
- star-lord: current `class_fight_loadouts` schema definition + migration conventions (your seam)
- gamora: the `recompose_energy_calibration_applied` field — where the recompose-energy-calibration flag is set in the balance loop

## Math-before-code (if applicable)

Schema migration — no algorithmic math note required. star-lord documents the migration rationale + rollback in the MIGRATION.md per ADR-004.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

**YES — this dispatch IS the cross-seam contract change.** It adds two fields to a telemetry schema table (`class_fight_loadouts`):
- `archetype_label` — rocket spec (the transitional coordinate-derived bridge string)
- `recompose_energy_calibration_applied` — gamora spec (boolean; recompose-loop calibration flag)

**Acceptance MUST include the round-trip clause** (and does, below).

## Scope

- [ ] **star-lord:** single `ALTER TABLE` migration to schema v2.15 adding both columns to `class_fight_loadouts`
- [ ] **gamora:** provide the `recompose_energy_calibration_applied` field spec (type, default, where set in the balance loop) to star-lord
- [ ] **rocket** provides the `archetype_label` field spec (type, nullable, max length for the coordinate string) — coordinate via the Stage-1 dispatch; star-lord pings rocket if spec detail is missing
- [ ] Migration is forward-only with documented rollback
- [ ] Smoke-test: migration applies cleanly to a copy of the current telemetry DB
- [ ] MIGRATION.md authored (star-lord) per ADR-004 — affects rocket (emits `archetype_label`) + gamora (emits `recompose_energy_calibration_applied`)
- [ ] Round-trip smoke (clause below) per Principle 6
- [ ] AGENT_STATE.md updated (star-lord)
- [ ] Tag: `star-lord/v?.?-a4-v2-15-alter-table`

## Acceptance criteria

- [ ] `class_fight_loadouts` at schema v2.15 has `archetype_label` + `recompose_energy_calibration_applied`
- [ ] Migration applies cleanly to the current telemetry DB (smoke)
- [ ] Round-trip smoke: a production-path loadout write (or a representative fixture) round-trips through the export/telemetry boundary with both new columns present and writable; a read-back confirms field presence and type
- [ ] MIGRATION.md documents the cross-seam impact (rocket + gamora as producers)

## Out of scope (explicit non-goals)

- The actual EMISSION of `archetype_label` from generation — that is rocket's Stage-1 work; this dispatch only provides the column
- Any change to the AI keying or balance-loop logic — gamora provides the field spec only; the Stage-2 AI bin-keying migration is a SEPARATE later dispatch
- Deletion of any legacy `archetype_tag` machinery — that is Stage 3
- Schema changes beyond these two columns

## Open questions for the agent to resolve

- **star-lord:** `archetype_label` column type/length — the coordinate string can be long (`"ranged-slow/large-AOE/damage-pure/glass/overflow_damage_mana"`); confirm a sufficient VARCHAR/TEXT choice with rocket
- **gamora:** default value for `recompose_energy_calibration_applied` (false vs null) and whether historical rows need backfill or stay null
- **sequencing:** confirm with rocket whether Stage-1 persistence wants this landed before or alongside the Stage-1 implementation (the math note does not depend on A4; the implementation's telemetry write does)

## References

- gandalf §7 ruling; W0.2 math note §8.4; rocket probe §4
- ADR-004 (MIGRATION.md cross-seam handoff)
- Per-stage / cross-seam gate: jack-ryan Gate-2 on the migration
