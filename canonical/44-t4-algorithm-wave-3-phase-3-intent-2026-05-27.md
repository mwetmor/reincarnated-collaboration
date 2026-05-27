# 44 — T4 Algorithm Wave 3 Phase 3 Intent — Character-Wide vs Chain-Wide Scope Dimension (Cycle 13 — 2026-05-27)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — Wave 3 T4 algorithm Phase 3 design INTENT canonical for Cycle 13 multi-T4 architecture cycle; see `canonical/00-ground-state.md`

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — Wave 3 T4 algorithm Phase 3 design intent; character-wide vs chain-wide scope dimension operationalized + per-category scope-dimension applicability + scope-dimension selection algorithm + biggest-design-risk handling per doc 40 D81 Phase 3 framing + composition with Wave 2 outputs (3-category taxonomy + 7-strategy registry + parallel-chain reach + compositional synergy scan + Option F + Pattern 9+10 stubs) + sub-wave structure W3.0-W3.5 + Wave 3 implementation guidance for rocket
**Authority:** Matt 2026-05-27 verbatim — "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope. No further Matt-creative-ratification gates on Cycle 13 progression." + jack-ryan Wave 2 Gate-2 PASS verdict (commit `0783860`) UNBLOCKS Wave 3 + Wave 2 CLOSED + WARN-pattern REMEDIATED milestone full closure
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — engine workflow Phase 2d spec-driven gear gen
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation (D1-D86 + 2026-05-27 amendments; § 8.2 Phase 3 "biggest design risk" framing is Wave 3 substrate; § 8.4 3-category taxonomy + § 8.4.2 parallel-chain reach are scope-dimension foundation)
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid + cell × node × cohort context (cohort archetype substrate for scope-dimension preference)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — Wave 1 partition substrate (T4-attunement annotation feeds scope-dimension scoring)
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` — Wave 2 precedent (3-category taxonomy + DUAL_ELEMENT_ADDITION + parallel-chain reach + compositional synergy scan + Option F + Pattern 9+10 stubs); Wave 3 builds on top
- `canonical/02-roadmap.md` — engine build visual-flow progress tracker
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — Matt + gandalf Pattern-B session closeout § 1.3 (one-T4-at-a-time scope-consequence) + § 1.4 (variable 3-or-4 chain architecture) + § 2.4 (T4 algorithm 3-category taxonomy substrate)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` — Wave 2 Gate-2 PASS + WARN-pattern full closure milestone (Wave 3 implementation expectation: maintain 100% accurate post-script empirical count assertions)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC operational truth (cross-cohesion validation coordinate system; scope-dimension cross-cohesion validation extends Wave 2 pattern)

---

## 0. TL;DR

Wave 3 T4 algorithm Phase 3 design intent for Cycle 13 multi-T4 architecture cycle. Operationalizes the **character-wide vs chain-wide scope dimension** — the **variance generator** per doc 40 § 8.2 (Phase 3 = "biggest design risk"). Phase 3 introduces a SCOPE dimension orthogonal to the 3-category taxonomy locked in Wave 2: each T4 capstone's effect surface has a scope question (character-wide = applies to ALL chains in kit; chain-wide = applies to a single chain — own-chain per Wave 2 default, or parallel-chain per Wave 2 W2.3 reach). For Category A (class mechanical/energy alteration) scope is INHERENTLY character-wide and fixed at the category level. For Categories B (chain multiplicative) + C (chain element conversion/addition) scope is chain-wide by default but the **parallel-chain reach sub-dimension** locked Wave 2 means chain-wide-OWN vs chain-wide-PARALLEL is itself a within-chain-wide variance lever. Phase 3 ADDS character-wide variants of selected Category B/C strategies (e.g., character-wide multiplier-on-all-chains; character-wide element-addition-to-all-chain-skills) as opt-in variance generators where genre precedent + synergy scan support them; this is the **biggest design risk** because it expands the combinatorial space of T4 effects to (3 categories × 7 strategies × {own-chain, parallel-chain, character-wide-where-eligible}) with **one-T4-active gating per closeout § 1.3 + D66 sharpening** amplifying per-T4-decision consequence. Specs the **scope-dimension selection algorithm** as a per-category branching tree with cohort-archetype-driven preference (DPS-min-maxer → character-wide-favoring; Defensive → chain-wide-favoring; Balanced + Hybrid → synergy-scan-decides) anchored by Discipline #32 first-do-no-harm Pass 2 preserve check (character-wide promotion of a Category B/C strategy must NOT trigger Pattern 9 passive-screen-clear OR Pattern 10 DoT-stack degenerate at expanded scope). Specs the **biggest-design-risk handling** as a 4-strategy mitigation bundle: (1) per-archetype scope-dimension defaults (bound space architecturally before scoring); (2) cohort-archetype-driven scope preference (shape distribution per cohort intent); (3) one-T4-active gating composes with scope-dimension to keep per-build complexity bounded (only one scope-dimension instance active per character at any time); (4) gamora SC-7 post-Wave-3-baseline calibration of scope-promotion thresholds per Discipline #18.2 (consultation at extension hotspots fires AFTER baseline empirical data, not before). Composes with Wave 2 outputs through extension of `T4CandidateV2` schema (add `scope_dimension` field; preserves V2-as-stable surface; no V3 schema bifurcation needed; mirrors W2.3 `parallel_chain_mode` field-addition pattern). Provides **sub-wave structure W3.0-W3.5** (6 sub-waves; smaller than Wave 2 W2.0-W2.9 to match smaller scope) for rocket Wave 3 implementation. Provides **Wave 3 implementation guidance for rocket** including substrate consumption from Wave 2 (T4CandidateV2 + 3-category taxonomy + parallel-chain reach + synergy scan + Option F + Pattern 9+10 stubs all extend naturally) + maintain WARN-pattern REMEDIATED status (100% accurate post-script empirical count assertions). Wave 3 close criterion = jack-ryan Gate-2 PASS on rocket Wave 3 implementation against this intent; ready to feed Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling + gamora SC-7 methodology consultation FULL per Discipline #18.2. Disciplines #1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32 compose throughout.

---

## 1. Architectural foundation cross-references

This doc operationalizes the Wave 3 T4 algorithm Phase 3 design intent grounded in the locked architectural foundation + Wave 2 baseline.

| Foundation doc | What it provides | Where this doc operationalizes |
|---|---|---|
| **Doc 38** (D1-D10 delivery strategy) | Variant C engine-vs-game; isekai provisional; ~30-day seasonal | Composes with § 10 |
| **Doc 39** (QD-engine workflow Architecture B) | Phase 2 spec-driven content gen substrate-bound | Wave 3 T4 algorithm extends Phase 2 generation pipeline; scope-dimension feeds Phase 2d spec-driven gear gen Wave 4 attunement |
| **Doc 40** (Cycle 13 architectural foundation, post-amendments) | § 8.2 Phase 3 = "biggest design risk" (character-wide vs chain-wide scope dimension; variance generator); § 8.4 3-category taxonomy (scope-dimension extension layer); § 8.4.2 parallel-chain reach (chain-wide sub-dimension precedent); D66 sharpening one-T4-at-a-time (scope-consequence amplifier); D76 dual-effect; D83 T4 count = chain count − 1; D81 4-phase canonical form | This doc IS the operationalization of doc 40 § 8.2 Phase 3 + § 8.4.x scope-dimension layer for Wave 3 implementation |
| **Doc 41** (L50 hybrid progression framework) | 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C scaffolding); cohort substrate for scope-preference shaping | Cohort-archetype-driven scope preference (§ 4.3) composes with L50 framework cohort substrate |
| **Doc 42** (Wave 1 partition intent) | T4-attunement annotation metadata on Tier-1+2 legendary + sets; capability-toolkit-as-chain-effect-composer surface | Wave 3 scope-dimension scoring CONSUMES Wave 1 partition output: T4-attunement annotation indicates kit-intended scope alignment; capability-toolkit composes with character-wide-promoted Category B/C strategies |
| **Doc 43** (Wave 2 T4 algorithm intent + Wave 2 implementation in `t4_*.py`) | 3-category taxonomy operationalized (Category A/B/C enum + composition rule); 7-strategy registry (6 + DUAL_ELEMENT_ADDITION); parallel-chain reach (`ParallelChainTarget` enum); compositional synergy scan two-pass; Option F 4-phase mechanism; Pattern 9+10 stubs (WARN-not-BLOCK); T4CandidateV2 schema; one-T4-active gating (D66); variable 3-or-4 chain architecture | Wave 3 scope-dimension is an EXTENSION of Wave 2 substrate: extends T4CandidateV2 (no V3 bifurcation); extends synergy scan with scope-dimension scoring; extends Option F retry sequence to include scope-flip retry; extends Pattern 9+10 detection to fire at expanded scope; preserves all Wave 2 contracts |
| **Closeout doc 2026-05-27** | § 1.3 one-T4-active gating substrate (scope-consequence amplifier); § 1.4 variable 3-or-4 chains; § 2.4 T4 algorithm 3-category taxonomy substrate | Source authority for scope-dimension composition with one-T4-active + variable chain count |
| **Wave 2 Gate-2 finding 2026-05-27** | Wave 2 PASS verdict (commit `0783860`); WARN-pattern REMEDIATED milestone (full closure); rocket implementation discipline established | Wave 3 inherits the discipline: 100% accurate post-script empirical count assertions; module-load `assert len(X) == N` pattern; no count drift |
| **8-axis BC lock** | 68,040 cells; operational measurement coordinate system | Wave 3 cross-cohesion validation (§ 7.4 W3.4) extends Wave 2 BC-cell sweep to include scope-dimension variance |

**Authority basis:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 2 Gate-2 PASS verdict on rocket Wave 2 implementation (commit `0783860`) + Wave 2 CLOSED + WARN-pattern REMEDIATED milestone full closure unblock Wave 3 dispatch authoring.

---

## 2. Character-wide vs chain-wide scope dimension — operationalization

Per doc 40 § 8.2 Phase 3 framing + doc 40 § 8.4.2 parallel-chain reach precedent + closeout § 1.3 one-T4-active gating substrate.

### 2.1 Scope dimension definition

**The SCOPE of a T4 capstone effect = the breadth of the kit surface it applies to.**

Three scope values:

| Scope | Definition | Wave 2 status | Wave 3 introduces |
|---|---|---|---|
| **character-wide** | Effect applies to ALL chains in the character kit (every skill on every chain receives the effect) | Wave 2 Category A is inherently character-wide; Categories B/C had NO character-wide option | Wave 3 ADDS character-wide variants for selected Categories B/C strategies (per § 3 applicability table) |
| **chain-wide-OWN** | Effect applies to the T4's own host chain only | Wave 2 default for Categories B/C (the original "chain-specific effect" surface) | Wave 3 preserves this scope as the default-fallback |
| **chain-wide-PARALLEL** | Effect applies to a parallel chain (per Wave 2 W2.3 `ParallelChainTarget` reach) | Wave 2 W2.3 implemented as `ParallelChainTarget.PARALLEL` field on T4CandidateV2 | Wave 3 preserves this scope; treats it as a chain-wide sub-variant |

**Orthogonality to 3-category taxonomy:** scope is a DIMENSION orthogonal to category. Every T4 candidate has BOTH a category (A/B/C) and a scope (character-wide / chain-wide-OWN / chain-wide-PARALLEL). The category × scope combination is the variance space Phase 3 unlocks.

### 2.2 Why scope dimension is the variance generator

Per doc 40 § 8.2: Phase 3 is the variance generator because scope choice DOMINATES the player-experience surface of a T4. Two T4s with identical category + strategy but different scopes feel structurally different:

- **Example A (chain-wide-OWN multiplier):** "Your fire chain skills deal 3× damage when below 50% HP." Affects 1 chain. Build identity: fire-glass-cannon.
- **Example B (character-wide multiplier):** "ALL your skills deal 3× damage when below 50% HP." Affects all chains. Build identity: full-character-glass-cannon. Composes very differently with parallel-chain investment.

The scope choice is the variance generator BECAUSE the effect text is nearly identical but the build implications diverge significantly. Player decisions about which T4 to embody (per D66 one-T4-active sharpening) hinge on scope as much as on category/strategy.

### 2.3 Why scope dimension is the biggest design risk

Per doc 40 § 8.2 framing language and § 5 below detail:

| Risk vector | Description |
|---|---|
| **Combinatorial expansion** | Adding character-wide variants of Categories B/C multiplies T4 design space (3 categories × 7 strategies × 3 scopes = 63 cells, where Wave 2 was 21; only ~30 cells are valid per § 3 applicability constraints, but the design space grows ~50%) |
| **Parallel-chain reach interaction** | Wave 2 W2.3 already introduced parallel-chain as a chain-wide sub-variant; Wave 3 adds character-wide as a peer; the {own-chain, parallel-chain, character-wide} triplet must be selected coherently |
| **Cohort-archetype preference shaping** | Different cohorts (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C scaffolding) prefer different scope distributions; algorithm must shape distribution per cohort intent without homogenizing within-cohort |
| **One-T4-active gating amplification** | Per D66 + closeout § 1.3 only one T4 is active at any time; scope-dimension selection has higher consequence per kit because the player commits to a single scope per active-T4 instance (no aggregating multiple T4 scopes) |
| **Pattern 9 / Pattern 10 expanded-scope risk** | Character-wide promotion of a multiplier OR DoT-additive strategy risks Pattern 9 (passive screen-clear at expanded scope) OR Pattern 10 (DoT-stack degenerate across all chains); Wave 2 Pattern 9+10 detection must extend to operate at scope-promoted effective rates |
| **Spirit-guide projection surface complexity** | Per closeout § 3.4 data-oracle voice surfaces per-T4 projections; scope-dimension adds a dimension to projection messaging ("T4-A character-wide: projected KPM 75; T4-A chain-wide-OWN: projected KPM 68; T4-B chain-wide-PARALLEL to wind chain: projected KPM 71") |

§ 5 spells out the mitigation strategy bundle.

### 2.4 Scope dimension field on T4CandidateV2

Per implementation guidance § 8.4: scope is added as a NEW FIELD on the existing T4CandidateV2 schema rather than bifurcating to a T4CandidateV3. Justifications:

- T4CandidateV2 already carries `parallel_chain_mode: ParallelChainTarget` as analogous field-addition pattern (Wave 2 W2.3)
- Wave 2 → Wave 3 contract change is additive (new field with default value); no breaking change to Wave 2 consumers
- Avoids dual-schema burden during Wave 4 + Wave 5 spec-driven gear gen + sim cycling
- Per Discipline #1.2 code-citation: field addition cites `t4_category_schema.py:240` T4CandidateV2 class as extension point

**Proposed field:** `t4_scope: T4Scope` where `T4Scope` is a new enum with values `CHARACTER_WIDE`, `CHAIN_WIDE_OWN`, `CHAIN_WIDE_PARALLEL` (note: `CHAIN_WIDE_PARALLEL` collapses with the existing `parallel_chain_mode: ParallelChainTarget.PARALLEL` — see § 8.5 for the schema-coherence guidance).

---

## 3. Per-category scope-dimension applicability

Per doc 40 § 8.4 3-category taxonomy + Wave 2 doc 43 § 2 + Wave 2 t4_category_schema.py implementation.

Not every (category, scope) combination is valid. Per-category applicability is bounded structurally before scoring fires.

### 3.1 Applicability matrix

| Category | character-wide eligibility | chain-wide-OWN eligibility | chain-wide-PARALLEL eligibility | Notes |
|---|---|---|---|---|
| **A — Class mechanical / energy alteration** | INHERENT (the category IS character-wide by definition per Wave 2 § 2.1) | NOT applicable (Category A cannot be chain-scoped — would degenerate to "consequences of character-wide effect spelled out in chain terms" per Discipline #31 separability) | NOT applicable (same as above) | Category A has scope FIXED at character-wide; Wave 3 does not add scope variance to Category A |
| **B — Chain multiplicative event** | ELIGIBLE for promotion (e.g., character-wide multiplier on all chains' skills; subject to magnitude-band downscaling per § 4.5) | DEFAULT (Wave 2 baseline; preserved) | ELIGIBLE (Wave 2 W2.3 baseline; preserved) | Scope variance space: all three values possible per generation; algorithm selects per § 4 |
| **C — Chain element conversion / addition** | ELIGIBLE for promotion (e.g., character-wide DUAL_ELEMENT_ADDITION = all chains' skills add a secondary element; subject to magnitude-band downscaling per § 4.5) | DEFAULT (Wave 2 baseline; preserved) | ELIGIBLE (Wave 2 W2.3 baseline; preserved) | Scope variance space: all three values possible per generation; algorithm selects per § 4 |

**Key constraint per Discipline #31 separability:** Category A's scope is FIXED (inherent character-wide). Adding chain-wide variants of Category A would produce non-separable T4 designs where the chain-wide effect is just the character-wide effect re-stated. § 11 framing-audit Q1 surfaces this as the load-bearing assumption to refute.

### 3.2 Per-strategy scope eligibility within Categories B/C

Not every Category B/C strategy supports character-wide promotion equally. Per-strategy applicability:

| Strategy | Category | character-wide eligible? | Rationale + genre precedent |
|---|---|---|---|
| Skill-specific TRADE_OFF | B | YES (with magnitude downscaling) | PoE keystone equivalents (e.g., "all skills cost mana but deal 50% more damage" — Mind Over Matter-adjacent variants); D4 paragon character-wide tradeoffs |
| GEOMETRY_COLLAPSE | B | NO | Geometry alteration is structurally per-skill (a skill IS the unit of geometry); character-wide geometry collapse would degenerate to "all your skills become projectiles" producing unplayable kits (parallel-chain reach is the appropriate breadth lever for this strategy, NOT character-wide promotion) |
| Multiplier strategies | B | YES (with HEAVY magnitude downscaling per § 4.5) | PoE "increased damage with skills" character-wide; D4 "damage to enemies" character-wide variants; **Pattern 9 risk vector — Pass 2 preserve check fires hard here per § 5.2** |
| ELEMENT_CONVERSION | C | YES (with secondary-element coherence check) | PoE "all skills deal cold instead of [their natural element]" character-wide variants; **risk vector: kit may lose element-coverage diversity if all chains convert to same element; Pass 2 preserve check via element-gap-fill pattern per Wave 2 § 5.4** |
| DUAL_ELEMENT_ADDITION | C | YES (with magnitude downscaling per § 4.5) | PoE "all skills deal X% as fire" character-wide; D4 "all skills deal X% as cold" canonical; **Pattern 10 risk vector — Pass 2 preserve check fires hard here when secondary element is DoT-capable per § 5.2** |

**Wave 3 scope-eligibility flags per strategy:** rocket implementation MUST encode the eligibility flag as module-level constant `STRATEGY_CHARACTER_WIDE_ELIGIBILITY: dict[str, bool]` for `assert len(...)` empirical-count discipline per Wave 2 Gate-2 WARN-pattern REMEDIATED milestone.

### 3.3 Composition with parallel-chain reach (Wave 2 W2.3)

Wave 3 scope-dimension does NOT supersede parallel-chain reach; it sits as a peer dimension. Composition:

- **chain-wide-OWN** = Wave 2 default; `parallel_chain_mode = OWN_CHAIN`
- **chain-wide-PARALLEL** = Wave 2 reach; `parallel_chain_mode = PARALLEL` (preserved Wave 2 surface; collapse with `t4_scope` per § 8.5 schema-coherence guidance)
- **character-wide** = Wave 3 new; `t4_scope = CHARACTER_WIDE`; `parallel_chain_mode` is NOT MEANINGFUL when scope is character-wide (algorithm sets to OWN_CHAIN as schema-default; documentation note in T4CandidateV2 docstring per § 8.5)

---

## 4. Scope-dimension selection algorithm

Per doc 40 § 8.2 Phase 3 framing + Wave 2 doc 43 § 4.5 own-chain-vs-parallel-chain selection precedent.

For each T4 candidate generation event, the algorithm executes the following selection sequence.

### 4.1 Step 1 — Bound applicability per category

Per § 3.1 applicability matrix:

- If category = **A** → scope = `CHARACTER_WIDE` (fixed; no selection needed; proceed to Wave 2 algorithm)
- If category = **B** or **C** → scope candidates = `{CHARACTER_WIDE if strategy eligible per § 3.2, CHAIN_WIDE_OWN, CHAIN_WIDE_PARALLEL}` (cardinality 2-3 per strategy)

### 4.2 Step 2 — Cohort-archetype prior per scope

Apply cohort-archetype prior to score each scope candidate. Per Block C scaffolding 4-cohort architecture (DPS-min-maxer / Balanced / Defensive / Hybrid).

**Cohort-archetype scope preference priors (starting estimates; gamora SC-7 iterates per #18.2):**

| Cohort archetype | character-wide prior weight | chain-wide-OWN prior weight | chain-wide-PARALLEL prior weight | Rationale |
|---|---|---|---|---|
| **DPS-min-maxer** | 0.50 | 0.30 | 0.20 | Maximizes per-multiplier coverage across kit; character-wide promotion serves this intent |
| **Defensive** | 0.20 | 0.55 | 0.25 | Prefers focused chain-wide investment with predictable behavior; character-wide effects can dilute defensive layering |
| **Balanced** | 0.30 | 0.40 | 0.30 | Modest preference for chain-wide-OWN; otherwise approximately uniform |
| **Hybrid** | 0.25 | 0.30 | 0.45 | Strongly prefers chain-wide-PARALLEL (the cross-chain composition surface that defines Hybrid identity) |

**Application:** prior weight feeds into the per-scope synergy-score multiplier; higher prior weight amplifies the candidate's net synergy score by `(1 + prior_weight)`.

### 4.3 Step 3 — Per-scope synergy scan candidate generation

For each eligible scope (Step 1 output), generate a T4 candidate with that scope filled in and route through Wave 2 compositional synergy scan (doc 43 § 5). The synergy scan operates on the candidate's full effect surface — character-wide scope produces a different effect surface than chain-wide-OWN, so the synergy scan scores them as distinct candidates.

**Pass 1 (resolve) extension for scope:** add a Pass 1 pattern entry — **scope-coverage-fit** — that rewards character-wide scope when the kit has broad element-coverage gaps (character-wide ELEMENT_CONVERSION or DUAL_ELEMENT_ADDITION can resolve coverage breadth) AND rewards chain-wide-PARALLEL when parallel-chain has identifiable composition synergy AND rewards chain-wide-OWN as the neutral baseline.

**Pass 2 (preserve) extension for scope:** add Pass 2 pattern entries reflecting scope-specific risks:
- **scope-promotion-trap (character-wide):** character-wide promotion of multiplier strategy fires Pattern 9 check at expanded scope; character-wide promotion of DoT-additive strategy fires Pattern 10 check at expanded scope (per § 5.2 below for detection-threshold extension)
- **scope-dilution-trap (character-wide):** character-wide promotion of element-conversion can REMOVE element-coverage diversity (every chain converts to same element); Pass 2 preserve via element-gap-fill pattern (doc 43 § 5.4) detects this and rejects

### 4.4 Step 4 — Net synergy score selection with cohort prior

Per Wave 2 doc 43 § 4.5 selection pattern, extended for scope:

1. Compute net synergy score per candidate (Pass 1 resolve − Pass 2 preserve, including § 4.3 extensions)
2. Multiply by cohort-archetype prior weight `(1 + prior_weight)` per § 4.2
3. Select highest cohort-weighted net synergy score
4. **Tie-breaker (within ±5%):** prefer chain-wide-OWN (preserves chain identity by default; character-wide and parallel-chain are opt-in via synergy score). Aligned with Wave 2 doc 43 § 4.5 step 5 own-chain-default tie-breaker.

### 4.5 Step 5 — Magnitude downscaling for character-wide-promoted strategies

When scope = `CHARACTER_WIDE` and strategy is from Category B/C (i.e., promoted from chain-wide to character-wide), apply magnitude downscaling:

- **Multiplier strategies:** downscale magnitude by factor of `1 / sqrt(class_chain_count)` (3-chain class: downscale to ~58%; 4-chain class: downscale to ~50%). Rationale: character-wide multiplier across N chains effectively multiplies coverage by N; preserving per-chain effective impact prevents Pattern 9 runaway
- **DUAL_ELEMENT_ADDITION:** downscale secondary-element magnitude by factor of `1 / sqrt(class_chain_count)`. Rationale: same as multiplier — character-wide added-element across N chains amplifies effective contribution
- **ELEMENT_CONVERSION:** no magnitude change (conversion is binary, not multiplicative)
- **Skill-specific TRADE_OFF (when character-wide-promoted):** trade-off ratio downscaled by `1 / sqrt(class_chain_count)` on the gain side; cost side preserved (makes character-wide trade-off less rewarding per scaling axis, encouraging chain-wide-OWN as default)

**Magnitude downscaling is STARTING ESTIMATE.** Gamora SC-7 calibrates post-Wave-3-baseline per Discipline #18.2. Wave 3 ships with `1 / sqrt(N)` downscaling as algorithm-default; sidecar telemetry per § 8.6 informs SC-7 iteration.

### 4.6 Step 6 — Option F retry sequence extension

Per Wave 2 doc 43 § 6.2 Option F retry pattern, extended for scope:

- **Retry 1 (Wave 2):** alternative Category B/C strategy
- **Retry 2 (Wave 2):** alternative Category A strategy
- **Retry 3 (Wave 2):** flip parallel-chain reach
- **Retry 4 (Wave 3 NEW):** flip scope dimension (if Category B/C → try character-wide if eligible; else try chain-wide-PARALLEL; else try chain-wide-OWN)

Retry count extended from 3 to 4 per Wave 3. Per Discipline #29 commitment-to-consequence: configurable per D62 compute budget (Cycle 14+ may expand or contract per gamora SC-7 calibration).

---

## 5. Biggest-design-risk handling

Per doc 40 § 8.2 "biggest design risk" framing. § 2.3 enumerated the 6 risk vectors; this section spells out the 4-strategy mitigation bundle.

### 5.1 Mitigation 1 — Per-archetype scope-dimension defaults (architectural bounding)

**Bound the design space ARCHITECTURALLY before scoring fires.** Per § 3.1 applicability matrix:

- Category A scope is FIXED at character-wide (no scope variance; ~33% of T4 design space is scope-deterministic)
- Per § 3.2 strategy-specific eligibility flags structurally exclude character-wide promotion for GEOMETRY_COLLAPSE (~14% of strategy × scope cells excluded)

Net: of 63 nominal (category × strategy × scope) cells, ~30 are valid per § 3 applicability. Architectural bounding reduces the search space by ~50% BEFORE scoring discriminates further.

### 5.2 Mitigation 2 — Pattern 9 + Pattern 10 detection extension at scope-promoted effective rates

Per Wave 2 doc 43 § 7.1 + § 7.2 Pattern 9 + Pattern 10 detection (currently WARN-not-BLOCK stubs per Wave 2 Gate-2 D2 verification): extend detection logic to operate at SCOPE-PROMOTED effective rates.

**Pattern 9 (passive screen-clear) — scope extension:**
- Wave 2 detection: per-build active-input-rate at <1 active skill per 10 sec
- Wave 3 extension: when character-wide multiplier strategy is selected, effective per-chain multiplier × number-of-chains can produce passive screen-clear effective-DPS even with non-passive input rate; Wave 3 detection ADDS a check on character-wide-promoted multiplier strategies: if `(effective_multiplier × class_chain_count) > expected_DPS_threshold_for_screen_clear` then WARN-flag with `scope_amplification` attribution
- Detection threshold STARTING ESTIMATE (gamora SC-7 iterates): `expected_DPS_threshold_for_screen_clear = 8 × kit_baseline_DPS_at_node` (8× is the "passive screen-clear" effective-DPS approximation per Wave 2 doc 43 § 7.1 calibration band)

**Pattern 10 (DoT-stack degenerate) — scope extension:**
- Wave 2 detection: per-build DoT-DPS-at-max-stack-count > 5× expected sustained DPS
- Wave 3 extension: when character-wide DUAL_ELEMENT_ADDITION is selected with DoT-capable secondary element (burn / bleed / poison / cold-degen), effective DoT contribution stacks across all chains; Wave 3 detection ADDS a check: if `(per_chain_DoT_contribution × class_chain_count × max_stack_count) > 5 × expected_sustained_DPS` then WARN-flag with `scope_amplification` attribution
- Detection threshold STARTING ESTIMATE preserved at 5× (Wave 2 calibration band); scope multiplier (`class_chain_count`) propagates through detection arithmetic

**WARN-not-BLOCK preserved per Wave 2 Gate-2 D2 verification.** Wave 3 detection extension follows the same v1 vs v1.1 catalog discipline (gamora SC-7 decision post-Wave-3-baseline per Discipline #18.2 on inclusion in v1 catalog; Wave 3 ships as stubs).

### 5.3 Mitigation 3 — One-T4-active gating composes with scope-dimension

Per closeout § 1.3 + doc 40 D66 sharpening: only one T4 capstone is active at any time. Per-build complexity bounded by gating — no need to score scope-dimension across multiple-T4-active combinations (would be 3^k scope combinations for k active T4s; one-T4-active reduces to 3 scope cells per generation event).

**Discipline #29 commitment-to-consequence application:** the player chooses ONE T4 to embody = ONE scope to commit to. Switching scope requires respec-with-legendary-trigger per D65 (the same SWAP mechanism as switching active T4 per Wave 2 doc 43 § 8.2). Scope choice is durable within the active-T4 window, NOT free-toggleable.

**Spirit-guide projection extension per closeout § 3.4 data-oracle voice:** spirit-guide messaging surfaces per-T4 + per-scope projections when multiple T4s are at-threshold:

> "Currently playing fire chain T4 chain-wide-OWN: projected KPM 75, defensive uptime 62%. Switching to fire chain T4 character-wide: projected KPM 88 BUT defensive uptime drops to 51% per Pattern 9 stub warning. Switching to wind chain T4 chain-wide-PARALLEL to fire chain: projected KPM 71 with composition bonus to both elements."

Wave 3 implementation MUST emit per-scope projection data for spirit-guide consumption per doc 41 D31 spirit-guide-projection language framework + closeout § 3.4 data-oracle voice.

### 5.4 Mitigation 4 — Gamora SC-7 post-Wave-3-baseline calibration delegation

Per Discipline #18.2 consultation timing: methodology consultation at extension hotspots fires AFTER baseline empirical data, not before. Wave 3 ships with starting estimates; gamora SC-7 calibrates post-baseline.

**Specific delegations to gamora SC-7 post-Wave-3-baseline:**

| Calibration target | Starting estimate (Wave 3 ships) | gamora SC-7 iterates |
|---|---|---|
| Cohort-archetype scope-preference prior weights (§ 4.2) | DPS-min-maxer 0.50/0.30/0.20; Defensive 0.20/0.55/0.25; Balanced 0.30/0.40/0.30; Hybrid 0.25/0.30/0.45 | Empirical baseline of scope distribution per cohort per progression node; prior weights adjusted to produce target distribution |
| Magnitude downscaling formula (§ 4.5) | `1 / sqrt(class_chain_count)` for multiplier + DUAL_ELEMENT_ADDITION + TRADE_OFF gain | Empirical baseline of character-wide effective-DPS contribution vs chain-wide; downscaling formula adjusted to equalize effective per-T4 build impact |
| Pattern 9 scope-amplification threshold (§ 5.2) | `8 × kit_baseline_DPS_at_node` | Empirical baseline of effective DPS distribution across cohorts × scopes; threshold adjusted to catch true passive-screen-clear cases without false-positives on legitimate high-DPS builds |
| Pattern 10 scope-amplification threshold (§ 5.2) | 5× expected sustained DPS preserved from Wave 2 | Same as Pattern 9 above for DoT-stack |
| Option F Retry 4 retry-budget allocation (§ 4.6) | 1 additional retry (total 4) | Empirical regeneration-rate distribution; retry budget adjusted per cost-vs-fallback-rate trade-off per D62 compute budget |
| Tie-breaker tolerance (§ 4.4) | ±5% preserves Wave 2 own-chain default tie-breaker | Empirical distribution of tie-breaker activations; tolerance adjusted to reduce tie-breaker dominance vs. genuine synergy selection |

**Discipline #18.2 founding instance composition:** Wave 3 IS an extension hotspot of the Wave 2 T4 algorithm framework (per doc 43 § 11.7 + Discipline #32 first-do-no-harm operating against scope-promoted effects). Per #18.2: consultation fires AFTER Wave 3 baseline, not before. Wave 3 design intent (this doc) operationalizes the framework; Wave 3 implementation produces baseline empirical data; gamora SC-7 consultation post-baseline calibrates.

---

## 6. Composition with Wave 2 outputs

Wave 3 Phase 3 extends Wave 2 substrate; does NOT supersede or breaking-change any Wave 2 contract.

| Wave 2 surface | Wave 3 composition |
|---|---|
| **`t4_category_schema.py` 3-category taxonomy** (`T4Category` enum A/B/C; composition rule "always A + exactly one of B or C") | Preserved unchanged. Scope-dimension sits orthogonal to category; does NOT alter category composition rule |
| **`ALL_T4_STRATEGIES` 7-strategy registry** (6 + DUAL_ELEMENT_ADDITION) | Preserved unchanged. Scope-dimension applies per-strategy eligibility flag (§ 3.2 `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` constant) |
| **`ParallelChainTarget` enum** (`OWN_CHAIN`, `PARALLEL`) on T4CandidateV2 | Collapses with `t4_scope`: `PARALLEL` value of `ParallelChainTarget` maps to `CHAIN_WIDE_PARALLEL` value of `T4Scope`; backward-compatible (Wave 2 callers reading `parallel_chain_mode` continue to work; Wave 3 readers consult `t4_scope` for the unified scope picture). See § 8.5 for the schema-coherence guidance |
| **`t4_synergy_scan.py` compositional synergy scan two-pass** (`PASS_1_CATALOG` 5 entries; `PASS_2_CATALOG` 8 entries; net synergy score; threshold 10.0) | Extended per § 4.3: Pass 1 gains 1 entry (scope-coverage-fit pattern → 6 entries total); Pass 2 gains 2 entries (scope-promotion-trap + scope-dilution-trap → 10 entries total). Module-load `assert len(PASS_1_CATALOG) == 6` and `assert len(PASS_2_CATALOG) == 10` per Wave 2 Gate-2 WARN-pattern REMEDIATED discipline |
| **`t4_option_f.py` 4-phase Option F mechanism** | Extended per § 4.6: Retry sequence adds Retry 4 (scope-flip); `OPTION_F_PHASES` constant length preserved at 4 (phase 1 retry count internally extends from 3 to 4; phase count unchanged) |
| **Pattern 9 + Pattern 10 detection stubs** (WARN-not-BLOCK; `DEGENERATE_DETECTION_PATTERNS` length 2) | Extended per § 5.2: detection logic operates at scope-promoted effective rates; pattern count preserved at 2 (`assert len(DEGENERATE_DETECTION_PATTERNS) == 2` per Wave 2 Gate-2 D2); scope-amplification attribution added to WARN messaging |
| **T4CandidateV2 schema** | Extended per § 2.4 + § 8.5: add `t4_scope: T4Scope` field with default value derived from `(category, parallel_chain_mode)` for backward compatibility (Wave 2 candidates default to `CHAIN_WIDE_OWN` or `CHAIN_WIDE_PARALLEL` per their `parallel_chain_mode`; Wave 3 candidates may also be `CHARACTER_WIDE`). Schema is still T4CandidateV2; no V3 bifurcation per § 8.5 schema-coherence guidance |
| **`T4ClassChainConfig.t4_count = class_chain_count - 1`** (D83 formula) | Preserved unchanged. Scope-dimension is orthogonal to chain-count |
| **`T4ActiveGateResult`** (one-T4-active enforcement per D66) | Preserved unchanged. Scope-dimension is bounded by one-T4-active (per § 5.3 mitigation 3) |
| **Wave 1 partition (T4-attunement annotation + capability toolkit)** | Wave 3 scope-dimension scoring consumes T4-attunement annotation as scope-preference input: annotation indicates kit-intended scope alignment (e.g., "character-wide-favoring annotation" tilts synergy score toward character-wide-promoted candidates) |
| **5-category synergy taxonomy** (tension-resolution + theme-compound + cross-chain composition + element-gap fill + scaling-interaction) | Preserved unchanged. Scope-dimension extensions per § 4.3 sit within existing pattern entries (new entries are catalog extensions, not new categories) |

---

## 7. Sub-wave structure W3.0-W3.5 for rocket Wave 3 implementation

Mirrors Wave 2 doc 43 § 10 W2.0-W2.9 pattern but smaller (6 sub-waves; Wave 3 scope is single-phase). Each sub-wave ends in a gate.

| Sub-wave | Work-unit | Owner | Gate |
|---|---|---|---|
| **W3.0 — Substrate prep + repo-scaffold** | Review Wave 2 outputs (`t4_category_schema.py` + `t4_synergy_scan.py` + `t4_option_f.py` + `t4_algorithm_wave2.py`); identify extension points (T4CandidateV2 field addition; PASS_1_CATALOG + PASS_2_CATALOG extension; Pattern 9+10 detection scope-amplification extension; Option F Retry 4 extension); spot-check Wave 2 schema coherence to confirm field-addition pattern viable | rocket | Substrate prep audit committed; ready for W3.1 |
| **W3.1 — Scope-dimension schema extension** | Schema for `T4Scope` enum (CHARACTER_WIDE / CHAIN_WIDE_OWN / CHAIN_WIDE_PARALLEL); `t4_scope: T4Scope` field added to T4CandidateV2 with backward-compatible default derivation per § 8.5 schema-coherence guidance; `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` constant (per-strategy boolean) per § 3.2; math note per Discipline #1 BEFORE schema implementation | rocket | jack-ryan Gate-1 critique on schema; math note PASS per #1; backward-compat preserved per `parallel_chain_mode` ↔ `t4_scope` coherence |
| **W3.2 — Per-category scope-dimension applicability implementation** | § 3 applicability matrix encoded; Category A scope FIXED at CHARACTER_WIDE (no selection branch); Categories B/C scope-eligibility branch per § 3.2 strategy flags; Discipline #31 separability guard for Category A scope-fixity | rocket | jack-ryan Gate-1 critique; test coverage on per-category scope-eligibility paths; Category A separability guard verified |
| **W3.3 — Scope-dimension selection algorithm + biggest-design-risk mitigation** | Selection algorithm per § 4 (6 steps: applicability bound + cohort prior + per-scope synergy scan + cohort-weighted score selection + magnitude downscaling for character-wide-promoted + Option F Retry 4 scope-flip); biggest-design-risk mitigation bundle per § 5 (4 mitigations); Pattern 9 + Pattern 10 detection scope-amplification extension per § 5.2 with `scope_amplification` attribution; PASS_1_CATALOG extended to 6 entries (+ scope-coverage-fit); PASS_2_CATALOG extended to 10 entries (+ scope-promotion-trap + scope-dilution-trap); module-load `assert len()` for all extended catalogs per Wave 2 Gate-2 WARN-pattern REMEDIATED discipline | rocket | jack-ryan Gate-1 critique; test coverage on per-scope synergy scoring + cohort prior + magnitude downscaling + Retry 4 + Pattern 9+10 scope-amplification |
| **W3.4 — Cross-cohesion validation + Block C scaffolding extension** | Extends Wave 2 W2.8 cross-cohesion pattern with scope-dimension variance: gamora spot-check sim runs against generated T4s across 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid) × 3 scope values (where eligible per § 3.1); validation criteria: per-cohort scope distribution approximates § 4.2 cohort priors (not exactly — synergy scan dominates; priors shape distribution); no cohort × scope cell structurally locked out (every cohort has SOME T4 candidates that score well at SOME scope); Pattern 9 + Pattern 10 scope-amplification WARN-rate within acceptable bounds (starting estimate <15% per cohort × scope cell; gamora SC-7 iterates) | gamora + jack-ryan | jack-ryan Gate-2 PASS on cross-cohesion validation; per-cohort scope distribution within expected bounds; Pattern 9+10 scope-amplification WARN-rate within bounds |
| **W3.5 — Round-trip smoke per Principle 6 (CRITICAL: maintain WARN-pattern REMEDIATED milestone)** | Full round-trip smoke covering all 10 rarity tiers including `legendary_t0_5` (Wave 1+2 carryover discipline); T4 generation per chain × per class × per rarity × per scope (where eligible); T4-attunement annotation matching verified across scope variants; capability-toolkit composition verified across scope variants; per-scope projection emission verified for spirit-guide consumption per § 5.3; post-script empirical count assertions per Discipline #11 (CRITICAL: maintain WARN-pattern REMEDIATED milestone — Wave 3 Gate-2 = 0 empirical assertion failures; module-load `assert len()` for all extended catalogs); MIGRATION.md filed per ADR-004 (Wave 2 → Wave 3 contract change is additive: new `t4_scope` field on T4CandidateV2 with backward-compat default) | rocket + jack-ryan | jack-ryan Gate-2 PASS on round-trip smoke + maintained WARN-pattern REMEDIATED + MIGRATION.md filed |

Sub-wave sequencing is implementation-atomic; rocket + knight-rider may adjust dependencies per Wave 3 implementation dispatch.

---

## 8. Wave 3 implementation guidance for rocket

Concrete next-steps for rocket Wave 3 implementation against this design intent.

### 8.1 Wave 2 substrate consumption

Wave 3 algorithm CONSUMES Wave 2 substrate as platform. Specific consumption points:

| Wave 2 surface | Wave 3 consumption |
|---|---|
| **`T4Category` enum + composition rule** | Wave 3 scope selection branches on category (§ 4.1 Step 1) |
| **`ALL_T4_STRATEGIES` registry** | Wave 3 per-strategy character-wide eligibility flag per § 3.2 |
| **`ParallelChainTarget` enum** | Wave 3 collapses into `T4Scope` per § 8.5 schema-coherence guidance |
| **`t4_synergy_scan.py` two-pass framework** | Wave 3 extends Pass 1 + Pass 2 catalogs per § 4.3 + § 6 |
| **`t4_option_f.py` 4-phase mechanism** | Wave 3 extends Phase 1 retry count to 4 per § 4.6; phase count preserved |
| **`DEGENERATE_DETECTION_PATTERNS`** | Wave 3 extends detection logic at scope-promoted rates per § 5.2; pattern count preserved at 2 |
| **`T4CandidateV2`** | Wave 3 adds `t4_scope: T4Scope` field per § 2.4 + § 8.5 |

### 8.2 Math-before-code (Discipline #1) requirement

Per Discipline #1: math note BEFORE schema implementation. Wave 3 math note location: `~/Games/reincarnated-engine/src/reincarnated/generation/math/cycle-13-wave-3-t4-algorithm-phase-3-math-2026-05-2X.md` (rocket-authored at W3.1).

**Math note must cover:**
- Scope-dimension applicability matrix (per § 3.1 + § 3.2)
- Cohort-archetype scope-preference prior weights (per § 4.2)
- Per-scope synergy scan extension formulas (per § 4.3)
- Cohort-weighted net synergy score formula (per § 4.4)
- Magnitude downscaling formula (per § 4.5; `1 / sqrt(class_chain_count)`)
- Option F Retry 4 scope-flip ordering (per § 4.6)
- Pattern 9 + Pattern 10 scope-amplification detection thresholds (per § 5.2)

### 8.3 Discipline #11 empirical inspection (CRITICAL — maintain WARN-pattern REMEDIATED milestone)

Per Wave 2 Gate-2 WARN-pattern full closure milestone: Wave 3 Gate-2 MUST maintain the discipline. **Every post-script empirical count assertion in completion record MUST verify against actual code state via `len()` or equivalent at write-time.** Per Wave 2 rocket pattern, prefer module-load `assert len(X) == N` enforcement for constant collections.

**Asserted counts to verify empirically at Wave 3 completion-record authoring time:**
- `T4Scope` enum length = 3 (CHARACTER_WIDE + CHAIN_WIDE_OWN + CHAIN_WIDE_PARALLEL)
- `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` keys count = 7 (one per strategy in ALL_T4_STRATEGIES)
- `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count = 4 (TRADE_OFF + Multiplier + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION per § 3.2; GEOMETRY_COLLAPSE = false; Category A strategies = N/A since Category A scope is fixed)
- `PASS_1_CATALOG` extended length = 6 (Wave 2 baseline 5 + scope-coverage-fit)
- `PASS_2_CATALOG` extended length = 10 (Wave 2 baseline 8 + scope-promotion-trap + scope-dilution-trap)
- `DEGENERATE_DETECTION_PATTERNS` length = 2 PRESERVED (Pattern 9 + Pattern 10; scope-amplification is detection-logic extension, not new pattern)
- `OPTION_F_PHASES` length = 4 PRESERVED (Retry count internal to Phase 1 expands; phase count unchanged)
- Cohort archetype count = 4 (DPS-min-maxer + Balanced + Defensive + Hybrid per Block C scaffolding)
- Sub-wave count = 6 (W3.0-W3.5)
- Round-trip smoke rarity coverage = 10 (preserved from Wave 1+2; including `legendary_t0_5`)

Each assertion MUST be drawn from `len()` against the module-level constant at write-time. No pre-addition draft counts.

### 8.4 Cross-seam contract change (Principle 6 gate)

Wave 3 introduces an ADDITIVE cross-seam contract change:
- `T4CandidateV2.t4_scope` new field (default value preserves Wave 2 read-back compatibility per § 8.5)
- T4 telemetry emission gains per-scope distribution (input to D25 cross-season learning + gamora SC-7 calibration)
- Spirit-guide projection consumption surface gains per-scope projections per § 5.3

Round-trip smoke per Principle 6 fires at W3.5 covering all 10 rarity tiers × scope variants + cross-seam consumer paths (spirit-guide consumption + telemetry consumption). MIGRATION.md filing per ADR-004 required (additive; no breaking change to Wave 2 consumers).

### 8.5 Schema-coherence guidance — `T4Scope` vs `ParallelChainTarget`

The `ParallelChainTarget` enum (Wave 2) and the new `T4Scope` enum (Wave 3) overlap at the `PARALLEL` value. Two architectural options:

**Option A (preferred): keep both fields on T4CandidateV2 with coherence rule.**
- Preserve `parallel_chain_mode: ParallelChainTarget` field unchanged (Wave 2 consumers continue to work)
- Add `t4_scope: T4Scope` field as new authoritative scope surface
- Coherence rule: `t4_scope == CHAIN_WIDE_PARALLEL` IFF `parallel_chain_mode == PARALLEL`; `t4_scope == CHAIN_WIDE_OWN` IFF `parallel_chain_mode == OWN_CHAIN`; `t4_scope == CHARACTER_WIDE` THEN `parallel_chain_mode` is irrelevant (algorithm sets to OWN_CHAIN as schema-default; documentation note in T4CandidateV2 docstring)
- Coherence enforced via `__post_init__` validator on T4CandidateV2 (`assert (t4_scope == CHAIN_WIDE_PARALLEL) == (parallel_chain_mode == PARALLEL)` etc.)

**Option B: deprecate `parallel_chain_mode` in favor of `t4_scope` only.**
- Requires Wave 2 consumer migration to read `t4_scope` instead of `parallel_chain_mode`
- Breaking change (Wave 2 consumers fail to read `parallel_chain_mode`)
- Not aligned with field-addition pattern from Wave 2 W2.3

**Recommendation: Option A.** Preserves Wave 2 read-back compatibility; cleanly extends scope surface; coherence-rule-enforced via dataclass validator. Rocket may adjust per implementation experience; gandalf flags either as acceptable provided coherence rule is enforced.

### 8.6 Telemetry emission for gamora SC-7 calibration (#18.2)

Per § 5.4 gamora SC-7 calibration delegation: Wave 3 implementation MUST emit telemetry sufficient for post-baseline calibration.

**Required telemetry fields per T4 generation event:**
- `t4_scope` selected (CHARACTER_WIDE / CHAIN_WIDE_OWN / CHAIN_WIDE_PARALLEL)
- Per-scope candidate net synergy score (3 values per generation event; supports cohort-prior calibration)
- Cohort-archetype prior weight applied (supports prior-weight calibration)
- Magnitude downscaling factor applied (supports downscaling-formula calibration)
- Pattern 9 + Pattern 10 scope-amplification WARN trigger (supports scope-amplification threshold calibration)
- Option F Retry 4 scope-flip activation (supports retry-budget calibration)
- Tie-breaker activation (supports tolerance calibration)

Telemetry feeds into D25 cross-season learning + gamora SC-7 methodology consultation post-Wave-3-baseline.

### 8.7 LLM raw-reasoning constraint (D7 AI-tell line) preserved

Per Wave 2 doc 43 § 11.5: synergy scan is pattern library + statistical priors + algorithmic composition. **NOT LLM raw-reasoning.** Wave 3 scope-dimension extension preserves this constraint:

- Per-scope synergy scan extension entries are gandalf-curated patterns
- Cohort-archetype prior weights are tabular constants per § 4.2
- Magnitude downscaling formula is arithmetic per § 4.5
- Pattern 9 + Pattern 10 scope-amplification thresholds are arithmetic per § 5.2

LLM is permitted for player-facing T4 NAMING per scope variants (e.g., character-wide DUAL_ELEMENT_ADDITION may produce different naming than chain-wide-OWN variant) but NOT for synergy SCORING. The line between naming (LLM-allowed) and scoring (LLM-prohibited) is preserved per D7.

### 8.8 Disciplines #27 / #31 / #32 composition preserved

Per Wave 2 doc 43 § 11.7 + Wave 2 Gate-2 D3+D4+D5 verification: Disciplines #27 + #31 + #32 compose throughout Wave 2; Wave 3 preserves the composition.

- **#27 dual-effect capstone:** preserved unchanged. Every T4 still has Category A (character-wide) + Category B/C (chain-specific OR Wave 3 character-wide-promoted). Scope-dimension does NOT alter the dual-effect rule
- **#31 dual-effect separability:** EXTENDED in Wave 3. When Category B/C is character-wide-promoted, the separability test extends: removing the character-wide-promoted Category B/C effect must still leave Category A as standalone meaningful (preserved from Wave 2); AND removing Category A must leave the character-wide-promoted Category B/C as standalone meaningful (preserved); AND the character-wide promotion itself must NOT make Category A redundant (e.g., character-wide-promoted multiplier strategy AND character-wide multiplier-favoring Category A is redundancy risk per § 11 framing-audit R1)
- **#32 first-do-no-harm:** EXTENDED in Wave 3. The two-pass synergy scan extensions per § 4.3 + Pattern 9+10 scope-amplification per § 5.2 ARE the implementation of #32 at scope-dimension layer

Each Wave 3 sub-wave dispatch (W3.0-W3.5) must cite the relevant disciplines explicitly.

---

## 9. Wave 3 close criterion

Wave 3 closes when:

- [ ] W3.0-W3.5 all complete per completion record table
- [ ] `T4Scope` enum operational (3 values); `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` operational (per § 3.2); T4CandidateV2 extended with `t4_scope` field per § 8.5 schema-coherence guidance
- [ ] Per-category scope-dimension applicability enforced per § 3.1; Category A scope FIXED at CHARACTER_WIDE; Categories B/C scope-eligible per § 3.2 strategy flags; Discipline #31 separability guard for Category A scope-fixity
- [ ] Scope-dimension selection algorithm implemented per § 4 (6 steps); cohort-archetype priors applied; magnitude downscaling for character-wide-promoted Category B/C; Option F Retry 4 scope-flip implemented
- [ ] Biggest-design-risk mitigation bundle implemented per § 5 (4 mitigations: architectural bounding + Pattern 9+10 scope-amplification detection + one-T4-active gating composition + gamora SC-7 post-baseline calibration delegation)
- [ ] PASS_1_CATALOG extended to 6 entries (Wave 2 baseline 5 + scope-coverage-fit); PASS_2_CATALOG extended to 10 entries (Wave 2 baseline 8 + scope-promotion-trap + scope-dilution-trap); module-load `assert len()` enforcement
- [ ] Pattern 9 + Pattern 10 detection scope-amplification operational; `scope_amplification` attribution emitted; WARN-not-BLOCK preserved per Wave 2 Gate-2 D2; `DEGENERATE_DETECTION_PATTERNS` count preserved at 2
- [ ] Cross-cohesion validation per #26 + Block C scaffolding (4 cohort archetypes × 3 scope values per § 3.1 applicability; gamora spot-check sim); jack-ryan Gate-2 PASS on cross-cohesion
- [ ] Round-trip smoke per Principle 6 covering all 10 rarity tiers × scope variants; jack-ryan Gate-2 PASS
- [ ] **WARN-pattern REMEDIATED milestone PRESERVED** per Discipline #11 (Wave 3 Gate-2 = 0 empirical assertion failures; module-load `assert len()` enforcement for all extended catalogs; full closure milestone maintained)
- [ ] Disciplines #27 + #31 + #32 explicitly composed throughout Wave 3 dispatches (per Wave 1+2 Gate-1 routing precedent)
- [ ] MIGRATION.md filed per ADR-004 (additive cross-seam contract change introduced)
- [ ] Math note authored per Discipline #1 BEFORE schema implementation (per § 8.2)
- [ ] Telemetry emission operational per § 8.6 (supports gamora SC-7 post-baseline calibration)
- [ ] jack-ryan Gate-2 PASS on aggregate Wave 3 close
- [ ] Wave 3 close unlocks Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling + gamora SC-7 methodology consultation FULL per Discipline #18.2

**Wave 3 ready to feed Wave 4 + Wave 5 implementation when:** rocket's Wave 3 T4 algorithm produces generated T4 candidates per chain per class per scope whose `t4_scope` metadata can be consumed by Wave 4 spec-driven gear gen (gear attunement at gear-instance generation time consumes scope to determine character-wide vs chain-wide affinity) AND by Wave 5 gauntlet sim (per-scope sim cycling validates character-wide vs chain-wide T4 viability under D67 independent gauntlet sim).

---

## 10. Composition with locked architecture

| Locked architectural element | How this doc composes |
|---|---|
| **Doc 38 D1-D10 delivery strategy** | Variant C engine-as-product: Wave 3 scope-dimension is per-product config; future commercial profiles may config scope eligibility differently |
| **Doc 39 Architecture B substrate-bound at Phase 2** | Phase 2 spec-driven content gen consumes Wave 3 T4 algorithm output; scope-dimension feeds Phase 2d spec-driven gear gen (Wave 4) attunement |
| **Doc 40 § 8.2 Phase 3 framing** | This doc IS the operationalization of doc 40 § 8.2 Phase 3 character-wide vs chain-wide scope dimension as variance generator + biggest design risk |
| **Doc 40 § 8.4 3-category taxonomy** | Wave 3 scope-dimension sits orthogonal to category; preserves 3-category framework |
| **Doc 40 § 8.4.2 parallel-chain reach** | Wave 3 chain-wide-PARALLEL scope collapses with Wave 2 W2.3 `ParallelChainTarget.PARALLEL` per § 8.5 schema-coherence guidance |
| **Doc 40 D66 sharpening (one-T4-at-a-time)** | Wave 3 scope-dimension composes with one-T4-active gating: per-build complexity bounded to one scope per active T4 (per § 5.3 mitigation 3) |
| **Doc 40 D76 dual-effect** | Preserved unchanged. Every T4 still has dual effect (character-wide via Category A + chain-specific or character-wide-promoted via Category B/C) |
| **Doc 40 D83 T4 count = chain count − 1** | Preserved unchanged. Scope-dimension orthogonal to chain count |
| **Doc 40 D81 T4 algorithm canonical form** | Wave 3 IS Phase 3 of the 4-phase canonical form; Wave 3 close unlocks Phase 4 (full sim cycling) |
| **Doc 41 L50 hybrid progression framework** | Cohort-archetype scope priors (§ 4.2) compose with L50 framework cohort substrate per Block C scaffolding |
| **Doc 42 Wave 1 partition intent** | T4-attunement annotation feeds scope-preference scoring per § 8.1 substrate consumption |
| **Doc 43 Wave 2 T4 algorithm intent** | Wave 3 EXTENDS Wave 2 substrate per § 6 composition table; no breaking change |
| **8 BC axes (qd-engine-bc-axes-lock-2026-05-20.md)** | Cross-cohesion validation (W3.4) operates on BC-axis cells × scope variants per § 7.4 |
| **8 resource models (closeout § 2.2)** | Category A RESOURCE_CONVERSION strategy (always character-wide) operates within 8-model catalog; preserved from Wave 2 |
| **Block C calibration scaffolding** | 4-cohort scaffolding feeds cohort-archetype scope priors (§ 4.2) AND cross-cohesion validation (W3.4) |
| **Discipline #1 math-before-code** | Math note BEFORE schema implementation per § 8.2 + W3.1 gate |
| **Discipline #1.2 code-citation** | Wave 3 implementation references Wave 2 code per #1.2; T4CandidateV2 field addition cites `t4_category_schema.py:240`; ParallelChainTarget collapse cites `t4_category_schema.py:221` |
| **Discipline #11 empirical inspection** | Wave 3 post-script assertions MUST verify against `len()` at write-time per § 8.3 (CRITICAL — maintain WARN-pattern REMEDIATED milestone from Wave 2 Gate-2 full closure) |
| **Discipline #18 methodology-before-execution** | Wave 3 T4 algorithm Phase 3 is extension hotspot; gamora SC-7 methodology consultation FULL fires post-Wave-3-baseline per #18.2 (consultation at extension hotspots AFTER baseline empirical data, not before) |
| **Discipline #18.2 consultation timing** | Cohort-archetype priors (§ 4.2) + magnitude downscaling (§ 4.5) + Pattern 9+10 scope-amplification thresholds (§ 5.2) + Option F Retry 4 budget (§ 4.6) + tie-breaker tolerance (§ 4.4) DELEGATED to gamora SC-7 post-Wave-3-baseline; Wave 3 ships with starting estimates |
| **Discipline #23 framing-audit** | This doc includes § 11 framing-audit FROM START per Wave 2 Gate-1 W1 amendment lesson (NOT amendment pattern) |
| **Discipline #26 playability** | Wave 3 T4 algorithm MUST produce playable kits per 6 sub-gates across all scope variants; cross-cohesion validation per W3.4 |
| **Discipline #27 dual-effect capstone** | Preserved unchanged from Wave 2 (per § 8.8) |
| **Discipline #29 commitment-to-consequence** | Scope choice is durable within active-T4 window per § 5.3; switching scope requires respec-with-legendary-trigger per D65 |
| **Discipline #30 sim methodology naming** | Composes with gamora SC-7 post-Wave-3-baseline naming per #18.2 |
| **Discipline #31 dual-effect separability** | EXTENDED in Wave 3 per § 8.8: scope-promoted Category B/C separability test extends to redundancy-risk check with character-wide Category A |
| **Discipline #32 first-do-no-harm** | EXTENDED in Wave 3 per § 8.8: Pass 2 preserve check extensions (scope-promotion-trap + scope-dilution-trap) + Pattern 9+10 scope-amplification ARE the implementation of #32 at scope-dimension layer |

---

## 11. Discipline #23 framing-audit (three-question protocol)

Per Discipline #23 (framing-audit checklist) + Wave 2 doc 43 § 11.9 precedent: at any Pattern A-deep verdict authoring, methodology consultation at a math hotspot, or work-unit committing load-bearing framing assumptions, apply the three-question protocol before execution proceeds. Doc 44 is a load-bearing design-intent doc for the Wave 3 T4 algorithm Phase 3 and operationalizes the "biggest design risk" scope-dimension per doc 40 § 8.2 + closeout § 1.3; the protocol applies at structural layer. **§ 11 included FROM START per Wave 2 Gate-1 W1 amendment lesson — doc 44 does NOT repeat the W1 pattern.**

**Load-bearing framing assumption (Q0 — what's being audited):** the **character-wide vs chain-wide scope dimension** as an orthogonal extension of the 3-category taxonomy IS the correct structural framing for Wave 3 implementation, AND the per-category scope-dimension applicability constraints (Category A scope FIXED at character-wide; Categories B/C eligible per per-strategy flags per § 3.2; GEOMETRY_COLLAPSE structurally excluded from character-wide promotion) bound the design space correctly to manage the "biggest design risk" combinatorial expansion.

### Q1 — What evidence would refute the scope-dimension orthogonality + applicability framing?

The orthogonal scope-dimension framing (every T4 has BOTH category AND scope; per-category applicability per § 3.1) means scope is independent of category at the design-spec layer (modulo per-category structural constraints). Refutation evidence would surface as one of:

- **(R1) Category-A-scope-variance requirement.** Rocket implementation, gandalf design-side audit of v1 Pass 1/Pass 2 catalog entries (§ 4.3), OR gamora SC-7 baseline measurement surfaces a meaningful Category A T4 design intent that genuinely requires scope variance (e.g., a chain-wide Category A that is NOT just "consequences of character-wide effect spelled out in chain terms" per Discipline #31 separability). One example would prompt revisit; a pattern across multiple intents would refute the "Category A scope is FIXED at character-wide" architectural constraint and require revisiting the applicability matrix (§ 3.1).
- **(R2) Systematically degenerate character-wide-promoted Category B/C scoring.** W3.5 round-trip smoke output reveals >25% of generated character-wide-promoted Category B/C candidates trigger Pattern 9 OR Pattern 10 scope-amplification WARN due to combinatorial scope-promotion effects (per § 5.2). Threshold rationale: scope-amplification WARN-rate >25% per character-wide cohort signals the magnitude downscaling formula (§ 4.5) is insufficient OR the character-wide promotion itself is structurally degenerate AT EXISTING applicability; might force §§ 3.1-3.2 applicability tightening (e.g., demoting Multiplier strategies from character-wide eligible) OR force §§ 4.5 magnitude downscaling formula adjustment (e.g., `1 / class_chain_count` linear scaling instead of `1 / sqrt(class_chain_count)`). Either response is a Wave 3+ architectural amendment, not a Wave 3 baseline tunable.
- **(R3) Genre precedent refutation.** Discovery during Wave 3 or beyond that PoE keystones / GD masteries / LE skill trees / D4 paragon do NOT separate scope (character-wide vs chain-wide) as a meaningful design dimension (currently doc 40 § 8.2 framing asserts they do; the parallel-chain reach precedent + PoE "X% as fire" character-wide variants + D4 paragon character-wide-favoring nodes + LE skill tree scope variance all support the framing). Counter-evidence would invalidate the variance-generator framing and require revisiting Phase 3 as "biggest design risk" framing entirely (potential collapse of Phase 3 = Phase 2 with parallel-chain reach extended; would simplify Wave 3 substantially).
- **(R4) Cohort-archetype scope-preference uniformity.** Cross-cohesion validation (W3.4) reveals all 4 cohort archetypes produce statistically indistinguishable scope distributions despite the § 4.2 cohort-prior weights. This would refute the "cohort-archetype-driven scope preference" mitigation (§ 4.3 mitigation 2) and signal cohort priors are not effectively shaping distribution. Wave 3+ amendment: revisit cohort priors OR collapse to a single uniform prior.
- **(R5) Schema-coherence violation between `t4_scope` and `parallel_chain_mode`.** Rocket W3.1 implementation discovers the coherence rule per § 8.5 cannot be enforced cleanly (e.g., a Wave 2 consumer reads `parallel_chain_mode` in a context where Wave 3 `t4_scope` is `CHARACTER_WIDE` but the Wave 2 default value of `parallel_chain_mode` produces incorrect downstream behavior). Wave 3+ amendment: adopt Option B (deprecate `parallel_chain_mode`) OR rethink field-addition coherence.

**Current evidence stance:** doc 40 § 8.2 Phase 3 framing + Wave 2 W2.3 parallel-chain reach precedent + closeout § 1.3 one-T4-active gating substrate + genre precedent (PoE/D4/LE/GD scope variance in equivalents) + Wave 2 substrate intactness all triangulate on the scope-dimension orthogonality framing as well-grounded. No refutation evidence surfaced at intent-authoring time. Wave 3 implementation + W3.4 cross-cohesion validation + W3.5 round-trip smoke is the cheapest empirical test (see Q2).

### Q2 — How cheaply can rocket + gamora implementation falsify?

The cheapest refuting tests piggyback on existing W3.4 + W3.5 sub-wave deliverables; **no separate dispatch needed.**

- **R1 refutation cost:** zero (surfaces during gandalf pattern-library audit at W3.1 design-spec review OR during rocket W3.2 per-category implementation; if Category A scope-variance requirement surfaces, gandalf escalates as Wave 3+ framing review item per recognition-validate-commit § 3.4)
- **R2 refutation cost:** zero (W3.5 round-trip smoke telemetry already emits Pattern 9 + Pattern 10 scope-amplification WARN per § 8.6; aggregate WARN-rate per cohort × character-wide cell is a single SQL aggregation; refutation threshold check is single boolean per cell)
- **R3 refutation cost:** ~30 min for gandalf Pattern A-light query to legolas Mode A for spot-check on a single genre game's scope-variance pattern (not a full literature pass; spot-check sufficient to refute or confirm framing)
- **R4 refutation cost:** zero (W3.4 cross-cohesion validation telemetry per § 8.6 already emits per-cohort scope distribution; cohort uniformity check is single statistical test)
- **R5 refutation cost:** ~15 min for rocket spot-check on `parallel_chain_mode` consumer paths in Wave 2 code (grep + read); discoverable at W3.1 design-spec review BEFORE W3.2 implementation

**Refutation cycle:** W3.4 + W3.5 telemetry surfaces → aggregate checks fire → if threshold breached, gandalf Pattern A-deep verdict revisits scope-dimension framing OR per-category applicability OR magnitude downscaling OR cohort priors per which refutation surfaced before Wave 4 dispatch authoring. If under threshold + uniformly green, scope-dimension framing is empirically validated by Wave 3 baseline AND framework intactness is preserved for Wave 4.

### Q3 — Alternative framing — "scope as orthogonal dimension" vs "scope as category-specific sub-strategy"

**Alternative framing considered:** scope-dimension could be modeled NOT as orthogonal dimension but as category-specific sub-strategy (e.g., add new Category D = "character-wide-promoted Category B" and Category E = "character-wide-promoted Category C"; 5-category taxonomy instead of 3-category + scope-dimension orthogonal).

**Resolution: orthogonal scope-dimension framing chosen.**

Reasoning:

1. **Preserves Wave 2 3-category taxonomy intactness.** Wave 2 doc 43 § 2 locked the 3-category taxonomy as design-spec + player-facing vocabulary. Adding 2 new categories at Wave 3 would force re-litigation of the Wave 2 framing AND would force Wave 1 partition T4-attunement annotation (doc 42) re-categorization. Orthogonal scope-dimension layer preserves Wave 2 intactness.

2. **Player-facing surface comprehensibility.** Per Wave 2 doc 43 § 2.3 player-facing vocabulary mapping, the 3-category taxonomy is the player-facing primary unit. A 5-category taxonomy with character-wide-promoted variants as peer categories would require player-facing mental-model expansion ("Wait, is Category D the same as Category B but applied everywhere?"). Orthogonal scope-dimension allows player-facing surface to remain 3-category + 1 scope decision, which maps cleanly to spirit-guide projection messaging per § 5.3.

3. **Implementation cost.** 5-category taxonomy would require T4Category enum expansion + per-category strategy mapping bifurcation + Wave 1 partition consumer-path migration + cross-seam telemetry schema migration. Orthogonal scope-dimension is a field-addition pattern (per Wave 2 W2.3 `parallel_chain_mode` precedent) — much lower implementation surface area.

4. **Composition with parallel-chain reach.** Wave 2 W2.3 introduced parallel-chain reach as a chain-wide sub-variant (`ParallelChainTarget.PARALLEL`). The orthogonal scope-dimension framing collapses parallel-chain cleanly into the scope dimension as `CHAIN_WIDE_PARALLEL` value per § 8.5 schema-coherence guidance. The 5-category framing would require parallel-chain reach to live OUTSIDE the category surface (as it does in Wave 2) AND scope-promotion to live INSIDE — incoherent layering.

**No re-litigation in Wave 3.** Q3 is resolved by this design call. If R1-R5 refutation evidence (per Q1) surfaces during Wave 3 implementation, the Wave 3+ framing review revisits BOTH the orthogonality framing AND the 5-category alternative as a paired question (the alternatives are linked — refuting one might cascade into the other).

### Framing-audit verdict

The three questions are addressable at intent-authoring time and do **not** surface a BLOCK condition. The orthogonal scope-dimension framing is empirically well-grounded per doc 40 § 8.2 framing + Wave 2 parallel-chain precedent + closeout § 1.3 + genre precedent; refutation evidence (R1-R5) is cheaply surfaceable via W3.4 cross-cohesion + W3.5 round-trip smoke piggyback (per Q2 cycle); Q3 alternative framing (5-category) is resolved by Wave 2 3-category intactness + player-facing comprehensibility + implementation cost + parallel-chain reach composition.

**Composition with § 3.4 recognition-validate-commit:** the >25% scope-amplification WARN-rate threshold (Q2 R2) is the primary empirical-evidence criterion that gates re-engagement on the scope-dimension framing question. The other refutation criteria (R1, R3, R4, R5) provide additional empirical gates. If any breached, recognition (refutation evidence surfaced) → validate (Pattern A-deep verdict reviews framing) → commit (Wave 3+ amendment if warranted). If all under threshold, the framing is empirically validated by baseline; commit holds.

**First-canonical-example anchor:** this framing-audit follows the Wave 2 doc 43 § 11.9 pattern (dedicated subsection on load-bearing intent doc) INCLUDED FROM START per Wave 2 Gate-1 W1 lesson (W1 amendment surfaced § 11 absence on doc 43; doc 44 includes from start). Doc 42 § 11 was in-table cell; doc 43 § 11.9 was dedicated subsection added post-amendment; doc 44 § 11 is dedicated subsection from-start. The trajectory is "framing-audit appears in larger more load-bearing canonical docs as standard structure," with doc 44 establishing the from-start expectation as Wave 3+ baseline.

---

## 12. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Wave 3 T4 algorithm Phase 3 design intent canonical for Cycle 13 multi-T4 architecture cycle
**Composition:** with doc 38 + doc 39 + doc 40 (post-2026-05-27 amendments § 8.2 Phase 3 + § 8.4.x) + doc 41 + doc 42 (Wave 1 partition substrate) + doc 43 (Wave 2 T4 algorithm intent + Wave 2 rocket implementation in `t4_*.py`) + closeout doc 2026-05-27 (§ 1.3 + § 1.4 + § 2.4) + Wave 2 Gate-2 finding (PASS + WARN-pattern REMEDIATED milestone full closure) + 8-axis BC lock + 8-model resource catalog + Block C calibration scaffolding + Disciplines #1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32
**Authority:** Matt 2026-05-27 verbatim — autonomous Wave 0 → Wave 1 → Wave 2 → Wave 3 sequencing per ratified framing brief § 4.1 + jack-ryan Wave 2 Gate-2 PASS verdict (commit `0783860`) + Wave 2 CLOSED + WARN-pattern REMEDIATED milestone full closure unblock Wave 3
**Next gates:**
- jack-ryan Wave 3 Gate-1 critique on this doc (post-authoring; separate dispatch fires)
- Rocket Wave 3 implementation per § 7 sub-wave structure + § 8 guidance (post-Gate-1 close; separate dispatch fires)
- Gamora SC-7 methodology consultation FULL post-Wave-3-baseline per Discipline #18.2 (separate dispatch; Wave 3 cohort-archetype priors + magnitude downscaling + Pattern 9+10 scope-amplification thresholds + Option F Retry 4 budget + tie-breaker tolerance are SC-7 territory)
- Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling (unlocked post Wave 3 close)

**For:** the Wave 3 T4 algorithm Phase 3 design intent canonical for Cycle 13 multi-T4 architecture cycle. Character-wide vs chain-wide scope dimension operationalized (orthogonal to 3-category taxonomy; 3 scope values CHARACTER_WIDE + CHAIN_WIDE_OWN + CHAIN_WIDE_PARALLEL; per-category applicability constraints — Category A scope FIXED at character-wide; Categories B/C scope-eligible per per-strategy flags; GEOMETRY_COLLAPSE structurally excluded from character-wide promotion). Scope-dimension selection algorithm (6 steps: applicability bound + cohort prior + per-scope synergy scan + cohort-weighted score selection + magnitude downscaling for character-wide-promoted Category B/C via `1 / sqrt(class_chain_count)` formula + Option F Retry 4 scope-flip). Biggest-design-risk handling 4-mitigation bundle (architectural bounding + Pattern 9+10 scope-amplification detection extension + one-T4-active gating composition + gamora SC-7 post-baseline calibration delegation per #18.2). Composition with Wave 2 outputs via T4CandidateV2 field-addition pattern (NOT V3 bifurcation; preserves Wave 2 contracts; schema-coherence guidance for `t4_scope` ↔ `parallel_chain_mode` collapse). Sub-wave structure W3.0-W3.5 (6 sub-waves; smaller than Wave 2 W2.0-W2.9 to match smaller Phase 3 scope). Wave 3 implementation guidance for rocket (Wave 2 substrate consumption + math-before-code + Discipline #11 maintain WARN-pattern REMEDIATED milestone + cross-seam contract per Principle 6 additive + schema-coherence guidance + telemetry emission for gamora SC-7 + LLM raw-reasoning constraint preserved + Disciplines #27/#31/#32 composition preserved). § 11 Discipline #23 framing-audit INCLUDED FROM START per Wave 2 Gate-1 W1 lesson (NOT amendment pattern). Wave 3 close criterion = jack-ryan Gate-2 PASS on rocket Wave 3 implementation against this intent + maintained WARN-pattern REMEDIATED milestone per Wave 2 full closure precedent. Wave 3 ready to feed Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling + gamora SC-7 methodology consultation FULL upon close. Authoritative source for CURRENT-status truth remains `canonical/00-ground-state.md`.

**Signed:** gandalf (story-and-design steward)
