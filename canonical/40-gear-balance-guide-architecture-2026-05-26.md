# 40 — Gear, Balance, Guide, and Multi-T4 Architecture (Cycle 13 Foundation)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27 — amendment-pass-record per § 0.1) — see `canonical/00-ground-state.md`

**Date:** 2026-05-26 (initial authoring); 2026-05-27 (Cycle 14 SC-2 amendment pass — doc 46 + doc 47 inheritance; see § 0.1)
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock + 2026-05-27 amendment pass — Cycle 13 architectural foundation; 86 locked decisions across 5 design blocks; doc 46 (concentration architecture, 9 layers) + doc 47 (damage scaling architecture) amendments to specific D-entries landed in-place per § 0.1 amendment-pass-record; specific implementation items still deferred to T4 PM1 + stat-sheet partition cycle (now landed as doc 42) + gamora methodology consultation + drax player surface work with explicit ownership markers
**Authority:** Matt 2026-05-26 — full session greenlight after iterative refinement across 5 design blocks; Matt 2026-05-27 — Cycle 14 framing brief Q5 ratification authorizes SC-2 doc 40 amendment pass (doc 46 + doc 47 inheritance work)
**Companion docs:**
- `agentic_orchestration/gandalf/matt_conversations/skills_and_gear_discussion` — source conversation (substantive design insights; auto-combat framing throughout source does NOT propagate per § 1)
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/02-roadmap.md` — roadmap (Cycle 13 scope-doc gates on this doc + T4 PM1)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone; "balance as property" composes with D10 Path A pitch material per § 2
- **`canonical/46-concentration-architecture-2026-05-27.md` — concentration architecture, 9 layers (Cycle 14 sidecar foundation); § 13 lists D-entries amended per Cycle 14 SC-2 inheritance pass (D9 / D33 / D38 / D49 / D50 / D51 / D52 / D54 / D55 / D56); see § 0.1 amendment-pass-record (NEW 2026-05-27)**
- **`canonical/47-damage-scaling-architecture-2026-05-27.md` — damage scaling architecture (physical / magical / hybrid routing); § 5.5 lists D-entries composing with the scaling-path dimension (D7 / D9 / D55 / D63-D86); see § 0.1 amendment-pass-record (NEW 2026-05-27)**
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B substrate-bound at Phase 2; spec-driven gear gen sharpens toward Architecture B per § 3
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` — T4 architecture defaults (1 signature + 1-3 secondary capstones); § 8 of this doc extends with full algorithm canonical form
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — substrate composition policy; § 5.4 per-season anchor variability lock composes with multi-T4 architecture per § 8
- `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` — T4 PM1 prep doc; this canonical doc informs T4 PM1 + receives T4 PM1 outputs in Cycle 13 sequencing

---

## 0. TL;DR

This doc captures the architectural foundation for Cycle 13, derived from Matt's `skills_and_gear_discussion` source conversation + an iterative 5-block design session (2026-05-26). It locks 86 decisions across:

1. **Balance as property, not process** (Block 1; D1-D6) — generation specifies; simulation validates at generation time; cycle structure prevents drift; commercial pitch keystone for D10 Path A
2. **Spec-driven gear generation + rarity power escalation + capability toolkit + tier structure** (Block 2; D7-D17 + D48-D57) — gear gen mirrors T4 algorithm pattern; rarity IS power escalation; legendary/set capability toolkit; 4-tier legendary/unique structure + 2-tier set structure
3. **85th-percentile cumulative endgame target + Option A acquisition curve + multi-node calibration** (Block 3; D18-D27) — balance band targets 85% cumulative; calibrated drop rates not deterministic milestones; four progression nodes (early / mid / endgame start / endgame)
4. **Spirit guide as data-oracle + T4-attuned gear intent + peak-moment community layer + auto-combat attribution correction** (Block 4; D28-D47) — universal data-oracle pattern; T4-attuned gear as connective tissue; KPM-spike community currency; explicit auto-combat-not-canonical capture
5. **Multi-T4 architecture + T4 algorithm canonical form + respec-with-legendary-trigger mechanism + active-skill-budget + T4-count-per-class + sim methodology** (Block 5; D63-D86) — 4-phase T4 algorithm canonical lock; respec-driven attunement with legendary-triggered free-respec opportunities; flat 8 active skills; T4 count = chain count - 1; hybrid cohort + edge-case sim sampling with per-legendary anchoring

**CRITICAL framing correction (§ 1 — PROMINENT):** the source conversation extensively framed the design as "strategic auto-combat ARPG." Matt corrected this at the end of source conversation: auto-combat is reserved as deferred mobile-game-variant option, NOT primary-game direction. All architectural commitments in this doc apply to conventional-execution ARPG and do NOT depend on auto-combat premise.

**Cycle 13 scope expansion (§ 8 + § 9):** all 4 phases of T4 algorithm wrap into Cycle 13 (NOT phased across multiple cycles) because T4-and-gear interaction is architecturally inseparable. This expands Cycle 13 substantially and elevates multi-seam coordination + gamora methodology consultation + jack-ryan Gate-1 throughput as load-bearing constraints.

---

## 0.1 Amendment-pass-record — Cycle 14 SC-2 (2026-05-27)

> **STATUS:** This doc has received an in-place amendment pass on 2026-05-27 per Cycle 14 SC-2 dispatch authorized by Matt's Cycle 14 framing brief Q5 ratification (`agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 12). The original D-entries are preserved in body; amendments are inline-annotated **AMENDED 2026-05-27 (doc 46 § N / doc 47 § N)** with cross-references to superseding canonical content. This anchor § 0.1 is the index. STATUS remains CURRENT — amendments extend the architecture; they do not demote it.

### 0.1.1 Why this amendment pass fires

Doc 40 is the Cycle 13 architectural foundation (86 locked decisions). Two Cycle 14 canonical docs landed 2026-05-27 that refine or supersede specific doc 40 D-entries:

- **`canonical/46-concentration-architecture-2026-05-27.md`** — concentration architecture, 9 layers (stat-range bounds + affix migration + capability scope reduction + trigger vocabulary + concentration probability table + cohesion layering + synergy scan refinement + set keying + class-agnostic drops). § 13 lists doc 40 D-entries requiring amendment. The architectural through-line: identity = chain composition + T4 + 4-6 build-defining items + stat-affix support. Gear amplifies; gear does not constitute. Remediates the "capability soup" pattern empirically surfaced by Cycle 13 mechanical season.
- **`canonical/47-damage-scaling-architecture-2026-05-27.md`** — physical / magical / hybrid damage scaling routing per skill `damage_scaling_type`. § 5.5 lists doc 40 D-entries that COMPOSE with the scaling-path dimension (not supersession; composition). The architectural through-line: weapon is damage source for physical skills; skill is damage source for magical skills; weapon's role differs by attribute.

Without this amendment pass, downstream readers (rocket Wave 0.5 + Waves 1-2; gamora Wave 5 re-calibration; jack-ryan Gate-1 reviewers; future agents) would consume the unamended D-entries as canonical truth — a Discipline #1 (math-before-code) violation if rocket implements against unamended D-entries.

### 0.1.2 Amendment index — doc 46 § 13 inheritance (supersession + refinement)

| D-entry | Doc 40 anchor | Doc 46 superseding section | Amendment type | Synopsis |
|---|---|---|---|---|
| **D9** | § 3.7 | Doc 46 § 4 (Layer 3 capability scope reduction) + § 6 (Layer 5 concentration probability table) | REFINED | Capability scope LOCAL per Layer 3; tier-density per Layer 5 concentration probability table (not flat-across-tiers). Single-capability-per-legendary preserved. |
| **D33** | § 6.7 | Doc 46 § 4 + § 9 (Layer 8 set keying to T4 strategy × element clusters) | REFINED (composes with prior 2026-05-27 morning amendment) | T4-attunement is metadata (per Block B1 content-compositional framing locked morning 2026-05-27); sets ALSO carry T4-strategy-cluster keying per Layer 8. |
| **D38** | § 6.7 | Doc 46 § 9 (Layer 8 set keying) + § 10 (Layer 9 class-agnostic per-drop generation) | RESOLVED (composes with prior 2026-05-27 morning amendment) | Content-compositional attunement (morning lock) + set keying to strategy clusters (Layer 8) + class-agnostic per-drop generation (Layer 9) collectively close the prior "T4-attuned gear specifics deferred" framing. |
| **D49** | § 3.7 | Doc 46 § 6 (Layer 5 concentration probability table) | PRESERVED + ADDITIVE | 4-tier legendary + drop pool restriction structure preserved; Layer 5 adds tier-density probability table calibrating capability count per tier. |
| **D50** | § 3.7 | Doc 46 § 6 (Layer 5) | PRESERVED + ADDITIVE | Drop pool restriction preserved; Layer 5 adds tier-density probability calibration. |
| **D51** | § 3.7 + § 6.7 amendment | Doc 46 § 9 (Layer 8 set keying) | REFINED (composes with prior 2026-05-27 morning amendment) | Tier 1+2 legendaries + ALL sets carry T4-strategy-cluster keying; non-attuned content retains base value (consistent with content-compositional model). The annotation IS metadata; capability scope is keyed to substrate strategy clusters. |
| **D52** | § 3.7 | Doc 46 § 6 (Layer 5) | PRESERVED + ADDITIVE | Power-escalation-within-categories preserved; Layer 5 adds tier-density calibration to power-escalation logic. |
| **D54** | § 3.7 | Doc 46 § 4 (Layer 3 capability scope reduction) + § 6 (Layer 5 concentration probability table; § 6.4 set-pieces-replace-individual) | AMENDED — capability density scales with tier | Capability density scales with tier per Layer 5 concentration probability table (NOT flat across all 4 tiers). Set pieces replace individual capability per Layer 5.4. Original "toolkit at all 4 tiers" preserved as upper-bound presence; Layer 5 calibrates density per tier within that envelope. |
| **D55** | § 3.7 | Doc 46 § 4 (Layer 3) + § 6 (Layer 5) | PRESERVED + WEAPONS-ONLY ENFORCEMENT ADDED | Triggered-passive-high-prob preserved; tier-density per Layer 5; **weapons-only enforcement for `true_active_secondary_skill`** ADDED per Cycle 13 empirical inspection (substrate generation produced true_active_secondary_skill rolls on off-hand slots — violation of D55 weapons-only intent; Layer 5 enforcement plus generation-side fix required). |
| **D56** | § 3.7 | Doc 46 § 4 (Layer 3 capability scope reduction) | PRESERVED + SCOPE CLARIFIED | Modifier-surface expansion preserved as legendary primary differentiator; clarified: scope of mechanic-altering content is LOCAL per Layer 3 (not character-wide). New stat-type rolls operate within local capability scope. |

### 0.1.3 Amendment index — doc 47 § 5.5 composition (scaling-path dimension; not supersession)

Doc 47 introduces the damage scaling-path dimension that was implicit in `skill-system-2026-05-24.md` composition pattern. These D-entries COMPOSE with the doc 47 scaling-path architecture; the original D-entry claims are PRESERVED. The amendment is annotative — downstream implementers (rocket Track D.2 per-skill emission; gamora Track D.4 fight engine routing) MUST consume both the original D-entry AND the doc 47 routing logic.

| D-entry | Doc 40 anchor | Doc 47 composition section | Amendment type | Synopsis |
|---|---|---|---|---|
| **D7** | § 3.7 | Doc 47 § 5.5 + § 7.1 (Track D.2 per-skill emission) | COMPOSITION ADDED | Spec-driven gear gen routes gear modifiers to physical or spell pools per gear type. Gear modifier surface partitions by damage scaling path (physical_damage_pct / spell_damage_pct / element_damage_pct / weapon_spell_modifier). Composes with doc 42 stat-sheet modifier partition (Category 1 Damage sub-divisions). |
| **D9** | § 3.7 | Doc 47 § 5.5 | COMPOSITION ADDED (in addition to doc 46 amendment above) | Legendary/set capabilities operate ON the scaling path; capability semantics declared per damage_scaling_type alignment. A weapon-bound capability inherits the weapon's damage_scaling_type alignment. |
| **D55** | § 3.7 | Doc 47 § 5.5 | COMPOSITION ADDED (in addition to doc 46 amendment above) | Weapons-only true-active rule — true-active skills declared on weapons inherit weapon's damage_scaling_type alignment. Physical weapon → true-active skill is physical-scaled; caster weapon → true-active skill is magical-scaled (unless skill explicitly declares otherwise). |
| **D63-D86 (Block 5 T4 architecture en bloc)** | § 8.9 | Doc 47 § 5.5 + § 4.2 / § 4.3 / § 4.4 (fight engine damage calculation) | COMPOSITION ADDED | Multi-T4 architecture composes with damage scaling routing: Category A T4 effects (character-wide) apply on top of routed damage calculation per damage_scaling_type; Category B effects apply chain-multiplicatively within the routed path; Category C effects (element conversion / dual element addition) apply at the element resolution step within the appropriate path. The 4-phase T4 algorithm canonical form is NOT amended by doc 47; the integration point is at fight engine routing (Track D.4 gamora scope). |

### 0.1.4 Sub-entry amendment companions (Q-SC2-1 resolution)

The dispatch open question Q-SC2-1 asked whether subordinate D-entries (e.g., D54.1 / D55.1) warrant companion amendments. Resolution: doc 40 D-entries are flat (no subordinate D-entries in the original schema). Doc 46 amendments operate at the parent D-entry level. The "single capability per legendary" provision within D9, the "weapons-only true-active" provision within D55, and the "tier 2 > tier 1 > tier 0.5 > tier 0" provision within D52 are all preserved as sub-clauses of their parent entries — not promoted to separate sub-entries.

### 0.1.5 STATUS line disposition (Q-SC2-3 resolution)

The dispatch open question Q-SC2-3 asked whether this amendment pass demotes doc 40 to "CURRENT-with-amendments" or preserves "CURRENT". Resolution: doc 40 remains **CURRENT**. The amendment pass extends the architecture (concentration discipline + scaling-path routing) — it does not invalidate the foundational architecture. Prior 2026-05-27 morning amendments (Block B1 content-compositional, D33/D35/D38/D51 inline + § 3.6 9-category × 11-slot lock + § 3.2 3-category T4 taxonomy + § 8.3 / § 8.3.1 / § 8.4 sharpening + § 6.6.1 trait absorption + various § 8 D-entry sharpenings) already exist as in-place amendments without demoting STATUS. This pass follows the same pattern. The STATUS line "load-bearing as of" date is rolled forward to 2026-05-27 to reflect the latest amendment pass; the § 0.1 anchor is the discriminator pointing downstream readers to the amendment-pass-record.

### 0.1.6 What is OUT OF SCOPE for this amendment pass

- Doc 40 D-entries NOT listed in doc 46 § 13 or doc 47 § 5.5 are NOT amended (per dispatch out-of-scope clause)
- No D-entries are deleted or moved to historical/ (amendment preserves originals with supersession markers in-place)
- Doc 41 / doc 42 / doc 43 / doc 44 / doc 45 (Cycle 13 design-intent canonical docs) are NOT amended in this pass (separate amendment cycle if needed)
- The gauntlet sim representative loadout discipline (§ 6.5 amendment) is Wave 2 work, NOT SC-2 scope
- Discipline canonical writes (#33-#37 from doc 46 + #38 from doc 47) are jack-ryan SC-1 scope, NOT SC-2 scope
- Cycle 13 mechanical season empirical references in doc 40 body are NOT updated per Cycle 14 framing brief Q9 (Cycle 13 season DISREGARDED for Cycle 14 reference; doc 40 retains its Cycle-13-authoring-date empirical context as historical record)

### 0.1.7 Bidirectional cross-reference

Doc 46 § 13 + doc 47 § 5.5 cross-reference forward to the amended D-entries; this § 0.1 cross-references backward to doc 46 § 13 + doc 47 § 5.5. Per canonical doc format § 4 bidirectional cross-reference protocol.

---

## 1. Auto-combat attribution correction (CRITICAL)

### 1.1 The correction

> **The primary game retains conventional execution mechanics. Auto-combat is NOT canonical direction for the primary game. It is reserved as a deferred option available later for a mobile-game variant.**

### 1.2 Why this needs explicit canonical capture

The source conversation (`agentic_orchestration/gandalf/matt_conversations/skills_and_gear_discussion`) extensively framed the design as "your game is a strategic auto-combat ARPG." This framing was built up across the second half of the conversation and shaped substantial portions of the other AI's reasoning before Matt corrected it at the very end (line 2420):

> "I'm not leaning into the auto-battle mechanic but saving it as an option available at a later date when I make the mobile game."

Without explicit canonical capture, future readers of this doc referencing the source conversation could inherit the auto-combat premise silently. The portable insights captured in §§ 2-8 do NOT depend on auto-combat — they apply to conventional-execution ARPG architecture. The auto-combat framing was the source-conversation other-AI's over-fitted synthesis that Matt then corrected.

### 1.3 What this means for canon

- **Spirit guide as data-oracle (§ 5):** applies to conventional-execution ARPG; not auto-combat-specific
- **T4-attuned gear intent (§ 6):** applies regardless of execution model
- **Peak-moment community layer (§ 7):** applies regardless of execution model
- **The "audience this serves" enumeration in source conversation** (accessibility-limited players, older players, mobile-first audiences) was over-fitted to the auto-combat premise and does NOT propagate to canon as the primary game's audience framing

### 1.4 Discipline this protects

This is the framing-audit / Discipline #23 pattern operating on inherited-from-external-conversation findings. Source-conversation framings that were corrected by Matt do not propagate uncritically. The correction is captured prominently to prevent silent inheritance by future readers.

This is the **3rd operational instance of Discipline #23**, now catching inherited-framing failure DURING canonization rather than post-hoc. Worth referencing in Discipline #23 amendment work alongside the prior two instances (all-0.5 win-rate framing 2026-05-25; "drax requires no work" understatement 2026-05-25).

### 1.5 Decision points

- **D44** — Primary game retains conventional execution mechanics; auto-combat NOT canonical
- **D45** — Source conversation referenced for substantive design insights only; embedded auto-combat framing does NOT propagate
- **D46** — Source conversation's "audience this serves" framing does NOT propagate as primary-game audience
- **D47** — Discipline #23 3rd operational instance flagged to jack-ryan for amendment write-up

---

## 2. Block 1 — Balance as property, not process

### 2.1 Core principle

> **Balance is a property of generation, not a process of operation.** Each season's content is generated to a balance specification; simulation validates the specification at generation time; the validated content ships and runs unchanged for the season's duration; the cycle structure retires content before drift can accumulate.

### 2.2 Structural prerequisite

The structural prerequisite is **a finite, comprehensively-validated shipped content set whose scope is bounded such that drift cannot accumulate beyond what the content set covers.** Two architectural patterns achieve this:

**Pattern A — Seasonal cycling (Reincarnated's primary direction).** Cycle reset retires content before drift accumulates. Each season is its own finite content set; the cycle structure prevents accumulation. Drift-prevention mechanism: *content retirement before drift window opens*.

**Pattern B — Pre-generated thematically-clustered content library (engine-as-product alternative; potentially also Reincarnated).** 1-2+ year sustainable volume of unique, viable, thematically-clustered, faction-specific playable entities shipped as a comprehensive package. Combinatorial pre-validation covers the player surface. Drift-prevention mechanism: *volume + comprehensive pre-validation*.

**Hybrid composes.** A multi-year pre-gen library deployed via seasonal cycling combines both drift-prevention mechanisms. This may actually be Reincarnated's mature shape — pre-generate library; ship seasonally; cycle prevents within-library drift while library size ensures content sufficiency across the cycle.

### 2.3 Commercial pitch implication (D10 Path A / engine-as-product)

The live-service ARPG industry spends substantial resources on balance-as-process — dedicated balance teams, telemetry dashboards, patch cadences, community sentiment monitoring. Diablo IV, Path of Exile, Last Epoch, Lost Ark — all of them. Our engine produces balanced content as an output, not a process to be operated.

**This is genuinely differentiating positioning for studio licensees** who want sophisticated ARPG content without the post-deployment balance operations cost. Substantially BROADER applicability than monthly-cycle-only games: studios building monthly-cycle games get Pattern A; studios building persistent-character games with pre-gen libraries get Pattern B; studios building hybrids get both.

The engine produces the shipped content set; the licensee chooses deployment shape. The engine's balance-as-property guarantee is portable across game architectures.

### 2.4 Discipline implication

Validation happens AT GENERATION TIME via simulation. Post-deployment "rebalancing" is anti-pattern. This is a real engineering discipline that propagates to every seam:

- **Generation seam (rocket):** generates against balance specification
- **Simulation seam (gamora):** validates at generation; not a live monitoring tool
- **Telemetry seam (star-lord):** collects for future-season inputs, not for current-season balance feedback
- **Spirit guide:** surfaces specification-derived projections, not live-meta-derived adjustments

### 2.5 Boundary positions

1. **Bug fixes vs rebalancing.** Genuine bugs (a skill multiplier off by 10x; a damage calculation overflow) get hotfixed. Bugs are NOT rebalancing — the spec said X, the implementation produced Y; fix restores spec compliance. The discipline is "no rebalancing of validated specifications," not "no patches ever."

2. **In-season variance systems** (rift events, infusion, tower depth — if those land). These introduce within-season variance but they're SPECIFIED variance — the generation pass includes the variance bounds. Doesn't violate balance-as-property because the spec covers them.

3. **Cross-season learning.** This season's telemetry informs NEXT season's generation. That's not balance-as-process; that's input refinement for the next generation cycle.

### 2.6 Decision points

- **D1** — Adopt "Balance is a property of generation, not a process of operation" as canonical principle
- **D2** — Structural prerequisite: finite, comprehensively-validated shipped content set; Pattern A (seasonal cycling) + Pattern B (pre-gen library) + Hybrid all viable; Reincarnated's preference is hybrid-leaning-seasonal but not load-bearing-on-seasonal
- **D3** — Load-bearing commercial-pitch positioning for D10 Path A with explicit pattern-portability
- **D4** — Validation-at-generation-time becomes cross-seam discipline; engineering-discipline candidate for jack-ryan ratification
- **D5** — Three boundary positions: bugs ≠ rebalancing; specified variance ≠ unbalanced; cross-season learning ≠ live balancing
- **D6** — Doc 38 cross-reference: own § in doc 40 for principle-level capture; cross-reference from doc 38 D10 Path A pitch material

---

## 3. Block 2 — Spec-driven gear generation + rarity escalation + capability toolkit + tier structure

### 3.1 Core proposition

> **Gear generation uses the same architectural pattern as T4: a scored-candidate strategy registry.** A kit-plus-T4-selection produces a gear specification; the strategy registry produces candidate gear pieces that fit the spec; simulation validates the result against the kit's endgame power target.

> **Rarity IS power escalation** (traditional ARPG model retained). Common → Uncommon → Rare → Epic → Legendary in raw power.

> **Legendary/set tier carries a capability TOOLKIT** of mechanic-alteration capabilities beyond mere stat escalation. Toolkit applies at all 4 tiers of legendaries; T4-attunement is the EXTRA layer reserved for top 2 tiers.

### 3.2 Strategy registry pattern

> **AMENDED 2026-05-27 per Matt + gandalf Pattern-B session 2026-05-27 (closeout § 2.4):** the 3-category T4 taxonomy (A class-mechanical/energy alteration + B chain multiplicative event + C chain element conversion/addition) SUPERSEDES the 6-strategy registry as the player-facing taxonomy + design-spec. The existing 6 strategies are RETAINED as algorithm implementation detail under the 3-category umbrella. See § 8.4 for full taxonomy + § 8 new sub-section for DUAL_ELEMENT_ADDITION strategy.

T4 algorithm (Algorithm § 8) uses scored-candidate strategy registry. The **design-spec taxonomy** (player-facing, design-intent) is the **3-category structure** locked at § 8.4 (post-amendment):

| Category | Role | Implementation strategies (under umbrella) |
|---|---|---|
| **A — Class mechanical/energy alteration** | Character-wide effect (always present) | RESOURCE_CONVERSION, DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, class-wide TRADE_OFF |
| **B — Chain multiplicative event** | Chain-specific (exactly one of B or C per T4) | Skill-specific TRADE_OFF, GEOMETRY_COLLAPSE, multiplier strategies |
| **C — Chain element conversion / addition** | Chain-specific (exactly one of B or C per T4) | ELEMENT_CONVERSION, **NEW: DUAL_ELEMENT_ADDITION** (per § 8 new sub-section) |

Gear generation gets an analogous registry. The specific gear strategies are implementation territory (deferred to stat-sheet partition cycle per § 3.6 D14), but the pattern locks: **scored-candidate strategy registry; kit+T4 produces spec; strategies produce candidates; sim validates; selected candidate ships.**

### 3.3 Capability toolkit (legendary/set tier)

| Capability | Description | Slot constraint |
|---|---|---|
| **Multiplicative** | Numerical multiplier on matching T4 path (tier 1+2 only) | All legendary/set slots |
| **Mechanic-adjusting** | Changes HOW a mechanic works (e.g., bleeds also slow) | All legendary/set slots |
| **Spatial-adjusting** | Changes geometry/range/area (cone→circle; ranged→melee) | All legendary/set slots |
| **Axis-adjusting** | Changes damage type or resource axis (fire→ice; mana→HP) | All legendary/set slots |
| **Added skill — passive (triggered-effect-dominant)** | Legendary grants a passive with active-like triggered effect (e.g., "spawns tornadoes upon hit from wind attack," "shrapnel burst on physical hit"); HIGH PROBABILITY on weapons | All slots |
| **Added skill — true active** | Player-activated via skill-bar; EXTREMELY RARE; additive to base skill budget | **Weapons only** |

**Dominant flavor:** triggered-passive on weapons. Auto-triggers from gameplay actions (on-hit, on-crit, on-element-cast, on-kill, etc.); no player budget impact. Diablo 2 "10% chance to cast tornado on hit" lineage. Triggered-passive-dominant flavor REINFORCES auto-combat-not-canonical correction (§ 1) — player still executes; triggered effects add procedural cascades to that execution.

### 3.4 Modifier-surface expansion over scalar escalation

Legendaries differentiate from lesser rarities primarily through **modifier-surface expansion** (new stat types Epic cannot roll) rather than **scalar-numerical-escalation**.

| Mechanism | Legendary's primary use |
|---|---|
| New modifier types not available on Epic | **Dominant differentiator** |
| Scalar power increase across stats | Slight; supplementary |
| Capability toolkit | Available; less frequent than added-skill |
| Added skill (triggered-passive any-slot; rare true-active weapon-only) | **High probability** |
| T4-attunement (tier 1+2 only) | Endgame-exclusive layer |

Drop fantasy: **"did I get NEW capabilities"** rather than "did I get bigger numbers." Preserves rarity-as-upgrade satisfaction without stat-inflation tedium.

### 3.5 Tier structure (legendary/unique/set)

Three distinct sub-categories AT the legendary rarity tier (not escalating rarity tiers above legendary):

| Category | Tier 0 (early game) | Tier 0.5 (mid game) | Tier 1 (end game start) | Tier 2 (end game / 85%) |
|---|---|---|---|---|
| **Set items** | — | — | ✅ unlocked | ✅ unlocked |
| **Unique items** | ✅ unlocked | ✅ unlocked | ✅ unlocked | ✅ unlocked |
| **Legendary gear** | ✅ unlocked | ✅ unlocked | ✅ unlocked | ✅ unlocked |

**Drop pool restriction by content-tier play (Legendaries):**

| Playing at... | Legendary tiers in drop pool |
|---|---|
| Early game (tier 0 content) | Tier 0 only |
| Mid game (tier 0.5 content) | Tier 0 + 0.5 |
| End game start (tier 1 content) | All 4 tiers |
| End game (tier 2 content) | All 4 tiers |

**Power escalation:** within each category, power increases across tiers (tier 2 > tier 1 > tier 0.5 > tier 0). Same pattern as Common → Uncommon → Rare → Epic across rarities.

**T4-attunement restriction:** Tier 0 and tier 0.5 legendaries are NOT T4-attuned — they follow standard chain-alignment only. Tier 1 and tier 2 legendaries carry T4-attunement (composes with § 6 T4-attuned gear intent).

### 3.6 Stat-sheet modifier partition (principle locked; 9-category × 11-slot architectural surface AMENDED 2026-05-27; affinity matrix + 6 principles LOCKED)

> **AMENDED 2026-05-27 per Matt + gandalf Pattern-B session 2026-05-27 (closeout § 3.1 + § 3.2 + § 3.3):** the 9-category character sheet surface (Damage / Defense / Resource / Crit / Speed / Resistance-Penetration / On-trigger / Build-identity / Utility-Meta-progression) + 11-slot taxonomy (1 main-hand + 1 off-hand + 5 armor + 4 accessory) + per-slot affinity matrix (graduated affinity, not binary) + 6 principles are LOCKED architectural surface. Specific modifier enumerations + weighted probabilities per slot per category land in Wave 1 partition cycle (NEW canonical doc 42 — `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md`).

> **Character stat sheet has a defined, enumerated 9-category modifier surface. The 11-slot taxonomy is partitioned via a per-slot affinity matrix such that each slot rolls modifiers with graduated affinity (primary ~50% / secondary ~30% / tertiary ~15% / off-affinity ~5%) per slot per category. The partition is designed to (a) produce build diversity through stat composition across loadouts, and (b) make skill-node-count and chain-distribution decisions matter as differentiated mathematical impact.**

**9-CATEGORY CHAR SHEET SURFACE (LOCKED 2026-05-27 — per ultra-think pass against Diablo 1-4 + Immortal + PoE 1-2 + LE + Grim Dawn + Lost Ark; revised from 8 to 9 categories adding Utility/Meta-progression):**

| # | Category | Sub-divisions |
|---|---|---|
| 1 | **Damage** | base / by-element / by-mechanic / by-condition / weapon-scaling |
| 2 | **Defense** | armor / DR% / dodge / block / +HP / +HP-regen / element-resists / status-resists |
| 3 | **Resource** (8-model-dependent per § 6 + closeout § 2.2) | per-model specific stats (mana max/regen/cost-reduction; cooldown reduction; stamina max/regen; rage gen/decay/cap; energy gen/max; channel efficiency/duration; combo retention/cap; HP-cost efficiency) |
| 4 | **Crit** | crit chance / crit multiplier / crit-on-condition / crit-on-element |
| 5 | **Speed** | attack-speed / cast-speed / cooldown-reduction / movement-speed |
| 6 | **Resistance / Penetration** | element penetration / armor penetration / status duration / status resistance |
| 7 | **On-trigger** | on-hit / on-crit / on-kill / on-block / on-dodge / on-element-cast (toolkit-only at legendary tier per D54) |
| 8 | **Build-identity** | T4-attunement annotation / set-bonus rank / class-intrinsic supporting-chain investment |
| 9 | **Utility / Meta-progression** (NEW) | magic find / currency drop rate / experience boost / rare-find chance |

**11-SLOT TAXONOMY (LOCKED 2026-05-27):**

| Slot family | Slots | T4-attunement eligible (Tier 1+2) |
|---|---|---|
| Weapon | Main-hand (main_weapon) | Yes |
| Off-hand | Secondary-item (shield / tome / banner / focus / horn / talisman / dual-wield-secondary per `canonical/story/off-hand-items-2026-05-24.md`) | Yes |
| Armor | Head / chest / hands / feet / legs (5 slots) | Yes |
| Accessory | Amulet / ring × 2 / belt (4 slots) | Yes |
| **Total** | **11 slots** | All eligible at upper tiers |

**PER-SLOT AFFINITY MATRIX (architectural lock 2026-05-27; specific weights operationalized in doc 42):**

Affinity matrix: 9 categories × 11 slots, with **primary (~50%) / secondary (~30%) / tertiary (~15%) / off-affinity (~5%)** weighted probability per slot per category.

Sample affinity entries (full matrix in doc 42 § 2):
- Main-hand weapon: Damage primary / On-trigger primary / Crit secondary / Speed secondary / Resource tertiary
- Chest: Defense primary / Resource primary / On-trigger (on-being-hit per D55) secondary / Build-identity secondary
- Feet: Speed (movement) primary / Defense (dodge) primary / Resource (stamina/energy regen) secondary

**6 LOCKED PRINCIPLES (LOCKED 2026-05-27):**

1. **Graduated affinity, not binary** — every slot CAN roll any category but with weighted probability per affinity tier (primary/secondary/tertiary/off-affinity)
2. **Tier-restricted modifiers** — ~10-20% of modifier types are tier-restricted (Epic+ / Legendary+ / Tier-1+2) regardless of slot affinity
3. **Resource-model-gated** — resource modifiers map by class resource model (per 8-model catalog § 6 + closeout § 2.2); cross-resource rolls DO NOT APPEAR
4. **Gap-filling discipline (D80)** — spirit guide surfaces gap-fill opportunities; stat-sheet partition + acquisition curve calibration incorporate gap-filling discipline
5. **No-skill-modifier rule** — gear NEVER modifies existing chain-node skills (no +levels-to-Fireball); capability toolkit ADDS new triggered-passives + rare true-actives only per D54/D55
6. **Cross-cohesion validation** — Wave 1 partition cycle MUST validate affinity matrix supports build-diversity via spot-check simulation across cohort archetypes (per D61 + D84 + Discipline #26)

Specific partition design is **stat-sheet partition cycle work — early Cycle 13 milestone (Wave 1)**, landing BEFORE gauntlet battle sim (so sim validates against real stat surface, not placeholder). Multi-seam: gandalf intent + gamora simulation methodology + rocket implementation + jack-ryan critique + legolas Mode A research. Discipline #18 methodology consultation fires before partition lock (per #18.2 refinement: at extension hotspots fires AFTER baseline empirical data lands; SC-7 gamora consultation fires post-Wave-1).

**Partition cycle scope explicitly includes (per Matt 2026-05-26 amendment):**

1. **Modifier surface enumeration** (which stat types exist on the character stat sheet — per 9-category surface above)
2. **Per-slot partition design** (which slots roll which modifier types — per affinity matrix above)
3. **Probability distribution per slot per modifier** (gap-filling discipline per D80; weighted probability per affinity tier per principle 1)
4. **Node-count + chain-distribution interaction math** (D13 differentiation requirement)
5. **Weapon damage spec completeness check** for main + off-hand/secondary weapons (BC-axis coverage per `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` 8-axis spec; off-hand items per `canonical/story/off-hand-items-2026-05-24.md` 6+ categories — shield/tome/banner/focus/horn/talisman/dual-wield; ensure damage geometry/timing/amplitude/etc. fully specified for all weapon types eligible for either slot)
6. **Non-weapon gear baseline stats** for common variants without added stats (the "plain chest piece with X HP and Y defense" baseline — foundational stat sheet work for armor + jewelry + accessory slots; baseline for legendary additive stats per D56 modifier-surface expansion to layer on top of)
7. **Main_weapon vs secondary_weapon routing cleanup** (substrate curation pollution per prior Cycle 12 capture: 13 of 35 forms had off-hand-category items as main_weapon; three compound root causes — substrate curation pollution + Layer 2 substrate-binding not filtering by category + secondary_item routing not firing; partition cycle includes this cleanup work as substrate-side input to clean partition design)

**Gap-filling acquisition discipline:** stat-sheet partition + acquisition curve calibration should incorporate gap-filling discipline — gear acquisition over time should fill gaps in the player's accumulated stat sheet, not just produce items that duplicate already-strong stats. Spirit guide can surface gap-filling opportunities.

**Cross-reference:** full per-rarity × per-slot grid + tier-restricted modifier surface enumeration + sample modifier enumerations per category + Wave 1 implementation guidance for rocket land in `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` (Wave 1 partition design intent canonical).

### 3.7 Decision points

- **D7** — Spec-driven gear gen as architectural pattern (scored-candidate strategy registry mirroring T4 Algorithm § 8); all rarities are spec-driven. **AMENDED 2026-05-27 (doc 47 § 5.5 + § 7.1; composition added):** spec-driven gear gen routes gear modifiers to physical or spell pools per gear type and per damage_scaling_type path. Gear modifier surface partitions by damage scaling path (physical_damage_pct / spell_damage_pct / element_damage_pct / weapon_spell_modifier). Composes with doc 42 stat-sheet modifier partition (Category 1 Damage sub-divisions). See § 0.1 amendment-pass-record.
- **D8** — Rarity IS power escalation (traditional ARPG model retained); Common → Legendary in raw power
- **D9** — Legendary/set tier carries TOOLKIT of mechanic-alteration capabilities (toolkit at all 4 tiers per D54); single capability per legendary, not all simultaneously. **AMENDED 2026-05-27 (doc 46 § 4 Layer 3 + § 6 Layer 5; refined):** capability scope LOCAL per Layer 3 (mechanic-altering content operates within the local capability scope, not character-wide); tier-density per Layer 5 concentration probability table (not flat-across-tiers). Single-capability-per-legendary preserved. **AMENDED 2026-05-27 (doc 47 § 5.5; composition added):** legendary/set capabilities operate ON the scaling path; capability semantics declared per damage_scaling_type alignment (weapon-bound capability inherits weapon's damage_scaling_type alignment). See § 0.1 amendment-pass-record.
- **D10** — Build identity multi-layered (kit + chain + T4-attunement); decision space scales with progression
- **D11** — Epic→Legendary discontinuity LOAD-BEARING for endgame parity (tier 1+2 legendary saturation required for endgame target power); composes with § 4 Option A acquisition calibration
- **D12** — Strategy registry: single registry + T4-attunement annotation gate at legendary/set tier
- **D13** — Stat-sheet partition PRINCIPLE locked: defined modifier surface; slot-partitioned; designed for build diversity + node-count/chain-distribution differentiation
- **D14** — Stat-sheet partition design is named early-Cycle-13 milestone landing BEFORE gauntlet sim; multi-seam work cycle; Discipline #18 methodology consultation before partition lock; output: canonical/41-style doc; **scope per § 3.6 includes 7 enumerated items including weapon damage spec completeness + non-weapon gear baseline stats + main_weapon routing cleanup (Matt 2026-05-26 scope expansion amendment)**
- **D15** — Cycle 13 A/B/C decision sharpened toward Architecture B (substrate-bound at Phase 2) — spec-driven gear gen + tier structure strongly indicate this
- **D16** — Compute-improvement claim from source conversation (~100x vs validation-cycling): qualitative direction canonized; specific magnitude deferred to empirical measurement
- **D17** — Active-skill-budget question RESOLVED by D55+D57 (triggered-passive-dominant flavor + rare-active additivity)
- **D48** — Sets: 2 tiers, endgame-only (tier 1 + tier 2); always T4-attuned
- **D49** — Uniques: 4 tiers, full progression arc; distinct sub-category from generic legendaries. **AMENDED 2026-05-27 (doc 46 § 6 Layer 5; preserved + additive):** 4-tier structure preserved; Layer 5 concentration probability table adds tier-density calibration on top (capability count per tier scaled per Layer 5). See § 0.1 amendment-pass-record.
- **D50** — Legendaries: 4 tiers, cross-tier drop pool restrictions (early-game play → tier 0 only; mid-game → tier 0+0.5; endgame → all 4 tiers). **AMENDED 2026-05-27 (doc 46 § 6 Layer 5; preserved + additive):** drop pool restriction preserved; Layer 5 adds tier-density probability calibration. See § 0.1 amendment-pass-record.
- **D51** — T4-attunement RESERVED for tier 1+2 of legendaries and all sets; tier 0+0.5 legendaries follow chain-alignment only. **(prior morning 2026-05-27 amendment captured below at line for D51 AMENDMENT 2026-05-27 closeout § 3.4; afternoon 2026-05-27 SC-2 inheritance work adds:) AMENDED 2026-05-27 (doc 46 § 9 Layer 8; refined):** tier 1+2 legendaries + ALL sets carry T4-strategy-cluster keying per Layer 8 (sets keyed to T4 strategy × element clusters); non-attuned content retains base value (consistent with content-compositional model). Annotation IS metadata; capability scope is keyed to substrate strategy clusters. See § 0.1 amendment-pass-record.
- **D52** — Power escalation within categories: tier 2 > tier 1 > tier 0.5 > tier 0. **AMENDED 2026-05-27 (doc 46 § 6 Layer 5; preserved + additive):** power-escalation-within-categories preserved as ordering; Layer 5 concentration probability table adds tier-density calibration (capability density scales monotonically with tier). See § 0.1 amendment-pass-record.
- **D53** — Legendary/unique/set as distinct sub-categories at legendary rarity tier (NOT escalating rarity tiers above legendary)
- **D54** — Capability toolkit applies at ALL 4 tiers of legendaries; T4-attunement is the EXTRA layer reserved for top 2 tiers. **AMENDED 2026-05-27 (doc 46 § 4 Layer 3 + § 6 Layer 5 + § 6.4):** capability density scales with tier per Layer 5 concentration probability table — NOT flat across all 4 tiers. Original "toolkit at all 4 tiers" preserved as upper-bound presence envelope (all tiers MAY carry capabilities); Layer 5 calibrates DENSITY per tier within that envelope (tier 2 high density; tier 0 low density). Set pieces replace individual capability per Layer 5.4 (sets concentrate via multi-piece commitment, not via flat-additive capability stacking). Capability scope LOCAL per Layer 3. See § 0.1 amendment-pass-record.
- **D55** — High probability of triggered-passive added skill on weapons (active-like triggered effects); truly active skills extremely rare AND additive to base skill budget when they roll (weapon-only). **AMENDED 2026-05-27 (doc 46 § 4 Layer 3 + § 6 Layer 5; preserved + weapons-only enforcement added):** triggered-passive-high-prob preserved; tier-density per Layer 5; **weapons-only enforcement for `true_active_secondary_skill` ADDED** per Cycle 13 empirical inspection — substrate generation produced true_active_secondary_skill rolls on off-hand slots in violation of D55 weapons-only intent. Layer 5 enforcement plus generation-side fix required (rocket Wave 1 scope). **AMENDED 2026-05-27 (doc 47 § 5.5; composition added):** true-active skills declared on weapons inherit weapon's damage_scaling_type alignment — physical weapon → true-active is physical-scaled; caster weapon → true-active is magical-scaled (unless skill explicitly declares otherwise). See § 0.1 amendment-pass-record.
- **D56** — Legendary differentiation primarily via modifier-surface expansion (new stat types Epic cannot roll); slight scalar increase supplementary. **AMENDED 2026-05-27 (doc 46 § 4 Layer 3; preserved + scope clarified):** modifier-surface expansion preserved as legendary primary differentiator; clarified: scope of mechanic-altering content is LOCAL per Layer 3 (not character-wide). New stat-type rolls operate within local capability scope. See § 0.1 amendment-pass-record.
- **D57** — D17 active-skill-budget question resolved by D55 (triggered passives don't compete; rare actives additive)

### 3.8 Gap-filling discipline

- **D80** — Stat-sheet partition + acquisition curve calibration incorporate gap-filling discipline; spirit guide surfaces gap-filling opportunities; partition cycle (D14) treats gap-filling as explicit design input

---

## 4. Block 3 — 85th-percentile cumulative endgame target + Option A acquisition curve + multi-node calibration

### 4.1 Core proposition

> **The balance band targets the 85th-percentile endgame engagement window: the power level that 85% of players reach AT LEAST before their engagement with the content ends.** Acquisition curve is calibrated such that the typical player's natural engagement reliably delivers them to or past this target. The top 15% who exceed it are explicitly outside the balance band, playing acknowledged-aspirational content.

### 4.2 Endgame as journey, not destination

**Endgame is itself a power curve, not a fixed state.** Players arrive at endgame with baseline power, then continue progressing along the endgame power curve as they acquire gear, refine builds, and engage with progressively appropriate content. The 85th percentile target is a specific point ON the endgame curve, not the entry-to-endgame point.

Balancing for the 85th percentile means balancing for where most players actually spend most of their endgame time. The bulk of endgame engagement happens between entry and the 85th percentile point.

### 4.3 The 85% interpretation: cumulative

**85% of players reach AT LEAST the target power level before their engagement ends. The 15% who go further are above-target; the bottom (whatever percentage) who never reach it are below-target.**

Cumulative interpretation is:
- Achievable through deterministic acquisition design + calibrated drop rates
- Tolerant of player engagement variance
- Validated by simulation reasonably
- Forgiving (not a tight distribution requirement)

### 4.4 Acquisition curve as primary engine output — Option A (calibrated drop rate)

**Legendary acquisition uses calibrated drop rate (Option A), not deterministic-milestone-based.** Drop rate is calibrated against expected KPM ratio × expected engagement-time distribution to produce reliable legendary saturation for the 85th-percentile-engaged player.

**Why Option A works (math):** at endgame scale, drop-rate variance becomes small as fraction of mean (~90k kills for 20hr endgame engagement at ~75 KPM). Engagement-time variance dominates drop-rate variance. Calibrating against the 85th-percentile-engagement-time hitting target legendary saturation directly hits the cumulative 85% target by construction.

**Why prefer Option A over Option B (smart-loot with pity systems):**
- Smart-loot has hidden-mechanic resentment risk
- Reverse-pity gaming distorts intended play patterns
- Implementation complexity ongoing
- Community drama vector
- Option A is simpler, more transparent, respects player autonomy

**Deferred fallback (NOT committed):** smart-loot with pity (Option B) reserved as fallback IF Option A's calibration proves empirically insufficient across multiple seasons. Default preference is Option A; reach for Option B only after calibration refinement attempts exhaust.

### 4.5 Top 15% explicitly outside the band

The 15% who exceed the target are playing aspirational content by definition. This content is **not validated against the balance band**. Simulation doesn't try to keep these encounters in-band. Tuned by intent ("should feel challenging for someone who's pushed past typical depth"), not by simulation-validated balance.

Explicit design call rather than implicit difficulty-tier convention.

### 4.6 Multi-node calibration (D27 extension)

Balance calibration spans **four named progression nodes:**

| Node | Player population in-band | Rarity composition (typical) | Calibration target |
|---|---|---|---|
| **Early game** | All players engaging | Common / Uncommon dominance | Power band tuned to baseline kits + early gear |
| **Mid game** | Players continuing past early | Rare / early Epic introduction | Power band tuned to kits + mid-progression gear |
| **End game start** | Players reaching endgame entry | Epic dominance, early Legendaries | Power band tuned to entry-to-endgame composition |
| **End game (85% node)** | 85% of players reach AT LEAST this depth | Legendary / Set saturation | Power band tuned to endgame target (D18 target) |

Each node has its own balance band + simulation validation + acquisition-saturation target. Acquisition curve calibration (Option A per D21) is multi-node, not single-node.

**Multi-node calibration WORK is post-Cycle-13 engine extension; Cycle 13 lays the architectural foundations.** Stat-sheet partition (D14) and Pattern B pre-gen library (D2) scope across all four nodes.

### 4.7 What's underspecified (intentionally deferred)

1. **Specific endgame target power level number** — depends on actual game mechanics + simulation work; principle locks, number is downstream calibration
2. **Expected engagement distribution** — underspecified empirically; first-season operates against estimates; cross-season learning refines

### 4.8 Decision points

- **D18** — 85th-percentile endgame engagement window as calibration target; cumulative interpretation (AT LEAST target reached by 85%)
- **D19** — Endgame is journey, not destination; balance band targets a specific point on the curve
- **D20** — Acquisition curve is primary engine output; calibrated, not configured
- **D21** — Option A (calibrated drop rate against KPM ratio × engagement distribution); preserves kill-to-kill engagement loop; Option B deferred fallback only
- **D22** — Top 15% outside balance band; aspirational content, not validated by sim, tuned by intent
- **D23** — Bottom-tier players accepted as engagement-distribution variance, not calibration failure
- **D24** — Specific endgame target power-level + engagement distribution: underspecified empirically; principle locks, numbers downstream
- **D25** — Cross-season learning loop: season N telemetry → season N+1 generation inputs; NOT live-balance-during-season
- **D26** — Pattern A vs Pattern B engagement-distribution shape; same principle, different shape
- **D27** — Balance calibration spans 4 named progression nodes; multi-node WORK is post-Cycle-13; Cycle 13 lays foundations

---

## 5. Block 4 Part A — Spirit guide as data-oracle (universal pattern)

### 5.1 Core proposition

> **The spirit guide operates in data-oracle voice (neutral observation) rather than counselor voice (evaluative recommendation). The same data-presentation pattern applies universally across all in-game decision spaces — content selection, T4 selection, gear loadout combinations, encounter selection, infusion or tower decisions if those land. One consistent interface; many decisions; players learn the pattern once and apply everywhere.**

Additive to existing spirit-guide canon (from-the-future entity, Heroic Spirit framework). The ORACLE ROLE is the new architectural commitment; the character itself is already established.

### 5.2 Why data-oracle, not counselor

Counselor voice ("you should switch to T4-B") has structural failure modes:
- Carries implicit judgment; player feels graded on choices
- Loses credibility when "should" recommendations diverge from player preferences
- Compresses player autonomy
- Doesn't scale across player sophistication

Oracle voice ("KPM 75 at current; KPM 89 projected if you switched to T4-B") avoids these:
- Presents data; player evaluates
- Same surface serves all sophistication levels
- Multiple valid choices coexist
- Player retains full strategic agency

### 5.3 Universal-pattern principle

Same data-presentation interface across decision spaces. Players learn one vocabulary; consistent framing reduces cognitive load; engine intelligence surfaces uniformly. Accessibility-through-consistent-interface broadens addressable audience without dumbing down systems.

### 5.4 Projection language honesty

Simulation produces averages; individual play has variance. Guide language reflects this:
- "Projected to..." (not "will...")
- "Has typically produced..." (not "produces...")
- "Estimated at X, with typical variance of plus or minus Y..."
- "Players in similar configurations have averaged..."

Trust in guide depends on projections feeling like projections rather than promises.

### 5.5 What this requires (implementation cycle flags)

- **Simulation accuracy is load-bearing.** Guide is only as useful as projection accuracy. Ongoing maintenance burden as engine produces new content.
- **Pacing design is non-trivial.** "Ever-present" vs "always-available" tension. Threshold-based interjection, pull-vs-push, tone-aware presence, player-tunable verbosity.
- **Universal-pattern integration is multi-seam.** Touches every decision system. Spec-and-build work spans gamora + drax + rocket + gandalf.

### 5.6 Decision points

- **D28** — Spirit guide adopts data-oracle voice; additive to existing character canon
- **D29** — Universal-pattern principle across all decision spaces
- **D30** — Throne-resident framing composes with Heroic Spirit canon; oracle reads patterns
- **D31** — Projection language honesty: "projected to / typically / estimated"
- **D32** — Implementation specifics deferred to implementation work cycle; simulation-accuracy maintenance flagged as ongoing

---

## 6. Block 4 Part B — T4-attuned gear (connective tissue intent)

### 6.1 Core proposition

> **Legendary/set gear (tier 1+2 only) can carry T4-attunement: a multiplicative bonus + mechanic-alteration capability that activates on matching T4 paths. Acquired-but-non-matching attunement creates persuasion-to-experiment opportunities; spirit guide surfaces these. Sets are set-level T4 attuned (multi-piece commitment for full bonuses). Together with multi-T4-per-class architecture, this creates multiple viable build identities accessible to a single Servant within a single seasonal arc.**

### 6.2 Connective tissue

This is the architecture that unifies the commitments:

- **Multi-T4-per-class** creates the build-path branching (§ 8)
- **Spec-driven gear gen** ensures gear fits kit+T4 specifications (§ 3)
- **Legendary/set capability toolkit** provides the mechanic-alteration vocabulary (§ 3.3)
- **T4 attunement on tier 1+2 legendary/set** specializes pieces to specific T4 paths
- **Spirit guide as data-oracle** surfaces latent builds in stash (§ 5)
- **Respec-driven attunement with legendary-triggered free-respec opportunities** is the mechanism for build-switching (§ 8.5)
- **Replay value within Servant** emerges from accessing multiple build identities

T4-attuned gear is the load-bearing keystone tying these together.

### 6.3 Heroic Spirit narrative cohesion

Different T4 paths = different aspects of the Spirit the Master can manifest. T4-attuned legendary acquisition = encountering evidence of an aspect the Spirit could express. Switching T4 with attuned gear = manifesting a different aspect of the same Spirit.

The Throne metaphor extends: the Throne contains the full Spirit including all possible manifestations. Accumulated gear in the stash is evidence of aspects the Spirit could express. The Master chooses which aspects to draw out via T4 + attunement selection.

Mechanical depth and narrative resonance reinforcing each other.

### 6.4 Replay value within a single Servant

A single Servant within a single seasonal cycle can support multiple full build identities through respec + attunement swaps + set completions across different T4 paths.

This SHARPENS the seasonal cycle's value proposition. Each Servant is a multi-build exploration window rather than a single-build commitment-and-discard.

### 6.5 What's deferred to T4 PM1 + downstream

Architectural specifics depend on downstream work:
- T4 count per class formula (locked at D83: chain count - 1) — but specific class chain counts are T4 PM1
- Attunement bonus magnitudes (1.5x match, 0.8x mismatch, or different curve) — simulation-validation territory
- Cross-rarity attunement distribution — partition design + acquisition curve calibration
- Set bonus structure (2pc/4pc/full bonuses; T4-attunement granularity within sets) — implementation territory
- Binary vs graduated attunement — design + simulation territory

### 6.6 Casual complexity mitigation

Multi-T4 + attunement + sets + stat-sheet partition + acquisition mechanics is a lot of decisions for casual audiences. Spirit guide (§ 5) is primary mitigation — surfaces relevant decisions contextually; lets casual players engage with depth at their pace. Progressive concept introduction via play encounter.

### 6.6.1 Per-kit supporting chain absorbs trait architecture (RE-AMENDED 2026-05-27 evening — no-class architectural recommitment)

> **REDACTION NOTE 2026-05-27 evening:** Matt no-classes architectural recommitment retires "class-intrinsic" framing. Supporting chain is per-kit (emerges from substrate-cluster-shared-theme at the kit's BC cell), NOT class-intrinsic. See `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`. Original section title "Class-intrinsic supporting chain" → "Per-kit supporting chain"; original term "class identity" → "kit identity emerging from substrate-cluster theme" throughout body text below.

**May 12 trait architecture (per `project_trait_architecture.md` memory) is SUPERSEDED by current chain + stat-sheet + legendary-passives architecture.** ~90% of trait architecture absorbs automatically; the remaining "per-kit intrinsic baseline passive" surface lands in:

**Option C — Supporting chain absorbs kit identity.** The T3-only supporting chain (every kit has one per D83 per § 8.3) serves as the "per-kit intrinsic passives" location. Supporting chain represents kit identity (emerging from substrate-cluster theme); T4 chains represent build specialization.

- **No separate "trait modifier" axis** on character sheet (the 9-category surface § 3.6 does not include a trait column)
- **Player chooses investment level** in kit-identity (supporting chain) vs build-specialization (T4 chains) — real opportunity cost
- **Composes with depth-vs-breadth lever** (variable 3-or-4 chains; supporting chain present in both per § 8.3)
- **Substrate-led**: uses existing architectural surface rather than adding new layer
- **Minimum viable trait integration** (per Verdict D.1; deferred Matt async — see doc 42 § 8 for Wave 1 implementation guidance): 55-entry trait pool (5 per archetype × 11 archetypes) lands in Wave 1 as bounded scope; per-archetype 5-10 + L12/L25/L38 floors DEFERRED to Cycle 14+ — note "archetype" here references **substrate-cluster archetype-shapes**, not pre-authored classes

### 6.7 Decision points

- **D33** — Legendary/set (tier 1+2) carry T4-attunement; lesser rarities/tiers do not. **AMENDED 2026-05-27 (closeout § 3.4):** content-compositional attunement supersedes binary/graduated framing. Per D33 + D51: Tier 1+2 legendary/unique have chain+T4 ANNOTATION (metadata); all sets have chain+T4 annotation (endgame-only); Tier 0+0.5 have chain-alignment annotation only. The annotation IS metadata recording generation-time alignment intent; it does NOT toggle anything ON/OFF at consumption time. Gear's CONTENT (passives, weapon specs) IS the attunement; magnitude IS content quality. **AMENDED 2026-05-27 afternoon SC-2 (doc 46 § 4 Layer 3 + § 9 Layer 8; refined):** T4-attunement is metadata (per Block B1 content-compositional framing locked morning 2026-05-27); sets ALSO carry T4-strategy-cluster keying per Layer 8 (set bonuses are keyed to T4 strategy × element clusters, not to character-specific identifiers). Capability scope LOCAL per Layer 3. See § 0.1 amendment-pass-record.
- **D34** — Acquired-but-non-matching attunement creates persuasion-to-experiment opportunity; spirit guide surfaces via data-oracle voice; spirit-guide synergy-score projection ("playing T4-A: projected KPM 75. Switching to T4-B: projected KPM 62. Net synergy score: T4-A composes 23% better with this gear") per closeout § 3.4
- **D35** — Sets are set-level T4 attuned; multi-piece commitment for full bonuses; **AMENDED 2026-05-27 (closeout § 3.4):** 4-piece sets standard; 2pc minor bonus (always-active) + 4pc full bonus (content composed with chain + T4)
- **D36** — Heroic Spirit narrative cohesion: T4 paths = aspects of Spirit; T4-attuned gear = latent aspect evidence
- **D37** — Replay value within single Servant arc via multi-T4 + attunement + set completions
- **D38** — **AMENDED 2026-05-27 (closeout § 3.4):** Content-compositional attunement model LOCKED. Gear's content (passives, weapon specs) IS the attunement; annotation field exists as metadata recording generation-time alignment intent; drives drop pool restriction (D50), spirit-guide projection (D34), algorithm-side optimization. Annotation does NOT toggle anything ON/OFF at consumption time — gear passives always fire; synergy value varies by build. NO separate multiplier; gear content design is sim-calibrated to produce playability-AND-in-band synergy with target chain+T4. Magnitude IS the content quality. Binary vs graduated attunement REJECTED; content-compositional supersedes. Per closeout § 8 #10: graduated attunement DEFERRED to v1.1+ if substrate-evidence shows content-compositional too rigid. **RESOLVED 2026-05-27 afternoon SC-2 (doc 46 § 9 Layer 8 + § 10 Layer 9):** the prior "T4-attuned gear specifics deferred" framing (the original D38 deferral) is collectively CLOSED by — (a) content-compositional attunement (morning lock); (b) set keying to T4 strategy × element clusters (Layer 8); (c) class-agnostic per-drop generation (Layer 9). No specifics remain deferred at the architectural level; downstream is implementation (rocket Wave 4 Track A amendment + new `set_generator.py` module). See § 0.1 amendment-pass-record.
- **D39** — Casual complexity acknowledged; spirit guide primary mitigation
- **D51 AMENDMENT 2026-05-27 (closeout § 3.4):** T4-attunement annotation = METADATA (recording generation-time alignment intent), NOT a toggle mechanism. The annotation drives drop-pool restriction (D50), spirit-guide projection (D34), algorithm-side optimization at generation time. At consumption time, gear passives always fire; the attunement does NOT gate any mechanic ON/OFF.

---

## 7. Block 4 Part C — Peak-moment community layer (design intent; phasing deferred)

### 7.1 Core proposition

> **The spirit guide authenticates noteworthy player performance moments (KPM spikes, depth achievements, build-execution highlights). These moments produce shareable artifacts and accumulate as Throne-recorded mythology. Casual players can compete on peak performance (3 minutes of optimal play) while hardcore players retain cumulative-accomplishment prestige. Multiple competitive axes serve different audiences without forcing them onto the same terms.**

### 7.2 Why this matters

Most ARPG community systems are biased toward cumulative metrics (total hours, currency, depth pushed) which structurally favor hardcore time-investment audiences. Casual players can't compete on these terms and feel excluded.

Peak-moment competition is genuinely democratizing — it measures preparation + optimization + execution-in-the-moment rather than time accumulation. A casual player who optimizes their build well and has one perfect 3-minute run produces a shareable peak that competes meaningfully with hardcore players' peaks.

This is real industry value — most live-service games struggle with this exact inclusion problem.

### 7.3 Throne-recorded mythology

Composes with Heroic Spirit framework. The Throne contains all summoned Spirits and their accomplishments. Notable performances of a Master's Servants get recorded in the Throne's mythology. Cross-season, Masters accumulate a record. Community has shared mythology that grows.

Mythologically resonant rather than just statistically competitive.

### 7.4 Honest framing

The casual-hardcore inclusion claim needs honest scope:
- **Peak competitions:** accessible to anyone with preparation + a good moment; casuals can win
- **Consistency competitions** (average performance, percentage above threshold): favor hardcore through repetition
- **Cumulative competitions** (total accomplishments): strictly favor hardcore

Marketing as "casuals equal hardcore" would be misleading. Honest framing: "the Throne notices moments of greatness from all summoned Spirits. Masters with limited time can record notable performances. Masters with extensive time accumulate broader mythological histories. Both remembered."

### 7.5 Phased implementation (deferred)

Source conversation Stage 1-6 (KPM detection → personal bests → shareable artifacts → in-game social layer → leaderboards → historical mythology) is multi-season build-out. Architectural intent locks; phasing decisions defer to implementation work cycle that fires post-launch or alongside community-system work.

### 7.6 Decision points

- **D40** — Spirit guide authenticates noteworthy performance moments; shareable artifacts; Throne-recorded mythology
- **D41** — Casual-accessible competitive layer (peak moments) coexists with hardcore cumulative-accomplishment layers; honest framing
- **D42** — Heroic Spirit / Throne mythology composition: notable moments enter accumulated lore
- **D43** — Implementation phasing deferred; architectural intent locks; phasing defers post-launch

---

## 8. Block 5 — Multi-T4 architecture + T4 algorithm canonical form + respec-with-legendary-trigger mechanism

> **AMENDED 2026-05-27 per Matt + gandalf Pattern-B session 2026-05-27 (closeout § 1.3 + § 2.4 + § 2.5):**
> - **D66 SHARPENED (one-T4-at-a-time)**: Only ONE T4 capstone unlocked at a given time. Sharpens D66 from passive description to active identity discipline. Composes with D65 respec-with-legendary-trigger as swap mechanism + D76 dual-effect architecture (concentrated identity, not diluted).
> - **3-category T4 taxonomy** SUPERSEDES 6-strategy registry as design-spec + player-facing vocabulary; existing 6 strategies retained as algorithm implementation detail (see § 8.4 for full taxonomy).
> - **NEW algorithm strategy: DUAL_ELEMENT_ADDITION** (see § 8.4.1) — chain skills retain primary element AND add a secondary element; substantively expands T4 design space.
> - **Parallel-chain reach** (see § 8.4.2) — chain-specific effect can target the T4's OWN chain OR a PARALLEL chain; algorithm-fixed at generation time (not player-chosen).
> - **Compositional synergy scan** (see § 8.4.3) — two-pass synergy detection (resolve + preserve); algorithmic composition (pattern library + statistical priors); NOT LLM raw-reasoning per D7 AI-tell discipline.
> - **Class-intrinsic supporting chain absorbs class identity** (see § 6 amendment for trait architecture absorption per Option C).

### 8.1 T4 algorithm canonical form (per Matt 2026-05-26 + 2026-05-27 amendments)

> **T4 skills are CAPSTONES at the top of skill tree chains. 2-3 T4 capstones per class (per § 8.3 formula). Only ONE T4 unlocked at a time (per D66 sharpening 2026-05-27 — active identity discipline, not passive description; composes with respec mechanism per § 8.5). Dual mechanical impact: character-wide AND within-chain (or parallel-chain per § 8.4.2). Implementation phased across 4 phases — all 4 wrap into Cycle 13 because T4-and-gear interaction is architecturally inseparable.**

### 8.2 Phased implementation (all 4 phases in Cycle 13)

| Phase | Scope |
|---|---|
| **Phase 1** | T4s into chains as capstones (structural alignment); single T4 per chain initially |
| **Phase 2** | Multiple T4 options per chain with selection mechanic (player-choice element without character-wide vs chain-wide scope dimension yet) |
| **Phase 3** | Character-wide vs chain-wide scope dimension (variance generator; biggest design risk) |
| **Phase 4** | Full simulation cycling through all T4 configurations during convergence (compute-heavy validation) |

**ALL FOUR PHASES WRAP INTO CYCLE 13.** Shipping Phase 1 alone produces architectural debt because the gear-attunement layer (§ 6) requires Phases 2-4 to be meaningful. Multi-T4 viability + spirit-guide-driven respec opportunities + endgame replay value all depend on full architecture landing together.

**T4-failure-handling — Option F (Hybrid) LOCKED 2026-05-27 (closeout § 1.7):**

1. Algorithm regenerates failing T4 with alternate strategies from registry (3 attempts; configurable per D62 compute budget)
2. If all regeneration attempts fail, ship character with partial T4 (in-band subset; chain keeps T1-T3 nodes but no functional capstone)
3. Minimum threshold = ≥1 T4 in-band for character to ship at all
4. Track regeneration rate as quality metric

Composes with D1 (balance-as-property — failures are honest), D67 (independent gauntlet sim validation), D65 (respec mechanism), D62 (compute budget).

### 8.3 Per-kit chain structure (RE-AMENDED 2026-05-27 evening — no-class architectural recommitment)

> **REDACTION NOTE 2026-05-27 evening:** Matt no-classes architectural recommitment retires "class" as a unit of architecture. Per-kit chain structure emerges from substrate clustering at the kit's BC cell, NOT from pre-authored class metadata. See `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`. The original "class chain structure" framing (PRESERVED IN PLACE BELOW with terminology redacted) reflected vestigial class-as-unit-of-architecture thinking now retired.
>
> _Earlier framing history (now retracted):_
> - **Interpretation A confirmed** 2026-05-26 (uniform 3-chain per class)
> - **AMENDED 2026-05-27 morning** (variable 3-or-4 chains per class per closeout § 1.4)
> - **RE-AMENDED 2026-05-27 evening** (per-kit chain count from substrate clustering; class concept retired)

**T4 capstone count per kit = chain count − 1.** Chain count per kit (3 or 4) emerges from substrate clustering at the kit's BC cell — denser substrate cells with greater BC-axis coverage vote 4-chain; sparser substrate cells vote 3-chain default. NO pre-authored per-class chain count.

**Per-kit chain structure** (substrate-emergent):

| Kit's emergent chain count | T4 capstones | Architecture |
|---|---|---|
| 3 chains | 2 T4 capstones | 2 T4 chains × ~5 nodes (branching-eligible per § 8.3.1) + 1 supporting chain × ~3 nodes |
| 4 chains | 3 T4 capstones | 3 T4 chains × ~3-4 nodes (linear) + 1 supporting chain × ~3 nodes |

Per-kit supporting chain (T3-cap; no T4 capstone) emerges from substrate-cluster-shared-theme at the kit's BC cell. Architecture first-class supports hybrid/multi-element kits: primary-element chains can have T4 capstones (defining kit identity); secondary-element chains can be T3-only (supporting damage/utility without capstone).

Example: a fire-primary, lightning-secondary kit's emergent chain structure might be:
- 2 fire chains (each with T4 capstone) — primary build identity choices
- 1 lightning chain (T3, no capstone) — supporting secondary damage
- Total: 3 chains, 2 T4 capstones

**No "first-pass class roster" exists. Substrate clustering at kit-generation-time produces per-kit chain structures. doc 48 (PRESERVED as VESTIGIAL) is the historical curated-archetype reference baseline, NOT a class roster the engine consumes.**

### 8.3.1 Branching refinement (LOCKED 2026-05-27 — closeout § 1.2; preserved under no-class recommitment)

**Branching gated by chain depth ≥4 nodes**, not by any class concept.

- Chains ≥4 nodes eligible for 1 branch point: 1 → 2 → {3a OR 3b} → 4 → T4-capstone
- Chains ≤3 nodes linear only
- Substrate-led: chain depth (emergent per kit) votes on branching eligibility
- Supporting chains stay linear (shallow by construction)

### 8.4 T4 algorithm 3-category taxonomy (LOCKED 2026-05-27 — closeout § 2.4)

> **The 3-category taxonomy SUPERSEDES the 6-strategy registry (§ 3.2) as design-spec + player-facing vocabulary. The existing 6 strategies are RETAINED as algorithm implementation detail under the 3-category umbrella.**

**3-category T4 taxonomy** (composes with D76 dual-effect):

| Category | Role | D76 dual-effect part | Algorithm strategies mapping |
|---|---|---|---|
| **A — Class mechanical/energy alteration** | Character-wide effect (always present) | Character-wide effect | RESOURCE_CONVERSION, DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, class-wide TRADE_OFF |
| **B — Chain multiplicative event** | Chain-specific (exactly one of B or C per T4) | Chain-specific effect | Skill-specific TRADE_OFF, GEOMETRY_COLLAPSE, multiplier strategies |
| **C — Chain element conversion / addition** | Chain-specific (exactly one of B or C per T4) | Chain-specific effect | ELEMENT_CONVERSION, **NEW: DUAL_ELEMENT_ADDITION** (per § 8.4.1) |

**Dual-effect separability discipline (D76 amendment; engineering-discipline candidate #31 per § 12.1):** Category A (character-wide) and Category B/C (chain-specific) effects MUST be INDEPENDENTLY COHERENT — removing one should leave the other as a genuine standalone mechanic. Failure mode: T4s where chain effect is just "consequences of character-wide effect spelled out in chain terms." Founding instance: corrected Blood Magic example 2026-05-27.

#### 8.4.1 DUAL_ELEMENT_ADDITION strategy (NEW LOCKED 2026-05-27)

**Chain skills retain primary element AND add a secondary element.**

- **Genre precedent:** PoE's "X% physical as fire"; D4's "all skills deal X% as cold"
- **Substantively expands T4 design space** beyond pure conversion (ELEMENT_CONVERSION replaces; DUAL_ELEMENT_ADDITION composes)
- **Algorithm category:** C (chain element conversion/addition)
- **Implementation:** rocket extends the 6-strategy registry to 7 strategies under Category C; gamora validates dual-element interactions don't produce degenerate cases (per Discipline #26 playability + Discipline #31 first-do-no-harm per § 8.4.3)

#### 8.4.2 Parallel-chain reach (LOCKED 2026-05-27 — closeout § 2.4)

**Chain-specific effect can target the T4's OWN chain OR a PARALLEL chain.**

- **Algorithm-fixed at generation time** (not player-chosen) — per generation cycle, the algorithm selects own-chain vs parallel-chain target as part of T4 scoring
- **Composes with depth-vs-breadth lever** — variable chain count + branching gated by depth means parallel-chain reach has variable target space per class
- **Enables cross-chain composition** — e.g., a fire-primary chain T4 could amplify a wind-secondary chain's mechanic, producing build-craft opportunities the player discovers via spirit-guide projections

#### 8.4.3 Compositional synergy scan (LOCKED 2026-05-27 — closeout § 2.5; Cycle 13 algorithm extension, NOT v1.1+)

**Two-pass synergy scan** (Matt 2026-05-27 button-up; required for parallel-chain reach to function as design):

| Pass | Description |
|---|---|
| **Pass 1 (resolve)** | Does candidate resolve existing kit tensions? (e.g., HP-cost-without-regen → life-steal-from-bleed) |
| **Pass 2 (preserve)** | Does candidate CREATE new tensions not resolved elsewhere? (e.g., life-steal-from-bleed against bleed-immune bosses → mechanism has no fuel) |

**Net synergy score = resolve-score − create-score.** Candidates that resolve more than they create get the boost. Cohesion-judge validates BOTH directions.

**Synergy opportunity patterns (v1 catalog):**

| Pattern | Description |
|---|---|
| **Tension-resolution** | Kit has a mechanic creating a problem the T4 could solve |
| **Theme-compound** | Kit has a passive theme the T4 could amplify |
| **Cross-chain composition** | Parallel chains have elements/mechanics that could combine |
| **Element-gap fill** | Kit has element coverage gap a T4 could fill |

**Honor AI-tell line (D7):** pattern library (gandalf-curated) + statistical co-occurrence priors (elrond) + algorithmic composition. **NOT LLM raw-reasoning** for core synergy detection.

**Engineering-discipline candidate #32 (per § 12.1):** First-do-no-harm discipline for algorithmically-generated T4 keystones — T4 synergy detection MUST include downstream-tension-creation check (Pass 2 preserve), not just upstream-tension-resolution (Pass 1 resolve). Failure mode: T4s that solve a stated problem by introducing an equally-bad new problem. Founding instance: two-pass synergy scan 2026-05-27.

**Compositional synergy scan serves BOTH** T4 generation AND legendary added-skill generation at consumption time. Same engine; two consumers.

### 8.4.4 Active skill budget

**Maximum 8 active skills.** Flat 8. Replaces prior chain-scaling formula proposal (simpler).

Players choose which chain actives to slot from their tree investment; chain-active selection naturally aligns with current T4 selection. Triggered-passive added skills (§ 3.3) don't count toward this budget. Rare additive true-active rolls from legendaries extend it situationally.

### 8.5 Respec-driven attunement with legendary-triggered free-respec opportunities

> **Multi-T4 viability achieved via respec-driven attunement. Base mechanism: respec is normally friction-bearing (cost / time — specifics T4 PM1). Tier-1 and tier-2 legendary/set acquisitions trigger spirit-guide-surfaced free-respec opportunities when the legendary advocates a different T4 than current build OR is a higher tier than current.**

| Implementation specification | Detail |
|---|---|
| **Trigger conditions** | Tier-1 or tier-2 legendary/set acquisition AND (a) advocates different T4 than current build, OR (b) higher tier than current build's anchor pieces |
| **Offer presentation** | Spirit guide surfaces in data-oracle voice (§ 5) with honest power-dip + projected-upside framing |
| **Expiration** | 30 minutes game-clock; use-it-or-lose-it |
| **Multi-drop events** | Compound offer (single decision across multiple qualifying drops) |
| **No revert capability** | Standard respec cost applies if player wants to undo (commitment-to-consequence discipline per D79) |
| **Opt-out always available** | Un-attuned legendary retains base + capability-toolkit value (D54) |

### 8.6 Commitment-to-consequence design discipline

The no-revert call (D79) is a sharper design insight than the specific decision implies. Three effects:

1. **Anti-optimization-through-flipping:** rewarding back-and-forth swaps degrades into degenerate optimization
2. **Spirit guide trust preservation:** if projections can be reverted away from, players treat them as cheap suggestions rather than load-bearing data
3. **Self-validation discipline:** forced commitment makes players engage with decisions seriously

Discipline candidate: **decision-mechanisms that require commitment-to-consequence produce more meaningful player engagement AND preserve trust in advisory systems. Reversibility degrades both. Escape valves should exist (pay standard cost to undo) but should NOT be free/easy reversibility.**

Applies broadly to any system where spirit guide advises and player chooses (respec, gear destruction, skill investment, archetype commitment, faction allegiance).

### 8.7 Combat sim node-population algorithm

**Hybrid cohort + edge-case sampling with per-legendary cohort anchoring.** Methodology:

1. Cycle each tier-2 legendary/set weapon
2. For each, determine which cohort archetypes (DPS-min-maxer, balanced, defensive, hybrid, etc.) would realistically equip it
3. Map appropriate node configurations for cohort × weapon combinations
4. Sample and validate those configurations against playability criterion (D61)

**Sub-option A (per-weapon cohort coverage):** validate each legendary across all plausible cohorts. Higher compute, higher fidelity, lower bias risk. Primary methodology.

**Sub-option B (per-legendary cohort selection):** for each legendary, infer most-likely cohort from mechanics/stats; validate against that cohort only. Lower compute, higher bias risk. Fallback for compute-constrained scenarios.

**Hybrid-within-hybrid (recommended starting point):** Sub-option A for ambiguous legendaries; Sub-option B for cohort-clear legendaries. Gamora methodology consultation (per Discipline #18) evaluates and refines.

### 8.8 Playability criterion (load-bearing sim validation gate)

The sim's validation criterion is not just "numerically in-band against content difficulty." It's the broader **"is this configuration actually PLAYABLE?"** including:

- KPM in target band for the progression node
- Skill rotation feels coherent (not degenerate; not chaotic)
- Resource flow works (mana/energy/cooldowns produce sustained-but-non-trivial play)
- Defensive uptime adequate
- No degenerate states (per § 8.8.1 8-pattern v1 catalog — explicit checks for known patterns FIRST + KPM-out-of-band as second-pass proxy)
- Visual/cognitive load manageable

**Playable-AND-in-band is the validation criterion.** Engineering-discipline candidate (now ratified as Discipline #26 per jack-ryan SC-2 2026-05-26).

#### 8.8.1 Degenerate-state detection — 8-pattern v1 catalog (LOCKED 2026-05-27 — closeout § 5.2)

**D61 AMENDMENT 2026-05-27:** Explicit degenerate-state detection COMPOSES with KPM-band gate. Hybrid approach (Approach C): explicit checks for known patterns FIRST + KPM-out-of-band as second-pass proxy.

**8-pattern v1 catalog:**

| # | Pattern | Detection rule |
|---|---|---|
| 1 | **Infinite stunlock** | time-in-CC > 60% encounter duration |
| 2 | **Zero-damage void** | player damage dealt < 1% expected OR taken < 1% expected |
| 3 | **Mandatory-skill-lock** | only 1 viable rotation (cohesion-judge metric) |
| 4 | **Permanent-CC** | movement-blocked > 70% encounter |
| 5 | **Resource-starvation** | resource < skill cost > 50% encounter |
| 6 | **Degenerate-tank** | defensive_uptime > 99%; pure DPS check (offensive-floor failed) |
| 7 | **Bounce-CC** | skill-cancellation rate > 50% attempted casts |
| 8 | **Resource-overflow** | resource at max > 80% encounter (paradoxical — unused capacity) |

**Substrate-led extension via Cycle 13 telemetry:** as new degenerate patterns surface empirically, the catalog extends. v1 catalog ships with these 8; future cycles add per pattern recognition.

**Methodology consultation per Discipline #18 fires:** gamora + legolas Mode A + star-lord (per closeout § 5.2; consultation timing per #18.2 — fires post-baseline empirical data, not before).

### 8.9 Decision points

> **EN-BLOC AMENDMENT 2026-05-27 (doc 47 § 5.5 + § 4.2 / § 4.3 / § 4.4; composition added — applies to D63-D86):** the Multi-T4 architecture decision block (D63-D86) composes with doc 47 damage scaling routing. Integration points: Category A T4 effects (character-wide) apply on top of routed damage calculation per damage_scaling_type; Category B effects apply chain-multiplicatively within the routed path; Category C effects (element conversion / dual element addition) apply at the element resolution step within the appropriate path. The 4-phase T4 algorithm canonical form (D81) is NOT amended by doc 47; the integration point is at fight engine routing (Track D.4 gamora scope). Per-skill `damage_scaling_type` declaration (Track D.2 rocket scope per doc 47 § 7.1) is the upstream emission that the fight engine routes against. See § 0.1 amendment-pass-record.

- **D63** — Skill tree SUPPORTS 2-3 T4 capstones per class
- **D64** — All class T4 capstones REACHABLE; no exclusivity-gate locks between T4 paths
- **D65** — Multi-T4 viability via respec-driven attunement with legendary-triggered free-respec opportunities; full mechanism specification per § 8.5
- **D66** — Non-attuned T4 chains NOT mechanically active (only current-invested T4 chain accessible until respec). **SHARPENED 2026-05-27 (closeout § 1.3):** ONE T4 unlocked at a time — sharpens from passive description to ACTIVE IDENTITY DISCIPLINE. Composes with D65 respec-with-legendary-trigger as swap mechanism + D76 dual-effect architecture (concentrated identity, not diluted).
- **D67** — Balance validated via independent gauntlet sim per attuned-T4 configuration per progression node
- **D68** — Retired/replaced by D76 (dual-effect T4 architecture provides natural differentiation; play-feel discipline redundant)
- **D69** — Specific skill tree architecture deferred to T4 PM1. **AMENDED 2026-05-27 (closeout § 1.1, Q7 item 1):** LOCKED — chain-based investment + LINEAR default within chain + SHARED skill point pool across chains + T4 unlocked by chain-investment threshold. Branching gated by chain depth ≥4 (per § 8.3.1). Closest genre analog: Grim Dawn mastery trees with PoE-2-tight node count + algorithmic mechanic-alteration as per-node payload. 9-16 total nodes per kit matches `canonical/story/skill-system-2026-05-24.md` 10-15 budget. Per-skill mini-trees (LE-style) rejected; PoE mega-tree rejected.
- **D70** — Specific T4 count per class formula locked at D83
- **D71** — Skill point economy + investment mechanic deferred to T4 PM1. **AMENDED 2026-05-27 (closeout § 1.5):** LOCKED with graduated per-node investment caps — Per-node max Passive = **5 points**; Active T1-T3 = **15 points**; T4 capstone = **1/1 binary** (0/1 if another T4 selected per D66 sharpening); Endgame total budget = **~70 points** (anchor; tunable); T4-unlock threshold = **70% of chain max** (per-chain calc; chain max varies by composition); Earn rate = **Per-level (L1→L50 = 50 points) + per-content-completion bonuses (~20)**; Branched-chain T4-unlock = all UNIQUE prerequisites along one path; other branch optional pay-extra. Composes with L50 hybrid framework (`canonical/41-progression-framework-2026-05-27.md`) — 50 raw + ~20 bonus = 70-point endgame anchor.
- **D72** — Closed by D82 (flat 8 active skills)
- **D73** — Respec rules within Servant deferred to T4 PM1. **AMENDED 2026-05-27 (closeout § 1.6):** LOCKED two-option respec — (1) **T4-respec** IF player has multiple chains above T4-unlock-threshold (swap which T4 is active); (2) **Full respec** always available. Spirit Guide offers to auto-allocate points during full respec if desired. Full respec cost = DEFERRED to Cycle 14+ (gear/currency infrastructure needed). Player-facing trigger = **Spirit Guide initiated OR player asks Spirit Guide**. D75 T4-swap UX resolves to Spirit-Guide-as-surface. Chain-level respec (between T4-only and full) DEFERRED to v1.1+ if substrate-evidence shows binary too rigid.
- **D74** — Multi-T4 sim methodology refined by D84
- **D75** — T4 swap UX + spirit-guide-presented respec offer presentation deferred to drax player-surface work; revert use-case rejected per D79 (drax can deprioritize save/load if no other use-case)
- **D76** — Dual-effect T4 architecture: each T4 mechanically alters BOTH character as a whole AND within-chain (or parallel-chain); differentiation emerges by construction
- **D77** — Closed by D65 specification (implementation questions answered)
- **D78** — Spirit-guide pacing discipline operationalized through D65 mechanism (selective triggers + time-bounded expiration + no-revert)
- **D79** — Commitment-to-consequence design discipline; engineering-discipline candidate; applies broadly
- **D81** — T4 algorithm canonical form locked: capstones at chain tops; 2-3 per class; one selected at a time; dual mechanical impact; all 4 phases in Cycle 13
- **D82** — Active skill budget: flat 8 maximum
- **D83** — T4 count per class = chain count - 1; supporting chains enable hybrid/multi-element builds
- **D84** — Combat sim node-population algorithm: hybrid cohort + edge-case sampling with per-legendary anchoring; gamora methodology consultation per Discipline #18
- **D85** — Cycle 13 scope expansion: all 4 phases of T4 + full gear-attunement architecture wrap into Cycle 13; scope-doc authoring expands (4-8 hours gandalf); compute budget for Phase 4 + multi-T4 sim methodology load-bearing
- **D86** — Multi-seam coordination criticality elevated; Gate-1 critique-pair throughput becomes scheduling constraint; knight-rider orchestration load-bearing for Cycle 13 viability

### 8.10 Playability criterion as discipline candidate

- **D61** — Playability elevated as load-bearing sim validation criterion beyond raw numerical balance; engineering-discipline candidate for jack-ryan
- **D62** — Low-compute-yet-meaningful sim cycle is real constraint; methodology approaches (stratified sampling, tiered validation, quick-estimate hybrid, caching) gamora territory

### 8.11 Dependency markers for downstream work cycles

- **D58** — Skill-tree structure deferred to T4 PM1
- **D59** — Active skill budget locked by D82 (closes earlier deferral)
- **D60** — Sim methodology for node-population sampling + playability validation deferred to gamora consultation (Discipline #18) within Cycle 13

---

## 9. Cycle 13 scope mapping

This § maps every doc-40 decision to its Cycle 13 (or post-Cycle-13) work-cycle home. Companion to § 10 (which lists orphans — decisions without a Cycle 13 home).

### 9.1 Cycle 13 in-scope (architectural foundation applied)

| Decision range | Topic | Cycle 13 home |
|---|---|---|
| D1-D6 | Balance as property | Cycle 13 cross-cutting principle; applies to all generation/validation work |
| D7-D17 (selected) | Spec-driven gear gen pattern + capability toolkit + tier structure | Cycle 13 generation work (rocket); informs stat-sheet partition cycle (D14) |
| D11 | Epic→Legendary discontinuity load-bearing | Cycle 13 acquisition curve calibration |
| D13-D14 | Stat-sheet partition principle + work cycle | **EARLY Cycle 13 milestone** — multi-seam work cycle (gandalf + gamora + rocket + jack-ryan + legolas Mode A); fires BEFORE gauntlet sim |
| D15 | Architecture B substrate-bound at Phase 2 | Cycle 13 substrate-binding work (composes with existing Architecture B lock) |
| D18-D27 | 85th-percentile target + Option A + multi-node calibration architecture | Cycle 13 acquisition curve work; multi-node WORK is post-Cycle-13 (D27 final clause) |
| D28-D32 | Spirit guide as data-oracle pattern | Cycle 13 spirit-guide integration work; multi-seam (gamora projections + drax surface + rocket metric exposure + gandalf voice) |
| D33-D39 | T4-attuned gear intent | Cycle 13 gear-attunement implementation; gates on T4 PM1 specifics (D38) |
| D44-D47 | Auto-combat correction | Cycle 13 cross-cutting (canonical correction; not a work-cycle item per se but propagates) |
| D48-D57 | Tier structure + capability toolkit at all tiers + triggered-passive added skills | Cycle 13 generation work (rocket); informs partition cycle |
| D63-D67 | Skill tree supports 2-3 T4 capstones reachable; balance via independent sim validation | Cycle 13 skill tree architecture (gates on T4 PM1) |
| D65 | Respec-with-legendary-trigger mechanism | Cycle 13 mechanism implementation (rocket + drax + gamora); multi-seam |
| D76 | Dual-effect T4 architecture | Cycle 13 T4 algorithm implementation per § 8.2 Phase 3 |
| D78-D79 | Spirit-guide pacing + commitment-to-consequence disciplines | Cycle 13 cross-cutting disciplines |
| D80 | Gap-filling acquisition discipline | Cycle 13 stat-sheet partition cycle + acquisition curve calibration |
| D81 | T4 algorithm canonical form (all 4 phases in Cycle 13) | Cycle 13 T4 implementation work — ALL FOUR PHASES |
| D82 | Active skill budget flat 8 | Cycle 13 implementation |
| D83 | T4 count per class = chain count - 1 | Cycle 13 class design (per T4 PM1) |
| D84 | Sim methodology: hybrid cohort + edge-case + per-legendary anchoring | Cycle 13 gamora methodology consultation (Discipline #18); fires BEFORE gauntlet sim at scale |
| D85 | Cycle 13 scope expansion (all 4 T4 phases) | Cycle 13 scope-doc explicit |
| D86 | Multi-seam coordination criticality | Cycle 13 knight-rider orchestration |

### 9.2 Gates on T4 PM1 (Cycle 13 deferred specifics)

These decisions are Cycle-13-in-scope but their SPECIFICS depend on T4 PM1 output:

| Decision | Specifics deferred to T4 PM1 |
|---|---|
| **D58** | Skill-tree structure (LE-style mini-trees vs chain-based vs hybrid) |
| **D69** | Specific skill tree architecture choice |
| **D71** | Skill point economy + investment mechanic |
| **D73** | Respec rules within Servant |
| **D38** | T4-attuned gear architectural specifics (attunement magnitudes, cross-rarity distribution, set bonus structure, binary vs graduated) |
| **D70** | (Closed by D83 formula) |

### 9.3 Post-Cycle-13 work (architectural foundation applies; work fires later)

| Decision range | Topic | When |
|---|---|---|
| D27 (multi-node WORK) | Full multi-node calibration WORK across all 4 progression nodes | Post-Cycle-13 engine extension |
| D2 (Pattern B pre-gen library) | 1-2 year sustainable content library generation | Post-Cycle-13 (engine maturity work) |
| D40-D43 | Peak-moment community layer (Stage 1-6) | Post-launch (multi-season build-out) |
| D75 (T4 swap UX) | Drax player-surface work for T4 swap mechanics + legendary trigger UI | Cycle 13 OR post-Cycle-13 (drax scoping) |

### 9.4 Cycle 13 sequencing summary

Based on dependencies + named milestones:

1. **T4 PM1 design session** (gates Cycle 13 launch) — produces architectural specifics for D58, D69, D71, D73, D38
2. **Cycle 13 scope-doc authoring** (gandalf, 4-8 hours per D85) — captures expanded scope
3. **Stat-sheet partition design cycle** (early Cycle 13 milestone) — multi-seam work
4. **Gamora methodology consultation** (per D60 + D84) — establishes sim node-population approach
5. **Phase 1 implementation:** T4s into chains as capstones — rocket + jack-ryan critique
6. **Phase 2 implementation:** multiple T4 options per chain — rocket + gandalf + jack-ryan
7. **Phase 3 implementation:** character-wide vs chain-wide scope dimension — rocket + gandalf + gamora + jack-ryan
8. **Phase 4 implementation:** full sim cycling — gamora + rocket
9. **Gauntlet battle sim** against full architecture
10. **Drax integration:** T4 swap UX, legendary triggers, spirit-guide offers

---

## 10. Orphan check — decisions WITHOUT a Cycle 13 home

Per Matt's request: explicit identification of doc-40 decisions that do NOT have a Cycle 13 home.

### 10.1 True orphans (deferred indefinitely / require separate cycles)

| Decision | Status | Disposition |
|---|---|---|
| **D40-D43** (peak-moment community layer Stage 1-6 implementation) | Architectural intent locks; implementation phasing fully post-launch | **NOT in Cycle 13** — implementation work cycle fires post-launch or alongside community-system work; architectural intent applies to Cycle 13 generation/spirit-guide work (foundations laid) |
| **D2 (Pattern B pre-gen library)** | Architectural pattern committed; sustained content library generation is engine maturity work | **NOT in Cycle 13** — Cycle 13 lays foundations (spec-driven gear gen, partition design, validation methodology); 1-2 year sustainable library generation is post-Cycle-13 engine extension |
| **D27 (multi-node calibration WORK)** | Architecture committed (4 named nodes); full multi-node calibration WORK is engine extension | **PARTIAL in Cycle 13** — Cycle 13 lays architectural foundations (partition design accounts for 4 nodes; acquisition curve math is multi-node); full multi-node implementation + cross-season learning loop is post-Cycle-13 |

### 10.2 Cycle 13 in-scope but requires explicit scope-doc enumeration

These decisions are Cycle 13 work-units but easy to overlook without explicit enumeration in the Cycle 13 scope-doc:

| Decision | Why explicit enumeration matters |
|---|---|
| **D44-D47** (auto-combat correction) | Cross-cutting canonical correction; not a "build something" task but propagates everywhere; scope-doc should reference doc 40 § 1 as authoritative |
| **D61 + D62** (playability criterion + low-compute sim constraint) | Engineering-discipline candidates flagged to jack-ryan but operationally apply to Cycle 13 gauntlet sim work; scope-doc should reference |
| **D78 + D79** (spirit-guide pacing + commitment-to-consequence) | Cross-cutting design disciplines; applied through D65 mechanism in Cycle 13 but the disciplines themselves propagate to OTHER systems too; scope-doc should reference |
| **D80** (gap-filling acquisition discipline) | Stat-sheet partition cycle input; scope-doc must propagate to partition cycle work explicitly |
| **D84** (sim methodology — gamora consultation gate) | Methodology consultation fires BEFORE partition lock + BEFORE gauntlet sim runs at scale; sequencing must be explicit in scope-doc |
| **D85 + D86** (Cycle 13 scope expansion + multi-seam coordination criticality) | Scope-doc IS the documentation of D85/D86; meta-decision that scope-doc must capture itself |

### 10.3 Disposition

**No true orphans require Cycle 13 reconsideration.** All architectural foundations either:
- Apply to Cycle 13 work directly (most decisions)
- Defer specifics to T4 PM1 within Cycle 13 (named items)
- Defer implementation to post-Cycle-13 with architectural foundation laid (D2, D27, D40-D43)

Doc-40 is operationally complete as Cycle 13 architectural foundation. Cycle 13 scope-doc (when authored, gates on T4 PM1) maps every doc-40 decision to specific work-units OR explicit deferral with empirical-evidence gate.

---

## 11. Cross-references

### 11.1 Canonical docs

- `canonical/00-ground-state.md` — register doc 40 as new CURRENT entry in § 1; auto-combat correction (§ 1.4 D44) updates § 3 DEAD entries (auto-combat REJECTED 2026-05-23) with current Matt-clarified disposition for mobile-variant deferral
- `canonical/02-roadmap.md` — add doc 40 to companion docs; add Cycle 13 architectural foundation entry to roadmap § 1.0 active workstreams (when Cycle 13 opens); add stat-sheet partition cycle as named early-Cycle-13 milestone
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — cross-reference balance-as-property § 2 from D10 Path A pitch material
- `canonical/37-engine-and-game-two-products.md` — composes with engine-as-product pitch (D10 Path A); balance-as-property strengthens engine commercial pitch
- **`canonical/46-concentration-architecture-2026-05-27.md` — concentration architecture, 9 layers; § 13 inheritance amendments LANDED at doc 40 per § 0.1.2 amendment-pass-record (Cycle 14 SC-2; 2026-05-27)**
- **`canonical/47-damage-scaling-architecture-2026-05-27.md` — damage scaling architecture (physical / magical / hybrid); § 5.5 composition amendments LANDED at doc 40 per § 0.1.3 amendment-pass-record (Cycle 14 SC-2; 2026-05-27)**
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B substrate-bound at Phase 2; spec-driven gear gen (§ 3) sharpens toward this; D15 explicit
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` — T4 architecture defaults predecessor; § 8 of this doc extends with full algorithm canonical form (D81 + 4-phase implementation)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — per-season anchor variability lock composes with multi-T4 architecture
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern + 10-15 node skill tree predecessor; § 8 multi-T4 + active-skill-budget extends
- `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system composes with stat-sheet partition cycle (D14)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` — per-kit skill-budget (~11-13 nodes); § 8 D82 (flat 8 active skills) refines

### 11.2 Operational + agent docs

- `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` — T4 PM1 prep doc; this canonical doc INFORMS T4 PM1 + RECEIVES T4 PM1 outputs in Cycle 13 sequencing
- `agentic_orchestration/gandalf/matt_conversations/skills_and_gear_discussion` — source conversation; § 1.2 captures auto-combat attribution correction; substantive design insights extracted across Blocks 1-5
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #18 (methodology consultation at math hotspots) applies to stat-sheet partition cycle + sim methodology consultation per D60/D84; Discipline #23 (framing-audit) 3rd operational instance per § 1.4
- `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md` — Cycle 13 will require per-cycle scope-of-autonomy enumeration; doc 40 informs that scope-doc authoring

### 11.3 Decisions-log

Cycle 13 launch + scope-doc landing will produce decisions-log entries for the architectural commitments here. Not yet logged (Cycle 13 not yet open as of 2026-05-26).

---

## 12. Operational notes

### 12.1 To jack-ryan (engineering-discipline candidates)

Five new engineering-discipline candidates emerge from this session for jack-ryan to ratify alongside ongoing engineering-disciplines work:

1. **Playability discipline (D61):** combat sim validation criterion beyond raw numerical balance; "playable-AND-in-band" is the gate — ✅ RATIFIED 2026-05-26 as Discipline #26
2. **Dual-effect capstone discipline (D76):** multi-capstone systems should architect capstones to have dual-effect structure (character-wide + chain-specific) to ensure natural differentiation — ✅ RATIFIED 2026-05-26 as Discipline #27
3. **Spirit-guide-pacing discipline (D78):** offer-triggering mechanisms must avoid training players to defer commitment indefinitely — ✅ RATIFIED 2026-05-26 as Discipline #28
4. **Commitment-to-consequence discipline (D79):** decision-mechanisms that require commitment-to-consequence produce more meaningful engagement; reversibility degrades engagement AND advisory-system trust — ✅ RATIFIED 2026-05-26 as Discipline #29
5. **Sim methodology naming discipline (D84):** combat sim methodology must explicitly name its node-population sampling approach + cohort coverage + edge-case handling — ✅ RATIFIED 2026-05-26 as Discipline #30

**NEW candidates from Matt + gandalf Pattern-B session 2026-05-27 (closeout § 7):**

6. **Dual-effect separability discipline (D76 amendment) → #31:** Category A (character-wide) and Category B/C (chain-specific) effects MUST be INDEPENDENTLY COHERENT — removing one should leave the other as a genuine standalone mechanic. Failure mode: T4s where chain effect is just "consequences of character-wide effect spelled out in chain terms." [Founding instance: corrected Blood Magic example 2026-05-27.] — ❌ awaiting jack-ryan SC-2 expansion ratification
7. **First-do-no-harm discipline for algorithmically-generated T4 keystones → #32:** Synergy detection MUST include downstream-tension-creation check (Pass 2 preserve), not just upstream-tension-resolution (Pass 1 resolve). Net synergy score balances both passes. Failure mode: T4s that solve a stated problem by introducing an equally-bad new problem. [Founding instance: two-pass synergy scan 2026-05-27 per § 8.4.3.] — ❌ awaiting jack-ryan SC-2 expansion ratification

Plus operational note: **Discipline #23 3rd operational instance** captured here (§ 1.4) — caught DURING canonization. Worth referencing in Discipline #23 amendment write-up. (Now ratified inline at engineering-disciplines.md as of 2026-05-26.)

### 12.2 To gamora (methodology consultation gate)

Methodology consultation per Discipline #18 (+ OP § 4.2 refinement) fires for:

1. **Stat-sheet partition design (D14):** modifier surface enumeration + slot partition design + node-interaction mathematics; uses existing empirical baseline (W1.13 + prior sim findings)
2. **Combat sim node-population (D84):** hybrid cohort + edge-case sampling with per-legendary anchoring; primary methodology evaluation; Sub-option A vs B vs hybrid-within-hybrid
3. **Multi-T4 sim methodology (D74):** how sim samples across T4 configurations; composes with D84

All three consultations fire BEFORE the corresponding implementation work at scale (partition lock before gauntlet sim; methodology before sim runs at full combinatorial scale).

### 12.3 To knight-rider (Cycle 13 orchestration criticality)

Cycle 13 scope expansion per D85 + D86 means knight-rider orchestration becomes load-bearing for cycle viability:

- **All 4 T4 phases** in single cycle (vs phased across multiple cycles) = more concurrent + sequenced work
- **Multi-seam coordination** across gandalf + gamora + rocket + jack-ryan + drax + legolas
- **Gate-1 critique-pair throughput** is real constraint (Phase 1 + 2 + 3 + 4 + partition cycle + sim methodology consultation = 6+ critique-pair cycles)
- **Compute budget for Phase 4** + multi-T4 sim methodology = real constraint; gamora consultation per D84 must address
- **Cycle 13 scope-doc authoring** expands to 4-8 hours gandalf (vs prior 2-4 estimate) given coordination complexity

Knight-rider scope-doc consumption + dispatch sequencing become elevated work.

### 12.4 To drax (player surface deferred work)

D75 (T4 swap UX + legendary-trigger UI + spirit-guide-presented respec offer presentation) deferred to drax player-surface work cycle. Revert use-case rejected per D79 — drax can deprioritize build save/load if no other compelling use-case emerges. Other build save/load use-cases (peak-moment artifacts per D40; spirit-guide historical-context surface) may surface; deprioritize until they do.

### 12.5 To rocket (generation implementation across 4 T4 phases)

Cycle 13 generation work spans all 4 T4 phases + stat-sheet partition implementation + capability toolkit + tier structure + spec-driven gear gen registry pattern. Substantial generation-side work; multi-cycle work-units within single Cycle 13.

### 12.6 To elrond (substrate-side)

Substrate-binding decisions composes with existing Architecture B lock; spec-driven gear gen + tier structure may require schema extensions for T4-attunement metadata + capability toolkit metadata + tier classification. Schema extension MIGRATION docs as appropriate.

### 12.7 To legolas (Mode A research)

Methodology grounding for stat-sheet partition cycle (D14): external-literature research on how other ARPGs partition stat modifiers (Diablo affixes, PoE modifier pools, Last Epoch idol/affix system, Grim Dawn prefixes/suffixes). Mode A consultation per gandalf or gamora request when partition cycle fires.

---

**Signed:** gandalf (story-and-design steward)
**For:** the Cycle 13 architectural foundation derived from `skills_and_gear_discussion` source conversation + iterative 5-block design session 2026-05-26. 86 locked decisions across balance-as-property + spec-driven gear generation + 85th-percentile acquisition + spirit-guide-as-data-oracle + multi-T4-architecture-with-respec-mechanism. Cycle 13 scope-doc (when authored post-T4-PM1) maps every decision to specific work-units. Authoritative source for CURRENT-status truth remains `canonical/00-ground-state.md`.
