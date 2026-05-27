# Gandalf Verdict — `OMEGA_PENALTY` value for Wave 0.5 hybrid damage routing

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward; sub-agent invocation by knight-rider)
**Mode:** Pattern A-deep (Pattern-A query routed per hive-mind decision-routing directive Matt 2026-05-23; file-output requested in invocation)
**Authority basis:** Matt 2026-05-27 Q1-Q11 RATIFIED (Cycle 14 framing brief); KR routes substrate-design Pattern-A query to seam-owner; gamora seam-of-record raised Q-W05-G1 deferred to gandalf.
**Anchor docs cited:**
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 3.3 (Option C rationale + ω-field resource-dimension citation)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` § 1.1 (ω-field definition; resource-dimension scoring)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.4 (hybrid damage calculation with `dmg *= OMEGA_PENALTY` reference)
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` § 2.3 + § 3.3 + § 6 R6 (SC-5 genre-canon coverage for hybrid cross-attribute)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wave-0-5-damage-routing-math-2026-05-27.md` § 7 (gamora's provisional 0.80 + rationale)

---

## 0. TL;DR — VERDICT

**CONFIRM `OMEGA_PENALTY = 0.80` as the locked Wave 0.5 value**, with three load-bearing additions:

1. **Rename to `OMEGA_CROSS_ATTRIBUTE_PENALTY` in code.** Bare `OMEGA_PENALTY` collides with the canonical ω-field name and risks semantic drift in future readers. The constant is *one specific application* of the ω-field resource-dimension; it is not the ω-field itself. Naming clarity prevents the load-bearing canonical concept from being silently overwritten by an engine constant.

2. **Constrain scope: applies ONLY to `magical_with_martial_weapon` and `sum_paths` hybrid patterns.** `physical_with_element_flavor` is a physical-path skill with element flavor; it is NOT a cross-attribute wielding case and must NOT receive the penalty. Gamora's math note already implements it this way (only Patterns B and C check `is_cross_attribute_wielding`); this verdict locks that scope to prevent future drift.

3. **Empirical-evidence criterion for re-engagement is named** (per gandalf OP § 3.4 recognition-validate-commit; per OP § 3.5 substitute pattern): Wave 4 (gear cohesion + D21 acquisition curve calibration) is the gate where empirical signal from real hybrid-cell content firing at scale informs whether 0.80 holds, needs softening (0.85), or needs sharpening (0.75 / variable-by-archetype). 0.80 is the **locked Wave-0.5 value**, NOT a permanent canonical commitment.

**Sequencing impact: DOES NOT GATE Wave 0.5 close, DOES NOT GATE Wave 5 fresh-roster gauntlet sim.** 0.80 is the locked starting value; empirical re-evaluation is queued for post-Wave-4. Wave 5 fires against locked 0.80.

**Anti-pattern guarded against:** Wave 5 fresh-roster gauntlet sim against a *flagged-provisional* placeholder is worse than firing against a *locked* value with a queued empirical-evaluation gate. Locking is the discipline; the empirical gate is the relief valve.

---

## 1. Question-by-question reasoning

### 1.1 What is ω in the canonical?

Per `bdi-omega-tau-tables-v1-2026-05-22.md` § 1.1 (the canonical source for the ω-field):

> ω is computed as a weighted average across the five dimensions (uniform weight 0.2 each in v1; H2 hypothesis test result may motivate per-dimension reweighting in v2). Each dimension scores 0.0 (no overlap), 0.5 (partial overlap), or 1.0 (full overlap).

The five dimensions are: geometry, tempo, range, **resource (scaling-attribute)**, effect-category. The resource dimension is the one that fires here:

> Pairs that share the scaling-attribute have automatic 1.0 resource-dimension overlap; cross-attribute pairs have 0.0 resource-dimension overlap (unless mixed-resource bridge substrate present).

Per `weapon-substrate-composition-policy-v1-2026-05-24.md` § 3.3:

> Substrate-binding rule: cross-attribute wielding permitted with ω-penalty per BDI ω-field resource-dimension (**0.0 cross vs 1.0 same-attribute**)

**Critical semantic distinction:** ω is an *overlap score* (canonical: high ω = more aligned = "better"). The damage-multiplier `OMEGA_PENALTY` in `damage_resolver.py` is a *damage scaling factor* (engineering: high value = less penalty = "better"). These run in opposite directions semantically. Gamora's collapsed mapping is:

| Wielding | ω_resource | Damage multiplier (gamora's mapping) |
|---|---|---|
| Same-attribute (e.g., INT skill on caster wand) | 1.0 | 1.0 (no penalty; doesn't fire) |
| Cross-attribute (e.g., INT skill on martial sword in Cell 15 Red Mage / Holy Knight) | 0.0 | 0.80 (20% damage reduction) |

The mapping is correct in shape: ω_resource=1.0 → multiplier=1.0; ω_resource=0.0 → multiplier=0.80. The mapping is a binary collapse of a [0, 1] field (the BDI ω allows partial overlap = 0.5; gamora's `is_cross_attribute_wielding` returns boolean). This is acceptable for v1 — partial-overlap "bridge substrate" is a v1.1+ refinement when the BDI ω/τ tables recalibrate per `legacy-categorical-cleanup-audit-2026-05-22.md` § "Recalibrate ω/τ tables under role_orientation drop."

### 1.2 Does the canonical lock a specific damage-multiplier value?

**No.** The canonical anchors lock:
- The *existence* of the ω-penalty (composition policy v1 § 3.3)
- The *semantic source* (BDI ω-field resource dimension)
- The *binary endpoints* (0.0 cross vs 1.0 same-attribute)

The canonical does NOT lock the conversion function from ω_resource to damage-multiplier. That conversion is engine-implementation territory.

This is the right canonical division. Locking a magnitude in canonical would couple design-intent to a tunable parameter that should respond to empirical sim evidence. The composition policy's silence on magnitude is correct.

### 1.3 What does SC-5 genre-canon say about hybrid cross-attribute penalties?

Per `2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` § 2.3 + § 3.3 + § 6 R6:

> **Pattern 2 (magical_with_martial_weapon):** PoE's Battlemage keystone applies intelligence to attacks; various intelligence-scaled builds use martial weapons with spell-scaling overlays. GD's Arcanist/Soldier hybrid uses STR/Cunning to boost physical component while Spirit boosts magical component. CONFIRMED genre pattern.

And § 3.3 on the "hybrid tax":

> If balance_factor = 0.5 and physical_path outputs X while magical_path outputs Y, the total is 0.5X + 0.5Y. This is NOT the same as running either path at 100%. The player who invests heavily in `+%physical damage` for a hybrid skill only benefits from the 50% physical component — the investment efficiency halves. **This is the "hybrid tax" pattern — genre-canonical** (see Lost Ark's identity skills that scale poorly with stat optimization, or PoE's hybrid-damage gems that resist perfect optimization). The ω-penalty for Option C cells already addresses this architecturally.

**SC-5 surface: no specific community-canonical magnitude is named.** Genre games handle hybrid cross-attribute via:
- PoE Battlemage keystone (binary unlock; no flat multiplier)
- GD Arcanist/Soldier hybrid (independent component scaling; no flat multiplier)
- Lost Ark identity skills (poor stat-optimization scaling; emergent ~20-40% optimization penalty)
- D2 has no formal hybrid cross-attribute class (per § 1.1)

The 20% penalty (0.80) sits in the middle of the emergent-via-design penalty range that Lost Ark identity-skills produce (~20-40% loss to optimization ceiling). It is a *plausible* starting magnitude grounded in genre observation but not community-canonical lock.

### 1.4 Why 0.80 over 0.75 / 0.85 / variable-by-archetype?

**0.80 is the right starting commitment for Wave 0.5.** Reasoning:

| Candidate | Argument for | Argument against | Verdict |
|---|---|---|---|
| **0.75 (25% penalty)** | Sharper hybrid-tax; clearer build-design pressure; Lost Ark heavier emergent-penalty alignment | Risks making Option C cells (Red Mage / Holy Knight / Monk) feel weak at v1; may suppress hybrid-archetype identity emergence in Phase 5 cohesion-judge before content is shaped enough to know | Defer — would be considered if 0.80 produces "hybrid feels too strong" empirical signal at Wave 4 |
| **0.80 (20% penalty)** ✅ | Matches gamora's provisional choice grounded in "20% penalty" framing per ω-field's "0.0 vs 1.0" binary; sits at middle of emergent genre-penalty range (~20-40%); preserves Option C archetype viability while signaling cross-attribute is non-optimal; meaningful but not crippling | None substantial for v1 starting value | **CONFIRM** |
| **0.85 (15% penalty)** | Softer; preserves hybrid archetype identity strongly; closer to "no penalty" | Risks making cross-attribute wielding *equivalent* to same-attribute wielding; defeats the architectural purpose of Option C (which is that cross-attribute is *permitted but penalized*); collapses the 0.0/1.0 ω-resource distinction toward 1.0 | Defer — would be considered if 0.80 produces "hybrid feels punishingly weak" empirical signal at Wave 4 |
| **Variable-by-archetype** (e.g., 0.85 Red Mage / 0.80 Holy Knight / 0.75 Monk) | Per-cell tuning matches the cohesion-judge per-cell design philosophy | Premature optimization; no empirical signal yet to inform per-cell calibration; adds implementation complexity without v1 justification; couples ω-penalty to cell identity in ways that resist future refactoring | Defer — v1.1+ refinement when per-cell empirical data exists |
| **Tied to BDI ω-field directly (multiplier = ω_resource + (1 - ω_resource) × 0.80)** | Most canonically clean; ω_resource=0.5 (partial overlap) gives multiplier=0.90; ω_resource=0.0 gives 0.80; ω_resource=1.0 gives 1.0 | Requires `is_cross_attribute_wielding` to return ω_resource score, not boolean; "bridge substrate" detection not yet implemented; defers complexity to v1.1+ when BDI recalibration lands | Defer — captured as v1.1+ refinement; gamora's binary collapse is acceptable v1 simplification |

### 1.5 Does this gate Wave 0.5 close or Wave 5 fresh-roster gauntlet sim?

**No.** The verdict is:
- Wave 0.5 close gate (synthetic_mode retirement + damage routing existence) is independent of OMEGA_PENALTY magnitude.
- Wave 5 fresh-roster gauntlet sim against real content fires with locked 0.80.
- Wave 4 (gear cohesion + D21 acquisition curve calibration) is the natural empirical-evaluation gate — at that wave, hybrid-cell skills will be exercised at scale against real cohort-band KPM and the calibration question becomes data-informed.

**Sequencing rationale (per hive-mind discipline + Discipline #18 refinement gandalf OP § 4.2):**
The OMEGA_PENALTY is an *extension* of the damage-routing baseline. The locked baseline must fire first to produce empirical signal that informs per-archetype magnitudes. Calibrating OMEGA_PENALTY before baseline is consultation-in-the-dark; calibrating it after Wave 4 lands is consultation against signal.

---

## 2. Load-bearing additions / dissents from gamora's framing

### 2.1 Naming refinement — `OMEGA_CROSS_ATTRIBUTE_PENALTY` over bare `OMEGA_PENALTY`

**Issue:** `OMEGA_PENALTY` as a bare constant collides with the canonical ω-field name. The ω-field is a load-bearing canonical concept (BDI ω/τ tables; gear-substrate rule table § 8 BDI ω-alignment; skill-system § 5 ω-field operationalization at tree-adjacency). The constant in `damage_resolver.py` is *one specific application* of the ω-field resource-dimension to a *damage scaling factor*. Conflating the field name with the constant name will produce future-reader confusion when they search for "omega" and find a damage multiplier instead of the field itself.

**Resolution:** Rename to `OMEGA_CROSS_ATTRIBUTE_PENALTY` (or `HYBRID_CROSS_ATTRIBUTE_PENALTY`). The semantic of "cross-attribute" is what the constant codifies; "omega" merely points to the canonical-derivation chain.

**Sequencing:** gamora updates `damage_resolver.py` Wave 0.5 implementation to use the renamed constant + adds the doc-comment citation to composition policy v1 § 3.3.

### 2.2 Scope constraint — apply ONLY to Patterns B + C

Gamora's math note § 2.3 already implements scope correctly:
- Pattern A (`physical_with_element_flavor`): no penalty check (correct — physical-path skill with element flavor is not cross-attribute)
- Pattern B (`magical_with_martial_weapon`): penalty applies if cross-attribute (correct)
- Pattern C (`sum_paths`): penalty applies to the summed result if cross-attribute (correct)

**This verdict locks that scope.** Future maintainers must NOT extend OMEGA_CROSS_ATTRIBUTE_PENALTY to Pattern A or to non-hybrid paths. The penalty exists specifically because Option C cells are *cross-attribute by architecture*; it does not exist as a generalized damage modifier.

### 2.3 Bridge-substrate provision is a v1.1+ refinement

Per BDI ω/τ tables v1 § 1.1: "pairs that share the scaling-attribute have automatic 1.0 resource-dimension overlap; cross-attribute pairs have 0.0 resource-dimension overlap (**unless mixed-resource bridge substrate present**)."

The "mixed-resource bridge substrate" concept (partial-overlap ω=0.5 case) is NOT implemented in Wave 0.5. Gamora's `is_cross_attribute_wielding` returns boolean; the binary collapse is acceptable for v1.

**v1.1+ refinement (captured here for future re-engagement):** when the BDI ω/τ tables recalibrate per `legacy-categorical-cleanup-audit-2026-05-22.md` § "Recalibrate ω/τ tables under role_orientation drop," reconsider whether `is_cross_attribute_wielding` should return ω_resource score (0.0 / 0.5 / 1.0) and whether OMEGA_CROSS_ATTRIBUTE_PENALTY becomes a function `f(ω_resource) → damage_multiplier`.

### 2.4 No dissent on gamora's provisional choice

Gamora's 0.80 was reached through grounded reasoning: cited the substrate composition policy directly, recognized the "20% penalty" framing as load-bearing, flagged the deferral correctly per Discipline #1 math-before-code, and waited for gandalf confirmation before locking. This is exactly how cross-seam Pattern-A-deferred items should land. The seam discipline is correct; this verdict ratifies the engineering judgment.

---

## 3. Per-option assessment table

| Option | Magnitude | Genre-canon fit | Canonical-fidelity | v1 risk profile | Verdict |
|---|---|---|---|---|---|
| 0.75 | 25% penalty | Lost Ark identity emergent-penalty heavier end | Within canonical [0.0 cross, 1.0 same] range | Risks suppressing Option C identity at v1; sharper hybrid-tax | Defer to Wave-4-empirical re-evaluation |
| **0.80** ✅ | **20% penalty** | **Genre-emergent middle of range; matches "20%" framing implicit in 0.0/1.0 binary** | **Within canonical range; gamora's provisional commitment** | **Balanced; locked; queue empirical re-evaluation at Wave 4** | **CONFIRM** |
| 0.85 | 15% penalty | Closer to "no penalty"; soft hybrid-tax | Within canonical range but compresses 0.0/1.0 distinction | Risks collapsing Option C distinctiveness | Defer to Wave-4-empirical re-evaluation |
| Variable-by-archetype | 0.75-0.85 per cell | No genre precedent for per-archetype-tuned cross-attribute penalty | Adds canonical complexity without v1 justification | Premature optimization | Defer to v1.1+ |
| ω-tied formula | `1 - 0.20 × (1 - ω_resource)` | Cleanest canonical fidelity | Requires partial-overlap "bridge substrate" detection | Premature for v1 binary `is_cross_attribute_wielding` | Defer to v1.1+ post-BDI-recalibration |

**Tier-ranked recommendation:**
- **Tier 1 (must-fire Wave 0.5):** CONFIRM 0.80 + rename to OMEGA_CROSS_ATTRIBUTE_PENALTY + scope-lock to Patterns B + C
- **Tier 2 (queue post-Wave-4):** Empirical re-evaluation of magnitude (consider 0.75 / 0.80 / 0.85 against real hybrid-cell damage data)
- **Tier 3 (v1.1+):** Variable-by-archetype OR ω-tied formula refinement (post-BDI-recalibration)
- **Reject (do not implement):** Variable-by-archetype at v1 (premature); ω-tied formula at v1 (premature)

---

## 4. Downstream sequencing impact

### 4.1 Does this gate Wave 0.5 Gate-2 closure?

**No.** Wave 0.5 close gate per Cycle 14 framing brief Q4 is synthetic_mode retirement + damage routing existence. OMEGA_PENALTY value is implementation-detail-within-locked-routing. Gate-2 fires in parallel; 0.80 stays in code.

### 4.2 Does this gate Wave 5 fresh-roster gauntlet sim?

**No.** Wave 5 fires against locked 0.80. The fresh-roster gauntlet sim will produce empirical hybrid-cell damage data that informs the Wave-4-empirical re-evaluation gate.

### 4.3 Empirical-evidence criterion for re-engagement (per gandalf OP § 3.4 / OP § 3.5 substitute pattern)

**Re-engage on OMEGA_CROSS_ATTRIBUTE_PENALTY magnitude when:**

1. **Wave 4 (gear cohesion + D21 acquisition curve calibration) lands** AND
2. Empirical hybrid-cell damage data surfaces in any of these patterns:
   - **Pattern A (softening signal):** hybrid-cell archetypes (Red Mage / Holy Knight / Monk) consistently fail to converge to in-band KPM at Wave 5 baseline at locked 0.80 → consider relaxing to 0.85
   - **Pattern B (sharpening signal):** hybrid-cell archetypes consistently over-perform same-attribute baselines at Wave 5 in real-content gauntlet → consider tightening to 0.75
   - **Pattern C (per-archetype divergence signal):** Red Mage vs Holy Knight vs Monk produce significantly different convergence patterns at locked 0.80 → consider variable-by-archetype calibration
   - **Pattern D (no signal):** hybrid-cell archetypes converge within bounds and produce thematically appropriate damage at Wave 5 → 0.80 holds; promote from "Wave-0.5 lock" to "v1 lock"

3. Or post-BDI-recalibration (per `legacy-categorical-cleanup-audit-2026-05-22.md` queued item): when BDI ω/τ tables recalibrate per role_orientation drop, reconsider whether ω-tied formula refinement is ready to fire.

### 4.4 Out-of-scope (per invocation)

Per invocation explicit out-of-scope:
- Do NOT amend doc 47 / doc 46 / weapon-substrate-composition-policy → composition policy v1 § 3.3 is canonical lock for *semantic existence* of the penalty; the magnitude is engine-implementation territory and does NOT require canonical amendment
- Do NOT touch damage_resolver.py → KR routes Pattern-A to gamora to (a) confirm 0.80 lock, (b) rename to OMEGA_CROSS_ATTRIBUTE_PENALTY, (c) add doc-comment citation, (d) update MIGRATION.md as resolved Q-W05-G1
- No Pattern-B sustained dialogue with Matt required → verdict reachable from canonical anchors alone
- No Wave 0.5 Gate-2 closure delay → OMEGA_PENALTY is deferred-not-blocking per dispatch framing

---

## 5. Recognition record — what landed in this verdict

Per gandalf OP § 2 recognition-record mode (architectural commitment + deferred refinement):

**Commitments LOCKED at Wave 0.5:**
1. `OMEGA_CROSS_ATTRIBUTE_PENALTY = 0.80` (renamed from bare `OMEGA_PENALTY`)
2. Scope: applies to Pattern B `magical_with_martial_weapon` + Pattern C `sum_paths` only (NOT Pattern A)
3. Binary collapse of ω_resource at v1 (cross-attribute returns boolean, not score)
4. Wave 5 fresh-roster gauntlet sim fires against this locked value

**Refinements DEFERRED with empirical-evidence criteria:**
1. Wave 4 empirical re-evaluation of magnitude → criteria § 4.3 above
2. Bridge-substrate provision (partial-overlap ω_resource=0.5) → v1.1+ post-BDI-recalibration
3. Variable-by-archetype calibration → v1.1+ if Pattern C divergence signal surfaces at Wave 4
4. ω-tied formula refinement → v1.1+ post-BDI-recalibration

---

## 6. Framing-audit (per OP § 4.1 three-question protocol)

**Q1 — Load-bearing framing assumptions this verdict depends on:**
- That the canonical composition policy v1 § 3.3 + BDI ω/τ tables v1 § 1.1 are authoritative for ω-field semantic. (Confirmed; both are STATUS CURRENT canonical docs.)
- That gamora's `is_cross_attribute_wielding` boolean check correctly identifies Option C cells (Cell 15 Red Mage / Cell 23 Monk / Holy Knight per composition policy § 4.1 + § 3.3). (Per gamora math note § 7 logic; correct shape.)
- That Wave 4 empirical signal will be sufficient to inform re-evaluation. (Plausible; gear cohesion + acquisition curve calibration exercises hybrid cells at scale.)

**Q2 — Evidence that could refute these assumptions:**
- If Wave 5 surfaces that `is_cross_attribute_wielding` is firing on cases that AREN'T Option C cells (e.g., a hybrid skill on a same-attribute weapon getting penalized), the scope-lock to Patterns B + C is wrong. → Mitigation: gamora's logic in § 7 specifically checks skill_family vs weapon_family; this should not produce false positives.
- If Wave 5 produces NO hybrid-cell skills (because Cell 15 / 23 / Holy Knight content isn't ready), then OMEGA_CROSS_ATTRIBUTE_PENALTY is not exercised and Wave-4 empirical re-evaluation lacks signal. → Mitigation: this is acceptable; the value stays locked and re-evaluation defers to when hybrid content fires.
- If canonical ω/τ tables recalibrate before Wave 4 (per `legacy-categorical-cleanup-audit-2026-05-22.md` queued recalibration), the 0.0/1.0 binary may change. → Mitigation: BDI recalibration is not currently in active workstream queue; verdict captures the v1.1+ refinement path.

**Q3 — Should framing be refined before execution?**
**No.** The verdict is reachable from current canonical anchors; the empirical-evidence criterion for re-engagement is named; the scope-lock prevents drift; the renaming prevents semantic collision. Wave 0.5 fires with confidence.

---

## 7. Cross-references

### 7.1 Canonical
- `canonical/00-ground-state.md` § 1 (current truth oracle — anchors composition policy v1 + doc 47 as load-bearing)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.4 (hybrid damage with `dmg *= OMEGA_PENALTY` reference; this verdict locks the value but does NOT amend doc 47)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 3.3 (Option C ω-penalty rationale)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` § 1.1 (ω-field resource-dimension definition)

### 7.2 Operational
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` § 2.3 + § 3.3 + § 6 R6 (SC-5 genre-canon hybrid coverage)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wave-0-5-damage-routing-math-2026-05-27.md` § 7 + § 10 (gamora's provisional 0.80 + Q-W05-G1 deferred to gandalf)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` (Cycle 14 framing brief Q1-Q11 RATIFIED; Q-W05-G1 NOT in Q1-Q11 — this verdict closes a deferred sub-item)
- `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-14-wave-0-5-damage-routing-synthetic-retirement.md` (gamora's parent dispatch; Q-W05-G1 origin)

### 7.3 Decisions-log (for jack-ryan future-reference)

This verdict is engine-implementation calibration within canonical lock; per `reincarnated-decision-log-format` skill, this is **NOT a decisions-log entry candidate** — composition policy v1 § 3.3 is the canonical lock; this verdict is its v1 calibration. If Wave-4 empirical evidence surfaces a magnitude change, THAT becomes a decisions-log candidate (calibration shift = ADR-shape).

---

## 8. Sign-off

**Verdict:** **CONFIRM `OMEGA_PENALTY = 0.80`** as the locked Wave 0.5 value, with renaming to `OMEGA_CROSS_ATTRIBUTE_PENALTY` + scope-lock to Patterns B + C + empirical-evidence criterion for Wave-4 re-evaluation.

**Authority:** gandalf (story-and-design steward) — sub-agent invocation by knight-rider per hive-mind decision-routing directive Matt 2026-05-23; design-fit + canonical-fidelity assessment basis.

**Empirical-evidence criterion for re-engagement:** Wave 4 gear cohesion + D21 acquisition curve calibration + Wave 5 real-content gauntlet sim produce hybrid-cell convergence data. Re-engage on Pattern A (softening) / Pattern B (sharpening) / Pattern C (per-archetype divergence) / Pattern D (validation = no-change) signal per § 4.3.

**Out-of-scope respected:** no doc 47 / doc 46 / composition policy v1 amendment; no damage_resolver.py touch (KR routes Pattern-A to gamora for in-code update); no Wave 0.5 Gate-2 delay.

**Signed:** gandalf (story-and-design steward)
**For:** the Wave-0.5 lock of OMEGA_CROSS_ATTRIBUTE_PENALTY = 0.80 with empirical-evaluation gate at Wave 4, enabling Cycle 14 Wave 5 fresh-roster gauntlet sim to fire against real content with confidence.
