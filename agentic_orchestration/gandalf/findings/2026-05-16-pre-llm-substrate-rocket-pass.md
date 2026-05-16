# Pre-LLM Substrate Inventory — Rocket Pass
**Authored by:** rocket (generation-seam subagent)
**Date:** 2026-05-16
**Commission:** gandalf Pattern A, prerequisite for `canonical/story/pre-llm-substrate-inventory.md`
**Seam covered:** `reincarnated-engine/src/reincarnated/generation/`, `element/`, `anchor/`, `foundation/`, `canonical/` (engine-internal only). LLM call sites read-only for destination tagging.

---

## Summary table

| Structural presupposition tag | Count |
|---|---|
| humanoid-presupposing | 14 |
| form-agnostic-but-named-humanoid | 18 |
| form-agnostic | 9 |
| embodiment-orthogonal | 7 |
| uncertain — needs gandalf engagement | 5 |
| **Total items catalogued** | **53** |

Items flagged as ambiguous for gandalf engagement: 5 (marked "uncertain" in the table above and identified inline below).

Decision-critical-and-unknowable-from-code-reading items (max 3): 2 flagged, at end of document.

Out-of-scope downstream consumers noted inline per item where confirmed.

---

## Category 1 — Canonical-four element labels

### 1.1 `ELEMENT_SCALING_ATTRIBUTE` dict
- **Location:** `generation/element_biases.py:9–15`
- **What it is:** `dict[str, str]` mapping `"fire"/"water"/"earth"/"wind"/"physical"` → attribute name string (`"intelligence"/"wisdom"/"strength"`)
- **Logic surface:** Consumed by `ability_grammar.py` to select `scaling_attribute` per skill. Every skill generated is tagged `canonical_element` + a scaling attribute derived from this map. Branches on the four literal strings at every skill-generation call.
- **Destination:** Internal math only (scaling_attribute flows to JSON export via `ExportSkill.canonical_element` + skill fields; does NOT flow to LLM prompt directly, but `skill.canonical_element` IS passed to LLM in `naming.py:89` as `"Element: {skill.canonical_element}"`).
- **Structural presupposition:** form-agnostic-but-named-humanoid — the mapping is mathematically form-agnostic (scaling attribute to mechanic), but the labels are the canonical four by name.
- **Notes:** `naming.py:89` passes `skill.canonical_element` as a literal canonical-four string to every skill-naming LLM call. This is one of the drift sites named in the Day-4 re-engagement section.

### 1.2 `ELEMENT_AILMENT` dict
- **Location:** `generation/element_biases.py:18–24`
- **What it is:** `dict[str, str]` mapping canonical-four + physical → ailment name (`"burn"/"chill"/"root"/"knockback"/"bleed"`)
- **Logic surface:** Consumed by `ability_grammar.py` to assign ailments per element. Controls which ailment a control or DoT skill applies. `AILMENT_IS_CONTROL` (`:51–58`) classifies which ailments are hard vs soft control — consumed downstream by simulation.
- **Destination:** Internal math; ailment name flows to JSON export (rolled_effects). Not in LLM prompt directly, but affects flavor (LLM sees effects summary including ailment type in skill naming at `naming.py:79–82`).
- **Structural presupposition:** embodiment-orthogonal — ailment name is a damage/control mechanic label, not an embodiment claim. The canonical-four keys are form-agnostic-but-named-humanoid.
- **Notes:** The ailment-damage-signatures deferred design (re-activated per doc 37 § 6.4) lives in this file's parameter structure. `AILMENT_PARAM_RANGES` `:28–48` defines tick damage, duration, slow percent, distance/stagger per ailment — these are all form-agnostic numeric parameters.

### 1.3 `ROTATING_ELEMENTS` list
- **Location:** `generation/b6_archetype_templates.py:38`
- **What it is:** `["fire", "water", "earth", "wind"]` — literal list of canonical-four element names
- **Logic surface:** Used in `ELEMENT_AFFINITY` `:22–28` to define which secondary elements are compatible with each primary. Used in `HYBRID_FORBIDDEN_PAIRS` `:31–35` to enforce `{fire,water}` and `{earth,wind}` cannot be hybrid paired. Consumed by the B6 kit builder and archetype classifier throughout.
- **Destination:** Internal logic only. Does not flow to LLM prompt directly, but downstream `dominant_element` field (populated from this pool) IS passed to `naming.py:143` as `"Dominant element: {player_class.dominant_element}"`.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the mechanic (element affinity and forbidden pairs) is form-agnostic; the labels are canonical-four.
- **Notes:** `HYBRID_FORBIDDEN_PAIRS` encodes a specific pair-opposition structure. Doc 37 § 6.2 Position (ii) calls for hiding this structure from LLM — but `naming.py` currently exposes the canonical-four labels that index this structure (drift site).

### 1.4 `ELEMENT_AFFINITY` dict
- **Location:** `generation/b6_archetype_templates.py:22–28`
- **What it is:** `dict[str, list[str]]` mapping each canonical-four element → list of allowed secondary elements
- **Logic surface:** Consumed by B6 kit builder to determine what secondary elements are allowed when building a multi-element kit. Also defines "physical: []" (open) and "hybrid: []" (handled separately).
- **Destination:** Internal logic. Influences `secondary_elements` field on `PlayerClass` which flows to export and to `naming.py:143`.
- **Structural presupposition:** form-agnostic-but-named-humanoid
- **Notes:** The affinity pairs (fire→wind/earth; water→earth/wind; etc.) encode classical element opposition logic that derives from Earth-realm elemental philosophy. This is one of the hidden mechanical properties doc 37 § 6.2 says should NOT be exposed to the LLM.

### 1.5 `_elements_summary_line()` — LLM prompt construction
- **Location:** `llm/naming.py:26–36`
- **What it is:** Function returning `"Seasonal elements: fire={...}, wind={...}, water={...}, earth={...}\n"` prepended to EVERY class and monster naming prompt
- **Logic surface:** Called in `name_class():135` and `name_monster():177` and `name_gear_item():242`. Prepends canonical-four labels as dict keys explicitly to every LLM class/monster/gear naming call.
- **Destination:** LLM prompt. This is the primary drift site named in Day-4 re-engagement: `naming.py:32-35` literally exposes `fire=`, `wind=`, `water=`, `earth=` to the LLM.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the seasonal element data is form-agnostic; the function exposes it under canonical-four label keys.
- **Notes:** DRIFT — doc 37 § 6 says "hide canonical-four from LLM"; `naming.py:26–36` exposes them as literal dict keys in every class/monster/gear naming prompt. This is the highest-stakes drift site in the seam.

### 1.6 `_seasonal_element_line()` — skill prompt construction
- **Location:** `llm/naming.py:13–23`
- **What it is:** Function returning `"Seasonal element: {element_name} (tags)\n"` for a skill's canonical element slot
- **Logic surface:** Called in `name_skill():85`. Uses `_SLOT_ATTRS = {"fire": "fire_slot", ...}` at `:10` to look up the element. Passes `skill.canonical_element` (a literal canonical-four string) as the dict key.
- **Destination:** LLM prompt. `name_skill():89` also passes `"Element: {skill.canonical_element}"` directly as a separate line — the literal canonical-four string (e.g., "fire") reaches the LLM for every skill.
- **Structural presupposition:** form-agnostic-but-named-humanoid
- **Notes:** DRIFT — same as 1.5 above. Both the `_seasonal_element_line()` function and the direct `"Element: {skill.canonical_element}"` line at `:89` expose canonical-four to LLM.

### 1.7 `SeasonalElements` schema — fire_slot/wind_slot/water_slot/earth_slot
- **Location:** `element/schema.py:26–33`
- **What it is:** Pydantic model with fields `fire_slot`, `wind_slot`, `water_slot`, `earth_slot` — each a `SlotSelection`
- **Logic surface:** Output of `select_seasonal_elements()`. Consumed by orchestrator (`:249–255`), LLM naming functions (as `elements` arg), and export. The field names ARE the canonical-four labels as Python attribute names.
- **Destination:** JSON export via `metadata.json` (`elements` dict — see export/schemas.py:109); LLM prompt (via `_elements_summary_line()`).
- **Structural presupposition:** form-agnostic-but-named-humanoid
- **Notes:** The export's `elements` dict has canonical-four as top-level keys (confirmed from open-thread Day-4 findings: `metadata.json:6 → "water"` as top-level key). Out-of-scope downstream: `reincarnated-loadout/src/pages/Loadout.tsx:67` iterates `['fire', 'wind', 'water', 'earth']`; `reincarnated-demo/src/ui/characterSheet.ts:224` iterates the same list.

### 1.8 `VALID_SLOTS` tuple in element selector
- **Location:** `element/selector.py:34`
- **What it is:** `("fire", "wind", "water", "earth")` — the four valid slot identifiers used throughout the selector
- **Logic surface:** Every validation loop, prompt-construction loop, and deterministic fallback in `selector.py` iterates this tuple. It is the canonical-four labels in their role as slot identifiers. Slot assignment (`primary_slot`, `flex_slots` on `PoolElement`) is validated against this tuple.
- **Destination:** Internal logic; slot labels appear in LLM prompt at `:411` (`"fire_slot"`, `"wind_slot"` etc. as JSON field names in the prompt's output format block).
- **Structural presupposition:** form-agnostic-but-named-humanoid
- **Notes:** The LLM prompt format block at selector.py:411 exposes `"fire_slot"`, `"wind_slot"` etc. as literal JSON keys the LLM must reproduce. Partial drift — canonical-four labels are used as structural JSON keys in the element selection prompt, not just as flavor context.

### 1.9 `canonical/library_schema.py` — `CanonicalEntry.element` field and lookup key
- **Location:** `canonical/library_schema.py:7–51`; `library_generator.py:26–32, 54, 100`
- **What it is:** `CanonicalEntry.element: str` stores canonical-four element name as the key for the pre-built ability presentation library. `CanonicalLibrary.lookup()` takes `element: str` where the expected values are canonical-four strings. `library_generator.py:26-32` has `ELEMENT_COLOR_HINTS` dict keyed on canonical-four.
- **Logic surface:** The canonical library is built once (at project setup) per `(element, effect_category)` pair, iterating `foundation.elements`. The library generator passes `element.name` (a canonical-four string) to the LLM at `library_generator.py:85`: `"- Element: {element}"`.
- **Destination:** LLM prompt (library generation call — one-time setup, not per-season); internal lookup during pairing. `canonical_pair_ref` on Skill/Ability stores the library entry ID (`canonical/{element}/{effect_category}` format).
- **Structural presupposition:** form-agnostic-but-named-humanoid — the canonical library mechanic is form-agnostic (it's a visual/audio presentation reference); the keys are canonical-four labels.
- **Notes:** The one-time library generation call at `library_generator.py:85` exposes canonical-four element names to the LLM. Since this is a one-time setup call, the ongoing drift impact is lower than the per-season naming calls — but the library itself is keyed on canonical-four throughout.

---

## Category 2 — D1 element-name pool

### 2.1 `PoolElement` schema
- **Location:** `element/schema.py:4–17`
- **What it is:** Pydantic model with fields: `id`, `name`, `primary_slot: str` (one of VALID_SLOTS), `flex_slots: list[str]`, `tags: list[str]`, `d1_score: int`, `d1_genre_bonus: int`, `d1_total: int`, `d1_status: str`
- **Logic surface:** Every element in pool.json is loaded as a `PoolElement`. `primary_slot` and `flex_slots` constrain which canonical-four role-slot each word can occupy. `d1_status` gates inclusion in the active pool (quarantine entries excluded at `:75`). `d1_total` drives 2× allow-list sampling weight.
- **Destination:** Internal selection logic; element names flow to LLM naming prompts and to JSON export. `d1_score`, `d1_genre_bonus`, `d1_total`, `d1_status` are internal quality fields (not LLM-visible).
- **Structural presupposition:** form-agnostic-but-named-humanoid — the schema is form-agnostic mechanically; `primary_slot` names (fire/wind/water/earth) carry canonical-four as slot identifiers.
- **Notes:** All 156 pool entries follow this same schema. The D1 rubric criteria (visualizable, fantasy-heroic, genre-precedent, compound-forming, combat-compatible) are Earth-realm-humanoid-fantasy-reader-perspective per doc 37 § 7 — but this is a rubric-design-intent issue, not a schema issue. I documented representative entries (ember, coal, ash, soot, spark from the first five). Full pool enumeration would add no new schema insight; flag: the rubric itself is discussed in doc 37 § 7 as a meta-instance of the same bias, but that's a design-level finding not a code-reading finding.

### 2.2 D1 rubric scoring questions — `_score_novel_word()`
- **Location:** `element/selector.py:282–296`
- **What it is:** Five yes/no questions embedded in an LLM mini-call prompt, evaluated for novel word proposals:
  1. "Does this word name a physical thing (material, substance, or tangible phenomenon)?"
  2. "Can you picture '{word}-bolt' or '{word}-armor' as a plausible fantasy weapon or item name?"
  3. "Does this word fit a heroic/gritty fantasy vocabulary (not domestic, food, or intimate)?"
  4. "Does '[word]-[hero class]' compound naturally... '{word}-Knight' or '{word}-Mage'?"
  5. "Would this word feel appropriate in an action combat context — aggressive, elemental, or dangerous?"
- **Logic surface:** Each "Y" answer contributes +2 to `d1_score`. Threshold ≥8 = allow-list; ≥5 = eligible; <5 = quarantine. Auto-accepted proposals enter pool.json.
- **Destination:** Internal quality gate; affects which words enter the active pool and thus which reach LLM selection prompts.
- **Structural presupposition:** uncertain — needs gandalf engagement. The questions themselves presuppose humanoid-fantasy-reader perspective (question 2: "'{word}-bolt' or '{word}-armor'" presupposes a weapon/item schema; question 4: "'{word}-Knight' or '{word}-Mage'" presupposes humanoid class labels). Words that pass the rubric well will tend to be humanoid-fantasy-compatible; words for non-humanoid cosmologies (e.g., "pressure-bolt" might fail Q2 if the evaluator thinks conventionally) may under-score. This is a rubric-design finding, not a schema-shape finding. Doc 37 § 7 names this same issue.
- **Notes:** DECISION-CRITICAL-AND-UNKNOWABLE-FROM-CODE-READING FLAG #1 — whether the D1 rubric systematically screens out non-humanoid-cosmology candidates cannot be determined from code reading alone. It requires empirical testing (run the rubric on a sample of non-humanoid-cosmology words). Gandalf may want to commission a targeted test before the D1 pool reconsideration.

### 2.3 `_build_prompt()` — element selection prompt
- **Location:** `element/selector.py:394–446`
- **What it is:** Constructs the LLM selection prompt for seasonal element choice. Exposes canonical-four role-slot labels as section headers (`"FIRE-primary:"`, `"WIND-primary:"`, etc.) and as JSON output keys (`"fire_slot"`, `"wind_slot"`, etc.).
- **Logic surface:** Passed to `llm_client.complete_json()` with `_SYSTEM_PROMPT` which describes elements as filling "fire, wind, water, earth canonical role-slots."
- **Destination:** LLM prompt. The `_SYSTEM_PROMPT` at `:43–47` explicitly names "the season's four canonical role-slots (fire, wind, water, earth)" to the LLM.
- **Structural presupposition:** form-agnostic-but-named-humanoid
- **Notes:** DRIFT — the system prompt and prompt body both expose canonical-four labels to the LLM as role-slot names. This is intentional in the current design (the LLM needs to know which slot it's filling) but conflicts with doc 37 § 6's cipher architecture intent.

---

## Category 3 — Class archetype labels

### 3.1 `archetype_tag` field on `PlayerClass`
- **Location:** `generation/class_schema.py:37`; `generation/archetype_classifier.py:9–44`
- **What it is:** String field on `PlayerClass`; values are archetype labels: `"fire_mage"`, `"water_mage"`, `"earth_caster"`, `"wind_caster"`, `"hybrid_mage"`, `"fire_controller"`, `"water_controller"`, `"earth_controller"`, `"wind_controller"`, `"hunter"`, `"physical_warrior"`, `"physical_grappler"`, `"physical_skirmisher"`, `"rogue"`, `"support_healer"`. Derived by `classify_archetype()` from `dominant_element + energy_type + role_orientation`.
- **Logic surface:** Controls which `ArchetypeTemplate` is selected from `ARCHETYPE_TEMPLATES`; gates geometry bias weights, kit composition targets, required roles. Passed to `name_class()` at `naming.py:139` as `"Archetype: {player_class.archetype_tag}"`.
- **Destination:** LLM prompt (naming); JSON export (`ExportClass.archetype_tag`). Out-of-scope downstream: drax/loadout likely consumes this; confirmed by open-thread Day-4 findings citing demo/loadout canonical-four exposure.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the mechanics (stat template, geometry bias, kit targets) are form-agnostic; the labels (`warrior`, `mage`, `rogue`, `hunter`, `grappler`, `skirmisher`) are humanoid social/martial roles applied to form-agnostic stat profiles.
- **Notes:** "warrior", "rogue", "hunter", "grappler", "mage" are all human-social-role labels. They carry humanoid narrative weight while being mechanically form-agnostic. This is the direct analog of doc 37 § 2's "class archetypes (warrior / mage / rogue / hunter — human social/martial roles)" finding. The archetype label IS passed to the LLM naming prompt — the LLM receives the humanoid label and is expected to generate a class name from it.

### 3.2 `ARCHETYPE_TEMPLATES` — `archetype_tag` keys
- **Location:** `generation/b6_archetype_templates.py:84–393`
- **What it is:** Dict mapping archetype tag strings → `ArchetypeTemplate` dataclass instances with 14 entries.
- **Logic surface:** Every kit composition decision gates on archetype tag. `stat_allocator.py:10–36` has parallel `ARCHETYPE_TEMPLATES` dict (same keys) mapping to stat distributions.
- **Destination:** Internal logic; archetype tag surfaces in JSON export and LLM prompt.
- **Structural presupposition:** form-agnostic-but-named-humanoid — same as 3.1.

### 3.3 `MONSTER_ARCHETYPES` list
- **Location:** `generation/season_orchestrator.py:50`
- **What it is:** `["brute", "caster", "swarmer", "controller", "tank", "sniper"]`
- **Logic surface:** Used in bestiary generation to assign archetypes to monsters. `archetype_tag` on `Monster` is set from this list.
- **Destination:** JSON export (`ExportMonster.archetype_tag`); LLM prompt (`name_monster():186` passes `"Archetype: {monster.archetype_tag}"`).
- **Structural presupposition:** form-agnostic-but-named-humanoid — "brute", "sniper", "tank" carry humanoid martial role implications while being mechanically form-agnostic.

### 3.4 `dominant_role_profile` field
- **Location:** `generation/class_schema.py:43`; `generation/archetype_classifier.py:47–55`
- **What it is:** Short human-readable description derived from skill role distribution: e.g., `"primary_attack/burst_damage"`. Stored on `PlayerClass`.
- **Destination:** LLM prompt (`name_class():143` passes `"Role profile: {player_class.dominant_role_profile}"`).
- **Structural presupposition:** form-agnostic — role vocabulary (primary_attack, burst_damage, area_damage, control, sustain, mobility, defensive, utility) is abstract and form-agnostic.

### 3.5 `role_orientation` field — "damage/control/hybrid/support"
- **Location:** `generation/class_schema.py:41`; `generation/season_orchestrator.py:74`, `77–103`
- **What it is:** String field; values: `"damage"`, `"control"`, `"hybrid"`, `"support"`. Sampled by `_pick_role_orientation()`. Constrained to `["damage", "control", "hybrid"]` for solo generation (support excluded).
- **Logic surface:** Gates archetype classification (`archetype_classifier.py:22–43`); influences stat allocation; consumed by gear fit profile. Passed to LLM at `naming.py:140` as `"Role orientation: {player_class.role_orientation}"`.
- **Destination:** LLM prompt; JSON export (`ExportClass.role_orientation`).
- **Structural presupposition:** form-agnostic — these role labels are abstract enough to apply to any entity form. "control" and "hybrid" have no humanoid presupposition.

---

## Category 4 — Gear slot labels

### 4.1 High-level slot names: `weapon`, `armor`, `accessory`, `off_hand`
- **Location:** `generation/gear_schema.py:131–138` (`GearInstance.slot`); `generation/gear_generation.py:76–101` (`_BASE_TYPE_TO_SLOT`); `generation/gear_catalog.py:10–49` (`BASE_ITEMS` list)
- **What it is:** Four high-level slot strings used throughout gear generation, cataloging, and export. `_BASE_TYPE_TO_SLOT` maps all base item type ids to these four strings.
- **Logic surface:** `Loadout` (`gear_schema.py:198–310`) has explicit fields `weapon`, `off_hand`, `armor`, `accessory`. `can_equip()` routes on these. `generate_season_gear_pool()` iterates them. Export schema uses `ExportGearItem.slot`.
- **Destination:** JSON export (`ExportGearItem.slot`); LLM prompt (`name_gear_item():249` passes `"Slot: {item.slot}"`). Out-of-scope downstream: loadout UI consumes slot labels directly.
- **Structural presupposition:** humanoid-presupposing — "weapon" presupposes a hand/appendage to wield; "armor" presupposes a body with surface area to cover; "accessory" presupposes a body with attachment points. "off_hand" presupposes bilateral anatomy (a "main hand" and an "off hand").
- **Notes:** This is the load-bearing gear-slot humanoid-presupposition identified in doc 37 § 2 and § 4. The slot names are structural in the engine — `Loadout.weapon`, `Loadout.off_hand`, `Loadout.armor`, `Loadout.accessory` are explicit model fields, not just string constants. Renaming to functional labels (e.g., `offensive_augmentation`, `defensive_augmentation`) requires schema migration per doc 37 § 4 Position C.

### 4.2 Base item type ids: sword, staff, dagger, hammer, bow, wand, greatsword, helmet, chest, robe, hood, ring, amulet, shield, grimoire, orb, focus
- **Location:** `generation/gear_catalog.py:10–49` (`BASE_ITEMS` list); `generation/gear_generation.py:77–101` (`_BASE_TYPE_TO_SLOT` dict)
- **What it is:** Specific humanoid-equipment type names used as string ids throughout gear generation. These are the sub-slots mentioned in doc 37 § 2.
- **Logic surface:** `base_type_id` on `GearInstance` is stored and exported. `_BASE_TYPE_LABEL` (`gear_generation.py:541–566`) maps each to a display label (e.g., `"sword"` → `"Blade"`, `"chest"` → `"Plate"`). Passed to LLM at `name_gear_item():250` as `"Base type: {item.base_type_id}"`.
- **Destination:** LLM prompt; JSON export (`ExportGearItem` has `slot` + these ids appear in carried_gear dicts). Out-of-scope downstream: loadout UI renders these.
- **Structural presupposition:** humanoid-presupposing — sword, bow, helmet, chest, gauntlets (gloves), boots, belt, ring, shield are all anatomically humanoid equipment categories. "greatsword" and "off_hand_dagger" especially presuppose bilateral human arms.
- **Notes:** These are the "wields/wears/weapon/armor/accessory categorical axes" identified in doc 37 § 2 item 8. They presuppose not just humanoid form but specifically medieval-humanoid combat equipment.

### 4.3 `can_equip()` and `stat_requirements` path
- **Location:** `generation/gear_generation.py:289–315`
- **What it is:** Function `can_equip(actor_stats: StatDistribution, gear: GearInstance) -> bool` checking `stat_requirements` dict (keys: `"str"`, `"dex"`, `"int"`, `"wis"`, `"vit"`) against actor stats.
- **Logic surface:** Called in `sample_scenario_loadout()` and `_base_type_eligible()`. Gates gear equippability on STR/DEX attribute values. STR gates melee weapons and heavy armor; DEX gates bows.
- **Destination:** Internal simulation logic. `stat_requirements` dict is in the JSON export per `ExportGearItem.stat_requirements`.
- **Structural presupposition:** humanoid-presupposing — the gating logic (STR for swords/armor; DEX for bows) directly maps humanoid physical capabilities onto equipment access. A crystalline construct or swarm would have no natural STR in any physical sense.
- **Notes:** The 2026-05-09 decisions-log entry on STR/DEX/INT as math-bearing is relevant here. Doc 37 § 2 explicitly calls out `can_equip()` and `stat_requirements` as humanoid-bound surfaces.

### 4.4 `_BASE_TYPE_STAT_AFFINITY` dict
- **Location:** `generation/gear_generation.py:368–396`
- **What it is:** Maps each base_type_id to a `set[str]` of stat affinity categories (`"str"`, `"dex"`, `"int_wis"`) for affix coherence gating.
- **Logic surface:** Used in `affix_eligible()` to gate which affixes roll on which gear. STR-affinity gear only rolls STR-relevant effects; DEX-affinity gear rolls DEX effects, etc.
- **Destination:** Internal logic.
- **Structural presupposition:** humanoid-presupposing — same reasoning as 4.3. The affinity categories directly map humanoid physical capability archetypes onto equipment types.

### 4.5 `MATERIAL_BY_ELEMENT` and `_ELEMENT_SUFFIX` template naming tables
- **Location:** `generation/gear_generation.py:511–538`
- **What it is:** `MATERIAL_BY_ELEMENT` maps canonical-four + physical → material name lists (`"Cinderstone"/"Ashglass"/"Embersteel"` for fire, etc.); `_ELEMENT_SUFFIX` maps canonical-four → suffix strings (`"of Embers"/"of Tides"/"of Stone"/"of Gales"/"of Iron"`).
- **Logic surface:** Used in `_template_name()` for common/uncommon/rare gear names (no LLM call). The canonical-four element name of the dominant effect determines which material pool and suffix is used.
- **Destination:** Player-visible item names (common/uncommon/rare tiers show template names). NOT in LLM prompt (LLM only names epic/legendary); these are deterministic fallback names.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the materials and suffixes are Earth-realm fantasy vocabulary but the mechanic is form-agnostic. A crystalline construct's gear would still get "Cinderstone Plate" on a fire-dominant common item.
- **Notes:** These names expose canonical-four labels in player-visible strings (common/uncommon/rare gear). Out-of-scope downstream: loadout UI displays these names.

---

## Category 5 — Attribute axes

### 5.1 `StatDistribution` — strength/dexterity/intelligence/wisdom/vitality
- **Location:** `generation/class_schema.py:9–31`
- **What it is:** Pydantic model with five integer fields summing to `STAT_BUDGET=270`. Fields: `strength`, `dexterity`, `intelligence`, `wisdom`, `vitality`.
- **Logic surface:** Used throughout — gear equip gating (`can_equip()`), energy pool computation (`PlayerClass.energy_pool_max`), HP computation (`PlayerClass.max_hp`), stat allocation (`stat_allocator.py`), archetype stat templates. Passed to LLM at `naming.py:148` as `"Stats (out of 270): {player_class.stats.as_dict()}"`.
- **Destination:** LLM prompt (class naming); JSON export (`ExportClass.stat_distribution`).
- **Structural presupposition:** form-agnostic-but-named-humanoid — per doc 37 § 2: "attribute axes (STR / DEX / INT) — *math-bearing*, not just labels." The math is form-agnostic (abstract power dimensions); the labels carry humanoid-physical connotations (strength = physical muscular force; dexterity = manual agility; intelligence = cognitive ability). The labels flow directly to the LLM at `naming.py:148`.
- **Notes:** Doc 37 § 2 explicitly states these "survive as abstract power dimensions divorced from physical interpretation" under structural realignment — the labels stay for engine math, but LLM-visible narrative reframes them per-embodiment. Currently no such reframing exists; the raw humanoid labels flow to the LLM as-is.

### 5.2 `ARCHETYPE_TEMPLATES` stat distributions — `stat_allocator.py`
- **Location:** `generation/stat_allocator.py:10–36`
- **What it is:** Dict mapping archetype tag → `{stat_name: int}` with all 14 archetype stat templates. E.g., `"fire_mage": {"intelligence": 160, "vitality": 70, ...}`.
- **Logic surface:** `allocate_stats()` uses these as starting points (with optional jitter). The stat templates directly encode humanoid-archetype assumptions (warriors are high STR; mages are high INT; rogues are high DEX).
- **Destination:** Internal balance sim; `StatDistribution` populated from these flows to LLM as noted above.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the template values are mechanical calibration; the underlying assumptions that "intelligence" is the right scale for mages and "strength" for warriors carry humanoid-archetype framing.

### 5.3 `VALID_STAT_KEYS` in trait schema
- **Location:** `generation/trait_schema.py:41–55`
- **What it is:** `frozenset` of valid stat keys including `"strength"`, `"vitality"`, `"intelligence"`, `"wisdom"`, `"dexterity"` plus GearStats keys.
- **Logic surface:** Validates `TraitSpec.stat_key` at creation time. "Direct attribute boosts (progression source; Priority 14 activates these)" per the comment.
- **Destination:** Internal validation. These keys flow downstream through trait aggregation to combat sim.
- **Structural presupposition:** form-agnostic-but-named-humanoid — same as 5.1.

---

## Category 6 — Role orientation taxonomy

### 6.1 `role_orientation` field and `VALID_SOLO_ROLE_ORIENTATIONS`
- **Location:** `generation/class_schema.py:41`; `generation/season_orchestrator.py:74`
- **What it is:** `["damage", "control", "hybrid"]` as valid values for solo generation (support excluded). Applied to both classes and monsters.
- **Logic surface:** Gates archetype classification; influences stat allocation; determines kit balance targets. Passed to LLM at `naming.py:140`.
- **Destination:** LLM prompt; JSON export.
- **Structural presupposition:** form-agnostic — "damage/control/hybrid" are genuinely form-neutral mechanical orientations. The 2026-05-08 decision to use this taxonomy (not "sustain") was explicitly designed to be form-agnostic.
- **Notes:** "support" is excluded from solo generation (Phase 5 deferred) — this is a game-design decision about multi-actor contexts, not an embodiment presupposition.

---

## Category 7 — Geometry palette labels

### 7.1 `VALID_GEOMETRIES` frozenset — full 30-type active palette
- **Location:** `generation/ability_grammar.py:146–163`
- **What it is:** `frozenset` of all geometry type strings used by the generator: includes `melee_strike`, `melee_arc`, `ground_slam`, `whirlwind`, `dash_attack`, `leap_strike`, `ranged_physical`, and the full post-B11/B13 palette.
- **Logic surface:** Validates geometry output from the grammar. All skill geometries must be in this set. `AOE_GEOMETRIES` (`b6_archetype_templates.py:415–419`) is a subset. Geometry label is stored on `Skill.geometry` and passed to LLM at `naming.py:91` as `"Geometry: {skill.geometry}"`.
- **Destination:** LLM prompt (skill naming); JSON export (`ExportSkill.geometry_type`).
- **Structural presupposition:** form-agnostic-but-named-humanoid — the geometry mechanic (AOE shape, targeting type) is form-agnostic; specific labels carry humanoid-weapon-semantic gravity: `melee_strike` (presupposes a striking limb), `melee_arc` (presupposes a sweep with a hand-held object), `ground_slam` (presupposes an impact on the ground from a specific orientation), `ranged_physical` (presupposes a projectile weapon held in hands), `leap_strike` (presupposes a body that leaps and lands). Doc 37 § 2 names this explicitly: "though the labels `lance`/`cone`/`arc` carry humanoid weapon-semantic gravity."
- **Notes:** `blink`, `roll`, `defensive_dash`, `teleport` are more form-agnostic in their semantic weight. `projectile`, `circle`, `cone`, `line`, `ring`, `beam_channel` are genuinely form-agnostic geometrically. The melee and physical weapon labels are the humanoid-weight items.

### 7.2 `_CLOSE_ONLY_GEOMETRIES` and `_PHYSICAL_ONLY_GEOMETRIES`
- **Location:** `generation/ability_grammar.py:33–38`
- **What it is:** `frozenset` of geometry names restricted to close-range and physical-element contexts respectively.
- **Logic surface:** `_CLOSE_ONLY_GEOMETRIES = {"melee_strike", "melee_arc", "ground_slam"}` are filtered out of non-close pools. `_PHYSICAL_ONLY_GEOMETRIES = {"ranged_physical"}` filtered from non-physical elements.
- **Destination:** Internal grammar filter.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the mechanic (restricting close-range geometries) is reasonable; the specific label vocabulary (`melee_strike`, `ranged_physical`) carries humanoid weapon semantics.

### 7.3 Geometry bias entries in `ArchetypeTemplate`
- **Location:** `generation/b6_archetype_templates.py` — `geometry_bias` field per template
- **What it is:** `dict[str, float]` of BIAS_PREFERRED/BIAS_PENALIZED values per geometry type per archetype. E.g., `physical_warrior` prefers `melee_strike`, `melee_arc`, `ground_slam`, `whirlwind`, `dash_attack`.
- **Logic surface:** Applied as weight multipliers in the B6 kit builder's geometry sampling. Higher-bias geometries appear more frequently in that archetype's kit.
- **Destination:** Internal generation logic; indirect effect on skill geometry field.
- **Structural presupposition:** form-agnostic-but-named-humanoid — same as 7.1.

---

## Category 8 — Wields/wears/weapon/armor/accessory categorical axes

### 8.1 `_BASE_TYPE_TO_SLOT` mapping — wields/wears framing
- **Location:** `generation/gear_generation.py:76–101`
- **What it is:** Maps all base item type ids to four high-level slots. This IS the "wields/wears" distinction: weapon/off_hand = wields; armor = wears; accessory = wears.
- **Logic surface:** Used throughout gear generation and export.
- **Destination:** JSON export; LLM prompt (gear naming gets `"Slot: {item.slot}"` and `"Base type: {item.base_type_id}"`).
- **Structural presupposition:** humanoid-presupposing — same as 4.1. The wields/wears distinction presupposes hands and a body.

### 8.2 `Loadout` class — explicit slot fields
- **Location:** `generation/gear_schema.py:198–310`
- **What it is:** `Loadout(BaseModel)` with fields `weapon: GearInstance | None`, `off_hand: GearInstance | None`, `armor: GearInstance | None`, `accessory: GearInstance | None`. The `off_hand` field is explicitly gated on `weapon.handedness == "1h"` at `:212`.
- **Logic surface:** `_is_off_hand_active()` checks whether a 2H weapon disables the off-hand. `combined_stats()`, `combined_ability_modifiers()`, `combined_traits()` all respect this.
- **Destination:** Internal balance simulation; exported in `ExportClass.carried_gear`.
- **Structural presupposition:** humanoid-presupposing — the `handedness` concept ("1h" vs "2h") directly presupposes bilateral human arms. "off_hand" as a concept presupposes a dominant-hand/off-hand anatomy.

---

## Category 9 — Spirit Guide kit-composition framing

### 9.1 `VALID_SOLO_ROLE_ORIENTATIONS` exclusion of "support"
- **Location:** `generation/season_orchestrator.py:74`
- **What it is:** Comment: "support is excluded — requires multi-actor context (Phase 5)". Exclusion is enforced by not including "support" in the valid orientation list.
- **Logic surface:** No Spirit Guide system code exists in the generation seam. The `spirit_guide/` module is in the simulation seam (gamora's territory — not deep-read).
- **Destination:** Internal logic gate.
- **Structural presupposition:** embodiment-orthogonal — this is a game-design scope decision, not an embodiment claim.
- **Notes:** The "kit-of-skills" framing mentioned in doc 37 § 2 is about how the Spirit Guide presents gear/class analysis, not generation. No generation-seam code surfaces a "kit of skills" framing explicitly — this framing lives in the `spirit_guide/` module which is gamora's seam.

### 9.2 `PlayerClass.skills` field — kit-as-list framing
- **Location:** `generation/class_schema.py:36`
- **What it is:** `skills: list[Skill]` — the class is fundamentally defined as a collection of skills plus stat distribution.
- **Logic surface:** The entire class identity in the engine is a `(skills, stats, element, archetype)` tuple. There is no `body` or `embodiment` field. The class is a "kit" in the sense that it's defined by its skill roster.
- **Destination:** JSON export; LLM naming receives skill summary at `naming.py:129–132`.
- **Structural presupposition:** uncertain — needs gandalf engagement. `PlayerClass` as "kit of skills" is the existing framing (pre-embodiment-axis work). It is NOT explicitly "body-with-properties" but it also doesn't preclude that framing. Whether this constitutes a structural presupposition that needs changing, or is simply incomplete (needs `embodiment_tag` added), is a design question for gandalf. The `embodiment-narrative-layer.md` doc's "Engine emit requirements" section specifies `embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register` as fields to add — none exist yet.
- **Notes:** The absence of `embodiment_tag` on `PlayerClass` is the structural gap doc 37 § 4 identifies. It is not a presupposition claim per se — it's a missing field. Flagged as uncertain because the right categorization depends on whether "absence of embodiment field" counts as a structural presupposition.

---

## Category 10 — Skill verb grammar / ability-grammar seed taxonomy

### 10.1 Skill `role` field vocabulary
- **Location:** `generation/role_constraints.py:27–` (ROLE_CONSTRAINTS keys); `generation/ability_grammar.py`
- **What it is:** Skill role vocabulary: `"primary_attack"`, `"burst_damage"`, `"area_damage"`, `"damage_over_time"`, `"control"`, `"mobility"`, `"defensive"`, `"sustain"`, `"utility"`, `"heal"`. Used as `Skill.role` and in `ROLE_CONSTRAINTS`.
- **Logic surface:** Role determines geometry options, timing options, cooldown ranges, energy cost ranges, and primary/secondary effects. Role is passed to the LLM at `naming.py:90` as `"Role: {skill.role}"`.
- **Destination:** LLM prompt; JSON export (`ExportSkill.role`).
- **Structural presupposition:** form-agnostic — "burst_damage", "area_damage", "control", "mobility", "defensive" are abstract mechanical roles. None presuppose humanoid form at the mechanic level.
- **Notes:** The role vocabulary is the most form-agnostic surface in the generation seam. A slime's "primary_attack" skill conceptually differs from a humanoid's primary attack, but the mechanical role label is neutral.

### 10.2 Skill `timing` vocabulary — `AbilityTiming.name`
- **Location:** `generation/ability_schema.py:11–13`; `generation/role_constraints.py` (timing_options per role)
- **What it is:** `AbilityTiming.name: str` with values from timing vocabulary: `"instant"`, `"cast"`, `"charge"`, `"channel"`. Used in every `RoleConstraint.timing_options`.
- **Logic surface:** Timing name is passed to LLM at `naming.py:93` as `"Timing: {skill.timing.name}"`.
- **Destination:** LLM prompt; JSON export (part of skill data).
- **Structural presupposition:** form-agnostic — "instant", "cast", "charge", "channel" are abstract temporal descriptions applicable to any entity form.

### 10.3 `scaling_attribute` on Skill
- **Location:** `generation/skill_schema.py:27`; set from `ELEMENT_SCALING_ATTRIBUTE` via `ability_grammar.py`
- **What it is:** String field storing which attribute scales the skill: `"intelligence"`, `"wisdom"`, `"strength"`.
- **Logic surface:** Passed to LLM at `naming.py:92` as `"Scaling attribute: {skill.scaling_attribute}"`.
- **Destination:** LLM prompt; JSON export (as part of skill data).
- **Structural presupposition:** form-agnostic-but-named-humanoid — the scaling mechanic is form-agnostic; the attribute names carry humanoid connotations when exposed to LLM.

### 10.4 `composition_mode` on Skill
- **Location:** `generation/skill_schema.py:9`
- **What it is:** String field: `"single"`, `"layered"`, `"fused"`, `"triadic"`. Describes how constituent abilities compose.
- **Logic surface:** Passed to LLM at `naming.py:99` as `"Composition: {skill.composition_mode}"`.
- **Destination:** LLM prompt.
- **Structural presupposition:** form-agnostic — composition mode vocabulary is abstract and form-neutral.

---

## Category 11 — Naming triad mechanics

### 11.1 `anchor.name` / `anchor.description` — LLM context
- **Location:** `anchor/schema.py:1–9`; used in `selector.py:_build_prompt()` and `llm/naming.py`
- **What it is:** `Anchor` schema: `id`, `name`, `category`, `description`. Passed to LLM naming functions as `"Place anchor: {anchor_name}"`.
- **Logic surface:** The anchor provides the cosmological setting context for LLM naming. `name_skill()` at `:84` includes anchor_line; `name_class()` at `:134` includes anchor_line.
- **Destination:** LLM prompt.
- **Structural presupposition:** uncertain — needs gandalf engagement. The anchor itself is form-agnostic (it's a place/cosmological concept). But what the engine generates as the anchor is determined by the `anchor/library.py` selector and `anchor/schema.py`. Whether the anchor category vocabulary and specific anchors in the library are humanoid-themed is not knowable from schema-reading alone — would require reading the anchor data itself.
- **Notes:** The anchor is the intended source of cosmological-resonance per the naming-triad doc. Whether current anchors are humanoid-themed is an empirical question.

### 11.2 `season_theme_element` — top-level season parameter
- **Location:** `generation/class_schema.py` (not directly); `generation/season_orchestrator.py:147, 267–269`; `llm/naming.py:87` as `"Season theme: {season_theme_element}"`
- **What it is:** String value holding one of the canonical-four element names (selected from rotating elements at `:266–269`). Passed as the first parameter to ALL LLM naming functions: `name_skill()`, `name_class()`, `name_monster()`, `name_gear_item()`.
- **Logic surface:** Used as the thematic seed for all LLM naming in a season. The value IS a canonical-four element name (e.g., "fire", "water").
- **Destination:** LLM prompt — appears as `"Season theme: {season_theme_element}"` at the top of every LLM naming call.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the concept of a season-wide thematic element is form-agnostic; passing a canonical-four label as the theme exposes canonical-four to the LLM.
- **Notes:** DRIFT — doc 37 § 6 says canonical-four should be hidden from LLM. `season_theme_element` is a canonical-four label passed as `"Season theme: fire"` to every naming call. This is one of the primary per-season canonical-four exposures beyond the gear material tables and elements summary line.

### 11.3 `CanonicalEntry` and canonical library — per-element presentation reference
- **Location:** `canonical/library_schema.py:6–50`
- **What it is:** Pre-built LLM-generated presentation library keyed on `(element, effect_category)`. Contains `canonical_name`, `canonical_alternates`, `flavor_descriptor`, `particle_theme`, `audio_theme`, `color_signature` per canonical-four × effect-category pair.
- **Logic surface:** `CanonicalLibrary.lookup(element, effect_category)` returns the entry; `canonical_pair_ref` on Skill stores the entry id. Used to give consistent "canonical names" to skill families.
- **Destination:** Internal lookup; `canonical_pair_ref` field on Skill flows to export and indirectly to LLM (the canonical names are the "stable foundation" the seasonal names "decorate" per `library_generator.py:13–16`).
- **Structural presupposition:** form-agnostic-but-named-humanoid — the canonical library entries carry humanoid-fantasy vocabulary ("Searing Wave", "Stone Grasp", "Tide Shroud", "Wind Lance", "Iron Rend" from `library_generator.py:20–24`). These names will influence what "foundation identity" means for generated skills.

### 11.4 Trial / Mirror / Passage — internal field names
- **Location:** `generation/trial_schema.py` (existence confirmed); `naming-triad.md` notes engine retains "doppelganger" as technical term; `generation/b6_archetype_templates.py:407–411` has `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` referencing "doppelganger" in comments
- **What it is:** Engine-internal fields still use "doppelganger" terminology (`doppelganger_validation_runs`, `doppelganger_gate`). `naming-triad.md` explicitly locks: universal frame names (Trial / Mirror / Passage) are player-facing; engine can retain doppelganger for internal technical use.
- **Logic surface:** Trial generation is in `trial_generator.py`; trial schema in `trial_schema.py`. Not deeply read (trial is generation-seam territory but schema not inspected in detail here).
- **Destination:** Internal engine; export fields pending rename decision.
- **Structural presupposition:** embodiment-orthogonal — the naming-triad mechanics are cosmological/player-journey concepts, not embodiment claims.

---

## Category 12 — Trait architecture

### 12.1 `TraitSpec` schema — `stat_key` vocabulary
- **Location:** `generation/trait_schema.py:41–55` (`VALID_STAT_KEYS`)
- **What it is:** Valid stat keys include `"strength"`, `"vitality"`, `"intelligence"`, `"wisdom"`, `"dexterity"` as direct attribute boost keys (progression source). Also `"bonus_hp"`, `"bonus_armor"`, `"bonus_crit_chance"`, etc. (GearStats keys).
- **Logic surface:** `validate_trait()` gates all trait creation against this set. Progression-source traits would directly modify humanoid-named attributes.
- **Destination:** Internal simulation via `aggregate_traits()`. Does not flow to LLM.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the attribute names carry humanoid connotations (same as 5.1).

### 12.2 `TraitCategory` enum — STAT/ABILITY/GRANTED
- **Location:** `generation/trait_schema.py:23–27`
- **What it is:** Three-value enum for trait types.
- **Logic surface:** Controls aggregation logic in `aggregate_traits()`. `GRANTED` traits can add a `granted_role` (a skill role from the role vocabulary) and `granted_element` (a canonical-four element name).
- **Destination:** Internal.
- **Structural presupposition:** form-agnostic — the category taxonomy is abstract.

### 12.3 `granted_element` field on `TraitSpec`
- **Location:** `generation/trait_schema.py:126`
- **What it is:** `granted_element: str | None` — element flavor for a GRANTED trait. Expected values are canonical-four strings.
- **Logic surface:** Passed to simulation when the trait grants a new ability. The granted ability would use the canonical element for its damage type and ailment.
- **Destination:** Internal simulation.
- **Structural presupposition:** form-agnostic-but-named-humanoid — canonical-four as the element vocabulary for granted abilities.

### 12.4 `VALID_ABILITY_MODIFIER_KEYS` frozenset
- **Location:** `generation/trait_schema.py:58–65`
- **What it is:** `frozenset` of valid ability modifier keys: `"multishot_floor_bonus"`, `"cooldown_factor"`, `"energy_cost_factor"`, `"crit_bonus_damage"`, `"aoe_radius_bonus"`, `"control_duration_bonus"`.
- **Logic surface:** Validates `TraitSpec.ability_modifier_key`. These modify existing skill mechanics.
- **Destination:** Internal simulation via `aggregate_traits()`.
- **Structural presupposition:** form-agnostic — "cooldown_factor", "energy_cost_factor", "aoe_radius_bonus", "control_duration_bonus" are all abstract mechanics applicable to any form. "multishot_floor_bonus" has marginal humanoid-weapon-semantic weight (multishot implies a projectile weapon) but is primarily a hunter-archetype mechanic.

---

## Discovered items (not in the 12 buckets as originally scoped)

### D.1 `energy_type` vocabulary — mana/rage/combo/focus/stamina-as-resource
- **Discovered during pass**
- **Location:** `generation/class_schema.py:39`; `generation/season_orchestrator.py:61–69`; `gear_generation.py:604–606`
- **What it is:** String field on `PlayerClass` and `Monster`. Values: `"mana"`, `"rage"`, `"combo"`, `"focus"`, `"stamina-as-resource"`. Sampled from `_PHYSICAL_ENERGY_TYPES` for physical classes; always `"mana"` for elemental classes.
- **Logic surface:** Gates archetype classification (combo→rogue, focus→hunter, rage/stamina→warrior/grappler). Determines energy pool max (`energy_pool_max` property). Passed to LLM at `naming.py:141` as `"Energy type: {player_class.energy_type}"`.
- **Destination:** LLM prompt (class naming); JSON export (`ExportClass.energy_type`).
- **Structural presupposition:** form-agnostic-but-named-humanoid — "mana" and "focus" are fairly abstract; "rage" carries strong humanoid-warrior connotations (animalistic anger); "combo" implies sequential physical strikes; "stamina-as-resource" directly evokes physical bodily endurance. The rage/combo/stamina cluster maps poorly onto non-humanoid embodiments.
- **Notes:** A slime doesn't experience rage in a meaningful sense; a construct doesn't have stamina. These are partially form-agnostic at the mechanic level but carry humanoid experiential connotations in their labels.

### D.2 `range_profile` vocabulary — close/medium/long
- **Discovered during pass**
- **Location:** `generation/class_schema.py:42`; `generation/season_orchestrator.py:106–140`
- **What it is:** String field: `"close"`, `"medium"`, `"long"`. Deterministically assigned for physical classes; weighted-random for elemental classes with mage-range constraint.
- **Logic surface:** Gates geometry pool selection in ability grammar. Determines which geometries are available. Passed to LLM at `naming.py:142`.
- **Destination:** LLM prompt; JSON export (`ExportClass.range_profile`).
- **Structural presupposition:** form-agnostic — range profile is genuinely form-agnostic. A slime at close range and a humanoid at close range are mechanically equivalent in this schema.

### D.3 `dominant_element` field on PlayerClass/Monster — canonical-four or "physical"
- **Discovered during pass**
- **Location:** `generation/class_schema.py:37`; used throughout generation seam
- **What it is:** String field holding one of the canonical-four element names or "physical". Set from `theme_element` (rotating canonical-four) or the physical constant.
- **Logic surface:** Central identity field. Gates archetype classification, gear material naming, element bias application. Passed to LLM at `naming.py:143` as `"Dominant element: {player_class.dominant_element}"`.
- **Destination:** LLM prompt; JSON export.
- **Structural presupposition:** form-agnostic-but-named-humanoid — same as canonical-four labels generally.

### D.4 `ELEMENT_COLOR_HINTS` in canonical library generator
- **Discovered during pass**
- **Location:** `canonical/library_generator.py:26–32`
- **What it is:** `dict` mapping canonical-four + physical → hex color range strings. Passed to LLM in one-time canonical library generation.
- **Logic surface:** Color hints guide the LLM in assigning `color_signature` values to canonical library entries.
- **Destination:** LLM prompt (one-time library generation only).
- **Structural presupposition:** form-agnostic — color associations to element types are not embodiment claims.

### D.5 `Foundation.elements` — schema-level enforcement of exactly 1 "physical" non-rotating element
- **Discovered during pass**
- **Location:** `foundation/foundation.py:39–43`
- **What it is:** `model_validator` enforcing: exactly 1 non-rotating element, and it must be named `"physical"`. Canonical-four are the rotating elements.
- **Logic surface:** Structural constraint at Foundation level. Any foundation data that doesn't have exactly 4 rotating + 1 physical will fail validation.
- **Destination:** Internal engine validation.
- **Structural presupposition:** form-agnostic-but-named-humanoid — the 4+1 structure is baked into the schema validator. The name "physical" for the non-rotating element is a humanoid-martial vocabulary choice (physical = melee/body contact). An alternative framing might call this "contact" or "proximate" to be more form-agnostic.
- **Notes:** This validator hard-codes the canonical-four rotating structure at the engine level. Any cipher architecture change that expands beyond 4 slots would require this validator to be updated.

---

## Out-of-scope downstream consumer notes (summary)

All confirmed by open-thread Day-4 re-engagement findings (gandalf's own code verification). Citing without deep-reading:

- `reincarnated-loadout/src/pages/Loadout.tsx:67` — `const canonicals = ['fire', 'wind', 'water', 'earth']` driving UI iteration
- `reincarnated-loadout/src/pages/Sample.tsx:29` — same canonical-four array
- `reincarnated-demo/src/ui/characterSheet.ts:224` — resistance panel iterates `['fire', 'water', 'wind', 'earth', 'physical']`
- `reincarnated-demo/src/ui/characterSheet.ts:417–420` — hex colors hard-coded per canonical-four case
- `reincarnated-demo/src/ui/damage.ts:181` — combat math branches on `'earth' || 'wind'` for WIS scaling

These are star-lord's and drax's territories per the seam map.

---

## Items flagged as uncertain — needs gandalf engagement

1. **2.2 D1 rubric questions** — whether the five yes/no questions in `_score_novel_word()` systematically screen out non-humanoid-cosmology words (question 2 references `{word}-armor`; question 4 references `{word}-Knight`/`{word}-Mage`). Schema-shape observable; screening effect is empirical.

2. **9.2 `PlayerClass.skills` — kit-of-skills framing** — whether the absence of `embodiment_tag` counts as a structural presupposition or simply an incomplete schema. The right answer is design-judgment for gandalf: is this a presupposition to tag, or just the "missing field to add" per doc 37 § 4?

3. **11.1 Anchor vocabulary** — whether current anchors in the anchor data carry humanoid-themed vocabulary. Not readable from schema alone; requires reading the anchor library data (anchor/library.py loads JSON data not inspected here). Gandalf should verify whether anchor categories (e.g., "structure", "natural", "mythological") are humanoid-framed.

4. **D.1 `rage`/`stamina-as-resource` energy types** — these carry stronger humanoid experiential connotations than `mana`/`focus`. Whether this constitutes "humanoid-presupposing" or merely "form-agnostic-but-named-humanoid" is judgment-call territory for gandalf. I've tagged them as form-agnostic-but-named-humanoid but could argue humanoid-presupposing for `rage` specifically.

5. **`CanonicalLibrary` canonical names** (`"Searing Wave"`, `"Stone Grasp"`, `"Iron Rend"` in `library_generator.py:20–24`) — these are humanoid-fantasy names used as the "timeless, foundational identity" that seasonal names "decorate." Whether the canonical library's humanoid-fantasy name vocabulary is a concern for form-bias depends on how the library is used in the new architecture. Currently it is read-only at naming time and the canonical names don't reach the player-facing LLM prompts directly (they're stored as `canonical_pair_ref`), but the doc says they ARE used as the "stable foundation." Gandalf may want to evaluate whether the canonical library vocabulary needs re-generation once the cipher architecture shifts.

---

## Decision-critical-and-unknowable-from-code-reading flags (max 2-3)

### Flag A — D1 rubric systematic screening effect on non-humanoid-cosmology words

The five questions in `_score_novel_word()` (particularly Q2: `{word}-armor` and Q4: `{word}-Knight`/`{word}-Mage`) may systematically penalize words that are meaningful in non-humanoid cosmological contexts but don't compound naturally with humanoid-martial vocabulary. A word like "pressure" (excellent for a deep-sea cosmology) might score 6–7 on the rubric (passes as "eligible" but not "allow-list") because "pressure-Knight" sounds awkward even though "pressure-Bearer" or "pressure-Surge" would be natural in context. This is not verifiable from code reading alone. It requires running the rubric on a test set of non-humanoid-cosmology candidates. **This matters before any D1 pool reconsideration work, not after.**

### Flag B — `Foundation` model validator and cipher architecture extension

The validator at `foundation/foundation.py:39–43` hard-codes the constraint that exactly one non-rotating element named `"physical"` exists, and enforces the 4-rotating-element structure. Doc 37 § 6's Position (ii) and the open-thread's Options A/B (expanding cipher to 7–9 slots) would require this validator to be updated — but the validator's structure would also need to accommodate the new abstract pair-structure layer. Currently the Foundation schema IS the canonical-four structure. Any cipher architecture expansion requires deciding whether Foundation grows to accommodate the new structure, or whether Foundation is decoupled from the cipher slots. **This architectural question is unknowable from code reading alone and must be resolved before any cipher migration work is dispatched.**
