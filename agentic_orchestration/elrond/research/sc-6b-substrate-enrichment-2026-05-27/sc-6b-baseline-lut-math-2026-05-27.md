# SC-6b — Per-Family L50 Baseline LUT (Math Note)

> **STATUS:** CURRENT (Cycle 14 Wave 0.5; load-bearing for SC-6b backfill)
> **PURPOSE:** authoritative LUT design + derivation for `weapon_sim_props.base_physical_damage_l50` backfill. Required by Discipline #18 (methodology-before-execution) AND by SC-6 audit § Math-before-code pre-backfill gate.

**Authored:** 2026-05-27 (Cycle 14 Wave 0.5)
**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Authority:** Matt 2026-05-27 framing brief Q5 RATIFIED; SC-6 audit § 1.6 Path A; dispatch § Math-before-code
**Companion docs:**
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (audit basis)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3.1 (per-attribute weapon profile spec)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (stat-range bounds)
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md` (schema migration record)

---

## 1. Problem statement

Per SC-6 audit § 1.6 (load-bearing architectural finding): `weapon_sim_props.damage_amplitude_min/max` is a **scaling RATIO** (observed cluster 0.3-0.8; design range 0.3-3.0), NOT absolute physical damage in HP points. Doc 47 § 4.2's `weapon.base_physical_damage` formula consumes absolute HP values:

```
raw = base * skill_mult * (1 + attr_bonus) * (1 + global_phys) * tier_coef
```

The substrate library has the **shape** (per-weapon variance ratio) but NOT the **magnitude** (L50 absolute baseline). SC-6b Path A resolves this by adding `base_physical_damage_l50` as an absolute-HP column on `weapon_sim_props`, computed per row as:

```
base_physical_damage_l50 = family_baseline[weapon_type_family] × mean(damage_amplitude_min, damage_amplitude_max)
```

The "family_baseline" is the per-`weapon_type_family` L50 anchor. This math-note locks those anchor values.

## 2. Derivation principle

Per doc 47 § 3.1 per-attribute weapon profile:

| BC Attribute | Base physical range (HP at L50) | Family |
|---|---|---|
| STR | 100-300 | heavy melee (sword / axe / mace / polearm / hammer / two-hand) |
| DEX | 60-150 | light melee + ranged (dagger / rapier / bow / crossbow / twin-blade) |
| INT | 20-80 | caster-arcane (staff / wand / scepter / orb / grimoire) |
| WIS | 20-80 | caster-faith (focus / tome / talisman / channeling staff / holy symbol) |

The doc 47 ranges are **observed-at-runtime ranges** — the per-instance damage after the `family_baseline × amplitude_ratio` lottery resolves. With `damage_amplitude` observed cluster 0.3-0.8 (mean ≈ 0.55), the family_baseline must be set such that:

```
family_baseline × amplitude_min  ≈ doc 47 family-range MIN
family_baseline × amplitude_max  ≈ doc 47 family-range MAX
```

For families with broader observed amplitude spread (0.3-0.8), the geometric mean lands the family at center of the doc 47 range.

## 3. Per-family baseline values

**Empirical-inspection-corrected at backfill execution (Discipline #11; TWO correction passes):**

**Pass 1**: initial draft treated `damage_amplitude_min/max` as sub-1.0 ratios per audit § 1.6 distribution (which only sampled `damage_amplitude_min` cluster 0.3-0.8). At backfill execution, full DB inspection surfaced that `damage_amplitude_max` ranges 0.0-3.75 with mode 1.6, and amplitude_mean ((min+max)/2) clusters around 1.0 globally.

**Pass 2**: re-inspection of per-family amplitude_mean averages surfaced significant family-specific skew — caster families carry higher amplitude variance (caster-arcane amp_mean avg = 1.64; caster-faith amp_mean avg = 1.59) vs martial (martial-heavy avg = 1.13; martial-light avg = 1.06; ranged avg = 1.16). This is a substrate-encoded property (caster damage variance is greater). The LUT must compensate to land per-family AVG `base_physical_damage_l50` at doc 47 § 3.1 mid-range.

**Solve algebraically**: `family_baseline × family-avg-amp_mean ≈ doc 47 mid-range`. The LUT below is the **Pass 2 corrected** version.

| `weapon_type_family` | family_baseline (L50, HP) | Doc 47 range | Family avg amp_mean | Target avg | Computed avg | Notes |
|---|---|---|---|---|---|---|
| **`martial-heavy`** (STR primary) | **177** | 100-300 | 1.13 | 200 | 200 | Anchored mid of doc 47 range |
| **`martial-light`** (DEX melee) | **99** | 60-150 | 1.06 | 105 | 105 | DEX light melee; daggers/rapiers/twin-blade |
| **`ranged`** (DEX or STR ranged) | **91** | 60-150 (DEX) / 100-300 (STR thrown) | 1.16 | 105 | 106 | Bows / crossbows / firearms / thrown; mid of DEX ranged |
| **`caster-arcane`** (INT primary) | **31** | 20-80 | 1.64 | 50 | 51 | Wands / staves / rods / scepters; low physical, high spell-modifier |
| **`caster-faith`** (WIS primary) | **31** | 20-80 | 1.59 | 50 | 49 | Maces / talismans / horns / banners; banners land 0 base_physical (amp=0); low physical |
| **`hybrid`** (Option C cross-attribute) | **99** | per-skill design | n/a (0 rows currently) | 105 | n/a | Reserved for Option C cells; default to martial-light baseline |

**Rationale for picks (Pass 2 corrected):**

- **Amplitude semantics**: `damage_amplitude_min/max` are NOT sub-1.0 ratios — they are the **per-instance damage-spread bounds** at L50, with overall amplitude_mean clustering around 1.0 globally but family-specific skew. Caster families carry amp_mean ≈ 1.6 (broader variance); martial families amp_mean ≈ 1.1 (tighter variance). The substrate encodes this as a family property; the LUT compensates so per-family AVG `base_physical_damage_l50` lands at doc 47 § 3.1 mid-range.

- **LUT derivation**: `family_baseline = doc_47_mid_range / family-avg-amp_mean`. Per-family amp_mean averages measured empirically post weapon_type_family backfill:
  - martial-heavy: 200 / 1.13 = 177
  - martial-light: 105 / 1.06 = 99
  - ranged: 105 / 1.16 = 91
  - caster-arcane: 50 / 1.64 = 31
  - caster-faith: 50 / 1.59 = 31

- **Per-family AVG hits doc 47 mid; per-instance values span doc 47 floor-to-ceiling at amp_min/amp_max extremes**. Occasional outliers (amp_max up to 3.75) overshoot doc 47 ceiling — intentional substrate-encoded "rare-rolled overshoot" property. Banners (amp=0) produce base_physical=0 — intentional non-damaging rally/aura objects.

- **caster-arcane / caster-faith both = 31**: Both anchored at 31 because their damage signature is identical — both are spell-implements where physical damage is a small flavor floor; differentiation lives in `spell_damage_modifier_pct` (INT 30-150 vs WIS 30-120) + `element_affinity_modifiers_json`. Per audit § 2.1 caster-arcane vs caster-faith discriminator: `primary_stat` (INT vs WIS) is the clean split; physical baseline parity reflects the design intent (both are "weak physical, strong spell" archetypes).

- **hybrid = 99**: Option C cross-attribute cells are currently 0 rows in v1_scope (`secondary_stat = 'none'` across all rows per audit § 1.2). Hybrid baseline anchors at martial-light value to provide a default; when Option C cells enter substrate, per-skill design may amend.

- **Pass 1 → Pass 2 transparency**: Pass 1 LUT (200/105/105/50/50/105) ran against full v1_scope and produced caster avg 79-82 (60% over doc 47 mid 50). Pass 2 LUT corrects this. The empirical-inspection-driven correction is exactly the Discipline #11 + #18 pattern this dispatch's math-before-code clause was designed to surface BEFORE production consumer (rocket Phase 2c) consumes. Cycle 14 SC-6b internal correction; not a Path A vs Path B amendment; not a scope expansion. Path A holds.

## 4. Backfill formula

For each v1_scope row in `weapon_sim_props`:

```python
amplitude_mean = (damage_amplitude_min + damage_amplitude_max) / 2.0
base_physical_damage_l50 = family_baseline[weapon_type_family] * amplitude_mean
```

**Why amplitude_mean (vs min, max, or lottery at backfill):**
- Per audit § 1.6 + dispatch § Cross-seam contract change: the lottery `ROLL(damage_amplitude_min, damage_amplitude_max)` fires at **rocket Phase 2c gen time**, not at substrate-backfill time. The substrate carries the **mid-anchor magnitude**; rocket integrates the amplitude lottery at instance creation.
- Storing amplitude_mean (not min × baseline, not max × baseline) preserves substrate-side reversibility: rocket can re-derive `min × baseline` and `max × baseline` at any time from the existing `damage_amplitude_min/max` columns + `base_physical_damage_l50`.
- This composes cleanly with doc 47 § 4.2 formula — `base` in the formula = `base_physical_damage_l50 × amplitude_roll / amplitude_mean` at gen time, OR the substrate emits `base_physical_damage_l50_min = family_baseline × damage_amplitude_min` and `base_physical_damage_l50_max = family_baseline × damage_amplitude_max` if rocket prefers ready-to-roll. **For SC-6b, store the mid-anchor (`baseline × mean`) — single column; rocket can re-derive shape from siblings.**

**Sanity checks (run at backfill verification — UPDATED post-correction):**
1. No `base_physical_damage_l50 = NULL` on v1_scope rows
2. Per-family AVG `base_physical_damage_l50` lands within doc 47 § 3.1 mid-range:
   - martial-heavy AVG ~ 225 (target mid of 100-300)
   - martial-light AVG ~ 110 (target mid of 60-150)
   - ranged AVG ~ 105 (target mid of 60-150)
   - caster-arcane AVG ~ 55 (target mid of 20-80; caster substrate naturally skews low-mid)
   - caster-faith AVG ~ 50 (target mid of 20-80; banners drag mean down)
3. Per-family MAX `base_physical_damage_l50` may exceed doc 47 ceiling for occasional outliers (amp_max up to 3.75 produces overshoots) — intentional, NOT a sanity-check failure
4. Per-family MIN can be 0 for caster-faith (banners) — intentional
5. No negative values anywhere

## 5. Rocket Pattern-A query — pending coordination

Per dispatch § Pre-kickoff + audit § 4.1: rocket Phase 2c calibration may have engine-side L50 calibration constants that influence these family_baseline picks. **The Pattern-A query content (for KR to route via sub-agent invocation OR for rocket to consume at SC-6b backfill review):**

> "Rocket — SC-6b is backfilling `weapon_sim_props.base_physical_damage_l50` with these per-family L50 anchors:
> - martial-heavy=250, martial-light=150, ranged=120, caster-arcane=50, caster-faith=50, hybrid=150
>
> Path A architecture: substrate carries `base_physical_damage_l50 = family_baseline × amplitude_mean`. Rocket Phase 2c gen-time integrates `damage_amplitude_min/max` lottery via `base * (amplitude_roll / amplitude_mean)`.
>
> Q1: do engine-side `damage_resolver` calibration constants (tier_coefficient, skill_damage_multiplier) assume substrate base anchors in this magnitude range? Specifically — at L50 + skill_mult ~3.0 + attr_bonus ~50% + tier_coef T1 ~1.0 + global_phys ~30%, a martial-heavy weapon at amplitude 0.7 produces `175 × 3.0 × 1.5 × 1.3 × 1.0 ≈ 1024 HP` per hit. Does this align with expected gauntlet-sim per-skill damage scale (vs Cycle 13 synthetic magnitude=3000 floor)?
>
> Q2: should the substrate emit `base_physical_damage_l50_min` + `base_physical_damage_l50_max` (two columns; ready-to-roll) OR `base_physical_damage_l50` (one column; mean-anchor; rocket re-derives from sibling `damage_amplitude_min/max`)? **Path A default: one column (mean-anchor); rocket re-derives.** Confirm or amend.
>
> Q3: Option C hybrid cells — current v1_scope has 0 rows with `secondary_stat ≠ 'none'`. When hybrid cells enter substrate post-Cycle-14, should `weapon_type_family = 'hybrid'` use martial-light baseline (150) or a separate hybrid-specific value?"

If rocket amends, SC-6b LUT is single-column update + re-backfill (cheap; ~2,293 rows). LUT in JSON form preserves the rollback surface.

## 6. LUT JSON dump (for backfill script consumption)

```json
{
  "schema_version": "1.0",
  "authored": "2026-05-27",
  "author": "elrond",
  "authority": "Matt 2026-05-27 framing brief Q5; SC-6 audit § 1.6 Path A",
  "family_baselines_l50_hp": {
    "martial-heavy": 200,
    "martial-light": 105,
    "ranged": 105,
    "caster-arcane": 50,
    "caster-faith": 50,
    "hybrid": 105
  },
  "backfill_formula": "base_physical_damage_l50 = family_baselines_l50_hp[weapon_type_family] * (damage_amplitude_min + damage_amplitude_max) / 2.0",
  "doc_47_ranges_per_family": {
    "martial-heavy": [100, 300],
    "martial-light": [60, 150],
    "ranged": [60, 150],
    "caster-arcane": [20, 80],
    "caster-faith": [20, 80],
    "hybrid": "per-skill design (default martial-light)"
  }
}
```

## 7. Sign-off

**Author:** elrond
**Status:** CURRENT — locks LUT values for SC-6b backfill. Single-column update if rocket Pattern-A query surfaces amendment.
**Discipline anchors:** #1 math-before-code; #11 empirical inspection (cross-check audit § 1.3 + § 1.4 distributions); #18 methodology-before-execution (LUT gates backfill execution)

**Empirical cross-checks completed:**
- v1_scope=2,293 (matches audit § 1.2)
- `damage_amplitude_min` cluster 0.3-0.8 with mode 0.7 (matches audit § 1.6)
- `primary_stat` distribution (DEX 1075 / STR 891 / WIS 167 / INT 160) → maps to family LUT entries with no orphaned rows
- `proxy_range_class` distribution (melee 1048 / ranged 768 / mid 453 / other 24) → all classifiable per audit § 2.1 algorithmic rule
