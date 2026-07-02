# Atomic Substrate Registry — Layer 0 + Layer 0.5 + Derivation Chains

> **STATUS:** CANONICAL (load-bearing as of 2026-06-06) — first authored 2026-06-06 as Path B output of Matt + gandalf multi-iteration design call on cosmograph architecture
>
> **Promotion candidate:** numbered canonical 52 (deferred to Matt directive; doc warrants numbering given its architectural-load-bearing status). Author preference: stays in `canonical/story/` until Matt promotes.

**Date:** 2026-06-06
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-06 verbatim ratification across multi-iteration design call:
- (a) confirmation that hypothesis-flow doc § 3 needs an upstream substrate layer enumerated (Path B);
- (b) inclusion of race + racial trait primitives + seasonal-substrate-rotation operator;
- (c) inclusion of skill-tree-position + damage-scaling primitives;
- (d) Layer 0.5 combinatory operators (element + sub-element, main + off-hand, race × element-attribute, seasonal-rotation);
- (e) Depth-2 derivation-chain documentation (textual; no full causal math);
- (f) LLM-derived content lives in separate Naming Layer stack (N1-N4), NOT in engine substrate;
- (g) schema-only race authoring + escape hatch for multi-axis seasonal rotation

**Companion docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` (cell schema + flag enum + pattern library Phase A-E) — this doc CAPTURES the upstream Layer 0 + Layer 0.5 that hypothesis-flow § 3 referenced but did not enumerate
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (engine end-to-end workflow + content lifecycle 6-step chain)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (gear/balance/guide/multi-T4 architecture)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` (damage scaling per skill-tree-tier)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` (investment scaling 6 patterns)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes + 68,040 cells)
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` (15-gear catalogue + weapon-form-token aggregation)
- `canonical/historical/09-geometry-palette-discussion.md` (16-type geometry palette)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (per-primary flavor pool registry)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system + element-attribute coupling)
- `canonical/story/off-hand-items-2026-05-24.md` (off-hand item parallel substrate)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` (BDI ω/τ — composed-primitive identity prediction)
- `canonical/story/2026-06-05-cosmograph-pivot.md` (cosmograph architectural commitment; consumes this registry)
- `canonical/story/weapon-substrate-conclusion-declaration.md` (89,839-row weapon substrate library)
- `~/Games/reincarnated-engine/src/reincarnated/foundation/` (substrate identity YAMLs)
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py` (element-attribute coupling registry)
- `~/Games/reincarnated-engine/config/elements.yaml` (canonical-7+1 element catalog)

---

## 0. TL;DR

The hypothesis-flow doc (2026-05-31) locked the cell schema + flag enum + Phase A-E pattern library architecture but referenced upstream "designer-writes substrate" as Layer 1 without enumerating the **atomic primitive registry** that composes into those Layer 1 coordinates. This doc IS that registry.

**Layer 0 atomic substrates** enumerated across 20 primitive families: elements, sub-elements/flavors, attributes, T4 strategies, skill geometry palette, skill-tree-position, scaling-pattern-per-tier, chain architecture, investment-scaling-patterns, mechanic-altering passives, resource models, modifier types, ailment types, weapon-form tokens, weapon-substrate properties, off-hand items, **race primitives (NEW)**, **racial traits (NEW)**, race-element affinity, race-attribute affinity.

**Layer 0.5 combinatory operators** explicit: element-count → kit_architecture derivation; element × sub-element scope; main + off-hand combinatorics; race × element-attribute interaction; **seasonal-substrate-rotation operator (NEW; single-axis default with multi-axis escape hatch)**.

**Layer 1 derivation chains** documented at Depth 2 (textual derivation rules; full causal math lives in engine code + canonical cross-references).

**Naming Layer stack (N1-N4)** introduced as separate downstream identity-naming family that lives ABOVE engine substrate hierarchy. Per Matt: LLM-derived content does NOT enter engine substrate; it lives in N1-N4 as cohesion-judge-validated identity.

**Cosmograph implications:** stars exist at multiple layers (Layer 0 primitives are first-class stars; Layer 0.5 combinatory operators are axis-pair edges; Layer 1 derived fields are labeled overlays; Naming Layer N1-N4 attaches as side-panel identity). Constellations (kits = composed primitives per hypothesis-flow § 3) CROSS LAYERS — showing how Layer 0 atomic substrates compose up to player-facing identity at Layer 2 + Naming Layer.

---

## 1. Layer 0 — Atomic substrate primitive families

These are the GENERATIVE INPUTS the engine composes from. The engine pulls atomic primitives at Phase 2 substrate-binding (per canonical 39 § 1) and produces kits whose Layer 1 coordinates emerge from atomic-primitive composition.

### 1.1 Element primitives

**Canonical source:** `~/Games/reincarnated-engine/config/elements.yaml`; `flavor-pool-per-primary-element-lock` (2026-06-01)

| Primitive | Type | Notes |
|---|---|---|
| `fire` | canonical-7 rotating | INT scaling; canonical |
| `water` | canonical-7 rotating | INT scaling; canonical |
| `earth` | canonical-7 rotating | WIS scaling; canonical |
| `wind` | canonical-7 rotating | WIS scaling; canonical |
| `lightning` | canonical-7 rotating | INT scaling; canonical |
| `holy` | canonical-7 rotating | WIS scaling; canonical |
| `shadow` | canonical-7 rotating | INT scaling; canonical |
| `physical` | +1 retained | STR scaling; not canonical-rotating but retained per element_biases.py |

**Count:** 8 (canonical-7 + physical)

### 1.2 Sub-element / flavor primitives (per-primary pool)

**Canonical source:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`

Each primary element has its own flavor pool of sub-element primitives (e.g., earth's pool includes bone, stone, clay; shadow's pool includes umbra; fire's pool includes ember). Per-primary pool size is locked per the flavor-pool doc; per-skill bounded LLM judgment (WS1A.4) selects from within the kit's primary's flavor pool, NOT from the full canonical-2.5 vocabulary.

**Count:** TBD per pool; locked authoritatively in flavor-pool-per-primary-element-lock doc.

### 1.3 Attribute primitives

**Canonical source:** `canonical/story/attribute-system-2026-05-24.md`; `element_biases.py:28 ELEMENT_SCALING_ATTRIBUTE`

| Primitive | Type | Element coupling |
|---|---|---|
| `STR` | Strength | physical → STR |
| `DEX` | Dexterity | (no native canonical-7 coupling; cross-attribute via T4 ELEMENT_CONVERSION) |
| `INT` | Intelligence | fire / water / lightning / shadow → INT |
| `WIS` | Wisdom | earth / wind / holy → WIS |

**Count:** 4 (VIT deferred per attribute-system doc)

### 1.4 T4 strategy primitives

**Canonical source:** `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.5.1 Step 2 + § 2b; canonical 40 Algorithm § 8

| Primitive | Effect |
|---|---|
| `RESOURCE_CONVERSION` | Converts one resource economy to another |
| `TRADE_OFF` | Mutual exchange between two character dimensions |
| `ELEMENT_CONVERSION` | Converts mechanical element to a different element |
| `DEFENSIVE_CONVERSION` | Converts offensive mechanic to defensive (or vice-versa) |
| `GEOMETRY_COLLAPSE` | Collapses skill geometry distribution |
| `DEFENSIVE_TRADEOFF` | Defensive vs survival/recovery tradeoff |

**Count:** 6 current (21 proposed expansion per canonical 47 § 11)

### 1.5 Skill geometry palette

**Canonical source:** `canonical/historical/09-geometry-palette-discussion.md` § Decision table + B11 expansion (2026-05-11)

**Primitives:** scatter / line / arc / cone / sweep / circle / aura / beam_channel / persistent_zone / ground_targeted_circle / melee_arc / totem / ground_slam / + 2 marginal types

**Count:** 16 (CORE 14 + CORE-MARGINAL 2)

### 1.6 Skill-tree position primitives (NEW per Matt 2026-06-06)

**Canonical source:** `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 2a + canonical 40 D-series

| Position-axis | Values |
|---|---|
| `tier_within_tree` | T1_rotation / T2_β_pair / T3_build_defining / T4_capstone |
| `chain_position` | which-of-N-chains (1-indexed; per class chain count) |
| `chain_role` | capstone_chain / supporting_T3_only_chain |
| `node_depth` | root → leaf progression within chain |

**Count:** combinatorial; ~50-100 distinguishable position-coordinates per kit at typical chain count

**Composition:** every individual skill node in a kit's tree has one tuple `(tier, chain, role, depth)` describing its position. Position-primitive composes with scaling-pattern-per-tier (§ 1.7) to determine damage_signature (Layer 1 derived per canonical 47).

### 1.7 Scaling pattern per tier primitives (NEW per Matt 2026-06-06)

**Canonical source:** `canonical/47-damage-scaling-architecture-2026-05-27.md`

| Position-tier | Scaling pattern | Effect |
|---|---|---|
| T1 rotation | **additive** | Each rank adds flat power |
| T2 β-pair | **additive + multiplicative interaction** | Rank adds power; pair combos multiply |
| T3 build-defining | **multiplicative** | Rank multiplies prior investment |
| T4 capstone | **transformative** | Changes the axis the character operates on (qualitative, not quantitative) |

**Count:** 4 named scaling patterns

**Composition:** skill-tree-position (§ 1.6) determines which scaling pattern applies; the scaling pattern determines per-skill damage scaling characteristics; aggregate skill damage scaling composes into BC Axis 3A tempo + Axis 3B amplitude variance + canonical 47 damage signatures.

### 1.8 Chain architecture primitives

**Canonical source:** `canonical/40-gear-balance-guide-architecture-2026-05-26.md` D83 (class chain count)

| Primitive | Composition |
|---|---|
| 3-chain class | 2 T4 capstone chains + 1 supporting T3-only chain |
| 4-chain class | 3 T4 capstone chains + 1 supporting T3-only chain |

**Count:** 2 current architecture patterns; future expansion possible

**Derivation rule:** T4 count = chain count − 1 (per doc 40 D83). Supporting chains enable hybrid + multi-element builds.

### 1.9 Investment scaling pattern primitives

**Canonical source:** `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md`

| Pattern | Effect |
|---|---|
| 1 — Linear additive | Each investment tier adds flat power |
| 2 — Multiplicative | Each tier multiplies prior investment |
| 3 — Threshold-unlock | Qualifies for new capability at investment threshold |
| 4 — Tradeoff | Investment shifts balance (not just adds power) |
| 5 — Capstone | Singular peak at max investment; flat below threshold |
| 6 — Progressive transformation | Investment changes mechanic TYPE |

**Count:** 6 patterns

**Orthogonal to tier scaling pattern (§ 1.7):** a T4 capstone with transformative tier-scaling can ALSO carry investment-scaling pattern 5 (capstone) — same mechanism, two orthogonal scaling-model dimensions.

### 1.10 Mechanic-altering passive pool

**Canonical source:** `canonical/story/skill-system-2026-05-24.md`; `~/Games/reincarnated-engine/src/reincarnated/foundation/` mechanic registry

The unified mechanic pool the engine pulls from at Phase 2 substrate-binding. Per canonical 39 substrate-agnostic mechanical generation principle, this pool is shared across all substrate types; substrate-binding selects from the pool per BC-target requirements.

**Count:** TBD; per-mechanic enumeration lives in skill-system + foundation/ at engine canonical layer.

### 1.11 Resource model primitives

**Canonical source:** `reincarnated-loadout/data/cycle13_characters.db` schema CHECK constraint; foundation/ resource registry

| Primitive |
|---|
| `cooldown` |
| `energy` |
| `mana` |
| `stamina` |
| `ki` |

**Count:** 5 current (composes into BC Axis 5 7-bin resource economy)

### 1.12 Modifier type primitives

**Canonical source:** `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md`

Per-slot per-tier modifier pool defining what stat-sheet modifications gear can carry. Cycle 13 partition design milestone (per doc 40 D14) locks the modifier vocabulary.

**Count:** TBD; per-modifier enumeration locked via canonical 42 + downstream Cycle 13 partition work.

### 1.13 Ailment type primitives

**Canonical source:** `~/Games/reincarnated-engine/src/reincarnated/foundation/ailment_loader.py` + per-element YAMLs

Per-element ailment registry (fire → ignite/burn; shadow → drain/curse; lightning → shock; etc.). Each element has a registered ailment set; the registry is boot-time-loaded per element_biases.py initialization.

**Count:** TBD per element; per-element registry in foundation/.

### 1.14 Weapon-form token primitives

**Canonical source:** `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/weapon_form_token_lookup.json`

~200 weapon-form tokens (greatsword, claymore, katana, longsword, falchion, rapier, longbow, crossbow, blunderbuss, wand, orb, etc.) each mapped to `(range, geometry, tempo, attribute)` tuple.

**Count:** ~200

**Aggregation rule:** weapon-form tokens aggregate to the 15-gear catalogue (§ 3 derivation chain) via gear-substrate-rule-table-v1 priority hierarchy (canonical pairing → range-axis dominance → role-tie-breakers → stat-dist alignment).

### 1.15 Weapon-substrate property primitives

**Canonical source:** `canonical/story/weapon-substrate-conclusion-declaration.md`; `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md`

Per-weapon properties carried by the 89,839-row weapon substrate library:

| Property | Type | Coverage |
|---|---|---|
| `cultural_lineage_canonical` | 14-enum | Per-row populated where determinable; 4-mode caveat per marginal-lineage-tagging-pattern |
| `historical_period_canonical` | 9-enum | Per-row populated where determinable |
| `register_canonical` | 6-enum | Per-row populated |
| `weapon_type_family` | 6-enum | DERIVED via weapon-form-token aggregation (§ 3 derivation) |
| `named-bearer attribution` | text | Per Track M1 / sub-agent gandalf seed list |
| Tier S/A/B/C quality | composite | Per substrate library composite quality scoring |

**Count:** 89,839 rows

### 1.16 Off-hand item substrate primitives (parallel to main-weapon)

**Canonical source:** `canonical/story/off-hand-items-2026-05-24.md`

Off-hand is a PARALLEL substrate axis to main-weapon. Off-hand can carry different cultural_lineage + period than main-weapon, enabling **hybrid culture/period kits** as first-class.

**Primitive types:**
| Type | Mechanical aspect |
|---|---|
| Shield | Block + survivability |
| Ammo pouch | Quiver + ranged-sustain |
| Focus / orb | Cast-focus + spell-power |
| Off-hand weapon-form-token | Dual-wield + combination attacks |
| Tome / grimoire (off-hand) | Spell-storage + summon-focus |
| Censer (off-hand) | Aura sustain |
| Etc. | per off-hand-items doc |

**Per-off-hand-token properties** mirror main-weapon (cultural_lineage + period + register + form_class) → off-hand × main-weapon culture/period combinatorics emerge as Layer 0.5 operator (§ 2.3).

**Count:** parallel to weapon-form-tokens; off-hand-specific enumeration TBD via off-hand-items doc.

### 1.17 Race primitives (NEW per Matt 2026-06-06; SCHEMA ONLY)

**Canonical source:** TO BE AUTHORED at per-season design time

**Schema spec:**

| Field | Type | Notes |
|---|---|---|
| `race_id` | str | Unique identifier within race-set |
| `race_set_id` | str | Which seasonal race-set this race belongs to (e.g., `tolkien_s1` / `warhammer_s2` / `aztec_indo_s3`) |
| `race_name` | str | Player-facing race name (Hobbit / Empire-Man / Lizardman / etc.) |
| `race_substrate_anchor` | str | The cultural-substrate the race is anchored to (Tolkien-medieval / Warhammer-grimdark / Aztec-mythical / etc.) |
| `race_trait_pool` | list[str] | Per-race racial trait pool (see § 1.18) |
| `race_element_affinity` | dict | Per-element weighting (see § 1.19) |
| `race_attribute_affinity` | dict | Per-attribute lean (see § 1.20) |
| `race_cultural_tradition_compatibility` | list[str] | Which weapon-substrate cultural traditions are race-coherent |

**Authoring discipline:** per-season race-set authoring happens at per-season design time. Default rule when no season-design is selected: races + racial traits randomized within the pool's possible race-trait combinations (per Matt 2026-06-06 directive).

**Count:** schema-locked; per-season race-set count TBD per season-design.

### 1.18 Racial trait primitives (NEW per Matt 2026-06-06; SCHEMA ONLY)

**Schema spec:**

| Field | Type | Notes |
|---|---|---|
| `racial_trait_id` | str | Unique identifier within race's trait pool |
| `race_id` | str (FK) | Which race this trait belongs to |
| `trait_name` | str | Player-facing trait name (halfling-resilience / fury-bonus / range-immunity-trait / secret-finder / doomed-mortality / etc.) |
| `trait_mechanical_effect` | str | What the trait does mechanically (composes with mechanic-altering passive pool § 1.10) |
| `trait_substrate_layer` | enum | Layer 0 substrate primitive vs Layer 1 derived effect |
| `trait_seasonal_rotation_membership` | str (FK to race_set_id) | Which seasonal substrate this trait rotates with |

**Authoring discipline:** schema-only; per-race trait pool authored at per-season design time.

**Count:** schema-locked; per-season trait pool count TBD per season-design.

### 1.19 Race-element affinity primitives

**Schema spec:**

Per-race weighting toward elements. Composes with Layer 0.5 race × element-attribute interaction operator (§ 2.4).

Example (Tolkien S1; illustrative not committed):

| Race | Affinity weighting |
|---|---|
| Tolkien Hobbit | shadow + wind (stealth + light-footed) |
| Tolkien Elf | wind + holy + water (graceful + lordly + tidal) |
| Tolkien Dwarf | earth + fire + physical (craft + forge + sturdy) |
| Tolkien Man | physical + holy (martial + heritage) |
| Tolkien Wizard | fire + lightning (channeling + maia-spirit) |

**Authoring discipline:** schema only; per-season per-race affinity authored at season-design.

### 1.20 Race-attribute affinity primitives

**Schema spec:**

Per-race weighting toward 4 attributes (STR/DEX/INT/WIS). Composes with Layer 0.5 race × element-attribute interaction.

Example (Tolkien S1; illustrative):

| Race | Attribute lean |
|---|---|
| Hobbit | DEX (light-footed + nimble) |
| Elf | DEX + WIS (graceful + sage) |
| Dwarf | STR (forge + sturdy) |
| Man | STR + WIS (balanced + heritage) |
| Wizard | INT + WIS (channeling + wisdom) |

**Authoring discipline:** schema only.

---

## 2. Layer 0.5 — Combinatory operators

These are OPERATORS on Layer 0 primitives, not primitives themselves. They produce composed substrate states from atomic primitive selection.

### 2.1 Element-count → kit_architecture derivation operator

**Inputs:** count of selected primary elements (1 or 2 per kit)
**Output:** kit_architecture label (`single_element` / `hybrid_2_element`)
**Rule:** present `kit_primary_element_2` is non-null → `hybrid_2_element`; otherwise `single_element`
**Composition:** drives per-skill flavor judgment scope (3-option for single vs 15-option for hybrid per hypothesis-flow § 1.7)

### 2.2 Element × sub-element scope operator

**Inputs:** kit's element selection (P1, optionally P2) + sub-element selection (S1, optionally S2)
**Output:** per-skill flavor judgment scope domain

| Kit architecture | Domain size |
|---|---|
| Single element (P1 + S1) | 3-option: {primary, sub, blend} |
| Hybrid 2-element (P1 + P2 + S1 + S2) | 15-subset: {P1, P2, S1, S2, {P1,P2}, {P1,S1}, ..., {P1,P2,S1,S2}} |

**Composition:** consumes per-primary flavor pool registry (§ 1.2); produces predicted emergent kit concept (hypothesis-flow § 3.10).

### 2.3 Main + off-hand combinatorics operator

**Inputs:** main-weapon cultural_lineage + period + main-weapon-form-token + off-hand cultural_lineage + period + off-hand-form-token
**Output:** hybrid culture/period kit possibility + combined mechanical aspect set
**Rule:** main_weapon.culture ≠ off_hand.culture → hybrid culture kit; same for period
**Composition:** enables culture-bridge kits (e.g., Norse main-weapon + Aztec off-hand-shield); LLM cohesion-judge uses combined cultural context downstream for kit identity naming.

### 2.4 Race × element-attribute interaction operator

**Inputs:** race-element-affinity (§ 1.19) + race-attribute-affinity (§ 1.20) + kit's selected element + kit's selected attribute
**Output:** race-coherence score (how well race fits the kit's mechanical substrate)
**Use:** scoring input to cohesion-judge during kit identity finalization; LOW race-coherence kits are flagged for alternative race-selection or alternative-element fit.

### 2.5 Seasonal-substrate-rotation operator (NEW per Matt 2026-06-06)

**The operator that rotates which substrate axes are HELD vs ROTATED between seasons.**

**Default rule (per Matt 2026-06-06):** single-axis rotation per season minimum; ≥1 axis held for continuity.

**Escape hatch (per Matt 2026-06-06):** if single-axis rotation does not produce meaningful seasonal differentiation, multi-axis rotation activates (no hard limit; bounded only by "≥1 axis held for continuity").

**Rotatable substrate axes:**

| Substrate axis | Rotation behavior |
|---|---|
| Race-set (§ 1.17-1.20) | Per-season race-set rotation (Tolkien S1 → Warhammer S2 → etc.) |
| Cultural-tradition pool (§ 1.15) | Per-season cultural-tradition weighting/availability rotation |
| Historical-period pool (§ 1.15) | Per-season historical-period weighting/availability rotation |
| Element pool (§ 1.1) | Per-season element subset (could subset canonical-7+1; default is all-8 active) |
| Sub-element pool (§ 1.2) | Per-season per-primary flavor pool refresh / weighting rotation |
| Weapon-form token pool (§ 1.14) | Per-season weapon-form availability (subset of 200) |
| Off-hand substrate pool (§ 1.16) | Per-season off-hand availability/rotation |
| Skill-geometry palette (§ 1.5) | Per-season geometry availability/weighting (default: all 16 active) |
| T4 strategy availability (§ 1.4) | Per-season T4 strategy subset (default: all 6 active) |
| Race-trait pool (§ 1.18) | Per-season trait pool refresh (composes with race-set rotation) |

**Example sequence (per Matt 2026-06-06 vision):**

| Season | Race-set | Cultural-tradition | Period | Notes |
|---|---|---|---|---|
| S1 | Tolkien | Celtic-Norse + Germanic medieval | Early medieval | Single-axis-rotation baseline |
| S2 | **Warhammer** | Same as S1 (held) | Same as S1 (held) | Race-set rotated only |
| S3 | Warhammer (held) | **Aztec + Indo-Asian dark ages** | **Pre-Columbian + South Asian dark ages** | Multi-axis rotation (escape hatch activated) — race held; culture + period both rotated |

**Composition with D4 continuity architecture:** held axes provide seasonal continuity (Earth Self recognizes familiar substrate); rotated axes provide seasonal differentiation (each season's incarnation feels distinct). The form library accumulates across seasons; rotated-substrate diversity grows over time.

**Composition with realm-expansion-pivot doc** (`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`): each Realm Expansion can introduce a new race-set + cultural+period rotation; the cosmograph displays the seasonal-substrate-rotation as a META-NARRATIVE (which constellations become visible/active per season).

---

## 3. Layer 1 — Derivation chains (Depth 2 textual)

How Layer 0 atomic primitives + Layer 0.5 combinatory operators compose into the Layer 1 fields that hypothesis-flow § 3.2 enumerates.

### 3.1 `bc_axis_signature` (8-vector) derivation

**Composes from:** Layer 0 — mechanical primitives (§ 1.10) + element (§ 1.1) + attribute (§ 1.3) + skill geometry palette (§ 1.5) + resource model (§ 1.11) + skill-tree-position (§ 1.6) + scaling-pattern-per-tier (§ 1.7)

**Per-axis derivation:**

| BC Axis | Composes from |
|---|---|
| Axis 1 Engagement profile (6 bins) | Skill geometry palette + skill-mechanic range + movement-skill prevalence |
| Axis 2 Damage geometry (5 bins) | Skill geometry palette aggregation per-skill |
| Axis 2A Proxy density (3 bins) | Mechanic-altering passive pool — minion/summon/totem mechanics |
| Axis 2B Control density (3 bins) | Mechanic-altering passive pool — control vs damage mechanics partition |
| Axis 3A Damage tempo (3 bins) | Skill cooldown × cast time × tempo-modifiers per scaling-pattern-per-tier |
| Axis 3B Damage amplitude variance (3 bins) | Per-event magnitude CV; scales with scaling-pattern-per-tier × investment-scaling-pattern |
| Axis 4 Defensive profile (4 bins) | Mechanic-altering passive pool — defensive mechanic family |
| Axis 5 Resource economy (7 bins) | Resource model + mechanic-altering passive pool resource-interaction |

**Derivation rules in engine canonical:** qd-engine-bc-axes-lock-2026-05-20.md § 3-4 (per-axis measurement formulas).

### 3.2 `weapon_type_family` (6-enum) derivation

**Composes from:** Layer 0 — weapon-form tokens (§ 1.14) + weapon-substrate properties (§ 1.15)

**Derivation rule:** weapon-form tokens aggregated to 15-gear catalogue via gear-substrate-rule-table-v1 priority hierarchy (canonical pairing → range-axis dominance → role-tie-breakers → stat-dist alignment); 15-gear catalogue further aggregated to 6-enum weapon_type_family at BC-bin level.

**Engine canonical:** gear-substrate-rule-table-v1-2026-05-22.md § 2 (15-gear catalogue) + § 3 (priority hierarchy).

### 3.3 `kit_architecture` (single/hybrid) derivation

**Composes from:** Layer 0.5 — element-count → kit_architecture operator (§ 2.1)

**Derivation rule:** if `kit_primary_element_2` non-null → `hybrid_2_element`; else `single_element`. NOT a peer substrate field with element-selection; STRICTLY derived from element count.

### 3.4 15-gear catalogue entry derivation

**Composes from:** Layer 0 — weapon-form tokens × range × geometry × tempo × attribute (§ 1.14)

**Derivation rule:** gear-substrate-rule-table-v1 mapping per § 2-3.

### 3.5 Damage / defense / mobility signatures derivation

**Composes from:** Layer 0 — skill-tree-position (§ 1.6) × scaling-pattern-per-tier (§ 1.7) × T4 strategy (§ 1.4) × investment-scaling-pattern (§ 1.9)

**Derivation rules:** canonical 47 damage-scaling-architecture (per-tier scaling) + canonical 51 investment-scaling-6-pattern (per-investment scaling) + T4 strategy mechanical-impact-pair (per canonical 39 § 2b DUAL mechanical impact).

### 3.6 Race-coherence derivation

**Composes from:** Layer 0.5 — race × element-attribute interaction operator (§ 2.4)

**Derivation rule:** race-element-affinity (§ 1.19) × race-attribute-affinity (§ 1.20) × kit's selected element × kit's selected attribute → race-coherence score. Used downstream by cohesion-judge for kit identity finalization.

---

## 4. Layer 1.5 + Layer 2 + Layer 3 — cross-reference

Well-captured in hypothesis-flow doc. Per Path B discipline, this registry does NOT re-author content already locked in hypothesis-flow doc.

| Layer | Source |
|---|---|
| Layer 1.5 — Coupling architecture | hypothesis-flow § 3.6 (coupling_layer_count + coupling_strength + single_axis_viability) |
| Layer 2 — Experiential axes (player-names-experience) | hypothesis-flow § 3.5 + § 4.1 (Target-Pattern / Depth-vs-Breadth / Progression-Stage / Viability / Loot-Focus / Activity-Format / Investment-Tier / Variant / Cell-Shape) |
| Layer 3 — Vestigial-class identity | hypothesis-flow § 3.7 (vestigial_class_label + class_lineage_coherence_signal) |

---

## 5. Naming Layer stack — N1-N4 (downstream of engine substrate)

**Per Matt 2026-06-06:** LLM-derived content does NOT enter Layer 0 atomic substrate (or any engine substrate layer). It lives in a separate downstream Naming Layer stack that consumes engine substrate output:

| Naming Layer | Content | Source | Position |
|---|---|---|---|
| **N1 — Per-skill flavor judgment + skill names** | Per-skill flavor element judgment (P/S/P+S subset) + skill name | WS1A.4 per-skill bounded LLM judgment + skill-naming LLM | DOWNSTREAM of Layer 0 + Layer 0.5 |
| **N2 — Kit identity name** | Kit name + identity narrative ("Duskweaver of the Eclipsed Meridian" + prose) | Wave B per-kit LLM identity-finalization | DOWNSTREAM of N1 + Layer 0 element substrate |
| **N3 — Faction name** | Per-faction emergent name + narrative | Wave A faction-naming LLM (from cohesion-judge clustering) | DOWNSTREAM of N1 + N2 + Layer 0 substrate |
| **N4 — Season name** | Season name + theme | Per-season seasonal-rotation operator output (§ 2.5) + race/culture/period theme | DOWNSTREAM of N1-N3 + seasonal-substrate-rotation operator |

**N1-N4 are emergent identity layers.** The cosmograph DISPLAYS them in side panel + constellation labels but does NOT render them as primitive stars. They are LABELS attached to constellations, not stars themselves.

**Composition with D7 (AI-tell line):** N1-N4 are bounded LLM output. Per-skill flavor judgment (N1) is bounded to substrate-element pair; kit naming (N2) consumes pre-vetted skill names; faction (N3) + season (N4) names compose from pre-vetted kits. Engine substrate layer (Layer 0-3) is pure substrate; Naming Layer (N1-N4) is cohesion-judge-validated identity. The line is preserved.

---

## 6. Cosmograph implications

Per `canonical/story/2026-06-05-cosmograph-pivot.md` + Pattern A-deep verdict at `agentic_orchestration/gandalf/notes/2026-06-06-cosmograph-star-granularity-verdict.md`:

### 6.1 Layer 0 atoms render as primitive STARS

The atomic substrate primitives in § 1 ARE the cosmograph's first-class stars. Specifically:

- 8 element stars (color anchor for the entire cosmograph)
- 4 attribute stars (cardinal-direction anchors)
- 6 T4 strategy stars (extra-bright; capstone-keystone rendering)
- 16 skill-geometry stars
- ~30+ skill-tree-position stars (T1/T2/T3/T4 × chain-positions)
- 4 scaling-pattern stars
- 6 investment-scaling-pattern stars
- 5 resource model stars
- ~200 weapon-form token stars (drillable zoom-in within 15-gear catalogue clusters)
- Off-hand item substrate stars (parallel to main-weapon)
- Per-season race + racial-trait stars (visible/active per current season's rotation)
- 8 BC-axis × bin-label stars (34 atomic positions)

**Estimated star count (with Matt's additions):** ~100-150 first-class atomic stars + ~200 weapon-form drillable zoom-in stars + per-season race/trait stars (variable per season-design) = **~300-400 rendered stars per active season.**

### 6.2 Layer 0.5 combinatory operators render as AXIS PAIRS / EDGES

The 5 combinatory operators (§ 2.1-2.5) render as axis-pair edges or interactive sliders:

- Element-count → kit_architecture (binary toggle in UI)
- Element × sub-element scope (per-primary flavor pool palette)
- Main + off-hand combinatorics (parallel substrate axis with bridge-edge to main)
- Race × element-attribute interaction (race-coherence overlay on element-attribute stars)
- Seasonal-substrate-rotation (per-season visibility/activity overlay)

### 6.3 Layer 1 derived fields render as LABELED OVERLAYS on constellations

The Layer 1 fields (bc_axis_signature; weapon_type_family; kit_architecture; etc.) are NOT additional stars; they are LABELS on constellation (kit) shapes that emerge from atomic primitive composition. The cosmograph side panel shows these as "this kit's BC tuple = (close-fast / chain / mid / spiky / mitigator / energy)" — derived information.

### 6.4 Layer 2 + Layer 3 + Naming Layer attach to constellations as SIDE-PANEL CONTENT

When the player lassoes a region → matched constellation, the side panel surfaces:
- Layer 2 experiential profile (Maxroll 5-axis radar; archetype label; investment-tier badge)
- Layer 3 vestigial-class label ("Magic-Find Sorceress")
- Naming Layer N1 (per-skill names with flavor element)
- Naming Layer N2 (kit identity name + narrative)
- Naming Layer N3 (faction context)
- Naming Layer N4 (season name overlay)

### 6.5 Constellations CROSS LAYERS

A constellation (kit) is a pattern of atomic primitive stars connected by lines. The connections cross Layer 0 substrate-families (element + attribute + weapon-form + T4-strategy + skill-tree-position + ...). The cosmograph SHOWS HOW atomic substrate composes up to player-facing identity.

### 6.6 Seasonal-substrate-rotation animates the cosmograph

Per Matt 2026-06-06 vision: each season's rotation activates/deactivates certain regions of the cosmograph:
- S1 (Tolkien): Tolkien race stars + Celtic-Norse cultural-tradition stars active
- S2 (Warhammer): Warhammer race stars active; Celtic-Norse held active for continuity
- S3 (Warhammer + Aztec/Indo-Asian): Warhammer race held; Celtic-Norse deactivated; Aztec + South-Asian cultural-tradition stars activated

The cosmograph BECOMES the seasonal-rotation visualization. Players see which substrate is in play this season; held axes appear stable; rotated axes appear in flux. The Earth Self watches the firmament shift.

---

## 7. Cross-references

### 7.1 Composes with (existing canon)

- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 3 (cell schema — Layer 1+) + § 4 (flag enum — Layer 2+ flags) + § 5 (Phase A-E roadmap)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.5.1 (6-step content lifecycle) + § 1 (engine workflow phases)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (gear + balance + multi-T4 architecture)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` (scaling-pattern-per-tier)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` (investment-scaling 6 patterns)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes; 68,040 cells)
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` (15-gear catalogue + priority hierarchy)
- `canonical/historical/09-geometry-palette-discussion.md` (16-type geometry palette)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (per-primary flavor pool)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system)
- `canonical/story/off-hand-items-2026-05-24.md` (off-hand parallel substrate)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` (BDI ω/τ composed-primitive identity)
- `canonical/story/weapon-substrate-conclusion-declaration.md` (89,839-row weapon substrate)
- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` (Realm Expansion content rhythm — composes with seasonal-substrate-rotation)
- `canonical/story/2026-06-05-cosmograph-pivot.md` (cosmograph architectural commitment — consumes this registry)

### 7.2 Anticipates (future canonical)

- Per-season race-set + racial-trait pool authoring (S1 Tolkien set; S2 Warhammer set; etc.)
- Per-season seasonal-substrate-rotation lock per season-design
- Pattern library Phase A `pattern_library.db` schema (consumes Layer 0 + Layer 0.5 + Layer 1)
- Cosmograph `/forge` build (consumes this registry for primitive star vocabulary)

### 7.3 Does NOT replace or amend

- Does NOT replace hypothesis-flow doc (which captures Layer 1+ and flag enum)
- Does NOT amend canonical 39 / 40 / 47 / 51 / qd-engine-bc-axes-lock — references them as authoritative source for Layer 0 enumeration

---

## 8. Sign-off

**Authored:** gandalf 2026-06-06 per Matt verbatim ratification of Path B + race + skill-tree-position + seasonal-substrate-rotation + Depth-2 derivation + Naming Layer stack
**Authority:** Matt 2026-06-06 multi-iteration design call (this session)
**Anchor evidence:** all referenced canonical docs in § 7.1 + Matt 2026-06-06 directives captured verbatim throughout

**This registry is the Layer 0 + Layer 0.5 enumeration that the hypothesis-flow doc (2026-05-31) referenced but did not enumerate. Together they constitute the cemented future-state architecture: Layer 0 + 0.5 (this doc) + Layer 1 + 1.5 + 2 + 3 (hypothesis-flow doc § 3) + N1-N4 Naming Layer (this doc § 5) = the full substrate hierarchy for the engine and the cosmograph.**

**Numbered canonical promotion candidate.** This doc is architecturally load-bearing enough to warrant numbering (canonical 52). Deferred to Matt directive.

**Next steps in this workstream:**
1. Amend hypothesis-flow doc to CANONICAL status with cross-reference to this doc
2. Amend cosmograph-pivot doc (2026-06-05) with this doc + hypothesis-flow doc as architectural anchors
3. Author elrond + drax cosmograph commission specs (consumes Layer 0 + Layer 0.5 from this doc; Layer 1+ + flag enum from hypothesis-flow doc)
4. Update ground-state oracle § 1 with this doc + hypothesis-flow CANONICAL amendment

**End of Atomic Substrate Registry.**
