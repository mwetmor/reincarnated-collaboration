# 47 — Damage Scaling Architecture (Physical / Magical / Hybrid)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — foundational architectural commitment; surfaces what was implicit in `skill-system-2026-05-24.md` + `weapon-substrate-composition-policy-v1-2026-05-24.md` (Option α / β / C cell-type matching); becomes prerequisite for Cycle 13 content gap closure (Track D scope) + Cycle 14 Phase 5 cohesion coalescence; see `canonical/00-ground-state.md`

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — three-path damage scaling routing (physical / magical / hybrid); composes with substrate composition policy v1 Option α / β / C cell-type matching + skill-system composition pattern + doc 46 stat-range bounds
**Authority:** Matt + gandalf Pattern-B design conversation continuation 2026-05-27 — Matt verbatim "I get that physical skills might want to scale weapon damage, but magical skills? Why would ice spike have anything to do with wooden staff physical damage?" — surfaced the architectural distinction my prior framing flattened
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern (element × geometry × tempo × amplitude × tier_coefficient); this doc surfaces the SCALING-PATH dimension implicit in the composition
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — Option α martial 5-tuple / Option β caster attribute-level / Option C cross-attribute ω-penalty; this doc defines the damage routing implications of those cell-type matching choices
- `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system (STR / INT / WIS / DEX); this doc defines per-attribute weapon type expectations
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation; damage scaling integrates at Phase 2c substrate binding + Phase 2d gear gen + Phase 3 sim validation
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid; per-level attribute scaling math deferred per § 4 #1 (this doc's attribute scaling formulas reference that gate)
- `canonical/46-concentration-architecture-2026-05-27.md` — Concentration architecture Layer 1 stat-range bounds; this doc operates against those caps
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — bounded-viability-with-specialization design directive (forward-link 2026-05-28); doc 50 is the architectural-experience layer over this doc's mechanical substrate; § 3 forward-link block added at section head

---

## 0. TL;DR

Skills declare a **`damage_scaling_type`** (physical / magical / hybrid). Fight engine routes damage calculation per the type. Three scaling paths:

1. **Physical skill damage** = weapon_base_physical_damage × skill_damage_multiplier × (1 + attribute_bonus) × tier_coefficient
2. **Magical skill damage** = base_spell_damage × skill_damage_multiplier × (1 + INT_or_WIS_bonus) × element_affinity × (1 + weapon_spell_modifier) × tier_coefficient
3. **Hybrid skill damage** = per-skill design decision; cross-attribute ω-penalty applies per Option C substrate composition policy

**Critical architectural correction**: weapon raw damage scales PHYSICAL skills (where the weapon IS the damage source) but NOT magical skills (where the skill IS the damage source and the weapon is a conduit/modifier). A wooden staff's 50 physical damage NEVER enters an Ice Spike's damage calculation — the staff modifies HOW the spell scales via `+%spell damage` / `+%element damage` / `+to-skill-level` modifiers, but does NOT provide raw damage that gets multiplied by spell skill coefficient.

This is genre canon (D2 / PoE / LE / GD) and aligns with our locked canonical architecture. Surfaces the SCALING-PATH dimension that was implicit in `skill-system-2026-05-24.md` composition pattern (element × geometry × tempo × amplitude × tier_coefficient — note absence of weapon damage in this composition).

---

## 1. Architectural through-line

> **The weapon is the damage source for physical skills; the skill is the damage source for magical skills. The weapon's role differs by attribute.**

### 1.1 Why this is load-bearing

Cycle 13 Track A remediation used a flat `magnitude=3000` synthetic primary_attack regardless of kit attribute. This was a stop-gap to make the gauntlet sim infrastructure work. When real content lands (Track D scope), the damage math must route correctly per skill type — otherwise we reproduce the chaos of "wooden staff scaling Ice Spike."

### 1.2 Genre canon

Every successful ARPG separates physical vs magical scaling paths:

| Game | Physical scales from | Magical scales from | Caster weapon role |
|---|---|---|---|
| **Diablo 2 (LoD)** | Weapon physical damage + STR + skill level | Base spell damage + skill level + synergies | +to-skills / +%element damage / +mana — NOT raw scaling |
| **Diablo 3** | "Weapon damage" + Strength/Dexterity | "Weapon damage" + Intelligence (caster weapons have appropriately scaled "weapon damage" stat) | Wand = "high-weapon-damage" but effectively spell power |
| **Diablo 4** | Weapon damage + DEX/STR | Weapon damage + INT/Willpower scaled appropriately | Caster weapons + skill ranks + attribute scaling dominate |
| **Path of Exile** | Weapon physical damage + STR/DEX + accuracy | Base spell damage + INT + skill gem level + supports + global %spell damage modifiers | Wand/staff provides +%spell damage / +%element damage / +to-gem-level — NEVER raw physical scaling |
| **Last Epoch** | Weapon physical damage + STR/DEX | Base spell damage + INT + skill level + spell modifiers | Caster weapons provide +%spell damage / +element affinity |
| **Grim Dawn** | Weapon physical damage + STR/Cunning + skill level | Base spell damage + Spirit/Cunning + skill level + %element modifiers | Caster weapons via Mythical affixes |

**Convergent pattern**: physical and magical have INDEPENDENT damage equations. Caster weapons modify spell damage VIA MULTIPLIERS, not by providing raw scaling.

### 1.3 What `skill-system-2026-05-24.md` already implies

The locked skill composition pattern is:

```
element × geometry × tempo × amplitude × tier_coefficient + algorithmic mechanic-alteration
```

**Weapon base damage is NOT in this composition.** The canonical already separates skill damage from weapon damage at the composition level. This doc surfaces what was implicit.

---

## 2. Damage scaling matrix

### 2.1 Three scaling types

Every skill declares its `damage_scaling_type` as one of:

| Type | Description | BC attribute alignment |
|---|---|---|
| **`physical`** | Skill's damage is weapon-derived; physical attack mediated by weapon swing/strike | STR (heavy melee) + DEX (light melee + ranged) cells |
| **`magical`** | Skill's damage is spell-derived; weapon is conduit/modifier; spell power independent of weapon physical | INT (caster) + WIS (faith/channel) cells |
| **`hybrid`** | Mixed; per-skill design decision; cross-attribute cells with ω-penalty per substrate composition policy Option C | Cross-attribute cells (Red Mage / Holy Knight / Spellsword / Monk archetypes) |

### 2.2 Damage formulas

**Physical skill damage:**

```
physical_skill_damage = weapon_base_physical_damage
                      × skill_damage_multiplier(skill_level)
                      × (1 + primary_attribute_bonus / 100)
                      × (1 + global_physical_damage_modifier / 100)
                      × tier_coefficient(skill_tier)
                      × element_conversion_factor (if T4 ELEMENT_CONVERSION applies)
                      × crit_multiplier (if crit fires)
```

Where:
- `weapon_base_physical_damage`: substrate-bound weapon's physical damage stat (varies; martial weapon high, caster weapon low)
- `primary_attribute_bonus`: STR for heavy melee; DEX for light melee + ranged; per BC attribute mapping
- `global_physical_damage_modifier`: sum of gear `+%physical damage` partition affixes + chain passives + T4 Cat A effects
- `tier_coefficient`: T1 / T2 / T3 / T4 scaling per skill-system § 8

**Magical skill damage:**

```
magical_skill_damage = base_spell_damage(element, skill_tier)
                     × skill_damage_multiplier(skill_level)
                     × (1 + caster_attribute_bonus / 100)
                     × (1 + weapon_spell_damage_modifier / 100)
                     × (1 + element_affinity_modifier / 100)
                     × (1 + global_spell_damage_modifier / 100)
                     × tier_coefficient(skill_tier)
                     × element_conversion_factor (if T4 ELEMENT_CONVERSION applies)
                     × dual_element_factor (if T4 DUAL_ELEMENT_ADDITION applies)
                     × crit_multiplier (if crit fires)
```

Where:
- `base_spell_damage`: spell base damage per element + tier (independent of weapon; calibrated at generation time)
- `caster_attribute_bonus`: INT for arcane casters; WIS for faith/channel casters; per BC attribute mapping
- `weapon_spell_damage_modifier`: substrate-bound caster weapon's `+%spell damage` modifier (or `+%element damage` for element-specialized weapons)
- `element_affinity_modifier`: gear `+%fire damage` / `+%cold damage` / etc. partition affixes + chain passives + T4 Cat C effects
- `weapon_base_physical_damage` is NOT in this equation — the wooden staff's 50 physical damage doesn't enter Ice Spike's calculation

**Hybrid skill damage:**

```
hybrid_skill_damage = per-skill design decision; one of:
  1. Pure physical path with element_conversion_factor for elemental flavor
  2. Pure magical path with martial_weapon modifier (cross-attribute ω-penalty applies)
  3. Sum of physical AND magical paths × hybrid_balance_factor (cross-attribute ω-penalty applies)
```

Hybrid is decided per-skill at generation time. Composes with substrate composition policy Option C cross-attribute matching with ω-penalty per the cell's mechanical fingerprint.

### 2.3 Damage scaling per skill type — declared at generation time

The Phase 2a per-skill mechanical content emission (Track D.2 scope) emits each skill with explicit `damage_scaling_type`:

| Skill | damage_scaling_type | Why |
|---|---|---|
| Whirlwind (barbarian melee) | physical | Weapon-mediated melee strike |
| Arrow Volley (archer ranged) | physical | Weapon-mediated bow shot |
| Fireball (fire mage) | magical | Spell-cast; weapon is staff/wand conduit |
| Ice Spike (water mage) | magical | Spell-cast; weapon is conduit |
| Lightning Chain (storm caller) | magical | Spell-cast |
| Holy Smite (cleric) | magical | Faith-cast |
| Magic Missile (basic mage) | magical | Spell-cast |
| Spellsword Slash (red mage) | hybrid | Cross-attribute; melee + spell |
| Holy Strike (holy knight) | hybrid | Melee + faith-mediated |
| Spinning Crane Kick (monk) | hybrid | Martial + ki/spiritual |

---

## 3. Weapon type implications per BC attribute

> **Forward-link (2026-05-28):** the 4-damage-path mechanical partition documented in this § 3 is the MECHANICAL SUBSTRATE for the bounded-viability-with-specialization design directive at `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md`. Doc 50 operates the ARCHITECTURAL-EXPERIENCE layer over this mechanical substrate: the 4 paths must produce comparable base DPS within ~1.5× variance (doc 50 § 4 target 1) AND distinct per-kit specialization profiles (doc 50 § 4 target 4) AND no-strict-dominance bidirectional clause (doc 50 § 4 targets 3+5). Path α work-stream (W-α1 damage formula refactor + W-α2 KPM ceiling raise/remove + W-α3 unified calibration pass + W-α4 design-target validation framework) refactors against this § 3 substrate to land doc 50 directive compliance. Composition: § 3 partitions damage routing; doc 50 specifies the cohort-output the partition must produce.

### 3.1 Per-attribute weapon profile

| BC Attribute | Primary weapon family | Base physical | Base spell modifier | +attribute scaling |
|---|---|---|---|---|
| **STR** | Heavy melee (sword / axe / mace / polearm / hammer) | **HIGH** (e.g., 100-300) | LOW (~0-10%) | STR scaling on physical |
| **DEX** | Light melee + ranged (dagger / rapier / bow / crossbow / twin-blade) | **MODERATE** (e.g., 60-150) | LOW (~0-10%) | DEX scaling on physical; speed/crit bonuses |
| **INT** | Caster implement (staff / wand / scepter / orb / grimoire) | **LOW** (e.g., 20-80) | **HIGH** (~30-150%) | INT scaling on magical; +to-skill-level; +mana; +element affinity |
| **WIS** | Faith / channel implement (focus / tome / talisman / channeling staff / holy symbol) | **LOW** (e.g., 20-80) | **HIGH** (~30-120%) | WIS scaling on magical; channel-efficiency / faith stats |

### 3.2 Substrate weapon binding implications

Per `weapon-substrate-composition-policy-v1-2026-05-24.md` cell-type matching:

| Option | Cell type | Weapon binding criterion |
|---|---|---|
| **Option α** | Martial cells (STR/DEX primary, physical-element) | Weapon-slot requires 5-tuple mechanical-fingerprint match — substrate weapon's mechanical profile must align with kit's BC fingerprint |
| **Option β** | Caster cells (INT/WIS primary, non-physical-element) | Weapon-slot requires ATTRIBUTE-LEVEL match only — substrate caster weapon binds by attribute affinity, not mechanical fingerprint |
| **Option C** | Cross-attribute hybrid cells | Weapon-slot permits cross-attribute wielding with ω-penalty per BDI ω-field resource-dimension |

Damage scaling implications:
- Option α martial cells use `damage_scaling_type=physical` → weapon base physical damage drives scaling
- Option β caster cells use `damage_scaling_type=magical` → base_spell_damage drives scaling; weapon provides spell-damage modifiers only
- Option C hybrid cells use `damage_scaling_type=hybrid` with per-skill design decision; ω-penalty applies if cross-attribute wielding is detected

---

## 4. Fight engine damage resolution

### 4.1 Routing logic

For each skill execution in the fight engine:

```
def calculate_skill_damage(player, weapon, skill, target):
    if skill.damage_scaling_type == "physical":
        return calculate_physical_damage(player, weapon, skill, target)
    elif skill.damage_scaling_type == "magical":
        return calculate_magical_damage(player, weapon, skill, target)
    elif skill.damage_scaling_type == "hybrid":
        return calculate_hybrid_damage(player, weapon, skill, target)
    else:
        raise ValueError(f"Unknown damage_scaling_type: {skill.damage_scaling_type}")
```

### 4.2 Physical damage calculation

```python
def calculate_physical_damage(player, weapon, skill, target):
    base = weapon.base_physical_damage
    skill_mult = skill.damage_multiplier
    attr_bonus = player.stats[skill.scaling_attribute] / 100  # STR or DEX
    global_phys = player.gear_aggregates["physical_damage_pct"] / 100
    tier_coef = TIER_COEFFICIENTS[skill.tier]

    raw = base * skill_mult * (1 + attr_bonus) * (1 + global_phys) * tier_coef

    # Apply T4 conversions if active
    if player.active_t4.category_a == "ELEMENT_CONVERSION":
        raw *= element_conversion_factor(player.active_t4)

    # Apply crit
    if rng() < player.crit_chance:
        raw *= player.crit_multiplier

    # Apply target defenses
    final = apply_target_defenses(raw, target, damage_type=skill.element or "physical")
    return final
```

### 4.3 Magical damage calculation

```python
def calculate_magical_damage(player, weapon, skill, target):
    base_spell = BASE_SPELL_DAMAGE[skill.element][skill.tier]  # independent of weapon
    skill_mult = skill.damage_multiplier
    caster_attr = player.stats[skill.scaling_attribute] / 100  # INT or WIS
    weapon_spell_mod = weapon.spell_damage_modifier / 100
    element_affinity = player.gear_aggregates[f"{skill.element}_damage_pct"] / 100
    global_spell = player.gear_aggregates["spell_damage_pct"] / 100
    tier_coef = TIER_COEFFICIENTS[skill.tier]

    raw = (base_spell * skill_mult
           * (1 + caster_attr)
           * (1 + weapon_spell_mod)
           * (1 + element_affinity)
           * (1 + global_spell)
           * tier_coef)

    # Apply T4 effects
    if player.active_t4.category_bc == "ELEMENT_CONVERSION":
        raw *= element_conversion_factor(player.active_t4)
    if player.active_t4.category_bc == "DUAL_ELEMENT_ADDITION":
        raw *= dual_element_factor(player.active_t4)

    # Apply crit
    if rng() < player.crit_chance:
        raw *= player.crit_multiplier

    # Apply target defenses (uses skill.element for resistance check)
    final = apply_target_defenses(raw, target, damage_type=skill.element)
    return final
```

### 4.4 Hybrid damage calculation

Hybrid skills compose physical + magical via per-skill design decision. Three patterns:

```python
def calculate_hybrid_damage(player, weapon, skill, target):
    if skill.hybrid_pattern == "physical_with_element_flavor":
        # Treat as physical; apply element_conversion for narrative flavor
        return calculate_physical_damage(player, weapon, skill, target)
    elif skill.hybrid_pattern == "magical_with_martial_weapon":
        # Treat as magical; weapon physical doesn't scale; apply ω-penalty
        dmg = calculate_magical_damage(player, weapon, skill, target)
        if is_cross_attribute_wielding(player, weapon):
            dmg *= OMEGA_PENALTY
        return dmg
    elif skill.hybrid_pattern == "sum_paths":
        # Sum physical + magical with hybrid_balance_factor
        phys = calculate_physical_damage(player, weapon, skill, target)
        magic = calculate_magical_damage(player, weapon, skill, target)
        return (phys * skill.hybrid_balance_factor +
                magic * (1 - skill.hybrid_balance_factor))
    else:
        raise ValueError(f"Unknown hybrid_pattern: {skill.hybrid_pattern}")
```

---

## 5. Composition with locked architecture

### 5.1 Skill-system composition pattern (skill-system-2026-05-24)

The locked composition pattern (element × geometry × tempo × amplitude × tier_coefficient) operates at the SKILL DEFINITION layer. This doc adds:
- `damage_scaling_type` field per skill
- Routing logic at fight resolution time
- Per-attribute weapon profile expectations

The composition pattern doesn't change; this doc adds the SCALING-PATH dimension implicit in it.

### 5.2 Substrate composition policy v1 (Option α / β / C)

This doc operationalizes the cell-type matching policies:
- Option α martial cells → physical scaling path
- Option β caster cells → magical scaling path
- Option C hybrid cells → hybrid scaling path with ω-penalty

### 5.3 Concentration architecture (doc 46)

Stat-range bounds (doc 46 Layer 1) apply to damage scaling outputs:
- Crit chance capped at 95%
- Crit multiplier capped at 500%
- Physical/spell damage modifiers compose additively with their respective cap formulas
- Damage outputs respect the bounded stat surface

### 5.4 L50 hybrid framework (doc 41)

Per-level attribute scaling math is deferred per doc 41 § 4 #1 (Cycle 14+ design call). When per-level scaling lands, the `primary_attribute_bonus` / `caster_attribute_bonus` formulas integrate with per-level attribute growth.

### 5.5 Doc 40 architectural foundation

Composes with:
- **D7 spec-driven gear gen (Phase 2d)** — gear modifiers route to physical or spell pools per gear type; gear modifier surface partitions by damage scaling path (physical_damage_pct / spell_damage_pct / element_damage_pct / weapon_spell_modifier). Composes with doc 42 stat-sheet modifier partition (Category 1 Damage sub-divisions).
- **D9 capability toolkit (legendary tier)** — capabilities operate on the scaling path; capability semantics declared per damage_scaling_type alignment (weapon-bound capability inherits weapon's damage_scaling_type alignment).
- **D55 weapons-only true-active rule** — true-active skills declared on weapons inherit weapon's damage_scaling_type alignment (physical weapon → physical-scaled true-active; caster weapon → magical-scaled true-active, unless skill explicitly declares otherwise).
- **D63-D86 multi-T4 architecture** — T4 effects route per damage_scaling_type (Category A character-wide; Category B chain-multiplicative within routed path; Category C element-conversion/addition at element resolution step within appropriate path). 4-phase T4 algorithm canonical form (D81) is NOT amended; integration point is at fight engine routing (Track D.4 gamora scope).

**✅ LANDED 2026-05-27 (Cycle 14 SC-2):** composition-amendments above filed in-place at doc 40 per § 0.1 amendment-pass-record. Bidirectional cross-references operational. See `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 0.1.3 for the doc 47 composition amendment index + § 0.1.2 for the parallel doc 46 inheritance amendment index. The D7 / D9 / D55 / D63-D86 entries are amended in-place at doc 40 § 3.7 and § 8.9 with cross-references back to this section.

---

## 6. Discipline candidate #38 — Damage-scaling-path discipline

**Candidate**: skills must declare `damage_scaling_type` (physical / magical / hybrid). Fight engine MUST route damage calculation per the declared type. NEVER apply a flat "weapon damage × multiplier" formula across all skill types. Composes with substrate composition policy v1 (Option α / β / C cell-type matching).

**Failure mode this guards against**: flat-weapon-scaling for all skills produces "wooden staff scales Ice Spike" chaos (Cycle 13 _SyntheticPlayerClass pattern) where the damage equation makes no thematic or mechanical sense for caster archetypes.

**Why this discipline matters now**: the synthetic primary_attack stub used in Cycle 13's gauntlet sim flattened all skills to one scaling path. When real per-skill content lands (Track D.2 scope), the routing MUST be correct from the start — retrofitting later means re-running Cycle 14 Phase 5 cohesion (cohesion judge consumes the damage equations).

**Queued for jack-ryan SC-2 expansion** alongside #33-#37 from doc 46.

---

## 7. Implementation discipline — Cycle 14 / Track D scope

### 7.1 Per-skill emission (Track D.2; rocket scope)

Phase 2a per-skill mechanical content emission must include:

| Field | Source |
|---|---|
| `damage_scaling_type` | Per skill design; declared at generation time based on skill role + element + kit attribute |
| `scaling_attribute` | STR / DEX / INT / WIS per skill mapping |
| `damage_multiplier` | Per skill_level scaling |
| `tier` | T1 / T2 / T3 / T4 |
| `tier_coefficient` | Per skill-system § 8 |
| `element` | Per kit element or T4 conversion |
| `geometry_type` | Per skill geometry |
| `hybrid_pattern` (hybrid only) | physical_with_element_flavor / magical_with_martial_weapon / sum_paths |
| `hybrid_balance_factor` (hybrid sum_paths only) | 0.0-1.0 split |

### 7.2 Substrate weapon binding (Track D.3; rocket + elrond scope)

Phase 2c substrate weapon emission must include:

| Field | Source |
|---|---|
| `base_physical_damage` | Substrate weapon's physical damage stat (substrate library data) |
| `spell_damage_modifier` | Substrate caster weapon's `+%spell damage` (substrate library data) |
| `element_affinity_modifiers` | Per-element `+%damage` per substrate weapon |
| `to_skill_level_modifiers` | Substrate caster weapon's `+to-skill-level` affixes |
| `attribute_requirement` | Substrate weapon's STR/DEX/INT/WIS requirement |
| `weapon_type_family` | martial-heavy / martial-light / ranged / caster-arcane / caster-faith / hybrid |

### 7.3 Fight engine routing (Track D.4; gamora scope)

`fight_engine.simulate_fight` damage_resolver routing:
- Check skill.damage_scaling_type at each skill execution
- Call appropriate path (calculate_physical / magical / hybrid)
- Apply target defenses based on skill.element
- Apply T4 effects per kit's active T4
- Respect stat-range bounds per doc 46 Layer 1

### 7.4 Cohesion-judge implications (Cycle 14 Phase 5)

The Phase 5 cohesion-judge LLM (per doc 46 Layer 6) consumes the skill content + weapon content + damage equations. It MUST narrate skills consistent with their damage_scaling_type:
- Physical skills narrated as weapon-mediated strikes
- Magical skills narrated as spell-cast / channeled effects with weapon as conduit
- Hybrid skills narrated as the specific hybrid_pattern in play

This ensures the cohesion narrative aligns with the mechanical reality.

---

## 8. Operational notes per seam

### 8.1 To rocket (generation seam)

- Per-skill emission (Track D.2) must include `damage_scaling_type` field at generation time
- Phase 2a kit composition determines per-skill scaling type based on skill role + kit attribute + element
- For hybrid cells (Option C), additional `hybrid_pattern` + `hybrid_balance_factor` fields
- Schema match v2_narrow_phase_5 lineage where applicable; extend with new scaling fields

### 8.2 To gamora (simulation seam)

- Fight engine damage_resolver routing per § 4 logic
- Per-skill damage path selection at execution time
- Stat-range bounds enforced per doc 46 Layer 1
- Real damage calculation replaces synthetic_mode magnitude=3000 stub (Track A remediation pattern retired when Track D lands)

### 8.3 To elrond (substrate seam)

- Substrate weapon library queries must expose: base_physical_damage / spell_damage_modifier / element_affinity_modifiers / to_skill_level_modifiers / attribute_requirement / weapon_type_family
- Per-weapon stat enrichment may be needed if substrate library doesn't already carry these (audit needed)

### 8.4 To star-lord (export seam)

- Loadout app season schema (per Track C star-lord transform) must include per-skill `damage_scaling_type` + substrate weapon stats so drax can display real damage projections

### 8.5 To drax (player surface seam)

- Loadout app damage display routes per skill type (physical damage tooltip vs magical damage tooltip)
- Spirit-guide projection (per D28-D32) narrates damage scaling correctly per type

### 8.6 To jack-ryan (discipline + critique-pair seam)

- Discipline candidate #38 (damage-scaling-path discipline) queued for ratification alongside #33-#37
- Gate-1 critique on per-skill emission validates damage_scaling_type assignments

### 8.7 To knight-rider (orchestration seam)

- Track D.2 + D.3 + D.4 scope absorbed into Cycle 14 Wave 0 / Wave 1 (per § 9 below)
- Cycle 14 framing brief consumes this doc as architectural foundation alongside doc 46

---

## 9. Cycle 13 close + Cycle 14 reframing — proposed plan

### 9.1 Cycle 13 status

**Cycle 13 close as-is**: PASS-with-WARN already ratified by jack-ryan (commit `482801c`); KR wind-down landed (commit `249fc92`). Track A remediation closed the empirical-sim-execution gap.

The content gaps Cycle 13 didn't deliver (per-skill mechanical content / substrate weapon binding output / elements expansion / damage scaling routing) are real but NOT a Cycle 13 close blocker — they are prerequisite scope for Cycle 14 Phase 5 cohesion coalescence (cohesion judge consumes the content layer).

**Recommendation**: Cycle 13 closes as-is. The honest close framing is "FRAMEWORK + ARCHITECTURE complete; content layer thin pending Cycle 14 Wave 0 prerequisites."

### 9.2 Cycle 14 reframing

Per Q9 Pattern A lock: Cycle 14 = Phase 5 cohesion coalescence. **Reframed**: Cycle 14 = Phase 5 cohesion coalescence + doc 46 concentration architecture amendments + Track D content gap closure (the Cycle 13 scope that wasn't fully delivered).

### 9.3 Cycle 14 wave structure (revised from doc 46 § 12)

| Wave | Scope | Source doc |
|---|---|---|
| **Wave 0** | Cycle 14 scope-doc + doc 40 amendments + doc 47 ratification + sidecar dispatches | doc 46 § 12.1 + this doc § 7 |
| **Wave 0.5 (NEW)** | **Track D content gap closure**: elements expansion (foundation passed through) + per-skill mechanical content emission with `damage_scaling_type` field + substrate weapon binding output to character JSON + fight engine damage scaling routing | doc 47 § 7 + this doc |
| **Wave 1** | Stat-range bounds + affix migration + capability scope reduction + trigger vocabulary + concentration probability table + synergy scan extension | doc 46 § 12.1 |
| **Wave 2** | New set_generator module (T4-strategy-aligned set keying) + class-agnostic spec-driven drops | doc 46 § 12.1 |
| **Wave 3** | Phase 5 cohesion-judge LLM architecture (layered cohesion per doc 46 Layer 6); consumes Wave 0.5 real content | doc 46 § 12.1 |
| **Wave 4** | T4-attuned gear cohesion + D21 acquisition curve calibration | doc 46 § 12.1 |
| **Wave 5** | Gauntlet sim re-calibration with real content (synthetic_mode retired) + cohesion validation | doc 46 § 12.1 + this doc |

Estimated Cycle 14 wall-clock: **~4-6 weeks** (vs original 3-5; Wave 0.5 adds ~1-2 weeks of content emission work).

### 9.4 What Cycle 14 delivers (the substantive close)

By Cycle 14 end:
- All 7 elements emitted across season generation (lightning / holy / shadow unlock)
- Per-skill mechanical content for chain T1-T3 + T4 capstones with proper damage_scaling_type routing
- Substrate weapon binding output reflected in character JSON
- Fight engine executes real combat (no synthetic stub) with proper physical vs magical vs hybrid damage routing
- Concentration architecture (doc 46) implemented (stat bounds + capability density + cohesion layering + set keying + class-agnostic drops)
- Phase 5 cohesion coalescence (cohesion-judge LLM + spirit-guide data-oracle + T4-attuned gear cohesion + acquisition curve)
- Defensive cohort empirical validation IMPROVES with real content (no longer 0/16 synthetic-stub limitation)
- Loadout app + HTML doc render the "character that was and is" with real skills + real weapons + real combat metrics

**Cycle 14 close becomes the SUBSTANTIVE delivery point** that Cycle 13 close was framed as. Cycle 15+ (per Q9 Pattern A) follows naturally: Phase 6 visual coalescence → Phase 7+8 → engine build COMPLETE → REINCARNATED-GAME UNLOCK.

---

## 10. Cross-references

### 10.1 Canonical docs

- `canonical/00-ground-state.md` — register doc 47 as new CURRENT entry
- `canonical/02-roadmap.md` — add doc 47 to companion docs; Cycle 14 scope expansion entry (Wave 0.5 added)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — composes; damage scaling routing per gear type
- `canonical/41-progression-framework-2026-05-27.md` — composes; per-level attribute scaling deferred per § 4 #1
- `canonical/46-concentration-architecture-2026-05-27.md` — composes; stat-range bounds Layer 1; cohesion layering Layer 6
- `canonical/story/skill-system-2026-05-24.md` — composes; SCALING-PATH dimension surfaced
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composes; Option α / β / C cell-type matching drives damage scaling routing
- `canonical/story/attribute-system-2026-05-24.md` — composes; per-attribute weapon profile

### 10.2 Operational + agent docs

- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — morning session closeout; this doc continues the same-day Pattern-B conversation
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-character-analysis.html` — cross-reference doc; needs update when Track D produces real per-skill content + substrate weapon binding
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — discipline candidate #38 queued

### 10.3 Decisions-log

Cycle 14 launch will produce decisions-log entries for damage-scaling-path discipline + Wave 0.5 Track D scope absorption. Not yet logged.

---

## 11. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — foundational architectural commitment for Cycle 14 Wave 0.5 + Phase 5 cohesion coalescence prerequisite
**Composition:** with doc 38 (delivery strategy), doc 39 (engine workflow), doc 40 (Cycle 13 architectural foundation), doc 41 (L50 hybrid framework), doc 46 (concentration architecture), skill-system canonical, weapon-substrate composition policy v1, attribute system canonical

**For:** the damage scaling architecture (three-path routing: physical / magical / hybrid) that surfaces what was implicit in skill-system composition pattern + substrate composition policy v1 Option α/β/C cell-type matching. Prerequisite for Cycle 14 Wave 0.5 Track D content gap closure. The wooden staff does NOT scale Ice Spike. Skills declare their damage_scaling_type; fight engine routes per type.

**Signed:** gandalf (story-and-design steward)
