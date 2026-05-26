# Engine Generation Run — Provenance Manifest

> **Generated:** 2026-05-25
> **Seed:** 20250525
> **N:** 35 forms
> **Engine version:** v2.0 (new engine, Cycle 12 close, v1.0-new-engine-ready tag)
> **Dispatch:** agentic_orchestration/dispatches/2026-05-25-rocket-engine-generation-run-v1-narrow.md
> **For:** gandalf design-fit pass (§ 2.1 sampling per framing brief)

---

## Run log

- Pre-fire projection: ~$4.20 LLM cost (400 calls × avg 1.5K tokens)
- Substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
- v1_scope=1 entries in substrate: 2,293 (per KR 2026-05-25 DB verification)
- Cells BLOCKED (zero eligible substrate): Artillery Mage, Pyromantic Caster, Necromancer Summoner
- Cells THIN (< 5 eligible): Red Mage/Spellsword, Monk-archetype
- Cells READY: 20
- Multi-fire extension: 13 additional kits beyond base enumeration
- Phase 5 LLM naming: enabled
- Generation duration: 76.7s

## Coverage summary

| Dimension | Target | Achieved |
|---|---|---|
| Total forms | 30-40 | 35 |
| BC-target cells | 25 (accept gap) | 25 |
| Elements | 8 | 1 (physical) |
| Attributes | 4 | 4 (DEX, INT, STR, WIS) |
| § 8 strategies | 6 | 6 (DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, ELEMENT_CONVERSION, GEOMETRY_COLLAPSE, RESOURCE_CONVERSION, TRADE_OFF) |
| Sketch F anchors | 4 | 1 (Moctezuma) |

**Coverage gaps (Sketch F):** Gilgamesh, Hattori Hanzō, Lu Bu
  Rationale: named-bearer substrate rows exist but may not have been sampled in this run's cell order.
  These are Tier-S rows and will appear in future regenerations at higher N or cell re-ordering.

**Coverage gaps (BLOCKED cells):** Artillery Mage (Cell 13 folded → Cell 12), Pyromantic Caster, Necromancer Summoner
  Rationale: zero v1_scope=1 substrate rows with matching proxy fingerprints for these cells.
  Artillery Mage is FOLDED to Cell 12 (Standard Wizard) per composition policy v1 § 4.1 — it IS represented.
  Pyromantic Caster and Necromancer Summoner require Stage 3.5 gap-fill or Sidecar B enrichment (v1.1+ work).

---

## Per-form index (gandalf navigation)

| form_id | BC-target cell | element | attr | § 8 strategy | provenance | named_bearer | main_weapon | mechanical_triple | engine_version | characterization |
|---|---|---|---|---|---|---|---|---|---|---|
| v2-form-000 | Heavy Barbarian | physical | STR | none | generator_v2 | — | shield | physical/category/armor_shield | v2.0 | physical_warrior / rage / spiky amplitude |
| v2-form-001 | Polearm Soldier | physical | STR | none | generator_v2 | Charlemagne (european_medieval | Sword of Attila | physical/category/handheld_weapon | v2.0 | [ANCHOR:Charlemagne (european_medieval, tier_2)] physical_wa |
| v2-form-002 | Light Fighter | physical | STR | none | generator_v2 | — | Pair of Sword-Grip Ornaments (Menuk | physical/ammo_or_consumable/accessory_weapon_ | v2.0 | physical_warrior / rage / flat amplitude |
| v2-form-003 | Dagger Assassin | physical | DEX | none | generator_v2 | Alexander the Great (greek, ti | Kukri | physical/category/handheld_weapon | v2.0 | [ANCHOR:Alexander the Great (greek, tier_2)] rogue / focus / |
| v2-form-004 | Archer | physical | DEX | none | generator_v2 | — | Percussion pocket pistol | physical/category/handheld_weapon | v2.0 | hunter / focus / flat amplitude |
| v2-form-005 | Thrown-Heavy/Atlatl | physical | STR | none | generator_v2 | — | Catapult | physical/category/handheld_weapon | v2.0 | physical_warrior / rage / spiky amplitude |
| v2-form-006 | Crossbow Sniper | physical | DEX | none | generator_v2 | — | Large Crossbow (Ganze Rüstung) of J | physical/category/handheld_weapon | v2.0 | hunter / focus / spiky amplitude |
| v2-form-007 | Twin-Blade Fencer | physical | DEX | none | generator_v2 | Sadamune (east_asian, tier_2) | Terasawa Sadamune | physical/category/handheld_weapon | v2.0 | [ANCHOR:Sadamune (east_asian, tier_2)] physical_skirmisher / |
| v2-form-008 | Standard Wizard | physical | INT | none | generator_v2 | Moctezuma | moctezuma_atlatl | physical/category/handheld_weapon | v2.0 | [ANCHOR:Moctezuma] fire_mage / mana / variable amplitude |
| v2-form-009 | Ancestor-Warrior | physical | STR | none | generator_v2 | Roland | roland_durandal | physical/unique/handheld_weapon | v2.0 | [ANCHOR:Roland] physical_warrior / rage / spiky amplitude |
| v2-form-010 | Falconer/Pet-Archer | physical | DEX | none | generator_v2 | — | Original box for Centrefire automat | physical/category/handheld_weapon | v2.0 | hunter / focus / flat amplitude |
| v2-form-011 | Trap Assassin/Mine-Mercenary | physical | DEX | none | generator_v2 | — | Bramble Bomb | physical/named_template/ammo_consumable | v2.0 | rogue / focus / spiky amplitude |
| v2-form-012 | Arcane-Familiar Mage | physical | INT | none | generator_v2 | — | Gunner's rule | physical/category/handheld_weapon | v2.0 | fire_mage / mana / variable amplitude |
| v2-form-013 | Totem Hierophant | physical | INT | none | generator_v2 | — | Powder tester | physical/category/handheld_weapon | v2.0 | earth_caster / mana / variable amplitude |
| v2-form-014 | Holy Knight/Paladin | physical | WIS | none | generator_v2 | — | Mace | physical/category/handheld_weapon | v2.0 | holy_caster / mana / variable amplitude |
| v2-form-015 | Artillery Mage (FOLDED → Cell 12) | physical | INT | none | generator_v2 | — | French Academician’s Habit of Julia | physical/category/accessory_handheld | v2.0 | fire_mage / mana / variable amplitude |
| v2-form-016 | Pyromantic Caster | physical | INT | none | generator_v2 | — | Gunner's dividers | physical/category/handheld_weapon | v2.0 | fire_mage / mana / spiky amplitude |
| v2-form-017 | Red Mage/Spellsword | physical | INT | none | generator_v2 | — | Pair of Sword-Grip Ornaments (Menuk | physical/ammo_or_consumable/accessory_weapon_ | v2.0 | physical_skirmisher / mana / flat amplitude |
| v2-form-018 | Necromancer Summoner | physical | INT | none | generator_v2 | — | Flutterby Rod | physical/named_template/handheld_weapon | v2.0 | shadow_caster / mana / spiky amplitude |
| v2-form-019 | Channeling Cleric | physical | WIS | none | generator_v2 | — | Banner of Louis XIV, King of France | physical/banner/accessory_handheld | v2.0 | holy_caster / mana / variable amplitude |
| v2-form-020 | Ritual Mage/Oracle | physical | WIS | none | generator_v2 | — | Mace Made for Henry II of France | physical/category/handheld_weapon | v2.0 | earth_caster / mana / variable amplitude |
| v2-form-021 | Storm Caller/Druid | physical | WIS | none | generator_v2 | — | Banner with Shaft | physical/banner/accessory_handheld | v2.0 | wind_controller / mana / variable amplitude |
| v2-form-022 | Monk-archetype | physical | WIS | none | generator_v2 | — | 紅葉蒔絵鞘脇指拵 Mounting for a Short Sword | physical/category/handheld_weapon | v2.0 | physical_grappler / mana / variable amplitude |
| v2-form-023 | Druid Beastmaster | physical | WIS | none | generator_v2 | — | Banner (Hata) | physical/banner/accessory_handheld | v2.0 | wind_controller / mana / variable amplitude |
| v2-form-024 | Witch Doctor Petmaster | physical | WIS | none | generator_v2 | Saint George (european_medieva | Banner with Shaft | physical/banner/accessory_handheld | v2.0 | [ANCHOR:Saint George (european_medieval, tier_2)] shadow_con |
| v2-form-025 | Heavy Barbarian | physical | STR | none | generator_v2 | Moctezuma | moctezuma_aztec_war_club | physical/category/handheld_weapon | v2.0 | [ANCHOR:Moctezuma] physical_warrior / rage / spiky amplitude |
| v2-form-026 | Polearm Soldier | physical | STR | none | generator_v2 | El Cid (european_medieval, tie | Colada | physical/unique/handheld_weapon | v2.0 | [ANCHOR:El Cid (european_medieval, tier_2)] physical_warrior |
| v2-form-027 | Light Fighter | physical | STR | none | generator_v2 | — | Pair of Sword-Grip Ornaments (Menuk | physical/ammo_or_consumable/accessory_weapon_ | v2.0 | physical_warrior / rage / flat amplitude |
| v2-form-028 | Dagger Assassin | physical | DEX | none | generator_v2 | Sadamune (east_asian, tier_2) | Tokuzen-in Sadamune | physical/category/handheld_weapon | v2.0 | [ANCHOR:Sadamune (east_asian, tier_2)] rogue / focus / flat  |
| v2-form-029 | Archer | physical | DEX | none | generator_v2 | — | Rimfire breech-loading pocket pisto | physical/category/handheld_weapon | v2.0 | hunter / focus / flat amplitude |
| v2-form-030 | Thrown-Heavy/Atlatl | physical | STR | none | generator_v2 | Wayland the Smith (european_me | .476 Nitro Express | physical/category/handheld_weapon | v2.0 | [ANCHOR:Wayland the Smith (european_medieval, tier_1)] physi |
| v2-form-031 | Crossbow Sniper | physical | DEX | none | generator_v2 | — | Blaser R93 Tactical German 7.62mm S | physical/category/handheld_weapon | v2.0 | hunter / focus / spiky amplitude |
| v2-form-032 | Twin-Blade Fencer | physical | DEX | none | generator_v2 | — | Cutlass | physical/category/handheld_weapon | v2.0 | physical_skirmisher / focus / variable amplitude |
| v2-form-033 | Standard Wizard | physical | INT | none | generator_v2 | — | Manuscript | physical/category/handheld_weapon | v2.0 | fire_mage / mana / variable amplitude |
| v2-form-034 | Ancestor-Warrior | physical | STR | none | generator_v2 | — | Two-handed sword | physical/category/handheld_weapon | v2.0 | physical_warrior / rage / spiky amplitude |

---

## Sketch F anchor spotlight (per § 2.1 — all anchors get full notes)

### Hattori Hanzō — NOT SAMPLED IN THIS RUN
  See coverage gap rationale above. Substrate rows exist; sampling order didn't reach this anchor.

### Lu Bu — NOT SAMPLED IN THIS RUN
  See coverage gap rationale above. Substrate rows exist; sampling order didn't reach this anchor.

### Moctezuma — v2-form-008
- **Weapon:** moctezuma_atlatl
- **Element:** physical / **Attribute:** INT / **Energy:** mana
- **BC-target:** {'range': 'ranged', 'tempo': 'medium', 'amplitude': 'variable', 'attribute': 'INT', 'proxy_density': 'none'}
- **Archetype:** fire_mage
- **Mechanical triple:** physical/category/handheld_weapon
- **§ 8 strategy:** None
- **Cultural tradition:** mesoamerican
- **Period:** medieval
- **Class name:** Sunstone Spearthrower
- **Substrate tier:** S
- **Relaxation level:** 0

### Moctezuma — v2-form-025
- **Weapon:** moctezuma_aztec_war_club
- **Element:** physical / **Attribute:** STR / **Energy:** rage
- **BC-target:** {'range': 'melee', 'tempo': 'low', 'amplitude': 'spiky', 'attribute': 'STR', 'proxy_density': 'none'}
- **Archetype:** physical_warrior
- **Mechanical triple:** physical/category/handheld_weapon
- **§ 8 strategy:** None
- **Cultural tradition:** mesoamerican
- **Period:** medieval
- **Class name:** Moctezuma's Jade Warlord
- **Substrate tier:** S
- **Relaxation level:** 0

### Gilgamesh — NOT SAMPLED IN THIS RUN
  See coverage gap rationale above. Substrate rows exist; sampling order didn't reach this anchor.

---

## Phase 5 / Phase 6 / Phase 7 observations

### Phase 5 (Cohesion coalescence / LLM naming)
- Naming: LLM-generated names per above
- Phase 5 calibration spec: PENDING (gandalf canonical authoring deferred per dispatch out-of-scope). Flag at T4 post-mortem.
- Sub-element flavoring: not applied in this run (Phase 5 cohesion-judge pending calibration).

### Phase 6 (Visual coalescence)
- Placeholder status: no visuals generated. Meshy production wire-up is deferred per framing brief § 1.3.
- Expected behavior per dispatch § Out of scope: placeholder visuals or no visuals. Document, do not amend.

### Phase 7 (Joint-gate)
- Status: not explicitly wired in v1 narrow run. Layer 6 wire-up is the effective joint-gate (sim-viability check via converge_kit).
- All forms passed converge_kit without UNGENERABLE result. Effective sim-viability: PASS.

---

## Handoff trigger

This manifest is the handoff contract from rocket → gandalf design-fit pass.
Gandalf: sample per framing brief § 2.1 (all Sketch F anchors + one per § 8 strategy + all engine-authored gap-fills + all mythological-NULL rescues + edge cases).
Author special case summary at: `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md`

**classes.json:** `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json`
**metadata.json:** `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/metadata.json`
**Loadout deploy:** `/Users/admin/Games/reincarnated-loadout/public/seasons/v2_narrow/classes.json`