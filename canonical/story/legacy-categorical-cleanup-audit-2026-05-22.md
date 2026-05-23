# Legacy Categorical Cleanup Audit — Six Vestigial-Pattern Retirements

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Date:** 2026-05-22 (evening session; canonical audit)
**Author:** gandalf (story-and-design steward; senior designer)
**Status:** v1 canonical lock — six categorical-pre-imposition retirements audited, named, replaced; per-surface cleanup checklist scoped
**Authority:** Matt 2026-05-22 evening — six canonical retirement calls executed in a single architectural cleanup pass
**Companion docs (this session):**
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C strategic lock (`f72690f`)
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — replacement for "traits carry stats" (companion to Pattern 3)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — vast-library substrate pivot (companion to Patterns 4-5-6)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — operationalizes the post-retirement substrate work

---

## 0. TL;DR

In one evening session, six vestigial categorical-pre-imposition patterns were retired from the engine architecture. **They are all the same shape.** Each was a pre-W0.2 (pre-substrate-as-cohesion) commitment that imposed identity *before* generation, where substrate-as-cohesion requires identity to *emerge* from generation.

| # | Pattern retired | Pre-imposed (old) | Emergent (new) |
|---|---|---|---|
| 1 | Archetype | `mage_controller`, `physical_rogue`, etc. as generation surface | Mechanical signature emerges from kit generation; archetype labels are post-hoc diagnostic |
| 2 | role_orientation | `damage / control / support / hybrid` (4 buckets) as rule-table input | Role flavor emerges from 8 BC axes post-convergence |
| 3 | Traits-carry-stats | Trait pool determines stats (B9a) | Stats are derived projection of (element_scaling_attribute × per-axis BC magnitudes); traits become optional identity modulators v1.1+ |
| 4 | Pre-imposed aesthetic-tuple dimensions | `5 tech × 4 tone × 6 culture = 120 tuples` as substrate axes | Aesthetic clusters emerge from imported weapon library |
| 5 | 15-entry gear catalogue | `greatsword / wand / censer / ...` as generation-input enumeration | Gear-form clusters emerge from the vast weapon library; designer post-hoc labels them |
| 6 | **The axes themselves** (deepest layer) | Pre-imposed dimensions: `tech / tone / culture` + `range / geometry / timing / charge / accuracy / rhythm` as axis definitions | **Axes derived from statistically significant sample (≥1,000 weapons) via PCA / factor analysis on extracted feature vectors; axes earned, not assigned** |

**The systematic insight worth canonical capture:** vestigial categorical pre-imposition tends to survive cleanup at one layer by hiding in the next. The 15-entry catalogue was a vestigial child of archetype taxonomy. The aesthetic-tuple dimensions were a parallel vestigial overlay. The role_orientation taxonomy was vestigial categorical role-imposition. The "traits carry stats" framework was vestigial stat-assignment-by-categorical-role. The archetype concept itself was vestigial pre-W0.2 categorical generation surface. The *axes* are the deepest layer — when you retire the values within an axis, the next vestigial question is whether the axis itself was pre-imposed.

**The audit principle going forward:** when something feels categorical, check whether it's pre-imposition disguised as natural taxonomy. Ask the substrate-as-cohesion question: *does this thing emerge from the substrate, or was it imposed before generation ran?* If the latter, it's a vestigial-pattern candidate.

This document captures the six retirements as canonical engineering wisdom and provides the per-surface cleanup checklist (engine code + canonical docs + memory files + telemetry schemas + dispatches).

---

## 1. The systematic insight — categorical pre-imposition as recurring vestigial pattern

### 1.1 Where the patterns came from

Pre-W0.2 (before substrate-as-cohesion was the architectural commitment), the engine generated via a categorical pipeline:

```
1. Pick an archetype from a fixed enumeration (mage_controller, physical_rogue, ...)
2. The archetype determined role (damage / control / support / hybrid)
3. The role determined stat distribution (INT-dom / WIS-dom / STR-dom)
4. The role + archetype determined gear (from a 15-entry catalogue)
5. The gear came with an aesthetic tuple (tech × tone × culture)
6. Stats were assigned via the trait pool the archetype owned
```

Every layer was a fixed, pre-imposed taxonomy. The engine never *discovered* anything — it *selected from* pre-built lists.

Substrate-as-cohesion (W0.2 onward) inverted this:

```
1. Element substrate (mechanically baked: damage types, scaling attribute) feeds into kit generation
2. Kit generation runs substrate-agnostic with the mechanical BC axes as the convergence surface
3. Stats are derived projection of (element_scaling_attribute × per-axis BC magnitudes)
4. Mechanical signature emerges from convergence
5. Aesthetic identity emerges from weapon-substrate selection during convergence
6. Cluster identity emerges from multimodal clustering of cemented kits
7. Faction/archetype labels (if surfaced at all) are post-hoc cluster names, not generation inputs
```

The old pipeline was *additive* (here are the categories; pick one of each). The new pipeline is *emergent* (here is the substrate; let convergence + clustering reveal what shape the population takes).

### 1.2 Why vestigial patterns survive cleanups

When the substrate-as-cohesion commitment landed at W0.2, the engine did not become substrate-as-cohesion overnight. The architectural commitment was made; the implementation carried legacy taxonomic surfaces forward because:

- **Pragmatic continuity.** Cleanup costs are high; legacy surfaces stayed wherever they could be hand-waved as "diagnostic" or "convenience."
- **Categorical thinking is cognitively cheap.** "What archetype is this?" is easier to reason about than "what's the converged mechanical signature of this kit?" Designers and code paths alike fell back to the easier mental model.
- **One-layer cleanups feel complete.** When archetype was retired as a generation input (W0.2), it survived as a *diagnostic label*. That looked like a clean retirement. But the next layer down (role_orientation, gear catalogue, aesthetic-tuple dimensions) inherited the same categorical logic — and those layers did not get retired in W0.2.
- **Dependencies hide upstream pre-imposition.** Telemetry schemas had `archetype_id` fields; canonical docs had archetype lists; memory files captured archetype rationale. Each downstream consumer of a pre-imposed value extended the lifespan of the pre-imposition.

The pattern is recursive: **each cleanup reveals the next vestigial layer.** Tonight's six-retirement pass demonstrates the recursion all the way down through the axes themselves.

### 1.3 The audit principle going forward

When auditing any architectural surface, apply this checklist:

1. **Is this value pre-imposed or emergent?** Pre-imposed values are vestigial candidates.
2. **Does it enter generation, or does it come *out of* generation?** If it enters generation, it's a substrate input — and substrate inputs must be either (a) mechanically necessary primitives (element substrate, BC axes as measurement targets) or (b) data the engine queries (weapon library, knowledge entries).
3. **Could this value be derived from a more primitive substrate?** If yes, the categorical surface is vestigial pre-imposition; derive it instead.
4. **Was this value's enumeration designer-authored or data-discovered?** Designer-authored enumerations are vestigial candidates when the data exists to discover them empirically.
5. **Does the next layer down also need auditing?** Categorical pre-imposition tends to nest. When you retire a value, audit the axis it lived on. When you retire the axis, audit the rule-table the axis fed into. When you retire the rule-table, audit the consumers downstream.

This is the auditing voice. It should be applied whenever a new architectural surface lands and whenever an existing surface needs revisiting.

### 1.4 ARPG canon parallel — what other studios got wrong by missing this

Diablo III shipped with a fixed-class fixed-skill-tree taxonomy where every class had a pre-imposed "what it is." Player builds emerged within categorical constraints. The expansion (Reaper of Souls) added Adventure Mode + Nephalem Rifts but kept the categorical scaffold; the categorical commitment couldn't be unwound. Diablo IV inherited it. The engine never asked "what if class identity emerged from kit composition?" because the pre-imposition was canonical from launch.

Path of Exile took the inverse approach: a single passive tree shared across classes, ascendancies as post-hoc identity layers, and skill-gem-as-substrate where every active skill is the gem, not the class. PoE's "what archetype is this build?" is a question the player asks the build, not a question the engine asks the player. The categorical pre-imposition is minimal — class is a starting position on the tree, not a pre-imposed identity that cascades through stats/gear/skills.

Last Epoch sits between: classes have skill trees (pre-imposed), but the masteries + skill specializations let identity emerge within wider lanes. The categorical commitment is softer than D3 but harder than PoE.

**Reincarnated under substrate-as-cohesion is closer to PoE's structural commitment than D3's.** The vestigial-pattern audit is what makes this real architecturally rather than aspirational. If the engine carries pre-imposed archetypes, role_orientations, traits-carry-stats, hand-authored catalogues, and pre-imposed axis dimensions, then it is structurally Diablo III with substrate-as-cohesion language painted on top. The audit unwinds the categorical commitment so the substrate-as-cohesion commitment is real.

---

## 2. The hierarchy of retirements — patterns 1-5 vs pattern 6

The six retirements fall into two tiers:

**Tier 1 — Retirements within axes (Patterns 1-5).** These retire *values* within an axis, or replace categorical enumerations with derived/emergent populations. The axes themselves were assumed sound. Examples:
- Archetype retirement (Pattern 1) retires the values `mage_controller`, `physical_rogue`, etc. but the axis "what is this kit's mechanical identity?" stayed.
- Aesthetic-tuple retirement (Pattern 4) retires the pre-imposed enumeration `5 tech × 4 tone × 6 culture` but the axes "tech level", "tone", "cultural lineage" stayed as descriptive vocabulary.
- 15-entry catalogue retirement (Pattern 5) retires the hand-authored list but the *concept* of "gear forms" stayed; emergent clusters fill the same slot.

**Tier 2 — Retirements of the axes themselves (Pattern 6).** This retires the *axis definitions*. The deepest possible cut. Examples:
- The aesthetic axes themselves (`tech_level`, `tone`, `cultural_lineage`) become candidates for retirement-as-axes if PCA on a large-enough weapon-knowledge sample produces *different* axes that explain more variance.
- The mechanical-property axes (`range`, `geometry`, `timing`, `charge`, `accuracy`, `rhythm`) become candidates if the same statistical pass on geometric+mechanical feature vectors reveals more parsimonious axis-sets.

**Why the distinction matters:** Tier 1 retirements are cheaper and more local. Tier 2 retirements ripple through every consumer of the axis. Pattern 6 is the deepest retirement in the audit because it touches the most surfaces.

**The audit principle restated under this hierarchy:** when you retire values within an axis (Tier 1), audit whether the axis itself was pre-imposed (Tier 2). Categorical pre-imposition hides one layer beneath each cleanup. The discipline is to keep asking the question at each layer.

---

## 3. Per-pattern detail

Each subsection below covers one retirement: what was vestigial, where it originated, why it survived prior cleanups, what replaces it, and the per-surface cleanup checklist.

### 3.1 Pattern 1 — Archetype as generation surface

**What was vestigial:**
`archetype` as a generation-input enumeration: `mage_controller`, `physical_rogue`, `holy_caster`, `support_cleric`, etc. The engine would select an archetype, and the archetype would determine downstream selections (role, gear, skill set, stat distribution, naming).

**Pre-W0.2 origin:**
The original Phase 0 generation pipeline (pre-2026-04) used archetype templates as the primary structuring object. Each archetype had a YAML/JSON definition with: associated role, gear family, stat priorities, skill pool, name patterns. Generation was "select archetype, instantiate from template, fill in seed-specific variation."

**Why it survived W0.2:**
The W0.2 substrate-as-cohesion commitment retired archetype *as substrate primitive* (the engine no longer reasoned about archetype during convergence). But archetype labels stayed as **diagnostic identity** for telemetry, cohesion-judge prompts, attribution tooling, and designer language. The diagnostic role was a clean retirement-by-half: archetype was no longer a generation input, but it was still a thing the engine reasoned about post-hoc.

The half-retirement meant downstream surfaces kept consuming archetype as if it were canonical: dispatches referenced archetypes by name, memory files captured archetype-centric design rationale, balance work (B14.5 sidecar analyses) reported per-archetype metrics. The diagnostic role grew teeth.

**What replaces it under substrate-as-cohesion:**
Kits have a **converged mechanical signature** — the 8 BC axis values + element substrate + weapon substrate + stats. The signature is rich enough to support identity recognition without an archetype label.

Where archetype labels were used:
- **Telemetry attribution** → use mechanical-signature hash + cluster_id (once clustering lands) for grouping
- **Cohesion-judge prompts** → cohesion-judge reads the converged kit + weapon aesthetic tuples and produces the thematic identity inline; the engine does not feed it an archetype label
- **Designer language** → use "reference build" for ARPG-canon descriptive labels ("Stormcaller-pattern build", "Smiter-pattern build"); this is *descriptive* vocabulary, not a generation primitive
- **Balance attribution (W0.7 LC-attribution work)** → diagnostic-only legacy groupings (`mage_controller`, `physical_rogue`) remain available for backward-compatibility on historical telemetry; new analyses should use mechanical-signature clusters

**Per-surface cleanup checklist:**

| Surface | Action |
|---|---|
| `~/Games/reincarnated-engine/src/reincarnated/canonical/archetype_templates/*.yaml` | Audit — files may still exist as legacy reference; should not be loaded as generation inputs |
| Engine code: any `archetype_id`, `archetype_name`, `archetype_template` references | Audit for generation-path usage; allow only in legacy attribution code paths |
| Telemetry schemas: `archetype_id` column | Mark deprecated; new records can write `null`; preserve column for historical-query support |
| Canonical docs referring to "archetype" as concept | Audit each; substitute "gear substrate" / "reference build" / "mechanical signature" per context |
| `memory/project_role_orientation_taxonomy.md` | Mark historical/diagnostic-only |
| Dispatches that use archetype as instruction | Audit for new dispatches; old dispatches stand as historical record |
| `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` § 2 catalogue table | Already renamed Archetype → Gear; complete the full restructure |
| Cohesion-judge prompts | Audit for archetype-injection; cohesion-judge should read kit substrate directly |

### 3.2 Pattern 2 — role_orientation as rule-table input

**What was vestigial:**
`role_orientation` as a 4-bucket enumeration (`damage / control / support / hybrid`) used as a generation-input dimension for the gear rule-table (and elsewhere). Each kit was assigned a role; the role determined gear selection within the rule-table and stat-priority signaling.

**Pre-W0.2 origin:**
The role-orientation taxonomy was established 2026-05-08 (`memory/project_role_orientation_taxonomy.md`) as part of the Phase 2 dimensional-generation refactor. It was meant as a structural primitive: four canonical roles that any class fits into. It paired with the archetype templates as a coordinate system for kit identity.

**Why it survived W0.2:**
role_orientation looked like it was *measurement* (a kit either does damage or control or support; this is a fact about the kit). But it was *pre-imposition* (we assigned the role before generation; generation then satisfied the role). The substrate-as-cohesion commitment retired archetype-as-input but role_orientation was treated as orthogonal: archetype was the kit's identity, role was the kit's function. Both were still pre-imposed; only one got retired.

The role_orientation taxonomy carried forward into:
- The gear rule-table (`canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` original 252-combination structure used role as 2nd axis)
- BDI ω/τ tables (per-element role-specific affinity tuning)
- Class-template stat distribution decisions
- Telemetry attribution patterns

**What replaces it under substrate-as-cohesion:**
**Role emerges from the 8 BC axes post-convergence.** The relevant axes are:
- Axis 3A damage tempo + Axis 3B amplitude variance → damage-class flavor
- Axis 2B control density → control-class flavor
- Axis 2A proxy density → support-class flavor (in multi-actor contexts; per `project_role_orientation_taxonomy.md` 2026-05-08 — "support is gated to multi-actor contexts" was correctly captured then)
- Axis 4 defensive profile → tank-class flavor
- Axis 1 range + mobility → engagement flavor

A kit that converges to high damage tempo + low control density + low proxy density is a damage class. A kit that converges to high control density + moderate damage tempo is a controller. These are *measurements*, not assignments. The engine reads them off the converged kit; it does not need to be told "this is a damage class" before generation runs.

**The diagnostic-only legacy:** the `mage_controller` / `physical_rogue` style groupings used in W0.7 LC-attribution work remain available as **legacy diagnostic-only attribution tooling**. New analyses should use BC-axis-measurement-based clustering. Old analyses stand.

**Per-surface cleanup checklist:**

| Surface | Action |
|---|---|
| `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` sections 4-9 | Full restructure pending (noted in current doc); collapse 252-combination structure to 63-combination v1 by dropping role_orientation axis; per-combination role-emergence is post-convergence |
| `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` | Recalibrate ω/τ tables under role_orientation drop; per-element ω weights become role-agnostic; role flavor emerges from convergence |
| `memory/project_role_orientation_taxonomy.md` | Mark historical/diagnostic-only (per skill_handoff § 9.5) |
| Engine code: any `role_orientation` parameter in generation paths | Remove from generation inputs; allow in diagnostic/attribution code paths only |
| Telemetry schemas: `role_orientation` column | Mark deprecated; future records can write null; preserve for historical queries |
| Cohesion-judge prompts | Audit for role-injection; cohesion-judge reads converged BC axes directly |
| Class-template stat distribution decisions | These now derive from element_scaling_attribute + per-axis BC magnitudes (see Pattern 3 + stat-derivation doc) |

### 3.3 Pattern 3 — Traits-carry-stats

**What was vestigial:**
The trait architecture (per `project_trait_architecture.md` 2026-05-12) treated traits as the load-bearing surface for stat assignment: B9a per-class intrinsic trait pool (5-10 traits, floors at L1/12/25/38, converge at L50) was where stats came from. The trait pool determined the class's stat distribution; gear-affix rolls (D9) added marginal stat variation.

**Pre-W0.2 origin:**
The trait-stats coupling was a Priority-14-era commitment (the original "Traits and Skills" progression sketch, predecessor to the current Stage A7 / B9 series). When traits became the canonical progression surface (file 32 + file 33), stats inherited from trait selections. Each archetype had a trait pool; each trait granted stat increments; stats were a downstream consequence of trait selection.

**Why it survived W0.2:**
Substrate-as-cohesion retired archetype-as-input but did not touch the trait-stats coupling because traits were not framed as categorical. Traits look continuous (each trait grants increments; you can stack them; rank-up modifies magnitudes). The substrate-as-cohesion audit (W0.2) targeted obvious categorical surfaces; the trait-stats coupling looked sufficiently emergent to escape audit.

But the coupling was vestigial in a more subtle way: **stats were treated as an additive consequence of categorical choices (which traits)** rather than as a **derived projection of the substrate's mechanical signature**. The categorical layer was the trait pool; the trait pool was per-archetype; archetype is retired. Therefore the trait-stat coupling was carrying forward a vestigial dependency on archetype.

**What replaces it under substrate-as-cohesion:**
**Stats are derived projection of (element_scaling_attribute × per-axis BC magnitudes).** This is the canonical replacement, captured in detail in the companion doc `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md`.

In short:
- Element substrate has a canonical scaling attribute (fire/water/lightning/shadow → INT; earth/wind/holy → WIS; physical → STR per the excluded canonical-7)
- The 8 BC axes have measured magnitudes per kit after convergence
- Stats are derived by projection: element_scaling_attribute is the primary damage stat; other stats follow from per-axis-necessity mapping (see § 2 of the stat-derivation doc)
- Traits become **optional identity modulators v1.1+** — they may exist as flavor layers (a fire kit with the "Smoldering" trait gets cosmetic burn-aftershock; a tank kit with the "Bulwark" trait gets a thematic defensive flourish), but they are **not load-bearing for stats**

**Per-surface cleanup checklist:**

| Surface | Action |
|---|---|
| `memory/project_trait_architecture.md` | Mark legacy / borderline vestigial under BC-axis-derived stats framework (per skill_handoff § 9.5) |
| `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` | Audit for trait-stats coupling references; flag for revision under new stat-derivation framework |
| `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` | Mark as v1.1+ optional-identity-modulator design; not load-bearing for v1 stats |
| `canonical/story/d8-trait-floor-design-phase-1-p1.md` | Same as above |
| `canonical/story/d9-gear-affix-design-phase-1-p1.md` | Audit: gear affixes can still roll stat affixes (the *gear* carries marginal stat variation); but the *base* stats come from BC-axis derivation, not trait sum |
| Engine code: trait-to-stat application paths | Replace with BC-axis-derivation pipeline; trait paths become optional flavor layer for v1.1+ |
| Telemetry schemas: any "trait gave stat X" attribution | Replace with "BC-axis-derived" attribution for v1; preserve historical |

### 3.4 Pattern 4 — Pre-imposed aesthetic-tuple dimensions

**What was vestigial:**
The aesthetic-tuple matrix (`5 tech × 4 tone × 6 culture = 120 tuples`) used as a **substrate axis system** for visual/cultural identity. Each weapon in the catalogue carried a tuple; the matrix was the closed enumeration of valid tuples; engine flags reference `cultural_lineage_register` as a list of tuples.

**Pre-W0.2 origin:**
The aesthetic-tuple vocabulary emerged from designer brainstorming about the visual register Reincarnated wanted to span. Tech-level (primitive / medieval / industrial / advanced / post-singularity) × tone (heroic / grim / mystical / playful) × cultural-lineage (European / East-Asian / South-Asian / Mesoamerican / African / fictional-hybrid) gave a coordinate system for talking about visual identity.

The 120-tuple matrix was useful as a *thinking tool*. Where it became vestigial was when it got promoted to a *substrate axis system* — when generation, cohesion-judging, and engine flags started treating the tuple list as canonical inputs.

**Why it survived prior cleanups:**
The substrate-as-cohesion commitment was about *mechanical* substrate (BC axes, element). Aesthetic substrate was a parallel concern; the audit didn't touch it because mechanical/aesthetic separation looked clean. But the same categorical pre-imposition pattern was operating: **the tuple list was designer-authored, not data-derived.** The closed enumeration was a vestigial taxonomy.

The vestigial pattern showed up when:
- Engine flags listed `cultural_lineage_register = [tuples]` as if the tuple list were canonical
- The gear catalogue carried per-entry tuple assignments
- Cohesion-judge prompts referenced tuples as ground-truth identity
- v1 scope debates anchored on "which tuples does v1 cover?" (medieval-spanning vs sci-fi-deferred) as if the tuples were the substrate

**What replaces it under substrate-as-cohesion:**
**Aesthetic clusters emerge from the imported vast weapon library.** The pivot is captured in detail in the companion doc `canonical/story/gear-heavy-promotion-2026-05-22.md`. In short:

- The weapon library (15,000-30,000 knowledge entries per the orchestration plan) carries rich textual + structured + visual + cultural-lineage data per weapon
- PCA / factor analysis on extracted feature vectors discovers *empirical* aesthetic axes (see Pattern 6 for the deeper axis-discovery framing)
- Clusters emerge from the data; designer post-hoc labels them with semantic vocabulary
- The aesthetic-tuple vocabulary (`tech_level`, `tone`, `cultural_lineage`) survives as **descriptive language** for cluster labeling, not as **generation input**

The matrix becomes a *thinking tool again*. It is not the substrate.

**Per-surface cleanup checklist:**

| Surface | Action |
|---|---|
| `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` § 3 + § 6 | Amend to retire `cultural_lineage_register` as pre-imposed-tuple-list; replace with cluster-id-list reference (per § 6 optional sixth amendment in skill_handoff) |
| `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` § 2 catalogue | Aesthetic-tuple assignments become *hypotheses* for cluster identification post-import, not canonical pre-imposed values |
| Engine flags: `cultural_lineage_register` schema | Change from `List[tuple]` to `List[cluster_id]`; cluster_id references the clusters table populated post-import |
| Cohesion-judge prompts | Cohesion-judge reads cluster identity (post-clustering) + weapon aesthetic descriptors (per-weapon, free-text), not pre-imposed tuples |
| Q1 aesthetic-tuple matrix proposal (per skill_handoff C6) | Demoted to "cluster-naming hypothesis" reference — designers can still use the matrix as a mental model; the substrate is the data |
| Memory files referring to aesthetic tuples | Audit; preserve descriptive language; remove "substrate axis" framing |

### 3.5 Pattern 5 — 15-entry gear catalogue

**What was vestigial:**
The 15-entry gear catalogue (`gear-as-substrate-2026-05-21.md` § 3) used as a **closed enumeration** of valid gear forms: greatsword, twin daggers, battle spear, mace/warhammer, longbow, crossbow, blunderbuss, throwing knives/chakram, wand/focus rod, orb/sphere, caster staff, tome/grimoire, censer/thurible, holy symbol/icon, war-trumpet/horn.

**Pre-W0.2 origin:**
The 15-entry catalogue was a designer-authored synthesis of ARPG canon (D2/D3/PoE weapon families) + thematic-class signaling. It captured "what kinds of weapons does this engine know about" as a finite, hand-authored list. Each entry was a generation-input enumeration: when the rule-table mapped substrate-vector → gear, the output was one of these 15 values.

**Why it survived prior cleanups:**
The 15-entry catalogue was treated as natural taxonomy because the entries were genre-canonical. Greatsword is a thing in ARPGs; wand is a thing; censer is a thing. The categorical list looked descriptive rather than prescriptive.

But the categorical pre-imposition was still operating: **the engine did not know about any gear form outside the 15 entries.** A katana? Not in the catalogue. A kpinga (African throwing weapon)? Not in the catalogue. A bolas, a shuriken, a war fan, a Mesoamerican macuahuitl? Not in the catalogue. The hand-authored list constrained what could be generated; the constraint was invisible because the catalogue felt comprehensive in a Eurocentric medieval-spanning frame.

Per legolas's Unity catalogue findings: Asset Store coverage is "asymmetric (medieval-European saturated; non-European thin or absent)" — which mirrors exactly the catalogue's coverage shape. The catalogue inherited the genre's biases.

The vestigial pattern showed up when:
- The rule-table enumerated 252 (or 63) combinations because the output space was 15 × element × range × stat-dist
- Memory files referenced "15 archetypes" as canonical
- Telemetry schemas had `gear_catalogue_id` enums with the 15 values

**What replaces it under substrate-as-cohesion:**
**The vast weapon library is the substrate.** Per the companion doc `canonical/story/gear-heavy-promotion-2026-05-22.md` and the orchestration plan:

- Knowledge crawls populate ~15,000-30,000 weapon knowledge entries (Wikipedia + Wikidata + game wikis + SRD + museums + anime/manga wikis)
- 3D model libraries (Sketchfab + Kenney + OGA + Smithsonian; Phase D Meshy gap-fill) attach as visual references
- PCA / factor analysis on feature vectors discovers emergent gear-form clusters (per Pattern 6)
- Clusters emerge from the data; designer post-hoc labels them
- The 15-entry catalogue is demoted from "canonical taxonomy" to "hypothesized clusters" — predictions that emergent clustering may or may not validate

The hypothesis test: do the empirical clusters match the 15 predicted families? Some will (greatsword cluster will likely appear; wand cluster will likely appear). Some won't (the catalogue's "Censer / thurible" entry may merge into a broader "ritual implement" cluster; the "War-trumpet / horn" entry may merge into "ceremonial sound-instrument"; cultural-lineage clusters will likely surface that the 15-entry catalogue elided).

**Per-surface cleanup checklist:**

| Surface | Action |
|---|---|
| `canonical/story/gear-as-substrate-2026-05-21.md` § 3 | Mark as "v0 hypothesized clusters; superseded by emergent clusters from imported library"; preserve as historical reference |
| `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` § 2 catalogue + § 4 rule-table | Full restructure pending; the 15-entry enumeration is demoted to hypothesis; post-clustering, the rule-table is replaced by substrate-vector → cluster_id queries |
| Engine code: `gear_catalogue_id` enum | Replaced by foreign-key to `weapons` table (per-weapon) + `cluster_id` (for cluster identity); the enum is deprecated |
| Telemetry schemas: `gear_catalogue_id` enum column | Migrate to `weapon_id` (FK to weapons) + `cluster_id` (FK to clusters); preserve old enum column for historical queries |
| Cohesion-judge prompts | Reads cluster identity (post-clustering) + per-weapon descriptors, not the 15-entry enumeration |
| Memory files referencing "15 archetypes" | Audit; mark legacy; use "emergent clusters" framing forward |
| Asset pipeline docs | Update to reference vast-library substrate + cluster identification, not 15-entry enumeration |

### 3.6 Pattern 6 — The axes themselves (deepest retirement)

**What was vestigial:**
The **axis dimensions themselves** as designer-authored coordinate systems:
- Aesthetic axes: `tech_level / tone / cultural_lineage` as the 3-axis system for aesthetic identity
- Mechanical-property axes: `range / geometry / timing / charge / accuracy / rhythm` as the canonical 6-dimension system for gear mechanical properties

Both axis-sets were hand-defined. The aesthetic axes came from designer brainstorming. The mechanical-property axes came from W0.2 substrate-as-cohesion architectural work (informed by ARPG canon).

**Pre-W0.2 origin / W0.2 partial cleanup:**
The mechanical-property axes were *measurement axes* (per Discipline #2 / Discipline #1 architectural commitments: BC axes are *measured* on cemented kits, not assigned during generation). So they were ostensibly already substrate-as-cohesion-coherent.

But the question Pattern 6 retirement asks is sharper: **were the right axes chosen?** The mechanical-property axes were *chosen by designers* as the right axes to measure. The aesthetic axes were *chosen by designers* as the right axes to describe. Both were pre-imposed at the axis-definition layer.

The vestigial pre-imposition is the axis-set itself. Even if values are measured (not assigned) per-kit, the *fact that we measure along these 6 (or 3) axes specifically* is a designer-authored taxonomy.

**Why it survived all prior cleanups:**
The axis-set is the deepest layer. Patterns 1-5 retire values within axes; Pattern 6 retires the axes themselves. Nobody asks "is this axis the right axis?" because the axis feels like the coordinate system itself, not a categorical choice.

But it is a categorical choice. There are infinitely many possible axis-sets. The one we chose came from designer intuition + ARPG canon. The audit principle (substrate-as-cohesion) asks: **could the axes themselves be derived from the substrate?** And the answer is yes, if we have a large enough sample to do statistical axis discovery.

**What replaces it under substrate-as-cohesion:**
**Axes derived from statistically significant sample (≥1,000 weapons) via PCA / factor analysis on extracted feature vectors.** The orchestration plan § 2 Phase 2 D7b spells this out in detail:

> Per Matt 2026-05-22 evening canonical call: the aesthetic axes and the geometrical/mathematical mechanical variables must be DERIVED from a statistically significant sample, NOT pre-imposed. This is the sixth vestigial-pattern retirement of the evening (categorical pre-imposition at the AXIS level).

Statistical methodology candidates (per the orchestration plan):
- **PCA** (Principal Component Analysis) — linear; produces orthogonal axes explaining variance
- **Factor Analysis** — identifies latent factors; more interpretable for semantic axes
- **UMAP / t-SNE** — non-linear; good for visualization + cluster prep, less interpretable as canonical axes
- **Sparse PCA / NMF** — produces sparse loadings; more interpretable axis definitions
- **Mixed-effects:** PCA on geometric/mechanical features + Factor Analysis on semantic/visual features

**Expected outcome of axis discovery on knowledge-entry feature vectors:** the discovered axes will be substantive and substrate-rooted. Candidates per the plan:
- Edged-vs-blunt
- One-vs-two-handed
- Melee-vs-projectile
- Cultural lineage (likely surfaces from museum + cultural-tag metadata)
- Historical-vs-fictional
- Ceremonial-vs-utility
- Genre-anchored (fantasy vs sci-fi vs historical-fiction vs anime)

These are *real substrate dimensions*. The pre-imposed tech × tone × culture trio may or may not survive; the pre-imposed range/geometry/timing/charge/accuracy/rhythm sextet may collapse to a more parsimonious 4-axis set or expand to an 8-axis set. The data tells us.

**The empirical commitment:** Patterns 1-5 retire pre-imposed *values*; Pattern 6 retires pre-imposed *axes*. The audit goes to the deepest layer because the substrate-as-cohesion commitment is to let identity emerge from the substrate — and "what axes describe the substrate" is itself an emergent question once enough substrate is available.

**Per-surface cleanup checklist:**

| Surface | Action |
|---|---|
| `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC axes definitions) | Audit post-axis-discovery; the 8 BC axes are *measurement axes for mechanical convergence* (a different concern from gear-substrate axes); may survive Pattern 6 audit cleanly OR may need revision if axis discovery surfaces collapsed/expanded axis sets |
| `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` § 3.2 Engine-level flags | Amend post-axis-discovery; flags currently reference pre-imposed tuple dimensions; update to reference discovered-axis dimensions |
| Engine code: any `tech_level` / `tone` / `cultural_lineage` axis usage | Pending axis-discovery; current usage stands as Tier-1 cleanup target (Pattern 4 retirement); Tier-2 retirement waits on D7b results |
| `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` § 1 input dimensions | Reframe: input dimensions are *derived axes from clustering*, not pre-imposed `range_profile` / `stat_distribution_signature`; the rule-table itself becomes substrate-vector queries against clusters |
| Telemetry schemas: per-kit aesthetic/mechanical axis values | Migrate from pre-imposed-axis columns to derived-axis blob (post-axis-discovery); preserve historical |
| Cohesion-judge prompts | Read discovered-axis loadings + cluster identity, not pre-imposed axis values |
| Memory files referring to specific axis enumerations | Audit; mark legacy where axes change; update vocabulary forward |

**Pattern 6 is not yet operationally complete.** Patterns 1-5 are surface-cleaned in this session (with full restructure pending in companion docs). Pattern 6 requires the import + statistical-axis-discovery work to land (orchestration plan Phase 1 + Phase 2). The retirement is *committed canonically* tonight; the implementation lands across Phase 1-Phase 2 of the weapon library import workstream.

---

## 4. Surviving (not vestigial under audit)

Not everything categorical-looking is vestigial. The audit identified several surfaces that *survive* under substrate-as-cohesion's principles. They are listed here to make the audit's discriminating eye visible — categorical structure is not the diagnostic; *pre-imposition that should be emergent* is the diagnostic.

### 4.1 Element substrate

**Why it survives:**
Element substrate (fire / water / earth / wind / lightning / holy / shadow) is **mechanically baked**. Damage types, resistances, scaling attribute (per `element_biases.py:28` ELEMENT_SCALING_ATTRIBUTE) — element is a substrate primitive with mechanical consequences that drive the gauntlet sim's convergence.

It is categorical (7 values), but it is *substrate*, not pre-imposition-disguised-as-substrate. Element substrate's values exist because the engine's mechanical infrastructure treats them as load-bearing primitives — damage type interactions, element_scaling_attribute, element-derived VFX hooks.

**Watch-list note:** the 7-element substrate as a *closed list* is arguably itself a categorical commitment. Could there be an 8th element? A 6-element world? Probably yes; the 7 are designer-chosen + ARPG-canon. But the mechanical baking makes the list load-bearing enough that retirement-as-axes (Pattern 6 applied to element) is a v1.1+ question, not a v1 audit target. Flagged for explicit watch-list (§ 5).

### 4.2 The 8 BC axes (as measurement axes)

**Why they survive:**
The 8 BC axes are *measurement targets for mechanical convergence*. They are not generation inputs; they are observation surfaces. The engine generates kits substrate-agnostically; the BC axes are how we *describe* the kit's mechanical signature post-generation.

This is precisely substrate-as-cohesion's architectural commitment: identity (mechanical or otherwise) emerges from the substrate; the BC axes are the measurement vocabulary for that emergence.

**Pattern 6 caveat:** the *choice* of these 8 axes specifically is designer-authored (per § 3.6 above). Whether the right axes were chosen is a Pattern 6 question that the import + statistical axis discovery work will answer. The audit's working hypothesis is the 8 BC axes are sufficient for v1; revisit post-discovery if data surfaces parsimony or expansion candidates.

### 4.3 Mechanical-property measurement (range / geometry / timing computed not pre-imposed)

**Why it survives:**
Range, geometry, timing, charge, accuracy, rhythm — these are mechanical properties that the engine *computes per kit* from substrate behavior. The values are measured (continuous or bucketed), not assigned.

Compare to Pattern 6's deeper question (whether these specific 6 dimensions are the right ones), which is a Tier-2 audit. The Tier-1 fact — that *values* along these dimensions are computed, not pre-imposed — survives cleanly.

### 4.4 Aesthetic-tuple vocabulary (as descriptive language, not generation input)

**Why it survives:**
`tech_level`, `tone`, `cultural_lineage` are useful *descriptive vocabulary* for talking about aesthetic identity. A designer saying "this cluster reads as medieval-grim-European" is communicating clearly using this vocabulary.

What's retired (Pattern 4) is the *pre-imposed enumeration* used as substrate axes. The vocabulary survives as language. Cohesion-judge can use the vocabulary in prompts; designer docs can use the vocabulary in cluster labels; the engine flags should reference cluster_id (post-discovery), but the cluster labels themselves can use this vocabulary.

The distinction: vocabulary as *thinking tool* survives; vocabulary as *substrate axis* retires.

---

## 5. Borderline / watch list

These surfaces are *not* retired tonight but flagged for explicit watch.

### 5.1 range_profile 3-bucket categorization

**Status:** Borderline. Currently `melee / medium / ranged` per `qd-engine-bc-axes-lock-2026-05-20.md` Axis 1.

**Watch concern:** Bucketing is itself a categorical choice. The underlying Axis 1 range value is continuous (mean weighted skill range in units). The 3-bucket categorization is a hand-authored discretization.

**Retirement candidate:** v1.1+ — if the cohesion-judge or downstream consumers can handle continuous Axis 1 values directly, the 3-bucket categorization is vestigial. For v1, the buckets are operationally useful (rule-table inputs, telemetry tagging) so they stay.

### 5.2 7-element substrate as closed list

**Status:** Borderline. 7 elements + physical excluded per D2 resolution.

**Watch concern:** Even though element substrate is mechanically baked (§ 4.1), the closed-list-of-7 is itself a categorical commitment. Could there be an 8th element? Could shadow + holy collapse to a "moral-spectrum" axis? Could fire/water/earth/wind collapse to "classical-elemental" + lightning/holy/shadow as "transcendent"?

**Retirement candidate:** Not v1. The mechanical baking + canonical-7 lock is load-bearing enough that retirement-as-axes is a v1.1+ design question. Flagged for explicit watch when v1.1+ scope opens.

### 5.3 Variant C profile flags as currently enumerated

**Status:** Borderline. `engine-as-general-serial-content-product-2026-05-22.md` § 3.2 + § 3.3 list per-flag enumerations (e.g., `pairing_mode = unified / disjoint / mixed_triangulated`).

**Watch concern:** Some of these enumerations are designer-authored taxonomies. Are there 3 pairing modes only, or is there a continuous spectrum?

**Retirement candidate:** Not v1. The flag enumerations are operationally useful for v1 profile assembly; revisit when v1.1+ profile customization deepens.

### 5.4 Stat enumeration (INT / WIS / STR / DEX / CON / VIT / LUCK / CHA)

**Status:** Borderline. Implicit in stat-derivation work.

**Watch concern:** The stat list is genre-canonical (D&D-derived). Could the stats themselves be discovered from convergence data?

**Retirement candidate:** Almost certainly not. Stats are mechanically baked into combat math + UI affordances + player mental model. The list survives even under audit. Flagged for completeness.

---

## 6. Per-surface cleanup checklist — consolidated

This section consolidates per-pattern cleanup actions into a master checklist organized by file/surface. Each item references the pattern(s) it serves.

### 6.1 Engine code (reincarnated-engine/src/reincarnated/)

| Surface | Pattern(s) | Action |
|---|---|---|
| `canonical/archetype_templates/*.yaml` | 1 | Audit — files may exist as legacy reference; not loaded as generation inputs |
| `generation/element_biases.py` | (survives § 4.1) | No change; ELEMENT_SCALING_ATTRIBUTE is canonical |
| Any code path with `archetype_id` / `archetype_name` parameter on generation entry | 1 | Remove from generation inputs; preserve in attribution paths |
| Any code path with `role_orientation` parameter on generation entry | 2 | Remove from generation inputs; preserve in diagnostic paths |
| Any code path with trait-to-stat application during stat assignment | 3 | Replace with BC-axis-derivation; traits become v1.1+ flavor layer |
| Any code path with `cultural_lineage_register = List[tuple]` | 4 | Change schema to `List[cluster_id]` post-import; cluster_id references clusters table |
| Any code path with `gear_catalogue_id` enum | 5 | Replace with `weapon_id` FK to weapons + `cluster_id` FK to clusters |
| BC-axis measurement code (`generation/bc_axes/*` or similar) | (6 partial) | Survives Tier-1 audit; Tier-2 audit pending axis discovery |

### 6.2 Canonical docs

| Doc | Pattern(s) | Action |
|---|---|---|
| `canonical/16-project-roadmap.md` | 1, 2, 5 | Audit for archetype / role / 15-entry references; update vocabulary forward in next major edit |
| `canonical/28-engine-arpg-rebalance-design.md` | 1, 2, 3 | Audit for archetype / role / trait-stat references; flag as legacy where load-bearing |
| `canonical/29-design-overview.md` | 1, 2 | Audit for archetype / role framing; update vocabulary |
| `canonical/30-engine-explainer-current.md` | 1, 2 | Audit; this is current-state explainer so describe state truthfully — archetype/role are diagnostic-only now |
| `canonical/31-engine-explainer-future.md` | 1, 2, 3 | Audit; future-state should describe substrate-as-cohesion emergent identity |
| `canonical/32-progression-design.md` | 3 | Audit for trait-stats coupling; flag for revision under stat-derivation framework |
| `canonical/33-progression-skeleton.md` | 3 | Same |
| `canonical/34-monster-design-phase0-vs-production.md` | 1 | Audit for archetype framing in monster design |
| `canonical/story/gear-as-substrate-2026-05-21.md` | 4, 5 | § 3 catalogue marked as v0-hypothesized; preserve as historical reference |
| `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` | 1, 2, 4, 5 | Full restructure pending — collapse 252 → 63 combinations under role_orientation drop; demote 15-entry catalogue to hypothesis |
| `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` | 1, 2 | Recalibrate ω/τ under role_orientation drop |
| `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` | 3 | Mark as v1.1+ optional-identity-modulator design |
| `canonical/story/d8-trait-floor-design-phase-1-p1.md` | 3 | Same |
| `canonical/story/d9-gear-affix-design-phase-1-p1.md` | 3 | Audit gear affixes; base stats come from BC-axis derivation not trait sum |
| `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` | 4, 6 (partial) | § 3 + § 6 amendment retiring cultural_lineage_register as pre-imposed-tuple-list; optional sixth amendment per skill_handoff |
| `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` | 6 | Post-axis-discovery: audit for survival under Tier-2 retirement |
| `canonical/story/role-orientation-vestigial-audit-2026-05-22.md` (pending) | 2 | This doc supersedes — folded into § 3.2 here |

### 6.3 Memory files (~/.claude/projects/...)

**Out of session scope** per acceptance criteria. Matt handles memory updates manually. The cleanup items below are notes for Matt's manual pass:

| File | Pattern(s) | Action |
|---|---|---|
| `project_role_orientation_taxonomy.md` | 2 | Mark historical/diagnostic-only |
| `project_trait_architecture.md` | 3 | Mark legacy / borderline vestigial under BC-axis-derived stats framework |
| `project_earth_meta_layer.md` | (load-bearing) | No change needed; cross-reference Reincarnated overlay design |
| `project_pet_system.md` | (load-bearing for v1) | Companion architecture pulls forward into Reincarnated overlay v1 |
| `project_engine_state_findings.md` | 1, 2 | Audit for archetype/role framing |
| `project_geometry_palette.md` | (survives) | Geometry palette is mechanical substrate; not vestigial |

### 6.4 Telemetry schemas

| Schema surface | Pattern(s) | Action |
|---|---|---|
| `archetype_id` columns | 1 | Mark deprecated; new records write null; preserve for historical queries |
| `role_orientation` columns | 2 | Mark deprecated; preserve for historical queries |
| Trait-stat attribution fields | 3 | Replace with BC-axis-derived attribution |
| Pre-imposed aesthetic-tuple columns (`tech_level`, `tone`, `cultural_lineage` as classification fields) | 4 | Migrate to `cluster_id` FK post-clustering |
| `gear_catalogue_id` enum columns | 5 | Migrate to `weapon_id` + `cluster_id` |
| Per-kit pre-imposed-axis values | 6 (Tier 2) | Migrate to derived-axis blob post-axis-discovery |

### 6.5 Dispatches

| Dispatch surface | Pattern(s) | Action |
|---|---|---|
| New dispatches (any author) | All | Use post-retirement vocabulary; reference this audit doc |
| Old dispatches | All | Stand as historical record; do not retroactively rewrite |
| Cohesion-judge prompt templates | 1, 2, 4, 5 | Audit + update; cohesion-judge reads converged kit + cluster identity + weapon descriptors directly |

---

## 7. Canonical replacement language — vocabulary substitutions

Designers and code paths should use the post-retirement vocabulary. Substitution table:

| Old (vestigial) | New (post-retirement) | Use context |
|---|---|---|
| `archetype` (as generation input) | `gear substrate` (concept) / `mechanical signature` (per-kit) / `cluster` (per-population) | Engine, dispatches, docs |
| `archetype` (as descriptive label) | `reference build` (ARPG-canon descriptive: "Stormcaller-pattern build") | Designer language, docs |
| `archetype template` | `(retired — no replacement; templates were vestigial)` | Engine; remove from generation paths |
| `role_orientation` (as generation input) | `(retired — emerges from BC axes)` | Engine, rule-tables |
| `role_orientation` (as descriptive label) | `damage flavor` / `control flavor` / `support flavor` / `tank flavor` (descriptive, post-convergence) | Designer language |
| `traits carry stats` | `stats are derived projection of (element_scaling_attribute × per-axis BC magnitudes)` | Engine, progression docs |
| `trait pool determines class` | `traits are optional identity modulators v1.1+` | Trait docs |
| `aesthetic tuple` (as substrate axis) | `aesthetic cluster` (post-discovery) / `aesthetic descriptor` (per-weapon free-text) | Engine, cohesion-judge |
| `aesthetic tuple` (as descriptive vocabulary) | (survives — keep using as thinking tool) | Designer language |
| `tech_level × tone × cultural_lineage` (as 120-tuple matrix) | `cluster-naming hypothesis` / `aesthetic-descriptive-vocabulary` | Designer docs |
| `15-entry gear catalogue` (as enumeration) | `vast weapon library` (substrate) + `emergent clusters` (post-discovery) | Engine, gear docs |
| `15-entry gear catalogue` (as predicted shape) | `clustering hypothesis` (predictions about emergent clusters) | Designer language |
| `gear_catalogue_id` (FK to enum) | `weapon_id` (FK to weapons) + `cluster_id` (FK to clusters) | Schemas, engine |
| `pre-imposed axes` (designer-authored) | `discovered axes` (PCA / factor analysis derived) | Engine, post-Phase-2 |
| `range / geometry / timing / charge / accuracy / rhythm` (as canonical 6 axes) | (Tier-1 survives; Tier-2 audit pending) — refer to "BC mechanical axes" as a working description; post-axis-discovery vocabulary lands then | Engine, current-state docs |
| `LITE` (as gear-substrate phase qualifier) | `HEAVY` / `(retired — gear is real substrate in v1)` | Engine, dispatches, protocol |
| `signature_gear_archetype` (telemetry field) | `signature_gear` (referencing weapon_id) / `signature_cluster` (referencing cluster_id) | Telemetry, dispatches |
| `reference archetype` (in W0.7 attribution) | `reference build` (descriptive) / `diagnostic group` (for legacy attribution) | Analysis docs |

**Use forward.** Old language survives in historical documents; new work uses the right side of the table.

---

## 8. Cross-references

### 8.1 This session's canonical foundations
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C strategic lock (`f72690f`)
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` — surface-cleaned (`8037922`); full restructure pending under role_orientation drop
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — Profile A asset pipeline; finalization pending
- `agentic_orchestration/galadriel/notes/2026-05-22-canary-meshy-regen.md` § 8 — canonical pipeline rule (`06e91e9`)

### 8.2 Companion docs this session
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — Pattern 3 replacement detail
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — Patterns 4-5-6 implementation detail + vast-library pivot
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — operationalizes Pattern 6 axis discovery via library import + statistical pass

### 8.3 Research foundations
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/` — 7 files; weapon library import discovery + schema
- `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/` — Unity catalogue + Meshy armor capability
- `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` — Meshy pipeline capability research

### 8.4 Protocol + governance
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 — parent protocol; § 6.2.2 P1 substrate enrichment is the workstream where this audit operationalizes
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 RATIFIED 2026-05-22 (`0d1ad63`)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — Discipline #19 entry; future entries for vestigial-pattern retirements

### 8.5 Historical references
- `canonical/story/gear-as-substrate-2026-05-21.md` — Pattern 5's source artifact (15-entry catalogue); preserve as historical
- `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` — Pattern 3 trait-architecture origin
- `memory/project_role_orientation_taxonomy.md` — Pattern 2 origin

---

## 9. Closing — the audit's discipline

The recurring pattern this audit names — categorical pre-imposition surviving cleanup at one layer by hiding in the next — is structurally important to the engine's long-term coherence. Without explicit audit discipline, vestigial taxonomies will keep accumulating, and substrate-as-cohesion's architectural commitment will erode under their weight.

The discipline going forward:
- **When a new architectural surface lands**, ask the audit questions (§ 1.3). Pre-imposed? Derived? Enters generation or comes out of generation? Could it emerge from substrate?
- **When an existing surface gets revisited**, audit the layer below it. If you retire archetype, audit role. If you retire role, audit traits. If you retire traits, audit stats. If you retire stat-pre-imposition, audit how stats are derived.
- **When something feels "naturally categorical,"** trust the suspicion. The 15-entry catalogue felt natural because it was genre-canonical; the audit revealed it inherited the genre's biases. The mechanical-property axes felt natural because they were measurement axes; the audit revealed Pattern 6 (the axis-set itself was designer-authored). What feels natural is often what carries the most invisible pre-imposition.

The substrate-as-cohesion commitment lives or dies on this audit discipline. The architectural language can land in canonical docs all day long; if the implementation carries vestigial categorical surfaces, the commitment is performative.

Tonight's six-retirement pass is the first comprehensive audit. It will not be the last. Pattern 6 in particular operationalizes through the weapon library import + statistical axis discovery work; when that lands, a follow-on audit will surface whatever vestigial layer remains.

The road continues. The audit continues.

---

**Signed:** gandalf (story-and-design steward; senior designer)
**Authority:** Matt 2026-05-22 evening — six canonical retirement calls
**For:** canonical lock of six vestigial-pattern retirements + per-surface cleanup checklist + canonical replacement language + the systematic insight (categorical pre-imposition survives cleanup at one layer by hiding in the next) — to anchor all future architectural surface audits.
