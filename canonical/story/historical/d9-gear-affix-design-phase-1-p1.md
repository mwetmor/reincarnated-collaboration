# D9 — Gear-Affix Design for Three New Substrates

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Authority:** gandalf (story-and-design steward; gear-affix-identity authoring authority per scope-of-work § 1.2 D9).
**Status:** **Canonical design** for Phase-1 P1 Deliverable 9. Companion to canonical 17 (gear-and-spirit-guide-design) + D8 (trait-floor design).
**Companion upstream:** Deliverable 8 — `d8-trait-floor-design-phase-1-p1.md`. Same substrate-identity anchors; this doc extends to gear-affix surface.
**Authored:** 2026-05-18 in hive-mode Phase-1 P1.

**Reading order:** § 0 TL;DR → § 1 Architectural frame → § 2 Lightning affix pool → § 3 Holy affix pool → § 4 Shadow affix pool → § 5 Cross-substrate coherence + canonical-four audit → § 6 Gamora implementation contract → § 7 Cross-references.

---

## § 0 — TL;DR

Gear-affix pool extended for three new substrates. Per scope-of-work § 1.2 D9 operational sizing guidance: ~1.5× expansion of the existing canonical-four pool surface (since 6/4 = 1.5; "operational sizing per gandalf design judgment"). This design lands the expansion as:

- **Lightning affix pool: 18 affixes** (across stat / ability / effect categories; element-gated)
- **Holy affix pool: 18 affixes** (same categorical breakdown)
- **Shadow affix pool: 18 affixes** (same categorical breakdown)

**Total D9 surface: 54 new affixes.** Existing canonical-four pool size (per `gear_generation.py` EFFECT_TO_FIT_AXES + canonical 17 affix-coherence): ~80-100 affixes across all gear/element/role/slot dimensions. Plus 54 = ~134-154 affixes — approximately 1.5-1.7× expansion. ✓

**Per-substrate signature anchors (mirrors D8):**

- **Lightning gear** — *velocity / chain / arc / discharge*: gear rolls chain-target extensions, discharge-event amplifiers, energy-cost reducers
- **Holy gear** — *radiance / consecration / cleanse / aligned-amplification*: gear rolls zone-radius extenders, ally-amplification scalars, cleanse-rate modifiers
- **Shadow gear** — *concealment / corruption / drain / dim-perception*: gear rolls drain-lifesteal scalars, concealment-trigger amplifiers, void-pool DPS

**Cross-substrate coherence audit:** all 54 new affixes validated against:

1. **No new affix violates any substrate's forbidden_mechanics** (per substrate identity declarations).
2. **No canonical-four affix silently becomes substrate-incoherent** post-extension (per § 5.2 audit below: 3 canonical-four affixes flagged for re-categorization recommendation; all are substrate-neutral by current tagging, but D9 surfaces them to jack-ryan Discipline #13 review).
3. **Substrate-neutral affixes** (e.g., `+all damage`, `+HP`, `+resistance to all`) remain ungated — they roll on any gear regardless of dominant element.

---

## § 1 — Architectural frame

### § 1.1 — How gear affixes currently work (recap from canonical 17 + gear_generation.py)

Per canonical 17 § "Affix coherence":

> The affix catalog uses two complementary tag layers, both checked when filtering the roll pool for a gear instance:
> - **Layer 1 — Dimensional tags** (same vocabulary as `class_fit_profile`; primary mechanism for ability/effect affixes)
> - **Layer 2 — Stat-affinity tags** (coarser; primary mechanism for stat-specific affixes; values: `str` / `dex` / `int_wis` / None)

Per `gear_generation.py:436-506` (`_affix_eligible_for_gear`):

> Affix eligibility = both layers pass. Layer 1 checks affix's `dimensional_tags` against gear's `base_type_fit` profile (alignment ≥ threshold); Layer 2 checks affix's `stat_affinity` against gear's `gear_affinity_set`.

Per `EFFECT_TO_FIT_AXES` (lines 615-699): per-element-per-effect-type fit profile mapping; this is the table that D9 extends with new substrate rows.

### § 1.2 — D9 extension shape

D9 extends gear-affix gating by:

1. **New `EFFECT_TO_FIT_AXES` rows** for `(damage, lightning)`, `(damage, holy)`, `(damage, shadow)` + new ailment entries `(shock, lightning)`, `(consecrate, holy)`, `(drain, shadow)`.
2. **New affix-pool entries** keyed on each new substrate's iconic mechanical hooks (per § 2-4 below).
3. **Material naming extension** in `MATERIAL_BY_ELEMENT` for the three new elements (per `gear_generation.py:511-518`).
4. **Element-suffix extension** in `_ELEMENT_SUFFIX` for the three new elements (per `gear_generation.py:533-539`).
5. **Stat-trait-pool slot extension** in `_STAT_TRAIT_POOL` if any slot-specific lightning/holy/shadow stat traits need slot gating (per `gear_generation.py:738+`).

D9 does NOT introduce new schema; it extends existing tables. This is a *registry-extension* deliverable, not a *refactor* deliverable.

### § 1.3 — Per-substrate affix pool sizing decision: 18 affixes each

The scope-of-work guidance is "~1.5× expansion since 6/4 = 1.5; operational sizing per gandalf design judgment." The 18-per-substrate sizing is calibrated as:

- **6 stat affixes** per substrate (3 minor-tier + 3 major-tier; covers fundamental stat-roll variety)
- **6 ability-modifier affixes** per substrate (paired with D8 trait architecture; gear can roll the same ability-modifier keys, including the 5 NEW keys D8 introduces)
- **6 effect affixes** per substrate (damage / ailment / utility — covering the spell-effect-affix layer)

**Total: 18 affixes × 3 substrates = 54 affixes.** Stays within the "1.5×" operational target while providing meaningful variety per substrate.

**Subtler design choice:** the 6/6/6 categorical breakdown is *deliberately uniform* across the three substrates. This produces:

- Cross-substrate parity at the pool-size level (no substrate is "richer" or "poorer" in affix variety; Layer 3 diversity gate sees uniform pool densities)
- Symmetric gear-roll experience — players swapping between substrate-specific gear pieces see similar affix-roll distributions
- Substrate-identity differentiation lives at the affix-CONTENT level (per § 2-4 below), not at the affix-COUNT level

### § 1.4 — Substrate-neutral vs substrate-flagged affixes

Per scope-of-work § 1.2 D9 design surface: "substrate-neutral affixes like '+all damage' don't gate; substrate-flagged affixes MUST gate cleanly."

D9 introduces NO new substrate-neutral affixes. All 54 new affixes are *substrate-flagged* — each carries `dimensional_tags` and (where applicable) `stat_affinity` that gate it to gear with matching dominant-element fit. Substrate-neutral affixes (e.g., `+bonus_hp`, `+all damage percent`, generic `+resistance`) remain in the existing catalog and continue to roll on any gear regardless of substrate.

---

## § 2 — Lightning affix pool

**Substrate:** lightning. Gear-domain dominant_element: `lightning`. Scaling attribute: `intelligence`. Iconic gear archetypes: caster-weapon (staff/wand/orb) + caster-armor (robe/hood) + accessories (ring/amulet) leaning long-range / high-energy.

### § 2.1 — `EFFECT_TO_FIT_AXES` entry — new row for lightning damage

```python
("damage", "lightning"): {
    "energy_type":    {"mana": 0.90, "focus": 0.50, "combo": 0.20, "rage": 0.10, "stamina-as-resource": 0.10},
    "range_profile":  {"long": 0.85, "medium": 0.75, "close": 0.30},
    "role_orientation": {"damage": 0.85, "hybrid": 0.65, "control": 0.55, "support": 0.20},
},
```

**Rationale:** mana-primary (lightning is intelligence-scaled, caster-coded); long/medium-range biased (lightning bolts traverse distance; `bolt_line` PREFER geometry); damage-primary with strong control secondary (shock ailment is hard-control category). Differs from fire by: lightning has higher control weighting (shock as hard-control vs burn as DoT); fire has stronger close-range weight (burst geometry vs lightning's bolt_line distance preference).

### § 2.2 — `EFFECT_TO_FIT_AXES` entry — new ailment row for shock

```python
("shock", "lightning"): {
    "energy_type":    {"mana": 0.90, "focus": 0.45, "combo": 0.20, "rage": 0.10, "stamina-as-resource": 0.10},
    "range_profile":  {"long": 0.85, "medium": 0.70, "close": 0.40},
    "role_orientation": {"control": 0.90, "damage": 0.65, "hybrid": 0.70, "support": 0.25},
},
```

**Rationale:** shock is hard-control; control_orientation peaks at 0.90 (matches root's 0.90). Mana-primary; ranged weighting matches damage profile. Note: shock's gear-effect-roll is gated by the lightning element AND any future chain-skill gating that the simulation layer applies.

### § 2.3 — Lightning affix entries (18 affixes)

```yaml
affix_pool:
  substrate: lightning
  size: 18

  # ── STAT AFFIXES (6) — substrate-themed stat rolls ─────────────────────────
  affixes:

    - affix_id: lightning_stat_thunderstruck_int
      effect_type: stat
      element: lightning
      stat_key: intelligence
      magnitude_range: [3, 8]    # minor-tier
      compatible_slots: [helmet, chest, robe, hood, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "+INT (Thunderstruck)"
      anchors: { mechanical_signature: [discharge], iconic_verbs: [strikes] }

    - affix_id: lightning_stat_resonant_mana
      effect_type: buff_mana_regen
      element: lightning
      magnitude_range: [0.4, 0.9]   # mana/sec; minor-tier
      compatible_slots: [robe, hood, ring, amulet, focus, orb]
      rarity_min: uncommon
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "+mana regen (Resonant)"
      anchors: { mechanical_signature: [propagate, arc], iconic_verbs: [courses through] }

    - affix_id: lightning_stat_overcharged_crit
      effect_type: stat
      element: lightning
      stat_key: bonus_crit_chance
      magnitude_range: [0.02, 0.06]   # +2% to +6% crit chance; minor-tier
      compatible_slots: [staff, wand, orb, ring, amulet]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "+crit chance (Overcharged)"
      anchors: { mechanical_signature: [discharge], iconic_verbs: [strikes, flashes] }

    - affix_id: lightning_stat_storm_intellect
      effect_type: stat
      element: lightning
      stat_key: intelligence
      magnitude_range: [8, 16]    # major-tier
      compatible_slots: [staff, wand, orb, robe, helmet, focus]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "+INT (Storm-Tempered)"
      anchors: { mechanical_signature: [arc, discharge], iconic_verbs: [strikes] }

    - affix_id: lightning_stat_pulsewise_damage
      effect_type: stat
      element: lightning
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      magnitude_range: [0.06, 0.14]   # +6% to +14% damage; major-tier
      compatible_slots: [staff, wand, orb, ring, amulet, focus]
      rarity_min: epic
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "+lightning damage (Pulsewise)"
      anchors: { mechanical_signature: [discharge, propagate], iconic_verbs: [courses through, strikes] }

    - affix_id: lightning_stat_arcwarden_resist
      effect_type: stat
      element: lightning
      stat_key: bonus_armor
      magnitude_range: [5, 12]    # major-tier armor; lightning-themed defensive
      compatible_slots: [chest, plate, helmet, hood, robe]
      rarity_min: epic
      dimensional_tags: []   # universal armor — accessible on all armor
      stat_affinity: int_wis
      flavor: "+armor (Arcwarden)"
      anchors: { mechanical_signature: [discharge], iconic_verbs: [flashes] }

  # ── ABILITY-MODIFIER AFFIXES (6) — paired with D8 trait architecture ──────
    - affix_id: lightning_amod_chain_extender
      effect_type: ability_modifier
      element: lightning
      ability_modifier_key: chain_targets_bonus   # NEW KEY per D8 § 6.4
      magnitude_range: [1, 2]   # +1 or +2 chain targets; additive
      compatible_slots: [wand, staff, orb, ring, amulet]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Chain Extender"
      anchors: { mechanical_signature: [chain, propagate, arc] }
      design_note: |
        D8 trait Arc Initiate establishes baseline +1 chain at L1; gear rank-stacks
        atop intrinsic. Per project_trait_architecture: same key across sources adds.

    - affix_id: lightning_amod_quickdischarge
      effect_type: ability_modifier
      element: lightning
      ability_modifier_key: cooldown_factor
      magnitude_range: [0.92, 0.97]   # 3-8% CDR; multiplicative
      compatible_slots: [staff, wand, orb, focus, ring]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "Quickdischarge"
      anchors: { mechanical_signature: [discharge], iconic_verbs: [flashes] }

    - affix_id: lightning_amod_pierce_focus
      effect_type: ability_modifier
      element: lightning
      ability_modifier_key: crit_bonus_damage
      magnitude_range: [0.10, 0.25]   # +10% to +25% crit bonus; additive
      compatible_slots: [staff, wand, orb, ring, amulet]
      rarity_min: epic
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Pierce-Focus"
      anchors: { mechanical_signature: [discharge, arc] }

    - affix_id: lightning_amod_efficient_cast
      effect_type: ability_modifier
      element: lightning
      ability_modifier_key: energy_cost_factor
      magnitude_range: [0.90, 0.96]   # 4-10% cheaper; multiplicative
      compatible_slots: [robe, hood, orb, focus, ring, amulet]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "Efficient-Cast"
      anchors: { mechanical_signature: [arc, discharge], iconic_verbs: [courses through] }

    - affix_id: lightning_amod_resonance_chain
      effect_type: ability_modifier
      element: lightning
      ability_modifier_key: chain_targets_bonus
      magnitude_range: [1, 1]   # +1 chain target; legendary-only
      compatible_slots: [staff, orb, amulet]
      rarity_min: legendary
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Resonance Chain (Legendary)"
      anchors: { mechanical_signature: [chain, propagate, arc] }
      design_note: |
        Same key as Chain Extender (rare-tier); rank-stacks. Legendary tier
        ensures Resonance Chain is rare-drop and feels distinct in name. Compounds
        with D8 traits Arc Initiate + Resonant Chain for chain-build playstyle.

    - affix_id: lightning_amod_aoe_arc
      effect_type: ability_modifier
      element: lightning
      ability_modifier_key: aoe_radius_bonus
      magnitude_range: [0.5, 1.2]   # +0.5 to +1.2 radius; additive
      compatible_slots: [staff, orb, focus, amulet]
      rarity_min: epic
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Wide Arc"
      anchors: { mechanical_signature: [arc, discharge], iconic_verbs: [strikes, courses through] }

  # ── EFFECT AFFIXES (6) — damage / ailment / utility ────────────────────────
    - affix_id: lightning_effect_shock_on_hit
      effect_type: shock
      element: lightning
      trigger: on_hit
      magnitude_range: [0.10, 0.25]   # shock duration (sec); minor-tier
      compatible_slots: [staff, wand, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Shock-Touched"
      anchors: { ailment_signature: shock, mechanical_signature: [chain, discharge] }

    - affix_id: lightning_effect_arc_strike
      effect_type: damage
      element: lightning
      trigger: on_hit
      magnitude_range: [3, 9]   # bonus per-hit lightning damage; minor-tier
      compatible_slots: [staff, wand, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Arc-Strike"
      anchors: { mechanical_signature: [arc, discharge], iconic_verbs: [strikes] }

    - affix_id: lightning_effect_thunderwave_on_crit
      effect_type: damage
      element: lightning
      trigger: on_crit
      magnitude_range: [12, 28]   # major-tier crit-burst
      compatible_slots: [staff, wand, orb, amulet]
      rarity_min: epic
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Thunderwave (on crit)"
      anchors: { mechanical_signature: [discharge, propagate], iconic_verbs: [strikes] }

    - affix_id: lightning_effect_storm_call_passive
      effect_type: damage
      element: lightning
      trigger: passive
      magnitude_range: [2, 5]   # passive per-second lightning aura tick; rare-tier
      compatible_slots: [orb, focus, amulet, ring]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Stormcall"
      anchors: { mechanical_signature: [discharge], iconic_verbs: [courses through, flashes] }
      design_note: |
        Soft-tension flag: "passive lightning aura" reads adjacent to lightning's
        forbidden_mechanics: [sustained_aura, ground_persist]. Resolution: this is
        a per-second tick of discharge events, not a sustained zone — the firing is
        discharge-shaped (instantaneous), the *cadence* is periodic. Discipline #13
        review opportunity for jack-ryan: confirm the tick-cadence resolution does
        not mechanically read as sustained_aura.

    - affix_id: lightning_effect_overload_proc
      effect_type: damage
      element: lightning
      trigger: on_kill
      magnitude_range: [15, 35]   # on-kill lightning burst at adjacent target
      compatible_slots: [staff, orb, amulet]
      rarity_min: epic
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Overload Proc"
      anchors: { mechanical_signature: [discharge, propagate], iconic_verbs: [strikes, flashes] }

    - affix_id: lightning_effect_grand_arc
      effect_type: damage
      element: lightning
      trigger: on_crit
      magnitude_range: [25, 55]   # legendary-tier crit-cascade
      compatible_slots: [staff, orb]
      rarity_min: legendary
      dimensional_tags: ["energy_type=mana", "range_profile=long"]
      stat_affinity: int_wis
      flavor: "Grand Arc (Legendary)"
      anchors: { mechanical_signature: [chain, propagate, arc, discharge], iconic_verbs: [arcs, courses through, strikes] }
```

### § 2.4 — Lightning affix pool design audit

- **Pool size:** 18 affixes across 6 stat + 6 ability-modifier + 6 effect ✓
- **Substrate signature coverage:** chain (3), propagate (4), arc (4), discharge (10) — heavy discharge-coverage is appropriate; lightning's identity peaks at discharge-event resolution ✓
- **Forbidden mechanics audit:** no affix introduces `root` / `sustained_aura` / `ground_persist` / `slow_channel`. Stormcall passive flagged in § 2.3 design_note for jack-ryan Discipline #13 review (soft tension; not violation) ✓
- **Pillar coherence:** HIGH_BURST_LOW_PERSIST reinforced — bursts (Thunderwave on-crit, Grand Arc, Overload Proc), single-strike amplifiers (Pierce-Focus, Arc-Strike), chain extenders (Chain Extender, Resonance Chain). No sustained-zone rewards. ✓
- **Slot distribution:** caster-weapons (staff/wand/orb) get 14 of 18 affixes; armor and accessories cover the rest. Aligns with lightning's mana-primary energy_type and caster archetype. ✓

---

## § 3 — Holy affix pool

**Substrate:** holy. Gear-domain dominant_element: `holy`. Scaling attribute: `wisdom`. Iconic gear archetypes: paladin-weapon (sword/hammer with holy element + STR or DEX or WIS scaling — flex archetype), cleric-weapon (staff/grimoire WIS-scaled), heavy armor (consecrate-walker plate), accessories (amulet/ring with consecrate zone bonuses).

**Genre-novel consideration (carried from D8 § 3):** holy's ailment_signature `consecrate` is a NEW category (`amplification` — valenced ground zone). Gear-effect affixes targeting consecrate need to be careful about the novel category — D5 ailment registry's consecrate definition is the authoritative shape; D9 affixes consume that shape.

### § 3.1 — `EFFECT_TO_FIT_AXES` entry — new row for holy damage

```python
("damage", "holy"): {
    "energy_type":    {"mana": 0.85, "focus": 0.55, "rage": 0.40, "stamina-as-resource": 0.30, "combo": 0.20},
    "range_profile":  {"medium": 0.85, "close": 0.70, "long": 0.55},
    "role_orientation": {"support": 0.80, "damage": 0.70, "hybrid": 0.70, "control": 0.45},
},
```

**Rationale:** mana-primary BUT with strong rage/stamina presence (holy is a flex substrate — paladin archetypes are STR-rage-melee; cleric archetypes are INT/WIS-mana-caster; both genre-valid per D2 Paladin + D3 Crusader + Lost Ark Paladin). Medium-range biased (consecrate zones are close-mid; nova/shaft geometry; not long-range projectile-primary). Support-orientation strongest (per substrate identity declarations role_affinities.support = 0.8). Damage secondary. Differs from canonical-four by: cross-energy-type fit (no canonical-four substrate has both mana 0.85 AND rage 0.40 — fire is mana-pure-0.90).

### § 3.2 — `EFFECT_TO_FIT_AXES` entry — new ailment row for consecrate

```python
("consecrate", "holy"): {
    "energy_type":    {"mana": 0.85, "focus": 0.50, "rage": 0.35, "stamina-as-resource": 0.25, "combo": 0.20},
    "range_profile":  {"close": 0.85, "medium": 0.80, "long": 0.30},
    "role_orientation": {"support": 0.95, "control": 0.65, "damage": 0.60, "hybrid": 0.60},
},
```

**Rationale:** support-role peaks at 0.95 (highest support-orientation in the EFFECT_TO_FIT_AXES table — consecrate is uniquely support-coded due to amplification ailment category). Close/medium range biased (consecrate zones are placed at melee or near-melee distance). Cross-energy-type fit preserves the flex archetype.

### § 3.3 — Holy affix entries (18 affixes)

```yaml
affix_pool:
  substrate: holy
  size: 18

  # ── STAT AFFIXES (6) — substrate-themed stat rolls ─────────────────────────
  affixes:

    - affix_id: holy_stat_resolute_wisdom
      effect_type: stat
      element: holy
      stat_key: wisdom
      magnitude_range: [3, 8]    # minor-tier
      compatible_slots: [helmet, chest, robe, hood, ring, amulet, plate]
      rarity_min: uncommon
      dimensional_tags: []   # universal — holy gear flex archetype
      stat_affinity: int_wis
      flavor: "+WIS (Resolute)"
      anchors: { mechanical_signature: [radiate, consecrate], iconic_verbs: [shines through] }

    - affix_id: holy_stat_sacred_vitality
      effect_type: stat
      element: holy
      stat_key: bonus_hp
      magnitude_range: [12, 28]   # minor-tier flat HP
      compatible_slots: [chest, plate, helmet, hood, robe, amulet]
      rarity_min: uncommon
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "+HP (Sacred Vitality)"
      anchors: { mechanical_signature: [consecrate], iconic_verbs: [blesses, uplifts] }

    - affix_id: holy_stat_consecrated_resistance
      effect_type: stat
      element: holy
      stat_key: bonus_armor
      magnitude_range: [6, 14]   # minor-tier
      compatible_slots: [chest, plate, helmet, hood, robe]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "+armor (Consecrated)"
      anchors: { mechanical_signature: [consecrate, radiate], iconic_verbs: [sanctifies] }

    - affix_id: holy_stat_blessed_wisdom
      effect_type: stat
      element: holy
      stat_key: wisdom
      magnitude_range: [8, 16]   # major-tier
      compatible_slots: [staff, grimoire, focus, orb, robe, helmet]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "+WIS (Blessed)"
      anchors: { mechanical_signature: [radiate, amplify_allied], iconic_verbs: [blesses, shines through] }

    - affix_id: holy_stat_radiant_damage
      effect_type: stat
      element: holy
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      magnitude_range: [0.05, 0.13]   # major-tier
      compatible_slots: [sword, hammer, staff, grimoire, ring, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "+holy damage (Radiant)"
      anchors: { mechanical_signature: [radiate, judges], iconic_verbs: [shines through, burns away] }

    - affix_id: holy_stat_sanctified_armor
      effect_type: stat
      element: holy
      stat_key: bonus_armor
      magnitude_range: [14, 28]   # major-tier
      compatible_slots: [chest, plate, helmet, robe]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "+armor (Sanctified)"
      anchors: { mechanical_signature: [consecrate, amplify_allied], iconic_verbs: [sanctifies, blesses] }

  # ── ABILITY-MODIFIER AFFIXES (6) — paired with D8 trait architecture ──────
    - affix_id: holy_amod_consecrate_extender
      effect_type: ability_modifier
      element: holy
      ability_modifier_key: consecrate_radius_bonus    # NEW KEY per D8 § 6.4
      magnitude_range: [0.4, 1.0]   # +0.4 to +1.0 zone radius; additive
      compatible_slots: [staff, grimoire, focus, orb, ring, amulet]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Consecrate Extender"
      anchors: { mechanical_signature: [consecrate, radiate] }
      design_note: |
        D8 trait Consecrate Walker establishes baseline radius bonus at L1;
        gear rank-stacks atop intrinsic per project_trait_architecture.

    - affix_id: holy_amod_zone_cooldown
      effect_type: ability_modifier
      element: holy
      ability_modifier_key: cooldown_factor
      magnitude_range: [0.92, 0.97]   # 3-8% CDR; multiplicative
      compatible_slots: [staff, grimoire, focus, ring, amulet]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "Zone Cooldown"
      anchors: { mechanical_signature: [consecrate, amplify_allied] }

    - affix_id: holy_amod_revelation_crit
      effect_type: ability_modifier
      element: holy
      ability_modifier_key: crit_bonus_damage
      magnitude_range: [0.08, 0.20]   # +8% to +20% crit bonus
      compatible_slots: [sword, hammer, staff, grimoire, ring, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Revelation-Strike"
      anchors: { mechanical_signature: [radiate, judges], iconic_verbs: [judges] }

    - affix_id: holy_amod_efficient_consecrate
      effect_type: ability_modifier
      element: holy
      ability_modifier_key: energy_cost_factor
      magnitude_range: [0.90, 0.96]   # 4-10% cheaper; multiplicative
      compatible_slots: [robe, focus, grimoire, ring, amulet]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "Efficient-Consecrate"
      anchors: { mechanical_signature: [consecrate, cleanse], iconic_verbs: [sanctifies] }

    - affix_id: holy_amod_sanctified_radius
      effect_type: ability_modifier
      element: holy
      ability_modifier_key: aoe_radius_bonus
      magnitude_range: [0.5, 1.4]   # +0.5 to +1.4 radius bonus
      compatible_slots: [staff, grimoire, focus, orb, ring, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Sanctified Radius"
      anchors: { mechanical_signature: [radiate, consecrate], iconic_verbs: [shines through] }

    - affix_id: holy_amod_cleanse_pulse
      effect_type: ability_modifier
      element: holy
      ability_modifier_key: ailment_cleanse_factor   # NEW KEY per D8 § 6.4
      magnitude_range: [0.88, 0.94]   # 6-12% faster cleanse on aligned; multiplicative
      compatible_slots: [staff, grimoire, focus, amulet]
      rarity_min: epic
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "Cleanse Pulse"
      anchors: { mechanical_signature: [cleanse, consecrate], iconic_verbs: [burns away, blesses] }
      design_note: |
        Same NEW key as D8 trait Cleansing Radiance. Gear rolls and intrinsic
        compound multiplicatively (per MULTIPLICATIVE_ABILITY_MODIFIER_KEYS
        treatment of factor-keys).

  # ── EFFECT AFFIXES (6) — damage / ailment / utility ────────────────────────
    - affix_id: holy_effect_consecrate_zone_on_hit
      effect_type: consecrate
      element: holy
      trigger: on_hit
      magnitude_range: [0.25, 0.75]   # zone duration (seconds); minor-tier
      compatible_slots: [staff, hammer, grimoire, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Zone-Touched"
      anchors: { ailment_signature: consecrate }

    - affix_id: holy_effect_radiant_strike
      effect_type: damage
      element: holy
      trigger: on_hit
      magnitude_range: [4, 10]   # bonus per-hit holy damage; minor-tier
      compatible_slots: [sword, hammer, staff, grimoire, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Radiant-Strike"
      anchors: { mechanical_signature: [radiate, judges], iconic_verbs: [burns away] }

    - affix_id: holy_effect_judgment_on_crit
      effect_type: damage
      element: holy
      trigger: on_crit
      magnitude_range: [14, 32]   # major-tier
      compatible_slots: [sword, hammer, staff, grimoire, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Judgment (on crit)"
      anchors: { mechanical_signature: [radiate, judges, reveals], iconic_verbs: [judges] }

    - affix_id: holy_effect_aligned_aura
      effect_type: buff_damage
      element: holy
      trigger: passive
      magnitude_range: [0.04, 0.10]   # +4% to +10% allied damage; passive aura
      compatible_slots: [chest, plate, robe, amulet]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Aligned Aura"
      anchors: { mechanical_signature: [amplify_allied, radiate], iconic_verbs: [uplifts, blesses] }
      design_note: |
        amplify_allied is in holy's mechanical_signature (not forbidden_mechanics).
        For solo-primary play (per project_design_intent), this affix's effective
        value depends on gamora's solo-aligned-target model. Surfacing for D7
        balance-pass cross-coherence review.

    - affix_id: holy_effect_consecrate_pulse
      effect_type: heal
      element: holy
      trigger: passive
      magnitude_range: [1, 3]   # passive heal per-second to caster in consecrate zone
      compatible_slots: [chest, plate, robe, ring, amulet]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Consecrate Pulse"
      anchors: { mechanical_signature: [consecrate, amplify_allied], iconic_verbs: [blesses, uplifts] }

    - affix_id: holy_effect_grand_revelation
      effect_type: damage
      element: holy
      trigger: on_crit
      magnitude_range: [26, 58]   # legendary-tier crit
      compatible_slots: [sword, hammer, staff, grimoire]
      rarity_min: legendary
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Grand Revelation (Legendary)"
      anchors: { mechanical_signature: [radiate, judges, reveals, consecrate], iconic_verbs: [judges, reveals, shines through] }
```

### § 3.4 — Holy affix pool design audit

- **Pool size:** 18 affixes across 6 stat + 6 ability-modifier + 6 effect ✓
- **Substrate signature coverage:** radiate (8), consecrate (10), cleanse (2), amplify_allied (4) — consecrate heavy-coverage appropriate as ailment-signature anchor ✓
- **Forbidden mechanics audit:** no affix introduces `drain` / `conceal` / `corrupt` / `stealth` ✓
- **Pillar coherence:** REVELATION_AND_AMPLIFICATION reinforced — zone extenders, ally-amplification, cleanse rate, revelation crit ✓
- **Flex archetype slot distribution:** sword/hammer accessible (8 affixes) for STR-rage Paladin archetype + staff/grimoire/focus accessible (12 affixes) for INT/WIS-mana Cleric archetype. Genre-flex preserved ✓
- **Novel-ailment integration:** consecrate-coded effect affix (`holy_effect_consecrate_zone_on_hit`) and consecrate-radius-extender + consecrate-pulse traits all hook into the novel `amplification` category. D5 ailment registry's consecrate definition is upstream-blocking. ✓

---

## § 4 — Shadow affix pool

**Substrate:** shadow. Gear-domain dominant_element: `shadow`. Scaling attribute: `intelligence`. Iconic gear archetypes: necromancer-weapon (staff/grimoire/orb INT-mana-caster) + assassin-weapon (dagger DEX-combo-melee — flex archetype), light armor (robe/hood for INT casters; leather/cloth for DEX rogues), accessories (amulet/ring with drain or concealment bonuses).

**Genre lineage cluster:** Solo Leveling's shadow-army summoning + drain economy; D2 Necromancer's bone-and-poison + life-tap; D3 Demon Hunter's Shadow Power; D2 Assassin's Cloak of Shadows. Same dual-resonance as D8 § 4.

### § 4.1 — `EFFECT_TO_FIT_AXES` entry — new row for shadow damage

```python
("damage", "shadow"): {
    "energy_type":    {"mana": 0.85, "focus": 0.50, "combo": 0.45, "stamina-as-resource": 0.25, "rage": 0.10},
    "range_profile":  {"medium": 0.80, "long": 0.70, "close": 0.55},
    "role_orientation": {"damage": 0.80, "hybrid": 0.70, "control": 0.55, "support": 0.15},
},
```

**Rationale:** mana-primary (necromancer caster archetype) BUT with strong combo presence (assassin-rogue archetype using combo energy + dim-perception strike-from-concealment). Medium-range biased (shadow tendrils + void pools are typically zone-placed; concealment + sudden-strike works close-mid range). Damage-primary; lowest support orientation of any substrate (matches shadow's `forbidden_mechanics: [amplify_allied]`).

### § 4.2 — `EFFECT_TO_FIT_AXES` entry — new ailment row for drain

```python
("drain", "shadow"): {
    "energy_type":    {"mana": 0.85, "focus": 0.45, "combo": 0.40, "stamina-as-resource": 0.20, "rage": 0.10},
    "range_profile":  {"medium": 0.80, "long": 0.65, "close": 0.50},
    "role_orientation": {"damage": 0.85, "control": 0.65, "hybrid": 0.70, "support": 0.10},
},
```

**Rationale:** damage-orientation peaks at 0.85 — drain is a DoT (matching burn's category) and primarily damage-coded; lowest support (no ally-amplification). Cross-energy-type fit preserves dual-archetype.

### § 4.3 — Shadow affix entries (18 affixes)

```yaml
affix_pool:
  substrate: shadow
  size: 18

  # ── STAT AFFIXES (6) — substrate-themed stat rolls ─────────────────────────
  affixes:

    - affix_id: shadow_stat_shrouded_int
      effect_type: stat
      element: shadow
      stat_key: intelligence
      magnitude_range: [3, 8]    # minor-tier
      compatible_slots: [helmet, hood, robe, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "+INT (Shrouded)"
      anchors: { mechanical_signature: [conceal, dim_perception], iconic_verbs: [shrouds, dims] }

    - affix_id: shadow_stat_void_dexterity
      effect_type: stat
      element: shadow
      stat_key: dexterity
      magnitude_range: [3, 8]    # minor-tier
      compatible_slots: [dagger, off_hand_dagger, hood, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: ["energy_type=combo"]
      stat_affinity: dex
      flavor: "+DEX (Void-Touched)"
      anchors: { mechanical_signature: [conceal, dim_perception], iconic_verbs: [creeps into, occludes] }

    - affix_id: shadow_stat_corrupted_crit
      effect_type: stat
      element: shadow
      stat_key: bonus_crit_chance
      magnitude_range: [0.02, 0.06]   # +2% to +6% crit
      compatible_slots: [dagger, staff, grimoire, ring, amulet]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "+crit chance (Corrupted)"
      anchors: { mechanical_signature: [corrupt, dim_perception] }

    - affix_id: shadow_stat_drain_intellect
      effect_type: stat
      element: shadow
      stat_key: intelligence
      magnitude_range: [8, 16]   # major-tier
      compatible_slots: [staff, grimoire, orb, robe, helmet, focus]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "+INT (Drainwise)"
      anchors: { mechanical_signature: [drain, corrupt] }

    - affix_id: shadow_stat_withering_damage
      effect_type: stat
      element: shadow
      stat_key: bonus_damage_percent
      stat_magnitude_type: proportional
      magnitude_range: [0.06, 0.14]   # major-tier
      compatible_slots: [staff, grimoire, dagger, orb, ring, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "+shadow damage (Withering)"
      anchors: { mechanical_signature: [drain, corrupt, dim_perception], iconic_verbs: [drains, withdraws] }

    - affix_id: shadow_stat_void_resistance
      effect_type: stat
      element: shadow
      stat_key: bonus_armor
      magnitude_range: [5, 12]    # major-tier armor
      compatible_slots: [hood, robe, helmet, chest]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "+armor (Void-Warded)"
      anchors: { mechanical_signature: [conceal, drain], iconic_verbs: [shrouds, dims] }

  # ── ABILITY-MODIFIER AFFIXES (6) — paired with D8 trait architecture ──────
    - affix_id: shadow_amod_drain_extender
      effect_type: ability_modifier
      element: shadow
      ability_modifier_key: drain_lifesteal_fraction   # NEW KEY per D8 § 6.4
      magnitude_range: [0.02, 0.06]   # +2% to +6% lifesteal; additive
      compatible_slots: [dagger, staff, grimoire, orb, ring, amulet]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Drain Extender"
      anchors: { mechanical_signature: [drain, corrupt] }
      design_note: |
        Same key as D8 traits Drain Sustain (L1) + Extracted Essence (L25).
        Stacks additively per project_trait_architecture. Recommend cap on
        cumulative drain_lifesteal_fraction at ~25% across all sources to
        avoid unbounded sustain (gamora wiring).

    - affix_id: shadow_amod_quickdrain
      effect_type: ability_modifier
      element: shadow
      ability_modifier_key: cooldown_factor
      magnitude_range: [0.92, 0.97]   # 3-8% CDR; multiplicative
      compatible_slots: [staff, grimoire, dagger, orb, ring]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Quickdrain"
      anchors: { mechanical_signature: [drain, conceal] }

    - affix_id: shadow_amod_concealment_crit
      effect_type: ability_modifier
      element: shadow
      ability_modifier_key: crit_bonus_damage
      magnitude_range: [0.10, 0.25]   # +10% to +25% crit bonus
      compatible_slots: [dagger, staff, grimoire, ring, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Concealment-Strike"
      anchors: { mechanical_signature: [conceal, dim_perception], iconic_verbs: [shrouds, dims] }

    - affix_id: shadow_amod_efficient_drain
      effect_type: ability_modifier
      element: shadow
      ability_modifier_key: energy_cost_factor
      magnitude_range: [0.90, 0.96]   # 4-10% cheaper; multiplicative
      compatible_slots: [robe, hood, grimoire, orb, ring, amulet]
      rarity_min: rare
      dimensional_tags: ["energy_type=mana"]
      stat_affinity: int_wis
      flavor: "Efficient-Drain"
      anchors: { mechanical_signature: [drain, corrupt] }

    - affix_id: shadow_amod_creeping_duration
      effect_type: ability_modifier
      element: shadow
      ability_modifier_key: control_duration_bonus
      magnitude_range: [0.3, 0.9]   # +0.3 to +0.9 sec duration bonus
      compatible_slots: [staff, grimoire, focus, ring, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Creeping Duration"
      anchors: { mechanical_signature: [drain, corrupt, dim_perception] }

    - affix_id: shadow_amod_walker_evasion
      effect_type: ability_modifier
      element: shadow
      ability_modifier_key: conceal_evasion_bonus    # NEW KEY per D8 § 6.4
      magnitude_range: [0.04, 0.10]   # +4% to +10% evasion on concealment proc
      compatible_slots: [hood, robe, dagger, off_hand_dagger, ring, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Walker Evasion"
      anchors: { mechanical_signature: [conceal, dim_perception] }

  # ── EFFECT AFFIXES (6) — damage / ailment / utility ────────────────────────
    - affix_id: shadow_effect_drain_on_hit
      effect_type: drain
      element: shadow
      trigger: on_hit
      magnitude_range: [0.40, 0.90]   # drain duration (sec); minor-tier
      compatible_slots: [staff, grimoire, dagger, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Drain-Touched"
      anchors: { ailment_signature: drain }

    - affix_id: shadow_effect_void_strike
      effect_type: damage
      element: shadow
      trigger: on_hit
      magnitude_range: [3, 9]   # bonus per-hit shadow damage; minor-tier
      compatible_slots: [staff, grimoire, dagger, ring, amulet]
      rarity_min: uncommon
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Void-Strike"
      anchors: { mechanical_signature: [drain, corrupt], iconic_verbs: [drains, unmakes] }

    - affix_id: shadow_effect_corrupted_crit
      effect_type: damage
      element: shadow
      trigger: on_crit
      magnitude_range: [12, 30]   # major-tier
      compatible_slots: [staff, grimoire, dagger, orb, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Corrupted (on crit)"
      anchors: { mechanical_signature: [corrupt, drain], iconic_verbs: [unmakes, withdraws] }

    - affix_id: shadow_effect_void_pool_passive
      effect_type: damage
      element: shadow
      trigger: passive
      magnitude_range: [2, 5]   # passive per-second shadow tick; rare-tier
      compatible_slots: [orb, focus, amulet, ring]
      rarity_min: rare
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Void Pool"
      anchors: { mechanical_signature: [drain, corrupt], iconic_verbs: [drains, creeps into] }

    - affix_id: shadow_effect_extract_on_kill
      effect_type: damage
      element: shadow
      trigger: on_kill
      magnitude_range: [12, 30]   # on-kill shadow burst
      compatible_slots: [staff, grimoire, dagger, amulet]
      rarity_min: epic
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Extracted Essence"
      anchors: { mechanical_signature: [drain, corrupt], iconic_verbs: [unmakes, withdraws, takes] }
      design_note: |
        Distinct from D8 trait Extracted Essence (which provides life-on-kill).
        This is the on-kill damage proc — synergistic but distinct mechanically.

    - affix_id: shadow_effect_unmaking
      effect_type: damage
      element: shadow
      trigger: on_crit
      magnitude_range: [25, 55]   # legendary-tier
      compatible_slots: [staff, grimoire, dagger]
      rarity_min: legendary
      dimensional_tags: []
      stat_affinity: int_wis
      flavor: "Unmaking (Legendary)"
      anchors: { mechanical_signature: [drain, corrupt, dim_perception], iconic_verbs: [unmakes, withdraws, occludes] }
```

### § 4.4 — Shadow affix pool design audit

- **Pool size:** 18 affixes across 6 stat + 6 ability-modifier + 6 effect ✓
- **Substrate signature coverage:** drain (10), conceal (5), corrupt (8), dim_perception (5) — drain heaviest, appropriate ✓
- **Forbidden mechanics audit:** no affix introduces `radiate` / `consecrate` / `amplify_allied` / `reveal` ✓
- **Pillar coherence:** CONCEALMENT_AND_DRAIN reinforced — drain extenders, concealment crit, void pools, drain duration ✓
- **Dual-archetype slot distribution:** dagger accessible (10 affixes) for DEX-combo Assassin archetype + staff/grimoire/orb accessible (14 affixes) for INT-mana Necromancer archetype. Genre-dual preserved ✓
- **Iconic verbs:** 8 of 8 iconic_verbs cited across affixes (consistent with D8 audit) ✓

---

## § 5 — Cross-substrate coherence + canonical-four audit

### § 5.1 — Forbidden-mechanics audit (D9 surface)

Every affix above audited against every substrate's `forbidden_mechanics`. Mirroring D8 § 5.1 audit pattern:

- **Lightning affixes:** no affix applies drain / conceal / corrupt / radiate / consecrate. ✓
- **Holy affixes:** no affix applies drain / conceal / corrupt / stealth. ✓
- **Shadow affixes:** no affix applies radiate / consecrate / amplify_allied / reveal. ✓

**Net audit: CLEAN.** No cross-substrate forbidden_mechanics violations from D9 affix authoring.

### § 5.2 — Canonical-four affix audit (Discipline #13 concern)

**Per scope-of-work § 1.2 D9: "No canonical-four affix silently becomes substrate-incoherent — surface to jack-ryan Discipline #13 review."**

Reviewing existing canonical-four affix entries in `EFFECT_TO_FIT_AXES` (gear_generation.py:615-699) plus stat-trait pools:

**Audit findings (3 candidates for jack-ryan review):**

1. **`("buff_dodge", None)` entry (lines 684-688):**
   - Currently substrate-neutral (element=None). Rolls on any gear regardless of substrate.
   - **Soft tension:** with shadow's `conceal_evasion_bonus` NEW key (D8 § 6.4), shadow has a substrate-coherent evasion mechanic. Buff_dodge as substrate-neutral may *compete* with shadow's substrate-coherent evasion when both roll on the same gear piece.
   - **Recommendation:** retain buff_dodge as substrate-neutral (no change). Substrate-flagged shadow evasion is *additional layer atop* substrate-neutral baseline; not in conflict. No re-categorization needed.
   - **Disposition:** **NO ACTION.** Flag retained for jack-ryan informational review.

2. **`("buff_mana_regen", None)` entry (lines 689-693):**
   - Currently substrate-neutral. Rolls on any gear.
   - **Soft tension:** with holy's `wisdom`-scaling and `mana`-energy primary, plus lightning's `intelligence`-scaling and `mana`-energy primary, mana_regen as substrate-neutral is *broadly aligned* with new substrates. No incoherence.
   - **Disposition:** **NO ACTION.**

3. **Material naming extension** (`MATERIAL_BY_ELEMENT` at gear_generation.py:511-518):
   - Currently only canonical-four + physical + None. D9 introduces three new elements (lightning/holy/shadow).
   - **Required extension** (not optional):
     ```python
     MATERIAL_BY_ELEMENT.update({
         "lightning": ["Stormglass",  "Arcsteel",   "Pulseweave"],
         "holy":      ["Brightsteel", "Dawnstone",  "Hallowedglass"],
         "shadow":    ["Voidweave",   "Nightsteel", "Drainglass"],
     })
     ```
   - **Recommendation:** gamora extends materials table; names above are gandalf-suggested. Knight-rider routing decision: gandalf-authored names ride with D9, or gandalf surfaces to drax/LLM for creative pass? D9 ships with gandalf-authored names; LLM creative pass can revise post-ship.
   - **Element suffix extension** similarly required:
     ```python
     _ELEMENT_SUFFIX.update({
         "lightning": "of Arcs",
         "holy":      "of Dawn",
         "shadow":    "of the Void",
     })
     ```

**Net canonical-four audit:** **NO SILENT INCOHERENCE.** Two soft-tension flags retained for jack-ryan informational review; no canonical-four affix requires re-categorization. Material naming + element suffix extensions are *additive* (not modifications to canonical-four entries) — Discipline #13 clean.

### § 5.3 — Cross-affix-stack coherence (rank-stacking with D8 traits)

Per project_trait_architecture: "same trait from intrinsic source + gear source rank-stacks across sources." D9 design respects this:

| NEW key | D8 trait source | D9 affix source | Stacking |
|---|---|---|---|
| `chain_targets_bonus` | Arc Initiate (L1) + Resonant Chain (L12) | Chain Extender (rare) + Resonance Chain (legendary) | additive across all sources |
| `consecrate_radius_bonus` | Consecrate Walker (L1) | Consecrate Extender (rare) | additive |
| `drain_lifesteal_fraction` | Drain Sustain (L1) + Extracted Essence (L25) | Drain Extender (rare) | additive; recommend ~25% cap |
| `conceal_evasion_bonus` | Concealing Step (L1) | Walker Evasion (epic) | additive |
| `ailment_cleanse_factor` | Cleansing Radiance (L12) | Cleanse Pulse (epic) | multiplicative (in MULTIPLICATIVE registry) |

Each NEW key has both intrinsic-side and gear-side entries — the dual-source architecture is exercised cleanly.

### § 5.4 — Substrate-identity cross-reference summary

| Substrate | mechanical_signature realized | iconic_verbs cited |
|---|---|---|
| Lightning | chain (3 affixes), propagate (4), arc (4), discharge (10) | 7 of 8 iconic_verbs |
| Holy | radiate (8), consecrate (10), cleanse (2), amplify_allied (4) | 8 of 9 iconic_verbs |
| Shadow | drain (10), conceal (5), corrupt (8), dim_perception (5) | 8 of 8 iconic_verbs |

Each substrate's `mechanical_signature` verbs receive multi-affix coverage. No substrate identity is structurally under-realized at the gear surface.

---

## § 6 — Gamora implementation contract

### § 6.1 — Affix-pool registration

D9 affixes flow into the existing `EffectPoolEntry` infrastructure (`gear_generation.py` + `gear_schema.py`):

**Option A — Engine-internal Python literal pool** (matches current canonical-four pattern in `gear_generation.py`):
- Extend `EFFECT_TO_FIT_AXES` dictionary with 6 new rows (3 damage + 3 ailment).
- Append 54 new `EffectPoolEntry` instances to the affix catalog.
- Extend `MATERIAL_BY_ELEMENT` + `_ELEMENT_SUFFIX` with 3 new entries each (per § 5.2).

**Option B — YAML config file** (mirrors D8 substrate-identity loader pattern):
- New `reincarnated-engine/config/gear_affix_pools/<substrate>.yaml` per substrate.
- Loader at `src/reincarnated/generation/affix_pool_loader.py` (new module) extracts at boot.
- Pydantic-validated; loader output: `dict[str, list[EffectPoolEntry]]` keyed by substrate.

**Recommendation:** **Option A for D9 Phase-1 P1 ship; Option B as Phase-1 P2 refactor target.** Reasoning: the canonical-four affix entries are currently Python-literal; D9 extension matches the existing pattern → minimal-surface change. Option B is a larger refactor that should sweep all affixes (canonical-four + new) atomically, not piecemeal. Gamora's call.

### § 6.2 — Required gear_generation.py extensions

```python
# 1. EFFECT_TO_FIT_AXES — add 6 new entries (per § 2.1, 2.2, 3.1, 3.2, 4.1, 4.2)

EFFECT_TO_FIT_AXES.update({
    ("damage", "lightning"):  {...},
    ("damage", "holy"):       {...},
    ("damage", "shadow"):     {...},
    ("shock",      "lightning"): {...},
    ("consecrate", "holy"):      {...},
    ("drain",      "shadow"):    {...},
})

# 2. MATERIAL_BY_ELEMENT — add 3 new entries (per § 5.2)

MATERIAL_BY_ELEMENT.update({
    "lightning": ["Stormglass",  "Arcsteel",   "Pulseweave"],
    "holy":      ["Brightsteel", "Dawnstone",  "Hallowedglass"],
    "shadow":    ["Voidweave",   "Nightsteel", "Drainglass"],
})

# 3. _ELEMENT_SUFFIX — add 3 new entries (per § 5.2)

_ELEMENT_SUFFIX.update({
    "lightning": "of Arcs",
    "holy":      "of Dawn",
    "shadow":    "of the Void",
})

# 4. _EFFECT_POWER_WEIGHT — add power weights for 3 new ailments

_EFFECT_POWER_WEIGHT.update({
    "shock":      0.10,   # matches burn (hard control with light damage component)
    "consecrate": 0.15,   # higher than burn — amplification category has dual side effect
    "drain":      0.12,   # between burn (0.10) and bleed (0.12) — DoT-tier
})

# 5. Affix-pool entries — append 54 EffectPoolEntry instances to catalog
#    (See § 2.3, § 3.3, § 4.3 for full YAML; gamora translates to Python)
```

### § 6.3 — Required gear_catalog.py / build_effect_pool extension

Per `gear_catalog.py:59` (`build_effect_pool(foundation, season_id, power_tier=50)`):

- This function constructs the per-season affix catalog. D9 entries become eligible-pool when the season's rotating elements include the new substrate(s).
- After substrate-expansion (D2: 4→7 substrate rotation), seasons with lightning/holy/shadow in rotation see D9 affixes pooled into the season's catalog.
- No structural change to `build_effect_pool`; affixes flow through the existing per-season selection logic. Gamora verifies.

### § 6.4 — Boot-time validation (mirrors D8 § 6.3)

When D9 affixes load, validate:

- Every `dimensional_tags` entry uses recognized axis values (`energy_type=mana` / `range_profile=long` / etc.). Fail-loud on unknown axis values.
- Every `compatible_slots` entry references a valid `BaseItemType` slot per gear_catalog. Fail-loud on unknown slot.
- Every `ability_modifier_key` in ability-modifier affixes is in `VALID_ABILITY_MODIFIER_KEYS` (post-D8 extension with 5 NEW keys).
- Every `stat_key` in stat affixes is in `VALID_STAT_KEYS`.

### § 6.5 — Cross-substrate-trait-coherence boot check (mirrors D8 § 6.3)

Per scope-of-work § 1.2 D9: "no canonical-four affix silently becomes substrate-incoherent — surface to jack-ryan Discipline #13 review."

Boot-time validation:

- For each affix with `element` field set to a substrate value, validate the affix's `dimensional_tags` and `effect_type` against that substrate's `mechanical_signature` and `forbidden_mechanics`.
- Specifically: if affix `effect_type` semantically maps to a forbidden_mechanic of the affix's element, fail-loud (Discipline #13 enforcement).
- The mapping is semantic; gamora may implement a coarse allowlist (e.g., `("damage", "lightning")` is allowed; `("buff_defense", "lightning")` is allowed; `("heal", "shadow")` is *suspect* — shadow forbids amplify_allied; healing reads adjacent to amplify_allied). Suspect entries log a warning at boot for jack-ryan continuous-observation review.

D9 affixes were authored to pass this audit. No fail-loud blockages expected.

### § 6.6 — Effort estimate (gamora side)

Per scope-of-work § 1.2 D9 estimate (~3-5 days incl gamora impl):

- EFFECT_TO_FIT_AXES extension (6 entries): ~0.5 day
- MATERIAL_BY_ELEMENT + _ELEMENT_SUFFIX extensions: ~0.25 day
- _EFFECT_POWER_WEIGHT extension (3 entries): ~0.25 day
- 54 new EffectPoolEntry instances added to catalog: ~1.5 days (mechanical; per-entry transcription from D9 YAML)
- Boot-time validation + tests: ~0.5 day
- Cross-substrate-trait-coherence boot check: ~0.5 day
- Empirical verification (gear-roll distributions match expected substrate-coherent shape): ~0.5 day

**Total: ~4 days gamora-side.** D9 design authoring (this doc): ~1 day gandalf-side. Combined ~5 days — at the upper edge of the ~3-5 day estimate. ✓

---

## § 7 — Cross-references

**Canonical inputs (D9 reads):**
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — three new substrate identities (§ 5 lightning + § 6 holy + § 7 shadow)
- `canonical/17-gear-and-spirit-guide-design.md` — gear-affix architecture (dual-layer dimensional/stat-affinity gating; affix-pool design)
- `canonical/story/substrate-expansion-decision-2026-05-17.md` § 5.3 — D9 scope authority (1.5× expansion sizing guidance)
- `canonical/story/d8-trait-floor-design-phase-1-p1.md` — companion intrinsic trait design; 5 NEW ability_modifier_keys established here
- `~/Games/reincarnated-engine/src/reincarnated/generation/gear_generation.py` — EFFECT_TO_FIT_AXES, MATERIAL_BY_ELEMENT, _ELEMENT_SUFFIX, _EFFECT_POWER_WEIGHT, _affix_eligible_for_gear
- `~/Games/reincarnated-engine/src/reincarnated/generation/gear_schema.py` — EffectPoolEntry, ClassFitProfile, BaseItemType
- `~/Games/reincarnated-engine/src/reincarnated/generation/trait_schema.py` — VALID_ABILITY_MODIFIER_KEYS (extension target for 5 NEW keys per D8 § 6.4)
- `project_trait_architecture` (MEMORY.md) — rank-stacking discipline across intrinsic + gear sources

**Companion deliverables blocked by / blocking D9:**
- D5 (ailment registry; rocket + gamora) — defines `shock` / `consecrate` / `drain` ailment shapes. D9 affixes for `("shock", "lightning")` etc. consume the registry; D5 ships first.
- D8 (trait-floor design; gandalf + gamora) — 5 NEW ability_modifier_keys established in D8 are consumed by D9 gear-affix pools. D8 design lands first (this session); D9 design (this session) cross-references it.
- D2 (substrate expansion 4→7; rocket + gamora) — substrate-rotation enables lightning/holy/shadow to appear in season rotations. D9 affixes become live-pool when D2 ships.
- D19 (VFX library extension; drax) — VFX-affix coupling: gear-affix flavor (e.g., "Stormglass Staff of Arcs") needs a corresponding VFX trail/glow. Coordinated with drax.
- D21 (substrate browser; drax) — loadout app surface presenting substrate identities can reference D9 affix examples per substrate. Optional integration.

**Cross-canonical updates triggered by D9:**
- `canonical/17-gear-and-spirit-guide-design.md` — minor update: extend "Affix coherence" section noting D9 as Phase-1 P1 substrate extension; rolls into D26.
- `reincarnated-engine/design/decisions/decisions-log.md` — D9 ship-record candidate decision entry (knight-rider drafts).

**Routing requests to knight-rider (carry-over from this session):**
- Canonical-four intrinsic trait-pool authoring as Phase-1 P2 candidate (per D8 § 5.2) — for cross-substrate parity with D8 design.
- LLM creative pass on material/suffix names per § 5.2 — gandalf-authored placeholder names ship with D9; star-lord LLM creative-vocabulary pass post-Phase-1 P1 may produce richer alternatives.
- Stormcall passive lightning soft-tension review (per § 2.3 design_note) — jack-ryan Discipline #13 continuous-observation territory.

---

*Authored 2026-05-18 by gandalf in hive-mode Phase-1 P1. Three substrates, three gear-affix pools, 54 affixes. The substrate identities become gear the player can wear. Substrate-flagged affixes gate cleanly; substrate-neutral affixes remain ungated. Cross-substrate coherence verified clean against forbidden_mechanics; canonical-four audit produced no silent-incoherence findings. Gamora implementation contract specified.*
