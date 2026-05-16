# Dispatch — star-lord gear-pool-stats re-export (2026-05-14)

**Target:** star-lord (reincarnated-engine, output for reincarnated-loadout consumption)
**Branch:** main
**Tag intent:**
- Intermediate: `star-lord/season-002328-gear-pool-stats` — star-lord-autonomous after acceptance verified
- No milestone tag — this is an internal artifact re-export, not a player-facing milestone

## Context

Matt's QA on drax v0.5-real-gear surfaced that gear display has no stats (Bug 5). The current gear_pool.json schema has `gear_id`, `slot`, `handedness`, `tier`, `name`, `flavor_text`, `fit_energy_type`, `fit_role_orientation`, `power_score`, `color_value` — but NO per-item stat fields (STR/DEX/INT bonuses, AC, damage, etc.).

Matt's decision (Option A from triage): **star-lord re-exports the gear_pool with per-item stat fields.** Drax wires up display in a follow-up patch.

## Work

Re-export `reincarnated-loadout/data/season_002328/gear_pool.json` to include per-item stat fields.

**Investigation likely needed first:**
1. What stats does the engine assign to gear at generation time? (Read engine gear-generation code in `reincarnated-engine/src/reincarnated/generation/` and any gear-related modules in `src/reincarnated/`.)
2. Are per-instance stats **deterministic per `gear_id`**, or **rolled with variance at drop time**?
   - If deterministic: export the stats directly per item.
   - If rolled with variance: decide whether to export (a) representative stats (e.g., median roll), (b) stat ranges (min-max), or (c) a sample-roll instance per gear_id. Matt's intent is "display meaningful stats on a gear card" — pick whichever shape supports that cleanly.

Schema design is star-lord's call; document the chosen schema either inline as comments or in a sibling README so drax knows what fields to expect.

## Cross-seam coordination

- **Drax consumes the new schema.** Drax dispatch v0.5.2 (or rolled into v0.7) wires up stats display after this dispatch lands.
- **MIGRATION.md required** if other consumers of `gear_pool.json` exist or if the schema is versioned. Star-lord assesses and authors if needed (ADR-004).
- If schema versioning is added or changed, note it in the completion record so drax knows to handle the version field.

## Acceptance

1. `reincarnated-loadout/data/season_002328/gear_pool.json` re-exported with per-item stat fields
2. Schema documented (inline comments or sibling README)
3. No regressions in any other gear_pool consumers (audit who else reads the file)
4. Sample a few items at different tiers and confirm stat values are sensible (e.g., legendary items have higher stats than common, where applicable)

## Out of scope

- Telemetry fight-log schema (separate research pass dispatched in parallel)
- Other seasons' gear pools (Yomi season_002328 only for now)
- Drax display work (separate dispatch)
- Re-running balance/convergence (the existing season's classes don't depend on the gear_pool export, only on the engine's internal gear state)

## Required reading

- Prior dispatch: `agentic_orchestration/dispatches/2026-05-14-star-lord-export-yomi-gear-pool.md`
- Engine gear generation: `reincarnated-engine/src/reincarnated/generation/` (gear-related modules)
- Current gear_pool.json layout

## Completion record — 2026-05-15

**Completed by:** star-lord  
**Status:** DONE — drax unblocked for stats display

### Engine changes

| File | Commit |
|---|---|
| `src/reincarnated/export/schemas.py` | c1f02ca |
| `src/reincarnated/export/season_exporter.py` | c1f02ca |
| `src/reincarnated/export/MIGRATION.md` | c1f02ca |
| `src/reincarnated/export/AGENT_STATE.md` | 4897023 |

**Intermediate tag:** `star-lord/season-002328-gear-pool-stats` at `4897023`

### Loadout changes

| File | Commit |
|---|---|
| `data/season_002328/gear_pool.json` | 7693af9 (loadout repo) |

File size: 196 KB → 350 KB (stats + rolled_effects + ability_modifiers added).

### Stat fields added

Three new fields on every `ExportGearItem`:

1. **`stats`** (dict) — flat GearStats: `bonus_hp`, `bonus_armor`, `bonus_crit_chance`,
   `bonus_damage_flat`, `bonus_damage_percent`, `bonus_mana_regen`,
   `elemental_resistances`, `block_chance`, `block_value`

2. **`rolled_effects`** (list) — raw effect list: `{effect_type, element, trigger, magnitude}`.
   Ailments (burn, bleed, chill, root, knockback) appear here but NOT in stats.

3. **`ability_modifiers`** (dict) — rare+ mechanical modifiers: `cooldown_factor`,
   `energy_cost_factor`, `crit_bonus_damage`, `control_duration_bonus`

### Schema documentation

`src/reincarnated/export/MIGRATION.md` — full v1.0 → v1.1 schema change documentation
including field semantics, derivation method, and drax action items.

### Investigation findings

- Stats are **not stored in the telemetry DB** — only derived at generation time.
- Stats are **deterministic** from the season seed: re-run
  `generate_season_gear_pool(catalog, 10, rng=np.random.default_rng(seed + 999))`
  with the season's `gear/catalog.json` to get exact same items.
- **Order mapping**: DB stores items oldest-rowid-first; export query is newest-first.
  `gear_pool.json[i]` corresponds to `regen_items[N-1-i]` (reverse position).

### Acceptance verified

- [x] 200 items with per-item stats (all non-null)
- [x] Tier-appropriate stats: shields have block values, armor has HP/armor, accessories have damage_percent/mana_regen
- [x] All existing fields unchanged — zero regressions
- [x] MIGRATION.md authored
- [x] Schema documented inline (field-level comments in `schemas.py`)

### Deviations from spec

- `rolled_effects` and `ability_modifiers` added beyond the spec minimum ("stat fields") —
  judged useful for drax tooltip display without adding complexity. Additive; no risk to drax.
- Stats **do not perfectly tier-scale** for bonus_damage_flat (common items can exceed some
  legendary values because ailment effects add to power_score but not to GearStats).
  `power_score` is the canonical strength ranking; documented in MIGRATION.md.

### For drax

See `MIGRATION.md` for wiring guidance. Suggested display:
- Primary: `bonus_damage_flat`, `bonus_hp`, `bonus_armor`, `bonus_crit_chance`
- Secondary: `bonus_damage_percent`, `bonus_mana_regen`, `block_chance`/`block_value`
- Tooltip: `rolled_effects` for "On Hit: 623 fire damage" style text
- `ability_modifiers` for "Cooldown −11.7%" modifier lines
