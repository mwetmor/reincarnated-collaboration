# Trait Constellation Audit — GAP 5
# Cycle 13 Block D Feed-in

**Author:** rocket
**Date:** 2026-05-26
**Dispatch:** `agentic_orchestration/dispatches/2026-05-26-rocket-cycle-13-gap-5-trait-constellation-audit.md`
**Purpose:** Pre-launch design session Block D verification — audit current trait pool coverage vs expected for v1; feed Matt + gandalf's decision on expand-in-Cycle-13 vs sufficient-for-first-season.
**Mode:** Read-and-report only. No engine modifications. No regen.

---

## § 1 TL;DR

**Gap count: 3 structural gaps, severity: BLOCKING for first season.**

The engine's trait constellation does not exist at the per-class intrinsic level (B9a). Zero per-class trait pools are defined. Zero floors are implemented at L1/L12/L25/L38. No trait data appears in any generated output (v2_narrow, v2_narrow_phase_5_resmoke, or any of the 7 historical season exports). The gear-affix trait surface exists in schema and generation code but emits zero traits in production output (it is limited to STAT-category traits on rare/epic/legendary gear only; ABILITY and GRANTED traits are explicitly deferred to CP5).

**Recommendation: expand-in-Cycle-13 — this is a load-bearing gap.** The design specifies per-class intrinsic trait floors as a core progression mechanic. Cycle 13 Wave 2 kit composition work directly depends on knowing the trait surface per class. Without it, the T4 algorithm's chain-level trait interactions cannot be specified, and the gear-affix interaction (element/mechanic-gated) has nothing to interact with. Two deferred work items (D8 and D9 per AGENT_STATE.md:2037-2039) are the blocking units.

---

## § 2 Current State (8 dimensions)

### Dimension 1 — Current trait pool enumeration

**Per-class intrinsic trait pool (B9a): DOES NOT EXIST in code.**

There is no `config/traits/` directory. There is no per-class trait pool definition, loader, or generation integration. The AGENT_STATE.md explicitly tracks this as pending gandalf design dispatch (D8, line 2037). The class schema (`class_schema.py`) carries no trait pool field. The class generator (`class_generator.py`) has zero trait references. The bc_target_composer.py has a three-line comment at lines 788-791 explicitly deferring trait composition to W0.2+ and stating "the existing trait system (trait_schema.py) continues to operate unchanged."

**Gear-affix trait surface: partially defined, zero emission.**

`trait_schema.py` defines the mechanical trait vocabulary:
- `TraitCategory` enum (STAT / ABILITY / GRANTED) — lines 23-26
- `VALID_STAT_KEYS` (11 keys) — lines 41-55
- `VALID_ABILITY_MODIFIER_KEYS` (6 keys) — lines 58-65
- `TraitSpec` dataclass — lines 86-133
- `aggregate_traits()` aggregation function — lines 241-297

`gear_generation.py` defines two slot-partitioned trait pools used at gear generation time:
- `_STAT_TRAIT_POOL` (line 738): 7 entries across weapon/armor/accessory slots
- `_ABILITY_MODIFIER_POOL` (line 720): 7 entries across weapon/armor/accessory slots (these are ability_modifiers on the GearInstance, not TraitSpec objects)

`gear_schema.py` carries `traits: list[TraitSpec]` at line 148 and a `combined_traits()` method (lines 284-289).

`skill_schema.py` carries `trait_slots: list[str] = []` at line 58 — explicitly marked as a forward-compat stub for Priority 14.

### Dimension 2 — Per-class trait count vs 5-10 target

**Result: 0 traits per class across all 11 archetypes and 35 v2_narrow forms.**

Target per `project_trait_architecture.md`: 5-10 traits per class.

Actual state:
- v2_narrow: 35 classes across 11 archetypes — 0 traits each
- v2_narrow_phase_5_resmoke: 5 forms — 0 traits each
- season_001001 through season_001010 (7 seasons, 10 classes each) — 0 per-class intrinsic traits

Every archetype (physical_warrior, hunter, fire_mage, rogue, physical_skirmisher, earth_caster, holy_caster, wind_controller, shadow_caster, physical_grappler, shadow_controller) has 0 intrinsic traits defined or emitted.

**All 11 archetypes are outside the 5-10 band. All are at 0.**

### Dimension 3 — Floor coverage (L1 / L12 / L25 / L38 + L50 convergence)

**Result: 0 floors implemented for any class.**

Target per design: floors at L1, L12, L25, L38 with L50 convergence (all traits at max rank at L50 endgame baseline).

No floor definitions exist in code, config, or output. The `balance_loop.py` `_trait_fill_cycling_hook()` function (lines 3445-3465) is an explicit no-op hook that documents the design intent ("Sample different trait fills from class's B9a intrinsic trait pool (5-10 traits)") but confirms B9a has not shipped.

No class has any acquisition floor data at any level. Floor coverage = 0/4 levels × 0/11 archetypes.

### Dimension 4 — Trait taxonomy coverage

**What the schema defines (mechanically available but not used at per-class level):**

Three trait categories are defined in `trait_schema.py`:

| Category | Keys available | Notes |
|---|---|---|
| STAT | 11 keys: bonus_hp, bonus_armor, bonus_crit_chance, bonus_damage_flat, bonus_damage_percent, bonus_mana_regen, strength, vitality, intelligence, wisdom, dexterity | 5 gear-stat keys active; 5 attribute keys (strength/vitality/intelligence/wisdom/dexterity) present but labeled "Priority 14 activates these in combat" |
| ABILITY | 6 keys: multishot_floor_bonus, cooldown_factor, energy_cost_factor, crit_bonus_damage, aoe_radius_bonus, control_duration_bonus | All defined; cooldown_factor + energy_cost_factor multiplicative; rest additive |
| GRANTED | granted_role (validated against ability grammar) + granted_element | Schema defined; explicitly deferred to CP5 for wiring |

**Missing from current taxonomy relative to design intent:**
- No element-tagged traits (design specifies element-gated gear affixes requiring element-tagged trait definitions per `project_trait_architecture.md` § "Eligibility gating")
- No energy-mechanic-tagged traits (design specifies mechanic-tagged traits per same section)
- No skill-specific traits (design places these in per-class intrinsic pool only — reasonable to not have these yet since intrinsic pool is absent)
- No on-trigger traits (design intent implied by doc 40 § 3.3 "mechanic-adjusting" capability toolkit — adjacent surface; not the same as intrinsic traits but the boundary is not fully drawn)
- GRANTED category: zero wired mechanics; deferred to CP5

**Coverage vs design taxonomy: ~30-40% of expected surface** (STAT keys cover the flat-bonus class; ABILITY keys cover rate-modifiers; element/mechanic gating layer, on-trigger layer, and GRANTED wiring are all absent).

### Dimension 5 — Gear-affix trait surface

**Current state: STAT traits only, limited scope, zero element/mechanic gating.**

`gear_generation.py` implements `_generate_stat_traits()` (line 1001) which produces STAT-category TraitSpec objects for rare/epic/legendary gear. The function:
- Returns `[]` for common/uncommon gear (line 1010)
- Pulls from `_STAT_TRAIT_POOL` (line 738): weapon=(bonus_damage_flat, bonus_crit_chance), armor=(bonus_hp, bonus_armor), accessory=(bonus_damage_percent, bonus_mana_regen, bonus_crit_chance)
- Generates 0-1 trait for rare, 1 trait for epic, 1 trait (1.5x scale) for legendary

**No element-gating.** No mechanic-gating. No per-class eligibility check. The trait generated is purely slot-based. This is not the element/mechanic-gated gear-affix system described in the design.

**Verified zero emission in all production output.** All 7 season gear_pool.json exports (season_001001 through season_001010, 200 items each) show `"traits": NOT PRESENT` on gear items — the `gear_pool.json` exporter does not include the traits field from GearInstance. The `gear_schema.py` GearInstance carries `traits: list[TraitSpec]` but this is not propagated to the JSON export format consumed by drax/loadout.

The ABILITY-category traits are implemented as `ability_modifiers` on GearInstance (separate from `traits` list) and ARE present in gear generation via `_generate_ability_modifiers()` (line 984) — but these are not TraitSpec objects and are not subject to the trait aggregation pipeline.

**Bottom line:** the gear-affix trait surface as designed (element/mechanic-gated, per-class eligibility, rank-stacking with intrinsic source) does not exist. A limited precursor (slot-partitioned STAT-only traits) is defined in code but doesn't reach the export layer.

### Dimension 6 — Empirical emission in v2_narrow (spot-check)

**Spot-checked 5 forms from v2_narrow_phase_5_resmoke and 10 forms from v2_narrow. All return zero trait data.**

| Form | Archetype | trait_slots (skills) | carried_gear traits | Per-class intrinsic |
|---|---|---|---|---|
| v2-form-000 | physical_warrior | NOT PRESENT | 0 | 0 |
| v2-form-004 | hunter | NOT PRESENT | 0 | 0 |
| v2-form-015 | fire_mage | NOT PRESENT | 0 | 0 |
| v2-form-025 | physical_warrior | NOT PRESENT | 0 | 0 |
| v2-form-032 | physical_skirmisher | NOT PRESENT | 0 | 0 |

The `trait_slots` field on Skill is explicitly a `list[str] = []` forward-compat stub (`skill_schema.py:58`) — it never populates in any generated output. The "NOT PRESENT" reading above is because the v2_narrow export schema omits the field entirely when empty (Pydantic default exclusion), consistent with it always being `[]`.

No form from any export (7 seasons + 2 v2_narrow variants) carries any trait data of any kind.

### Dimension 7 — Per-class intrinsic vs gear-affix interaction

**Result: no interaction to evaluate — neither source is implemented at the class level.**

The design specifies rank-stacking: `effective_rank = intrinsic_rank + gear_rank`, capped at max rank. The `aggregate_traits()` function (trait_schema.py:241) implements the correct additive stacking logic for STAT and ABILITY categories. The dedup-by-role logic for GRANTED traits is also implemented (with gear source winning over progression source).

The **mechanical aggregation is correct**. The **input data (per-class intrinsic pool + element/mechanic-gated gear affixes) is missing**.

Per `project_trait_architecture.md` § "Eligibility gating": element-gated traits require "at least one of the trait's tagged elements is present in P's class element distribution." This gating logic does not exist anywhere in the codebase. The `secondary_elements` field on `PlayerClass` (class_schema.py:46-47) provides the element distribution that would feed this gating — but no gating code consumes it for trait eligibility.

### Dimension 8 — Coverage vs Cycle 13 Wave 2 kit composition needs

**Gap is load-bearing for Cycle 13 Wave 2.**

Cycle 13 Wave 2 focuses on spec-driven gear gen with rarity escalation + capability toolkit (per dispatch context and doc 40). The T4 algorithm's Phase 2 chains feed into gear specification. Trait affixes (per doc 40 D14 stat-sheet partition cycle) are part of the modifier surface that gear rolls against.

Without the per-class intrinsic trait pool:
1. T4 algorithm cannot specify "this chain's T4 node unlocks trait X" — the trait vocabulary doesn't exist
2. Gear-affix element/mechanic gating cannot implement the eligibility check (no trait tags, no gating logic)
3. The `_trait_fill_cycling_hook()` in balance_loop (line 3445) remains a no-op, meaning the balance loop's trait lever does not fire — balance validation does not account for trait contributions at all
4. Spirit Guide build-coaching trait recommendations (per doc 33 § "Spirit Guide as build coach") have no trait data to recommend
5. The stat-sheet partition cycle (doc 40 D14, an early Cycle 13 milestone) needs to explicitly account for how trait affixes interact with per-slot modifier partitions — this cannot be designed without knowing what the trait surface looks like

The coverage gap is not cosmetic. The trait system is mechanically integrated (aggregation pipeline, balance loop hook, Spirit Guide feed) but all inputs are missing. First-season output without traits is technically generatable but is architecturally incomplete per the design specification.

---

## § 3 Expected Coverage

Per `project_trait_architecture.md` (memory file, confirmed by `canonical/historical/33-progression-skeleton.md` § "Decided — character progression"):

**Per-class intrinsic (B9a):**
- 5-10 traits per class, archetype-appropriate
- Acquisition floors at L1, L12, L25, L38
- Max rank 4 per trait; L50 convergence (all traits at max rank at endgame baseline)
- Includes element-tagged, mechanic-tagged, AND skill-specific traits (skill-specific intrinsic only)
- Auto-unlock at each floor; auto-rank with character level
- Per-hybrid class: pool drawn weighted by element distribution (e.g., 60/40 fire-wind hybrid → ~3 fire + ~2 wind traits)
- Experimental classes: no gear-affix trait rolls; intrinsic pool still applies

**Gear-affix (B15/B16):**
- Element-gated: trait rolls on gear if at least one tagged element present in class element distribution
- Mechanic-gated: trait's energy mechanic matches class energy mechanic (or trait is mechanic-agnostic)
- No skill-specific traits on gear
- Rank-stacks additively with intrinsic source (same trait from gear + intrinsic adds ranks)
- Gear tier sets per-rank multiplier; player level sets cap

**Total expected gear-affix-eligible pool:**
- ~5-10 traits per element × ~6 elements = ~30-60 element-tagged
- ~5-10 traits per energy mechanic × ~3-4 mechanics = ~15-40 mechanic-tagged
- ~5-20 generic traits
- Total: ~50-120 gear-affix-eligible traits

Per doc 40 § 3 (spec-driven gear gen, D14): stat-sheet partition cycle is an early Cycle 13 milestone that must land BEFORE gauntlet sim. Trait affixes are part of the modifier surface this cycle designs. The partition cycle includes enumeration of modifier types that gear rolls — traits are part of this surface.

---

## § 4 Gap Identification

| # | Gap | Severity | Type |
|---|---|---|---|
| G1 | Per-class intrinsic trait pool (B9a) does not exist | BLOCKING | Missing component |
| G2 | Gear-affix element/mechanic gating does not exist | BLOCKING | Missing component |
| G3 | Gear-affix trait production reaches generation code but not export layer | NON-BLOCKING (low-pri) | Emission gap |

**G1 — Per-class intrinsic trait pool (BLOCKING):**
No `config/traits/` schema, no loader, no class_generator integration, no class-level trait pool field. Zero traits emitted for any class in any output. All 11 archetypes are at 0 traits; target is 5-10. All 4 floors (L1/L12/L25/L38) are absent for every class. This is the entire B9a deliverable. AGENT_STATE.md line 2037 documents it as pending gandalf design dispatch (D8). The balance loop's `_trait_fill_cycling_hook()` (balance_loop.py:3445) remains a confirmed no-op until B9a ships.

**G2 — Gear-affix element/mechanic gating (BLOCKING):**
The gear generation produces limited STAT-only traits (slot-partitioned, no element/mechanic gating), but the full gear-affix system per design requires element-tagged trait definitions, mechanic-tagged trait definitions, and per-class eligibility gating logic against `secondary_elements`. None of this exists. AGENT_STATE.md line 2039 documents it as pending gandalf design dispatch (D9). This requires G1 to land first (traits must be defined before gating against them is meaningful).

**G3 — Gear-affix trait export gap (NON-BLOCKING):**
`gear_schema.py:148` carries `traits: list[TraitSpec]` but the gear_pool.json export format (used by all 7 season exports) does not include the `traits` field. For rare/epic/legendary gear the STAT-only traits generated by `_generate_stat_traits()` are computed at generation time but do not appear in exported gear items. This is a low-priority gap since G1 and G2 are more foundational; fixing G3 without G1 and G2 only surfaces incomplete trait data.

---

## § 5 Recommendation

**Expand-in-Cycle-13. Both G1 and G2 are load-bearing blocking gaps. G3 is non-blocking and defers.**

### What is blocking vs non-blocking

**Blocking (must be in Cycle 13):**
- G1: Per-class intrinsic trait pool implementation (D8 in AGENT_STATE.md queue)
- G2: Gear-affix element/mechanic gating implementation (D9 in AGENT_STATE.md queue)

These cannot defer because:
1. The stat-sheet partition cycle (doc 40 D14, early Cycle 13 milestone) needs to account for trait affixes in the modifier surface. Designing the partition without knowing the trait surface introduces a rework risk.
2. The balance loop trait lever (`_trait_fill_cycling_hook`) is wired but a confirmed no-op. Balance validation in Cycle 13 does not account for trait contributions — the validated balance is not representative of the shipped trait-inclusive balance.
3. Cycle 13 Wave 2 kit composition (T4 algorithm Phase 1-2 chains) needs the trait vocabulary to specify which traits each chain enables. Without a trait library, chain-to-trait association is undefined.

**Non-blocking (can defer):**
- G3: gear-affix trait export gap — defers until G1/G2 land (trait data in export is meaningless without the full trait system)
- Fine-tuning of per-class trait counts (the 5-10 band target) — first-pass implementation at 5 traits per class is sufficient for Cycle 13; refinement is iteration work
- Trait rank calibration (max rank 4, per-rank scaling) — can land in a follow-on smoke pass after initial pool is defined

### Specific work-unit framing (for Matt + gandalf decision)

**D8 (G1):**
- Scope: author `config/traits/` YAML schema (one file per element or one flat file); implement loader; define ~5 traits per archetype as minimum viable first-pass (5 × 11 archetypes = ~55 trait entries); integrate with class_generator to populate per-class intrinsic pool at generation time; wire floor emission at L1/L12/L25/L38
- Dependency: requires gandalf to design trait vocabulary (per AGENT_STATE.md "awaiting gandalf design dispatch")
- Owner: rocket (implementation); gandalf (trait vocabulary design input)

**D9 (G2):**
- Scope: add element/mechanic tags to trait definitions (extends D8 schema); implement per-class eligibility gating in gear_generation.py or gear_roller.py; extend gear-affix pool to include element-gated + mechanic-gated entries; rank-stack logic is already correct in aggregate_traits() — only the input data is missing
- Dependency: requires D8 to land first (traits must be defined before gating)
- Owner: rocket (implementation); gandalf (gating rule design input)

**Sequencing recommendation for Cycle 13:** D8 before D9; both before stat-sheet partition cycle completion (doc 40 D14) to avoid partition-rework risk; both before gamora balance validation pass (so balance loop trait lever fires correctly during Cycle 13 validation).

---

## § 6 Source Citations

| Dimension | Source | File | Line(s) |
|---|---|---|---|
| Trait architecture design | `project_trait_architecture.md` | memory file (14 days old; verify against code) | all |
| Trait architecture (doc form) | `canonical/historical/33-progression-skeleton.md` | § "Decided — character progression" | lines 243-248 |
| Trait category schema | `trait_schema.py` | generation seam | lines 23-26 (TraitCategory), 41-55 (VALID_STAT_KEYS), 58-65 (VALID_ABILITY_MODIFIER_KEYS), 86-133 (TraitSpec), 241-297 (aggregate_traits) |
| Gear STAT trait pool | `gear_generation.py` | generation seam | lines 738-743 (_STAT_TRAIT_POOL), 1001-1048 (_generate_stat_traits) |
| Gear ABILITY modifier pool | `gear_generation.py` | generation seam | lines 720-735 (_ABILITY_MODIFIER_POOL) |
| Gear schema trait field | `gear_schema.py` | generation seam | lines 148, 284-289 |
| Skill trait_slots stub | `skill_schema.py` | generation seam | lines 56-58 |
| bc_target_composer trait deferral | `bc_target_composer.py` | generation seam | lines 788-791 |
| B9a no-op hook (balance loop) | `balance_loop.py` | simulation seam | lines 3420, 3445-3465 |
| Per-class schema (no trait field) | `class_schema.py` | generation seam | full file; trait field absent |
| D8/D9 deferred queue | `AGENT_STATE.md` | generation seam | lines 2037-2039 |
| Gear-affix design + D14 partition | `canonical/40-gear-balance-guide-architecture-2026-05-26.md` | canonical | § 3 (D7-D17, D48-D57) |
| Element distribution field | `class_schema.py` | generation seam | line 46-47 (secondary_elements) |
| v2_narrow empirical spot-check | `exports/v2_narrow/classes.json` | engine exports | 35 classes; all trait fields empty |
| v2_narrow resmoke spot-check | `exports/v2_narrow_phase_5_resmoke/resmoke_forms.json` | engine exports | 5 forms; all trait fields empty |
| Season gear_pool scan | `exports/season_001001-001010/gear_pool.json` | engine exports | 7 seasons × 200 items; all trait-absent |

---

## Post-Script — Empirical Count Assertions (Discipline #11 + WARN-pattern compliance)

Per dispatch acceptance criteria and skill_handoff_2026-05-25 § 1 Priority 2 WARN-pattern requirement: numerical count claims are backed by empirical command output here.

**Claim: 11 archetypes in v2_narrow across 35 classes**
Verified by:
```python
Counter(cls['archetype_tag'] for cls in json.load(open('exports/v2_narrow/classes.json')))
```
Output: physical_warrior=10, hunter=5, fire_mage=5, rogue=3, physical_skirmisher=3, earth_caster=2, holy_caster=2, wind_controller=2, shadow_caster=1, physical_grappler=1, shadow_controller=1. Total=35. Verified 35 classes, 11 unique archetypes.

**Claim: 0 classes with gear traits across all 7 season exports**
Verified by scanning all gear_pool.json files (season_001001 through season_001010):
```
season_001001: 200 items, has_traits=False
season_001002: 200 items, has_traits=False
season_001003: 200 items, has_traits=False
season_001004: 200 items, has_traits=False
season_001005: 200 items, has_traits=False
season_001009: 200 items, has_traits=False
season_001010: 200 items, has_traits=False
```
1,400 total gear items scanned. 0 with trait data.

**Claim: 11 VALID_STAT_KEYS, 6 VALID_ABILITY_MODIFIER_KEYS**
Verified by:
```python
from reincarnated.generation.trait_schema import VALID_STAT_KEYS, VALID_ABILITY_MODIFIER_KEYS
len(VALID_STAT_KEYS) == 11  # True
len(VALID_ABILITY_MODIFIER_KEYS) == 6  # True
```
VALID_STAT_KEYS (11): bonus_armor, bonus_crit_chance, bonus_damage_flat, bonus_damage_percent, bonus_hp, bonus_mana_regen, dexterity, intelligence, strength, vitality, wisdom
VALID_ABILITY_MODIFIER_KEYS (6): aoe_radius_bonus, control_duration_bonus, cooldown_factor, crit_bonus_damage, energy_cost_factor, multishot_floor_bonus

**Claim: 7 stat trait pool entries across 3 slots**
Verified by inspecting `_STAT_TRAIT_POOL` at gear_generation.py:738-743:
weapon=2 entries, armor=2 entries, accessory=3 entries. Total=7.

**Claim: 0 classes with non-empty skill trait_slots**
Verified by scanning all 35 v2_narrow classes' skill lists:
```
Classes with any non-empty skill trait_slots: 0
```
All skill trait_slots are `[]` (forward-compat stub per skill_schema.py:58).

**Claim: 5 v2_narrow_phase_5_resmoke forms**
Verified by `len(json.load(open('exports/v2_narrow_phase_5_resmoke/resmoke_forms.json'))) == 5`. True.

---

**Signed:** rocket
**For:** Block D verification in Cycle 13 pre-launch design session (Matt + gandalf). GAP 5 trait constellation completeness. Read-and-report only.
