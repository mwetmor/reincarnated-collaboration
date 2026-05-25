# MIGRATION.md — Cycle 10 Stage 4 — weapon_sim_props Schema Extension + Population

**Date:** 2026-05-25
**Author:** rocket
**Dispatch authority:** `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md`
**ADR-004 compliance:** required for schema changes that affect downstream consumers (gamora + star-lord)

---

## Schema changes

### 1. ADD COLUMN — damage_amplitude_min REAL

```sql
ALTER TABLE weapon_sim_props ADD COLUMN damage_amplitude_min REAL;
```

**Purpose:** Substrate-level minimum damage roll scalar for per-weapon hit rolls. Paired with damage_amplitude_max to define the per-hit damage range under a uniform distribution assumption. CV (Axis 3B bin) is derivable at sim time from the pair ratio: CV = (max - min) / (sqrt(3) * (max + min)).

**Downstream impact:** gamora sim engine reads this column at weapon binding (Phase 2 substrate-binding). star-lord export pipeline exports this field in export packet. Both consumers must handle NULL gracefully until Stage 4 population completes.

**Amplitude ratio bins (BC Axis 3B alignment):**
- flat (CV < 0.3): max/min ratio < 1.9x
- variable (CV 0.3-0.7): max/min ratio 1.9x - 4.5x
- spiky (CV >= 0.7): max/min ratio > 4.5x

### 2. ADD COLUMN — damage_amplitude_max REAL

```sql
ALTER TABLE weapon_sim_props ADD COLUMN damage_amplitude_max REAL;
```

**Purpose:** Substrate-level maximum damage roll scalar. See damage_amplitude_min above.

### 3. CRITICAL (LOAD-BEARING) — primary_stat CHECK constraint: add DEX

**Current constraint:** `CHECK (primary_stat IN ('STR','INT','WIS'))`
**Required constraint:** `CHECK (primary_stat IN ('STR','INT','WIS','DEX'))`

**Why load-bearing:** DEX is the largest single-attribute class in the typed v1_scope pool (46.4% of typed rows = ~877 rows have proxy_attribute_class = 'DEX'). Without this fix, population of weapon_sim_props fails on all DEX-primary weapons via CHECK constraint violation. This is a schema bug inherited from the pre-DEX (3-attribute) system.

**SQLite constraint:** SQLite does not support ALTER TABLE ... DROP CONSTRAINT or ADD CONSTRAINT. The constraint is baked into the column definition in the CREATE TABLE statement. To modify it, the table must be recreated.

**Migration strategy (SQLite-compatible):**

```sql
-- Step 1: create new table with corrected schema + new columns
CREATE TABLE weapon_sim_props_new (
    weapon_id              INTEGER PRIMARY KEY REFERENCES weapon_knowledge_entries(id) ON DELETE CASCADE,
    range_min_units        REAL,
    range_max_units        REAL,
    base_attack_speed      REAL,
    charge_time_s          REAL,
    hits_per_attack        INTEGER,
    aoe_radius_units       REAL,
    primary_stat           TEXT CHECK (primary_stat IN ('STR','INT','WIS','DEX')),
    secondary_stat         TEXT CHECK (secondary_stat IN ('STR','INT','WIS','DEX','none')),
    damage_amplitude_min   REAL,
    damage_amplitude_max   REAL,
    sim_viable             INTEGER NOT NULL DEFAULT 0,
    sim_viability_notes    TEXT,
    sim_verified_date      TEXT
);

-- Step 2: copy existing rows (0 rows currently, but for correctness)
INSERT INTO weapon_sim_props_new SELECT
    weapon_id, range_min_units, range_max_units, base_attack_speed,
    charge_time_s, hits_per_attack, aoe_radius_units, primary_stat,
    secondary_stat, NULL, NULL, sim_viable, sim_viability_notes, sim_verified_date
FROM weapon_sim_props;

-- Step 3: drop old table, rename new
DROP TABLE weapon_sim_props;
ALTER TABLE weapon_sim_props_new RENAME TO weapon_sim_props;
```

**FK reference change (also load-bearing):** The original weapon_sim_props schema references `weapons(weapon_id)`. The `weapons` table is legacy demo-asset content (Kenney blaster packs, UH-60M Blackhawk, F-16 avatar templates) — NOT the substrate knowledge entries. Only 49 of 2,293 v1_scope knowledge entries exist in the `weapons` table, making the FK reference wrong for substrate-tagging purposes. Migration corrects FK to reference `weapon_knowledge_entries(id)`. FK enforcement is OFF in this SQLite deployment (PRAGMA foreign_keys = 0), so this is a schema correctness fix, not a behavioral change.

---

## Downstream consumer impact

### gamora (sim engine)

- Reads `weapon_sim_props` at Phase 2 substrate-binding for fight simulation
- New columns `damage_amplitude_min` / `damage_amplitude_max`: gamora sim must be updated to consume these or treat as optional (NULL-safe) until Stage 4 population completes
- `primary_stat = 'DEX'` now valid: gamora code consuming `primary_stat` must handle DEX
- **Round-trip smoke required** per Principle 6 before tag: gamora writes fight_log containing weapon_id + damage roll; star-lord export packet must include damage_amplitude_min/max field values

### star-lord (telemetry / export pipeline)

- Exports `weapon_sim_props` fields in export packets
- New columns `damage_amplitude_min` / `damage_amplitude_max` must be exported
- Grep pattern to verify: `weapon_sim_props` column reads in star-lord export code

### drax / loadout app

- Does NOT directly consume `weapon_sim_props` in player-facing surface (verified; Phase D precedent)
- No immediate action required; update if v1.0+ adds player-facing weapon-sim-display

---

## Pre-population state

- `weapon_sim_props`: 0 rows (empty before Stage 4)
- `weapon_knowledge_entries` v1_scope = 1: 2,293 rows
- Typed (proxy columns populated): 1,851 rows
- NULL-typed: 442 rows

---

## Post-population expected state

- `weapon_sim_props`: ~2,293+ rows (v1_scope entries)
- All rows: non-NULL on range_min_units, range_max_units, base_attack_speed, charge_time_s, hits_per_attack, aoe_radius_units, primary_stat, damage_amplitude_min, damage_amplitude_max
- sim_viable: 0 for out-of-genre rows (odin-army-tradoc military_modern, royal_armouries components); 1 for verified viable entries
- Mythological-NULL rescue: ~21 rows updated with `v1_scope_composition_trace` = 'stage_4_mythological_rescue_complete'

---

## Rollback

Pre-population backup at:
`agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/backups/telemetry.db.pre-stage-4`
(gitignored per project convention)

Rollback procedure: `cp backups/telemetry.db.pre-stage-4 /Users/admin/Games/reincarnated-loadout/data/telemetry.db`
