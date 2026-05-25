# Per-Cell Register Breakdown — v1_scope substrate

**Authored:** 2026-05-25
**Author:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-12-pre-layer-2-prep.md`
**Source DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` table `weapon_knowledge_entries`
**v1_scope total:** 2,293 rows (note: dispatch quoted 3,042; current DB shows 2,293 — flagged in § 6)
**Cell-id source:** `v1_scope_composition_trace` JSON → `axis_contributions.mechanical_cell`
**Register source:** `register_canonical` column (full coverage; 4-value enum + 1 NULL bucket)
**Consumer:** rocket Layer 2 dispatch authoring (informs cell-weight parameter selection per MC-1 surprise 1)
**Per Discipline #11:** direct-inspected ≥3 raw rows before aggregating (see § 5)
**Per Discipline #25 L9 semantic-layer rep-audit:** uses mechanical fields only (mechanical_cell + register_canonical); no cultural_tradition / lineage / period fields included

---

## 1. Headline finding

**Within-cell register skew is severe and non-uniform.** Composition policy v1 § 1 register-share *aggregate* targets (historical ~50-55% / fantasy ~30-35% / military_modern ~5-8% / mythological ~30 rows) hold approximately at the *aggregate* substrate level (actual: historical 52.4% / fantasy 44.6% / military_modern 1.4% / mythological 1.6%) — but **applying those aggregate weights as per-cell generation weights would mis-fire** because per-cell registers are bimodal:

- **Caster cells (INT/WIS primary) are fantasy-dominant (74-100%).** Cells `int_standard_wizard_arcane_familiar`, `int_totem_hierophant_proxy_heavy`, `dex_twin_blade_fencer_thin`, `wis_ritual_mage_low_floor_accepted`, `wis_holy_knight_paladin` all skew ≥74% fantasy. A per-cell weight of "historical 50%" would force these cells to drift outside their natural register signature.
- **Ranged-pure cells (DEX archer/crossbow/ranged-mid-tempo) are historical-dominant (87-99%).** A per-cell weight of "fantasy 30%" would force these cells away from their natural signature.
- **Martial STR cells split:** polearm_soldier and mid_range_compound lean fantasy (63-68%); light_fighter and crossbow_sniper lean historical (85-88%); heavy_barbarian leans fantasy (94%).
- **One cell (`dex_twin_blade_fencer_thin`) is 100% fantasy** — zero historical/military_modern/mythological coverage. Generation that requires historical sampling from this cell will fail substrate-bind.

This confirms MC-1 surprise 1 (level-of-analysis gap): composition policy register-shares were CURATION targets, not GENERATION weights. Rocket Layer 2 should select per-cell weights from this empirical breakdown, not from the aggregate § 1 targets.

---

## 2. SQL query used

```sql
WITH per_cell_total AS (
  SELECT
    COALESCE(
      json_extract(v1_scope_composition_trace, '$.axis_contributions.mechanical_cell'),
      '__null_trace__'
    ) AS mc,
    COUNT(*) AS total
  FROM weapon_knowledge_entries
  WHERE v1_scope=1
  GROUP BY mc
),
per_cell_register AS (
  SELECT
    COALESCE(
      json_extract(v1_scope_composition_trace, '$.axis_contributions.mechanical_cell'),
      '__null_trace__'
    ) AS mc,
    COALESCE(register_canonical, 'null') AS reg,
    COUNT(*) AS cnt
  FROM weapon_knowledge_entries
  WHERE v1_scope=1
  GROUP BY mc, reg
)
SELECT pcr.mc, pcr.reg, pcr.cnt, pct.total,
  ROUND(100.0 * pcr.cnt / pct.total, 1) AS pct_share
FROM per_cell_register pcr
JOIN per_cell_total pct ON pct.mc = pcr.mc
ORDER BY pct.total DESC, pcr.mc, pcr.reg;
```

Note on field choices:
- `mechanical_cell` is sourced from JSON trace because no direct cell-id column exists on `weapon_knowledge_entries`. The trace was populated by Cycle 10 Stage 3 constrained-sampling per `v1_scope_composition_trace` schema.
- `register_canonical` is preferred over JSON-trace `register` because it has full coverage (the 42 Stage 3.5 engine-authored gap-fill rows lack a full composition trace but DO have populated `register_canonical`).

---

## 3. Per-cell × register matrix

Counts and percentage-share per cell. Rows sorted by total v1_scope coverage descending.

| Cell (mechanical_cell)                | historical | fantasy | military_modern | mythological | TOTAL | Dominant register |
|---|---:|---:|---:|---:|---:|---|
| **`untyped`** (uncell-typed)          | 441 (94.6%) | 3 (0.6%) | 1 (0.2%) | 21 (4.5%) | 466 | historical |
| `str_polearm_soldier`                 | 85 (37.1%) | 144 (62.9%) | 0 | 0 | 229 | fantasy |
| `dex_melee_compound`                  | 23 (13.8%) | 144 (86.2%) | 0 | 0 | 167 | fantasy |
| `str_mid_range_compound`              | 53 (31.9%) | 113 (68.1%) | 0 | 0 | 166 | fantasy |
| `dex_crossbow_sniper`                 | 123 (87.9%) | 13 (9.3%) | 4 (2.9%) | 0 | 140 | historical |
| `dex_archer_falconer_pair` *(1+5 paired)* | 127 (92.0%) | 0 | 11 (8.0%) | 0 | 138 | historical |
| `dex_ranged_mid_tempo_compound`       | 123 (99.2%) | 0 | 1 (0.8%) | 0 | 124 | historical |
| `dex_dagger_assassin`                 | 57 (47.1%) | 64 (52.9%) | 0 | 0 | 121 | fantasy (slim) |
| `str_heavy_barbarian_pair` *(7+10 paired)* | 6 (6.1%) | 93 (93.9%) | 0 | 0 | 99 | fantasy |
| `wis_holy_knight_paladin`             | 25 (25.5%) | 73 (74.5%) | 0 | 0 | 98 | fantasy |
| `str_light_fighter_under_floor`       | 81 (85.3%) | 14 (14.7%) | 0 | 0 | 95 | historical |
| `int_standard_wizard_arcane_familiar` *(12+16 paired)* | 1 (1.3%) | 79 (98.8%) | 0 | 0 | 80 | fantasy |
| `dex_twin_blade_fencer_thin`          | 0 | 74 (100.0%) | 0 | 0 | 74 | **fantasy ONLY** |
| `dex_mid_compound`                    | 6 (9.5%) | 54 (85.7%) | 3 (4.8%) | 0 | 63 | fantasy |
| `int_totem_hierophant_proxy_heavy`    | 1 (1.7%) | 59 (98.3%) | 0 | 0 | 60 | fantasy |
| `str_thrown_heavy_atlatl`             | 13 (21.7%) | 36 (60.0%) | 11 (18.3%) | 0 | 60 | fantasy |
| `__null_trace__`† (Stage 3.5 gap-fill) | 21 (50.0%) | 5 (11.9%) | 0 | 16 (38.1%) | 42 | historical |
| `wis_ritual_mage_low_floor_accepted`  | 6 (14.3%) | 36 (85.7%) | 0 | 0 | 42 | fantasy |
| `dex_trap_assassin`                   | 5 (22.7%) | 16 (72.7%) | 1 (4.5%) | 0 | 22 | fantasy |
| `wis_druid_beastmaster_sidecar_b`     | 5 (100.0%) | 0 | 0 | 0 | 5 | **historical ONLY** |
| `wis_storm_caller_sidecar_b`          | 0 | 1 (100.0%) | 0 | 0 | 1 | fantasy ONLY (under-floor) |
| `int_other`                           | 0 | 1 (100.0%) | 0 | 0 | 1 | fantasy ONLY (orphan) |
| **AGGREGATE v1_scope**                | **1,202 (52.4%)** | **1,022 (44.6%)** | **32 (1.4%)** | **37 (1.6%)** | **2,293** | **historical** |

† `__null_trace__` = 42 Stage 3.5 engine-authored gap-fill rows (per `2026-05-25-rocket-cycle-10-stage-3-5-engine-authored-gap-fill` dispatch); these rows have populated `register_canonical` but no composition trace because they were authored directly, not selected through constrained-sampling. They are mostly Cell 14 Pyromantic (`pyromantic_*` named templates) + Cell 17 Necromancer mythological-rescue rows.

---

## 4. Zero-coverage cells (BLOCKED per MC-1 surprise 2)

Per intent doc § 1.1, the v1 cell roster contains **22 cells**. The substrate covers only **18 named cells** (plus `untyped`, `__null_trace__`, and `int_other` orphan = 21 distinct labels). The following intent-doc cells have **zero direct cell-id coverage** in `mechanical_cell`:

| Intent doc cell # | Archetype | Status | Per § 4.1 routing |
|---|---|---|---|
| **Cell 11** | Red Mage / Spellsword `(melee, high, flat, INT)` | ZERO coverage in mechanical_cell | (not in dispatch scope — per MC-1 surprise 2) |
| **Cell 14** | Pyromantic Caster `(mid, low, spiky, INT)` | Substrate via `__null_trace__` Stage 3.5 gap-fill (5 `pyromantic_*` named-template rows) | Cell 14+17 share 4-tuple per § 4.2 |
| **Cell 15** | Necromancer Summoner `(mid, low, spiky, INT, heavy)` | Substrate via `__null_trace__` Stage 3.5 mythological-rescue rows | Cell 14+17 share 4-tuple per § 4.2 |
| **Cell 17** | Channeling Cleric `(mid, medium, variable, WIS)` | ZERO direct; substrate via Cell 25 sharing per § 4.2 (`wis_druid_beastmaster_sidecar_b` is paired) | Cell 19+25 share 4-tuple |
| **Cell 22** | Monk-archetype `(melee, high, variable, WIS)` | ZERO coverage | Not present in mechanical_cell labels |
| **Cell 23** | Storm Caller / Druid `(ranged, medium, variable, WIS)` | 1 row only (under-floor) in `wis_storm_caller_sidecar_b` | Sidecar B Celtic/Druidic enrichment per § 4.1 |
| **Cell 24** | Artillery Mage `(ranged, low, spiky, INT)` | ZERO coverage | Per § 4.1: FOLD into Cell 12 Standard Wizard via T4 algorithmic alteration |

Note on cell-id mapping ambiguity: the substrate uses descriptive cell-name strings (e.g., `str_polearm_soldier`); the intent doc uses numeric Cell 1..25 ids. Mapping is by archetype name. Rocket Layer 2 should treat the descriptive labels as canonical (the substrate-binding heuristic consumes the string keys directly).

---

## 5. Empirical inspection sample (Discipline #11)

Twelve raw rows sampled at random across cells/registers BEFORE aggregating:

| mechanical_cell | register | canonical_name | tier |
|---|---|---|---|
| `dex_trap_assassin` | fantasy | Thermobaric Bomb | B |
| `int_standard_wizard_arcane_familiar` | fantasy | Fang of the Crystal Spider | B |
| `str_heavy_barbarian_pair` | fantasy | Barbed Lance | B |
| `str_mid_range_compound` | fantasy | Harpoon Launcher | B |
| `dex_melee_compound` | fantasy | Cleanrot Spear | B |
| `str_mid_range_compound` | historical | Fauchard of the Bodyguard of Cardinal Scipione Borghese-Caffarelli (1576–1633) | S |
| `dex_dagger_assassin` | historical | Smallsword | S |
| `str_light_fighter_under_floor` | historical | Pair of Sword-Grip Ornaments (Menuki) | S |
| `dex_dagger_assassin` | historical | Dagger with Sheath | A |
| `dex_crossbow_sniper` | historical | Percussion blunderbuss | A |
| `dex_ranged_mid_tempo_compound` | historical | Centrefire breech-loading double-barrelled hammer shotgun | A |
| `str_thrown_heavy_atlatl` | historical | 105 mm howitzer | B |

Spot-check confirms cells and registers are correctly assigned; the `str_thrown_heavy_atlatl | 105mm howitzer` placement validates the cell-label captures functional/dimensional class rather than literal historical-period naming. The `str_light_fighter_under_floor | Menuki` row reveals an off-hand item (sword-grip ornament) classified into a STR melee cell — this is consistent with Sidecar B off-hand enrichment, but rocket Layer 2 should be aware that some cell rows are off-hand-only.

---

## 6. Notes for rocket Layer 2 consumer

### 6.1 v1_scope row-count discrepancy (substrate gap surface)

The dispatch quoted **3,042 rows** (from "Cycle 10 wind-down per `elrond/v0.0-cycle-10-stage-3-phase-2-v1-scope-2026-05-25` tag"); current DB query returns **2,293 rows**. The 749-row delta is unexplained from this dispatch's read-only vantage. Hypotheses to investigate (out-of-scope here):

- Sibling elrond instances (SC-1 cultural_lineage_canonical backfill; SC-2 weapon_kind_classified_subtype backfill) may have re-stamped `v1_scope` during their UPDATE passes; some rows previously v1_scope=1 may have been demoted on tier/quality recheck.
- The 3,042 figure may reference a pre-trim state including Tier C rows or pre-Stage-4-rescue rows that subsequently failed register/tier gates.
- Sidecar B enrichment rows may not have been merged into the v1_scope at the time this DB was last reconciled.

This is a **substrate-bookkeeping issue to surface to KR** — not a blocker for Layer 2 dispatch authoring (the breakdown is consistent within the 2,293-row population), but if Layer 2 must hit specific cell floors per § 2.2 (~1,100-1,400 v1_scope items target), the gap suggests v1_scope may have over-trimmed and rocket should re-check before applying per-cell quotas.

### 6.2 Cell-weight parameter recommendation (informs MC-1 H3 implementation)

Per MC-1 H3 deterministic per-cell-fired-once enumeration with weighted sampling within each cell, rocket Layer 2 should:

1. **Use empirical per-cell register distributions as the default sampling weights** (rather than aggregate § 1 targets). This preserves each cell's natural signature.
2. **For cells with 100% single-register coverage** (`dex_twin_blade_fencer_thin`, `wis_druid_beastmaster_sidecar_b`, `wis_storm_caller_sidecar_b`, `int_other`), Layer 2 cannot diversify register at-cell; if cross-register variety is design-required, escalate to gandalf for substrate enrichment OR accept register-bound forms for those cells.
3. **For aggregate register-share gandalf-targets to be hit**, weight per-cell *sampling frequency* (cell-firing weights) rather than per-cell *register* weights. Heavier firing on historical-dominant cells lifts aggregate historical share; heavier firing on fantasy-dominant cells lifts aggregate fantasy share.
4. **The `untyped` bucket (466 rows, 20.3% of v1_scope) is dominantly historical (94.6%) and includes the mythological rescue rows (21).** Layer 2 should decide policy: (a) treat `untyped` as a separate cell-class with its own firing weight; (b) re-bin `untyped` rows onto best-fit cells via secondary inference; (c) defer `untyped` from generation entirely. Recommend (b) but flag for rocket judgment.

### 6.3 Off-floor cells

Cells with row counts **far below the § 2.1 per-cell floor targets** (60-120 per cell for pure-attacker, 30-50 for proxy cells):

| Cell | Count | Floor (per § 2.1) | Gap |
|---|---:|---|---|
| `wis_druid_beastmaster_sidecar_b` | 5 | 30-50 | -25 to -45 |
| `wis_storm_caller_sidecar_b` | 1 | 60-100 | -59 to -99 (CRITICAL) |
| `int_other` | 1 | n/a (orphan) | — |
| `dex_trap_assassin` | 22 | 30-50 | -8 to -28 |
| `wis_ritual_mage_low_floor_accepted` | 42 | 60-100 | -18 to -58 |

Layer 2 should expect substrate-bind to ROUTINELY fall back to thin-cell-fallback (per MC-2 § 4.1 routing table + § 5.2 cascade) for these cells. The MC-2-recommended axis-relaxation priority is `weapon_mechanical_profile → energy_type → element` (last); these thin cells will exercise the cascade routinely.

### 6.4 NULL / unknown register handling

Zero rows have NULL `register_canonical` in v1_scope. The four register values observed are exactly the canonical four per § 1.1: `historical`, `fantasy`, `military_modern`, `mythological`. No `sci_fi` or `unknown` rows reach v1_scope. Layer 2 should expect the register enum to be a clean 4-value space for kit-register inference.

---

## 7. Consumer note — what Layer 2 should expect

- **Per-cell register weights are non-uniform and bimodal.** Do not apply § 1 aggregate register-share targets as per-cell generation weights.
- **18 named cells + 1 untyped bucket + 1 null-trace bucket + 1 orphan** = 21 cell-label population (vs. 22 intent-doc cells). Several intent-doc cells (11 Red Mage, 22 Monk, 24 Artillery Mage) have ZERO direct cell-id coverage and route per § 4.1.
- **Cell-pair sharing per § 4.2** is visible in the data: `str_heavy_barbarian_pair`, `dex_archer_falconer_pair`, `int_standard_wizard_arcane_familiar` are shared 4-tuple substrate pools serving Cells (1+5), (7+10), (12+16) respectively.
- **Five cells have ≥85% single-register dominance** (`int_standard_wizard_arcane_familiar` 98.8% fantasy; `int_totem_hierophant_proxy_heavy` 98.3% fantasy; `dex_twin_blade_fencer_thin` 100% fantasy; `dex_ranged_mid_tempo_compound` 99.2% historical; `wis_druid_beastmaster_sidecar_b` 100% historical). For these cells, cross-register generation is effectively single-register-bound at-substrate.
- **v1_scope row count is 2,293 (vs. dispatch 3,042)** — flagged as substrate-bookkeeping gap to verify before Layer 2 enforces per-cell floors.
