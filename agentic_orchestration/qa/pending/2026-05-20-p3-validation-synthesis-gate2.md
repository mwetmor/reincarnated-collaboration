# Gate-2 Critique — 2026-05-20 — P3 Validation Synthesis

**Reviewer:** jack-ryan
**Mode:** DEV-MODE (Gate-2, post-synthesis gatekeeper)
**Severity:** APPROVE-WITH-AMEND
**Date:** 2026-05-20
**Synthesis author:** gandalf
**Synthesis path:** `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md`
**Synthesis commit:** collab `3205d0e`; tag `gandalf/v0.4-p3-canonical-findings-synthesis`
**Protocol:** `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` § 3 P3 + § 6 P3
**Principles applied:** Review Principles 1 (completeness), 2 (technical correctness), 3 (scope), 5 (epistemic precision)
**Dispatch authority:** `agentic_orchestration/dispatches/2026-05-20-gandalf-plus-jack-ryan-p3-validation-synthesis.md` § 3.2

---

## § 0 — TL;DR + Disposition

**DISPOSITION: APPROVE-WITH-AMEND**

The synthesis is structurally sound and the CANNOT REJECT NULL verdict is correct. All major technical claims verify against the raw telemetry. The per-failure-mode disaggregation is the right level of granularity for the kit-redesign queue handoff. The single-Discipline-#11-elaboration framing is defensible and I concur. The § 10 alternatives are appropriately framed as Matt-options.

Three amendments required before knight-rider fires the verdict-handoff tag:

1. **(REQUIRED)** Recompose-attempt count: synthesis and star-lord both cite "33 recompose_attempts on 9 canonical classes" — raw telemetry (`balance_results.json`) shows **35 attempts** (class_0001=3, classes 0002-0009=4 each; total=35). The discrepancy is small but cited as a factual figure in multiple places; correct in the canonical findings doc for archival integrity.

2. **(REQUIRED)** Sub-pattern 5 nuance: class_0001's recompose outcome is `modifier_fallback` with all three attempts at delta=0 (no lever was accepted). Gandalf's synthesis maps class_0001 to sub-pattern 5 ("recompose-couldn't-recover") alongside classes 0002-0009 which had accepted lever deltas (all negative, -0.03 to -0.13). The sub-pattern 5 label is technically correct for class_0001 (recompose attempted; boss WR still 0), but the operational mechanism differs: 8/9 canonical classes exhibit "lever accepted but boss WR unchanged" (WR compression only occurs at lower tiers); class_0001 exhibits "all levers exhausted at delta=0 → modifier_fallback path." The kit-redesign queue downstream should understand this distinction. Amend § 6.1's class_0001 row to note the `modifier_fallback` path explicitly, and amend the § 6 sub-pattern 5 description to state "recompose attempted on all 9/9 canonical classes; 8/9 had at least one accepted lever (negative delta, lower-tier WR compression only, boss WR unchanged); 1/9 (class_0001) exhausted all levers at delta=0 before modifier_fallback path."

3. **(RECOMMENDED)** Substrate-generalization scope: § 7.2 nuance 2 and § 11.5 correctly state that the CANNOT REJECT NULL verdict and Option B's behavioral landing apply to "this season." The synthesis is clean on this point in the body, but the § 0 TL;DR opens with "100% Pattern-A, 100% kit-broken" without a substrate-scope qualifier visible to a reader who reads only the TL;DR. Add a single parenthetical: "(on shadow substrate, seed=100005, under disposition-3 calibration)" to the § 0 aggregate figure summary. This is advisory for the Matt briefing; a reader arriving cold needs to see the scope boundary in the first paragraph.

None of these block the verdict. APPROVE-WITH-AMEND with amendments 1-2 required before tag fires; amendment 3 advisory for knight-rider to fold into the Matt briefing if not in the findings doc.

---

## § 1 — Required Reading Absorbed

All nine primary documents read in full:

1. Hive log — all 1,380 lines through the knight-rider HANDOFF routing jack-ryan for Gate-2
2. Synthesis doc (`per-tier-recompose-validation-findings-2026-05-19.md`) — all 12 sections
3. Star-lord P3 analysis (`p2-classification-and-floor-lock-analysis.md`) — all 9 sections
4. Raw telemetry (`balance_results.json`) — full JSON; all 10 per_class entries + recompose_attempts arrays verified via Python
5. Scope-of-work (`scope-of-work-recompose-validation.md`) §§ 0-2 — mission + H_RC hypothesis + PASS thresholds
6. Protocol (`hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md`) §§ 3 + 6 P3 + § 7 — P3 deliverable + wind-down triggers
7. Prior Gate-1 critique (`2026-05-19-p1-option-b-recompose-trigger-gate1.md`) — precedent format
8. P3 dispatch (`2026-05-20-gandalf-plus-jack-ryan-p3-validation-synthesis.md`) § 3.2 — my task brief
9. Engineering disciplines — #1, #11, #12, #15, #18 (relevant audit anchors)

**Raw telemetry verification scope:** all 10 class entries; per-tier WR values; recompose_attempts (35 total); floor_lock_detected flags (0 True across all attempts); modifier_extreme_low values (0 True); cold_start_verified (10/10 True); boss_wr and mini_boss_wr (0.0 for all 10); class_0009 elite_wr (0.670 confirmed); class_0010 recompose_outcome (skipped_experimental confirmed, floor_lock_recompose=None confirmed).

---

## § 2 — Pattern A: Discipline Audit

### Discipline #1 — Math-before-code

**CONFIRMED.** The synthesis's architectural recommendations flow entirely from empirical findings, not from analytical priors. § 7 (verdict) is grounded in § 4-§ 6 (empirical record); § 10 (recommendations) is grounded in § 7 (verdict). The "three independent lines" triangulation claim in § 7.2 nuance 3 is traceable to three distinct artifact chains: R1 sprint v2 engine commit `2546180`, R2+ST counterfactual joint synthesis Row 5 (AMENDED), and this hive's P2 canonical cold-start regen. No recommendation is authored ahead of evidence. Discipline #1 is satisfied.

### Discipline #11 — Empirical inspection

**CONFIRMED with one precision note.** Both methodological findings are captured with appropriate state-space framing:

- **P1 smoke-design finding** (§ 3.4): the warm-start-signature error is diagnosed correctly as conflating TOLERANCE-satisfied-at-old-floor with true equilibrium. The mandatory-cold-start-dry-run discipline candidate is correctly framed.
- **P2 signal-reversal finding** (§ 9): the 6/10 → 0/10 reversal root cause is correctly identified as pipeline-state-conditioned vs equilibrium-conditioned signals. The prospective application (smoke-gate design + population-level reads + future R-batch telemetry) is correctly enumerated.

**Precision note (INFO, not amendment-required):** § 9.3 states "Two independent hive events surfaced the same methodological pattern within ~24 hours." This is accurate but underspecifies the independence: the two events share the same root mechanism (both involve a balance-loop invocation in a non-equilibrium initial state being conflated with equilibrium state). Mentioning this shared root would strengthen the Discipline #11 elaboration proposed in § 9.6 — but this is refinement work for P5 co-authoring, not a Gate-2 blocker.

### Discipline #12 — Semantic shift (verdict naming)

**CONFIRMED.** Gandalf uses "CANNOT REJECT NULL" with statistical precision throughout:
- § 0 TL;DR: "Hypothesis H_RC is **not supported** by season_100005 empirical evidence" — not "H_RC is false"
- § 7.1 verdict: "H_RC is not supported... H_RC_0 is **not refuted**" — correctly frames the asymmetry
- § 7.2 nuance 1-3: three explicit load-bearing distinctions that prevent over-claiming
- § 7.3: "not a hive failure" framing per protocol § 11

The verdict is named as a worst-case-bound result at the threshold, not as proof of H_RC_0. Discipline #12 is satisfied.

**One minor precision gap (INFO):** § 0 states "it is at the worst-case bound of the verdict gate." This is correct — 0% is the worst possible observation within the CANNOT REJECT NULL verdict category. However, "worst-case bound" means something specific: it is the lowest possible kit-acceptable count (0%), which produces the maximum statistical distance from any PASS threshold. Future Matt-briefing language should be careful with "worst-case bound" not to imply the kits are "as broken as possible" (a separate claim about severity). The synthesis uses it correctly; the Matt briefing should preserve that precision.

### Discipline #15 — Drift-detection

**CONFIRMED.** The synthesis triangulates across three independent evidence sources without drift between framings:

- R1 kit-redesign queue (38/51 broken kits): cited in § 10.1 as corroborating evidence, not overriding evidence
- R2+ST counterfactual joint synthesis Row 5 ("catalogue has deeper pathology"): cited in § 7.2 nuance 3 + § 10.1 with the AMENDED qualifier preserved
- This hive's P2 evidence: the primary empirical record

The synthesis explicitly notes that the P2 evidence "corroborates both at full-season scope on a fresh substrate (shadow)." No framing drift detected. The § 7.2 phrase "three independent lines of evidence converge on the same diagnosis" is accurate — the three sources are methodologically distinct (prior sprint sprint empirical; Phase B.2 math + R2 telemetry; fresh cold-start regen under new mechanism).

---

## § 3 — Pattern B: Technical Correctness

### Verdict soundness

**CONFIRMED.** CANNOT REJECT NULL is the correct verdict given the evidence:

- Observed: 0% kit-acceptable (0/10 classes)
- Threshold: < 60% → CANNOT REJECT NULL (scope-of-work § 1)
- Distance from PASS moderate threshold: 60 percentage points (not edge-of-observation)
- The verdict is unambiguous; no re-classification of any class would shift this

The PASS moderate threshold requires ≥ 60% kit-acceptable. To shift the verdict, 6/10 classes would need to be reclassified as kit-acceptable — a reclassification that would require all 5 per-tier targets to pass for those classes. The raw data shows universal boss_wr=0.000 and mini_boss_wr=0.000, which are themselves sufficient to classify every class as kit-broken under any reasonable kit-acceptable definition. There is no reading of the evidence that produces a PASS verdict.

### Per-class data verification

All 10 per-class rows verified against raw telemetry:

| class_id | final_modifier (synthesis) | final_modifier (raw) | boss_wr (synthesis) | boss_wr (raw) | Match |
|---|---|---|---|---|---|
| class_0001 | 0.1956 | 0.1956 | 0.000 | 0.0 | MATCH |
| class_0002 | 0.0719 | 0.0719 | 0.000 | 0.0 | MATCH |
| class_0003 | 0.1338 | 0.1338 | 0.000 | 0.0 | MATCH |
| class_0004 | 0.1338 | 0.1338 | 0.000 | 0.0 | MATCH |
| class_0005 | 0.1338 | 0.1338 | 0.000 | 0.0 | MATCH |
| class_0006 | 0.0719 | 0.0719 | 0.000 | 0.0 | MATCH |
| class_0007 | 0.1338 | 0.1338 | 0.000 | 0.0 | MATCH |
| class_0008 | 0.3812 | 0.3812 | 0.000 | 0.0 | MATCH |
| class_0009 | 0.3812 | 0.3812 | 0.000 | 0.0 | MATCH |
| class_0010 | 0.1338 | 0.1338 | 0.000 | 0.0 | MATCH |

**Elite WR for class_0009:** synthesis claims 0.670; raw shows 0.67; MATCH (rounding representation only).

**class_0009 failing_tiers:** synthesis names swarm + magic + elite + mini_boss + boss (5 tiers). Raw telemetry `failing_tiers` array: ['swarm', 'magic', 'elite', 'mini_boss', 'boss']. MATCH. The controller-mechanic mismatch sub-pattern on elite over-shoot is correctly identified.

**class_0010 experimental handling:** raw shows `recompose_outcome: "skipped_experimental"`, `floor_lock_recompose: null`, `recompose_attempts: []`. Synthesis and star-lord both note "NULL on experimental per MIGRATION.md v1.22 spec." MATCH.

### Sub-pattern verification

**Sub-pattern 2 (boss-DPS-floor structural) = 10/10:**
Verified via raw telemetry: `boss_wr == 0.0` for all 10 classes. CONFIRMED.

**Sub-pattern 4 (floor-lock-still-active) = 0/10:**
Verified: `floor_lock_recompose=True` count in aggregate = 0. Additionally, all 35 individual `recompose_attempts` have `floor_lock_detected=False`. Zero exceptions. CONFIRMED as explicitly NOT implicated.

**Sub-pattern 5 (recompose-couldn't-recover) = 9/9 canonical:**
Verified: all 9 canonical classes have `recompose_attempts` list (non-empty) and all have `boss_wr=0.0`. The recompose mechanism operated on all 9; none achieved boss-tier WR improvement. CONFIRMED.

**Nuance on sub-pattern 5 (Amendment 2 basis):** 8/9 canonical classes had at least one accepted lever (negative delta, WR compression at lower tiers only): classes 0002-0009. Class_0001 is the exception: 3 attempts, all delta=0, none accepted, outcome=`modifier_fallback`. Both paths confirm "recompose-couldn't-recover" but through different mechanisms. The synthesis § 6.1 table notes class_0001's `modifier_fallback` outcome but does not surface this in the sub-pattern 5 prose. Amendment 2 addresses this.

**Sub-pattern 6 (generation-rule-pathology) = 10/10:**
This sub-pattern is an architectural inference, not a directly observable field in telemetry. The synthesis correctly frames it as such (§ 6: "the lever library is compositional-rearrangement, not generation-rule rewrite"). The inference is sound given the observed data shape: levers operate, WR shifts at lower tiers, boss WR stays at zero. The root cause is upstream of lever space. CONFIRMED as appropriate inference from evidence.

### Recompose-attempt count discrepancy

**DISCREPANCY:** Synthesis and star-lord both cite "33 recompose_attempts on 9 canonical classes." Raw telemetry count: **35 attempts** (class_0001=3; classes 0002-0009=4 each; total=35, all on canonical classes; class_0010=0). The figure "33" does not match the raw data.

This is Amendment 1 — a factual correction to a figure cited in the canonical record. Impact: star-lord's analysis (engine artifact) also cites 33 — that document is the engine-side record and would require a separate correction; out of jack-ryan's scope for this critique. The synthesis doc (collab side) is within scope and must be corrected before the verdict-handoff tag fires.

### Two-event ~24h convergence argument

The synthesis's argument for elevating the pattern to a single Discipline #11 elaboration (rather than two standalone disciplines) rests on: two independent hive events surfacing the same epistemic pattern within ~24 hours. The argument is structurally sound. The convergence strengthens the case that the pattern is real and worth systematic documentation — a single occurrence could be local; two independent occurrences within a single hive cycle makes it an engineering-discipline-worthy systematic risk.

**Concurrence:** I concur with the single-elaboration framing. The two findings share a root-cause mechanism (balance loop invoked in non-equilibrium state treated as equilibrium state); separating them into two standalone disciplines would fragment the conceptual unity. The elaboration text in § 9.6 is well-drafted and suitable for P5 co-authoring refinement. The sub-clauses within the single elaboration handle the two specific application contexts (smoke-gate design; population-level signal reads) cleanly.

### "Two-event ~24h convergence" is load-bearing-sound

The argument is load-bearing-sound for elevating to engineering-discipline. The 24-hour convergence is observable in the hive log timestamps. The independence of the two events is real: P1 smoke-B1 was gandalf's brief § 4.1 design decision; P2 signal-reversal was knight-rider's Phase 1 read of rocket's generation-time table. Different agents, different phases, different artifacts, same epistemic error pattern. The argument holds.

---

## § 4 — Pattern C: Scope Discipline

### P3 scope adherence

**CONFIRMED.** The synthesis does not route P4 autonomously. § 8 explicitly: "P4 does NOT fire autonomously per protocol § 7 trigger #3 + dispatch § 6 HARD out-of-scope #1." § 8 recommendation is "SURFACE TO MATT (wind-down trigger #3)." No autonomous P4 routing anywhere in the document.

### Speculation beyond evidence

**CONFIRMED clean.** The synthesis explicitly bounds its evidence claims to season_100005 / shadow substrate / disposition-3 calibration. § 7.2 nuance 2 states: "absent ≠ proven nonexistent across all substrates." § 8 "why not diagnose further" explicitly flags that substrate-generalization is a Matt-direction question. § 11.3 describes the empirical record as "the canonical empirical record of catalogue pathology at full-season scope on shadow substrate under the new tuning contract" — not an all-substrates claim. Speculation discipline is maintained.

**Substrate-generalization scope (Amendment 3 basis):** The synthesis body is careful on scope. The single concern is that § 0 TL;DR states the aggregate findings ("0% kit-acceptable, 100% Pattern-A, 100% kit-broken") without a substrate-scope parenthetical visible in the TL;DR. A reader consuming only § 0 could interpret these figures as substrate-general. Amendment 3 (RECOMMENDED) addresses this for the Matt briefing; the body is clean.

### § 8 and § 10 framing (Matt-options vs hive directives)

**CONFIRMED.** § 8 recommends surfacing to Matt, does not direct Matt. § 10.1 introduces the kit-redesign queue recommendation with: "**Surface** the kit-redesign queue as the natural next-step architectural decision **for Matt's consideration**." § 10.2 frames the three alternatives as "options Matt may consider." § 10.3 explicitly lists "What this recommendation does NOT decide" — a five-item list of Matt-level decisions. The framing is non-prescriptive throughout.

**One edge case (INFO, not amendment):** § 10.2 option (C) names a specific class: "class_0006 lightning_mage — has the cleanest archetype-mechanic-mismatch signature per R1 queue § 1.2." This is a specific suggestion within an option, but it is presented as a design-judgment recommendation within a Matt-option (not as a directive). It does not cross into hive-directive territory. If the Matt briefing includes this specific class recommendation, it should be presented at the same register: one design-judgment candidate among others, not a queued work item.

### Kit-redesign queue recommendation transparency

**CONFIRMED.** The recommendation is transparent about its evidential basis (three independent lines), its scope (does not commit Matt to timeline or sequencing), and its alternatives (three options with cost/value assessment). The synthesis does not represent the kit-redesign queue as the only possible path; it explicitly enumerates alternatives and assigns a design-judgment preference among them without claiming that preference is binding.

---

## § 5 — Amendments

### Amendment 1 (REQUIRED) — Recompose-attempt count correction

**Target:** `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md`

**Finding:** Synthesis cites "33 recompose_attempts on 9 canonical classes" in § 4.3, § 11.3, and anywhere else this figure appears. Raw telemetry shows 35 attempts (class_0001=3, classes 0002-0009=4 each). The discrepancy is 2 attempts.

**Action:** Replace "33" with "35" in all occurrences within the synthesis doc. No change to interpretation or conclusions — all attempts have `floor_lock_detected=False`, sub-pattern verification is unchanged.

**Note:** Star-lord's engine-side analysis also shows "33" (star-lord § 3 references "33 total attempts"). That document is out of jack-ryan's scope here; knight-rider should note this for the record so star-lord can issue a corrective commit at P5 or as part of the decisions-log entry maintenance.

### Amendment 2 (REQUIRED) — Sub-pattern 5 operational nuance for class_0001

**Target:** `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` § 6 (sub-pattern 5 description) + § 6.1 (class_0001 row note)

**Finding:** Sub-pattern 5 ("recompose-couldn't-recover") is correctly applied to all 9 canonical classes but the operational mechanism differs for class_0001 vs classes 0002-0009:
- Classes 0002-0009: at least one lever accepted (negative delta); WR compression occurs at lower tiers only; boss_wr stays 0. Recompose operated and produced compositional change; the change didn't reach boss tier.
- Class_0001: 3 attempts, all delta=0, none accepted; `modifier_fallback` path. Recompose operated but all levers found no signal at the eval_modifier; the loop exhausted options.

**Action:** Amend § 6 sub-pattern 5 description to distinguish: "Recompose attempted on all 9/9 canonical classes. 8/9 classes (0002-0009) had at least one accepted lever (delta < 0; lower-tier WR compression only; boss_wr unchanged at 0). 1/9 (class_0001) exhausted all levers at delta=0 before reaching modifier_fallback path. Both paths confirm recompose-couldn't-recover; the operational distinction matters for the kit-redesign queue: class_0001's path suggests the lever library found no signal even at lower-tier WR, which may indicate a more fundamental kit-composition gap than the compression-only case."

Amend § 6.1 class_0001 row note (already mentions `modifier_fallback`) to reference this distinction explicitly.

**Rationale:** The kit-redesign queue downstream will use this disaggregation to prioritize classes. Class_0001's modifier_fallback path represents a deeper kit signal gap than the compression-only cases. One-size-fits-all kit-redesign would miss this distinction (the same Diablo II framing gandalf applied to class_0009's controller-mechanic mismatch applies here at the lever-signal level).

### Amendment 3 (RECOMMENDED) — Substrate scope parenthetical in § 0 TL;DR

**Target:** `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` § 0 TL;DR

**Action:** In the sentence "Observed 0% kit-acceptable, 100% kit-broken, 100% Pattern-A (boss-DPS-floor structural), 0/10 floor-lock-recovery candidates," add a parenthetical: "(on shadow substrate seed=100005 under disposition-3 calibration)."

**Rationale:** The body is clean on substrate scope. The TL;DR is the first-read surface; a reader arriving cold (e.g., Matt reading the briefing without the body) needs the scope boundary to be visible immediately. The Matt briefing will likely quote from or summarize § 0. This is advisory for the Matt briefing quality, not a canonical correctness requirement.

---

## § 6 — Open Questions for Knight-Rider

1. **Star-lord attempt-count correction (Amendment 1 cross-seam):** star-lord's engine-side analysis doc also cites "33 total attempts." This is an engine-repo artifact. Knight-rider should note whether to route a minor star-lord corrective commit at P5 (or fold into the decisions-log entry) to align the engine-side record with the corrected figure (35). Low priority; the sub-pattern verdicts are unaffected.

2. **Matt briefing § 0 scope parenthetical (Amendment 3):** if gandalf does not apply Amendment 3 to the findings doc, knight-rider should apply the substrate-scope qualifier explicitly in the Matt briefing's executive summary section. The briefing must not allow a "100% Pattern-A across all substrates" misread.

3. **Engineering-disciplines Discipline #11 elaboration — P5 vs trigger #3 inclusion:** gandalf frames the elaboration as "P5 amendment OR Matt-briefing inclusion at trigger #3." Given that CANNOT REJECT NULL fires and the hive deactivates, the P5 arc may not complete under this hive's autonomous operation. The Matt briefing should include the proposed elaboration language (§ 9.6) as an engineering-discipline recommendation for Matt's awareness, even if the formal amendment awaits P5 authorization. Knight-rider's call on where to put it.

4. **Sub-pattern 5 class_0001 note in the Matt briefing:** the modifier_fallback operational distinction for class_0001 (Amendment 2) is a kit-redesign queue input. If the Matt briefing summarizes the failure-mode disaggregation, it should capture this distinction (not just "100% boss-DPS-floor") so the kit-redesign queue's first authoring session has the right granularity from the start.

---

## § 7 — Disposition + Sign-Off

**APPROVE-WITH-AMEND.**

**Required before tag fires:**
- Amendment 1 (count correction 33→35 in synthesis doc)
- Amendment 2 (sub-pattern 5 operational nuance for class_0001 in § 6)

**Advisory (fold into Matt briefing if not in findings doc):**
- Amendment 3 (substrate scope parenthetical in § 0 TL;DR)

**No BLOCK.** The synthesis does not materially misrepresent the evidence. The verdict is technically correct and structurally sound. The per-failure-mode disaggregation is appropriately granular and will serve the kit-redesign queue downstream. The methodology finding is captured with the right epistemic precision. Scope discipline is maintained throughout. The single-Discipline-#11-elaboration framing is the right shape.

The verdict-handoff fires on Amendment 1 + 2 resolution (gandalf concurs or knight-rider applies inline). Amendment 3 is advisory and does not hold the tag.

**Routing recommendation:** APPROVE-WITH-AMEND; route amendments 1-2 to gandalf for inline resolution (lightweight; both are factual corrections to two sentences — gandalf does not need to re-synthesis); on gandalf concurrence, knight-rider fires `recompose-hive/v0.4-validation-verdict` + authors Matt briefing per protocol § 7 trigger #3.

Jack-ryan signs off.

---

**Reviewer:** jack-ryan
**Date:** 2026-05-20
**Cites:** Discipline #1, #11, #12, #15; Review Principles 1, 2, 3, 5; ADR-002 (approval authority)
