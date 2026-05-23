# Wide-Net Engine Coupling Archaeology — 2026-05-17

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Authority:** gandalf (story-and-design steward), commissioning an Explore agent for systematic engine walk.
**Status:** audit-traceable archaeology record. Captures the coupling state of the engine at the time the substrate-expansion + five-layer-diversity-architecture decision was being committed.
**Companion artifacts:** `substrate-coupling-archaeology-2026-05-17.md` (13 substrate-keyed coupling sites) and `archetype-coupling-archaeology-2026-05-17.md` (10 archetype-keyed coupling sites). This doc captures the **14 additional sites surfaced beyond those two clusters.**
**Consumers:** jack-ryan engineering-disciplines pass; knight-rider Phase-1 P1 dispatch cascade sequencing; rocket / gamora implementation reference; Matt audit trail.

---

## § 0 — Why this exists

Two prior archaeology passes had surfaced **substrate-coupling** (13 sites where canonical-four element labels are hardcoded) and **archetype-coupling** (10 sites where archetype templates and dispatch logic are hardcoded). The pattern in both: registry-driven foundation + hardcoded consumers. Matt asked, before committing the substrate-expansion + diversity-architecture decisions: *"should we also commission a wide-net engine crawl, in parallel, just to be sure we have not missed any further instances of engine hard-coding for any other constructs?"*

The crawl ran 2026-05-17 against `reincarnated-engine/src/reincarnated/` and `reincarnated-engine/config/`. It surveyed 24 construct categories: geometry palette, role primitives, ailment families, energy types, stats, damage types, cooldowns, status effects, scaling formulas, LLM prompts, D1 rubric, anchor types, loot rarity, ritual structures, gear-affix categories, class shape primitives, spatial geometry, movement profiles, traits, form types, cosmology vocabulary, resource patterns, telemetry fields.

This doc is the record of what was found.

---

## § 1 — Headline summary

- **Total construct categories surveyed:** 17 categories with documented findings (others surveyed but clean / out-of-scope)
- **Registry-driven (clean):** 1 (attributes)
- **Hardcoded:** 14
- **Mixed (partial registry + hardcoded branches):** 2 (geometries; secondary effects)
- **HIGH-severity NEW clusters (beyond substrate + archetype):** 3 — roles, ailments, cosmology/grouping-layer vocab
- **Critical surprise:** LLM prompt structure is wired around the 5 grouping slots; expanding beyond requires LLM-pipeline refactor

---

## § 2 — HIGH-severity NEW clusters

### § 2.1 — Role primitives cluster

**Pattern:** 9 hardcoded role names (`primary_attack`, `burst_damage`, `area_damage`, `damage_over_time`, `control`, `mobility`, `defensive`, `sustain`, `utility`) replicated across 5+ files with no central registry.

**Sites:**

| File | Construct | Note |
|---|---|---|
| `generation/role_constraints.py:27-114` | `ROLE_CONSTRAINTS` dict | 9 hardcoded roles; canonical authoring site |
| `generation/role_constraints.py:119-129` | `CAST_TIME_RANGES` dict | Per-role cast-time windows hardcoded |
| `generation/class_generator.py` | `ROLE_SKILL_TEMPLATES`, `WEIRD_ROLE_POOLS`, `_EXPERIMENTAL_ROLE_POOL` | All hardcode same 9-role set |
| `generation/monster_generator.py:59-66` | `ARCHETYPE_ROLE_POOLS` dict | Monster archetypes → role subsets hardcoded |
| `simulation/ai_strategies.py:17-45` | `ARCHETYPE_ROLE_PRIORITY` dict | 20+ archetypes × role priority lists hardcoded |
| `generation/ability_grammar.py` | Role-keyed branching | Hardcoded role-name comparisons |

**Discipline #13 note:** the prior substrate-coupling archaeology examined `role_constraints.py` in isolation and concluded "FULLY COMBINATORIAL — proves the engine knows how to be extensible." That was a **scope-of-judgment error** — the file is combinatorial *within itself*, but the 9-role set is replicated as identical hardcoded lists across 5 other files. **A layer's extensibility cannot be judged from one file's shape; the perimeter must be checked.** Surface to jack-ryan for the disciplines pass.

**Convergence/extension risk:**
- New roles fail at lookup in ROLE_CONSTRAINTS
- Existing roles missing from a given archetype's role pool never generate
- AI strategies do not prioritize new roles (silent omission)
- Cast-time ranges fall to default for unknown roles

**Severity:** HIGH

**Diversity-architecture implication:** Roles must be added as a Layer-1 identity-declaration axis. The five-layer architecture's Layer 1 was scoped to substrates only; roles need parallel registry-driven treatment. **Phase-1 P1 scope grows by one axis.**

**Suggested fix-shape:** Define `config/roles.yaml` registry + a Role data class; rewrite the 5 consumer files to iterate the registry instead of hardcoding the 9-role list.

---

### § 2.2 — Ailment families cluster

**Pattern:** 5 hardcoded ailment names (`burn`, `chill`, `root`, `knockback`, `bleed`) across element-bias dicts, control-classification, AI logic, and validation.

**Sites:**

| File | Construct | Note |
|---|---|---|
| `generation/element_biases.py:18-58` | `ELEMENT_AILMENT`, `AILMENT_PARAM_RANGES`, `AILMENT_IS_CONTROL` | 5 ailments hardcoded with control classification |
| `foundation/effect_categorization.py` | `CONTROL_EFFECTS` frozenset | `{root, knockback, silence, chill}` — control-classification hardcoded |
| `generation/ability_grammar.py` | Fallback to `"silence"` | Hardcoded fallback control-effect name |

**Convergence/extension risk:**
- A new substrate proposing a new ailment (`shock` for lightning, `consecrate` for holy, `drain` for shadow) requires entries in 3+ sites
- New control-effect names not in `CONTROL_EFFECTS` are not recognized by AI priority logic → silent omission from AI strategy
- Telemetry may not track new ailments (column-name dependencies)

**Severity:** HIGH

**Diversity-architecture implication:** Ailment registry + identity-declaration treatment. Layer 1 substrate identity must declare its ailment_signature; the engine must accept registered new ailments. Control classification must also be extensible (or per-ailment metadata-declared) rather than a hardcoded frozenset.

**Suggested fix-shape:** `config/ailments.yaml` registry with per-ailment `is_control: hard|soft|none` + `param_ranges` + AI-priority metadata. Substrate identity declarations reference ailment names from this registry.

---

### § 2.3 — Cosmology / grouping-layer vocabulary cluster (**the critical surprise**)

**Pattern:** The L2 grouping-layer pair-structure (ignition/suffusion/bulwark/displacement/impact + Primary-Pair / Secondary-Pair / Foundation) is hardcoded **into the LLM prompt template structure itself**, not merely as a label dict.

**Sites:**

| File | Construct | Note |
|---|---|---|
| `llm/naming.py:32-42` | `_SLOT_ATTRS`, `_CANONICAL_TO_GROUPING` | Element-to-grouping label dicts (already in substrate-coupling-archaeology #8) |
| `llm/cosmological_vocabulary.py:63-75` | `GROUPING_SLOTS` tuple, `_SLOT_MODE_OF_ACTION` dict, `_PRIMARY_PAIR`, `_SECONDARY_PAIR`, `_FOUNDATION_SLOT` | **Pair-structure framework wired into prompt template** |

**The criticality:** earlier substrate-coupling archaeology flagged `naming.py:32-42` as a dict-extension problem. Wide-net reveals the deeper issue: **the LLM prompt structure is built around a 2-2-1 pair-structure assumption** (Primary Pair + Secondary Pair + Foundation). Expanding L1 substrate from 4 (+1 foundation) to 6-7 (with paired-luminance axis) requires either:

- (a) Reassigning new substrates into the existing 2-2-1 slots (compromises Layer-1 identity distinctness — back to convergence)
- (b) Growing the pair-structure (3-3 + foundation, or 3 pairs, or 2-2-2-1, etc.) — requires **rewriting the LLM prompt structure**, not just adding labels

**This is the load-bearing finding of the wide-net crawl.** The grouping-layer extension I have queued for Stage 2 of the substrate-expansion pre-work is **not merely "author labels for lightning/holy/shadow"** — it is **redesign the LLM prompt structure to be registry-driven against the substrate identity registry, then add the 3 new grouping labels.**

**Convergence/extension risk:**
- New substrates → unknown grouping slot mappings → LLM prompts fail or produce incoherent output
- LLM flavor generation pipeline is the *primary* surface vocabulary mechanism; structural breakage compromises Stage 3 cipher migration

**Severity:** HIGH (critical)

**Diversity-architecture implication:** Layer 4 (LLM as Flavor Diversifier) requires Layer 1 substrate identity declarations to drive prompt-template construction dynamically. The prompt template is not a fixed string with 5 named slots; it is a *function of the substrate identity registry*. Substantial Layer-4 design work.

**Suggested fix-shape:** Refactor `llm/cosmological_vocabulary.py` to read pair-structure shape from a design-doc-authored config (e.g., `canonical/story/grouping-layer-vocabulary.md` machine-extractable section, or a `config/grouping_structure.yaml`). Prompt templates iterate the registered grouping slots at call-time. Maintenance protocol: substrate-identity declaration changes auto-propagate to prompt template.

---

## § 3 — MEDIUM-severity sites

### § 3.1 — Energy types

**Sites:**

| File | Construct |
|---|---|
| `simulation/combatant.py:239-244` | `_ENERGY_CONFIGS` dict (4 non-mana types: rage/combo/focus/stamina) |
| `generation/gear_generation.py` | `_ALL_ENERGY_TYPES` list |
| `generation/season_orchestrator.py` | `_PHYSICAL_ENERGY_TYPES` list |
| `generation/monster_generator.py:93-100` | `_PHYSICAL_MONSTER_ENERGY` archetype→energy dict |

**Note:** Energy types are NOT substrate-coupled (mana/rage/combo/focus/stamina are universal). A new substrate doesn't need a new energy type. **But:** if a substrate identity declaration WANTS a custom energy resource (e.g., "consecration" energy for holy, "shadow-pool" for shadow), the hardcoding blocks it. Discretionary extension. Surface as P1b candidate.

**Severity:** MEDIUM (discretionary)

---

### § 3.2 — Threat tiers (monster scaling)

**Sites:**

| File | Construct |
|---|---|
| `simulation/combatant.py:25-34` | `TIER_EFFECTIVE_ATTRIBUTE` (8 tiers: swarm/magic/trash/standard/elite/mini-boss/boss/trial) |
| `generation/monster_generator.py:26-56` | `TIER_HP_FACTOR_RANGE`, `TIER_ARMOR_FRACTION`, `TIER_SKILL_COUNT` per-tier dicts |
| `generation/b6_archetype_templates.py` | `TIER_SCALING_BANDS`, `TIER_UNLOCK_REQUIREMENTS` |

**Note:** Tiers are universal monster-building constructs, not substrate-coupled. Math-locked per balance docs. Stable design. **Diversity-architecture impact: none.** Surface only if game-mode expansion (Nightmare+ tiers) is on roadmap.

**Severity:** MEDIUM (stable; low extension probability)

---

### § 3.3 — Geometry / damage resolver branching

**Sites:**

| File | Construct |
|---|---|
| `simulation/damage_resolver.py:~80+` | Geometry-specific `if geometry == "ranged_physical"`, `if geometry == "chain_lightning"` branches |

**Note:** Geometries themselves are registry-driven from `config/vocabularies.yaml` (clean). But the damage resolver has hardcoded geometry-specific behavior branches that won't auto-apply to new geometries. **New geometries fall to default damage treatment; specialized mechanics (fork, chain, vortex_pull) won't trigger.**

This is a Pattern-P7 instance (silent-default) at the simulation seam.

**Severity:** MEDIUM

**Suggested fix-shape:** Refactor geometry-specific behavior to a dispatch table / strategy pattern keyed off `geometry_metadata` (declared in the geometry registry) rather than name-comparison branches.

---

### § 3.4 — Movement speed by archetype

**Sites:**

| File | Construct |
|---|---|
| `generation/monster_generator.py:79-86` | `ARCHETYPE_MOVEMENT_SPEED` (6 monster archetypes → m/s values) |
| `simulation/fight_engine.py` | AI speed multiplier (0.719) + distance thresholds math-locked |

**Note:** Movement speed is archetype-coupled, not substrate-coupled. New archetypes need movement-speed entries. The math-lock (0.719 multiplier ↔ distance thresholds) means changes propagate carefully. **Diversity-architecture impact: covered by archetype-coupling cluster; movement-speed becomes a Layer-2-composition output, not a Layer-1 declaration.**

**Severity:** MEDIUM

---

### § 3.5 — Status effects / control effects (partial overlap with ailments)

**Sites:**

| File | Construct |
|---|---|
| `foundation/effect_categorization.py` | `CONTROL_EFFECTS` frozenset (already named in § 2.2) |
| `simulation/combatant.py` | `is_silenced` property hardcodes "silence" name; `MELEE_GEOMETRIES` frozenset |
| `generation/ability_grammar.py` | "silence" hardcoded as fallback |

**Note:** Overlaps with § 2.2 ailment cluster but extends to non-ailment status effects (buffs, debuffs, silences). Same fix-shape applies — control-effect membership becomes registry-declared per-ailment metadata, not a hardcoded set.

**Severity:** MEDIUM

---

### § 3.6 — Timing types / cast-time profiles

**Sites:**

| File | Construct |
|---|---|
| `generation/role_constraints.py:11-12` | `timing_options` tuple in RoleConstraint |
| `generation/role_constraints.py:119-129` | `CAST_TIME_RANGES` per-role dict |

**Note:** 4 timing types (`instant`, `cast`, `charge`, `channel`) used across role_constraints and ability_grammar. No central enum. New timing types (e.g., hybrid `channel_instant`) require multi-file updates.

**Severity:** MEDIUM (stable; low extension probability)

---

### § 3.7 — Secondary effects / buff types

**Sites:**

| File | Construct |
|---|---|
| `generation/role_constraints.py:20-22` | `secondary_effects` tuples with hardcoded effect names |

**Effects observed:** lifesteal, buff_damage, buff_dodge, buff_defense, buff_mana_regen, shield, heal, heal_over_time, silence, damage.

**Note:** No central enum; hardcoded as string literals. New substrate-coherent buff types (e.g., `consecrate` buff for holy, `shadow_veil` for shadow) require role-constraint-tuple edits + ability_grammar updates.

**Severity:** MEDIUM

**Diversity-architecture implication:** Substrate identity declaration's `secondary_effects` slot may need to declare substrate-coherent buff types; effect registry extension.

---

## § 4 — LOW-severity sites (stable; no architectural attention needed)

### § 4.1 — Attributes (STR/DEX/INT/WIS/VIT)

`config/attributes.yaml` registry-driven. Clean. **Diversity-architecture impact: none.** No work needed.

### § 4.2 — Range profiles

`_ALL_RANGE_PROFILES = ["close", "medium", "long"]` hardcoded but stable. Not substrate-coupled.

### § 4.3 — Gear rarity tiers

`GEAR_TIERS = ["common", "uncommon", "rare", "epic", "legendary"]` hardcoded but stable. Not substrate-coupled.

### § 4.4 — Gear slot types

`BASE_ITEMS` list hardcodes 18 item types + slots. Stable structure. Not substrate-coupled.

### § 4.5 — Cast-time ranges

Per-role; not substrate-coupled.

### § 4.6 — Tier scaling bands

`TIER_SCALING_BANDS` math-locked per balance docs. Universal scaling.

### § 4.7 — Distance bands / room variants

`CLOSE_THRESHOLD`, `ENGAGEMENT_DISTANCE_START`, `KITE_TRIGGER_DISTANCE`, `ROOM_VARIANTS` hardcoded but stable. Math-locked to AI speed multiplier.

### § 4.8 — Traits / trait categories

Mixed (schema-driven categories + hardcoded per-stat trait pools). New trait categories require schema + pool updates. Not substrate-coupled. Low extension probability.

---

## § 5 — Verdict and diversity-architecture impact

### § 5.1 — Diversity architecture scope change

The five-layer diversity architecture's **Layer 1 (substrate identity declaration)** scope was originally substrates-only. Wide-net findings expand it to **four axes:**

| Axis | Original architecture | Post-crawl architecture |
|---|---|---|
| Substrate | Layer 1 identity declaration ✅ | unchanged ✅ |
| Archetype | Composed at Layer 2 from substrate × role | unchanged ✅ |
| **Role** | Assumed registry-driven (was wrong) | **Layer 1 identity declaration needed** |
| **Ailment** | Implicit via substrate | **Layer 1 identity declaration needed (+ control-classification metadata)** |
| **Grouping-vocab + LLM prompt structure** | Layer 4 prompt-template (was assumed fixed) | **Registry-driven against substrate identity** |

### § 5.2 — Phase-1 P1 scope estimate revision

**Original estimate:** 4-6 weeks for Layers 1-4 (substrates + archetype refactor + diversity gate + LLM flavor).

**Revised estimate:** 6-8 weeks, OR partition into P1a + P1b:

- **P1a** — substrate identity declarations + archetype combinatorial refactor + grouping-vocab + LLM prompt structure refactor (the load-bearing critical path)
- **P1b** — role registry + ailment registry + control-classification extensibility + geometry damage-resolver refactor (the cleanup pass)

Layer 5 (telemetry feedback loop) remains deferrable to Phase-1 P2.

### § 5.3 — Open questions raised by the crawl

1. **Roles-as-Layer-1-axis vs roles-as-static-set.** Does the design want substrate-specific role variants (e.g., lightning has a *resonant* damage role distinct from fire's *burst* damage role)? Or do the 9 existing roles cover the substrate × role matrix at appropriate granularity? **Matt design call.**

2. **Ailment proliferation.** 7 substrates × 1 native ailment = 7 ailments. With control-effects extended, the AI priority logic faces N choices instead of 5. **Player cognitive-load implication; defer to Legolas literature pass for guidance on cognitive-load thresholds for control effects.**

3. **Grouping pair-structure shape.** 2-2-1 (current) → 3-3 (paired-luminance), 3-2-1-1 (paired-luminance + unpaired lightning), or registry-driven where the shape is data, not code? **The choice affects LLM prompt template structure design substantially. Surface to gandalf grouping-vocab extension work (Stage 2 of pre-work).**

---

## § 6 — Cross-references

- `canonical/story/substrate-coupling-archaeology-2026-05-17.md` (companion; 13 substrate-keyed sites)
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` (companion; 10 archetype-keyed sites)
- `canonical/story/substrate-expansion-decision-2026-05-17.md` (the decision this archaeology supports)
- `canonical/story/grouping-layer-vocabulary.md` (current 5-slot vocabulary; § 6 pair-structure framing; § Q4 future-expansion reserved labels)
- `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` (Legolas Mode A; pending; will inform Layer-1-5 failure-mode adjustments)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #13 (implicit-pillar drift) is the underlying pattern this archaeology surfaces; jack-ryan disciplines pass consumes this artifact for D14/D15/D16 + the new D17-candidate ("layer extensibility judged at perimeter not at site")

---

## § 7 — Maintenance

This doc is a **point-in-time audit artifact.** It is not re-rolled on each engine change; it captures the state at the substrate-expansion-decision commitment moment.

Future archaeology passes (when the next substrate / role / ailment expansion is contemplated) produce sibling artifacts (`wide-net-coupling-archaeology-YYYY-MM-DD.md`), not amendments to this one. Pattern-recognition over time: comparing successive archaeology passes shows whether the engine is becoming more or less registry-driven; this is a slow-cycle health metric for the diversity architecture's effectiveness.

---

*Authored 2026-05-17 by gandalf. Captures wide-net coupling state at the substrate-expansion + diversity-architecture decision commitment moment. Companion to substrate-coupling and archetype-coupling archaeology artifacts.*
