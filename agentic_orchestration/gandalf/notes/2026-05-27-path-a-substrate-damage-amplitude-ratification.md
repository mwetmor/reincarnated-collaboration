# Path A Ratification — Substrate damage_amplitude → absolute base_physical_damage

> **STATUS:** CURRENT — Matt 2026-05-27 ratified Path A per SC-6 substrate weapon audit architectural finding. Load-bearing for Cycle 14 Wave 0.5 + SC-6b substrate enrichment implementation.

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "ratify path A"
**Source artifact:** `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` § 1.6
**Companion docs:**
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile + base_physical_damage formula)
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md` (implementation vehicle)
- `canonical/00-ground-state.md` (this note registers as recognition record reference)

---

## 0. TL;DR

**Decision**: substrate library adds `base_physical_damage_l50` absolute column (per-weapon-family L50 baseline). Final damage at generation time computed as:

```
weapon.base_physical_damage = base_physical_damage_l50 × damage_amplitude_min/max (lottery at gen time)
```

Substrate carries BOTH the shape (`damage_amplitude_min/max` ratio) AND the magnitude (`base_physical_damage_l50` absolute). Rocket Phase 2c consumes both directly per doc 47 § 4.2 formula.

**Rejected**: Path B (substrate carries ratio only; engine computes magnitude from per-family multiplier table). Path A keeps calibration data co-located with substrate where weapon-family designers naturally work.

---

## 1. Architectural finding (per SC-6 audit § 1.6)

`weapon_sim_props.damage_amplitude_min/max` is a RATIO (scaling multiplier), not absolute HP damage. Values cluster 0.3–0.8; range observed 0.3–3.0. This is the per-weapon-variance shape, NOT the L50 baseline magnitude.

Doc 47 § 3.1 expects absolute base_physical_damage values per weapon family:
- STR heavy melee: ~100-300 HP
- DEX light/ranged: ~60-150 HP
- INT caster: ~20-80 HP
- WIS faith/channel: ~20-80 HP

**Mismatch**: substrate ratio (0.3-3.0 multiplier) cannot directly feed doc 47 § 4.2 `weapon.base_physical_damage` formula which expects absolute HP values.

---

## 2. Path A — adopted

### 2.1 Implementation

| Change | Owner | Status |
|---|---|---|
| Add `base_physical_damage_l50` (FLOAT NOT NULL) column to `weapon_sim_props` | elrond (SC-6b) | scope; not yet implemented |
| Per-weapon-family L50 baseline calibration (e.g., greatsword family = 200; dagger family = 100; staff family = 50; tome = 30; etc.) | elrond + gandalf design call OR elrond solo per family taxonomy | scope; not yet implemented |
| Populate `base_physical_damage_l50` per row (backfill across 2,293 v1_scope rows; can default by `primary_stat` family for fast initial population) | elrond (SC-6b) | scope |
| Update doc 47 § 3 to reference substrate-side `base_physical_damage_l50` column | gandalf | this note authorizes; doc 47 § 3 amendment queued (~10 min gandalf authoring) |
| Rocket Phase 2c consumes `base_physical_damage_l50 × damage_amplitude_min/max` lottery at gen time → emits `weapon.base_physical_damage` field on `gear_representative.main_weapon` | rocket (Wave 0.5) | dependent on SC-6b column landing |

### 2.2 Per-weapon-family L50 baseline (anchored intent; elrond + gandalf may refine)

Anchored intents per doc 47 § 3.1 per-attribute weapon profile:

| Weapon family | Primary attribute | L50 baseline (anchor) |
|---|---|---|
| Greatsword / Greataxe / Greathammer / Polearm / Two-handed melee | STR | ~200-300 |
| One-handed sword / Mace / Axe / Spear | STR | ~150-200 |
| Dagger / Rapier / Twin-blade | DEX | ~80-120 |
| Bow (longbow / shortbow) | DEX | ~100-150 |
| Crossbow | DEX | ~120-180 |
| Staff / Wand (arcane) | INT | ~30-60 |
| Tome / Orb / Scepter | INT | ~20-50 |
| Focus / Talisman / Holy symbol | WIS | ~20-50 |
| Channeling staff / Banner | WIS | ~30-60 |
| Horn (off-hand utility) | WIS | ~15-40 |

These are anchors. SC-6b calibration may refine per substrate library actual weapon-family distribution + per-cell gauntlet sim feedback.

### 2.3 Composition with doc 47 § 4.2 physical damage formula

Doc 47 § 4.2:
```
physical_skill_damage = weapon_base_physical_damage
                      × skill_damage_multiplier(skill_level)
                      × (1 + primary_attribute_bonus / 100)
                      × (1 + global_physical_damage_modifier / 100)
                      × tier_coefficient(skill_tier)
                      × element_conversion_factor
                      × crit_multiplier
```

Under Path A:
```
weapon.base_physical_damage = weapon.base_physical_damage_l50 × roll_in(damage_amplitude_min, damage_amplitude_max)
```

Where `roll_in()` produces a random multiplier within the substrate-supplied amplitude range at gen time. This adds per-instance variance to the otherwise-deterministic L50 baseline — the "did you roll a higher-damage variant of the same weapon family" pattern genre-canonical to ARPGs.

### 2.4 Composition with substrate composition policy v1 Option α / β / C

- **Option α martial cells** (STR/DEX primary): substrate weapon's `primary_stat` matches kit attribute; substrate weapon's `base_physical_damage_l50` is high; damage_scaling_type=physical routes correctly
- **Option β caster cells** (INT/WIS primary): substrate weapon's `primary_stat` matches kit attribute; substrate weapon's `base_physical_damage_l50` is low (~20-60); spell-damage modifier dominates per doc 47 § 4.3 magical formula; physical baseline barely contributes when skill is magical
- **Option C cross-attribute hybrid cells**: ω-penalty applies per substrate composition policy v1; weapon may have mismatched `primary_stat` to kit attribute; damage_scaling_type=hybrid routes per per-skill design

Path A composes cleanly with all three.

---

## 3. Why Path A over Path B

| Criterion | Path A | Path B |
|---|---|---|
| Substrate completeness | ✅ Substrate carries shape AND magnitude | ❌ Substrate carries shape only |
| Calibration data location | ✅ Co-located with substrate (where weapon-family designers work) | ❌ Engine-side; separate from substrate library |
| Rocket integration | ✅ Consumes 2 substrate fields directly | ❌ Consumes 1 substrate field + engine-side multiplier table |
| Weapon-family calibration UX | ✅ Designers edit substrate row, see calibration impact | ❌ Designers edit code, engineers maintain table |
| Composability with v1.1+ enrichment | ✅ Per-row L50 baselines naturally extensible | ❌ Per-family L50 baselines harder to refine per-row |
| Compose with doc 47 § 4.2 formula | ✅ Direct substitution | ⚠ Requires engine-side magnitude resolution before formula applies |

Path A wins on substrate-as-source-of-truth discipline + designer UX + composability.

---

## 4. Implementation gates

| Gate | Owner | Status |
|---|---|---|
| Path A ratification | Matt | ✅ 2026-05-27 |
| Recognition record authored (this doc) | gandalf | ✅ 2026-05-27 |
| SC-6b dispatch consumes Path A scope | elrond | gates on jack-ryan Wave 0.5 Gate-1 PASS (current state: PASS-with-REVISIONS amendments applied) |
| Doc 47 § 3 amendment referencing substrate column | gandalf | queued (~10 min authoring) |
| SC-6b implementation: column add + backfill | elrond | Wave 0.5 firing |
| Rocket Phase 2c consumes substrate column at gen time | rocket | Wave 0.5 firing |
| End-to-end test: gen-time damage = baseline_l50 × roll_in(amplitude_min, max) | gamora + jack-ryan Gate-2 | Wave 0.5 close gate |

---

## 5. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — recognition record capturing Matt 2026-05-27 Path A ratification
**Composition:** with doc 47 § 3 (per-attribute weapon profile) + SC-6 substrate audit § 1.6 (architectural finding) + SC-6b dispatch (implementation vehicle) + doc 47 § 4.2 (physical damage formula)

**For:** the Matt 2026-05-27 ratification of Path A — substrate library adds `base_physical_damage_l50` absolute column; per-weapon-family L50 baseline calibration; gen-time `weapon.base_physical_damage = base_physical_damage_l50 × damage_amplitude_min/max lottery`. Path A keeps calibration data co-located with substrate where weapon-family designers naturally work; composes cleanly with doc 47 + substrate composition policy v1 Option α/β/C. SC-6b enrichment dispatch becomes the implementation vehicle.

**Signed:** gandalf (story-and-design steward)
