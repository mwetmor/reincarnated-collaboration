# Attribute System — Reincarnated v1 Operational Definition

> **STATUS:** CURRENT — PROPOSED operational definition consolidating scattered attribute references; Stage 0 design call may amend at lock-time. Authored as Cycle 10 substrate-curation dispatch prerequisite per Matt 2026-05-24.

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — locks 4-attribute system (STR / INT / WIS / DEX) as v1 operational truth; defers VIT to v1.1+
**Authority:** Matt 2026-05-24 — Cycle 10 Stage 0 prerequisite confirmation (Stream A1 composite authoring)
**Companion docs:**
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes (attribute = 4-tuple BC-target subspace dimension)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — Phase 2 generation consumes attribute coupling
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — element-attribute coupling per ω-field resource dimension
- `canonical/story/skill-system-2026-05-24.md` — Stream A1 sibling doc; Phase 2 skill composition consumes attribute coupling
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE (current 3-attribute coupling)
- `~/Games/reincarnated-loadout/data/telemetry.db` (`weapon_sim_props.primary_stat` + `secondary_stat` — current 3-attribute CHECK constraint)

---

## 0. TL;DR

Reincarnated v1 operates on a **4-attribute system: STR / INT / WIS / DEX.**

- **STR / INT / WIS** — already partially documented across `element_biases.py:28` (ELEMENT_SCALING_ATTRIBUTE) and `weapon_sim_props` schema
- **DEX** — added as Stage 0 prerequisite per BC-target 4-tuple subspace requirements (range × tempo × amplitude × attribute = 108 cells); needed to distinguish dagger-rogue / archer / sniper from STR-melee and INT-caster patterns
- **VIT** — deferred to v1.1+; defensive-profile BC axis (Axis #7) subsumes for v1; revisit when player-facing health-scaling architecture surfaces as load-bearing

This doc consolidates scattered attribute references into a single canonical reference. It is a PROPOSED operational definition; Stage 0 design call may amend at lock-time.

---

## 1. The 4 attributes

### 1.1 STR — Strength
- **Scaling domain:** Physical damage; melee weapon damage; carrying capacity (if surfaced); heavy-weapon attack speed
- **Genre precedent:** D&D STR; D2/D3/D4 STR; PoE Strength; isekai brawler/berserker archetypes
- **Class archetypes:** Barbarian, Warrior, Greatsword Champion, Heavy Knight, Berserker
- **Weapon families:** Greatswords, war-hammers, two-handed axes, heavy polearms, mauls

### 1.2 INT — Intelligence
- **Scaling domain:** Arcane / spell damage; cast-speed; mana capacity (if surfaced)
- **Genre precedent:** D&D INT; D2/D3/D4 INT; PoE Intelligence; isekai mage archetypes
- **Class archetypes:** Wizard, Sorcerer, Pyromancer, Frost Mage, Shadow Caster
- **Weapon families:** Wands, staves, arcane focuses, tomes, orbs

### 1.3 WIS — Wisdom
- **Scaling domain:** Channeled / ritual / divine effect magnitude; channel-stability; willpower-cast damage
- **Genre precedent:** D&D WIS; D2 has no separate WIS (uses ENG); PoE has no separate WIS; D4 has no separate WIS; **Reincarnated splits WIS from INT** to distinguish ritual/channel-cast (earth/wind/holy elements) from arcane-cast (fire/water/lightning/shadow elements)
- **Class archetypes:** Cleric, Druid, Holy Knight, Ritualist, Channeler, Oracle, Witch Doctor
- **Weapon families:** Maces, holy-symbols, ritual-implements, channeled-staves, censers, horns

### 1.4 DEX — Dexterity (NEW for v1)
- **Scaling domain:** Precision / finesse damage; attack-speed (light weapons); critical-strike rate; ranged-weapon damage; dodge/evasion (if surfaced)
- **Genre precedent:** D&D DEX; D2 DEX; D3 DEX; PoE Dexterity; isekai rogue/archer archetypes
- **Class archetypes:** Rogue, Dagger Assassin, Archer, Crossbow Sniper, Twin-Blade Fencer, Wind-Dancer
- **Weapon families:** Daggers, kris, stilettos, bows, crossbows, twin-blades, light shields

### 1.5 VIT — Vitality (DEFERRED to v1.1+)
- **Scaling domain (when activated):** Max HP; physical damage mitigation; status-resistance
- **Genre precedent:** D&D CON; D2 VIT; D3 has no separate VIT (life from main stat); D4 has no separate VIT
- **v1 disposition:** NOT a separate attribute; defensive-profile BC axis (Axis #7) carries the design space
- **v1.1+ trigger:** Player-facing health-scaling architecture surfaces as load-bearing AND class-defensive-identity differentiation needs more dimensionality than defensive-profile axis provides

---

## 2. Element-attribute coupling

Per `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` (`ELEMENT_SCALING_ATTRIBUTE`):

| Element | Scaling attribute | Notes |
|---|---|---|
| fire | INT | Arcane combustion |
| water | INT | Arcane fluid |
| lightning | INT | Arcane electricity |
| shadow | INT | Arcane darkness |
| earth | WIS | Ritual stone / nature |
| wind | WIS | Ritual air / breath |
| holy | WIS | Divine / channeled |
| physical | STR | Strength-cast / mundane |
| **(DEX coupling)** | **(TBD — see § 2.1 below)** | **PROPOSED for v1 lock** |

### 2.1 DEX coupling proposal

DEX scaling needs an element-coupling that distinguishes it from the existing STR/INT/WIS bindings. Proposed:

**Option A — DEX couples to physical (alongside STR), differentiated by weapon-class:**
- physical + STR-weapons (greatswords, two-handed-axes) → STR scaling
- physical + DEX-weapons (daggers, bows, light blades) → DEX scaling
- Element_biases.py extension: `ELEMENT_SCALING_ATTRIBUTE['physical'] = ['STR', 'DEX']` (multi-attribute coupling with weapon-class disambiguation)

**Option B — DEX couples to wind (alongside WIS), differentiated by tempo/geometry:**
- wind + WIS-weapons + ritual/channel patterns → WIS scaling
- wind + DEX-weapons + precision-strike patterns → DEX scaling
- Genre precedent: wind-DEX archer (Sylvanas-archetype, isekai wind-elf-archer); WIS-wind ritual druid

**Option C — DEX couples to no element specifically; weapon-class drives DEX scaling independent of element:**
- DEX is a "weapon-property" attribute rather than an "element-property" attribute
- Element scaling (per existing table) determines spell-effect magnitude; DEX scaling determines weapon-strike magnitude; both can apply simultaneously to a hybrid kit
- Cleaner architecture; matches D&D 5e + most modern ARPGs

**Recommended (gandalf lean):** Option C. DEX as weapon-property attribute decouples cleanly from element-system. Avoids forcing element-DEX binding decisions that have to be made for every new element added.

**Lock at Stage 0 design call.**

---

## 3. Attribute-weapon coupling

Each weapon's `primary_stat` in `weapon_sim_props` schema indicates which attribute the weapon scales with. Current schema: `CHECK (primary_stat IN ('STR','INT','WIS'))`.

**Proposed schema extension for v1:**

```sql
ALTER TABLE weapon_sim_props
DROP CONSTRAINT IF EXISTS check_primary_stat;
ALTER TABLE weapon_sim_props
ADD CONSTRAINT check_primary_stat CHECK (primary_stat IN ('STR','INT','WIS','DEX'));

ALTER TABLE weapon_sim_props
DROP CONSTRAINT IF EXISTS check_secondary_stat;
ALTER TABLE weapon_sim_props
ADD CONSTRAINT check_secondary_stat CHECK (secondary_stat IN ('STR','INT','WIS','DEX','none'));
```

(Elrond seam executes ALTER as part of Cycle 10 Stage 1.5 or Stage 4 schema-extension work.)

**Weapon-family attribute mappings (representative, not exhaustive):**

| Weapon family | Typical primary_stat | Typical secondary_stat | Notes |
|---|---|---|---|
| Greatsword / two-handed-axe / maul / heavy-polearm | STR | none | Heavy melee; STR-anchored |
| Shortsword / arming-sword / falchion | STR | DEX | Light melee; STR-primary, DEX-finesse-flexible |
| Dagger / kris / stiletto / main-gauche | DEX | none | Finesse melee; DEX-anchored |
| Bow / longbow / shortbow | DEX | none | Precision-ranged; DEX-anchored |
| Crossbow / arbalest | DEX | STR | Mechanical-ranged; DEX-precision + STR-draw |
| Wand / orb / arcane-focus | INT | none | Arcane-cast; INT-anchored |
| Staff (arcane) | INT | WIS | Arcane-cast with channel-pattern flexibility |
| Staff (channel) / holy-symbol / censer | WIS | INT | Ritual/channel-cast; WIS-anchored |
| Mace / war-hammer (one-handed) | STR | WIS | Holy-warrior pattern; STR-primary, WIS-divine-channeling |
| Throwing weapons (javelin / chakram / throwing-axe) | DEX | STR | Precision-throw; DEX-aim + STR-power |

Note: many weapons have **dual-attribute viability** (e.g., a shortsword viable for both STR-fighter and DEX-fencer). The substrate-curation work (Cycle 10 Stage 4 mechanical-tagging) determines `primary_stat` + `secondary_stat` per substrate row.

---

## 4. Attribute-BC-target coupling

The 4-tuple BC-target subspace (per Cycle 10 dispatch + Matt design dialogue 2026-05-24):

```
(range × tempo × amplitude × attribute)
= 3 (melee/mid/ranged) × 3 (low/med/high) × 3 (flat/variable/spiky) × 4 (STR/INT/WIS/DEX)
= 108 cells
```

Each cell represents a Phase 2 BC-target the engine can fire against. Substrate-curation work (Cycle 10) ensures each populated cell has viable weapon coverage.

**Per-cell density (qualitative, per genre canon):**

| Density tier | Approximate cell count | Examples |
|---|---|---|
| Core archetypes (high genre-canon density) | 10-20 cells | (melee, high, flat, DEX) = dagger-rogue; (melee, low, spiky, STR) = barbarian; (ranged, low, spiky, INT) = artillery-wizard |
| Niche but viable (medium genre-canon density) | 20-30 cells | (mid, low, spiky, WIS) = oracle; (melee, INT, *, *) = red-mage cross-attribute; (ranged, STR, *, *) = thrown-heavy |
| Sparse / contested (low genre-canon density) | 30-40 cells | (melee, low, flat, *) = heavy slow even-damage feels off; (ranged, WIS, high, *) = ranged WIS-channeling typically static |
| Effectively empty (no genre canon) | 30-40 cells | Combinations that don't manifest in genre canon |

Stage 0 design call locks which cells v1 ships forms from + relative target-weights.

---

## 5. Schema integration

### 5.1 Current state
- `weapon_sim_props.primary_stat` — CHECK ('STR','INT','WIS')
- `weapon_sim_props.secondary_stat` — CHECK ('STR','INT','WIS','none')
- DEX absent from schema

### 5.2 Proposed extension (v1 lock at Stage 0)
- Add DEX to both CHECK constraints (per § 3 ALTER TABLE statements)
- Substrate-curation work (Cycle 10 Stage 4) populates per-row primary_stat + secondary_stat including DEX

### 5.3 v1.1+ schema candidate (VIT)
- If VIT surfaces as load-bearing post-v1, add to primary_stat + secondary_stat OR add separate `vitality_scaling` column
- Currently NO schema commitment to VIT

---

## 6. Engine code references

- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — `ELEMENT_SCALING_ATTRIBUTE` lookup table
- `~/Games/reincarnated-engine/src/reincarnated/generation/` — skill composition consumes attribute coupling at Phase 2
- `~/Games/reincarnated-engine/src/reincarnated/simulation/` — sim resolves attribute-scaled damage at runtime
- `~/Games/reincarnated-loadout/data/telemetry.db` — `weapon_sim_props` schema

---

## 7. Decisions deferred to Stage 0 design call

1. **DEX element coupling** — Option A (physical multi-attribute) / Option B (wind multi-attribute) / Option C (weapon-property only) per § 2.1; gandalf recommends C
2. **DEX cell-weight in v1 BC-target intent** — what fraction of v1 forms target DEX-attribute cells
3. **Multi-attribute kit support** — can a kit have BOTH primary STR AND primary DEX (dual-attribute build), or is primary attribute strictly one
4. **Secondary attribute coverage** — what fraction of substrate weapons have meaningful secondary_stat vs primary-only

---

## 8. What this doc does NOT do

- NOT a final lock — Stage 0 design call may amend any section
- NOT an engine-code change — proposed schema extensions execute at Cycle 10 Stage 1.5 or Stage 4
- NOT a VIT commitment — VIT explicitly deferred to v1.1+
- NOT a skill-system doc — see sibling `canonical/story/skill-system-2026-05-24.md`
- NOT a class-roster doc — pipeline architecture obviates class roster per Cycle 10 design dialogue 2026-05-24

---

## 9. Cross-references

### Active project canon this doc grounds in
- `canonical/00-ground-state.md` § 1 (current truth oracle)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes — attribute is dimension of 4-tuple BC-target subspace)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` (Phase 2 generation consumes attribute coupling)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` § 1.1 (ω-field resource dimension uses attribute coupling)
- `canonical/story/skill-system-2026-05-24.md` (Stream A1 sibling — consumes attribute coupling)

### Live state references
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28`
- `~/Games/reincarnated-loadout/data/telemetry.db` (`weapon_sim_props` schema)

### Downstream artifacts this doc anchors
- Cycle 10 Stage 0 design call (consumes vocabulary)
- Cycle 10 Stage 1 + 1.5 + 4 (consumes attribute schema for weapon tagging)
- Future v1.1+ VIT addition (if/when triggered)

---

## 10. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-24 — Cycle 10 Stage 0 prerequisite per Stream A1 composite authoring confirmation
**Status:** CURRENT — PROPOSED operational definition; Stage 0 design call may amend
**Re-engagement gate:** Stage 0 design call locks final attribute system for v1; this doc updates per Stage 0 outputs OR stands as v1 operational truth if Stage 0 endorses without amendment

---

**Signed:** gandalf
**For:** the canonical operational definition of the 4-attribute system (STR / INT / WIS / DEX) consolidating scattered references and preparing Stage 0 design call substrate. VIT explicitly deferred. DEX coupling lock proposed at Stage 0.
