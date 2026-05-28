# 47 — Damage Scaling Architecture (Physical / Magical / Hybrid)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27; § 4.5 T4 ELEMENT_CONVERSION lock amendment 2026-05-28) — foundational architectural commitment; surfaces what was implicit in `skill-system-2026-05-24.md` + `weapon-substrate-composition-policy-v1-2026-05-24.md` (Option α / β / C cell-type matching); becomes prerequisite for Cycle 13 content gap closure (Track D scope) + Cycle 14 Phase 5 cohesion coalescence; § 4.5 amendment locks T4 ELEMENT_CONVERSION specification (identity-1.0 + Phase 3d-anchored specialization + pure-unification PoE precedent) per rocket Phase 3e consultation request; see `canonical/00-ground-state.md`

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
>
> **Forward-link (2026-05-28 evening):** the `skill_damage_multiplier` term in the § 2.2 physical and magical damage equations is operated by `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` Pattern 1 (active skill damage scaling) — a per-node points-invested function `damage_multiplier_at_points = base_at_max × ((1 - decay) + decay × (points / NODE_MAX_active))`. Doc 51 specifies the inner-layer multiplier composition; this doc § 2.2 specifies the outer-layer damage routing. The two layers compose at the `skill_damage_multiplier` slot. Per-tier ratio 1:1.5:2.17:4.0 (Matt Phase 2 spec) is preserved at the `tier_coefficient` layer, OUTER to the investment-scaling layer. Pattern 2 (passive skill effect scaling) operates over passive-effect targets (stat bonuses, defenses, triggered-passive proc-rates) per doc 51 § 4. Patterns 3-6 (threshold unlocks / QoL modifiers / synergy bonuses / resource economy modifiers) are canonical-locked at doc 51 § 8 for Cycle 15+ implementation. Integrated W-α7+ Phase 3 (rocket Patterns 1+2 implementation + gamora BASE re-derivation + encounter HP rebalancing) lands the doc 51 design intent against this § 3 substrate.

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

### 4.5 T4 ELEMENT_CONVERSION mechanic specification — v1 canonical lock (2026-05-28)

> **STATUS:** v1 canonical lock — added 2026-05-28 in response to rocket Phase 3e consultation request `agentic_orchestration/gandalf/requests/2026-05-28-rocket-element-conversion-factor-design-lock-request.md`. Resolves `damage_resolver.py:618` TODO + names the specialization mechanism + locks PoE genre-precedent shape. Companion: rocket math note `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-7-phase-3e-element-conversion-factor-implementation-2026-05-28.md` § 4 (flat-cancellation impossibility proof) — load-bearing for this lock.

**Authority:** gandalf design-lock under rocket Phase 3e dispatch guard clause invocation + Discipline #47 design-time check (element conversion is balance-affecting; doc 50 § 4 5-target gate applies). Composes with `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4.4 (Target 4 specialization mechanism) + `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 7.2 (specialization peaks emerge from `base_at_max` distribution, NOT from investment scaling — symmetry extended here to T4 conversion factor).

#### 4.5.1 The lock — three answers

**Q1 — `element_conversion_factor` numeric value: 1.0 (identity).**

`element_conversion_factor` is canonically 1.0 for ELEMENT_CONVERSION T4 mechanic activation. Options B (fixed boost), C (element-pair lookup), and D (per-encounter elemental advantage) are REJECTED. The conversion is value-neutral at the numeric-factor layer; the mechanic's combat value emerges from element-affinity gear routing + Phase 3d-calibrated `base_at_max` under T4 context.

The TODO stub at `damage_resolver.py:618` is replaced with an explicit lookup from `attacker.t4_alteration_type` context; the lookup returns 1.0 when ELEMENT_CONVERSION is active. The implementation cleanup is real (T4 context wiring); the numeric value is identity by design.

**Q2 — Specialization mechanism: Phase 3d `base_at_max` distribution under T4 context (NOT the numeric factor).**

Doc 51 § 7.2 establishes that specialization peaks emerge from `base_at_max` distribution. This lock extends that architectural symmetry to T4 conversion: the bounded-viability-with-specialization Target 4 peaks (1.5-2× cohort median on 1-2 encounter types per kit) emerge from Phase 3d-calibrated `base_at_max(path, kit, tier, encounter_type)` UNDER T4 CONTEXT, not from `element_conversion_factor`.

The rocket math note § 4.2 flat-cancellation proof is load-bearing for this answer: within every mono-element path cohort in the Season 001 population (str_physical=earth, dex_physical=wind, int_magical=fire identity, wis_faith=water), a flat factor F cancels in the specialization ratio. The specialization signal MUST come from a non-flat source. The architecturally consistent non-flat source is `base_at_max` under T4 context — because (a) it already carries per-kit × per-encounter-type variation, (b) Phase 3d is the calibration owner of `base_at_max`, (c) running Phase 3d under T4 context is a re-run of an existing calibration pass, not a new design surface.

**Q3 — PoE genre precedent: pure unification (NO numeric fire bonus).**

PoE Avatar of Fire is canonically two mechanics: (a) the conversion node (50% non-fire → fire conversion; value-neutral at the conversion node), and (b) a separate "Avatar of Fire" Ascendancy-tier passive (+40% fire damage if you have it). The PoE Avatar of Fire "experience" the community discusses is the COMPOSITE of (a)+(b). The conversion mechanic ITSELF (a) is unification-only; the bonus (b) is the player's chain-investment compounding.

Reincarnated T4 ELEMENT_CONVERSION corresponds to PoE's (a) only. The Reincarnated (b) equivalent is the player's fire-affinity gear partition + fire-chain passives — surfaced by the conversion routing all damage through fire-affinity gear modifiers (per doc 47 § 2.2 magical path: `element_affinity_modifier` partition). The player's build is what compounds; T4 ELEMENT_CONVERSION makes the compounding accessible by unifying the damage type.

The Reincarnated conversion is 100% (all damage → fire), not PoE's 50%. The implication: the player CANNOT preserve a partial water/wind/earth split when ELEMENT_CONVERSION is active. The build choice is "commit fully to fire-affinity routing." This is the cleaner architectural commitment that matches Reincarnated's locked T4 capstone framing (D66 ONE T4 unlocked at a time → all-in commitment).

#### 4.5.2 Design rationale — why identity + Phase 3d anchoring (NOT a flat numeric boost)

**Genre architectural reading.** The mature ARPG pattern (D2, PoE, LE, GD per doc 50 § 2.3) is that element-conversion mechanics derive value from GEAR/AFFINITY ROUTING, not from a flat damage boost. D2 Conviction aura debuffs target resistance; PoE Avatar of Fire routes damage through fire-affinity stack; LE elemental conversion routes through elemental affinity nodes; GD Avatar of Mogdrogen routes through chaos-affinity gear. The numeric boost (when present) is from a SEPARATE compounding source (passive, debuff, ascendancy), not from the conversion node itself. A flat conversion boost (Option B) would conflate two mechanics that the genre keeps separate; it would degrade build-crafting legibility because players couldn't reason about "what does the conversion do" separately from "what does my gear do."

**Bounded-viability-with-specialization compliance.** Doc 50 § 4.4 Target 4 specifies peaks in the [1.5×, 2.0×] cohort-median band, NOT a flat +20-30% boost on all encounter types. A flat boost (Option B) at 1.2-1.3× shifts the kit's KPM curve uniformly upward without producing PEAKS — it produces "kit is slightly better than cohort on all encounter types," which fails the specialization clause and risks the no-strict-dominance clause if multiple T4-converted kits accumulate the same flat boost. The directive REQUIRES non-uniform per-encounter specialization. The non-uniform source is `base_at_max` under T4 context (per Q2).

**Player-experience anchor.** A player picking T4 ELEMENT_CONVERSION on a water-path WIS kit (e.g., `endgame_wis_03_ritual_mage`) is making a build choice with consequences: "I'm converting my element to fire to route my damage through fire-affinity gear; my water-affinity gear becomes dead-weight unless I respec." If the conversion ALSO gave a flat +20% boost, the player decision flattens — they'd take ELEMENT_CONVERSION for the boost regardless of gear strategy, and the strategic dimension of "should I commit to fire-affinity routing" disappears. The build-crafting community discourse load-bearing for ARPG long-tail retention (doc 50 § 4.3) requires the player choice to be STRATEGIC (gear/affinity reshape) not NUMERIC (flat multiplier). Identity-1.0 preserves the strategic dimension.

**Phase 3d RE-RUN architectural fit.** Phase 3d's purpose is BASE calibration per (path, kit, tier). Currently Phase 3d ran T4-naive (the gamora Part 2 wiring gap meant T4 alteration was never applied during the Phase 4 sim Phase 3d calibrated against). Re-running Phase 3d UNDER T4 context (with gamora Part 2 wiring fix landed) produces `base_at_max` values that embed the element-affinity-gear-shift effect. The specialization peaks fall out of this calibration NATURALLY — fire-affinity gear stacks fully when the kit's damage is fire-routed; the per-encounter-type interactions with mob composition produce the 1-2 peak distribution. This is not new design surface; it is the existing Phase 3d mechanism applied under the correct context.

**Scope-coherence with Cycle 14 v1 close trajectory.** Option D (per-encounter elemental advantage table on `EndgameMobStatProfile`) would introduce a new design vocabulary — per-element mob advantage — that doesn't currently exist in Reincarnated's locked design language. Adding it ad-hoc to unblock T4 mechanic resolution is a Discipline #45 vocabulary expansion that should be a Pattern-B Matt conversation, not a rocket-Phase-3e unblock. Option A + Phase 3d RE-RUN operates entirely within existing vocabulary. Per-element mob advantage may be a legitimate Cycle 15+ design surface; surfacing it for Phase 3e is premature.

#### 4.5.3 Composition with bounded-viability-with-specialization (doc 50 § 4)

| Doc 50 Target | This lock's compliance |
|---|---|
| Target 1 — Base DPS variance ≤1.5× across 4 paths | T4 ELEMENT_CONVERSION does not affect base DPS variance; identity-1.0 preserves W-α3 unified calibration semantics |
| Target 2 — Every kit non-zero KPM on every encounter type | Identity-1.0 + Phase 3d RE-RUN preserves the non-zero floor; gear-routing-through-fire-affinity provides DAMAGE (not zero) on all encounter types |
| Target 3 — No kit saturates KPM ceiling | Identity-1.0 cannot push kits above ceiling; Phase 3d RE-RUN calibrates against W-α2 ceiling |
| Target 4 — Specialization peaks (1.5-2× cohort median on 1-2 encounter types) | **Achieved via Phase 3d RE-RUN under T4 context**, NOT via numeric factor; per Q2 answer |
| Target 5 — No kit <30% cohort median on any encounter type | Identity-1.0 + Phase 3d RE-RUN preserves the floor; gear-routing produces meaningful output on all encounter types |

**The Doc 50 5-target compound pass criterion is the validation anchor for this lock.** Phase 4 RE-RUN under the new wiring (rocket Part 1 + gamora Part 2 + Phase 3d RE-RUN) MUST satisfy all 5 targets simultaneously across the 18 kits × 6 encounter types matrix for Cycle 14 v1 close-criterion to fire.

#### 4.5.4 Phase 4 RE-RUN dispatch routing (rocket Part 1 + gamora Part 2)

Per rocket math note § 5 two-part root cause decomposition:

**Part 1 (rocket seam — `damage_resolver.py:618`):** replace `element_conversion_factor = 1.0  # TODO` with explicit lookup from `attacker.t4_alteration_type` context returning 1.0 when ELEMENT_CONVERSION is active. Pseudocode (gandalf-specified):

```python
# Read element_conversion_factor from T4 alteration context on CombatantState.
# Per canonical doc 47 § 4.5 (gandalf 2026-05-28 design lock):
# ELEMENT_CONVERSION is value-neutral at the conversion-factor layer (identity 1.0).
# Combat value emerges from element-affinity gear routing + Phase 3d base_at_max under T4 context.
if getattr(attacker, "t4_alteration_type", None) == "ELEMENT_CONVERSION":
    element_conversion_factor = 1.0  # identity per canonical doc 47 § 4.5 Q1 lock
else:
    element_conversion_factor = 1.0  # default; no T4 conversion active
```

(The two branches produce the same value at v1 lock; the EXPLICIT lookup is required for Discipline #12 semantic-tracking and Discipline #39 scaffold-with-pending-decision retirement — the TODO comment is REMOVED.)

**Part 2 (gamora seam — `season_generation_pipeline.py` + `unified_calibration_loop.py`):** wire T4 alteration fields into `_build_real_player_class(kit, t4_variant)` so the T4 ELEMENT_CONVERSION alteration ACTUALLY APPLIES during gauntlet sim runs. Per rocket math note § 5 Part 2, this requires:
- `_build_real_player_class(kit, t4_variant=None)` accepts T4 variant context
- When `t4_variant != None` and variant has `gamora_combatant_fields`, pass `alteration_fields=kit.gamora_combatant_fields[t4_variant_id]` to combatant construction
- Phase 4 sweep runs once per profile × T4 variant (not skip T4 variants per the current `unified_calibration_loop.py:2408-2416` comment)

**Routing recommendation (gandalf → knight-rider):**

| Sequence | Reason |
|---|---|
| **Part 1 + Part 2 fire IN PARALLEL post this lock** | Independent code paths; rocket can replace `damage_resolver.py:618` TODO immediately while gamora wires `_build_real_player_class`. No dependency between them. |
| **Phase 3d RE-RUN fires SEQUENTIALLY after Part 1 + Part 2 close** | Phase 3d RE-RUN needs T4 wiring landed to calibrate `base_at_max` UNDER T4 context. Without Part 2 wiring, Phase 3d RE-RUN reproduces the original T4-naive calibration (zero progress). |
| **Phase 4 RE-RUN fires SEQUENTIALLY after Phase 3d RE-RUN** | Phase 4 validates against doc 50 5-target gate; needs Phase 3d's new BASE values to evaluate. |

**Phase 3d RE-RUN required: YES.** Per Q2 answer, the specialization mechanism IS Phase 3d `base_at_max` distribution under T4 context. The current Phase 3d output was calibrated T4-naive (per rocket math note § 5 Part 2 + `_build_real_player_class` not passing `alteration_fields`). Without Phase 3d RE-RUN under T4 context, the `base_at_max` values do not embed the element-affinity-gear-shift effect, and doc 50 Target 4 cannot fire.

**Estimated wall-clock post this lock (per rocket assessment + gandalf concurrence):**
- Part 1 (rocket): 1-2 hours (lookup function + unit tests + Discipline #12 declaration in commit)
- Part 2 (gamora): 2-4 hours (alteration-field wiring + unified_calibration_loop.py refactor + smoke test)
- Phase 3d RE-RUN (gamora): ~few hours (re-run existing calibration under T4 context)
- Phase 4 RE-RUN (gamora): ~0.5d (gauntlet sweep across 18 kits × 6 encounter types × profiles + 5-target validation)

Total: ~3-6 hours of compute + design review. Fits Cycle 14 v1 close trajectory per Path α master scoping budget.

#### 4.5.5 What this lock does NOT cover (deferred)

- **Per-encounter elemental advantage data structure (Option D):** legitimate Cycle 15+ design surface; surfacing as ad-hoc T4 unblock is premature per § 4.5.2 scope-coherence framing. If Phase 4 RE-RUN under Identity-1.0 + Phase 3d RE-RUN produces 5-target PASS, Option D is unnecessary. If Phase 4 RE-RUN produces partial-PASS with specialization-target shortfall in specific kit-cohorts, Option D becomes a Pattern-B Matt conversation candidate for Cycle 15+.
- **`dual_element_factor` (T4 DUAL_ELEMENT_ADDITION mechanic):** separate TODO at `damage_resolver.py` magical path (per rocket math note § 2). Out of Phase 3e scope per dispatch § 3. Future canonical lock will use the same Q1+Q2+Q3 framework — identity vs flat vs lookup vs per-encounter; specialization mechanism; genre precedent.
- **PoE Avatar of Fire `+40%` equivalent:** Reincarnated does NOT bundle the PoE Ascendancy +40% fire damage passive into T4 ELEMENT_CONVERSION. The compounding-source equivalent in Reincarnated is fire-affinity gear partition + fire-chain passives, assembled by the player. This is intentional per Q3 answer; not a future design surface.
- **Cross-element mixed cohorts:** the flat-cancellation proof (math note § 4.2) generalizes to cross-element kit mix — element-pair lookup would assign different factors per kit and break uniform cancellation. The Season 001 population is mono-element per path; future seasons MAY produce mixed cohorts. If that happens, the lock here STILL holds (identity-1.0 in mono-element case; element-pair lookup is a Cycle 15+ design surface if mixed cohorts produce target 4 shortfall).

#### 4.5.6 Discipline citations

- **Discipline #45 vocabulary audit:** "element_conversion_factor" is canonical-locked at this section; identity-1.0 value is canonical-locked; "ELEMENT_CONVERSION" mechanic name unchanged. No new prohibited-vocabulary introduced. No collision with prior canonical or engine source (rocket math note § 4.1 confirmed).
- **Discipline #47 design-time check:** ELEMENT_CONVERSION is balance-affecting; this lock specifies the 5-target compliance pathway (§ 4.5.3). Per-dispatch declaration: rocket Part 1 dispatch + gamora Part 2 dispatch + Phase 3d RE-RUN dispatch + Phase 4 RE-RUN dispatch all cite this section as the design-target acceptance bar.
- **Discipline #39 scaffold-with-pending-decision retirement:** the `damage_resolver.py:618` TODO is canonically retired by this lock. Future code referencing `element_conversion_factor` cites this section as the canonical source.
- **Discipline #1 math-before-code:** rocket math note `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-7-phase-3e-element-conversion-factor-implementation-2026-05-28.md` is the math anchor. Part 1 implementation references this lock + math note in commit message.
- **Discipline #12 semantic-shifting:** Part 1 implementation declares "replaces `# TODO` with explicit T4-context lookup; numeric value identity-1.0 per gandalf canonical lock; no semantic change to KPM outputs under v1 since prior TODO returned 1.0 — but SEMANTIC CONTEXT IS NEW (T4 alteration context is now read; future amendments may use this lookup site)."

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
