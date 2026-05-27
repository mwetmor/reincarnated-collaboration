# Cycle 13 — Wave 4 Sim Methodology Framework

> **STATUS:** AUTHORED 2026-05-26 — gamora Pattern A-deep per dispatch `2026-05-26-gamora-cycle-13-wave-0-methodology-consultation-prep.md`
>
> **Authority basis:** Matt 2026-05-26 Cycle 13 framing brief Q6 ratification (gamora consultation gates Wave 4) + gandalf Pattern A-deep verdicts Blocks C.1/C.2/C.3 RATIFIED DELEGATE-TO-GAMORA + hive-mind decision-routing directive (seam-owner decides in-scope methodology)
>
> **Discipline #18.2 constraint:** this is the PREP framework. Items classified PRE-BASELINE-RESOLVABLE are designed here and ready to execute. Items classified REQUIRES-WAVE-3-BASELINE are flagged with their empirical criterion for post-Wave-3 finalization. The full methodology consultation closure fires post-Wave-3 close.

**Author:** gamora (simulation + spirit-guide seam owner)
**Pattern:** Pattern A-deep (methodology framework; pre-baseline-resolvable + post-baseline-pending classification per Discipline #18.2)
**Companion docs:**
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 (D60-D86) — primary architecture source
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.5 — content lifecycle dependency chain
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` Blocks C.1/C.2/C.3 — delegation inputs
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 7 — compute budget framing
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #1.1 + #18 + #18.2 + #19.1 + #26 + #30

---

## § 1 — TL;DR

**Methodology pattern name (per Discipline #30):**
> **"Per-weapon-cohort-exhaustive with sub-option-B fallback for cohort-clear legendaries; stratified by progression node; tiered quick-estimate first validation"**

Four-axis per Discipline #30:
- **Node-population approach:** per-weapon cohort coverage (Sub-option A primary); per-legendary cohort selection (Sub-option B fallback for cohort-clear)
- **Edge-case coverage strategy:** per-legendary anchoring on tier-2 legendaries/sets; adversarial configuration inclusion via hybrid cohort (build-diversity stress case)
- **Cohort definition basis:** 4 archetypes (DPS-min-maxer / balanced / defensive / hybrid) defined by investment-pattern + gear-preference + KPM-expectation-band
- **Compute-burden management:** quick-estimate filter first; full-sim only on quick-estimate passers; stratified sampling with statistical floor per stratum; intermediate result caching

**D84 sub-option choice:** Hybrid-within-hybrid (A for ambiguous legendaries; B for cohort-clear legendaries). See § 2.

**PRE-BASELINE-RESOLVABLE count:** 22 items across sections A, B, E, and partial C/D/F.
**REQUIRES-WAVE-3-BASELINE count:** 12 items across sections C, D, and partial F.

---

## § 2 — Sub-option selection (D84 framework choice)

### 2.1 Sub-option A vs B vs Hybrid — decision

**Verdict: Hybrid-within-hybrid as starting point, with the discrimination criterion defined as:**

- **Sub-option A (per-weapon cohort coverage)** applies to legendaries where cohort attunement is mechanically ambiguous — i.e., the legendary's capability toolkit does not strongly signal a single cohort. Example: a legendary with generic +35% weapon damage and a "spawns tornadoes on wind hit" triggered passive is ambiguous — DPS-min-maxer, balanced, AND hybrid cohorts could plausibly equip it.

- **Sub-option B (per-legendary cohort selection)** applies to legendaries where the capability toolkit clearly signals a single dominant cohort. Example: a legendary with DEFENSIVE_CONVERSION T4-attunement + armor-focused capability toolkit is cohort-clear (defensive cohort primary; DPS-min-maxer would not equip it at near-endgame progression nodes).

**Discrimination heuristic (PRE-BASELINE-RESOLVABLE):**

A legendary is **cohort-clear** if AT LEAST ONE of the following is true:
1. Its T4-attunement (tier-1/2 only) matches a single T4 strategy archetype that maps to one cohort (DEFENSIVE_CONVERSION / DEFENSIVE_TRADEOFF → defensive cohort; RESOURCE_CONVERSION / ELEMENT_CONVERSION → hybrid cohort; TRADE_OFF → DPS-min-maxer or hybrid; GEOMETRY_COLLAPSE → case-by-case)
2. Its capability toolkit modifier type is exclusively defensive (armor/resistance/evasion-adjusting) with no offensive modifier surface → defensive cohort
3. Its modifier surface is exclusively offensive (crit/attack-speed/damage-multiplier heavy) with no defensive surface → DPS-min-maxer cohort

A legendary is **cohort-ambiguous** (use Sub-option A) if none of the above signals are exclusive.

**Estimated cohort-clear fraction:** based on tier-structure (tier-1 has 1 T4-attunement; tier-2 has 1-2), approximately 50-65% of tier-1+2 legendaries are likely cohort-clear per the attunement discrimination. This is a PRE-BASELINE-RESOLVABLE estimate — the actual fraction is REQUIRES-WAVE-3-BASELINE (depends on what the spec-driven gear gen produces for Wave 4).

### 2.2 Per-legendary cohort anchoring specifics (A.3)

**What "per-legendary cohort anchoring" means:**

For each tier-2 legendary (and tier-1 legendaries with T4-attunement), the sim:
1. Identifies which cohort(s) would equip this legendary at the item's relevant progression node
2. For Sub-option A legendaries: constructs representative builds for EACH cohort that would equip it (min 1 build per applicable cohort)
3. For Sub-option B legendaries: constructs representative build for the single dominant cohort
4. Validates EACH configuration independently per D67 (independent gauntlet sim per attuned-T4 configuration per progression node)

**Anchoring scope:** the per-legendary anchor is the T4-attunement match constraint. A DPS-min-maxer build anchored to legendary L must use L's T4-attunement path, not a different T4. This ensures the validation tests the intended legendary-T4 interaction, not an arbitrary T4 combination that happens to use the legendary for its scalar stats.

**Tier-0 and tier-0.5 legendaries (no T4-attunement):** these are validated against capability-toolkit fit only (which cohort would use this mechanic-adjusting capability?). Sub-option B applies to most tier-0/0.5 (simpler toolkit = more cohort-clear). Tier-0/0.5 are NOT gating items for Wave 4 compute budget — they are lower priority and can be batch-validated post tier-2 validation if compute budget tightens.

### 2.3 #18.2 timing classification for § 2

| Item | Classification |
|---|---|
| Sub-option A/B/hybrid discrimination heuristic | PRE-BASELINE-RESOLVABLE |
| Cohort-clear fraction estimate (50-65%) | PRE-BASELINE-RESOLVABLE (estimate); REQUIRES-WAVE-3-BASELINE (empirical confirmation) |
| Per-legendary cohort anchoring procedural spec | PRE-BASELINE-RESOLVABLE |
| Tier-0/0.5 validation priority order | PRE-BASELINE-RESOLVABLE |

---

## § 3 — Cohort archetype definitions (C.3 delegation)

Gandalf's Block C.3 verdict provides the design-intent qualitative definitions. This section adds gamora's quantitative operationalization for sim purposes.

### 3.1 DPS-min-maxer cohort

**Identity:** "Push damage as far as possible; accept fragility"

**Investment pattern (sim parameterization):**
- Stat-sheet: offensive prefixes maximized (crit-chance + crit-multiplier + weapon-damage at cap; defensive suffixes at floor — minimum HP/armor to survive encounter set without degenerate-state triggers)
- T4 selection: TRADE_OFF or ELEMENT_CONVERSION T4s preferred (damage-multiplier paths); DEFENSIVE_CONVERSION T4s avoided
- Gear selection: tier-1/2 legendaries with offensive capability toolkits; no shield off-hand (tomes/focuses preferred for spellcasters; dual-wield or offensive relic for martials)
- Legendary attunement: matched to the highest-damage T4 path per class

**KPM expectation band:** 85th–100th percentile of per-cell median. In sim terms: target KPM upper-band. Survival floor: 50% (can die to non-trivial content; acceptable for the cohort identity).

**Per-progression-node distribution:**
- Early game: less differentiated (limited legendary access); KPM 75th–90th percentile
- Mid game: differentiation begins with tier-0/0.5 legendary access; KPM 80th–95th
- Endgame start: tier-1 legendary T4-attunement kick in; KPM 85th–100th
- Endgame (85% node): full tier-2 legendary saturation; KPM ceiling band

**Degenerate-state risk:** HIGH. DPS-min-maxer builds with low defensive stats are the primary surface for mandatory-skill-lock detection (if their single damage-maxing skill is required >80% of the time, fails #3 degenerate validator per Verdict D.4).

### 3.2 Balanced cohort

**Identity:** "Solid offense + adequate defense; reliable progression"

**Investment pattern (sim parameterization):**
- Stat-sheet: mixed — 60% offensive / 40% defensive by affix count; neither extreme
- T4 selection: 1 damage-oriented T4 + 1 utility/mixed T4; RESOURCE_CONVERSION or DEFENSIVE_CONVERSION acceptable
- Gear selection: mix of rare/epic + tier-1 legendaries; shield off-hand acceptable for close-range classes; balanced set selections
- Legendary attunement: matched to mixed-purpose T4 path

**KPM expectation band:** 40th–65th percentile of per-cell median. The stable middle of the distribution.

**Per-progression-node distribution:** consistent distribution across all 4 nodes (this is the reference cohort for first-cycle calibration anchoring — the "median player" approximation).

**Degenerate-state risk:** LOW. This cohort is the canary — if balanced builds hit degenerate states, the kit architecture is broken, not the player's investment pattern.

### 3.3 Defensive cohort

**Identity:** "Survive everything; damage is secondary"

**Investment pattern (sim parameterization):**
- Stat-sheet: defensive suffixes maximized (HP + armor + resistance + evasion at cap); offensive prefixes at floor — minimum to avoid zero-damage-floor detection
- T4 selection: DEFENSIVE_CONVERSION or DEFENSIVE_TRADEOFF T4s exclusively; no TRADE_OFF or GEOMETRY_COLLAPSE
- Gear selection: tier-1/2 legendaries with defensive capability toolkits; shield off-hand always; defensive set bonuses
- Legendary attunement: matched to defensive T4 path

**KPM expectation band:** 10th–30th percentile of per-cell median. LOW KPM is expected and acceptable. Survival rate: ≥95% required (this cohort's pass criterion is weighted toward survival, not KPM).

**Per-progression-node distribution:**
- Early/mid game: may barely hit KPM floor — expect 15th–35th percentile
- Endgame: defensive T4-attunements narrow the gap; 10th–30th percentile
- **Special handling:** defensive cohort KPM floor is the primary calibration signal for zero-damage-floor detector. If defensive cohort KPM = 0, this is a degenerate-state detection trigger, not a "defensive build is fine" outcome.

**Degenerate-state risk:** MEDIUM. Low-damage builds can trigger zero-damage-floor if encounter defensive stats (resistances) outpace the character's damage floor. The mandatory-skill-lock detector is LESS relevant for this cohort (defensive builds are expected to lean on fewer high-damage skills).

### 3.4 Hybrid cohort

**Identity:** "Build-craft optimization; capability-toolkit synergies; spirit-guide-driven"

**Investment pattern (sim parameterization):**
- Stat-sheet: variable per build — defined NOT by stat allocation but by T4 + gear combination creating cross-chain synergies
- T4 selection: RESOURCE_CONVERSION or ELEMENT_CONVERSION T4s preferred (these create the cross-chain interactions that define hybrid builds)
- Gear selection: tier-1/2 legendaries with mechanic-adjusting or axis-adjusting capability toolkits (not purely offensive or defensive); cross-chain synergy legendaries
- Legendary attunement: matched to the T4 that creates the synergy, not the highest-damage path

**KPM expectation band:** 60th–85th percentile of per-cell median; HIGH variance (builds that land well spike to 90th+ percentile; builds that misconfigure land near 50th percentile).

**Sim representation challenge:** hybrid cohort is the hardest to parameterize because the investment pattern is emergent. Gamora's approach:
- Construct hybrid builds by picking T4 paths across different chains (one from chain A, activating chain B synergy via RESOURCE_CONVERSION or ELEMENT_CONVERSION)
- This is the "hybrid-within-hybrid" case that Sub-option A specifically handles — hybrid cohort builds often land as cohort-ambiguous legendaries

**Per-progression-node distribution:**
- Endgame nodes: meaningful synergies require tier-1/2 gear; hybrid cohort is primarily an endgame measurement target
- Early/mid game: approximate hybrid cohort with best-available synergy configuration; expect KPM near balanced-cohort range until tier-1 gear arrives

### 3.5 Cross-cohort overlap handling

**Multi-T4 attunement creates cohort membership ambiguity.** A kit with 3 T4 paths (4-chain class per Verdict A.2) can be valid for multiple cohorts depending on which T4 is activated during respec.

**Resolution rule:**
- Each T4 configuration is validated INDEPENDENTLY per D67 (independent gauntlet sim per attuned-T4 configuration)
- Each configuration is assigned to its primary cohort based on the ACTIVATED T4's capability archetype
- A legendary that advocates T4-A (TRADE_OFF → DPS-min-maxer) is validated in DPS-min-maxer cohort for that T4 configuration
- The same legendary in a respec'd configuration activating T4-B (DEFENSIVE_CONVERSION → defensive cohort) is validated SEPARATELY in defensive cohort

This means a 4-chain class with 3 T4s may produce 3 cohort-specific validation runs per progression node per legendary that could support any of those T4s. This is a key compute-budget driver (see § 5).

### 3.6 Cohort granularity — should 4 collapse or split?

**Assessment:** 4 cohorts are appropriate for Wave 4. The two boundary cases:

**Collapse candidate:** defensive + balanced could collapse to a single "non-DPS" cohort. **Rejected.** Defensive cohort's 95% survival floor creates a qualitatively different validation signal than balanced's 50% survival. Conflating them would make zero-damage-floor detection harder (defensive-floor signal would be masked by balanced-cohort average damage).

**Split candidate:** DPS-min-maxer could split into "DPS-glass-cannon" (accepts death to non-trivial content) vs "DPS-survivor" (high damage + enough defense to survive). **Deferred to post-Wave-3-baseline.** If Wave 3 baseline shows DPS-min-maxer cohort has bimodal survival rates (some kits die trivially, others survive), the split becomes empirically motivated. Pre-baseline, a single DPS-min-maxer cohort with survival floor = 50% covers the range adequately.

### 3.7 #18.2 timing classification for § 3

| Item | Classification |
|---|---|
| 4 cohort identities + qualitative definitions | PRE-BASELINE-RESOLVABLE (from gandalf C.3 + gamora operationalization) |
| DPS-min-maxer KPM band (85th–100th percentile) | PRE-BASELINE-RESOLVABLE (starting estimate) |
| Balanced KPM band (40th–65th percentile) | PRE-BASELINE-RESOLVABLE (reference cohort anchor) |
| Defensive KPM band (10th–30th percentile) | PRE-BASELINE-RESOLVABLE (starting estimate) |
| Hybrid KPM band (60th–85th percentile; high variance) | PRE-BASELINE-RESOLVABLE (starting estimate) |
| DPS-min-maxer / DPS-survivor split decision | REQUIRES-WAVE-3-BASELINE (bimodal survival signal needed) |
| Per-cell KPM percentile calibration (actual numbers) | REQUIRES-WAVE-3-BASELINE (empirical from Phase 3 execution) |
| Cohort-clear fraction of actual generated legendaries | REQUIRES-WAVE-3-BASELINE (depends on spec-driven gear gen output) |

---

## § 4 — Power-level targets per progression node (C.1) + WR-bracket definition (C.2)

### 4.1 Per-node "in-band" definition

**Gamora seam authority decision per C.1 delegation:** DELEGATE-TO-EMPIRICAL-ITERATION for the numerical values; ANCHOR the structural form now.

**Structural anchor (PRE-BASELINE-RESOLVABLE):**

The in-band criterion is a compound gate applied per BC cell per progression node:

```
IN-BAND(kit, T4-config, node) = 
    KPM_IN_BAND(kit, T4-config, node)
    AND SURVIVAL_FLOOR(kit, T4-config, node)
    AND NOT DEGENERATE_STATE(kit, T4-config, node)
```

Where:
- **KPM_IN_BAND:** kit's measured KPM (kills-per-minute) vs encounter set falls within ±15% of per-cell median KPM for the applicable progression node AND cohort
- **SURVIVAL_FLOOR:** kit survives ≥80% of test encounters (≥95% for defensive cohort)
- **NOT DEGENERATE_STATE:** all 3 degenerate-state validators pass (per § 6.3)

**Per-cell median computation:** gamora computes empirically during Phase 3 execution, not pre-imposed. First execution against the new engine (post-Wave-3-baseline) produces the per-cell medians that anchor subsequent iteration.

**Starting band: ±15% KPM variance from cell median.** This is tighter than the historical ±25% per project_b14_5_sidecar_analyses.md. Rationale: multi-T4 + spec-driven gear should produce tighter cell-coherence than legacy generation. The ±15% starting estimate is the ANCHOR; it adjusts per cross-season learning D25 if:
- WR-bracket pass rate < 60%: band is too tight — widen to ±18-20%
- WR-bracket pass rate > 95%: band is too loose — tighten to ±12%

### 4.2 Banding shape

**ANCHOR: flat-band-per-node** (same ±15% applied uniformly within a node, regardless of cell type). This is PRE-BASELINE-RESOLVABLE.

**Gradient / curve bands** are DEFERRED pending empirical signal from Wave 3/4 baseline. If cell-type variance (e.g., high proxy-density cells produce systematically lower KPM than low proxy-density cells within the same progression node) is large, gradient banding becomes empirically motivated. That signal requires Wave 3 baseline.

**Per-cohort band modifier (PRE-BASELINE-RESOLVABLE starting position):**
- DPS-min-maxer: upper band shifts +5% (allow ceiling KPM above general band)
- Balanced: ±15% (reference cohort; no modifier)
- Defensive: lower band shifts -5% (allow floor KPM below general band, because defensive builds are expected to kill slower)
- Hybrid: ±20% (wider band; high variance is expected)

### 4.3 Cross-node validation rule

**ANCHOR (PRE-BASELINE-RESOLVABLE, per D67 + D27):**

A kit is validated at ITS TARGET NODE (the progression node the kit was generated for). The kit does NOT need to fall in-band at ALL nodes — only at its target node.

However, the kit MUST NOT cause degenerate states at adjacent nodes tested incidentally during the gauntlet. The cross-node check is:
- Kit generated for endgame-start: primary validation at endgame-start band. Secondary check: does it break playability at mid-game progression (can it even function if the player under-gears)? A kit that is ONLY functional at exactly endgame-start-tier gear is a degenerate-state risk for mid-season players.

**Cross-node degenerate-state check (secondary; fires only if kit is endgame tier):** run kit at mid-game gear tier; confirm KPM > 0 and no degenerate state. This is NOT a KPM-in-band requirement at mid-game — it is a zero-damage-floor detection check at lower gear tier.

### 4.4 Anchoring vs empirical iteration call (C.4)

**Decision: DELEGATE-TO-EMPIRICAL-ITERATION on numerical targets; ANCHOR structural form.**

The initial per-node KPM medians are NOT pre-imposed numerical values. They are computed from first-cycle sim output during Wave 4 execution. The ±15% KPM band is anchored as the starting tolerance; the medians around which the band applies are substrate-led (whatever the engine generates + validates in the first pass IS the reference population).

**What IS anchored now:**
- Band shape: flat ±15% (per-cohort modifiers as above)
- Survival floor: 80% general / 95% defensive
- Degenerate-state gate: compound 3-criterion check
- Cross-node degenerate-state secondary check rule

**What is EMPIRICAL-ITERATION:**
- Actual KPM medians per cell per node (computed Wave 4)
- Whether ±15% is right or needs widening/tightening (validated post first-cycle)
- Specific percentile thresholds (85th / 40th / 10th / 65th) per cohort — these are starting estimates, calibrated to first-cycle output

### 4.5 WR-bracket definition (C.2)

**ANCHOR (PRE-BASELINE-RESOLVABLE):**

The WR-bracket is the 3-criterion compound gate per Verdict C.2:

```
WR_BRACKET_PASS = 
    KPM_IN_BAND  (per § 4.1)
    AND SURVIVAL_FLOOR  (per § 4.1)
    AND NOT DEGENERATE_STATE  (per § 6.3)
```

All three criteria must pass per T4 configuration per progression node per cohort. Per Q10 amendment: all characters that pass WR_BRACKET constitute the season's content — substrate-led N.

**Cross-cell consistency:** each cell uses its own per-cell KPM median as the band anchor. No cross-cell normalization in the WR-bracket definition. Two cells at the same progression node can have different KPM medians (a high proxy-density cell may require more kills-per-minute than a low proxy-density cell) — this is architecturally correct, not a consistency problem.

**WR-bracket FAIL disposition (per gandalf Q10 amendment + Verdict A.6 Option F):**
- Kit fails WR-bracket at T4-A → retry T4 generation (3 attempts max)
- After 3 retries, ship kit with partial-T4 (in-band subset) IF at least 1 T4 passes WR-bracket
- If 0 T4s pass WR-bracket after retries → kit REJECTED from season
- Regeneration rate tracked as quality metric per D85

### 4.6 #18.2 timing classification for § 4

| Item | Classification |
|---|---|
| IN-BAND compound gate structure (3-criterion) | PRE-BASELINE-RESOLVABLE |
| Starting band ±15% KPM variance | PRE-BASELINE-RESOLVABLE |
| Flat-band-per-node banding shape | PRE-BASELINE-RESOLVABLE |
| Per-cohort band modifiers | PRE-BASELINE-RESOLVABLE |
| Cross-node validation rule | PRE-BASELINE-RESOLVABLE |
| WR-bracket 3-criterion structure | PRE-BASELINE-RESOLVABLE |
| WR-bracket FAIL disposition + retry logic | PRE-BASELINE-RESOLVABLE |
| Actual per-cell KPM medians | REQUIRES-WAVE-3-BASELINE |
| Band widening/tightening calibration (is ±15% right?) | REQUIRES-WAVE-3-BASELINE |
| Gradient banding (cell-type-dependent) | REQUIRES-WAVE-3-BASELINE |
| Percentile anchoring per cohort (85th / 40th / etc.) | REQUIRES-WAVE-3-BASELINE |

---

## § 5 — Compute discipline (D62 + Discipline #1.1)

### 5.1 Stratified sampling design

**Strata definition:** `(BC-cell) × (cohort) × (progression-node) × (T4-configuration)`

Each stratum is one validation instance. The strata are NOT exhaustive — the sampling strategy determines which strata are populated.

**Primary sampling rule (Sub-option A legendaries):**
- For each tier-2 legendary/set weapon: 4 strata (one per cohort) × 4 nodes = 16 validation instances per legendary per T4-attunement path
- For a legendary with 2 T4-attunements (tier-2): 32 validation instances

**Fallback sampling rule (Sub-option B legendaries):**
- For each cohort-clear legendary: 1 stratum (dominant cohort) × 4 nodes = 4 validation instances per legendary

**Statistical floor per stratum:**
- Minimum 30 fights per stratum (consistent with existing GAUNTLET_FIGHTS_PER_MATCHUP=100 upper bound; use 30 as quick-estimate floor)
- Full-sim stratum: 100 fights (matches existing constant)

### 5.2 Tiered validation (quick-estimate first)

**Tier 1 — Quick-estimate filter (RECOMPOSE_QUICK_ITERS=10 analogy):**
- Run 10-fight mini-gauntlet per stratum
- If KPM is clearly out-of-band (>30% outside ±15% band) → reject stratum immediately; flag for T4 retry
- If KPM is clearly in-band (within ±5% of cell median) → provisional pass; move to Tier 2 confirmation
- If KPM is borderline (within ±5-20% of cell median) → Tier 2 full confirmation required

**Tier 2 — Full stratum validation:**
- 100 fights per stratum
- All 3 compound gate criteria evaluated
- Degenerate-state validators run (§ 6.3)

**Cost savings:** quick-estimate filter eliminates ~60-70% of failed strata at Tier 1 cost (10 fights vs 100 = 10x reduction on rejects). This is the primary compute-burden management lever.

### 5.3 Caching strategy

**What caches:**
- Per-cell KPM medians: computed once per Phase 3 wave; reused across all stratum evaluations in that wave
- Per-cohort stat-sheet parameterizations: pre-built at Wave 4 start; reused across all legendary evaluations
- Encounter sets per progression-node: pre-generated once; all strata within a node use the same encounter set

**Invalidation rules:**
- Per-cell KPM median cache: invalidated if stat-sheet partition design changes (any Wave 1 amendment that affects modifier magnitudes)
- Cohort parameterization cache: invalidated if cohort definitions change (this document is the anchor; changes here invalidate)
- Encounter set cache: invalidated if playability gate thresholds change

**No cross-seed caching:** per Discipline #3, parallel regens of the same seed are prohibited. Cache invalidation per seed run is automatic.

### 5.4 Compute budget projection (Discipline #1.1 pre-fire resource-bounds projection)

**Host:** M2 8GB (from AGENT_STATE.md — "Gamora seam ready on M2 8GB").
**Available RAM for sim:** 62.5% × 8GB = 5.0 GB (per Discipline #1.1 threshold).

**Per-fight runtime baseline (from engineering-disciplines.md § 2):**
- Smoke: ~51s for 5 classes × 30 fights = 0.34s per fight-eval
- Full regen: ~10 minutes total for full convergence pass (~600s)

**Stratum-level compute projection:**

Assumptions for Wave 4 first-season scope:
- Target BC cells: ~22 cells (per v1-bc-target-intent-2026-05-24.md "~22 cells" in 5-tuple BC-target subspace)
- Tier-2 legendaries: unknown pre-Wave-4; estimated 15-30 tier-2 legendaries/sets for first season (substrate-led per Q10)
- Sub-option A legendaries (ambiguous): assume 50% = 8-15 legendaries → 4 cohort × 4 nodes × 2 T4-avg = 128-240 strata each → 32 Tier-2 fights each = ~4,096-7,680 fights for Sub-option A pool
- Sub-option B legendaries (cohort-clear): assume 50% = 8-15 legendaries → 1 cohort × 4 nodes × 2 T4-avg = 8 strata each → 100 Tier-2 fights = ~6,400-12,000 fights for Sub-option B pool
- Quick-estimate filter (Tier 1): 10 fights × all strata before Tier 2 fires = roughly 1/3 of Tier 2 volume (most strata proceed to Tier 2 from Tier 1 borderline; rejected strata save cost)

**Total fight estimate:**
- Tier 1 quick-estimate: ~(128-240 + 8) strata × 10 fights = 1,360-2,480 fights
- Tier 2 full-sim: ~(128-240 + 8) strata × 100 fights × 0.7 pass-rate (30% rejected at Tier 1) = 9,520-17,360 fights
- **Total: approximately 11,000-20,000 fights for first-season Wave 4**

At 0.34s per fight: **~1.0-1.9 hours wall-clock for full Wave 4 sim cycling** (sequential). Within the framing brief estimate of "3-7 days wall-clock for Wave 4" — this suggests parallelism OR additional validation layers are expected.

**Peak memory projection (Discipline #1.1):**

The fight engine runs sequentially (no parallel sim per Discipline #3 for same seed). Memory per fight: CombatantState × 2 (player + monster) + fight log + damage resolver working set. Estimate:
- CombatantState: ~5-10KB per combatant (dataclass with numeric fields, skill lists)
- Fight log: ~50-100KB per fight (event stream)
- Working set per fight: <1MB
- Total peak for a single fight: < 5MB
- Stratum-level peak (100 fights sequential): < 5MB (fights are sequential; memory not cumulative)

**Peak memory: < 5MB for sequential fight execution.** Well within 5GB limit. NO memory concern flagged for sequential fight sim.

**CAVEAT on memory bound:** if Wave 4 implementation introduces parallelism (e.g., multiprocessing per stratum), the memory scales with parallelism factor. At P parallel processes: P × 5MB per-fight working set + shared caches. At P=50 (aggressive): ~250MB + caches — still within 5GB. Memory is NOT the binding constraint. **Wall-clock is the binding constraint** at 1-2 hours for 11-20K fights sequential.

**Compute budget verdict:** WITHIN AVAILABLE RESOURCE. No Matt creative ratification required on compute scope for first-season Wave 4 sizing.

**If scope expands (more legendaries, more cells):** the scaling is linear in strata count. At 2× legendaries (30-60 tier-2), compute doubles to 2-4 hours. Still within single-session tolerance. Flag if legendary count exceeds 60 (rare at first season; more likely at Cycle 14+ expansion).

### 5.5 #18.2 timing classification for § 5

| Item | Classification |
|---|---|
| Strata definition structure | PRE-BASELINE-RESOLVABLE |
| Sub-option A / B stratum sizing logic | PRE-BASELINE-RESOLVABLE |
| Tiered validation (quick-estimate Tier 1 + full Tier 2) | PRE-BASELINE-RESOLVABLE |
| 10-fight Tier 1 / 100-fight Tier 2 fight counts | PRE-BASELINE-RESOLVABLE (starting estimate) |
| Caching strategy structure + invalidation rules | PRE-BASELINE-RESOLVABLE |
| Compute budget projection: ~11-20K fights / ~1-2 hours / <5MB peak memory | PRE-BASELINE-RESOLVABLE |
| Actual legend count (inputs to strata count) | REQUIRES-WAVE-3-BASELINE (depends on spec-driven gear gen output) |
| Whether Tier 1 fight count (10) is sufficient or needs increase | REQUIRES-WAVE-3-BASELINE (calibrate from first-cycle Tier 1 rejection rate) |

---

## § 6 — Playability gate operationalization (Discipline #26)

Per Discipline #26, PLAYABLE-AND-IN-BAND has 6 sub-gates. This section specifies what the sim measures and what threshold passes/fails for each.

### 6.1 Six sub-gate definitions

**Sub-gate 1: KPM in target band**

- **What sim measures:** kills per minute against the standard encounter set for the kit's progression node, averaged over 100 fights (Tier 2)
- **Pass threshold:** measured KPM within ±15% of per-cell median KPM for the applicable cohort (with cohort-band modifiers from § 4.2)
- **Fail trigger:** KPM outside the band → WR-bracket criterion (a) FAIL
- **Quick-estimate proxy:** 10-fight KPM estimate (Tier 1) flags obvious failures

**Sub-gate 2: Coherent skill rotation**

- **What sim measures:** mandatory-skill-lock fraction — percentage of damage output attributable to a single skill across 100 fights
- **Pass threshold:** no single skill > 80% of total damage output (per Verdict D.4 mandatory-skill-lock detector threshold)
- **Fail trigger:** any skill > 80% of damage → mandatory-skill-lock flagged → degenerate-state criterion (c) FAIL
- **Implementation note:** this requires damage-attribution tracking per skill in fight log. Current `fight_engine.py` emits per-hit events — damage attribution aggregation is a post-fight computation on the existing fight log. No new fight engine changes required; post-fight analysis is new.

**Sub-gate 3: Resource flow functional**

- **What sim measures:** resource-depletion events (mana/energy reaching 0 with skills queued but no resource to cast them) across 100 fights; separately, trivial-infinite-generation rate (resource stays at cap without any cost pressure)
- **Pass threshold:**
  - Depletion-lock rate: < 10% of fight duration spent in resource-locked state (cannot cast any skill)
  - Infinite-generation rate: no fight where resource never dips below 80% cap (trivial generation = no cost pressure)
- **Fail trigger:** depletion-lock > 10% OR infinite-generation detected → playability sub-gate 3 FAIL (does NOT immediately trigger WR-bracket FAIL; surfaces as playability warning for first cycle; escalates to FAIL if consistent across >50% of fights)
- **Note on "escalates to FAIL":** for first cycle, resource-flow failures are WARNINGS not hard blocks. The threshold for hard-blocking will be calibrated from first-cycle data. This is a REQUIRES-WAVE-3-BASELINE calibration.

**Sub-gate 4: Defensive uptime adequate**

- **What sim measures:** character death rate per fight within the standard encounter set
- **Pass threshold:**
  - General: survival rate ≥ 80% of test encounters (≥ 80% of fights: character does not die)
  - Defensive cohort: ≥ 95% survival rate
  - DPS-min-maxer cohort: ≥ 50% survival rate (intentional fragility; below 50% is degenerate)
- **Fail trigger:** below cohort-specific threshold → survival-floor criterion (b) FAIL

**Sub-gate 5: No degenerate states**

Three explicit validators (per Verdict D.4 hybrid approach):

**Validator 1 — Stunlock-loop detector:**
- **What sim measures:** maximum consecutive stun duration for character OR enemy per fight (tracked in fight_engine event stream)
- **Pass threshold:** no stun loop > 5 seconds of game-time
- **Fail trigger:** stun loop > 5 seconds → degenerate-state criterion (c) FAIL immediately

**Validator 2 — Zero-damage-floor detector:**
- **What sim measures:** total damage dealt by character vs total enemy HP across fight
- **Pass threshold:** character deals ≥ 1% of enemy HP within first 30 seconds of fight (can eventually kill)
- **Fail trigger:** < 1% damage in 30 seconds → zero-damage-floor detected → degenerate-state criterion (c) FAIL
- **Relationship to KPM:** zero-damage-floor manifests as KPM ≈ 0 in Sub-gate 1; this validator confirms the ROOT CAUSE is damage floor (vs timeout for other reasons)

**Validator 3 — Mandatory-skill-lock detector:**
- Same as Sub-gate 2 above (> 80% single-skill damage share). Listed here as the third degenerate-state validator per Verdict D.4.

**Degenerate-state detection order:** KPM-out-of-band (Sub-gate 1) is the PRIMARY signal. Validators 1-3 fire as SECONDARY when Sub-gate 1 signals anomaly. Exception: stunlock can occur even when KPM is nominally in-band (if the stunlock affects enemy movement but not kill rate) — stunlock detector fires on ALL fights, not only KPM-anomaly flights.

**Sub-gate 6: Cognitive load manageable**

- **What sim measures:** simultaneous trigger events per second during peak combat (burst of triggered-passives, skill procs, on-hit effects all firing within the same 0.5-second window)
- **Pass threshold:** maximum simultaneous-trigger burst ≤ 8 distinct events within any 0.5-second window
- **Fail trigger:** burst > 8 events → cognitive-load WARNING (not hard block at first cycle; escalates if consistent)
- **Note:** cognitive load is difficult to sim-measure precisely (it's ultimately a player-perception metric). The burst-event count is a proxy. For Wave 4 first cycle: treat as WARNING only; hard threshold calibration is REQUIRES-WAVE-3-BASELINE.
- **Implementation note:** requires counting distinct simultaneous trigger events in fight_engine event stream. Existing event emission infrastructure supports this.

### 6.2 Composition with WR-bracket

The WR-bracket compound gate composes with the playability gate as follows:

```
WR_BRACKET_PASS = 
    (Sub-gate 1: KPM_IN_BAND)
    AND (Sub-gate 4: SURVIVAL_FLOOR)
    AND (Sub-gate 5: NOT DEGENERATE_STATE)

PLAYABILITY_PASS = 
    WR_BRACKET_PASS
    AND (Sub-gate 2: COHERENT_ROTATION)
    AND (Sub-gate 3: RESOURCE_FLOW)
    AND (Sub-gate 6: COGNITIVE_LOAD)
```

**Archive insertion gate (Phase 4):**
- `WR_BRACKET_PASS AND PLAYABILITY_PASS` → ACCEPTED into archive (kit ships in season)
- `WR_BRACKET_PASS AND NOT PLAYABILITY_PASS` (sub-gates 2/3/6 fail) → QUARANTINED for Wave 5 review; may still ship with warning annotation if playability failure is mild (sub-gate 3/6 WARNING-level)
- `NOT WR_BRACKET_PASS` → REJECTED; T4 retry or kit rejection per Option F

For first cycle: sub-gates 2, 3, and 6 that produce WARNINGS do not block archive insertion. Sub-gate 2 (mandatory-skill-lock > 80%) and Sub-gate 5 (stunlock / zero-damage-floor) are HARD blocks. Sub-gates 3 and 6 are soft blocks for first cycle, calibrated to hard blocks post-Wave-3-baseline.

### 6.3 Degenerate-state detection specification (Verdict D.4 composition)

The 3 validators above (§ 6.1 Sub-gate 5) are the gamora-operationalized implementation of Verdict D.4's "hybrid KPM-proxy + 3 validators" recommendation. They apply at Tier 2 (full-sim stratum). Tier 1 (quick-estimate) uses KPM-proxy only — degenerate-state validators require sufficient fight count to be reliable.

**Detection priority:**
1. Zero-damage-floor (fastest to detect; 1% damage in 30 seconds is apparent in Tier 1 10-fight run)
2. Stunlock-loop (needs fight-log event tracking; fires at all tiers)
3. Mandatory-skill-lock (requires damage attribution across full fight; Tier 2 only)

### 6.4 #18.2 timing classification for § 6

| Item | Classification |
|---|---|
| 6 sub-gate structure + measurement approach | PRE-BASELINE-RESOLVABLE |
| KPM band threshold (Sub-gate 1: ±15%) | PRE-BASELINE-RESOLVABLE (anchored; calibration is wave-3-baseline) |
| Mandatory-skill-lock threshold (Sub-gate 2: >80%) | PRE-BASELINE-RESOLVABLE |
| Survival floors (Sub-gate 4: 80% / 95% / 50%) | PRE-BASELINE-RESOLVABLE |
| Stunlock threshold (Sub-gate 5 validator 1: >5 sec) | PRE-BASELINE-RESOLVABLE |
| Zero-damage-floor threshold (Sub-gate 5 validator 2: <1% in 30s) | PRE-BASELINE-RESOLVABLE |
| Resource-flow depletion-lock threshold (Sub-gate 3: 10%) | PRE-BASELINE-RESOLVABLE (starting estimate) |
| Cognitive-load burst threshold (Sub-gate 6: ≤8 events / 0.5s) | PRE-BASELINE-RESOLVABLE (starting estimate) |
| Sub-gate 3 / 6 WARNING → HARD-BLOCK escalation calibration | REQUIRES-WAVE-3-BASELINE |
| Archive insertion quarantine policy calibration | REQUIRES-WAVE-3-BASELINE |
| Actual cohort-specific survival floor calibration for defensive cohort | REQUIRES-WAVE-3-BASELINE |

---

## § 7 — Pre-baseline vs post-baseline classification (Discipline #18.2) — consolidated

### 7.1 PRE-BASELINE-RESOLVABLE (total: 22 items)

These items are designed now and executable without Wave 3 baseline data. They constitute the complete Wave 4 methodology framework ready to execute post-Wave-3 close.

| Section | Item |
|---|---|
| § 2 | Sub-option A/B/hybrid discrimination heuristic |
| § 2 | Per-legendary cohort anchoring procedural spec |
| § 2 | Tier-0/0.5 validation priority order |
| § 3 | 4 cohort identities + qualitative definitions (from C.3) |
| § 3 | DPS-min-maxer KPM band (85th–100th percentile) starting estimate |
| § 3 | Balanced KPM band (40th–65th percentile) starting estimate |
| § 3 | Defensive KPM band (10th–30th percentile) starting estimate |
| § 3 | Hybrid KPM band (60th–85th percentile; high variance) starting estimate |
| § 4 | IN-BAND compound gate 3-criterion structure |
| § 4 | Starting band ±15% KPM variance |
| § 4 | Flat-band-per-node banding shape + per-cohort modifiers |
| § 4 | Cross-node validation rule + degenerate-state secondary check |
| § 4 | WR-bracket 3-criterion structure + FAIL disposition |
| § 5 | Strata definition structure |
| § 5 | Sub-option A/B stratum sizing logic |
| § 5 | Tiered validation (Tier 1 quick-estimate + Tier 2 full-sim) |
| § 5 | Fight counts (10-fight Tier 1 / 100-fight Tier 2) |
| § 5 | Caching strategy structure + invalidation rules |
| § 5 | Compute budget projection (~11-20K fights, ~1-2 hrs, <5MB peak) |
| § 6 | 6 sub-gate structure + measurement approach |
| § 6 | Hard-block thresholds (sub-gates 1, 2, 4, 5) |
| § 6 | Starting estimates for soft-block thresholds (sub-gates 3, 6) |

### 7.2 REQUIRES-WAVE-3-BASELINE (total: 12 items)

These items cannot be finalized without Wave 3 empirical output. They are explicitly flagged for post-Wave-3 methodology consultation closure.

| Section | Item | Empirical criterion needed |
|---|---|---|
| § 2 | Cohort-clear fraction of actual generated legendaries | Spec-driven gear gen output from Wave 3/4 |
| § 3 | DPS-min-maxer / DPS-survivor split decision | Bimodal survival signal in DPS-min-maxer cohort |
| § 3 | Per-cell KPM percentile calibration (actual numbers) | Phase 3 Wave 3 sim execution against new engine |
| § 3 | Cohort membership of actual generated legendaries | Spec-driven gear gen output |
| § 4 | Actual per-cell KPM medians | Phase 3 Wave 3 sim execution |
| § 4 | Band widening/tightening calibration (is ±15% right?) | First-cycle WR-bracket pass rate |
| § 4 | Gradient banding (cell-type-dependent variance) | Cell-type KPM variance distribution from Wave 3 |
| § 4 | Percentile anchoring per cohort calibration | Wave 3 cohort-distribution empirical signal |
| § 5 | Actual legendary count (strata sizing input) | Spec-driven gear gen output |
| § 5 | Tier 1 fight count sufficiency (is 10 enough?) | First-cycle Tier 1 rejection rate |
| § 6 | Sub-gate 3/6 WARNING → HARD-BLOCK escalation | First-cycle resource-flow + cognitive-load signal |
| § 6 | Archive insertion quarantine policy calibration | First-cycle quarantine rate |

---

## § 8 — Open questions surfaced

1. **Damage attribution per skill in fight_engine.py:** Sub-gate 2 (mandatory-skill-lock) requires per-skill damage attribution tracking in the fight log. Current fight log emits per-hit events — the aggregation is computable from existing events, but requires a post-fight attribution pass. This is an implementation scope item for gamora Wave 4 code. **NOT blocking methodology; design is complete.**

2. **Stun-duration tracking in fight_engine.py:** Sub-gate 5 validator 1 (stunlock-loop) requires tracking consecutive stun duration in the fight event stream. Current fight engine likely emits status-effect events but may not compute continuous-stun-duration. Requires audit of existing `effect_resolver.py` before Wave 4 implementation. **NOT blocking methodology; pre-implementation audit flagged.**

3. **Multi-T4 archive entry format (Phase 4):** archive insertion per D84 requires multi-T4 archive entries (one per attuned-T4 configuration per cell per cohort). Current archive insertion math gates operate on kit + substrate + 8-axis BC coordinate. Extension to multi-T4 entries requires schema design. **Pre-existing gap in Phase 4; gamora owns this Wave 4 extension. Out of scope for methodology framework; flagged for Wave 4 implementation dispatch.**

4. **Tier-2 legendary count dependency:** the compute budget projection depends on actual tier-2 legendary count from spec-driven gear gen (Wave 3/4). If the count significantly exceeds 30 (e.g., 80+ for a full season), the compute budget scales proportionally. At 80 legendaries: ~50-80K fights, ~5-8 hours wall-clock — still within single-day tolerance but warrants flag. **Flagged for Knight-rider attention when spec-driven gear gen output size is known.**

5. **Simultaneous fight parallelism (not same-seed):** Discipline #3 prohibits parallel regens of the SAME SEED. Wave 4 sim is not a season regen — it is a targeted validation of specific configurations. It MAY be possible to parallelize across DIFFERENT legendary configurations (different "seeds" in the convergence sense) using Python multiprocessing. **This is a compute-optimization question for Wave 4 implementation; methodology framework does not depend on it.**

---

## Sign-off

**Author:** gamora (simulation + spirit-guide seam owner)
**Pattern:** Pattern A-deep methodology framework (per Discipline #30 explicit naming + Discipline #18.2 PREP timing classification)
**Discipline composition:** #1.1 (resource-bounds projection) + #18 (methodology-before-execution) + #18.2 (timing classification at extension hotspot) + #19.1 (cheapest-refuting-test per claim) + #23 (framing-audit, applied implicitly throughout) + #26 (playability PLAYABLE-AND-IN-BAND) + #30 (sim methodology naming)
**Authority basis:** Matt Q6 ratification + gandalf C.1/C.2/C.3 DELEGATE-TO-GAMORA + hive-mind decision-routing directive
**Downstream:** this framework is the Wave 4 dispatch input for gamora sim execution; jack-ryan Gate-1 review expected at Wave 4 dispatch authoring; knight-rider consumes for Wave 4 scheduling
