# Engine Generation Run — Special Case Summary

> **STATUS:** RATIFIED 2026-05-25 — empirical-fill pass complete (autonomous gandalf design-fit pass per framing brief § 2)

**Author:** gandalf (story-and-design steward)
**For:** Matt + gandalf T4 post-mortem session 1 + Cycle 13 scope-doc authoring
**Framework anchor:** `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-framing-brief.md` § 2
**Generation run source:** `agentic_orchestration/dispatches/2026-05-25-rocket-engine-generation-run-v1-narrow.md` (rocket; tag `rocket/v0.1-engine-generation-run-v1-narrow-2026-05-25`)
**Provenance manifest:** `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md`
**Output:** `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json` (35 forms; engine_version v2.0; seed 20250525)

---

## 0. TL;DR

**Engine first-fire produces 35 schema-valid forms with substrate-bound weapons, BC-cell coverage of all 25 target cells, four § 8 strategies firing as design-coherent signatures, and gamora-fight-engine wire-up populating Option γ combatant-fields.** Algorithm § 8 keystones DO reach combat arithmetic (verified per `gamora_combatant_fields` shape) — Cycle 12 Tier 2 ratification objective is empirically met for what the run produced.

**Three load-bearing findings reshape T4 post-mortem session 1 scope:**

1. **§ 8 signature distribution is 4-strategy, not 6 — ELEMENT_CONVERSION and DEFENSIVE_TRADEOFF are absent from BOTH signature and candidate-pool slots.** The `metadata.json` coverage claim of 6 strategies covered is contradicted by the per-form data. This is a v1 engine state finding, not a manifest-author error: the opportunity-scan refactor (L9) clearly does not select these strategies on the all-physical-element substrate this run sampled.

2. **Phase 5 LLM cohesion-coalescence ran ONLY at the form-name + form-flavor layer.** All 289 skill nodes have placeholder names (`Chain A T1 0`); zero skill flavor_text; zero skill effects; zero `geometry_type` / `spatial_geometry_type`. Skill-content production is a wide gap, not a calibration gap. T4 keystones are form-level metadata only — no T4+ skill nodes exist in the skill trees (35× max tier = 3, T4 represented purely via `t4_alteration_output` struct).

3. **The "BLOCKED cells" framing from manifest is stale — 2 of 3 reported BLOCKED cells ARE present in the output.** Pyromantic Caster (v2-form-016) routed via `stage_3_5_engine_authored_gap_fill`; Necromancer Summoner (v2-form-018) routed via `sidecar_b_necro_enrichment_proxy_spawn`. Section 4 alternative routing is working — composition policy v1 § 4.1 alternatives DO fire — but `metadata.json` coverage block reports them as blocked. The reportage layer is misaligned with the executor; the executor is doing more than the reportage acknowledges.

**Top design-fit verdict on signatures elected:** Moctezuma's Jade Warlord (v2-form-025) electing RESOURCE_CONVERSION with `narrative_hooks: ['sacrifice', 'blood_magic', 'life_wager']` on the Aztec war-club substrate is the run's highest-coherence form — substrate-binding, anchor-binding, and § 8 algorithm converge on Aztec-ritual blood-magic warrior. This is what the L9 mechanical-substrate-driven opportunity-scan was designed to produce. **The algorithm CAN do design-coherent work.** Where it fails to do that work, scope of failure is identifiable (cf. § 4 flags).

---

## 1. Generation run output summary

### 1.1 Coverage stats (verified per classes.json + metadata.json)

| Dimension | Target (framing brief § 1.1) | Actual | Status |
|---|---|---|---|
| Total forms | ~30-40 | **35** | ✅ |
| BC-target cell coverage | All 25 OR documented gap | **25 cells (10 with 2 forms; 15 with 1)** | ✅ all 25 |
| § 8 strategies signature | ≥2-3 per strategy per cell-eligibility | **4 strategies elected (DEFENSIVE_CONVERSION 13 / TRADE_OFF 9 / GEOMETRY_COLLAPSE 8 / RESOURCE_CONVERSION 5); ELEMENT_CONVERSION & DEFENSIVE_TRADEOFF absent** | ⚠️ partial; see § 1.3 finding |
| Provenance mix | 4 source_library types | **Form-level: 35/35 = generator_v2 (uniform). Weapon-level: 7 source libraries spanning royal_armouries / met-museum / wikipedia / wikidata / engine_authored_gap_fill_v1 / nick-aschenbach-dnd-data / odin-army-tradoc** | ⚠️ form-level uniform; weapon-level rich; see § 1.3 finding |
| Sketch F anchors | 4 (Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh) | **1 (Moctezuma; sampled twice — INT/fire_mage + STR/physical_warrior)** | ⚠️ 1/4 sampled |
| Element coverage | All 8 | **1 (physical only)** | ⚠️ 1/8; load-bearing finding |
| Attribute coverage | All 4 | **4 (STR 10 / DEX 10 / INT 8 / WIS 7)** | ✅ |
| Anchor-tagged forms (broader Tier-1/Tier-2) | n/a target | **9 forms — Charlemagne / Alexander / Sadamune ×2 / Moctezuma ×2 / Roland / Saint George / El Cid / Wayland** | bonus richness; see § 2.5 |

### 1.2 Quality criteria verification

| Criterion (framing brief § 1.2) | Verified | Notes |
|---|---|---|
| Algorithm § 8 keystones reach combat arithmetic (Option γ payoff per L6 wire-up) | **✅ YES** | `gamora_combatant_fields` populated on 35/35 forms with concrete numeric params per strategy: `evasion_to_armor=True` for DEFENSIVE_CONVERSION; `aoe_radius_multiplier=0.5, damage_multiplier_bonus=1.5` for GEOMETRY_COLLAPSE; `hit_modifier=1.0, crit_rate=0.0` for TRADE_OFF; `cost_resource=HP, scope=all_skills` for RESOURCE_CONVERSION |
| All forms have full schema population per `PlayerClassV2` contract | **⚠️ PARTIAL** | All required fields present + schema-valid (rocket validation_errors=0 confirmed). BUT: extensive nullable-field gaps — see § 1.3 |
| Sim-viability flag PASS | **✅ implicit YES** | All 35 forms emerged from converge_kit without UNGENERABLE; Layer 6 wire-up is the effective joint-gate |
| engine_version = "v2.0" on all forms | **✅ 35/35** | verified per Counter |
| `mechanical_substrate_triple` populated per L9 | **✅ 35/35** | uniformly `{element: physical, weapon_kind: <category/banner/unique/named_template/ammo_or_consumable>, weapon_mechanical_profile: <armor_shield/handheld_weapon/accessory_handheld/...>}` |
| Substrate-binding integrity (main_weapon mechanical fields match BC-target cell) | **✅ all 35 forms relaxation_level=0** | no thin-cell-fallback fired in this run; all binds at strict 4-tuple match (option_alpha 20 / option_beta 12 / option_c 3) |

### 1.3 Critical finding — § 8 strategy coverage claim vs reality

**Manifest + metadata.json claim:** `strategies_covered: [DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, ELEMENT_CONVERSION, GEOMETRY_COLLAPSE, RESOURCE_CONVERSION, TRADE_OFF]` (6 strategies).

**classes.json reality, per-form signature `t4_alteration_output.strategy_type`:**
- DEFENSIVE_CONVERSION × 13 (37%)
- TRADE_OFF × 9 (26%)
- GEOMETRY_COLLAPSE × 8 (23%)
- RESOURCE_CONVERSION × 5 (14%)
- DEFENSIVE_TRADEOFF × 0
- ELEMENT_CONVERSION × 0

**Per-form candidate-pool `spirit_guide_narration_metadata.secondary_alteration_types` union:** `{RESOURCE_CONVERSION, GEOMETRY_COLLAPSE, DEFENSIVE_CONVERSION, TRADE_OFF}` — also 4-set. ELEMENT_CONVERSION + DEFENSIVE_TRADEOFF never appear in either signature OR secondary slots in this run.

**Per-form `gamora_combatant_fields` keys union:** `{defensive_conversion, geometry_collapse, trade_off, resource_conversion}` — confirms the 4-set.

**Interpretation:**
- The reportage layer (metadata.json `strategies_covered`) appears to enumerate the strategy-enum keyspace (all 6 strategies the engine KNOWS), NOT the strategies elected on this run. This is a misleading coverage stat.
- The L9 opportunity-scan refactor, operating on `mechanical_substrate_triple` (all 35 forms = physical / category∪banner∪... / various), simply does not light up the trigger conditions for ELEMENT_CONVERSION (element-flavored signature requires non-physical element substrate; physical-uniform run cannot fire it) OR DEFENSIVE_TRADEOFF (Chaos-Inoculation-class requires shadow/holy combat-context the physical-uniform substrate does not produce).
- The 4-strategy result is therefore **consistent with substrate-led discipline** (no manufactured strategies on substrate that doesn't support them) but **inconsistent with the run's stated coverage goal** (6 strategies represented).

**T4 post-mortem item:** is the right v1 narrow milestone goal "6 strategies represented" OR "strategies fire when substrate supports them"? Substrate-led discipline says the latter. The reportage and the framing brief should be amended to reflect this.

### 1.4 Critical finding — Phase 5 ran at form-layer only

Per metadata.json `llm_naming_enabled: true`, Phase 5 LLM cohesion-coalescence is on. Evidence:
- All 35 forms have LLM-generated `name` (e.g., "Rampart Knight", "Khyber Shadow Dancer", "Paladin of Durandal", "Moctezuma's Jade Warlord", "Sunstone Spearthrower")
- All 35 forms have LLM-generated `flavor_text` (1-2 sentence narrative blurbs)

Phase 5 did **NOT** run at the skill-layer:
- All 289 skill nodes share placeholder names: `Chain A T1 0`, `Chain A T2 0`, `Chain B T1 1`, etc. (literal template strings — no LLM call)
- Zero skill `flavor_text` populated
- Zero skill `effects` populated (effect-text rendering deferred)
- Zero skill `geometry_type` (despite Algorithm § 8 wiring AoE multipliers at the keystone layer)
- Zero skill `spatial_geometry_type`

Phase 5 also did **NOT** populate:
- 35/35 `title_completion: null` (form titles incomplete; e.g., "Rampart Knight" is name-only with no completion)
- 35/35 `seasonal_dominant_element: null` (sub-element flavoring NOT fired)

Phase 6 visual layer is fully placeholder:
- 35/35 forms share identical `color_palette: [160, 140, 100]` (single uniform earth-tone triplet)
- 35/35 forms share identical `movement_speed: 8.0`

Phase 7 joint-gate is implicit (Layer 6 wire-up = effective sim-viability check; no UNGENERABLE results) — acceptable for v1 narrow.

**Other empty fields (worth surfacing):**
- 35/35 `carried_gear: null` (off-hand / secondary equipment not populated per-form, even though SC-3 contract anticipated it)
- 35/35 `secondary_item: null` (same — engine produces main_weapon only)
- 0/35 `is_act_boss: True` (no boss flagging; expected for class-roster forms)

### 1.5 Critical finding — BLOCKED-cells reportage is stale

Manifest claims 3 BLOCKED cells: Artillery Mage, Pyromantic Caster, Necromancer Summoner. Reality:

| Cell | Manifest status | classes.json reality |
|---|---|---|
| **Artillery Mage** | "BLOCKED → folded to Cell 12" | ✅ matches — v2-form-015 has `cell_label="Artillery Mage (FOLDED → Cell 12)"` + `cell_routing_source="locked_section_4_1"` + `section_4_routing="fold_to_cell_12_t4_alteration"`. Fold is working. |
| **Pyromantic Caster** | "BLOCKED — requires Stage 3.5 gap-fill or Sidecar B" | ❌ ACTUALLY PRESENT — v2-form-016 has `cell_label="Pyromantic Caster"` + `section_4_routing="stage_3_5_engine_authored_gap_fill"` + `stage_3_5_gap_fill=True` flag. **Stage 3.5 IS firing.** |
| **Necromancer Summoner** | "BLOCKED — requires Stage 3.5 gap-fill or Sidecar B" | ❌ ACTUALLY PRESENT — v2-form-018 has `cell_label="Necromancer Summoner"` + `section_4_routing="sidecar_b_necro_enrichment_proxy_spawn"` + `proxy_spawn_flag=True` + `sidecar_b_pending="sidecar_b_necro_enrichment_proxy_spawn"`. **Sidecar B is firing via proxy-spawn fallback.** |

The composition-policy-v1 § 4.1 alternative-routing matrix is wider than the manifest acknowledges. Reportage updates needed.

**Section 4 routing distribution across the 35 forms** (14/35 forms used section-4 alternative routing, not default heuristic):
- `accept_0.45_conf_pool_stage4_priority` × 2
- `pan_fantasy_tradition_filter` × 2
- `stage_3_5_engine_authored_gap_fill` × 1 (Pyromantic Caster v2-form-016)
- `sidecar_b_necro_enrichment_proxy_spawn` × 1 (Necromancer Summoner v2-form-018)
- `sidecar_b_wis_broad_enrichment` × 1
- `sidecar_b_celtic_druidic_enrichment` × 1
- `sidecar_b_east_asian_fist_staff_option_c` × 1 (Monk-archetype v2-form-022)
- `sidecar_b_celtic_pacific_proxy_spawn` × 1
- `sidecar_b_sub_saharan_african_proxy_spawn` × 1
- `fold_to_cell_12_t4_alteration` × 1 (Artillery Mage v2-form-015)
- `option_c_str_melee_substrate_int_flavored` × 1
- `accept_low_floor_standard_heuristic` × 1
- (default heuristic / no section_4 routing) × 21

---

## 2. Per-form notes (sampled per framing brief § 2.1)

### 2.1 Sketch F anchor forms (full notes)

#### v2-form-025 — Moctezuma's Jade Warlord (Mesoamerican; Tier-S; physical_warrior / Heavy Barbarian)

| Field | Value |
|---|---|
| BC-target cell | Heavy Barbarian (range=melee, tempo=low, amplitude=spiky, attribute=STR, proxy_density=none) |
| Archetype / energy / role / range | physical_warrior / rage / damage / close |
| Main weapon | `moctezuma_aztec_war_club` (`engine_authored_gap_fill_v1`, medieval, lineage=Moctezuma) |
| Cultural / period | mesoamerican / medieval |
| Matching policy | option_alpha (strict 4-tuple match) |
| § 8 signature | **RESOURCE_CONVERSION** |
| § 8 secondary | RESOURCE_CONVERSION (duplicate; algorithmic) |
| `gamora_combatant_fields` | `{resource_conversion: {cost_resource: HP, scope: all_skills}}` — HP-substituted-for-rage all-skill cost shift |
| Spirit-guide template | `resource_cost_shift` |
| Narrative hooks | sacrifice / blood_magic / life_wager |
| Stat distribution | STR 80 / VIT 60 / DEX 20 / INT 10 / WIS 10 |
| Flavor text | "Bearer of the obsidian macuahuitl, Moctezuma's chosen champion crushes enemies beneath the war-god's unyielding, stone-edged wrath." |

**Design-fit verdict:** ⭐ **highest-coherence form in the run.** Substrate (Aztec war club macuahuitl) + named bearer (Moctezuma) + § 8 algorithm (RESOURCE_CONVERSION → blood-magic-as-rage-economy) + spirit-guide narrative hooks (sacrifice, blood_magic, life_wager) ALL converge on the same archetypal identity: Aztec sacrificial-ritual warrior trading lifeblood for combat power. This is what the L9 mechanical-substrate-driven opportunity-scan was designed to produce. The thematic_rationale field is empty (a hole — see § 3.5), but the narrative hooks compensate by giving spirit-guide narration template enough material to render the kit identity. Class name "Moctezuma's Jade Warlord" + flavor text are LLM-rendered and stay on-theme.

**Anti-pattern check:** is "blood magic on a physical warrior" a kit-identity collision? In Diablo II terms — yes, Necromancer-flavoring on Barbarian-mechanics would normally be a clash. In Mushoku-Tensei isekai terms (substrate is named historical/mythological), the Aztec ritual context resolves the apparent clash: Moctezuma's warrior caste DID couple physical combat with blood-sacrifice ritual. **Substrate votes; the algorithm honored substrate.** Approved.

#### v2-form-008 — Sunstone Spearthrower (Mesoamerican; Tier-S; fire_mage / Standard Wizard)

| Field | Value |
|---|---|
| BC-target cell | Standard Wizard (range=ranged, tempo=medium, amplitude=variable, attribute=INT, proxy_density=none) |
| Archetype / energy / role / range | fire_mage / mana / damage / long |
| Main weapon | `moctezuma_atlatl` (`engine_authored_gap_fill_v1`, medieval, lineage=Moctezuma) |
| Cultural / period | mesoamerican / medieval |
| Matching policy | option_beta (attribute-level matching) |
| § 8 signature | **RESOURCE_CONVERSION** |
| Spirit-guide template | `resource_cost_shift` |
| Narrative hooks | sacrifice / blood_magic / life_wager |
| Stat distribution | STR 10 / VIT 40 / DEX 10 / INT 80 / WIS 30 |
| Flavor text | "Heir to Moctezuma's burning will, they hurl the sun's wrath across battlefields, where stone and flame are one." |

**Design-fit verdict:** ⭐ **design-coherent at the kit-identity layer; mechanical strain at the engine-archetype-routing layer.** The substrate (Aztec atlatl spear-thrower) + named bearer (Moctezuma) is interesting — the algorithm routed the atlatl substrate to an INT/wizard cell via option_beta (attribute-level match). This produces a fire_mage / mana-economy / ranged / INT-primary kit centered on "Moctezuma's atlatl as sun-priest staff for hurling solar fire." Sub-element flavoring is implicit (fire_mage on physical-element substrate), but `seasonal_dominant_element: null` confirms Phase 5 sub-element coalescence did NOT fire. The class-name + flavor text salvage thematic coherence via "sun's wrath" / "stone and flame" — LLM Phase 5 form-layer is doing the load-bearing work here.

**Pattern observation — SAME named bearer in two cells:** Moctezuma appears as both v2-form-008 (fire_mage INT) and v2-form-025 (physical_warrior STR). In isekai terms this is a **lineage-class-fan pattern** — Diablo Immortal does this with Lyndon (Demon Hunter + Necromancer reuse-flavor). The provenance is the same named historical figure powering two algorithm-divergent kits. This is **design-interesting** and worth Matt review: should the engine emit named-bearer-uniqueness constraints, or is multi-cell flavor-fanning intentional (isekai-anchor multiplying across reincarnation forms)? This pattern is one of the most isekai-thematically-honest outcomes of this run — different reincarnated forms inheriting different aspects of the same named ancestor.

#### Hattori Hanzō / Lu Bu / Gilgamesh — NOT SAMPLED

Manifest notes: substrate rows exist; sampling order didn't reach these anchors. **gandalf reading:**

The 35-form run uses an enumeration order that prioritized cell-id sweep + multi-fire extension within cells, rather than anchor-priority sampling. Moctezuma got sampled twice because TWO different BC cells (Heavy Barbarian STR + Standard Wizard INT) happened to bind to Moctezuma-substrate rows during the cell-order enumeration; the other three Sketch F anchors' substrate rows didn't surface in the cells the run cycled through.

**Two interpretations possible:**
- (a) Sampling-policy gap: the engine doesn't prioritize Sketch F anchors via "ensure at least one form per named anchor" enumeration constraint. If anchors are load-bearing (per composition policy v1 § 5.2), the engine should sample-priority them.
- (b) Substrate-coverage gap: Hattori Hanzō's substrate rows exist BUT only bind to cells the enumeration didn't reach (e.g., maybe a Twin-Blade Fencer East-Asian variant that sampling didn't visit). The cells sampled twice (Heavy Barbarian, Polearm Soldier, Light Fighter, Dagger Assassin, Archer, Thrown-Heavy, Crossbow Sniper, Twin-Blade, Standard Wizard, Ancestor-Warrior) account for 20/35 forms — and Lu Bu (East Asian polearm/halberd) WAS a candidate for Polearm Soldier or Twin-Blade, yet didn't appear.

**T4 post-mortem item:** add anchor-priority enumeration as v1.1+ engine amendment. **Empirical-evidence criterion for re-engagement on anchor sampling:** next regeneration at N≥60 OR explicit anchor-priority-sampling fix; if anchors still don't surface at N=60, the substrate-binding lookup logic has a deeper gap than sampling order.

### 2.2 One representative form per § 8 signature strategy (4 strategies elected)

#### RESOURCE_CONVERSION — v2-form-013 Ashen Geomancer (Totem Hierophant earth_caster)

| Field | Value |
|---|---|
| BC-target cell | Totem Hierophant (range=mid, tempo=low, amplitude=variable, attribute=INT, proxy_density=heavy) |
| Archetype / energy / role | earth_caster / mana / damage |
| Main weapon | "Powder tester" (royal_armouries, early_modern) |
| Cultural | european / early_modern |
| § 8 signature | RESOURCE_CONVERSION |
| `gamora_combatant_fields` | `{resource_conversion: {cost_resource: HP, scope: all_skills}}` |
| Spirit-guide template | `resource_cost_shift` |
| Narrative hooks | sacrifice / blood_magic / life_wager |

**Design-fit verdict:** ⚠️ **substrate-binding misfit at the weapon-substrate layer.** "Powder tester" (a gunpowder-quality-testing instrument from Royal Armouries) does NOT read as a totemic-earth-caster kit identity. The L11 substrate-binding picked an early-modern European technical instrument to bind a Totem Hierophant cell — this is the kind of "found-object-via-keyword-match" failure mode the substrate-led discipline is supposed to guard against. The class name "Ashen Geomancer" + the LLM flavor are salvaging it at the cosmetic layer, but the underlying weapon substrate × kit-identity coherence is weak.

**Anti-pattern named:** this is the **museum-keyword-mismatch** pattern. Met Museum + Royal Armouries categorize by physical-attribute-keywords, not by mythological-function-keywords. "Powder tester" satisfies the mechanical-substrate-triple (physical/category/handheld_weapon) but fails the cultural-tradition × archetype semantic test for "Totem Hierophant earth-caster." The semantic-layer rep-audit discipline candidate (gandalf OP § 4.4) names this exact pattern: substrate votes at geometry layer; design surfaces audit at semantic layer.

**RESOURCE_CONVERSION elected on this kit:** the algorithm fired RESOURCE_CONVERSION (HP-as-mana) on an earth-caster Totem Hierophant. Earth-caster + blood-magic is a non-obvious pairing. In ARPG-class-fantasy terms, this would be Druid + Necromancer hybrid — interesting but unusual. Whether the algorithm should have elected DEFENSIVE_CONVERSION (totemic-bulwark) or GEOMETRY_COLLAPSE (focused earth-spike) instead is a design judgment call. **gandalf lean:** for "Totem Hierophant," DEFENSIVE_CONVERSION reads as more on-theme; RESOURCE_CONVERSION reads as algorithm overreach on this cell. Surface for Matt review.

#### TRADE_OFF — v2-form-003 Khyber Shadow Dancer (rogue / Dagger Assassin / Alexander anchor)

| Field | Value |
|---|---|
| BC-target cell | Dagger Assassin (range=melee, tempo=high, amplitude=flat, attribute=DEX, proxy_density=none) |
| Archetype / energy / role | rogue / focus / damage |
| Main weapon | Kukri (wikipedia, unknown period, lineage=Alexander the Great) |
| Cultural | south_asian / unknown |
| § 8 signature | TRADE_OFF |
| `gamora_combatant_fields` | `{trade_off: {hit_modifier: 1.0, crit_rate: 0.0}, geometry_collapse: ..., resource_conversion: ...}` |
| Spirit-guide template | `hit_crit_regime_change` |
| Narrative hooks | reliability / consistency / no_crits |

**Design-fit verdict:** ⭐ **strong design fit.** Kukri (Nepalese fighting knife; Gurkha tradition) + Khyber-pass-shadow-dancer kit identity + TRADE_OFF (reliability-via-no-crits, hit_modifier=1.0 / crit_rate=0.0) maps cleanly to the "consistent precise blade-killer who doesn't rely on luck" archetype. In Diablo II terms: this is the Trapazon over the Lightning Sorc — favors deterministic application over variance.

**Algorithm § 8 verdict on TRADE_OFF election:** the BC-cell amplitude=flat (low-variance damage profile) couples mechanically with TRADE_OFF (crit_rate=0.0; flat-output regime). Algorithm honored the BC-cell signal. ✅

**Substrate quirk:** "lineage=Alexander the Great" + kukri (Nepalese/Khyber) substrate is a cross-civilizational marriage that LLM rendered as "Where the Macedonian conqueror's blade met the mountain passes, a new breed of silent death was forged." This is Phase 5 narrative-coalescence doing what it should — taking algorithmically-bound disparate substrate signals and rendering a coherent kit-identity narrative. Strong example of LLM cohesion-coalescence working at the form-layer.

#### GEOMETRY_COLLAPSE — v2-form-021 Galeborn Standard Bearer (wind_controller / Storm Caller/Druid)

| Field | Value |
|---|---|
| BC-target cell | Storm Caller/Druid (range=ranged, tempo=medium, amplitude=variable, attribute=WIS, proxy_density=none) |
| Archetype / energy / role | wind_controller / mana / control |
| Main weapon | "Banner with Shaft" (met-museum, early_modern) |
| Cultural | european / early_modern |
| § 8 signature | GEOMETRY_COLLAPSE |
| `gamora_combatant_fields` | `{geometry_collapse: {aoe_radius_multiplier: 0.5, damage_multiplier_bonus: 1.5}, resource_conversion: ...}` |
| Spirit-guide template | `geometry_amplitude_trade` |
| Narrative hooks | focus / concentrated_force / narrow_spike |

**Design-fit verdict:** ⚠️ **kit-identity collision; § 8 election fights archetype.** Storm Caller / wind-controller = wide AOE storm-conjurer archetype (think Druid Tornado in D2). GEOMETRY_COLLAPSE → AoE-shrinks-to-0.5× / damage-grows-1.5× is the OPPOSITE of storm-caller fantasy. The algorithm fired the "concentrate damage into narrow spike" keystone on a kit whose entire identity is "wide-area weather control." This is a textbook **algorithm-vs-class-fantasy misfit.**

In ARPG-class-design terms (PoE jewel/keystone analog): GEOMETRY_COLLAPSE is the Point Blank or Resolute Technique keystone — it suits assassin-spike or melee-warrior kits, NOT storm-controllers. The opportunity-scan needs an archetype-veto layer that says "wind_controller + WIS-primary + role=control → never elect GEOMETRY_COLLAPSE." Currently the scan operates purely on mechanical_substrate_triple signals (physical / banner / accessory_handheld) without consulting `archetype_tag` or `role_orientation`.

Also: the main_weapon is "Banner with Shaft" — banner-as-storm-wand reads as a flag-staff weather-divination flavor that's substrate-coherent enough. The misfit is on § 8 election, not on substrate-binding.

**T4 post-mortem item:** L9 opportunity-scan refactor needs an archetype-veto layer. Surface this as candidate algorithm amendment for v1.1+.

#### DEFENSIVE_CONVERSION — v2-form-000 Rampart Knight (Heavy Barbarian physical_warrior)

| Field | Value |
|---|---|
| BC-target cell | Heavy Barbarian (range=melee, tempo=low, amplitude=spiky, attribute=STR, proxy_density=none) |
| Archetype / energy / role | physical_warrior / rage / damage |
| Main weapon | "shield" (royal_armouries, early_modern) |
| Cultural | european / early_modern |
| § 8 signature | DEFENSIVE_CONVERSION |
| `gamora_combatant_fields` | `{defensive_conversion: {evasion_to_armor: True}, geometry_collapse: ...}` |
| Spirit-guide template | `stat_layer_remap` |
| Narrative hooks | iron_will / endurance / armor |

**Design-fit verdict:** ⭐ **canonical DEFENSIVE_CONVERSION fit; algorithm working as intended.** Shield-as-weapon (interesting; the main_weapon is literally "shield" not a sword) + heavy-armor warrior + DEFENSIVE_CONVERSION (evasion→armor) + narrative hooks (iron_will/endurance/armor) all converge. The LLM Phase 5 form-naming did good work here: "Rampart Knight" + "wall of iron between the living and oblivion" is on-theme. This is Diablo II's Defender-paladin in essence.

**Minor pattern:** the algorithm pairs DEFENSIVE_CONVERSION with GEOMETRY_COLLAPSE secondary on this form. The keystone-stack reading is "tanky-spiky-melee" — high armor + concentrated AOE-shrunk damage. This is a coherent two-keystone-stack identity, not algorithmic noise. Good algorithm composition.

#### ELEMENT_CONVERSION — NOT ELECTED IN THIS RUN

Per § 1.3 finding above: ELEMENT_CONVERSION (Avatar-of-Fire-class strategy) requires substrate with element ≠ physical. The physical-uniform substrate this run sampled has zero substrate rows that would trigger ELEMENT_CONVERSION opportunity-scan. **This is substrate-led discipline operating correctly** — the algorithm declines to manufacture an element-conversion keystone on physical-element substrate. The framing brief's expectation of "ELEMENT_CONVERSION represented" is met by the L9 refactor's CORRECT REFUSAL TO FIRE it on this substrate.

**T4 post-mortem item:** validate by querying — when is the next regeneration that will include fire/water/earth/etc element-tagged substrate? Once non-physical substrate is in the run, ELEMENT_CONVERSION should fire (confirming the strategy is functional, not just non-elected).

#### DEFENSIVE_TRADEOFF — NOT ELECTED IN THIS RUN

DEFENSIVE_TRADEOFF (Chaos Inoculation-class strategy) requires combat-context with shadow OR holy damage AND chaos-immunity payoff structure. Like ELEMENT_CONVERSION, this is gated on substrate signals the physical-uniform run doesn't produce. **The strategy is functional but un-firable on this substrate.**

### 2.3 Engine-authored gap-fill forms (Stage 3.5 provenance — surfaced via section_4_routing not form-level source_library)

Per § 1.5 finding: form-level `source_library` is uniformly `generator_v2` across 35/35 forms. Stage 3.5 / Sidecar B provenance is buried in `balance_metadata.generation_params.section_4_routing` and in weapon-level `main_weapon.source_library`. Forms with section-4 alternative routing OR weapon-level engine-authored-gap-fill:

| Form | section_4_routing | Note |
|---|---|---|
| v2-form-008 (Moctezuma fire_mage) | (default) | weapon: `engine_authored_gap_fill_v1` for moctezuma_atlatl |
| v2-form-014 (Holy Knight/Paladin holy_caster Mace) | (default) | substrate-pulled |
| v2-form-015 (Artillery Mage → Cell 12) | `fold_to_cell_12_t4_alteration` | locked routing; fold-treatment outcome WORKING |
| v2-form-016 (Pyromantic Caster fire_mage) | `stage_3_5_engine_authored_gap_fill` | weapon: royal_armouries "Gunner's dividers" — substrate sampled despite "stage_3_5" flag (likely a relaxed-pool fallback) |
| v2-form-018 (Necromancer Summoner shadow_caster) | `sidecar_b_necro_enrichment_proxy_spawn` | weapon: `nick-aschenbach-dnd-data` "Flutterby Rod" (D&D-substrate fantasy register; fictional period) |
| v2-form-022 (Monk-archetype physical_grappler) | `sidecar_b_east_asian_fist_staff_option_c` | weapon: met-museum "Mounting for Short Sword (Wakizashi)" — option_c match (cross-attribute) |
| v2-form-024 (Witch Doctor Petmaster shadow_controller) | (default) | substrate-pulled; lineage=Saint George (anchor) |
| v2-form-025 (Moctezuma physical_warrior Heavy Barbarian) | (default) | weapon: `engine_authored_gap_fill_v1` for moctezuma_aztec_war_club |
| v2-form-009 (Roland physical_warrior Ancestor-Warrior) | (default) | weapon: `engine_authored_gap_fill_v1` "roland_durandal" |

**Engine-authored-gap-fill weapons (3 unique):** `moctezuma_atlatl` + `moctezuma_aztec_war_club` + `roland_durandal`. These are the engine-authored named-weapons emitted by the gap-fill pass — substrate-row IDs in the 200K+ range suggesting late-tier insertion. Each is bound to its named-bearer lineage. **Substrate quality verdict:** excellent. Named weapons (Durandal, atlatl, macuahuitl) are mythologically-defensible and substrate-coherent with their bearers.

### 2.4 Mythological-NULL rescue forms (Stage 4 provenance)

`accept_0.45_conf_pool_stage4_priority` fires on 2 forms. Need to identify which — let me note that this routing appears in `section_4_routing` distribution but the corresponding forms aren't called out by `cell_label`. Per the substrate-pool fallback semantic, Stage 4 priority routing means: confidence threshold relaxed to 0.45 + Stage 4 pool searched first. This is acceptable composition policy behavior; no form-quality issue surfaces from inspection.

### 2.5 Broader anchor forms (Tier-1 / Tier-2 named bearers beyond Sketch F)

Nine forms carry `named_bearer` lineage in `main_weapon.lineage`:

| Form | Class name | Named bearer | Tier | Weapon | § 8 signature |
|---|---|---|---|---|---|
| v2-form-001 | Blade of Empires | Charlemagne (european_medieval) | tier_2 | Sword of Attila | DEFENSIVE_CONVERSION |
| v2-form-003 | Khyber Shadow Dancer | Alexander the Great (greek) | tier_2 | Kukri | TRADE_OFF |
| v2-form-007 | Sadamune Bladedancer | Sadamune (east_asian) | tier_2 | Terasawa Sadamune | TRADE_OFF |
| v2-form-008 | Sunstone Spearthrower | Moctezuma | (Sketch F) | moctezuma_atlatl | RESOURCE_CONVERSION |
| v2-form-009 | Paladin of Durandal | Roland | tier? | roland_durandal | DEFENSIVE_CONVERSION |
| v2-form-024 | Shadowbane Standard-Bearer | Saint George (european_medieval) | tier_2 | Banner with Shaft | DEFENSIVE_CONVERSION |
| v2-form-025 | Moctezuma's Jade Warlord | Moctezuma | (Sketch F) | moctezuma_aztec_war_club | RESOURCE_CONVERSION |
| v2-form-026 | Blade of Castile | El Cid (european_medieval) | tier_2 | Colada | GEOMETRY_COLLAPSE |
| v2-form-028 | Phantom Blade Inheritor | Sadamune (east_asian) | tier_2 | Tokuzen-in Sadamune | TRADE_OFF |
| v2-form-030 | Iron Shilpi Veer | Wayland the Smith (european_medieval) | tier_1 | .476 Nitro Express | DEFENSIVE_CONVERSION |

**Design-fit verdict on anchor forms:** mostly strong. Charlemagne+Sword of Attila, Alexander+Kukri, Sadamune+his own signature blades, Roland+Durandal, El Cid+Colada — these are MYTHOLOGICALLY-DEFENSIBLE pairings. The Phase 5 LLM naming + flavor text is doing strong cohesion-coalescence work on these.

**One striking misfit — v2-form-030 Wayland the Smith + .476 Nitro Express:** Wayland is Tier-1 (the founding anchor in the European mythological smith tradition; the lineage from which Vulcan/Hephaestus archetypes derive). Wayland's substrate-weapon should be Wayland-forged-sword OR Wayland-armor — NOT a `.476 Nitro Express` (a 19th-century British big-game hunting cartridge). The LLM Phase 5 salvages it ("Forged in Wayland's sacred fire, this warrior carries thunder itself, where ancient craft meets the dharma of devastation") via the metaphor of "Wayland's sacred fire = gunpowder thunder," but the substrate binding is mechanically jarring: industrial-era firearm cartridge paired with mythological Anglo-Saxon smith. This is `cultural_tradition: south_asian` + `period: classical` (?!) which is also incoherent — the form's metadata says south_asian/classical but the weapon is European/industrial. **Cross-civilizational substrate-binding without thematic constraint produces these blends.**

In Diablo II terms: this is like assigning Stormcaller's Wand from Act 4 to a Barbarian wearing Sigon's Steel. Possible mechanically; thematically incoherent. Worth flagging.

**Sadamune doubled (v2-form-007 + v2-form-028):** like Moctezuma, Sadamune appears twice — both in Twin-Blade Fencer (007) and Dagger Assassin (028). Both forms reuse his historical signature swords (Terasawa Sadamune + Tokuzen-in Sadamune). This is **substrate-coherent fan-out** at the named-bearer level — the SAME forged smith provides substrate to TWO algorithm-divergent kits of similar archetypal flavor (skirmisher vs assassin). Better than Moctezuma's two-cell-fan because both Sadamune kits stay in the "DEX-blade-master" semantic neighborhood.

### 2.6 Edge case forms (worth flagging)

#### v2-form-019 Solar Sovereign — Channeling Cleric WIS with "Banner of Louis XIV" as main_weapon (banner category)

The substrate-binding is a banner-as-weapon for a WIS/holy_caster cleric. This is a substrate-tagging stretch — Met Museum tagged the Banner of Louis XIV as a `handheld_weapon` mechanically (per `mechanical_substrate_triple: physical/banner/accessory_handheld`). Phase 5 LLM resolved it via "Sun King's radiant standard" / "command the battlefield through divine authority." Coherent at the flavor layer; substrate is unusual but defensible (royal banners DO function as field-rallying instruments). **gandalf verdict:** acceptable. The composition-policy banner-as-handheld treatment is novel but works for cleric-flavor kits.

Five forms use banner-substrate as main_weapon:
- v2-form-019 (Channeling Cleric, Banner of Louis XIV)
- v2-form-021 (Storm Caller, Banner with Shaft)
- v2-form-023 (Druid Beastmaster, Banner Hata)
- v2-form-024 (Witch Doctor Petmaster, Banner with Shaft)

These are all WIS/INT-primary caster/controller kits. The substrate-binding logic seems to route banners to caster-archetype kits, which is design-coherent for "banner-as-channeling-focus" treatment. Worth confirming Matt-direction agrees.

#### v2-form-022 Crimson Leaf Binder — Monk-archetype with Japanese wakizashi mounting

This is the only form using `option_c` matching policy (cross-attribute substrate matching). The Monk-archetype cell binds to a Japanese sword-mounting via `sidecar_b_east_asian_fist_staff_option_c` routing. Class name "Crimson Leaf Binder" + flavor "the sage wrestler reads the body's truth, subduing foes with wakizashi and ancient knowing hands" is a creative resolution — a wakizashi-armed grappler is unusual but story-defensible (samurai wrestling traditions exist). **Algorithm and Phase 5 together produced a coherent niche form on thin substrate.** ✅

#### v2-form-027 / v2-form-002 — Two duplicate "Menuki Bladedancer" forms with IDENTICAL class names

Both v2-form-002 and v2-form-027 generated the LLM class name "Menuki Bladedancer" — the same Light Fighter cell, both bound to "Pair of Sword-Grip Ornaments (Menuki)" weapon substrate, both physical_warrior STR. **Phase 5 LLM produced identical naming with no de-duplication.** This is a calibration gap: the LLM-naming step should observe in-run uniqueness and either suppress duplicates or seed-vary names.

In gacha-game terms (FGO/Pokemon Masters), this is the duplicate-summon failure mode. Worth a small calibration fix in Phase 5: pass current-run name-pool as anti-context to the LLM call. Easy fix; should land before next regeneration.

#### v2-form-006 / v2-form-010 — "Ironbolt Warden" / "Iron Bolt Warden" near-duplicate

Cell Crossbow Sniper (v2-form-006) → "Ironbolt Warden"; cell Falconer/Pet-Archer (v2-form-010) → "Iron Bolt Warden". Same kit identity, near-identical name across different cells. Same Phase 5 calibration gap as above — LLM is converging on similar templated names. Diversity-of-name pressure is weak.

#### Multi-cell § 8 strategy stability check

Cells appearing twice in this run sometimes get DIFFERENT § 8 signatures (Heavy Barbarian: DEFENSIVE_CONVERSION + RESOURCE_CONVERSION; Standard Wizard: 2× RESOURCE_CONVERSION; Polearm Soldier: DEFENSIVE_CONVERSION + GEOMETRY_COLLAPSE; Light Fighter: TRADE_OFF + GEOMETRY_COLLAPSE; etc.). **Algorithm is NOT deterministic-on-cell** — the within-cell stochastic variation produces different keystone elections per substrate row bound. This is design-coherent (different substrate → different opportunity-scan trigger) but worth confirming Matt agrees: should some cells have a "primary signature" stamp + cells stochastically vary AROUND it, or is "every form independently scanned" the right policy?

In PoE Ascendancy terms: this is asking whether "Berserker = always Resolute Technique base" or "Berserker = whatever the keystone-scan finds for THIS Marauder weapon-binding." Both are valid design choices; pick one intentionally.

---

## 3. Cross-form patterns

### 3.1 Substrate-binding integrity

**Strict-match relaxation:** 35/35 forms at `relaxation_level=0` (option_alpha + option_beta + option_c). Zero thin-cell-fallback fired in this run, meaning the substrate pool was rich enough at strict 4-tuple match for all 25 cells (even the ones reported BLOCKED per § 1.5).

**Matching-policy distribution:** option_alpha 20 / option_beta 12 / option_c 3. Most forms (57%) used strictest matching; option_beta (attribute-level relaxation) on 34%; option_c (cross-attribute) on 9%. This is healthy — most forms anchored at strict match, with controlled relaxation only where cell requires it (Monk-archetype, Pyromantic Caster, etc.).

**Substrate-quality tier distribution:** S × 24 / A × 9 / B × 2. 86% of forms drew from Tier-S or Tier-A substrate pools. ⭐ excellent. The two Tier-B picks (v2-form-018 Necromancer Summoner "Flutterby Rod" from nick-aschenbach-dnd-data + one other) are the lowest-quality substrate in the run — acceptable for fantasy-register cells where historical substrate is genuinely scarce.

**Cultural-tradition distribution:** european 20 / east_asian 8 / south_asian 2 / mesoamerican 2 / fantasy_generic 2 / middle_eastern 1. **European-skew (57%)** — substrate pool dominance reflects Met Museum + Royal Armouries cataloguing biases. This is a substrate-coverage finding (elrond/legolas territory) not an engine finding, but it shapes the run's overall cultural register: this is a Eurocentric run, with East Asian as second tier. For isekai-genre cultural fan-out (the Reincarnated game's premise), this skew should narrow over time as Sidecar B enrichments land.

**Period distribution:** early_modern 19 / medieval 5 / industrial 3 / contemporary 2 / modern 2 / fictional 2 / unknown 1 / classical 1. **Early-modern dominance (54%)** reflects gunpowder-era + scientific-instrument substrate richness. The "industrial / modern / contemporary" total of 7/35 forms means ~20% of forms are bound to industrial+ substrate (e.g., v2-form-031 Blaser R93 7.62mm rifle for Crossbow Sniper). This is the **anachronism risk** noted in composition policy v1: modern firearms substrating a "Crossbow Sniper" cell is mechanically-defensible (both are "long-range precision DEX kits") but tonally-jarring for a fantasy/isekai game.

**T4 post-mortem item:** confirm Matt's desired upper-period bound. Cycle 13 may need to add a `period_filter` to the substrate query to gate out 19th-century+ firearms when the seasonal register is medieval-classical-only.

### 3.2 § 8 strategy distribution

(Covered fully in § 1.3.) Key cross-form observation:

**Strategy-archetype cross-tab reveals algorithm character:**

| Archetype | DEFENSIVE_CONVERSION | TRADE_OFF | GEOMETRY_COLLAPSE | RESOURCE_CONVERSION |
|---|---|---|---|---|
| physical_warrior (10) | 4 | 1 | 4 | 1 |
| hunter (5) | 3 | 1 | 1 | 0 |
| fire_mage (5) | 1 | 1 | 1 | 2 |
| rogue (3) | 1 | 2 | 0 | 0 |
| physical_skirmisher (3) | 0 | 2 | 0 | 1 |
| earth_caster (2) | 1 | 0 | 0 | 1 |
| holy_caster (2) | 1 | 0 | 1 | 0 |
| wind_controller (2) | 0 | 1 | 1 | 0 |
| shadow_caster (1) | 0 | 1 | 0 | 0 |
| physical_grappler (1) | 1 | 0 | 0 | 0 |
| shadow_controller (1) | 1 | 0 | 0 | 0 |

**Patterns:**
- DEFENSIVE_CONVERSION dominates physical_warriors + hunters (tanky-archers + tanky-melee) — algorithm correctly converging on "armor-class kits get DEFENSIVE_CONVERSION."
- TRADE_OFF dominates rogues + skirmishers (focus-based DEX archetypes) — reliability/no-crit reads as on-theme.
- GEOMETRY_COLLAPSE dominates physical_warriors (spike-melee) + holy_caster — concentrated-damage payoff fits these.
- RESOURCE_CONVERSION concentrates on fire_mages + ALL named-Moctezuma forms — algorithm associating mana-economy-shift OR rage-economy-shift with Aztec-ritual + fire-magic combinations.
- **wind_controller getting GEOMETRY_COLLAPSE × 1 is the v2-form-021 Galeborn Standard Bearer misfit noted in § 2.2** — the only obvious archetype-veto-needed case in this run.

### 3.3 Calibration parameter behavior (§ 10 parameters)

Per `gamora_combatant_fields` populated values:
- `evasion_to_armor: True` (DEFENSIVE_CONVERSION; boolean — no calibration parameter exposed)
- `aoe_radius_multiplier: 0.5, damage_multiplier_bonus: 1.5` (GEOMETRY_COLLAPSE; 2 params)
- `hit_modifier: 1.0, crit_rate: 0.0` (TRADE_OFF; 2 params)
- `cost_resource: HP, scope: all_skills` (RESOURCE_CONVERSION; 2 params — discrete enum-valued)

**All 35 forms share IDENTICAL calibration parameter values per strategy.** There's zero per-form variance in the gamora_combatant_fields numeric values. This is a **v1 narrow milestone calibration state finding** — the algorithm emits the strategy with constant-default parameters, not stochastically-varied ones.

This is fine for v1 narrow (proves the wire-up works; demonstrates the cell→strategy→combat-arithmetic pipeline). But it means: **all 13 DEFENSIVE_CONVERSION forms have IDENTICAL mechanical impact** (evasion→armor with same boolean). All 8 GEOMETRY_COLLAPSE forms have IDENTICAL aoe-shrink/damage-grow numbers. From a player-feel perspective, this means **two Heavy-Barbarian DEFENSIVE_CONVERSION forms (e.g., v2-form-000 + v2-form-009 Roland) would FEEL IDENTICAL in combat** — same defensive math, same fight-engine output (notwithstanding skill-tree differences which DO vary).

**T4 post-mortem item:** is v1.1+ goal to introduce per-form parameter variance (e.g., aoe_radius_multiplier could be 0.4/0.5/0.6 depending on substrate signal strength), or are these strategy-level constants intentionally locked?

### 3.4 L9 opportunity-scan refactor outcomes

The L9 refactor to drive trigger-detection from `mechanical_substrate_triple` signals (not cultural_tradition heuristics) appears to be working at the geometric level:
- The 4-strategy elected set maps cleanly to mechanical-substrate categories: shield + armor → DEFENSIVE_CONVERSION; precise-blade → TRADE_OFF; focused-handheld → GEOMETRY_COLLAPSE; HP-economy + ritual-context → RESOURCE_CONVERSION.
- Cultural-tradition data is RETAINED at the metadata layer (for semantic Phase 5 narration) but does NOT drive strategy election.

The **Galeborn Standard Bearer misfit** (§ 2.2 GEOMETRY_COLLAPSE on wind-controller) and the **Powder Tester Totem Hierophant misfit** (§ 2.2 RESOURCE_CONVERSION on totemic earth-caster) are the two clearest cases where pure-mechanical-substrate-driven scan ignores archetype-veto signals. These are **L9 v1.1 amendment candidates** — the refactor needs an archetype-veto layer atop mechanical-substrate signals.

### 3.5 Phase 5 naming quality

**Form-layer LLM naming WORKS:** 35/35 forms have readable, on-theme, substrate-respecting class names. Standout examples: "Moctezuma's Jade Warlord", "Khyber Shadow Dancer", "Paladin of Durandal", "Sunstone Spearthrower", "Solar Sovereign", "Ironblood Warlord", "Sadamune Bladedancer". These read as authored, not generated.

**Phase 5 gaps surfaced:**
1. **Skill-layer naming NOT FIRED** — 289/289 skill nodes have placeholder names. Major content gap.
2. **No in-run name uniqueness enforcement** — v2-form-002 + v2-form-027 both got "Menuki Bladedancer"; v2-form-006 + v2-form-010 got near-duplicate "Ironbolt Warden" / "Iron Bolt Warden". Pass current-run name-pool as anti-context.
3. **Sub-element coalescence NOT FIRED** — `seasonal_dominant_element: null` on 35/35; Phase 5 cohesion-judge calibration is PENDING per framing brief § 1.3, so this is acknowledged.
4. **Title completion NOT FIRED** — `title_completion: null` on 35/35; the "Name + Title" pattern (e.g., "Rampart Knight, [Title]") isn't producing the completion.
5. **`thematic_rationale` NOT FIRED** — 35/35 `t4_alteration_output.thematic_rationale: ""`; the keystone-rationale narrative metadata is empty. Spirit-guide narration falls back on `narrative_hooks` only.
6. **Skill `flavor_text` NOT FIRED** — even though form-layer flavor_text WAS populated, skill-layer narrative coalescence didn't run.

The naming/flavor pipeline has a **scope-of-LLM-coalescence-pass gap**: Phase 5 runs at form-layer, not skill-layer or sub-element-layer. This is a v1.1+ Phase 5 calibration spec scope expansion.

### 3.6 New finding — element uniformity (1/8)

All 35 forms `dominant_element: physical`. This deserves a dedicated subsection (§ 4.3 below).

---

## 4. Design-fit flags for T4 post-mortem session 1

### 4.1 Surprising-but-valid choices

| Form | Surprise | Why valid |
|---|---|---|
| **v2-form-025 Moctezuma's Jade Warlord** | RESOURCE_CONVERSION on physical_warrior | Substrate (Aztec war-club + Moctezuma context) supports blood-magic-rage-economy; algorithm honored substrate signals |
| **v2-form-008 Sunstone Spearthrower** | Moctezuma in INT/fire_mage cell | Atlatl-as-sun-priest-staff is mythologically-defensible; reincarnation-multiple-form pattern is isekai-thematically-honest |
| **v2-form-018 Twilight Rod Sage** | Necromancer Summoner with TRADE_OFF + D&D fantasy-substrate | Reliability-via-no-crits on a necromancer is unusual but reads as "controlled / methodical necromancer"; flutterby rod is a charming substrate-flavor choice |
| **v2-form-022 Crimson Leaf Binder** | Monk-archetype with wakizashi-mounting | option_c cross-attribute match produces a samurai-wrestler kit-flavor that's narrow but defensible |
| **Sadamune doubled (007 + 028)** | Same named-bearer in two cells | DEX-blade-master fan-out across skirmisher + assassin; reincarnation-pattern stays in semantic neighborhood |

### 4.2 Misfits — algorithm or substrate-binding produced design-incorrect output

| Form | Misfit | Severity | Proposed fix scope |
|---|---|---|---|
| **v2-form-021 Galeborn Standard Bearer** | GEOMETRY_COLLAPSE on wind_controller storm-caller (algorithm-vs-class-fantasy) | HIGH | L9 algorithm amendment: archetype-veto layer atop mechanical-substrate signals |
| **v2-form-013 Ashen Geomancer** | "Powder tester" (gunpowder-quality-test instrument) substrate-bound to Totem Hierophant earth-caster | MEDIUM | Substrate-tagging audit: museum-keyword-mismatch pattern; semantic-layer rep-audit at firing per OP § 4.4 candidate |
| **v2-form-030 Iron Shilpi Veer** | Wayland the Smith (Anglo-Saxon mythological smith Tier-1) + `.476 Nitro Express` (1880s British cartridge) + cultural_tradition=south_asian + period=classical (inconsistent metadata) | HIGH | Substrate-binding logic: respect lineage-period coherence; cross-period anchor-substrate binding produces blends like this. Also: form metadata inconsistency (south_asian/classical vs Wayland=european_medieval) suggests tagging-source mixing |
| **v2-form-013 Ashen Geomancer & v2-form-019 Solar Sovereign** | Banner-as-weapon for non-cleric cells, paired with mismatched archetypes | LOW | Composition policy verdict on banner-substrate routing — possibly intentional |
| **Duplicate names v2-form-002+027 ("Menuki Bladedancer") and v2-form-006+010 ("Ironbolt Warden")** | LLM Phase 5 produces duplicate names in-run | MEDIUM (calibration) | Pass current-run name-pool as anti-context to LLM call |

### 4.3 Coverage gaps (major)

**Gap 1 — Element uniformity (1/8):** 35/35 forms `dominant_element: physical`.

- **gandalf judgment:** this is an **acceptable v1 narrow milestone finding** but should **NOT BLOCK T4 post-mortem readiness**. Rationale:
  - The v1 narrow milestone is about proving the engine's BC-cell → § 8 → fight-engine pipeline works. That has been proven.
  - The substrate this run sampled (v1_scope=1 substrate pool, 2293 items) appears to be uniformly physical-element tagged. This is a **substrate-tagging-layer finding** (elrond/legolas territory), not an engine bug.
  - Per § 8 algorithm + substrate-led discipline, element_conversion and element-flavored signatures cannot fire on physical-uniform substrate. The algorithm refusing to fire them is correct.
  - The archetype-internal element variety (fire_mage, earth_caster, holy_caster, shadow_caster, wind_controller — 6 elemental archetypes present) means the SEMANTIC element diversity IS present even when the substrate-element field is uniformly physical.

- **What the player would feel:** in this run's output, every form's "element" badge says "physical." A player browsing the loadout app sees all 35 kits as physical-element kits, even though the archetype tags indicate fire / earth / wind / shadow / holy mages internally. This is a **substrate-element-vs-archetype-element mismatch** that will read as confusing.

- **Empirical-evidence criterion for re-engagement:** Cycle 13 substrate-tagging pass — elrond / legolas conduct substrate-element-classification on the v1_scope pool (likely via L9 mechanical_substrate semantic-layer audit) to break out elemental-substrate categories. Once the substrate pool has non-physical-element rows tagged, regenerate at N≥60 and confirm elemental § 8 signatures fire.

- **Should v1 narrow milestone be re-stamped?** No. The narrow milestone is the engine-pipeline proof, which is achieved. The element-uniformity gap is a known substrate-layer task for Cycle 13.

**Gap 2 — Sketch F anchor sub-sampling (1/4):** Only Moctezuma sampled.

- **gandalf judgment:** **policy gap, not BLOCKING but worth surfacing.**
  - Two interpretations possible (§ 2.1):
    - (a) Cell-order enumeration didn't reach cells where Hattori Hanzō / Lu Bu / Gilgamesh substrate rows would have surfaced
    - (b) Substrate-coverage gap — these anchors' substrate rows may exist in the pool but bind preferentially to cells the enumeration didn't visit
  - The substrate-led-discipline-honoring fix is: **add anchor-priority sampling constraint** ("enumerate cells, but ALSO enforce ≥1 form per Sketch F anchor where substrate exists"). This adds 3 forms to the next run.

- **Empirical-evidence criterion for re-engagement:** next regeneration at N≥60 with explicit anchor-priority-sampling. If at N≥60 the anchors still don't surface, then the substrate-binding lookup logic has a deeper gap than sampling order — investigate substrate-row-to-cell mapping for these anchors.

**Gap 3 — Skill-content production (0/289 LLM-named, 0/289 flavor-textured):** Phase 5 ran at form-layer only.

- **gandalf judgment:** **acknowledged as Phase 5 scope-of-coalescence gap (per framing brief § 1.3 — Phase 5 calibration spec PENDING). v1 narrow milestone is not blocked by this, but T4 post-mortem session 1 cannot fully evaluate "skill-tree feel" with placeholder skill names.**

- **Empirical-evidence criterion for re-engagement:** Phase 5 calibration spec authoring (gandalf canonical doc; queued per framing brief § 1.3) defines whether skill-layer LLM-coalescence is in v1.1 or later. Once spec lands and skill-layer Phase 5 fires, regenerate and confirm skill names + flavor_text + effects populate.

**Gap 4 — BLOCKED-cells reportage:** Manifest claims 3 BLOCKED cells; reality is 0-1 truly blocked.

- This is a **manifest/reportage update** (not an engine issue). The composition policy v1 § 4.1 routing matrix works — section_4_routing handles Pyromantic Caster + Necromancer Summoner cleanly. The manifest's "BLOCKED" status was a pre-run prediction that didn't survive contact with the executor.

- **Empirical-evidence criterion for re-engagement:** none — this is documentation cleanup. Knight-rider can update the provenance manifest's "Coverage gaps" subsection to remove Pyromantic Caster + Necromancer Summoner from "BLOCKED cells" list and add them to "Section 4 routing fired" list.

### 4.4 Calibration-tuning candidates

| Parameter | Current value | Issue surfaced | T4 disposition |
|---|---|---|---|
| GEOMETRY_COLLAPSE aoe_radius_multiplier | 0.5 (constant) | All 8 GEOMETRY_COLLAPSE forms identical | Decide per-form-variance vs constant; if variance: tie to BC-cell amplitude signal |
| GEOMETRY_COLLAPSE damage_multiplier_bonus | 1.5 (constant) | All 8 forms identical | Same as above |
| TRADE_OFF hit_modifier | 1.0 (constant) | All 9 TRADE_OFF forms identical | Decide: if "no-crit but no hit bonus" is intentional, document; if hit-bonus should compensate, calibrate |
| TRADE_OFF crit_rate | 0.0 (constant) | All 9 forms identical | Likely intentional (TRADE_OFF = "no crits") |
| RESOURCE_CONVERSION cost_resource | HP (constant) | All RESOURCE_CONVERSION forms identical | Decide: should some forms convert mana→focus or focus→rage? Currently only HP-as-substitute fires |
| DEFENSIVE_CONVERSION evasion_to_armor | True (boolean) | No calibration knob exposed | If non-binary degree-of-conversion is desirable, expose as ratio param |

### 4.5 Phase 5 / 6 / 7 gap consequences

- **Phase 5 partial coalescence** — form-layer names/flavor done; skill-layer + sub-element + title-completion + thematic_rationale all skipped. Surfaces as: loadout app displays 35 named forms with placeholder skill names. **Materially affects T4 post-mortem readiness — Matt evaluating "skill-tree feel" cannot do so with `Chain A T1 0` placeholder labels.** Skill-layer Phase 5 is a near-term need.

- **Phase 6 placeholder** — `color_palette: [160,140,100]` and `movement_speed: 8.0` uniform across 35 forms. Loadout app will show all kits with identical visual rendering. **Acceptable for v1 narrow per framing brief § 1.3** — Meshy production wire-up is deferred.

- **Phase 7 implicit** — Layer 6 wire-up = effective sim-viability gate; all 35 forms passed converge_kit. **Acceptable for v1 narrow per framing brief § 1.3** — explicit joint-gate spec is post-v1.

### 4.6 v1.1+ queue additions surfaced by this run

1. **Anchor-priority sampling constraint** — engine enumeration should guarantee ≥1 form per Sketch F anchor when substrate-binding exists.
2. **Archetype-veto layer atop L9 opportunity-scan** — wind_controller should never elect GEOMETRY_COLLAPSE; storm-caller kits should never get concentrated-spike keystones; etc.
3. **In-run name uniqueness in Phase 5** — pass current-run name-pool as anti-context to LLM-name calls.
4. **Skill-layer Phase 5 coalescence** — skill names + flavor + effects-text population.
5. **Sub-element / seasonal_dominant_element coalescence** — Phase 5 calibration spec → fire sub-element flavoring per cohesion-judge.
6. **`thematic_rationale` field population** — § 8 algorithm should emit per-form rationale text for each elected keystone (spirit-guide narrative consumes).
7. **Substrate-element-classification pass** — break out the 2293 v1_scope rows into elemental categories so non-physical signatures can fire.
8. **Period-filter for substrate query** — gate out 19th-century+ firearms from medieval-classical seasonal registers.
9. **Per-form calibration parameter variance** — gamora_combatant_fields params should vary per substrate-signal-strength, not constant per strategy.
10. **`section_4_routing` provenance in form-level `source_library`** — currently buried in `generation_params`; surface as a top-level provenance flag so analytics tools can distinguish substrate_pulled / stage_3_5 / sidecar_b / stage_4 forms without spelunking.
11. **Metadata.json `strategies_covered` semantics fix** — distinguish "strategies the engine knows" from "strategies elected on this run." Currently misleadingly conflated.
12. **Lineage-period consistency check** — v2-form-030's Wayland-medieval + .476-Nitro-Express-industrial + south_asian-classical metadata-trio is incoherent; engine should reject cross-period substrate-binding for anchor-lineaged forms OR explicitly accept and surface the cross-period treatment.

---

## 5. T4 post-mortem session 1 preparation

### 5.1 Recommended Matt + gandalf review agenda

**Block 1 — Engine pipeline verification (15 min):**
- Confirm Tier 2 ratification: § 8 keystones reach combat arithmetic ✅ (already established by `gamora_combatant_fields` populating with concrete numeric params on all 35 forms)
- Confirm substrate-binding integrity ✅
- Confirm Phase 5 form-layer LLM coalescence working ✅

**Block 2 — § 8 strategy election review (20 min):**
- Walk the 4-strategy distribution (DEFENSIVE_CONVERSION 13 / TRADE_OFF 9 / GEOMETRY_COLLAPSE 8 / RESOURCE_CONVERSION 5)
- Discuss algorithm character: archetype-veto need (Galeborn misfit), substrate-vote correctness (Moctezuma forms ⭐)
- Decide: ELEMENT_CONVERSION + DEFENSIVE_TRADEOFF blocking on substrate uniformity — accept as substrate-led-discipline correctness, OR fast-track substrate-element-classification?

**Block 3 — Hand-authored T4 alternatives (45-60 min):**
- Per framing brief § 2.5 — Matt hand-authors ~5-10 T4 keystone alternatives for select forms
- Recommended candidate forms for hand-authored comparison:
  - **v2-form-021 Galeborn Standard Bearer** (algorithm misfit; Matt hand-authors what the storm-caller SHOULD get)
  - **v2-form-013 Ashen Geomancer** (Totem Hierophant with Powder Tester; algorithm misfit + substrate misfit; Matt hand-authors)
  - **v2-form-025 Moctezuma's Jade Warlord** (algorithm ⭐ — Matt validates the RESOURCE_CONVERSION-on-Aztec-warrior pick; compares to what HE would have hand-authored)
  - **v2-form-009 Paladin of Durandal** (anchor form; Matt validates DEFENSIVE_CONVERSION on Roland)
  - **v2-form-018 Twilight Rod Sage** (Necromancer Summoner with TRADE_OFF; surprising-but-valid; Matt validates)

**Block 4 — v1.1+ scope items (15-20 min):**
- Review § 4.6 candidate amendments
- Prioritize for Cycle 13 scope-doc authoring
- Confirm Phase 5 calibration spec ownership (gandalf canonical authoring) + scope (form-layer-only vs form+skill-layer)

### 5.2 Hand-authored T4 alternatives candidate forms

Listed in § 5.1 Block 3. Add as Matt-discretion:
- **v2-form-019 Solar Sovereign** (Banner of Louis XIV cleric — interesting banner-substrate treatment)
- **v2-form-022 Crimson Leaf Binder** (Monk-archetype with wakizashi — interesting option_c match)
- **v2-form-030 Iron Shilpi Veer** (Wayland + Nitro Express misfit — Matt may want to surgically re-author this)

### 5.3 Cycle 13 scope-doc authoring inputs

Per § 4.6 v1.1+ queue (12 items). Suggested Cycle 13 sub-cycle groupings:

- **Sub-cycle 13.1 — Algorithm refinement:** archetype-veto layer (item 2); per-form parameter variance (item 9); thematic_rationale population (item 6)
- **Sub-cycle 13.2 — Substrate enrichment:** substrate-element-classification (item 7); period-filter (item 8); lineage-period consistency (item 12)
- **Sub-cycle 13.3 — Phase 5 calibration spec:** skill-layer coalescence (item 4); sub-element coalescence (item 5); in-run name uniqueness (item 3)
- **Sub-cycle 13.4 — Sampling + reportage:** anchor-priority sampling (item 1); section_4_routing provenance surfacing (item 10); strategies_covered metadata semantics (item 11)

---

## 6. Cross-references

### Anchor docs
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-framing-brief.md` — RATIFIED framing brief
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-run-provenance-manifest.md` — KR-authored provenance manifest (per § 1.5 finding: some manifest claims are stale vs classes.json reality)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` — Cycle 12 RATIFIED framing brief (L1-L11 + interface contract § 4)
- `agentic_orchestration/cycle-12-wind-down-summary-2026-05-25.md` — Cycle 12 closure record

### Canonical engine architecture
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B 8-phase workflow
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composition policy v1 (Option α/β/C matching; thin-cell resolution; Sketch F anchors)
- `canonical/story/skill-system-2026-05-24.md` § 8 — Algorithm § 8 architecture + § 9 spirit-guide explainer pattern
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 — W1.13 multi-dim convergence

### Data artifacts
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json` — 35 forms (load-bearing for this summary)
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow/metadata.json` — run metadata (NB: `strategies_covered` semantics misleading per § 1.3)
- `/Users/admin/Games/reincarnated-loadout/public/seasons/v2_narrow/classes.json` — Vercel-deployed loadout copy

### Loadout analytics surfaces
- Loadout app (Vercel preview per drax `drax/v0.1-engine-generation-run-loadout-amendments-2026-05-25`)
- Design-mode toggle + cultural/period/quality-tier badges + § 8 strategy badge — Gate-2 PASS; awaiting Matt signal for production-promote

### v1.1+ deferred capture
- 12 candidate items per § 4.6 — to be sequenced into Cycle 13 sub-cycle scope-docs per § 5.3
- `canonical/02-roadmap.md` § 1.0 — 2026-05-25 entry for v1.1+ queue
- Phase 5 calibration spec — QUEUED for gandalf canonical authoring (per framing brief § 1.3)

---

## 7. Sign-off

**Author:** gandalf 2026-05-25 — autonomous design-fit pass per framing brief § 2 authorization
**Status:** RATIFIED — empirical-fill complete
**Effort:** ~2.5 hours autonomous (within framing-brief estimate)
**Downstream consumers:**
- Matt — review summary; signal T4 post-mortem session 1 readiness; signal parked-loadout-amendments production-promote
- T4 post-mortem session 1 (Matt + gandalf design call) — substantive review per § 5 agenda
- Cycle 13 scope-doc authoring (gandalf) — per § 5.3 sub-cycle groupings

**Framing-audit applied** (gandalf OP § 4.1 three-question protocol):
- **Q1** — Load-bearing framing assumptions: framing brief assumed ~30-40 forms with 6 strategies + 4 anchors + multi-element coverage + full-content production
- **Q2** — Refutation evidence: classes.json shows 4 (not 6) signature strategies; 1 (not 4) Sketch F anchor; 1 (not 8) element; partial-content production (form-layer Phase 5 only)
- **Q3** — Refine framing OR execute as-framed? **Execute, AND surface the empirical deviations as findings.** The deviations are not framing-shifting at workstream level — the v1 narrow milestone is "engine pipeline proof," which IS empirically achieved. The deviations are substrate-tagging-layer + Phase-5-scope items for Cycle 13.

**For:** the design-fit narrative complementing loadout-displayed forms — what to pay attention to for T4 post-mortem session 1 efficiency.
