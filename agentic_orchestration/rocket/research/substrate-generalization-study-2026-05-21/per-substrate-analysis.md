# Per-Substrate Analysis — Track A Findings

**Date:** 2026-05-21
**Author:** rocket
**Data sources:**
- `/Users/admin/Games/reincarnated-engine/data/telemetry.db` — historical R1/R2 seasons
- `/Users/admin/Games/reincarnated-engine/output/p2-fresh-diagnostic-regen-2026-05-19/season_100005/` — P2 cold-start diagnostic regen

---

## Measurement methodology

**BC coordinates measured (partial; pre-rebuild):**

Full 8-axis BC measurement requires P2 infrastructure (not yet built). This analysis uses proxy measurements available from current telemetry:

| BC proxy | What it measures | Axis affinity |
|---|---|---|
| `final_balance_modifier` | Effective power scaling required for balance convergence | Indirect Axis 4 proxy |
| `boss_wr` at equilibrium | Upper-tier kill capability | Axis 3A/3B signal |
| `mini_boss_wr` at equilibrium | Upper-tier kill capability (weaker signal) | Axis 3A/3B signal |
| `modifier_CV` | Variance in power scaling across same-substrate classes | Compression signature |
| `boss_wr_zero_pct` | Fraction of classes with full upper-tier collapse | Pattern-A signature |
| `kit_size` | Total skill count | Axis 2/2B proxy |
| `damage_role_fraction` | Fraction of slots with DPS roles | Axis 2B proxy |
| `geometry_distribution` | Geometry types used in kit | Axis 2 proxy |

**Discipline #11 note:** All boss/mini-boss WR measurements are from cold-start equilibrium convergence (P2) or warm-start convergence from historical telemetry. Generation-time pipeline-state measurements (which showed 6/10 floor_lock_recompose=True in P2 Phase 1 before cold-start) are NOT used — those are pipeline-state-conditioned, not equilibrium-state measurements.

---

## Substrate analyses

---

### FIRE

**Data sources:** 24 class-season pairs from historical telemetry (seasons 012345-100003, schema v2.10-2.13) + class_0002 from P2 season_100005

**Sample size:** N=24 (historical) + N=2 P2 classes (fire_mage + experimental)

**Historical BC proxy distribution (pre-disposition-3):**
- Modifier: mean=0.0521, SD=0.0059, CV=0.11, range=[0.0500, 0.0797]
- Swarm WR: mean=0.999, tight cluster near 1.0
- Elite WR: mean=0.915, SD=0.118
- Mini-boss WR: mean=0.108, SD=0.162, zero_pct=41.7%
- Boss WR: mean=0.385, SD=0.407, zero_pct=25.0%
- Pattern-A (boss_wr=0.0): 25% of class-season pairs

**P2 cold-start (disposition-3):**
- class_0002 fire_mage: modifier=0.0719, boss_wr=0.000, Pattern-A
- class_0010 experimental (fire): modifier=0.1338, boss_wr=0.000, Pattern-A
- Kit_size=5 for fire_mage (no chain structure); kit_size=9 for experimental

**Kit composition (P2):**
- fire_mage: 4/5 damage roles, 1/5 defensive, geometry mostly ground_targeted_circle + multi_projectile
- geometry distribution historical: DoT-heavy (ground_targeted_circle dominant at 14% of slots), strong defensive burden (20.9% of slots)

**Compression signature:**
- Modifier CV=0.11 (low variance; tight compression near floor)
- Boss WR variance is high (SD=0.407) indicating bimodal distribution — some classes succeed, many fail
- The fire_mage's 5-skill kit in P2 is an anomaly relative to the historical 10-12 skill kits

**Comparison to shadow baseline:**
- Modifier compression similar to shadow (shadow modifier=0.1956 in P2, fire=0.0719)
- Both show Pattern-A in P2
- Historical fire shows better boss performance than expected from P2 — this is the calibration gap

---

### WATER

**Data sources:** 20 class-season pairs from historical telemetry + class_0003 from P2 season_100005

**Sample size:** N=20 historical + N=1 P2

**Historical BC proxy distribution:**
- Modifier: mean=0.0519, SD=0.0034, CV=0.07, range=[0.0500, 0.0648]
- **Tightest modifier distribution of all canonical-four substrates (CV=0.07)**
- Boss WR: mean=0.448, SD=0.382, zero_pct=15.0%
- Mini-boss WR: mean=0.340, zero_pct=20.0%
- Pattern-A: 15% — **lowest Pattern-A rate of all substrates**

**P2 cold-start:**
- class_0003 water_mage: modifier=0.1338, boss_wr=0.000, Pattern-A
- Kit_size=11 with proper chain structure (2 chains, 4 tiers)

**Kit composition analysis:**
- Water has the highest sustain role fraction (10.3% of slots) + highest burst_damage count
- 3× burst_damage skills in the P2 water_mage kit — the most concentrated single-target burst among mage substrates
- Yet boss_wr=0.0 despite higher theoretical DPS from burst skills

**Compression signature:**
- Lowest modifier CV (0.07) — most compressed modifier distribution
- Paradox: tightest modifier compression paired with best historical boss performance
- Interpretation candidate: water's sustained-presence zone-denial combat pillar produces kits that are consistently calibrated (hence low mod variance) but their sustained-damage mechanisms eventually overcome boss HP within timeout

**Comparison to shadow:**
- Water shows better historical boss performance and lower Pattern-A than shadow would be expected to show (shadow has no historical data)
- Water modifier range is the narrowest of all substrates

---

### EARTH

**Data sources:** 20 class-season pairs from historical telemetry + class_0004 from P2 season_100005

**Historical BC proxy distribution:**
- Modifier: mean=0.0524, SD=0.0065, CV=0.12, range=[0.0500, 0.0797]
- Boss WR: mean=0.242, SD=0.353, zero_pct=40.0%
- Mini-boss WR: mean=0.224, zero_pct=25.0%
- Pattern-A: 40%

**P2 cold-start:**
- class_0004 earth_caster: modifier=0.1338, boss_wr=0.000, Pattern-A
- Kit_size=11 with chain structure

**Kit composition analysis:**
- Earth_caster P2 kit: only 4/11 damage roles (36% damage fraction) — LOWEST among all substrates
- 7/11 non-damage roles: 2 defensive, 2 sustain, 2 mobility, 1 utility
- High non-damage burden consistent with earth's ANCHOR_AND_DISRUPT combat pillar
- The low damage fraction creates a structural boss DPS floor problem even with a 11-skill kit

**Kit role distribution (historical):**
- earth has highest control role burden (10.4%) among canonical-four
- area_damage dominant (17.8%) but with many AoE spells that do not concentrate damage on single boss entity

**Compression signature:**
- Modifier CV=0.12, similar to fire
- Boss WR bimodal — 40% zero, 60% variable
- Earth's ANCHOR_AND_DISRUPT pillar biases toward control/root geometries that underperform against high-HP single-target bosses

---

### WIND

**Data sources:** 20 class-season pairs from historical telemetry + class_0005 from P2 season_100005

**Historical BC proxy distribution:**
- Modifier: mean=0.0722, SD=0.0582, CV=0.81, range=[0.0500, 0.2875]
- **Highest modifier CV of canonical-four (0.81) — wind produces the most modifier-diverse outcomes**
- Boss WR: mean=0.320, SD=0.414, zero_pct=40.0%
- Mini-boss WR: mean=0.238, zero_pct=40.0%
- Pattern-A: 40%

**P2 cold-start:**
- class_0005 wind_caster: modifier=0.1338, boss_wr=0.000, Pattern-A
- Kit_size=11 with chain structure
- Kit composition: 5/11 damage roles (45%), 3/11 defensive (27%) — high defensive burden

**Kit composition analysis:**
- Wind kit in P2: primary attack is multi_projectile, burst_damage is single_target
- Three vortex_pull skills (area_damage, area_damage, damage_over_time) — displacement geometry unlikely effective on boss entities
- High mobility burden (1 blink) consumes kit slots

**Compression signature:**
- Wind has the widest modifier range among canonical-four (0.05 to 0.29)
- This high CV indicates wind produces kits that require DIFFERENT modifier scales — evidence of internal diversity
- However Pattern-A rate (40%) is same as earth — the diversity in modifier doesn't translate to boss success reliability

---

### LIGHTNING

**Data sources:** P2 season_100005 only (class_0006); no historical per-tier data

**P2 cold-start:**
- class_0006 lightning_mage: modifier=0.0719, boss_wr=0.000, Pattern-A
- Kit_size=11 with proper chain structure (2 chains, 4 tiers)

**Kit composition analysis:**
- Lightning has the HIGHEST damage fraction of all substrates in P2: 8/11 skills are damage roles (73%)
- 4 chain_lightning skills (chain geometry = PREFER per substrate config)
- chain_lightning has potential to hit single boss target on multiple hops
- Theoretical DPS: 3,230 raw (3rd highest); with no elemental resistance on boss: 3,230 effective DPS
- Boss effective HP ≈ 68,650 under disposition-3; DPS × 240s = 775,200 >> boss HP
- Despite favorable geometry and highest damage fraction: boss_wr=0.0

**Compression signature:**
- Single data point; no CV computable
- Modifier=0.0719 (same as fire_mage in P2 — the equilibrium value for the highest-power substrate)
- kit_size=11 with 73% damage fraction is structurally the healthiest kit in P2
- Yet still 0.0 boss WR — this is important: even the best-composed kit in P2 fails the boss kill

**Implication:** If any substrate should NOT generalize the pathology, it's lightning (best kit shape, highest damage fraction, most burst-capable geometry). Lightning's failure at boss tier under P2 calibration is the strongest single piece of evidence that the pathology is calibration-level, not substrate-composition-level, at season_100005.

---

### HOLY

**Data sources:** R1 kit-redesign queue (2 historical class entries: class_0033, class_0044); P2 season_100005 class_0007

**Historical context (from kit-redesign queue):**
- class_0033 (holy_caster): modifier=1.43, mini_boss_wr=0.533 (pass), boss_wr=0.000
- class_0044 (holy_caster): similar pattern
- class_0060 (holy_controller): modifier=4.0 (saturated), boss_wr=0.0

**P2 cold-start:**
- class_0007 holy_caster: modifier=0.1338, boss_wr=0.000, Pattern-A
- Kit_size=5 (NO chain structure — same as shadow_mage and fire_mage in P2)
- Kit composition: multi_projectile primary, single_target burst, ground_targeted_circle area, circle DoT, self_buff defensive

**Key observation: holy_caster has 5-skill kit in P2**
The template for holy (burst_damage/area_damage roles) composes kit=[10,12] per archetype_composer.py. The actual kit has 5 skills — same kit-size anomaly as shadow_mage and fire_mage in this season. This appears to be a seed-specific or pipeline-specific generation artifact for these three substrates in season_100005, not a systematic substrate rule.

**Compression signature:**
- Holy modifiers historically run 1.43-4.0 (much higher than canonical-four's 0.05-0.08 range)
- This high modifier requirement indicates holy_caster generates kits that need much higher power scaling — weak kit DPS by construction
- Pattern-A present in historical and P2 data

---

### SHADOW

**Data sources:** R1 kit-redesign queue (class_0018, class_0045 explicitly listed); P2 season_100005 (class_0001 shadow_mage, class_0009 shadow_controller); recompose-hive findings

**Historical context (from kit-redesign queue):**
- class_0018 (shadow_mage): modifier=4.0, WR=0.0 across ALL tiers — "totally broken kit"
- class_0045 (shadow_mage): modifier=4.0, same — fully saturated AND dysfunctional

**P2 cold-start:**
- class_0001 shadow_mage: modifier=0.1956, boss_wr=0.000, sub-mechanism 5b (lever-signal-gap)
- class_0009 shadow_controller: modifier=0.3812, boss_wr=0.000, additionally fails elite tier (0.670 overshoot)
- Kit_size=5 for shadow_mage (NO chain structure)
- Kit_size=5 for shadow_controller (NO chain structure)

**Key observations:**
1. shadow_mage has the lever-signal-gap sub-mechanism (5b), not just compression (5a) — uniquely, its lever library returned delta=0 on all 3 attempts
2. shadow_controller adds elite-tier overshoot on top of boss collapse — the CC-heavy kit over-controls weak enemies but has no impact on boss tier
3. Both shadow classes have 5-skill kits in P2 (same as holy and fire_mage)

**Compression signature:**
- Shadow modifier higher than canonical-four (0.1956 for shadow_mage vs 0.05-0.08 for fire/water/earth)
- The higher equilibrium modifier means shadow kits are less DPS-efficient by default
- Shadow's CONCEALMENT_AND_DRAIN combat pillar with preferred geometries (tendril, void_pool, creep) maps to sustained drain mechanics, not burst boss-kill
- Shadow kit's avoided geometries include melee_arc and shaft — geometries that provide direct concentrated damage

---

### PHYSICAL

**Data sources:** 20 class-season pairs from historical telemetry + class_0008 from P2 season_100005

**Historical BC proxy distribution:**
- Modifier: mean=0.4400, SD=0.3665, CV=0.83, range=[0.0797, 1.750]
- Boss WR: mean=0.000, SD=0.000, zero_pct=100.0%
- Mini-boss WR: mean=0.005, zero_pct=95.0%
- **Pattern-A: 100%** — physical is the canonical all-Pattern-A substrate

**P2 cold-start:**
- class_0008 physical_warrior: modifier=0.3812, boss_wr=0.000, Pattern-A
- Kit_size=11 with chain structure
- Highest raw theoretical DPS (13,154) but boss_wr=0.0

**Kit composition:**
- Highest defensive burden: 3/11 defensive roles (27%) + 3/11 area_damage roles
- Melee_strike primary_attack with 0.10s cooldown → theoretical DPS=10,560
- Physical damage formula uses armor mitigation (armor/(armor+3000))
- Boss armor 9,729 → mitigation = 9729/(9729+3000) = 76.4% — MUCH higher than elemental resistance
- Effective DPS for physical_warrior: 13,154 × (1 - 0.764) = 3,100/s
- 3,100 × 240s = 744,040 >> boss_eff_HP 68,650

**Physical's persistent 100% Pattern-A is the strongest evidence that the pathology is cross-substrate.** Physical was the MOST physical-DPS-capable substrate in the historical catalogue (highest modifiers, highest kit power scaling), yet achieved 0.000 boss WR in every single historical season.

---

## Cross-substrate compression signature table

| Substrate | Mod CV | Boss WR zero % | Pattern-A % | Historical calibration | P2 calibration |
|---|---|---|---|---|---|
| fire | 0.11 | 25% | 25% | pre-disp3 (partial Pattern-A) | 100% (full Pattern-A) |
| water | 0.07 | 15% | 15% | pre-disp3 (best of canonical-4) | 100% |
| earth | 0.12 | 40% | 40% | pre-disp3 | 100% |
| wind | 0.81 | 40% | 40% | pre-disp3 | 100% |
| physical | 0.83 | 100% | 100% | 100% in both calibrations | 100% |
| lightning | N/A | N/A (no hist.) | N/A | N/A | 100% |
| holy | HIGH | HIGH (cat-queue) | HIGH | historical entries: modifier ≥1.43 | 100% |
| shadow | HIGH | HIGH (cat-queue) | HIGH | historical entries: modifier ≥1.96 | 100% |

---

## Track A verdict

The Pattern-A (boss-DPS-floor collapse) compression signature is present across ALL 7 substrates in P2 season_100005. The compression is uniform — no substrate escapes the boss_wr=0.0 outcome under disposition-3 calibration regardless of kit size (5 vs 11 skills), damage role fraction (20%-80%), or geometry type (chain_lightning vs melee_strike vs void_pool).

The historical data shows gradient: water (15% Pattern-A) performs better than earth/wind (40%), which performs better than physical (100%). Shadow and holy show HIGH severity in the kit-redesign queue catalogue. Lightning has no historical baseline.

The Discipline #13b caveat: the gradient in historical data (water better than earth, etc.) is a candidate for element-specific substrate differences, but requires controlled ablation to confirm — the calibration change between historical and P2 data confounds direct comparison.
