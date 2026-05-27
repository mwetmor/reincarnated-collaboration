# 43 — T4 Algorithm Wave 2 Intent (Cycle 13 — 2026-05-27)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — Wave 2 T4 algorithm design INTENT canonical for Cycle 13 multi-T4 architecture cycle; see `canonical/00-ground-state.md`

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — Wave 2 T4 algorithm design intent; 3-category T4 taxonomy operationalized + DUAL_ELEMENT_ADDITION strategy spec + parallel-chain reach spec + compositional synergy scan two-pass framework with 5-category synergy taxonomy (4 original + NEW Scaling-interaction per SC-4 expansion) + T4-failure-handling Option F hybrid retry mechanism spec + Pattern 9 + Pattern 10 degenerate-state catalog candidates (design-intent; detection-algorithm calibration delegated to gamora SC-7) + one-T4-unlocked-at-a-time discipline + variable 3-or-4 class chain architecture + sub-wave structure W2.0-W2.9 + Wave 2 implementation guidance for rocket
**Authority:** Matt 2026-05-27 verbatim — "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope. No further Matt-creative-ratification gates on Cycle 13 progression." + jack-ryan Wave 1 Gate-2 PASS-with-WARN (commit `2aa6813`) + jack-ryan SC-6 Gate-2 PASS (commit `ee15c96`) unblock Wave 2 + jack-ryan Wave 1 Gate-1 I2/W3/I1 routing
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — engine workflow Phase 2d spec-driven gear gen
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation (D1-D86 + 2026-05-27 amendments; § 8 multi-T4 architecture is Wave 2 substrate)
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid + cell × node × cohort context
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — Wave 1 partition intent (precedent doc structure; Wave 2 consumes its gear-instance + T4-attunement annotation surface)
- `canonical/02-roadmap.md` — engine build visual-flow progress tracker
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — Matt + gandalf Pattern-B session closeout § 2.4 (T4 algorithm 3-category taxonomy lock) + § 2.5 (compositional synergy scan two-pass) + § 7 (engineering-discipline candidates #31 + #32 founding instances)
- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` — legolas SC-4 expansion; **Wave-2-informing:** 5th Scaling-interaction synergy category + Pass 1/Pass 2 empirical validation across ARPGs for Discipline #32 first-do-no-harm; **Wave-4-informing (surfaced here Wave-2):** Pattern 9 (passive screen-clear) + Pattern 10 (DoT-stack degenerate) catalog extension candidates
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-gate-1-doc-42-critique.md` — I2 (#27 + #31 + #32 composition routing) + W3 (SC-4 expansion 5th category + Pattern 9+10) + I3 (Wave 2 discipline citation gap) routing
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-1-partition-gate-2.md` — I1 (`legendary_t0_5` rarity round-trip carryover) + WARN-pattern partial remediation status (Wave 2 Gate-2 = full closure target)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC operational truth (cross-cohesion validation coordinate system)
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern (T4 capstones sit at chain tops)

---

## 0. TL;DR

Wave 2 T4 algorithm design intent for Cycle 13 multi-T4 architecture cycle. Operationalizes the **3-category T4 taxonomy** (A class-mechanical character-wide + B chain-multiplicative chain-specific + C chain-element-conversion-or-addition chain-specific; locked per closeout § 2.4 + doc 40 § 8.4 amended; SUPERSEDES the 6-strategy registry as design-spec + player-facing vocabulary while retaining the 6 strategies as algorithm implementation detail under the 3-category umbrella). Specs the **NEW DUAL_ELEMENT_ADDITION strategy** (Category C extension; chain skills retain primary element AND add secondary element; PoE "X% physical as fire" / D4 "all skills deal X% as cold" genre precedent; magnitude band ANCHORED with starting estimates per Verdict-B.4-pattern; gamora SC-7 iterates post-Wave-2). Specs the **parallel-chain reach** (chain-specific effect can target T4's OWN chain OR a PARALLEL chain; algorithm-fixed at generation time; composes with variable 3-or-4 chain architecture as depth-vs-breadth lever). Specs the **compositional synergy scan two-pass framework** (Pass 1 resolve + Pass 2 preserve; net synergy score = resolve − create; pattern library + statistical priors + algorithmic composition NOT LLM raw-reasoning per D7; **5-category synergy taxonomy** = tension-resolution + theme-compound + cross-chain composition + element-gap fill + NEW Scaling-interaction per SC-4 expansion Topic 2 verdict). Specs **T4-failure-handling Option F hybrid retry mechanism** (Phase 1: 3-attempt regeneration with alternate strategies; Phase 2: ship with partial T4 if all regeneration fails; Phase 3: ≥1 T4 in-band minimum threshold; Phase 4: track regeneration rate as quality metric). Surfaces **Pattern 9 (passive screen-clear / engagement-elimination) + Pattern 10 (DoT-stack degenerate / unbounded DoT compounding)** as design-intent for generation-time failing-fast detection (compose with #32 Pass 2 preserve check); full detection-algorithm calibration delegated to gamora SC-7 post-Wave-3-baseline per Discipline #18.2. Locks the **one-T4-unlocked-at-a-time discipline** (D66 sharpened: active identity, not passive description; composes with D65 respec-with-legendary-trigger swap + D76 dual-effect concentration). Locks the **variable 3-or-4 class chain architecture** at design-intent abstract layer (3-chain = 2 T4 capstones + 1 supporting; 4-chain = 3 T4 capstones + 1 supporting; per-class roster DEFERRED per Block A2b deferred-commitment per closeout § 1.4). Provides **sub-wave structure W2.0-W2.9** (10 sub-waves; mirrors doc 42 § 9.6 W1.0-W1.8 implementation-atomic pattern) for rocket Wave 2 implementation. Provides **Wave 2 implementation guidance for rocket** including substrate consumption from Wave 1 partition (T4-attunement annotation metadata on Tier-1+2 legendary + sets; capability-toolkit-as-chain-effect-composer surface). Wave 2 close criterion = jack-ryan Gate-2 PASS on rocket Wave 2 implementation against this intent; full WARN-pattern remediation target per Wave 1 Gate-2 partial-remediation status. Disciplines #1 + #1.2 + #11 + #18 + #18.2 + #26 + #27 + #29 + #30 + #31 + #32 compose throughout.

---

## 1. Architectural foundation cross-references

This doc operationalizes the Wave 2 T4 algorithm design intent grounded in the locked architectural foundation.

| Foundation doc | What it provides | Where this doc operationalizes |
|---|---|---|
| **Doc 38** (D1-D10 delivery strategy) | Variant C engine-vs-game; isekai provisional; ~30-day seasonal | Composes with § 13 |
| **Doc 39** (QD-engine workflow Architecture B) | Phase 2 spec-driven content gen substrate-bound | Wave 2 T4 algorithm executes within Phase 2 generation pipeline; consumes Wave 1 partition output |
| **Doc 40** (Cycle 13 architectural foundation, post-amendments) | § 8 multi-T4 architecture; § 8.4 3-category T4 taxonomy LOCKED; § 8.4.1 DUAL_ELEMENT_ADDITION strategy NEW LOCKED; § 8.4.2 parallel-chain reach LOCKED; § 8.4.3 compositional synergy scan LOCKED; D66 sharpening one-T4-at-a-time; D76 dual-effect; D83 T4 count = chain count − 1; D65 respec-with-legendary-trigger; D67 independent gauntlet sim validation; D62 compute budget; § 8.2 T4-failure-handling Option F LOCKED | This doc IS the operationalization of doc 40 § 8 + § 8.4.x for Wave 2 implementation |
| **Doc 41** (L50 hybrid progression framework) | L1-L50 cap + content-tier-driven endgame; node-to-level-band mapping; 4 progression nodes | T4 unlock economics (per closeout § 1.5 + D71 amended: 70-point endgame budget; T4 unlock at 70% chain max) compose with L50 framework |
| **Doc 42** (Wave 1 partition intent) | 9-category × 11-slot affinity matrix; per-rarity grid with T4-attunement annotation on Tier-1+2 legendary + sets; capability toolkit legendary-exclusive surface | Wave 2 T4 algorithm CONSUMES partition output: T4-attunement annotation metadata as scoring input; capability-toolkit-as-chain-effect-composer surface as legendary-added-skill consumption surface; spec-driven gear gen substrate ALREADY available per Wave 1 close |
| **Closeout doc 2026-05-27** | § 2.4 T4 algorithm 3-category taxonomy substantive lock + § 2.5 compositional synergy scan two-pass resolve+preserve + § 1.3 D66 sharpening one-T4-at-a-time + § 1.4 variable 3-or-4 chains + § 1.7 T4-failure-handling Option F lock + § 5.2 8-pattern v1 degenerate catalog + § 7 engineering-discipline candidates #31 + #32 founding instances | Source authority for all locks in this doc |
| **SC-4 expansion research 2026-05-27** | Topic 2 § 2.2-2.3 NEW Scaling-interaction synergy category + Pass 1/Pass 2 empirical validation across 4 ARPGs; Topic 3 § 3.4-3.5 Pattern 9 + Pattern 10 v1 catalog extension candidates | § 5 5-category synergy taxonomy includes Scaling-interaction as 5th category; § 7 Pattern 9 + Pattern 10 candidate specs |
| **8-axis BC lock** | 68,040 cells; operational measurement coordinate system | T4 algorithm scoring + cross-cohesion validation per #26 operate on BC-axis cells per § 11.8 cross-cohesion scaffolding |

**Authority basis:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 1 Gate-2 PASS-with-WARN on rocket partition implementation (commit `2aa6813`) + jack-ryan SC-6 Gate-2 PASS on rocket SC-6 work-unit (commit `ee15c96`) unblock Wave 2 dispatch + Wave 1 Gate-1 I2/W3 routing requirements direct Wave 2 fold-in of Disciplines #27/#31/#32 + SC-4 expansion 5th Scaling-interaction + Pattern 9+10.

---

## 2. T4 algorithm 3-category taxonomy — operationalization

Per closeout § 2.4 + doc 40 § 8.4 amended. The 3-category taxonomy SUPERSEDES the 6-strategy registry (doc 40 § 3.2 original) as design-spec + player-facing vocabulary. The existing 6 strategies are RETAINED as algorithm implementation detail under the 3-category umbrella.

### 2.1 Three-category framework

| Category | Role | D76 dual-effect part | Algorithm strategies mapping | Always present? |
|---|---|---|---|---|
| **A — Class mechanical / energy alteration** | Character-wide effect | Character-wide effect (always present per D76 dual-effect) | RESOURCE_CONVERSION, DEFENSIVE_CONVERSION, DEFENSIVE_TRADEOFF, class-wide TRADE_OFF | YES — every T4 has Category A |
| **B — Chain multiplicative event** | Chain-specific (exactly one of B or C per T4) | Chain-specific effect | Skill-specific TRADE_OFF, GEOMETRY_COLLAPSE, multiplier strategies | One of B or C |
| **C — Chain element conversion / addition** | Chain-specific (exactly one of B or C per T4) | Chain-specific effect | ELEMENT_CONVERSION, **NEW: DUAL_ELEMENT_ADDITION** (per § 3) | One of B or C |

**Composition rule:** every T4 = Category A (character-wide; always present) + exactly one of Category B OR Category C (chain-specific). NEVER both B and C on the same T4; NEVER neither.

### 2.2 Strategy-to-category mapping detail

The 7 algorithm strategies (6 original + DUAL_ELEMENT_ADDITION new) map under the 3-category umbrella:

| Strategy (algorithm-level) | Category | Notes |
|---|---|---|
| RESOURCE_CONVERSION | A | Character-wide: alters resource model (e.g., HP-as-resource conversion à la Blood Magic) |
| DEFENSIVE_CONVERSION | A | Character-wide: converts one defensive layer to another (e.g., evasion-to-armor à la Iron Reflexes) |
| DEFENSIVE_TRADEOFF | A | Character-wide: trades defensive capability for offensive multiplier or vice versa |
| Class-wide TRADE_OFF | A | Character-wide: general tradeoff pattern (e.g., movement-speed-for-damage; cooldown-for-resource-cost) |
| Skill-specific TRADE_OFF | B | Chain-specific: per-skill or per-chain tradeoff (e.g., this chain's skills cost double mana but deal 2.5× damage) |
| GEOMETRY_COLLAPSE | B | Chain-specific: alters geometry of chain's skill emanations (e.g., AoE-to-projectile collapse) |
| Multiplier strategies | B | Chain-specific: large multiplicative event on chain (e.g., 3× damage on this chain's skills when condition X) |
| ELEMENT_CONVERSION | C | Chain-specific: chain's primary element converted to alternative (e.g., fire chain becomes cold) |
| **DUAL_ELEMENT_ADDITION (NEW)** | C | Chain-specific: chain retains primary element AND adds secondary (per § 3 spec) |

### 2.3 Player-facing vocabulary mapping

The 3-category taxonomy is the player-facing surface. The 6 (now 7) strategies are algorithm implementation detail not surfaced to player vocabulary.

**Player-facing T4 description structure:**

> "[T4-name] alters [class-mechanic-altered] AND [chain-specific-effect]."

Where:
- `[class-mechanic-altered]` reflects Category A (character-wide; always present)
- `[chain-specific-effect]` reflects Category B OR Category C (chain-specific; exactly one)

Example (illustrative): a T4 with RESOURCE_CONVERSION + DUAL_ELEMENT_ADDITION would surface as:

> "Sanguine Pyre alters your class to spend HP instead of mana AND your fire chain skills also deal cold damage."

The player sees two effects (character-wide + chain-specific); the algorithm internally selected RESOURCE_CONVERSION (Category A) + DUAL_ELEMENT_ADDITION (Category C). The 6-strategy detail is invisible to the player.

### 2.4 D76 dual-effect separability discipline (Discipline #31)

Category A and Category B/C effects MUST be INDEPENDENTLY COHERENT. Removing one effect should leave the other as a standalone genuine mechanic — not as the "consequences of the other spelled out in chain terms."

**Failure mode** (founding instance per closeout § 7 candidate #6): a T4 where the chain effect is just "consequences of the character-wide effect spelled out in chain terms." Example: a Blood Magic T4 where the chain-specific effect is "your fire chain costs HP instead of mana" — this is NOT separable, because the chain effect is just the character-wide effect re-stated. Correct framing requires the chain effect be standalone meaningful (e.g., "your fire chain costs HP instead of mana AND fire skills convert 30% of physical damage to fire" — the second clause adds value independent of the first).

**Discipline #31 enforcement in algorithm:** Pass 2 preserve check (§ 5) includes a separability test — for each candidate T4, verify that removing Category A leaves Category B/C as a meaningful mechanic (not a degenerate restatement) AND vice versa. Candidates failing separability are rejected.

---

## 3. DUAL_ELEMENT_ADDITION strategy spec (NEW per closeout § 2.4)

Per doc 40 § 8.4.1 amended + closeout § 2.4 lock.

### 3.1 Mechanics

**Chain skills retain primary element AND add a secondary element.**

- Primary element preserved (chain identity intact)
- Secondary element added as additional damage layer
- Both elements scale from gear/passive investment in each element type
- Both elements interact with enemy resistances independently (creates tactical interplay)

### 3.2 Genre precedent

| Game | Mechanic | Notes |
|---|---|---|
| Path of Exile | "X% of physical damage as fire" (and similar conversions/additions) | Long-standing PoE design pattern; modular as "added-damage" affixes |
| Diablo 4 | "All skills deal X% as cold" (Aspect of Frozen Wake, etc.) | D4 aspect surface includes added-element variants |
| Last Epoch | Skill tree "X% of damage as [element]" nodes | LE's skill-tree-per-skill exposes added-element as a per-skill node-tier choice |
| Grim Dawn | Conversion chains (physical → fire → cold) | GD's full-conversion variant; DUAL_ELEMENT_ADDITION is partial-conversion analog |

**Substantively expands T4 design space** beyond pure conversion (ELEMENT_CONVERSION REPLACES the primary element; DUAL_ELEMENT_ADDITION COMPOSES with it). The strategy adds a category-C variant that's mechanically distinct from conversion.

### 3.3 Algorithm-side spec

**Generation:** when algorithm rolls Category C for a T4 candidate, it selects between ELEMENT_CONVERSION and DUAL_ELEMENT_ADDITION per:

1. **Class element compatibility check:** does the class have a `secondary_elements` list per `class_schema.py:46-47`? If yes, DUAL_ELEMENT_ADDITION is eligible (secondary element drawn from this list); if no, only ELEMENT_CONVERSION is eligible.
2. **Synergy scan score:** compositional synergy scan (§ 5) scores both candidates; the higher-net-synergy candidate wins.
3. **Pattern 10 (DoT-stack) preserve check:** if DUAL_ELEMENT_ADDITION would compound with existing DoT stacking on the chain to produce unbounded DoT compounding (per § 7.2 Pattern 10 candidate detection), the candidate fails Pass 2 preserve.

**Secondary element selection** (when DUAL_ELEMENT_ADDITION is selected):

- Drawn from class's `secondary_elements` list per `class_schema.py:46-47`
- If `secondary_elements` has multiple entries, scoring prefers the entry with highest cross-chain composition synergy score per § 5 (e.g., if a parallel chain already invests in cold, fire-with-added-cold composes well; if no parallel chain invests in cold, fire-with-added-lightning may compose better)
- If no `secondary_elements` entries exist for the class, DUAL_ELEMENT_ADDITION is not generated (only ELEMENT_CONVERSION available in Category C)

### 3.4 Magnitude calibration (ANCHORED starting estimates)

Per Verdict-B.4-pattern (doc 42 § 9.4): magnitude bands ANCHORED with starting estimates; gamora SC-7 iterates post-Wave-2-baseline per Discipline #18.2 (consultation at extension hotspots fires AFTER baseline empirical data, not before).

**Starting estimates for DUAL_ELEMENT_ADDITION secondary-element magnitude:**

| Magnitude tier | Secondary element damage as % of primary | Rationale (starting estimate; gamora SC-7 iterates) |
|---|---|---|
| **Low** | 15-25% added | Conservative; preserves primary-element identity; minimal trap-build risk |
| **Medium** | 25-40% added | Tactical-relevance threshold; secondary becomes meaningful in resistance-mismatch encounters |
| **High** | 40-55% added | Approaches PoE "X% as fire" mid-late-game tier; build-defining secondary contribution |

**Algorithm selects magnitude tier based on:**
- Class-archetype damage profile (higher-burst classes lean Low; sustained-DPS classes lean Medium/High)
- Cross-chain composition score (high cross-chain composition synergy → tilt Medium/High; low score → Low)
- Pattern 10 preserve-check headroom (DoT-stack risk reduces magnitude tier; non-DoT secondary tolerates higher tier)

**Gamora SC-7 consultation post-Wave-2:** baseline T4 generation telemetry (regeneration rate, in-band rate per cohort, KPM impact per magnitude tier) informs magnitude band recalibration. Starting estimates ship in Wave 2; calibration iterates Cycle 14+ per substrate evidence.

### 3.5 Composition with #27 + #31

- **#27 dual-effect capstone:** DUAL_ELEMENT_ADDITION is the Category C (chain-specific) effect; pairs with a Category A (character-wide) effect to form the dual-effect capstone
- **#31 dual-effect separability:** the Category A effect (e.g., RESOURCE_CONVERSION) must be standalone meaningful even if the DUAL_ELEMENT_ADDITION clause were removed; the DUAL_ELEMENT_ADDITION clause must add genuine secondary-element value independent of the Category A effect

---

## 4. Parallel-chain reach spec

Per doc 40 § 8.4.2 amended + closeout § 2.4 lock.

### 4.1 Mechanics

**Chain-specific effect can target the T4's OWN chain OR a PARALLEL chain.**

- T4 sits at the top of a particular chain (the "host chain")
- Category B/C chain-specific effect normally targets the host chain
- ALTERNATIVE: the chain-specific effect can target a different chain in the same class (a "parallel chain")
- Algorithm-fixed at generation time (not player-chosen)
- Per generation cycle, the algorithm selects own-chain vs parallel-chain target as part of T4 scoring

### 4.2 Composition with depth-vs-breadth lever

Variable chain count (3 or 4 per § 9) + branching gated by chain depth ≥4 means parallel-chain reach has variable target space per class:

| Class chain count | T4 count | Parallel-chain reach target space |
|---|---|---|
| **3-chain class** | 2 T4 capstones | Each T4 can target: (a) own chain, (b) the other T4-eligible chain, (c) the T3-only supporting chain |
| **4-chain class** | 3 T4 capstones | Each T4 can target: (a) own chain, (b) one of 2 other T4-eligible chains, (c) the T3-only supporting chain |

### 4.3 Enables cross-chain composition

Parallel-chain reach enables build-craft opportunities the player discovers via spirit-guide projections per closeout § 3.4 (data-oracle voice; "playing T4-A: projected KPM 75. Switching to T4-B: projected KPM 62. Net synergy score: T4-A composes 23% better with this gear AND amplifies wind chain by +18%").

Example (illustrative):
- A class has fire-primary + wind-secondary + supporting chains
- A fire-chain T4 with parallel-chain reach to wind: "Tempest Pyre alters resource model to spend HP instead of mana AND fire chain skills generate wind-channel buffs that amplify wind chain skill damage by 30% for 4 seconds"
- This composes with cross-chain composition synergy pattern (§ 5.3) and enables hybrid fire+wind builds that pure-fire T4s couldn't enable

### 4.4 Spec for which T4 strategies support parallel-chain reach

| Strategy | Parallel-chain reach? | Notes |
|---|---|---|
| Skill-specific TRADE_OFF (Category B) | YES | Tradeoff applies to parallel chain instead of host chain |
| GEOMETRY_COLLAPSE (Category B) | YES | Geometry alteration applies to parallel chain's skills |
| Multiplier strategies (Category B) | YES | Multiplier applies to parallel chain's skills |
| ELEMENT_CONVERSION (Category C) | YES | Converts parallel chain's element instead of host chain's |
| DUAL_ELEMENT_ADDITION (Category C) | YES | Adds secondary element to parallel chain instead of host chain |

ALL Category B/C strategies support parallel-chain reach. Category A is character-wide by definition; parallel-chain reach is not applicable (Category A always affects the whole character).

### 4.5 Algorithm spec for own-chain vs parallel-chain selection

For each T4 candidate, the algorithm:

1. **Generate own-chain candidate:** chain-specific effect targets host chain
2. **Generate parallel-chain candidates:** for each parallel chain in the class, generate a candidate where chain-specific effect targets that parallel chain
3. **Score all candidates via compositional synergy scan** (§ 5): Pass 1 resolve + Pass 2 preserve; net synergy score = resolve − create
4. **Select highest-net-synergy candidate** as the generated T4
5. **Tie-breaker:** if own-chain and parallel-chain candidates score within ±5%, prefer own-chain (preserves chain identity by default; parallel-chain reach is opt-in via synergy score)

---

## 5. Compositional synergy scan two-pass spec

Per doc 40 § 8.4.3 amended + closeout § 2.5 lock + Discipline #32 first-do-no-harm.

### 5.1 Two-pass framework

| Pass | Question | Output |
|---|---|---|
| **Pass 1 (resolve)** | Does candidate T4 resolve existing kit tensions? | Resolve-score: 0-100 |
| **Pass 2 (preserve)** | Does candidate T4 CREATE new tensions not resolved elsewhere? | Create-score: 0-100 |

**Net synergy score = resolve-score − create-score.**

Candidates with net synergy score above threshold are eligible for selection. Candidates below threshold are rejected. Threshold calibrated per gamora SC-7 post-Wave-2-baseline; starting estimate threshold = +10 (modest positive synergy required for selection).

### 5.2 Pass 1 (resolve) — methodology

**Algorithm:** pattern library + statistical priors + algorithmic composition. **NOT LLM raw-reasoning** per D7 AI-tell discipline.

**Pattern library (gandalf-curated):** explicit catalog of kit-tension patterns that T4s can resolve. v1 catalog:

| Kit tension pattern | Example | T4 resolution pattern |
|---|---|---|
| HP-cost-without-regen | Class uses HP-as-resource (e.g., Blood Magic) but lacks life-steal or HP regen | T4 adds life-steal-from-bleed; HP regen on element-cast; etc. |
| Mana-starvation under sustained-cast | Class has low mana pool + sustained-cast skill kit | T4 adds RESOURCE_CONVERSION (mana → cooldown); mana on kill; etc. |
| Element-resistance bottleneck | Class's primary element has resist-cap-vulnerable encounter coverage | T4 adds ELEMENT_CONVERSION; DUAL_ELEMENT_ADDITION for secondary coverage |
| Defensive-uptime gap | Class has high offensive output but defensive-uptime < playability threshold | T4 adds DEFENSIVE_CONVERSION (offense → defense); on-being-hit triggers |
| Build-identity blandness | Class's kit lacks signature mechanic distinguishing it from genre peers | T4 adds GEOMETRY_COLLAPSE; high-multiplier event; identity-defining tradeoff |

**Statistical priors (elrond-curated):** statistical co-occurrence priors from substrate corpus (which mechanic-tag combinations historically compose well in published ARPGs; surfaced via SC-4 + SC-4 expansion research findings).

**Algorithmic composition:** the algorithm composes pattern-library matches with statistical priors to produce a resolve-score. Score components: pattern match strength (0-50) + statistical prior weight (0-30) + kit-tension severity (0-20). Sum capped at 100.

### 5.3 Pass 2 (preserve) — methodology

**Algorithm:** mirror of Pass 1 but inverted — detect downstream tensions the candidate would CREATE.

**Pattern library (gandalf-curated, EXPANDED FROM SC-4 EXPANSION + closeout § 7 candidate #7):** explicit catalog of downstream-tension-creation patterns. v1 catalog:

| Downstream tension pattern | Example | Detection |
|---|---|---|
| Mechanism-needs-fuel-that-doesn't-exist | Life-steal-from-bleed against bleed-immune bosses → mechanism has no fuel | Check kit's bleed-application rate vs encounter bleed-immune rate |
| Binary-survivability | CI (chaos immunity) → any ES depletion is lethal; Ward extreme (50k Ward / 1k HP) → one-shot vulnerability if Ward depletes | Detect feast-or-famine defensive layering (single high-HP layer with no fallback) |
| Self-sabotage interaction | EE (Elemental Equilibrium) with imprecise element sequencing → self-inflicted resist debuff | Detect candidate's mechanic-tags requiring precise sequencing that the kit doesn't enforce |
| Degenerate-end multiplicative-stacking | Archmage 11× mana-to-damage at high investment → forced nerf eliminating investment value | Detect candidate's multiplier scaling vs investment-curve top-end |
| Passive-screen-clear (Pattern 9 — § 7.1) | Stacked numerical advantages eliminate active-engagement requirement | Detect candidate's combined effect with kit producing <1 active skill per 10 sec |
| DoT-stack degenerate (Pattern 10 — § 7.2) | Unbounded DoT compounding produces instant-kill on contact | Detect candidate's DoT contribution × kit DoT-stack-count exceeding 5× expected DPS |
| Resource-overflow trap | Capability that scales resource max past usable threshold | Detect candidate's resource-max scaling vs in-encounter consumption rate |
| Cross-rarity power-collapse | T4 only meaningful at Tier-2 legendary anchor → undermines L1-L45 progression | Detect candidate's mechanism dependent on Tier-1+2 legendary content presence |

**Algorithmic composition:** detection patterns produce a create-score with same scoring structure (pattern match strength + severity + downstream-impact-magnitude).

### 5.4 Five-category synergy taxonomy (UPDATED per SC-4 expansion Topic 2)

Per closeout § 2.5 4-category framework + SC-4 expansion verdict adding 5th Scaling-interaction category.

| # | Synergy category | Description | ARPG evidence (per SC-4 expansion § 2.1) |
|---|---|---|---|
| 1 | **Tension-resolution** | Kit has a mechanic creating a problem the T4 could solve | PoE Blood Magic (mana cost → life cost); D4 Lucky Hit Chance (proc randomness → reliability); GD RR (damage blocked by enemy resist → resist bypass) |
| 2 | **Theme-compound** | Kit has a passive theme the T4 could amplify | PoE support gem chains; LE skill tree node chains (Dive Bomb → Devastating Dive → Rushing Wings); D4 aspect composition; GD devotion + skill-type matching |
| 3 | **Cross-chain composition** | Parallel chains have elements/mechanics that could combine | PoE Elemental Equilibrium (multi-element manipulation); LE idol proc triggering parallel subsystem; D4 Lucky Hit boosting multiple on-hit effects; GD dual-mastery RR feeding other mastery's damage type |
| 4 | **Element-gap fill** | Kit has element coverage gap a T4 could fill | PoE off-element keystones (Iron Reflexes for hybrid); LE idol resistance fixes; D4 tempering recipe targeting; GD augments/components for resist cap |
| 5 | **NEW: Scaling-interaction** (per SC-4 expansion Topic 2 verdict) | Synergies arising purely from stacking same scaling axis | **High-value form (true multiplicative across separate buckets):** PoE Archmage mana scaling (pre-nerf); LE Ward generation rate stacking. **Trap form (additive within same bucket, mistaken for multiplicative):** D4 multiple "increased damage to close enemies" affixes stacked; GD double-conversion items splitting proportionally |

**Scaling-interaction distinction matters for algorithm design** because:
- True scaling-interaction synergies (multiplicative across separate buckets) are high-value AND high-trap-risk (degenerate top-end common — Archmage nerf precedent)
- False scaling-interaction (additive within same bucket) is the source of many trap builds in D4 and GD
- The synergy scan MUST distinguish "does this compound multiply independently?" vs "does this add to the same bucket?" — algorithm validates bucket-identity per candidate before scoring scaling-interaction synergy

### 5.5 Algorithm execution: pass-1-resolve + pass-2-preserve compose

For each T4 candidate (generated per § 4.5):

1. **Pass 1 — resolve:** score against tension-resolution patterns + theme-compound patterns + cross-chain composition patterns + element-gap fill patterns + scaling-interaction patterns. Sum to resolve-score (0-100, cap-bounded).
2. **Pass 2 — preserve:** score against downstream-tension-creation patterns including Pattern 9 + Pattern 10 detection (§ 7) + scaling-interaction trap detection (additive-bucket-stacking detection). Sum to create-score (0-100, cap-bounded).
3. **Net synergy score = resolve-score − create-score.** Range −100 to +100.
4. **Threshold selection:** candidates with net synergy score ≥ +10 (starting estimate; gamora SC-7 iterates) are eligible.
5. **Tie-breaker among eligible:** higher resolve-score wins (preference for genuine synergy resolution over neutral safety).

### 5.6 Dual-consumer pattern (T4 generation + legendary added-skill generation)

Per closeout § 2.5: **compositional synergy scan serves BOTH** T4 generation AND legendary added-skill generation at consumption time. **Same engine; two consumers.**

- **T4 generation consumer:** synergy scan runs at T4 candidate generation time (Wave 2 algorithm); selects highest-net-synergy candidate per chain
- **Legendary added-skill generation consumer:** synergy scan runs at legendary capability-toolkit content selection time (Wave 4 spec-driven gear gen); selects added-skill content that resolves kit tensions per current build state

Implementation: shared synergy-scan engine module; two callers; one engine. Avoids algorithm duplication; ensures consistent first-do-no-harm discipline application across both surfaces.

### 5.7 Discipline #32 first-do-no-harm enforcement

The two-pass framework IS the implementation of #32. Pattern 9 and Pattern 10 detection (§ 7) are specific applications of the Pass 2 preserve check.

**Founding instance per closeout § 7 candidate #7:** the two-pass synergy scan itself is the founding instance of Discipline #32 — T4 synergy detection MUST include downstream-tension-creation check (Pass 2 preserve), not just upstream-tension-resolution (Pass 1 resolve). Founded 2026-05-27 per closeout substantive content.

---

## 6. T4-failure-handling Option F hybrid retry mechanism spec

Per closeout § 1.7 + doc 40 § 8.2 amended.

### 6.1 Four-phase mechanism

| Phase | Action | Compose with |
|---|---|---|
| **Phase 1 — Regeneration** | Algorithm regenerates failing T4 with alternate strategies from registry (3 attempts; configurable per D62 compute budget) | D62 compute budget; D67 independent gauntlet sim validation |
| **Phase 2 — Partial-T4 ship** | If all regeneration attempts fail, ship character with partial T4 (in-band subset; chain keeps T1-T3 nodes but no functional capstone) | D1 balance-as-property (failures are honest, not hidden) |
| **Phase 3 — Minimum threshold** | ≥1 T4 in-band for character to ship at all | If fewer than 1 T4 in-band, fail character generation entirely (do not ship) |
| **Phase 4 — Quality metric tracking** | Track regeneration rate as quality metric (per-class, per-cohort, per-cycle) | D25 cross-season learning (high regeneration rate signals algorithm/pattern-library improvement target) |

### 6.2 Phase 1 retry detail

When a T4 candidate fails (per #26 playability gate, per § 5 synergy threshold, per § 7 Pattern 9/10 detection, per #31 separability check), the algorithm retries:

1. **Retry 1:** select alternative Category B/C strategy (e.g., if first attempt was ELEMENT_CONVERSION and failed, retry with DUAL_ELEMENT_ADDITION; if Multiplier strategies failed, retry with GEOMETRY_COLLAPSE)
2. **Retry 2:** select alternative Category A strategy (e.g., switch from RESOURCE_CONVERSION to DEFENSIVE_CONVERSION as character-wide effect base)
3. **Retry 3:** flip parallel-chain reach selection (if own-chain failed, retry parallel-chain; if parallel-chain failed, retry own-chain)

After 3 attempts: Phase 2 (partial-T4 ship). Retry count configurable per D62 compute budget — Cycle 14+ may increase to 5 or decrease to 2 per gamora SC-7 calibration.

### 6.3 Phase 2 partial-T4 specification

A partial T4 means:
- The chain retains its T1-T3 nodes (functional progression intact at lower investment levels)
- The chain has NO functional T4 capstone (no character-wide effect; no chain-specific effect)
- Player sees this as a chain that doesn't have a T4 unlock available (spirit-guide messaging: "Wind chain T4 generation was unable to produce a kit-coherent capstone for your current build; consider investing in fire or earth chains for T4 acquisition")

**Honest-failure framing:** per D1 balance-as-property, the algorithm does NOT ship a degenerate T4 to avoid the partial-T4 fallback. Shipping degenerate T4s would corrupt the playability gate; partial T4 is the correct fallback.

### 6.4 Phase 3 minimum threshold enforcement

≥1 T4 in-band for character to ship at all.

- 3-chain class (2 T4 capstones expected): minimum 1 in-band; 1 partial-T4 acceptable
- 4-chain class (3 T4 capstones expected): minimum 1 in-band; 2 partial-T4 acceptable

If ALL T4 capstones fail (zero in-band), character generation FAILS entirely. Algorithm logs the failure for D25 cross-season learning; character is not shipped.

### 6.5 Phase 4 quality metric tracking

Regeneration rate metric:

```
T4_regeneration_rate(class, cohort) = sum(retries_used) / sum(T4_candidates_attempted)
```

Per closeout: high regeneration rate (e.g., >50% per class) signals algorithm + pattern-library improvement target. Cycle 14+ uses regeneration-rate telemetry to:
- Add pattern-library entries for repeated failure modes
- Adjust synergy threshold per class
- Identify class-archetype × strategy mismatches

### 6.6 Composition with locked architecture

- **D1 balance-as-property:** failures are honest (partial-T4 ship); not hidden via degenerate-T4 papering-over
- **D67 independent gauntlet sim validation:** gauntlet sim runs against partial-T4 characters AND full-T4 characters; partial-T4 must still meet floor playability criterion (not degenerate; just less powerful)
- **D65 respec mechanism:** if a partial-T4 character acquires a legendary that advocates a different chain's T4, the respec-with-legendary-trigger mechanism applies normally — partial-T4 is not a permanent gate
- **D62 compute budget:** 3-attempt retry cap per D62; per-cycle budget allocation determines whether retry count expands

---

## 7. Pattern 9 + Pattern 10 degenerate-state catalog candidates

Per SC-4 expansion Topic 3 § 3.4 + closeout § 5.2 8-pattern v1 catalog extension candidates.

**Design-intent spec at Wave 2 layer.** Full detection-algorithm operationalization (threshold tuning, sim integration, telemetry instrumentation) DELEGATED to gamora SC-7 post-Wave-3-baseline per Discipline #18.2 (consultation at extension hotspots fires AFTER baseline empirical data, not before). Surfaced HERE in Wave 2 doc 43 so T4 algorithm implementation accounts for these patterns at generation-time via Pass 2 preserve check (§ 5.3).

### 7.1 Pattern 9 — Passive screen-clear / engagement elimination

**Verified by:** PoE2 0.2.0 patch rationale + 0.5.0 nerfs (Herald of Ice + Thunder; Archmage Spark; attribute-stacking; GGG language: "a rather stale meta where many builds used the same Ascendancies, items, and skills"; "passive screen-clearing through stacked numerical advantages rather than active engagement").

**Distinction from Pattern 3 (mandatory-skill-lock):**
- Pattern 3 = one skill dominates rotation (player still actively uses that skill)
- Pattern 9 = player barely needs to act at all (build self-executes against encounter)
- Pattern 3 is a rotation-narrowing problem; Pattern 9 is an engagement-elimination problem

**Proposed definition for v1 catalog extension** (per SC-4 expansion § 3.4): player's active inputs drop below a minimum engagement threshold (e.g., <1 active skill used per 10 seconds of encounter) while encounter proceeds successfully. Distinct from efficiency (good players minimize wasted actions) — passive-screen-clear ELIMINATES the requirement for meaningful input.

**T4 algorithm Pass 2 preserve check (Wave 2 design-intent):**
- For each T4 candidate, check whether candidate's combined effect with current kit would produce a build whose simulated active-input rate falls below threshold
- Detection threshold STARTING ESTIMATE (gamora SC-7 iterates): <1 active skill per 10 sec of sim encounter with the candidate T4 active
- Detection method: lightweight sim against synthetic encounter using candidate T4 + current build kit; count active skill triggers per encounter duration
- Failure routes to T4-failure-handling Phase 1 retry

**Gamora SC-7 calibration target** (post-Wave-3-baseline):
- Empirical baseline of active-input rate per cohort per progression node
- Threshold calibration (1-per-10-sec is starting estimate; empirical baseline may shift)
- Sim integration (lightweight sim cost; #18.2 compute-budget consideration)

### 7.2 Pattern 10 — DoT-stack degenerate / unbounded DoT compounding

**Verified by:** PoE2 0.5.0 Poison Pathfinder nerfs + GD DoT mechanics wiki (DoT stacking from different sources always does full damage per GD game mechanics).

**Distinction from Pattern 6 (degenerate-tank) and Pattern 2 (zero-damage void):**
- Pattern 6 = defensive uptime > 99% (player can't lose)
- Pattern 2 = player damage < 1% expected (player can't deal damage)
- Pattern 10 = DoT becomes de facto one-shot with infinite uptime (offensive analog where DoT mechanic produces burst-equivalent damage on first contact)

**Proposed definition for v1 catalog extension** (per SC-4 expansion § 3.4): damage-over-time sources stack without a per-type cap to the point where effective damage on application exceeds the encounter's HP pool within one tick window — degenerates to "instant kill on contact" despite using a DoT mechanic. Detection: DoT DPS sum at maximum stack count > 5× expected sustained DPS.

**T4 algorithm Pass 2 preserve check (Wave 2 design-intent):**
- For each T4 candidate that adds DoT layer (e.g., DUAL_ELEMENT_ADDITION with DoT-capable secondary element; chain mechanic adding bleed/burn/poison), check whether candidate's DoT contribution × current kit DoT-stack-count exceeds 5× expected sustained DPS
- Detection threshold STARTING ESTIMATE (gamora SC-7 iterates): sum-DoT-DPS at max stack count > 5× expected sustained DPS for cohort + progression node
- Detection method: estimate DoT-stack-count + per-DoT-DPS contribution analytically (no full sim needed for generation-time check); refine via sim per gamora SC-7
- Failure routes to T4-failure-handling Phase 1 retry (likely retry into ELEMENT_CONVERSION or non-DoT Category B strategy)

**Gamora SC-7 calibration target** (post-Wave-3-baseline):
- Empirical baseline of DoT-stack rates per class per cohort
- Threshold calibration (5× starting estimate; empirical baseline may shift)
- Sim vs analytical estimate trade-off (compute budget per #18.2)

### 7.3 Composition with locked architecture

- **#32 first-do-no-harm:** Pattern 9 + Pattern 10 detection are explicit instances of Pass 2 preserve check; T4 candidates failing these patterns at generation-time are rejected (route to T4-failure-handling)
- **#26 playability:** Pattern 9 + Pattern 10 compose with the playability gate; degenerate states by these patterns are NOT playable
- **#18.2 consultation timing:** detection algorithm calibration is gamora SC-7 territory; fires AFTER Wave-3 baseline empirical data
- **D61 + closeout § 5.2 8-pattern v1 catalog:** Pattern 9 + Pattern 10 are catalog EXTENSIONS (candidate status); inclusion in v1 catalog vs v1.1 catalog is gamora SC-7 decision per #18.2

---

## 8. One-T4-unlocked-at-a-time discipline

Per closeout § 1.3 + doc 40 D66 amendment.

### 8.1 Discipline statement

**ONLY ONE T4 capstone unlocked at a given time.**

Sharpens D66 from passive description ("non-attuned T4 chains NOT mechanically active") to ACTIVE IDENTITY DISCIPLINE — the player explicitly chooses which T4 to embody at any given time; other T4 chains have their T1-T3 nodes accessible but no functional capstone.

### 8.2 Composition with locked architecture

- **D65 respec-with-legendary-trigger** is the SWAP mechanism — players acquire a new tier-1+2 legendary that advocates a different T4; spirit guide surfaces a free-respec opportunity; player swaps active T4 via respec
- **D76 dual-effect concentration** is the WHY — each T4 has character-wide AND chain-specific effects; allowing multiple T4 simultaneously would dilute the concentrated identity (and would also produce metagame-degeneration via T4-stacking exploits)
- **D67 independent gauntlet sim** validates per-T4-configuration, not per-T4-combination — sim methodology assumes exactly one T4 active per character at validation time

### 8.3 Algorithm implication

Wave 2 algorithm generates T4 options PER CHAIN. Player selection (at runtime) determines which T4 is currently active. The algorithm does NOT need to generate T4-combination scoring (e.g., scoring "T4-A + T4-B simultaneously"); only single-T4 scoring (T4-A alone; T4-B alone; T4-C alone).

This simplifies the algorithm meaningfully — combinatorial scoring space is N (single-T4) vs N² or N×(N-1) (pair-T4) or 2^N (full-combination). Wave 2 implements N-scoring only.

### 8.4 Spirit-guide projection surface

When the player has multiple in-band T4s available (e.g., a 3-chain class with both T4 chains at unlock threshold), the spirit guide surfaces per-T4 projections per closeout § 3.4:

> "Currently playing T4-A: projected KPM 75, defensive uptime 62%. Switching to T4-B: projected KPM 62, defensive uptime 78%. T4-A composes 23% better with this gear; T4-B composes better with cold-resistance encounters."

The data-oracle framing (per D28 + spirit-guide-as-data-oracle § 5 doc 40) gives the player concrete decision substrate without dictating choice.

---

## 9. Variable 3-or-4 class chain architecture

Per closeout § 1.4 + doc 40 § 8.3 amended.

### 9.1 Architecture

**Variable 3-or-4 chains per class.** NOT uniform. Depth-vs-breadth lever for class differentiation.

| Class chain count | T4 count (per D83) | Architecture |
|---|---|---|
| **3 chains** | 2 T4 capstones | 2 T4 chains × ~5 nodes (branching-eligible at depth ≥4 per closeout § 1.2) + 1 supporting chain × ~3 nodes |
| **4 chains** | 3 T4 capstones | 3 T4 chains × ~3-4 nodes (linear) + 1 supporting chain × ~3 nodes |

### 9.2 Supporting chain absorbs class-intrinsic baseline passives

Per closeout § 2.1 Option C. The T3-only supporting chain serves as the "class-intrinsic passives" location:
- Carries the 55-entry minimum-viable trait pool integration (per doc 42 § 8 + W1.6)
- Represents class identity (not build specialization)
- Linear (no branching; shallow by construction)
- No T4 capstone

### 9.3 First-pass class roster DEFERRED

Per Block A2b deferred-commitment per closeout § 1.4. Specific per-class assignment (which classes are 3-chain vs 4-chain) is DEFERRED — substrate-evidence follow-on (Wave 1 BC-target review surfaces substrate vote).

**Empirical-evidence criterion for re-engagement:** Wave 1 BC-target review (per `v1-bc-target-intent-2026-05-24.md` substrate substrate-led design discipline) surfaces evidence informing per-class chain-count choice. Once substrate vote is in, gandalf authors class-roster canonical (or amendment to existing doc) assigning specific classes to 3-chain vs 4-chain.

### 9.4 Wave 2 algorithm implications

The Wave 2 T4 algorithm must support both 3-chain and 4-chain configurations:
- Algorithm receives `class_chain_count: Literal[3, 4]` parameter
- Generates `T4_count = chain_count - 1` per D83 (2 or 3 T4 capstones)
- Parallel-chain reach target space varies per chain count (per § 4.2)
- T4-failure-handling Phase 3 minimum threshold (≥1 T4 in-band) applies regardless of chain count

### 9.5 Branching refinement (per closeout § 1.2 + doc 40 § 8.3.1)

Branching gated by chain depth ≥4 nodes:
- Chains ≥4 nodes eligible for 1 branch point: 1 → 2 → {3a OR 3b} → 4 → T4-capstone
- Chains ≤3 nodes linear only
- Supporting chains stay linear (shallow by construction)

Wave 2 T4 algorithm operates on the capstone; branching is structural skill-tree concern, not T4-generation concern. T4 algorithm receives the chain's terminal node + the chain's resolved-content surface as input.

---

## 10. Sub-wave structure W2.0-W2.9 for rocket Wave 2 implementation

Mirrors doc 42 § 9.6 W1.0-W1.8 implementation-atomic pattern. 10 sub-waves; each ends in a gate.

| Sub-wave | Work-unit | Owner | Gate |
|---|---|---|---|
| **W2.0 — Substrate prep + repo-scaffold** | Review existing T4 algorithm code path; identify entry points; spot-check current 6-strategy registry implementation; identify integration points with Wave 1 partition output (T4-attunement annotation surface; capability-toolkit surface) | rocket | Substrate prep audit committed; ready for W2.1 |
| **W2.1 — 3-category T4 taxonomy schema** | Schema for Category A/B/C type field + strategy mapping + composition-rule enforcement (exactly one of B or C per T4; always Category A); math note per Discipline #1 BEFORE schema implementation | rocket | jack-ryan Gate-1 critique on schema; math note PASS per #1 |
| **W2.2 — DUAL_ELEMENT_ADDITION strategy implementation** | Category C extension per § 3 spec; class element compatibility check vs `class_schema.py:46-47` `secondary_elements`; secondary-element selection; magnitude band starting estimates per § 3.4 | rocket | jack-ryan Gate-1 critique; test coverage on DUAL_ELEMENT_ADDITION generation paths |
| **W2.3 — Parallel-chain reach implementation** | Chain-specific effect routing per § 4: own-chain vs parallel-chain target; algorithm-fixed at generation time; routing applies to all Category B/C strategies per § 4.4; tie-breaker per § 4.5 step 5 | rocket | jack-ryan Gate-1 critique; test coverage on own-chain vs parallel-chain routing |
| **W2.4 — Compositional synergy scan implementation** | Two-pass framework per § 5; Pass 1 resolve + Pass 2 preserve; pattern library implementation (gandalf-curated v1 catalogs from § 5.2 + § 5.3); statistical priors (elrond-cooperated where substrate corpus surfaces priors); algorithmic composition; 5-category synergy taxonomy including NEW Scaling-interaction; NOT LLM raw-reasoning per D7; dual-consumer pattern (T4 generation + legendary added-skill generation; same engine; two callers) | rocket | jack-ryan Gate-1 critique; test coverage on pass-1 + pass-2 scoring; cross-validation with starter pattern-library entries |
| **W2.5 — T4-failure-handling Option F hybrid retry mechanism implementation** | 4-phase mechanism per § 6: Phase 1 regeneration (3-attempt; configurable); Phase 2 partial-T4 ship (chain T1-T3 intact; no capstone); Phase 3 minimum threshold (≥1 T4 in-band); Phase 4 quality metric tracking (regeneration rate per class/cohort/cycle) | rocket | jack-ryan Gate-1 critique; test coverage on retry sequencing + partial-T4 fallback + minimum threshold + quality metric emission |
| **W2.6 — Pattern 9 + Pattern 10 generation-time detection** | Design-intent per § 7; Pattern 9 (passive screen-clear) detection at <1 active skill per 10 sec threshold STARTING ESTIMATE; Pattern 10 (DoT-stack degenerate) detection at >5× expected DPS threshold STARTING ESTIMATE; both detections compose with #32 Pass 2 preserve check; detection-algorithm calibration DELEGATED to gamora SC-7 post-Wave-3-baseline per #18.2 (so Wave 2 ships with starting estimates; iteration is post-baseline) | rocket | jack-ryan Gate-1 critique; test coverage on Pattern 9 + Pattern 10 detection paths against synthetic positive + negative cases |
| **W2.7 — One-T4-unlocked-at-a-time gating + variable 3-or-4 chain architecture per class** | One-T4-at-a-time per § 8 (algorithm generates per-chain candidates; runtime enforces single-active); variable 3-or-4 chain per § 9 (algorithm receives `class_chain_count` parameter; generates `T4_count = chain_count - 1`); per-class roster NOT specified at this layer (deferred per § 9.3) | rocket | jack-ryan Gate-1 critique; test coverage on 3-chain vs 4-chain generation paths |
| **W2.8 — Cross-cohesion validation per #26 + Block C scaffolding** | Composes with Wave 1 partition cross-cohesion pattern; gamora spot-check sim runs against generated T4s across 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C scaffolding); validation criterion: T4s produce playable kits per playability sub-gates; no cohort structurally locked out of T4 acquisition; partial-T4 rate within acceptable bounds (starting estimate <20% per cohort; gamora SC-7 iterates) | gamora + jack-ryan | jack-ryan Gate-2 PASS on cross-cohesion validation against 4 cohorts |
| **W2.9 — Round-trip smoke per Principle 6 (CRITICAL: legendary_t0_5 inclusion per Wave 1 Gate-2 I1)** | Full round-trip smoke covering all 10 rarity tiers including `legendary_t0_5` (Wave 1 carryover gap closure); T4 generation per chain × per class × per rarity; partition output consumption verified; T4-attunement annotation matching verified; capability-toolkit composition verified; post-script empirical count assertions per Discipline #11 (CRITICAL: full WARN-pattern closure target per Wave 1 Gate-2 partial-remediation status — Wave 2 Gate-2 = 0 empirical assertion failures) | rocket + jack-ryan | jack-ryan Gate-2 PASS on round-trip smoke + full WARN-pattern closure |

Sub-wave sequencing is implementation-atomic; rocket + knight-rider may adjust dependencies per Wave 2 implementation dispatch.

---

## 11. Wave 2 implementation guidance for rocket

Concrete next-steps for rocket Wave 2 implementation against this design intent.

### 11.1 Wave 1 partition substrate consumption

Wave 2 T4 algorithm CONSUMES Wave 1 partition output as substrate. Specific consumption points:

| Wave 1 surface | Wave 2 consumption |
|---|---|
| **T4-attunement annotation metadata** (per doc 42 § 5.8; Tier-1+2 legendary + sets) | T4 algorithm reads annotation field; uses as scoring input for synergy scan (annotation indicates kit-intended T4 alignment; high-synergy candidates favor matching annotation) |
| **Capability toolkit surface** (per doc 42 § 4.2 + § 5.7; legendary-exclusive) | T4 algorithm Category B/C effects compose with capability-toolkit added-skill content; synergy scan dual-consumer pattern (per § 5.6) runs at BOTH T4 generation AND legendary content selection |
| **9-category × 11-slot affinity matrix** (per doc 42 § 2.1) | T4 algorithm Pass 2 preserve check uses affinity matrix to detect kit-tension patterns (e.g., low Resource affinity in current build + T4 adding resource-cost mechanic → tension creation) |
| **Per-rarity grid** (per doc 42 § 3) | T4 algorithm scoring considers gear instance tier distribution (Tier-1+2 legendary T4-attunement carries more weight than Tier-0 legendary annotation) |
| **Sample modifier enumerations** (per doc 42 § 5) | T4 algorithm pattern library entries reference specific modifier types for synergy scoring |

### 11.2 Math-before-code (Discipline #1) requirement

Per Discipline #1: math note BEFORE schema implementation. Wave 2 math note location: `~/Games/reincarnated-engine/src/reincarnated/generation/math/cycle-13-wave-2-t4-algorithm-math-2026-05-2X.md` (rocket-authored at W2.1).

**Math note must cover:**
- 3-category taxonomy composition rule (exactly one of B or C per T4; always Category A)
- DUAL_ELEMENT_ADDITION magnitude band math (per § 3.4 starting estimates)
- Parallel-chain reach scoring formula (per § 4.5)
- Compositional synergy scan scoring (per § 5; resolve-score + create-score + net-synergy formula; threshold + tie-breaker)
- T4-failure-handling retry-count math (per § 6; 3-attempt cap; configurable)
- Pattern 9 + Pattern 10 detection thresholds (per § 7; starting estimates)
- Cross-cohesion validation kit-count-per-archetype (reference Block C scaffolding per Wave 1 Gate-1 I2 routing)

### 11.3 Discipline #11 empirical inspection (CRITICAL — full WARN-pattern closure target)

Per Wave 1 Gate-2 partial-remediation status: Wave 2 Gate-2 = full WARN-pattern closure target. **CRITICAL: every post-script empirical count assertion in completion record MUST verify against actual code state via `len()` or equivalent at write-time.**

**Asserted counts to verify empirically at Wave 2 completion-record authoring time:**
- Strategy registry count (7 strategies = 6 original + DUAL_ELEMENT_ADDITION)
- Category counts (3 categories; A + B + C)
- Synergy taxonomy categories (5: tension-resolution + theme-compound + cross-chain composition + element-gap fill + scaling-interaction)
- Pattern library entry counts (v1 catalogs § 5.2 + § 5.3)
- Pattern 9 + Pattern 10 detection paths (2 detection patterns)
- Sub-wave count (10 sub-waves W2.0-W2.9)
- Round-trip smoke rarity coverage (10 rarities including legendary_t0_5 per Wave 1 Gate-2 I1)
- T4-failure-handling phase count (4 phases)

Each assertion MUST be drawn from `len()` against the module-level constant at write-time. No pre-addition draft counts.

### 11.4 Cross-seam contract change (Principle 6 gate)

Wave 2 T4 algorithm implementation WILL introduce cross-seam contracts via T4 algorithm output surface:
- T4 generation output schema (Category A/B/C + strategy mapping + parallel-chain target + magnitude bands)
- T4 metadata for spirit-guide projection consumption (per § 8.4 data-oracle messaging)
- T4 telemetry for D25 cross-season learning (regeneration rate; partial-T4 rate; synergy score distribution per class/cohort)

Round-trip smoke per Principle 6 fires at W2.9 covering all 10 rarity tiers + cross-seam consumer paths (spirit-guide consumption + telemetry consumption). MIGRATION.md filing per ADR-004 required.

### 11.5 LLM raw-reasoning constraint (D7 AI-tell line)

Per § 5.2 + § 5.3 + closeout § 2.5: synergy scan is pattern library (gandalf-curated) + statistical co-occurrence priors (elrond-curated) + algorithmic composition. **NOT LLM raw-reasoning.**

Implementation MUST NOT route synergy scoring through an LLM call. Pattern matching is structural (mechanic-tag intersection; resistance-axis intersection; resource-model intersection). Statistical priors are tabular lookups. Algorithmic composition is arithmetic.

LLM may be used for player-facing T4 NAMING (post-generation; takes algorithm output as template input; names per closeout LLM-templated structure pattern) but NOT for synergy SCORING. The line between naming (LLM-allowed) and scoring (LLM-prohibited) preserves D7 AI-tell discipline.

### 11.6 Magnitude band starting estimates + gamora SC-7 iteration (#18.2)

Per § 3.4 + § 7 + Wave 1 § 9.4 precedent: Wave 2 ships with starting-estimate magnitude bands AND starting-estimate Pattern 9 + Pattern 10 detection thresholds. Gamora SC-7 methodology consultation fires post-Wave-3-baseline per Discipline #18.2 (consultation at extension hotspots fires AFTER baseline empirical data, not before).

Wave 2 implementation MUST emit telemetry sufficient to support gamora SC-7 calibration:
- Per-class T4 regeneration rate
- Per-cohort T4 in-band rate
- Per-T4-strategy distribution of generated T4s
- Per-T4-candidate scoring breakdown (resolve-score + create-score + net-synergy + selected vs rejected reason)
- Pattern 9 + Pattern 10 detection trigger counts (per class; per cohort)
- Active-input rate distribution (for Pattern 9 calibration)
- DoT-stack distribution (for Pattern 10 calibration)

### 11.7 Disciplines #27 / #31 / #32 invocation (Wave 1 Gate-1 I2 routing)

Per Wave 1 Gate-1 I2 routing requirement: Disciplines #27 + #31 + #32 MUST be invoked + composed throughout Wave 2.

- **#27 dual-effect capstone:** Wave 2 IS the implementation of #27. Every T4 has Category A (character-wide) + Category B/C (chain-specific) per § 2.1 composition rule.
- **#31 dual-effect separability:** Pass 2 preserve check (§ 5.3) includes separability test per § 2.4. Category A and Category B/C effects must be INDEPENDENTLY COHERENT. Founding instance: corrected Blood Magic example.
- **#32 first-do-no-harm:** the two-pass synergy scan IS the implementation of #32 per § 5.7. Pattern 9 + Pattern 10 detection are specific applications of Pass 2 preserve check. Founding instance: two-pass synergy scan 2026-05-27.

Each Wave 2 sub-wave dispatch (W2.0-W2.9) must cite the relevant disciplines explicitly.

### 11.8 Cross-cohesion validation (W2.8) execution per Block C

Per Wave 1 Gate-1 I2 routing + Block C scaffolding companion doc:
- 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid; scaling-independent per Block C scaffolding 2)
- Kit count per archetype: reference Block C scaffolding for specification (mirrors Wave 1 Gate-1 I2 routing for Wave 1)
- BC-axis coverage: 22 BC-target cells per `v1-bc-target-intent-2026-05-24.md` Sketch G
- Validation criterion per W2.8 gate: T4s produce playable kits per playability sub-gates; no cohort structurally locked out of T4 acquisition; partial-T4 rate within bounds

---

## 12. Wave 2 close criterion

Wave 2 closes when:

- [ ] W2.0-W2.9 all complete per completion record table
- [ ] 3-category T4 taxonomy schema operational; composition rule enforced (exactly one of B or C; always Category A)
- [ ] DUAL_ELEMENT_ADDITION strategy implemented; class element compatibility check operational; secondary-element selection operational; magnitude bands at starting estimates
- [ ] Parallel-chain reach implemented; routing per § 4.4; tie-breaker per § 4.5
- [ ] Compositional synergy scan implemented; Pass 1 + Pass 2 + net synergy + threshold + tie-breaker; 5-category synergy taxonomy including NEW Scaling-interaction; pattern library v1 catalogs (§ 5.2 + § 5.3) populated; NOT LLM raw-reasoning; dual-consumer pattern (T4 generation + legendary added-skill generation)
- [ ] T4-failure-handling Option F 4-phase mechanism implemented; retry sequencing per § 6.2; partial-T4 fallback per § 6.3; minimum threshold per § 6.4; quality metric emission per § 6.5
- [ ] Pattern 9 + Pattern 10 generation-time detection implemented at design-intent depth; starting-estimate thresholds; composes with #32 Pass 2 preserve check; detection-algorithm calibration DELEGATED to gamora SC-7 post-Wave-3-baseline
- [ ] One-T4-unlocked-at-a-time gating operational; variable 3-or-4 chain architecture supported; per-class roster NOT required at this layer
- [ ] Cross-cohesion validation per #26 + Block C scaffolding (4 cohort archetypes; gamora spot-check sim); jack-ryan Gate-2 PASS on cross-cohesion
- [ ] Round-trip smoke per Principle 6 covering all 10 rarity tiers INCLUDING `legendary_t0_5` (Wave 1 carryover gap closure); jack-ryan Gate-2 PASS
- [ ] Full WARN-pattern remediation per Discipline #11 (Wave 2 Gate-2 = 0 empirical assertion failures; CRITICAL — partial-remediation closure target from Wave 1 Gate-2)
- [ ] Disciplines #27 + #31 + #32 explicitly composed throughout Wave 2 dispatches (per Wave 1 Gate-1 I2 routing)
- [ ] MIGRATION.md filed per ADR-004 (cross-seam contract change introduced)
- [ ] Math note authored per Discipline #1 BEFORE schema implementation (per § 11.2)
- [ ] jack-ryan Gate-2 PASS on aggregate Wave 2 close
- [ ] Wave 2 close unlocks Wave 3 (T4 algorithm Phase 3: character-wide vs chain-wide scope dimension)

**Wave 2 ready to feed Wave 3 T4 algorithm Phase 3 implementation when:** rocket's Wave 2 T4 algorithm produces generated T4 candidates per chain per class whose composition rocket's Wave 3 implementation can consume as input for the character-wide vs chain-wide scope dimension (Phase 3). Specifically, the generated T4 candidates must include Category A/B/C metadata + parallel-chain target metadata + synergy-score metadata + magnitude-band metadata that Wave 3 Phase 3 consumes for scope-dimension scoring.

---

## 13. Composition with locked architecture

| Locked architectural element | How this doc composes |
|---|---|
| **Doc 38 D1-D10 delivery strategy** | Variant C engine-as-product: T4 algorithm is per-product config (Reincarnated v1 ships with 3-category + 7-strategy + DUAL_ELEMENT_ADDITION; future commercial profiles may config differently) |
| **Doc 39 Architecture B substrate-bound at Phase 2** | Phase 2 spec-driven content gen consumes T4 algorithm output; T4-attuned content downstream |
| **Doc 40 § 8 multi-T4 architecture (post-amendments)** | This doc operationalizes doc 40 § 8.4 (3-category taxonomy) + § 8.4.1 (DUAL_ELEMENT_ADDITION) + § 8.4.2 (parallel-chain reach) + § 8.4.3 (compositional synergy scan) + § 8.2 (T4-failure-handling Option F) for Wave 2 implementation |
| **Doc 41 L50 hybrid progression framework** | T4 unlock economics (D71 amended: 70-point endgame budget; T4-unlock at 70% chain max) compose with L50 framework; T4 acquisition pacing follows level bands |
| **Doc 42 Wave 1 partition intent** | Wave 2 T4 algorithm CONSUMES Wave 1 partition output (T4-attunement annotation metadata; capability toolkit surface; 9-cat × 11-slot affinity matrix; per-rarity grid; sample modifier enumerations) per § 11.1 |
| **8 BC axes (qd-engine-bc-axes-lock-2026-05-20.md)** | Cross-cohesion validation (W2.8) operates on BC-axis cells; cohort spot-check sim runs per-cell per cohort per § 11.8 |
| **8 resource models (closeout § 2.2)** | Category A RESOURCE_CONVERSION strategy operates within 8-model catalog; class resource model determines RESOURCE_CONVERSION target options |
| **Block C calibration scaffolding** | Cross-cohesion validation (W2.8) references Block C 4-cohort scaffolding; kit-count-per-archetype specified per Block C |
| **Discipline #1 math-before-code** | Math note BEFORE schema implementation per § 11.2 + W2.1 gate |
| **Discipline #1.2 code-citation** | Wave 2 implementation references existing code per #1.2; class element compatibility check cites `class_schema.py:46-47` |
| **Discipline #11 empirical inspection** | Wave 2 post-script assertions MUST verify against `len()` at write-time per § 11.3 (CRITICAL — full WARN-pattern closure target) |
| **Discipline #18 methodology-before-execution** | Wave 2 T4 algorithm is math hotspot; gamora SC-7 methodology consultation per #18 (full consultation post-Wave-3-baseline per #18.2) |
| **Discipline #18.2 consultation timing** | Detection algorithm calibration (Pattern 9 + Pattern 10) + magnitude band recalibration (DUAL_ELEMENT_ADDITION) DELEGATED to gamora SC-7 post-Wave-3-baseline; Wave 2 ships with starting estimates |
| **Discipline #26 playability** | Wave 2 T4 algorithm MUST produce playable kits per 6 sub-gates; cross-cohesion validation per W2.8 |
| **Discipline #27 dual-effect capstone** | Wave 2 IS the implementation of #27 (per Wave 1 Gate-1 I2 routing) |
| **Discipline #29 commitment-to-consequence** | T4-failure-handling Option F lands with consequence (partial-T4 ship; not free reversibility) per § 6.3 |
| **Discipline #30 sim methodology naming** | Composes with gamora SC-7 post-Wave-3-baseline naming per #18.2 |
| **Discipline #31 dual-effect separability** | Category A + Category B/C effects MUST be INDEPENDENTLY COHERENT per § 2.4 (per Wave 1 Gate-1 I2 routing) |
| **Discipline #32 first-do-no-harm** | Compositional synergy scan Pass 2 preserve check IS the implementation of #32 per § 5.7 (per Wave 1 Gate-1 I2 routing) |
| **SC-4 expansion 5th Scaling-interaction category** | Included in 5-category synergy taxonomy per § 5.4 (per Wave 1 Gate-1 W3 routing) |
| **SC-4 expansion Pattern 9 + Pattern 10** | Surfaced as design-intent per § 7 (per Wave 1 Gate-1 W3 routing); detection-algorithm calibration delegated to gamora SC-7 |

---

## 14. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Wave 2 T4 algorithm design intent canonical for Cycle 13 multi-T4 architecture cycle
**Composition:** with doc 38 + doc 39 + doc 40 (post-2026-05-27 amendments § 8 + § 8.4.x) + doc 41 + doc 42 (Wave 1 partition substrate) + closeout doc 2026-05-27 (§ 1.3 + § 1.4 + § 1.7 + § 2.4 + § 2.5 + § 7) + SC-4 expansion research (Topic 2 5th Scaling-interaction synergy + Topic 3 Pattern 9 + Pattern 10) + 8-axis BC lock + 8-model resource catalog + Block C calibration scaffolding + Disciplines #1 + #1.2 + #11 + #18 + #18.2 + #26 + #27 + #29 + #30 + #31 + #32
**Authority:** Matt 2026-05-27 verbatim — autonomous Wave 0 → Wave 1 → Wave 2 sequencing per ratified framing brief § 4.1 + jack-ryan Wave 1 + SC-6 Gate-2 PASS verdicts (commits `2aa6813` + `ee15c96`) unblock Wave 2
**Next gates:**
- jack-ryan Wave 2 Gate-1 critique on this doc (post-authoring; separate dispatch fires)
- Rocket Wave 2 implementation per § 10 sub-wave structure + § 11 guidance (post-Gate-1 close; separate dispatch fires)
- Gamora SC-7 methodology consultation post-Wave-3-baseline per Discipline #18.2 (separate dispatch; Wave 2 magnitude band + Pattern 9 + Pattern 10 detection calibration are SC-7 territory)

**For:** the Wave 2 T4 algorithm design intent canonical for Cycle 13 multi-T4 architecture cycle. 3-category T4 taxonomy operationalized (Category A class-mechanical character-wide + Category B chain-multiplicative chain-specific + Category C chain-element-conversion-or-addition chain-specific; composition rule = always A + exactly one of B or C). DUAL_ELEMENT_ADDITION strategy spec NEW (Category C extension; PoE/D4 genre precedent; magnitude bands anchored with starting estimates; gamora SC-7 iterates). Parallel-chain reach spec (own-chain vs parallel-chain target; algorithm-fixed at generation; tie-breaker = own-chain default). Compositional synergy scan two-pass framework (Pass 1 resolve + Pass 2 preserve; net synergy score; 5-category synergy taxonomy including NEW Scaling-interaction per SC-4 expansion). T4-failure-handling Option F hybrid retry mechanism (4-phase: regeneration + partial-T4 ship + minimum threshold + quality metric tracking). Pattern 9 (passive screen-clear) + Pattern 10 (DoT-stack degenerate) generation-time detection design-intent (starting estimates; gamora SC-7 calibrates). One-T4-unlocked-at-a-time discipline (D66 sharpened; active identity). Variable 3-or-4 class chain architecture (per-class roster deferred). Sub-wave structure W2.0-W2.9 implementation-atomic for rocket. Wave 2 implementation guidance for rocket (Wave 1 partition substrate consumption + math-before-code + Discipline #11 full WARN-pattern closure target + cross-seam contract per Principle 6 + LLM raw-reasoning constraint + magnitude band starting estimates with gamora SC-7 iteration + Disciplines #27/#31/#32 explicit composition + cross-cohesion validation per Block C). Wave 2 close criterion = jack-ryan Gate-2 PASS on rocket Wave 2 implementation against this intent + full WARN-pattern remediation per Wave 1 Gate-2 partial-remediation status. Wave 2 ready to feed Wave 3 T4 algorithm Phase 3 implementation upon close. Authoritative source for CURRENT-status truth remains `canonical/00-ground-state.md`.

**Signed:** gandalf (story-and-design steward)
