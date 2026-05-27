# SC-6 Progressive Findings — KR Capture (Cycle 14 Wave 0)

> **STATUS:** WORKING — KR-authored orchestration capture of elrond's discovered findings + KR DB diagnostic for the SC-6 substrate weapon audit. Two elrond invocations stalled at 600s stream watchdog mid-substantive-work. KR captures known state here so next elrond invocation can resume from this anchor rather than re-derive from scratch.

**Authored:** 2026-05-27 (Cycle 14 Wave 0)
**Author:** knight-rider (orchestration capture; NOT elrond audit authority)
**Authority:** none load-bearing — this is interim recovery state, not canonical elrond output
**For:** sub-agent elrond on re-fire (audit-report-only scope; see § 4)

---

## 1. Elrond progressive findings (from two stalled sessions)

### 1.1 First-session findings (stalled investigating catalogue.db dead-end)

- `catalogue.db` is the **multimedia asset catalogue**, NOT the weapon substrate library
- Elrond explicitly flagged investigating elsewhere for weapon substrate before stall

### 1.2 Second-session findings (stalled after substantive DB inspection)

- **2,293 v1_scope entries** in `weapon_knowledge_entries` (v1_scope=1)
- **1:1 join with weapon_sim_props**: all 2,293 v1_scope entries have weapon_sim_props rows
- **`damage_amplitude_min/max` are AMPLITUDE RATIOS (0.3-3.0 range), NOT absolute damage values in points** — important architectural finding
- **`proxy_attribute_class` (in weapon_knowledge_entries) and `weapon_sim_props.primary_stat` AGREE** across the join — redundancy or one is derived from the other
- **Distribution: martial-heavy** — DEX 1077 + STR 872 = ~85% martial; INT 160 + WIS 160 = ~14% caster
- Elrond was about to inspect: cluster table; named_template/unique entries (which would carry +to-skill mythological power) — stalled before completion

---

## 2. KR additional DB diagnostic (2026-05-27)

KR ran the following queries against `~/Games/reincarnated-loadout/data/telemetry.db` to fill in gaps:

### 2.1 v1_scope entry confirmation

```sql
SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1;
-- Result: 2293
```

### 2.2 weapon_sim_props.primary_stat distribution

```sql
SELECT primary_stat, COUNT(*) AS n FROM weapon_sim_props GROUP BY primary_stat ORDER BY n DESC;
-- DEX: 1075
-- STR:  891
-- WIS:  167
-- INT:  160
-- (Note: minor delta from elrond's count — 1075 vs 1077; 891 vs 872 — likely due to NULL handling or different filter scope; reconcile at re-fire)
```

### 2.3 damage_amplitude_min distribution

```sql
SELECT ROUND(damage_amplitude_min, 1) AS min_amp, COUNT(*) AS n FROM weapon_sim_props WHERE damage_amplitude_min IS NOT NULL GROUP BY ROUND(damage_amplitude_min, 1) ORDER BY min_amp;
-- 0.0: 7
-- 0.3: 328
-- 0.4: 133
-- 0.5: 228
-- 0.6: 66
-- 0.7: 938
-- 0.8: 591
-- 1.0: 2
```

**Interpretation:** Values cluster 0.3–0.8 with mode at 0.7 (938 entries). Consistent with elrond's "amplitude ratio" interpretation — these are scaling factors, NOT absolute damage values. **For doc 47 `base_physical_damage`, this means either (a) the substrate library needs a new absolute baseline column at L50 cap, OR (b) `base_physical_damage` is computed at gen time as (skill_level_calibration_constant × damage_amplitude_min/max).**

### 2.4 weapon_kind distribution (v1_scope only)

```sql
SELECT weapon_kind, COUNT(*) AS n FROM weapon_knowledge_entries WHERE v1_scope=1 GROUP BY weapon_kind ORDER BY n DESC;
-- category:           1139 (49.7%)
-- named_template:      927 (40.4%)
-- ammo_or_consumable:  148 (6.5%)
-- unique:               42 (1.8%)
-- shield:               17
-- talisman:             11
-- banner:                7
-- horn:                  1
-- unknown:               1
```

**Interpretation:** `weapon_kind` covers TYPE-of-entry (category vs named template vs unique vs accessories) but does NOT directly map to doc 47's `weapon_type_family` enum (martial-heavy / martial-light / ranged / caster-arcane / caster-faith / hybrid). Mapping work required — likely combine `weapon_kind` + `weapon_subclass` (in `weapons` table) + `primary_stat` to derive `weapon_type_family`.

### 2.5 weapons.stat_affinity (UNPOPULATED!)

```sql
SELECT stat_affinity, COUNT(*) AS n FROM weapons GROUP BY stat_affinity ORDER BY n DESC;
-- unknown: 5162  (ALL rows)
```

**Critical finding:** The `weapons` table's `stat_affinity` column is **completely unpopulated** (all 5,162 rows = 'unknown'). The authoritative attribute requirement source is `weapon_sim_props.primary_stat`, NOT `weapons.stat_affinity`. Audit-report disposition: do NOT rely on `weapons.stat_affinity`.

---

## 3. Field-by-field disposition (KR pre-staged per Discipline #11 empirical inspection)

For elrond re-fire — validate these dispositions OR amend:

| Doc 47 § 3 field | Disposition | Source / approach |
|---|---|---|
| **`base_physical_damage`** | **NEEDS NEW COLUMN** OR **COMPUTE AT GEN** | `weapon_sim_props.damage_amplitude_min/max` is a ratio (0.3–3.0), not absolute. Decision: either (a) add `weapon_sim_props.base_physical_damage_l50` column with calibrated L50 absolute values, OR (b) rocket Phase 2c computes at gen time from `(damage_amplitude × global_l50_calibration_constant)`. Elrond chooses + records rationale. |
| **`spell_damage_modifier`** | **NEEDS NEW COLUMN** | No existing field. Recommend `weapon_sim_props.spell_damage_modifier_pct` column; populate per-weapon-type defaults (martial=0, caster-arcane=high, caster-faith=high, hybrid=medium). |
| **`element_affinity_modifiers`** | **PARTIAL — needs structuring** | `weapons.dominant_element_affinities` is comma-separated list (NOT per-element pct). Recommend either (a) new `weapon_element_affinity_modifiers` table (weapon_id, element, pct), OR (b) JSON column on weapon_sim_props with `{"fire": pct, "water": pct, ...}` shape. Elrond chooses + records rationale. |
| **`to_skill_level_modifiers`** | **DEFERRED to rocket Wave 0.5** OR new column | Per-rarity-tier roll at gear instance gen time (rocket seam) is more substrate-clean than baking into substrate library. But unique-tier named weapons (e.g., mythological "Gáe Bolg always grants +1 to spear skills") may warrant substrate column. Elrond + rocket coordinate; recommend defer to Wave 0.5 unless unique-tier coverage requires substrate exposure. |
| **`attribute_requirement`** | **REUSE `weapon_sim_props.primary_stat`** | Direct 1:1 mapping (STR/DEX/INT/WIS); no enrichment needed. `weapons.stat_affinity` is UNPOPULATED and should NOT be used. |
| **`weapon_type_family`** | **NEEDS DERIVATION + NEW COLUMN** | Map from `weapon_kind` + `weapon_subclass` + `primary_stat` to doc 47 6-family enum. Recommend new column `weapon_sim_props.weapon_type_family` with CHECK constraint matching enum (martial-heavy / martial-light / ranged / caster-arcane / caster-faith / hybrid). Mapping table authored by elrond. |

---

## 4. SC-6 re-fire scope (TIGHTENED per stall recovery)

**Original SC-6 scope was too large** (audit + enrichment + MIGRATION + cross-seam coordination). Stalled twice. Decompose:

### SC-6 NARROW (audit-report only; this re-fire)

- [ ] Read this progressive-findings doc + dispatch
- [ ] Validate the per-field dispositions in § 3 OR amend per elrond domain expertise
- [ ] File audit report at `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md`
- [ ] Audit report contains: current state per-field; recommended approach per field; estimated enrichment effort; cross-seam impact summary (rocket Phase 2c at Wave 0.5; gamora damage_resolver at Wave 0.5)
- [ ] Append completion record to dispatch
- [ ] Commit + push
- [ ] **NO schema changes in this fire.** Enrichment deferred to next dispatch (SC-6b) OR rocket-coordinated at Wave 0.5 itself

### SC-6b (DEFERRED — fires after SC-6 NARROW closes)

- [ ] Apply schema extension per audit-report recommendations
- [ ] Write MIGRATION.md per ADR-004
- [ ] Cross-seam round-trip smoke at Wave 0.5 when rocket consumes

**Critical:** elrond is in Wave 0.5 owners list per framing brief § 2 Wave 0.5. SC-6b enrichment can happen IN Wave 0.5 (parallel with rocket's per-skill emission + substrate binding output). Wave 0.5 dispatch authoring does NOT need SC-6b complete; only SC-6 NARROW audit-report.

---

## 5. Anti-stall recommendations for elrond re-fire

Per Discipline #19 + observed stall pattern:

1. **Dump intermediate findings as you go** — write the audit-report file incrementally (header + § for each field as you investigate) rather than buffering all findings for end-of-session write
2. **Limit DB query batch size** — large GROUP BY operations on 90K rows can be slow; use targeted EXPLAIN + index-aware queries
3. **Defer enrichment + MIGRATION** to next dispatch — those are the open-ended portions; audit-report has bounded scope
4. **If audit requires extended LLM-generated mapping table (weapon_kind × weapon_subclass × primary_stat → weapon_type_family for hundreds of combinations), provide a SAMPLE mapping (top-20 most common) + algorithmic rule** rather than exhaustive per-row mapping in this fire — exhaustive mapping is SC-6b enrichment scope

---

## 6. Sign-off

**Author:** knight-rider (orchestration capture)
**Status:** WORKING — interim recovery state; elrond re-fire consumes this as anchor; audit report is the canonical output

**For:** sub-agent elrond on third invocation (audit-report-only scope) — resume from this anchor rather than re-derive from scratch. KR has captured substrate library state via Discipline #11 empirical inspection; elrond brings domain judgment to per-field dispositions + audit-report authoring.
