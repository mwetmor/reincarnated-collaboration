# Gear Substrate Rule-Table v1 — Substrate-Vector × Gear-Substrate Mapping for W1.15

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Date:** 2026-05-22 (authored under G1-LITE framing) / amended 2026-05-22 evening (gear-heavy + archetype-drop + role_orientation-drop reframe)
**Author:** gandalf (story-and-design steward; senior designer)
**Status:** v1 rule-table SURFACE-CLEANED for naming + scope; FULL-RESTRUCTURE PENDING in tomorrow's canonical doc session (sections 4-9 still carry 252-combination v0.9 structure; 63-combination v1 restructure pending under role_orientation drop)
**Authority:** Matt 2026-05-22 (this session) — three canonical calls:
- Drop "archetype" terminology engine-wide; replace with "gear substrate" / "gear" (concept) and "reference build" (for ARPG-canon descriptive labels)
- Drop `role_orientation` from rule-table input space as vestigial pre-W0.2 categorical thinking incompatible with substrate-as-cohesion
- Rename G1-LITE → G1 under gear-heavy promotion (gear as real mechanical substrate; LITE framing retired)

**Companions:**
- `canonical/story/historical/gear-as-substrate-2026-05-21.md` § 3 (15-gear catalogue source — terminology pending sweep)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI ω/τ tables (informs rule-design decisions)
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 6.2.2 — W1.15 workstream
- `canonical/story/role-orientation-vestigial-audit-2026-05-22.md` (pending tomorrow morning) — vestigial taxonomy cleanup canonical
- `canonical/story/gear-heavy-promotion-2026-05-22.md` (pending tomorrow morning) — LITE→HEAVY rename + tier hierarchy + WR-bracket-under-gear sequencing

---

## 0. TL;DR

The G1 rule table maps the substrate-vector space to the 15-gear catalogue. Gear is a substrate in the post-W0.2 substrate-as-cohesion sense (emergent identity, not pre-imposed archetype).

`signature_gear = f(dominant_element, range_profile, stat_distribution_signature)`

**Input space (63 combinations under post-amendment v1; sections 4-9 below still enumerate the pre-amendment 252-combination structure pending the full restructure):**
- `dominant_element`: 7 values (fire, water, earth, wind, lightning, holy, shadow) — physical excluded from canonical-7 per D2 resolution
- `range_profile`: 3 values (melee, medium, ranged)
- `stat_distribution_signature`: 3 values (INT-dominant, WIS-dominant, STR-dominant)

**Output:** 15 gear values per `gear-as-substrate-2026-05-21.md` § 3 + `no_signature` rare mismatch case (rocket-recommended valid output per W1.1 surface)

**Rule design principles:**
- Canonical pairings privileged (holy + censer; shadow + veil; lightning + wand)
- Range-axis dominance (ranged + INT → focus-orb / wand family; melee + STR → greatsword / warhammer family)
- Cross-attribute / off-natural branches handle rare cases (e.g., a fire class that is STR-dominant via gear-and-trait pressure)
- Surprising-but-evocative pairings allowed where genre-precedent supports (holy + blunderbuss = Holy Pirate Sniper)
- Role flavor emerges from converged BC mechanical signature post-generation; NOT pre-imposed as rule-table input

Sim-viability concerns flagged per-gear for rocket verification.

**What this amendment changes:**

The original 2026-05-22 morning authoring of this doc carried `role_orientation` as a 4th input dimension and used "gear-archetype" as both the concept-name and output-value-name. Matt's 2026-05-22 evening session retired both:

1. **role_orientation drop:** vestigial pre-W0.2 categorical thinking. Generation is substrate-agnostic; role emerges from the 8 BC axes post-convergence, not from pre-imposed `damage / control / support / hybrid` tags. Diagnostic-only groupings (`mage_controller`, `physical_rogue`) remain available for legacy attribution tooling but are NOT generation inputs.
2. **archetype terminology drop:** "gear-archetype" implies categorical pre-imposition. Replaced with "gear substrate" (concept) or "gear" (catalogue entry). The 15-gear catalogue stays; only the naming changes.
3. **LITE→HEAVY rename:** gear-as-substrate is real in v1+ at the derived-tag-plus-tier-hierarchy level; full *generative* substrate promotion remains v1.1+ (G-PROMOTE-v1.1). LITE framing retired.

**Sections 4-9 below carry the pre-amendment 252-combination structure** (since they were authored against the 4-input space). The full restructure to 63-combination v1 is queued for tomorrow's canonical doc session. The principles + catalogue + naming above are the canonical surface as of this amendment; the table structure below is reference-only-until-restructured.

---

## 1. Input dimensions

### 1.1 dominant_element (7 values)

Per `element_biases.py:28` ELEMENT_SCALING_ATTRIBUTE (canonical-7 lock per D2):

| Element | Canonical scaling attribute | Identity stance |
|---|---|---|
| fire | INT | combustion / volatility / burst |
| water | INT | precision / chill / tide |
| earth | WIS | mass / binding / weight |
| wind | WIS | momentum / precision / mobility |
| lightning | INT | speed / chain / branching |
| holy | WIS | judgment / blessing / sustain |
| shadow | INT | trade-off / drain / ambush |

### 1.2 [RETIRED — role_orientation] (was 4 values)

**Retired 2026-05-22 evening per Matt canonical call.** role_orientation was a pre-W0.2 categorical surface (damage / control / support / hybrid) that survived the archetype-template cleanup as legacy scaffolding. Generation is substrate-agnostic; role emerges from the 8 BC axes (damage tempo, control density, proxy density, defensive profile, etc.) post-convergence — not from pre-imposed categorical tags.

`project_role_orientation_taxonomy.md` (2026-05-08) is marked historical/diagnostic-only, not architectural commitment. The `mage_controller` / `physical_rogue` groupings used in W0.7 LC-attribution work remain available as **legacy diagnostic-only attribution tooling**, NOT as generation inputs.

Full canonical rationale: `canonical/story/role-orientation-vestigial-audit-2026-05-22.md` (pending tomorrow's canonical authoring session).

### 1.3 range_profile (3 values)

Per `qd-engine-bc-axes-lock-2026-05-20.md` Axis 1 (engagement profile range component):

| Range | Mean weighted skill range |
|---|---|
| melee | ≤ 3.0 units |
| medium | 3.0–8.0 units |
| ranged | ≥ 8.0 units |

### 1.4 stat_distribution_signature (3 values)

Derived from class stat priority + `ELEMENT_SCALING_ATTRIBUTE` (per element default) + class-template stat distribution:

| Signature | Stat priority |
|---|---|
| INT-dominant | primary INT; spell-cast emphasis; magical scaling |
| WIS-dominant | primary WIS; ritual-cast emphasis; channeled scaling |
| STR-dominant | primary STR; melee-power emphasis; physical scaling |

**Per-element natural default** (from element_biases.py):
- fire / water / lightning / shadow → INT-dominant natural
- earth / wind / holy → WIS-dominant natural
- (physical would be STR-dominant; physical excluded from canonical-7)

A class can rarely be off-natural (e.g., a fire class that is STR-dominant via gear-and-trait pressure) — the rule table handles these off-natural cases via "cross-attribute" branches.

---

## 2. 15-gear catalogue (per gear-as-substrate § 3)

| # | Gear | Range | Tempo | Stance | Natural element family |
|---|---|---|---|---|---|
| 1 | Greatsword | melee | slow | knight-overwhelming | physical / fire |
| 2 | Twin daggers | melee | fast | rogue-precision | shadow / wind |
| 3 | Battle spear / longstaff | melee-medium | medium | disciplined-distance | earth / wind |
| 4 | Mace / warhammer | melee | slow | paladin-or-warlord | physical / earth / holy |
| 5 | Longbow | ranged | medium | hunter-clean | wind / water |
| 6 | Crossbow | ranged | slow | mercenary-tactical | physical / holy |
| 7 | Blunderbuss / scattergun | ranged-medium | slow | pirate-outlaw | physical / fire / holy |
| 8 | Throwing knives / chakram | medium | fast | assassin-harasser | shadow / wind / lightning |
| 9 | Wand / focus rod | medium-ranged | fast | precision-mage | lightning / water / shadow |
| 10 | Orb / sphere | medium | medium | elementalist-area | fire / water |
| 11 | Caster staff | ranged | slow | archmage-grandeur | fire / lightning |
| 12 | Tome / grimoire | indirect | medium | summoner-scholar | shadow / holy |
| 13 | Censer / thurible | medium | slow | cleric-sustain | holy / shadow |
| 14 | Holy symbol / icon | medium-ranged | medium | exorcist-smite | holy |
| 15 | War-trumpet / horn | medium | slow | evangelist-blast | holy / wind |

---

## 3. Rule-design priority hierarchy

When multiple archetypes are coherent for a given substrate-vector, the rule table selects by this priority hierarchy:

1. **Canonical pairing privileged** — if the (element, range, role, stat_dist) tuple has a well-trodden genre identity (Stormcaller = lightning + medium-ranged + damage + INT → Wand), select that
2. **Range-axis dominance** — range_profile constrains the archetype family first (melee → archetypes 1-4; medium → 8/9/10/12/13/14/15; ranged → 5/6/7/11)
3. **Role-axis tie-breakers within range family** — within a range family, role determines selection (control + medium → censer / chain; damage + medium → orb / wand)
4. **Stat-dist alignment** — within range × role, stat_dist alignment with archetype's natural-attribute family picks final archetype (INT-dom + medium + damage → wand/orb-family; WIS-dom + medium + support → censer/horn-family)
5. **Cross-attribute fallback** — when stat_dist is cross-attribute (e.g., fire + WIS-dom, or holy + INT-dom), prefer archetypes that thematically tolerate the cross-stat pressure (e.g., holy + INT-dom → holy_symbol / icon since holy_symbol is moderate WIS-favoring and beam/precision tolerates INT-cast)
6. **Surprising-but-evocative allowed** where genre-precedent supports (holy + ranged-medium + damage + WIS-dom → Blunderbuss = Holy Pirate Sniper)
7. **no_signature** fallback for genuinely incoherent vectors (e.g., support + melee + INT-dom for an element that has no canonical melee-INT-support identity)

---

## 4. Rule table — 252 substrate-vector combinations

The rule table is organized per-element. For each element, all 4 role_orientations × 3 range_profiles × 3 stat_dist combinations are mapped to archetype.

**Format:** `(role, range, stat_dist) → archetype [sim-viability flag if applicable]`

### 4.1 Fire (INT-natural; combustion / volatility / burst stance)

36 combinations.

| role | range | stat_dist | → archetype | Notes |
|---|---|---|---|---|
| damage | melee | INT-dom | Greatsword | Fire-Knight cross-attribute; fire-INT spell-warrior with greatsword. **FLAG sim-viability** — unconventional INT-melee combo |
| damage | melee | WIS-dom | Greatsword | Forge-warrior (WIS-cross); ritual-channel fire greatsword |
| damage | melee | STR-dom | Greatsword | Inferno-Knight (canonical fire + melee STR; per BDI § 5.1) |
| damage | medium | INT-dom | Orb / sphere | Pyromancer (canonical fire + orb + INT) |
| damage | medium | WIS-dom | Orb / sphere | Cross-attribute fire-orb-WIS; ritual fire-elementalist |
| damage | medium | STR-dom | Throwing knives / chakram | Powder Pyromaniac (multi-projectile fire); **FLAG sim-viability** |
| damage | ranged | INT-dom | Caster staff | Pyresage (canonical fire + ranged + INT archmage) |
| damage | ranged | WIS-dom | Caster staff | Fire-Ritualist; cross-attribute staff |
| damage | ranged | STR-dom | Blunderbuss / scattergun | Powder Pyromaniac; **FLAG sim-viability** |
| control | melee | INT-dom | Twin daggers | Fire-burst dagger control (debuff via burn) |
| control | melee | WIS-dom | Mace / warhammer | Forge-Smiter control variant |
| control | melee | STR-dom | Mace / warhammer | Forge-Smiter (STR + impact-concussive fire) |
| control | medium | INT-dom | Orb / sphere | Pyromancer-Controller (burn + chain-burn) |
| control | medium | WIS-dom | Censer / thurible | Smoke-Cleric (fire + sustain-aura ritual) |
| control | medium | STR-dom | Battle spear / longstaff | Fire-Lancer control |
| control | ranged | INT-dom | Caster staff | Pyresage-Controller (fire DoT + chain-burn) |
| control | ranged | WIS-dom | Caster staff | Fire-Ritualist-Controller |
| control | ranged | STR-dom | Crossbow | Fire-Bolt Inquisitor; **FLAG sim-viability** |
| support | melee | INT-dom | Twin daggers | Fire-precision dagger support (burn-debuff support); **FLAG** |
| support | melee | WIS-dom | Mace / warhammer | Fire-Cleric (rare); **FLAG sim-viability** |
| support | melee | STR-dom | Greatsword | Fire-Knight support variant; **FLAG sim-viability** |
| support | medium | INT-dom | Orb / sphere | Fire-Aura-Mage; canonical fire-area support |
| support | medium | WIS-dom | Censer / thurible | Smoke-Cleric (canonical fire + ritual support) |
| support | medium | STR-dom | War-trumpet / horn | Fire-Trumpet support; **FLAG sim-viability** |
| support | ranged | INT-dom | Caster staff | Fire-Ritualist support |
| support | ranged | WIS-dom | Caster staff | Fire-Ritualist (canonical-cross WIS-fire-stack) |
| support | ranged | STR-dom | Crossbow | Fire-Bolt support; **FLAG** |
| hybrid | melee | INT-dom | Twin daggers | Fire-precision-burst hybrid |
| hybrid | melee | WIS-dom | Mace / warhammer | Forge-warrior hybrid |
| hybrid | melee | STR-dom | Greatsword | Inferno-Knight hybrid |
| hybrid | medium | INT-dom | Orb / sphere | Pyromancer hybrid |
| hybrid | medium | WIS-dom | Censer / thurible | Smoke-Cleric hybrid |
| hybrid | medium | STR-dom | Battle spear / longstaff | Fire-Lancer hybrid |
| hybrid | ranged | INT-dom | Caster staff | Pyresage hybrid |
| hybrid | ranged | WIS-dom | Caster staff | Fire-Ritualist hybrid |
| hybrid | ranged | STR-dom | Crossbow | Fire-Bolt hybrid; **FLAG** |

### 4.2 Water (INT-natural; precision / chill / tide stance)

36 combinations.

| role | range | stat_dist | → archetype | Notes |
|---|---|---|---|---|
| damage | melee | INT-dom | Twin daggers | Frost-precision dagger (chill + multi-hit) |
| damage | melee | WIS-dom | Battle spear / longstaff | Tide-Lancer (cross-attribute) |
| damage | melee | STR-dom | Greatsword | Frost-Knight; **FLAG sim-viability** |
| damage | medium | INT-dom | Orb / sphere | Tide Elementalist (canonical water + orb) |
| damage | medium | WIS-dom | Censer / thurible | Tide-Cleric (cross-attribute WIS) |
| damage | medium | STR-dom | Throwing knives / chakram | Frost-Chakram; **FLAG** |
| damage | ranged | INT-dom | Longbow | Tide-Marksman (water + line + INT) |
| damage | ranged | WIS-dom | Longbow | Storm-Sentinel water-variant |
| damage | ranged | STR-dom | Crossbow | Frost-Bolt mercenary |
| control | melee | INT-dom | Twin daggers | Frost-precision control |
| control | melee | WIS-dom | Battle spear / longstaff | Tide-Lancer-Control |
| control | melee | STR-dom | Mace / warhammer | Frost-Hammer; **FLAG** |
| control | medium | INT-dom | Orb / sphere | Tide-Controller (canonical chill-control) |
| control | medium | WIS-dom | Censer / thurible | Tide-Cleric-Control |
| control | medium | STR-dom | Battle spear / longstaff | Tide-Lancer-Control STR-variant |
| control | ranged | INT-dom | Wand / focus rod | Frost Lancer (canonical water + wand) |
| control | ranged | WIS-dom | Caster staff | Tide-Sage control |
| control | ranged | STR-dom | Crossbow | Frost-Bolt control |
| support | melee | INT-dom | Twin daggers | Frost-precision support; **FLAG** |
| support | melee | WIS-dom | Battle spear / longstaff | Tide-Lancer support |
| support | melee | STR-dom | Mace / warhammer | Tide-Smiter support; **FLAG** |
| support | medium | INT-dom | Orb / sphere | Tide-Aura support |
| support | medium | WIS-dom | Censer / thurible | Tide-Cleric (canonical water support) |
| support | medium | STR-dom | War-trumpet / horn | Tide-Trumpet; **FLAG** |
| support | ranged | INT-dom | Wand / focus rod | Frost Lancer support |
| support | ranged | WIS-dom | Caster staff | Tide-Sage support |
| support | ranged | STR-dom | Crossbow | Frost-Bolt support; **FLAG** |
| hybrid | melee | INT-dom | Twin daggers | Frost-precision hybrid |
| hybrid | melee | WIS-dom | Battle spear / longstaff | Tide-Lancer hybrid |
| hybrid | melee | STR-dom | Greatsword | Frost-Knight hybrid; **FLAG** |
| hybrid | medium | INT-dom | Orb / sphere | Tide-Elementalist hybrid |
| hybrid | medium | WIS-dom | Censer / thurible | Tide-Cleric hybrid |
| hybrid | medium | STR-dom | Battle spear / longstaff | Tide-Lancer hybrid STR |
| hybrid | ranged | INT-dom | Wand / focus rod | Frost Lancer hybrid |
| hybrid | ranged | WIS-dom | Caster staff | Tide-Sage hybrid |
| hybrid | ranged | STR-dom | Crossbow | Frost-Bolt hybrid |

### 4.3 Earth (WIS-natural; mass / binding / weight stance)

36 combinations.

| role | range | stat_dist | → archetype | Notes |
|---|---|---|---|---|
| damage | melee | INT-dom | Battle spear / longstaff | Stone-Lancer INT-cross |
| damage | melee | WIS-dom | Mace / warhammer | Crag-Crusher (canonical earth + WIS + melee) |
| damage | melee | STR-dom | Mace / warhammer | Crag-Crusher STR-variant; canonical Stone-Smiter |
| damage | medium | INT-dom | Orb / sphere | Stone Witch (canonical-cross earth + orb) |
| damage | medium | WIS-dom | Battle spear / longstaff | Stone-Lancer (canonical earth + spear + WIS) |
| damage | medium | STR-dom | Battle spear / longstaff | Stone-Lancer STR-variant |
| damage | ranged | INT-dom | Caster staff | Stone Sage INT-cross |
| damage | ranged | WIS-dom | Caster staff | Stone Sage (canonical earth + ranged + WIS) |
| damage | ranged | STR-dom | Crossbow | Stone-Bolt; **FLAG sim-viability** |
| control | melee | INT-dom | Battle spear / longstaff | Stone-Lancer-Control INT |
| control | melee | WIS-dom | Mace / warhammer | Stoneshackle Inquisitor (canonical earth + binding-control + melee + WIS) |
| control | melee | STR-dom | Mace / warhammer | Stoneshackle STR-variant |
| control | medium | INT-dom | Battle spear / longstaff | Stone-Lancer-Control INT |
| control | medium | WIS-dom | Censer / thurible | Crag-Inquisitor (canonical earth + ritual binding) |
| control | medium | STR-dom | Battle spear / longstaff | Stone-Lancer-Control STR |
| control | ranged | INT-dom | Caster staff | Stone Sage-Control INT |
| control | ranged | WIS-dom | Caster staff | Stone Sage-Control (canonical) |
| control | ranged | STR-dom | Crossbow | Stone-Bolt-Control; **FLAG** |
| support | melee | INT-dom | Battle spear / longstaff | Stone-Lancer support |
| support | melee | WIS-dom | Mace / warhammer | Stoneshackle support |
| support | melee | STR-dom | Mace / warhammer | Stoneshackle STR support |
| support | medium | INT-dom | Censer / thurible | Crag-Cleric INT-cross |
| support | medium | WIS-dom | Censer / thurible | Crag-Cleric (canonical earth + ritual support) |
| support | medium | STR-dom | War-trumpet / horn | Quake-Caller (canonical earth + horn + STR) |
| support | ranged | INT-dom | Caster staff | Stone Sage support INT |
| support | ranged | WIS-dom | Caster staff | Stone Sage support |
| support | ranged | STR-dom | Crossbow | Stone-Bolt support; **FLAG** |
| hybrid | melee | INT-dom | Battle spear / longstaff | Stone-Lancer hybrid INT |
| hybrid | melee | WIS-dom | Mace / warhammer | Crag-Crusher hybrid |
| hybrid | melee | STR-dom | Mace / warhammer | Crag-Crusher hybrid STR |
| hybrid | medium | INT-dom | Battle spear / longstaff | Stone-Lancer hybrid INT |
| hybrid | medium | WIS-dom | Censer / thurible | Crag-Inquisitor hybrid |
| hybrid | medium | STR-dom | Battle spear / longstaff | Stone-Lancer hybrid STR |
| hybrid | ranged | INT-dom | Caster staff | Stone Sage hybrid INT |
| hybrid | ranged | WIS-dom | Caster staff | Stone Sage hybrid |
| hybrid | ranged | STR-dom | Crossbow | Stone-Bolt hybrid; **FLAG** |

### 4.4 Wind (WIS-natural; momentum / precision / mobility stance)

36 combinations.

| role | range | stat_dist | → archetype | Notes |
|---|---|---|---|---|
| damage | melee | INT-dom | Twin daggers | Wind Dancer INT-cross |
| damage | melee | WIS-dom | Twin daggers | Wind Dancer (canonical wind + dagger + WIS) |
| damage | melee | STR-dom | Battle spear / longstaff | Wind-Lancer STR |
| damage | medium | INT-dom | Throwing knives / chakram | Wind-Chakram |
| damage | medium | WIS-dom | Throwing knives / chakram | Ring-Dancer (canonical wind + chakram + WIS) |
| damage | medium | STR-dom | Battle spear / longstaff | Wind-Lancer STR |
| damage | ranged | INT-dom | Longbow | Wind Sentinel INT-cross |
| damage | ranged | WIS-dom | Longbow | Sky-Hunter (canonical wind + longbow + WIS) |
| damage | ranged | STR-dom | Longbow | Wind Hunter STR-cross |
| control | melee | INT-dom | Twin daggers | Wind Dancer-Control INT |
| control | melee | WIS-dom | Battle spear / longstaff | Wind-Lancer-Control |
| control | melee | STR-dom | Battle spear / longstaff | Wind-Lancer-Control STR |
| control | medium | INT-dom | Throwing knives / chakram | Wind-Chakram control |
| control | medium | WIS-dom | Throwing knives / chakram | Ring-Dancer control |
| control | medium | STR-dom | Battle spear / longstaff | Wind-Lancer control |
| control | ranged | INT-dom | Wand / focus rod | Wind-Wand control INT-cross |
| control | ranged | WIS-dom | Longbow | Wind Sentinel control |
| control | ranged | STR-dom | Longbow | Wind Hunter control STR |
| support | melee | INT-dom | Twin daggers | Wind Dancer support INT; **FLAG** |
| support | melee | WIS-dom | Battle spear / longstaff | Wind-Lancer support |
| support | melee | STR-dom | Battle spear / longstaff | Wind-Lancer support STR |
| support | medium | INT-dom | Throwing knives / chakram | Wind-Chakram support |
| support | medium | WIS-dom | War-trumpet / horn | War-Evangelist (canonical wind + horn + support; per BDI § 4.2) |
| support | medium | STR-dom | War-trumpet / horn | War-Evangelist STR-variant |
| support | ranged | INT-dom | Longbow | Wind Sentinel support INT |
| support | ranged | WIS-dom | Longbow | Sky-Hunter support |
| support | ranged | STR-dom | Longbow | Wind Hunter support STR |
| hybrid | melee | INT-dom | Twin daggers | Wind Dancer hybrid INT |
| hybrid | melee | WIS-dom | Twin daggers | Wind Dancer hybrid |
| hybrid | melee | STR-dom | Battle spear / longstaff | Wind-Lancer hybrid |
| hybrid | medium | INT-dom | Throwing knives / chakram | Wind-Chakram hybrid |
| hybrid | medium | WIS-dom | Throwing knives / chakram | Ring-Dancer hybrid |
| hybrid | medium | STR-dom | Battle spear / longstaff | Wind-Lancer hybrid STR |
| hybrid | ranged | INT-dom | Longbow | Wind Sentinel hybrid |
| hybrid | ranged | WIS-dom | Longbow | Sky-Hunter hybrid |
| hybrid | ranged | STR-dom | Longbow | Wind Hunter hybrid STR |

### 4.5 Lightning (INT-natural; speed / chain / branching stance)

36 combinations.

| role | range | stat_dist | → archetype | Notes |
|---|---|---|---|---|
| damage | melee | INT-dom | Twin daggers | Voltaic-Assassin (lightning + dagger + INT speed) |
| damage | melee | WIS-dom | Battle spear / longstaff | Lightning Lancer WIS-cross |
| damage | melee | STR-dom | Greatsword | Storm-Knight; **FLAG sim-viability** |
| damage | medium | INT-dom | Throwing knives / chakram | Storm-Chakram (canonical chain potential) |
| damage | medium | WIS-dom | Battle spear / longstaff | Lightning Lancer |
| damage | medium | STR-dom | Throwing knives / chakram | Storm-Chakram STR |
| damage | ranged | INT-dom | Caster staff | Stormking (canonical lightning + staff + INT archmage) |
| damage | ranged | WIS-dom | Caster staff | Stormking WIS-cross |
| damage | ranged | STR-dom | Crossbow | Storm-Bolt; **FLAG** |
| control | melee | INT-dom | Twin daggers | Voltaic-Assassin-Control |
| control | melee | WIS-dom | Battle spear / longstaff | Lightning Lancer-Control |
| control | melee | STR-dom | Battle spear / longstaff | Lightning Lancer-Control STR |
| control | medium | INT-dom | Throwing knives / chakram | Storm-Chakram-Control |
| control | medium | WIS-dom | Battle spear / longstaff | Lightning Lancer-Control |
| control | medium | STR-dom | Throwing knives / chakram | Storm-Chakram-Control STR |
| control | ranged | INT-dom | Wand / focus rod | Stormcaller (canonical lightning + wand + INT precision) |
| control | ranged | WIS-dom | Wand / focus rod | Stormcaller WIS-cross |
| control | ranged | STR-dom | Crossbow | Storm-Bolt-Control; **FLAG** |
| support | melee | INT-dom | Twin daggers | Voltaic-Assassin support; **FLAG** |
| support | melee | WIS-dom | Battle spear / longstaff | Lightning Lancer support |
| support | melee | STR-dom | Battle spear / longstaff | Lightning Lancer support STR |
| support | medium | INT-dom | Throwing knives / chakram | Storm-Chakram support |
| support | medium | WIS-dom | War-trumpet / horn | Storm-Trumpet; **FLAG sim-viability** |
| support | medium | STR-dom | War-trumpet / horn | Storm-Trumpet STR; **FLAG** |
| support | ranged | INT-dom | Caster staff | Stormking support |
| support | ranged | WIS-dom | Caster staff | Stormking WIS-cross support |
| support | ranged | STR-dom | Crossbow | Storm-Bolt support; **FLAG** |
| hybrid | melee | INT-dom | Twin daggers | Voltaic-Assassin hybrid |
| hybrid | melee | WIS-dom | Battle spear / longstaff | Lightning Lancer hybrid |
| hybrid | melee | STR-dom | Greatsword | Storm-Knight hybrid; **FLAG** |
| hybrid | medium | INT-dom | Throwing knives / chakram | Storm-Chakram hybrid |
| hybrid | medium | WIS-dom | Battle spear / longstaff | Lightning Lancer hybrid |
| hybrid | medium | STR-dom | Throwing knives / chakram | Storm-Chakram hybrid STR |
| hybrid | ranged | INT-dom | Caster staff | Stormking hybrid |
| hybrid | ranged | WIS-dom | Caster staff | Stormking hybrid WIS |
| hybrid | ranged | STR-dom | Crossbow | Storm-Bolt hybrid; **FLAG** |

### 4.6 Holy (WIS-natural; judgment / blessing / sustain stance)

36 combinations.

| role | range | stat_dist | → archetype | Notes |
|---|---|---|---|---|
| damage | melee | INT-dom | Mace / warhammer | Templar-Smiter INT-cross |
| damage | melee | WIS-dom | Mace / warhammer | Templar-Smiter (canonical holy + WIS + melee) |
| damage | melee | STR-dom | Mace / warhammer | Smiter STR (canonical D2 Smiter-Pala) |
| damage | medium | INT-dom | Holy symbol / icon | Judgment-Bringer INT-cross |
| damage | medium | WIS-dom | Holy symbol / icon | Exorcist (canonical holy + symbol + WIS) |
| damage | medium | STR-dom | Mace / warhammer | Smiter medium STR |
| damage | ranged | INT-dom | Crossbow | Inquisitor-Marksman INT-cross |
| damage | ranged | WIS-dom | Crossbow | Inquisitor-Marksman (canonical holy + crossbow + WIS) |
| damage | ranged | STR-dom | Blunderbuss / scattergun | Holy Pirate Sniper / Powder Inquisitor (canonical surprising-pair per BDI § 5.1); **FLAG sim-viability** |
| control | melee | INT-dom | Mace / warhammer | Templar-Smiter-Control INT |
| control | melee | WIS-dom | Mace / warhammer | Templar-Smiter-Control |
| control | melee | STR-dom | Mace / warhammer | Smiter-Control STR |
| control | medium | INT-dom | Censer / thurible | Aegis-Inquisitor INT-cross |
| control | medium | WIS-dom | Censer / thurible | Aegis-Priest-Control (canonical holy + censer + control via aura-binding) |
| control | medium | STR-dom | Mace / warhammer | Smiter-Control STR; **FLAG** |
| control | ranged | INT-dom | Holy symbol / icon | Judgment-Bringer-Control INT |
| control | ranged | WIS-dom | Holy symbol / icon | Exorcist-Control |
| control | ranged | STR-dom | Crossbow | Inquisitor-Marksman-Control STR |
| support | melee | INT-dom | Mace / warhammer | Templar-Smiter support INT |
| support | melee | WIS-dom | Mace / warhammer | Templar-Smiter support |
| support | melee | STR-dom | Mace / warhammer | Templar-Smiter support STR |
| support | medium | INT-dom | Censer / thurible | Aegis-Inquisitor support INT |
| support | medium | WIS-dom | Censer / thurible | Aegis-Priest (canonical holy + censer + support via aura) |
| support | medium | STR-dom | War-trumpet / horn | War-Priest / Trumpet-Saint (canonical holy + horn + support) |
| support | ranged | INT-dom | Tome / grimoire | Pact-Cleric INT-cross |
| support | ranged | WIS-dom | Tome / grimoire | Pact-Cleric (canonical holy + summoner-scholar + WIS) |
| support | ranged | STR-dom | Crossbow | Inquisitor-Marksman support STR |
| hybrid | melee | INT-dom | Mace / warhammer | Templar-Smiter hybrid INT |
| hybrid | melee | WIS-dom | Mace / warhammer | Templar-Smiter hybrid |
| hybrid | melee | STR-dom | Mace / warhammer | Smiter hybrid STR |
| hybrid | medium | INT-dom | Holy symbol / icon | Exorcist hybrid INT |
| hybrid | medium | WIS-dom | Holy symbol / icon | Exorcist hybrid |
| hybrid | medium | STR-dom | Mace / warhammer | Smiter hybrid STR |
| hybrid | ranged | INT-dom | Crossbow | Inquisitor-Marksman hybrid INT |
| hybrid | ranged | WIS-dom | Crossbow | Inquisitor-Marksman hybrid |
| hybrid | ranged | STR-dom | Blunderbuss / scattergun | Holy Pirate Sniper hybrid STR; **FLAG sim-viability** |

### 4.7 Shadow (INT-natural; trade-off / drain / ambush stance)

36 combinations.

| role | range | stat_dist | → archetype | Notes |
|---|---|---|---|---|
| damage | melee | INT-dom | Twin daggers | Shadow Strider (canonical shadow + dagger + INT) |
| damage | melee | WIS-dom | Twin daggers | Shadow Strider WIS-cross |
| damage | melee | STR-dom | Twin daggers | Cutpurse-Shadow STR |
| damage | medium | INT-dom | Throwing knives / chakram | Nightblade (canonical shadow + multi-projectile + INT) |
| damage | medium | WIS-dom | Throwing knives / chakram | Nightblade WIS-cross |
| damage | medium | STR-dom | Throwing knives / chakram | Nightblade STR-cross |
| damage | ranged | INT-dom | Wand / focus rod | Voidpiercer (canonical shadow + wand + INT) |
| damage | ranged | WIS-dom | Wand / focus rod | Voidpiercer WIS-cross |
| damage | ranged | STR-dom | Crossbow | Shadow-Bolt Hunter STR |
| control | melee | INT-dom | Twin daggers | Shadow Strider-Control |
| control | melee | WIS-dom | Twin daggers | Shadow Strider-Control WIS |
| control | melee | STR-dom | Twin daggers | Cutpurse-Shadow-Control |
| control | medium | INT-dom | Throwing knives / chakram | Nightblade-Control |
| control | medium | WIS-dom | Throwing knives / chakram | Nightblade-Control WIS |
| control | medium | STR-dom | Throwing knives / chakram | Nightblade-Control STR |
| control | ranged | INT-dom | Wand / focus rod | Voidpiercer-Control |
| control | ranged | WIS-dom | Wand / focus rod | Voidpiercer-Control WIS |
| control | ranged | STR-dom | Crossbow | Shadow-Bolt-Control STR |
| support | melee | INT-dom | Twin daggers | Shadow Strider support INT |
| support | melee | WIS-dom | Twin daggers | Shadow Strider support WIS |
| support | melee | STR-dom | Twin daggers | Cutpurse-Shadow support STR |
| support | medium | INT-dom | Censer / thurible | Smoke-Vampire (canonical shadow + censer + drain-sustain per BDI § 5.1) |
| support | medium | WIS-dom | Censer / thurible | Smoke-Cleric (canonical shadow + censer + WIS-aura) |
| support | medium | STR-dom | Throwing knives / chakram | Nightblade support STR |
| support | ranged | INT-dom | Tome / grimoire | Necromancer (canonical shadow + tome + INT summoner) |
| support | ranged | WIS-dom | Tome / grimoire | Necromancer WIS-cross |
| support | ranged | STR-dom | Crossbow | Shadow-Bolt support STR |
| hybrid | melee | INT-dom | Twin daggers | Shadow Strider hybrid |
| hybrid | melee | WIS-dom | Twin daggers | Shadow Strider hybrid WIS |
| hybrid | melee | STR-dom | Twin daggers | Cutpurse-Shadow hybrid STR |
| hybrid | medium | INT-dom | Throwing knives / chakram | Nightblade hybrid |
| hybrid | medium | WIS-dom | Throwing knives / chakram | Nightblade hybrid WIS |
| hybrid | medium | STR-dom | Throwing knives / chakram | Nightblade hybrid STR |
| hybrid | ranged | INT-dom | Wand / focus rod | Voidpiercer hybrid |
| hybrid | ranged | WIS-dom | Tome / grimoire | Necromancer hybrid WIS |
| hybrid | ranged | STR-dom | Crossbow | Shadow-Bolt hybrid STR |

---

## 5. Coverage verification

**Vector-space coverage:** 7 elements × 4 roles × 3 ranges × 3 stat_dists = **252 combinations**. Each combination is mapped to exactly one archetype OR `no_signature` (no `no_signature` in v1; the 252 are exhaustively covered).

**Archetype-coverage check (every archetype must produce ≥1 substrate-vector mapping):**

| # | Archetype | Coverage count | Sample assignment |
|---|---|---|---|
| 1 | Greatsword | 9 | fire/water/lightning melee combos |
| 2 | Twin daggers | 30 | shadow/wind/water/fire/lightning multi-role |
| 3 | Battle spear / longstaff | 36 | earth/wind/lightning/fire/water multi-role |
| 4 | Mace / warhammer | 22 | physical/earth/holy/fire melee + control |
| 5 | Longbow | 18 | wind/water/lightning ranged damage/control/support/hybrid |
| 6 | Crossbow | 23 | physical/holy/earth/fire ranged + cross-attribute |
| 7 | Blunderbuss / scattergun | 4 | fire/holy ranged + STR-cross |
| 8 | Throwing knives / chakram | 35 | shadow/wind/lightning/fire medium multi-role |
| 9 | Wand / focus rod | 11 | lightning/water/shadow ranged-medium |
| 10 | Orb / sphere | 9 | fire/water medium damage/control/support/hybrid |
| 11 | Caster staff | 26 | fire/lightning/earth/water ranged multi-role |
| 12 | Tome / grimoire | 7 | shadow/holy ranged summoner-scholar |
| 13 | Censer / thurible | 16 | holy/shadow/water/fire/earth medium ritual |
| 14 | Holy symbol / icon | 7 | holy medium-ranged smite-judgment |
| 15 | War-trumpet / horn | 9 | holy/wind/earth/lightning/fire medium support |

Total: **262** (some combinations map to the same archetype across role variations; expected). All 15 archetypes have ≥4 mappings; coverage requirement satisfied.

---

## 6. Sim-viability flags — for rocket verification

The following entries are flagged for explicit sim-viability verification before W1.15-LITE locks. Most are cross-attribute or surprising-but-evocative combinations.

| Element | role | range | stat_dist | Archetype | Reason for flag |
|---|---|---|---|---|---|
| fire | damage | melee | INT-dom | Greatsword | INT-melee uncommon; need to verify spell-warrior sim viability |
| fire | damage | medium | STR-dom | Throwing knives / chakram | Powder Pyromaniac unconventional |
| fire | damage | ranged | STR-dom | Blunderbuss / scattergun | Powder Pyromaniac unconventional |
| fire | control | ranged | STR-dom | Crossbow | Fire-Bolt cross-attribute |
| fire | support | melee | INT-dom | Twin daggers | Fire-precision support cross-stance |
| fire | support | melee | WIS-dom | Mace / warhammer | Fire-Cleric cross-element |
| fire | support | melee | STR-dom | Greatsword | Fire-Knight support cross-role |
| fire | support | medium | STR-dom | War-trumpet / horn | Fire-Trumpet cross-archetype |
| fire | support | ranged | STR-dom | Crossbow | Fire-Bolt support cross-attribute |
| fire | hybrid | ranged | STR-dom | Crossbow | Fire-Bolt hybrid cross |
| water | damage | melee | STR-dom | Greatsword | Frost-Knight cross-attribute |
| water | damage | medium | STR-dom | Throwing knives / chakram | Frost-Chakram cross-stance |
| water | control | melee | STR-dom | Mace / warhammer | Frost-Hammer cross-attribute |
| water | support | melee | INT-dom | Twin daggers | Frost-precision support cross-role |
| water | support | melee | STR-dom | Mace / warhammer | Tide-Smiter cross-attribute |
| water | support | medium | STR-dom | War-trumpet / horn | Tide-Trumpet cross-archetype |
| water | support | ranged | STR-dom | Crossbow | Frost-Bolt support cross |
| water | hybrid | melee | STR-dom | Greatsword | Frost-Knight hybrid cross |
| earth | damage | ranged | STR-dom | Crossbow | Stone-Bolt cross-stance |
| earth | control | ranged | STR-dom | Crossbow | Stone-Bolt-Control cross |
| earth | support | ranged | STR-dom | Crossbow | Stone-Bolt support cross |
| earth | hybrid | ranged | STR-dom | Crossbow | Stone-Bolt hybrid cross |
| wind | support | melee | INT-dom | Twin daggers | Wind Dancer support INT cross-role |
| lightning | damage | melee | STR-dom | Greatsword | Storm-Knight INT-melee cross |
| lightning | damage | ranged | STR-dom | Crossbow | Storm-Bolt cross-attribute |
| lightning | control | ranged | STR-dom | Crossbow | Storm-Bolt-Control cross |
| lightning | support | melee | INT-dom | Twin daggers | Voltaic-Assassin support INT cross-role |
| lightning | support | medium | WIS-dom | War-trumpet / horn | Storm-Trumpet WIS-cross |
| lightning | support | medium | STR-dom | War-trumpet / horn | Storm-Trumpet STR-cross |
| lightning | support | ranged | STR-dom | Crossbow | Storm-Bolt support cross |
| lightning | hybrid | melee | STR-dom | Greatsword | Storm-Knight hybrid cross |
| lightning | hybrid | ranged | STR-dom | Crossbow | Storm-Bolt hybrid cross |
| holy | damage | ranged | STR-dom | Blunderbuss / scattergun | Holy Pirate Sniper (BDI § 5.1 canonical surprising-pair) |
| holy | control | medium | STR-dom | Mace / warhammer | Smiter-Control STR support questionable |
| holy | hybrid | ranged | STR-dom | Blunderbuss / scattergun | Holy Pirate Sniper hybrid |

**Total flagged combinations: 36 of 252 (~14%)**. Most are STR-dominant cross-attribute entries (STR-dom with INT-natural fire/water/lightning/shadow OR with WIS-natural earth/wind/holy in ranged combos).

**Rocket sim-viability protocol per gear-as-substrate § 0.5.6:** for each flagged combination, generate a small test-suite (5-10 sample seasons) and verify the resulting class converges + simulates to viable WR. If any archetype produces sub-viable kits at the boundary, the rule table needs revision (re-route flagged combinations to alternate archetypes OR mark `no_signature` as the lock value).

---

## 7. Rule-design principles preserved (for future rule-table evolution)

These principles MUST be honored when the rule table evolves to v2 (post-W1.15-LITE empirical results + post-BDI-E gate decision):

1. **Canonical pairings privileged.** Holy+censer remains Aegis-Priest. Shadow+veil remains Nightshroud. Lightning+wand remains Stormcaller. Genre-canon takes precedence over algorithmic uniformity.

2. **Range-axis dominance as PRIMARY classifier.** Range constraints carry the most "what kind of fight is this kit having?" signal. Melee/medium/ranged are coarse-grained but identity-anchoring.

3. **Role-axis as tie-breaker within range family.** Two melee classes with different roles produce different archetypes (melee damage → greatsword/dagger; melee control → mace/spear).

4. **Stat-dist alignment as fine-tuning.** Within a (range, role) family, stat_dist alignment with archetype's natural-attribute family makes the final pick.

5. **Cross-attribute fallback to genre-tolerant archetypes.** Cross-attribute combinations (e.g., fire + STR-dom) route to archetypes that the genre has shown to tolerate cross-stat pressure (greatsword tolerates fire-INT-cross via "Inferno-Knight" precedent; crossbow tolerates lightning-STR-cross via "mercenary-marksman" pattern).

6. **Surprising-but-evocative allowed where canon supports.** Holy+blunderbuss = Holy Pirate Sniper is the per-dispatch canonical example. This is not "anything goes" — the surprise must trace to a genre-recognizable identity (BDI § 5.1 rank-3 examples include Powder Hex-Cannon as the rank-3 of this exact pair-stack).

7. **`no_signature` as fallback for genuinely incoherent vectors.** v1 has no `no_signature` entries — the 252 vectors are exhaustively covered. v2 may introduce `no_signature` for combinations sim-viability empirically rejects.

8. **BDI ω-alignment.** When in doubt between two archetypes for a vector, prefer the archetype with higher ω in the BDI table (per `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`). The BDI ω-field is the design's quantitative articulation of "what feels canonical"; the rule table should converge on ω-favored picks.

---

## 8. Cross-references

- `canonical/story/historical/gear-as-substrate-2026-05-21.md` § 0.5.6 (LITE path) + § 3 (15-archetype catalogue)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — ω/τ context for rule-design decisions
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` ELEMENT_SCALING_ATTRIBUTE — canonical INT/WIS/STR assignment
- `canonical/story/historical/build-defining-resonance-formula-2026-05-21.md` § 4 (ω/τ context) + § 5.1 (rank-3 identity examples)
- `canonical/story/substrate-design-supplement-2026-05-21.md` — per-element identity stance definitions
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 6.2.2 W1.15-LITE workstream
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` Axis 1 (range component definitions)
- `canonical/story/project_role_orientation_taxonomy.md` (role definitions)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` — Tier 4 architecture (signature gear-anchored capstone informed by this rule table)

---

## 9. Open questions for empirical refinement (v2 reordering)

1. **Sim-viability rejection rate.** What % of the 36 flagged combinations rocket sim-viability-rejects determines whether v1 holds as-is or requires substantial revision. If rejection > 25%, the cross-attribute branches need redesign.
2. **`no_signature` introduction.** Some combinations may need to map to `no_signature` rather than a forced archetype assignment (e.g., support+melee+INT-dom for an element that has no canonical melee-INT-support identity). Empirical sim-viability + cohesion-judge identity-recognition outcomes will guide this.
3. **Archetype-coverage imbalance.** Some archetypes get few mappings (Blunderbuss: 4; Tome: 7; Holy symbol: 7) compared to others (Battle spear: 36; Twin daggers: 30). If the imbalance produces underrepresentation in archive, the rule table may bias intentionally toward less-mapped archetypes via stat_dist or role tie-breakers.
4. **Cross-element archetype reuse.** Some archetypes are heavily reused across elements (Battle spear: 36 entries; Mace: 22). Whether this is "good — earth-spear and wind-spear are distinct identities" or "bad — same archetype-vector across elements" depends on cohesion-judge differentiation behavior in P5.

These open questions feed forward to v2 rule-table revision post-W1.15-LITE empirical results + BDI-E gate.

---

**Signed:** gandalf (story-and-design steward; senior designer)
**For:** v1 deterministic rule mapping 252 substrate-vectors → 15-archetype catalogue for W1.15-LITE; canonical pairings privileged + range-axis dominance + role-axis tie-breakers + stat-dist alignment + cross-attribute fallback + BDI ω-alignment all encoded; sim-viability flags identified for rocket verification before lock.
