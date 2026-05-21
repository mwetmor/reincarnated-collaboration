# Gate-1 Review — W0.7 LC-011 Ablation Design
## Controller/Mage Floor-Lock Non-Convergence

**Reviewer:** jack-ryan
**Date:** 2026-05-21
**Verdict:** APPROVE-WITH-AMEND
**Mode:** DESIGN-MODE Gate-1
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-011-ablation-design.md`
**Developer:** gamora
**Principles applied:** Review Principles 1, 2, 3, 4 (REVIEW_PROCESS.md §1)
**Disciplines cited:** #1, #10, #11, #13a, #13b

---

## Top-Line Verdict

**APPROVE-WITH-AMEND**

The mechanism reframing is valid and well-evidenced. The 3-run ablation design is substantively sound. One blocking amendment required before run execution (Amendment A — see below). Two non-blocking amendments recommended.

**Blocking:**
- **Amendment A:** Attribution math for Run 2 is not Discipline #13b-compliant. Run 2 (lever acceptance, observational) currently produces descriptive context, not a controlled attribution input. The math note's attribution formula (`A% + B% + residual% = 100%`) claims to partition floor-lock rate across surfaces but the B% estimate ("from Run 2 lever-acceptance telemetry") is not a controlled subtraction — it is an observational correlation from a non-patched run. This will produce an attribution that cannot satisfy the `check: sum = 100%` requirement cleanly. The math note must be amended to either (1) explicitly label Run 2 as observational context, not an attribution component, and update the Discipline #13b template accordingly, or (2) redesign Run 2 as a controlled run (lever-pool widening patch) that produces a subtractable delta. See Focus area 4 below.

**Non-blocking (amend before tagging):**
- **Amendment B:** Math note §4 defends smoke-test mode but does not explicitly cite the LC-002 precedent and distinguish the two cases. Add one sentence documenting the structural distinction: LC-002's mechanism was cohort-size-dependent (n_classes=11 modulo bias disappears at n=5); LC-011's mechanism is per-class (floor-lock fires at any n_classes). This is a record-keeping obligation — the precedent must be named in the math note, not just in the dispatch.
- **Amendment C:** §6.2 references "B14.5 V2" (energy-type calibration lever) as a forthcoming fix that would interact with LC-011 results. The decisions-log shows Option B (floor-lock recompose re-conditioning) is currently SOFT-DISABLED (`LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR`) pending P2 empirical verification. The math note must acknowledge that the existing Option B infrastructure is already instrumented (telemetry: `floor_lock_detected`, `floor_lock_recompose`) and that LC-011 ablation runs will need to note whether `floor_lock_detected=TRUE` populates in the telemetry — which provides a cross-check against the 42% FAILED rate from the `classes` table convergence_status field.

---

## Per-Focus-Area Findings

### Focus Area 1 — Mechanism Reframing Validity: PASS

**Is the 41.8% FAILED rate statistically defensible?**

n=146 total mage_controller classes, 61 FAILED. This is not a small-sample concern — at n=61 FAILED the binomial confidence interval for the true rate is roughly [33%, 51%] at 95% CI. The reframing is statistically defensible. Era boundary is post-schema (`season_id >= season_000800`), which excludes the pre-B6-schema records that contaminated LC-009's hunter data. The era stratification protocol that caught the LC-009 artifact has been correctly applied here.

**Is avg_modifier=0.053 consistent with MODIFIER_SEARCH_FLOOR=0.01?**

Yes. `MODIFIER_SEARCH_FLOOR=0.01` is the binary search lower bound (balance_loop.py:160). FAILED classes exit at whatever modifier the binary search reached when MAX_ITERATIONS=10 is exhausted. For a class whose equilibrium modifier `m*` is below the floor (e.g., `m*=0.001`), the binary search will converge downward until it approaches the floor but may terminate at any value near it, depending on iteration count and step dynamics. The observed avg=0.053 is consistent with the binary search exhausting iterations while still above the floor — the search is approaching the floor but hasn't reached it because MAX_ITERATIONS=10 runs out first. This is mechanically coherent with `MODIFIER_SEARCH_FLOOR=0.01` being the lower bound, not a target. The 0.053 average reflects the search-path residual, not an arbitrary value.

**Are mage/controller floor-locks independent from W0.9.6 boss-tier floor-locks?**

Confirmed independent. W0.9.6 boss-tier floor-locks were arena-side: the boss-AI leash-reset bug made boss_wr=0.000 structurally regardless of modifier, which caused all classes to floor at a boss-tier WR boundary in the calibration sweep. That was an evaluation-time phenomenon (fight outcome corrupted by boss AI bug). LC-011 floor-locks are generation-side: the binary search in the convergence loop exhausts iterations before finding a 50% WR equilibrium modifier. The two phenomena operate at different pipeline stages (arena execution vs balance-loop convergence), affect different populations (all archetypes equally for W0.9.6 boss-tier vs mage/controller-specific for LC-011), and have different signatures (W0.9.6: modifier_extreme_low=True across all archetypes; LC-011: convergence_status=FAILED disproportionately in mage/controller). These are orthogonal.

**W0.10 interaction?**

W0.10 fixed the arena-side boss AI leash-reset bug. LC-011 is the balance-loop binary-search convergence path. The two are orthogonal by architecture: W0.10 changed spatial_engine.py and arena.py (fight execution layer); LC-011 mechanism is in balance_loop.py convergence loop (kit-evaluation layer that calls fight execution). The post-W0.10 era is actually the correct evaluation baseline for LC-011 — the post-schema era boundary used in §1 is consistent with the post-W0.10 environment. No interaction.

### Focus Area 2 — Smoke-Test Mode Applicability: PASS (with Amendment B)

The LC-002 lesson applies specifically when smoke-test's n_classes=5 clobber eliminates the mechanism under study (LC-002: n_classes=11 modulo bias disappears at n=5; any run produces 20% fire with no bias to measure). LC-011's mechanism is per-class: the binary search floor-lock fires independently for each class generated, regardless of cohort size. At n_classes=5, a smoke-test season still generates 1-2 mage/controller classes at the expected archetype assignment rate. The floor-lock mechanism fires (or doesn't) for each of those classes regardless of how many total classes are in the season. The signal is present at n_classes=5.

**Sample adequacy check:** 15 seasons × n_classes=5 = 75 classes total. At the historical archetype mix (~55% mage/controller), approximately 40 mage/controller classes expected per run. At 42% floor-lock rate, Run 1 expects ~17 FAILED — sufficient for rate comparison. Run 3 prediction threshold is <20% floor-lock; a 22-point reduction from 42% to 20% is detectable at n=40 with standard binomial test (power >0.90). The escalation path (30 seasons before full regen) is the right fallback if archetype mix runs lower than expected. **Smoke-test is appropriate here.** This is a correct application of Discipline #10 (right tool for the validation question).

Amendment B (non-blocking): the math note must cite the LC-002 precedent by name and state the structural distinction explicitly in §4. The current §4 makes the argument correctly but does not reference LC-002 or the canonical Option C decision tree. Omitting the precedent citation weakens the audit trail for future analysts.

### Focus Area 3 — Surface A Ablation Verification: PARTIAL

**Code path from `skill_power_tier` to floor-lock:**

The math note traces: `b6_archetype_templates.py → skill_power_tier → _generate_abilities() → raw DPS → equilibrium modifier in binary search`. This is mechanistically correct — higher DPS budget at same modifier produces higher WR → binary search drives modifier downward to compensate → if the required modifier to reach 50% WR is below MODIFIER_SEARCH_FLOOR, the class FAILED.

**Is this the actual mechanism or a proxy?**

`skill_power_tier` is a DPS budget parameter, not the equilibrium modifier directly. It is one step upstream from the actual driver (raw DPS of the generated kit). A higher `skill_power_tier` makes floor-lock more likely but does not deterministically produce it — kit composition RNG within the tier can produce high or low DPS kits. The math note §1.5 correctly identifies this: "The FAILED rate is per-archetype-type, not per-specific-class-instance." This means `skill_power_tier` is a structural probability driver, not a deterministic cause. Reducing it by one tier will shift the DPS budget distribution downward, which should reduce the fraction of kits requiring modifier < floor — but the effect size depends on how close the current tier boundary is to the floor-lock threshold.

**Confounding risk from tier reduction:**

Reducing `skill_power_tier` by one tier changes the DPS budget for the patched templates. This affects not just floor-lock rate but also: (a) CONVERGED modifier distribution (mage/controller classes now converge at higher modifier values, potentially changing archetype power balance), and (b) INTENTIONAL_OUTLIER rate (if the tier boundary interacts with outlier designation logic). The math note does not note these potential confounds. The ablation isolates `skill_power_tier` cleanly as a manipulation — but interpretation of Run 3 results requires acknowledging that the modifier distribution shift is a secondary effect. This is PARTIAL: the ablation design is structurally sound, but the math note should note the secondary effect on converged modifier distribution as a known confound to be measured (not controlled away).

**#13a-partition compliance:**

CONDITIONAL-PASS. The ablation patches template parameters for archetypes that happen to be mage/controller. The mechanism tested (DPS budget → equilibrium modifier → floor-lock) is substrate-neutral — the same mechanism operates for physical archetypes, and the patching is applied at the template level, not as a runtime branch on element/substrate identity. This matches the compliance reasoning in §2: permissible because the experimental manipulation is archetype-conditioned at the template layer, not at the execution layer. PASS.

### Focus Area 4 — Attribution Interpretability: PARTIAL (BLOCKING Amendment A)

The math note's Discipline #13b attribution formula:

```
Surface A contribution = (Run1_rate - Run3_rate) / Run1_rate × 100%
Surface B contribution = estimated from Run 2 lever-acceptance telemetry
Residual = 100% - A% - B%
Check: A% + B% + residual% = 100%
```

**The blocking problem:** Run 2 is observational — it adds instrumentation but makes no template changes. It reports lever acceptance rate per archetype as descriptive telemetry. This is not a controlled subtraction. Surface B% is estimated from correlation (mage/controller have lower lever acceptance rate → therefore B contributes X% of floor-lock) rather than from a controlled delta (Run1_rate - Run2_rate). The Discipline #13b attribution template, as shown in the math note, implies a three-way additive partition. But the three-way partition is:

```
A% = (Run1 - Run3) / Run1   ← controlled delta (valid)
B% = correlation from Run 2  ← NOT a controlled delta (not Discipline #13b-compliant)
Residual = 100% - A% - B%   ← inherits the B% estimation error
```

This produces a formally non-compliant attribution: A% is precise, B% is an estimate without a confidence interval, and residual inherits B%'s uncertainty. The check `A% + B% + residual% = 100%` will algebraically balance but will not be empirically grounded for B% + residual.

**Remediation options (gamora to select one):**
1. Label Run 2 as observational context only, not an attribution component. The Discipline #13b attribution is then two-way: `Surface_A% = (Run1 - Run3) / Run1`; `Residual% = Run3_rate` (attributable to Surface B + energy-type gradient, undifferentiated). This is honest — it does not claim to attribute the residual fractionally. The Run 2 data informs the follow-on workstream (null result handling) without corrupting the attribution math.
2. Replace Run 2 with a controlled lever-pool widening run (patch archetype constraints to widen valid-swap pool for mage/controller templates). Then B% = `(Run3_rate - Run4_rate) / Run1_rate × 100%` is a proper controlled delta. This adds a Run 4 and increases ablation cost.

Option 1 is preferred — it preserves the 3-run design, is low-cost to implement (amendment is a math note edit, not a run redesign), and produces honest attribution. Run 2 lever-acceptance data remains valuable as diagnostic evidence for follow-on workstream decisions.

### Focus Area 5 — gamora's 6 Explicit Gate-1 Questions

**Q1 — Mechanism reframing (floor-lock non-convergence vs slow WR-surface convergence):**
AGREED. The reframing is valid, well-evidenced, and changes the correct ablation target. The CONVERGED-only analysis (§1.2: mage 5.95 vs physical 4.23, 1.4× ratio) cleanly isolates the WR-surface speed difference from the floor-lock frequency effect. The dispatch framing ("slow convergence → compute overhead") was partially correct about the phenomenon but misattributed the cause. The ablation correctly redirects to floor-lock prevalence reduction.

**Q2 — Smoke-test mode validity (n_classes=5, escalate to 30 seasons before full regen):**
CONCUR. Smoke-test is appropriate (see Focus area 2 above). The escalation ladder (15 seasons → 30 seasons → full regen only if mechanism requires it) is correctly ordered. Discipline #10 endorses smoke-test here. Gate-1 endorses escalation to 30 seasons as the first fallback if archetype count per run is insufficient.

**Q3 — Run 2 instrumentation scope (lever-acceptance logging, READ-ONLY):**
NO CONCERN on the instrumentation per se. Adding lever-acceptance-rate logging to `_primary_recompose_loop` is read-only (no behavior change). However, if the telemetry is appended to `recompose_attempts` rows as new fields, star-lord owns schema for that table — confirm that the new fields are nullable (backward-compatible) and documented in the schema version increment. If the telemetry is written to a separate output (e.g., a JSON sidecar or stdout log rather than the database table), no schema impact. Gamora should confirm telemetry destination before execution. This is a coordination check, not a design concern.

**Q4 — Null result on Run 3 (lever-pool widening OR LC-004/B14.5-V2 cross-seam closure):**
Gate-1 endorses the following disposition order: (a) if Run 3 produces null result AND Run 2 shows demonstrably lower lever acceptance for mage/controller, follow-on lever-pool widening run is warranted; (b) if Run 3 produces null result AND Run 2 shows similar lever acceptance, the floor-lock differential is attributable to the energy-type gradient (LC-004 consequence) — close with math note documenting "overhead is LC-004 consequence; fix requires B14.5 V2 energy-type lever, not a sim-seam ablation." Option (b) is a valid Discipline #13b closure (attributing to a known cross-seam structural cause). Do not add a Run 4 on a null Run 3 unless Run 2 evidence supports it.

**Q5 — #13a partition compliance:**
CONFIRMED. Patching `skill_power_tier` in mage/controller templates targets a structural DPS-budget parameter. The mechanism measured (DPS budget → convergence modifier → floor-lock probability) is substrate-neutral. The experimental manipulation is archetype-conditioned at the template layer (a scheduling property), not a runtime branch on element/substrate identity as the causal mechanism. Compliant per Discipline #13a.

**Q6 — QD implications reframing (FAILED 42% → archive gaps vs compute overhead):**
AGREED, and the reframing is materially consequential. The original framing ("slow convergence → compute overhead → QD archive underrepresentation via cost") implied a mitigation of limiting mage/controller generation frequency to manage cost. The reframing ("non-convergence FAILED 42% → archive gaps via missing valid kits") implies the opposite: the archive underrepresentation cannot be fixed by compute management — the 42% of FAILED attempts produce no usable kit data regardless of cost. The fix priority must be convergence-reachability improvement. This changes QD generation-loop design: rather than throttling mage/controller generation, the loop must be able to generate valid kits for those archetypes at all — which requires fixing the floor-lock prevalence first. Gate-1 confirms this reframing is correct and the QD archive implications are materially different.

### Focus Area 6 — P0 Close-Out Implications: PARTIAL

**Does floor-lock finding require P1+ remediation before P0 milestone?**

The floor-lock prevalence (42% FAILED for mage/controller) is a known structural issue that predates W0.7. The `recompose-hive/v0.1-option-a-floor-widened` milestone tag already addressed the floor-widening (Option A). Option B (floor-lock recompose re-conditioning) is implemented but SOFT-DISABLED pending P2 empirical verification. LC-011 ablation is therefore not discovering a new problem — it is attributing a known problem to specific mechanical surfaces for the first time. Attribution documentation is the W0.7 deliverable; remediation is B14.5 V2 / P2+ territory.

**P0 close-out verdict:** Documentation + attribution is sufficient for W0.7 close-out. The 42% FAILED rate is not a new P1 blocker discovered by LC-011 — it was already known and partially mitigated (Option A). LC-011 provides the attribution math needed before any further mitigation is designed. P0 milestone can fire after LC-011 ablation runs complete and attribution is documented.

**Is the 41.8% FAILED rate a P1 archive blocker?**

Not for P0 close-out. The QD archive architecture for mage/controller cells is a P2/P3 design question (compose archive insertion). The 42% rate means archive cell filling for mage/controller archetypes will require approximately 1.7× more generation attempts to achieve the same filled-cell count as physical archetypes. This is a planning input for P2, not a P0 gate. Document in the math note's §6 forward implications as a P2 planning factor.

### Focus Area 7 — Discipline #18 Candidate Disposition

The registered Discipline #18 candidate (decisions-log 2026-05-21: joint-gate ship criterion — mechanical-BC AND cohesion-BC AND visual-BC) was registered in the context of QD archive kit-shipment criteria, not specifically mage/controller convergence. Does the 42% mage/controller FAILED rate interact with this candidate?

**Finding:** The interaction is real but not gate-opening for Discipline #18 ratification. The joint-gate ship criterion (Discipline #18 candidate) applies to kits that have been generated and are being evaluated for shipment. FAILED classes never produce a usable kit — they exit the convergence loop without a valid modifier and do not enter the archive. They therefore never reach the joint-gate evaluation stage. The 42% FAILED rate is a pre-gate problem (generation-side), not a gate-evaluation problem (ship criterion). The Discipline #18 candidate as registered remains scoped to the evaluation gate for successfully-generated kits.

However: if the 42% FAILED rate persists into P5 when the joint-gate fires at scale, mage/controller cells will be underrepresented in the archive relative to the joint-gate sample target. This is worth documenting in the Discipline #18 candidate registration as a generation-side precondition: "joint-gate ship criterion presupposes the archive has sufficient valid kits per archetype type; mage/controller archive fill rate requires LC-011 remediation to reach parity." This is a note for the candidate registration entry, not an amendment to the Discipline #18 registration itself. Gate-1 does not re-open the Discipline #18 registration — it notes the connection.

---

## Mechanism Reframing Assessment

**Valid and complete.** The empirical evidence (§1.1–§1.5 of the math note) cleanly supports the reframing from "slow convergence speed" to "floor-lock non-convergence." The key diagnostic moves are:

1. Stratification by convergence_status (CONVERGED vs FAILED vs INTENTIONAL_OUTLIER) — this isolates the FAILED population as the primary driver of the elevated iteration average.
2. CONVERGED-only comparison (mage 5.95 vs physical 4.23, 1.4×) — this shows the WR surface convergence speed is only modestly different; the large aggregate ratio is the FAILED population pulling the mean to MAX_ITERATIONS=10.
3. FAILED modifier clustering at 0.053 — consistent with binary search approaching MODIFIER_SEARCH_FLOOR before exhausting iterations.
4. Physical/rogue group: zero FAILED in post-schema era — the asymmetry is archetype-structural, not noise.

The reframing does not require additional empirical evidence before ratification. The math note §1 provides sufficient stratified telemetry evidence. **Reframing is ratified as of this Gate-1 review.**

**One observation on residual uncertainty:** the math note §1.4 attributes mage/controller floor-lock structural tendency to the LC-004 energy-type mechanical gradient (mana ~3-5× DPS advantage over rage at same modifier). This mechanistic link is by reference to existing decisions-log analysis, not by new empirical measurement. It is plausible and consistent with the evidence, but it is not directly measured in §1. The ablation (Run 3 and Run 2) will provide the first direct evidence of which structural surface (DPS budget tier vs lever acceptance rate) is the dominant driver. The reframing is valid regardless — the mechanism is floor-lock non-convergence, and the structural causes are the ablation's subject.

---

## Smoke-Test Disposition

**Acceptable here.** LC-002 lesson is that smoke-test eliminates the mechanism under study when the mechanism is cohort-size-dependent. LC-011 mechanism is per-class, present at any n_classes. The math note's §4 reasoning is correct. Smoke-test approved for all three runs. Escalation path (30 seasons before full regen) is correct. Full regen is explicitly NOT required for this ablation.

---

## Surface A Justification

**Sufficient for ablation, with noted limitations.** `skill_power_tier` is the correct primary ablation surface because:
- It is the upstream structural parameter that determines DPS budget
- It is in `b6_archetype_templates.py` (the template layer), which is the correct level to patch without cross-seam scope
- Reducing it by one tier produces a measurable, directional hypothesis (floor-lock rate should decrease)
- The patch is ephemeral (restore after run per math note §3.2)

Surface B (lever acceptance rate) is tested observationally in Run 2, which is the right scope — it is not an ablatable surface within this workstream without a more invasive template-constraint change. The null-result disposition for Run 3 correctly routes to Surface B follow-on if warranted by Run 2 evidence.

The secondary confound (CONVERGED modifier distribution shift) should be noted in the math note as a measurement to capture in Run 3 (not to control, but to observe). This does not block the ablation.

---

## Required Amendments Before Execution

**Amendment A (BLOCKING):** Revise math note §5 (Discipline #13b Attribution Template) to replace the current three-way attribution formula with an honest two-way partition:

```
Surface_A_contribution% = (Run1_rate - Run3_rate) / Run1_rate × 100%
Residual% = Run3_rate   (attributable to Surface B + energy-type gradient, undifferentiated)
Check: Surface_A% + Residual% = 100% (Run3_rate / Run1_rate + (1 - Run3_rate/Run1_rate) = 100%) ✓
```

Run 2 lever-acceptance data is retained as observational evidence to inform the null-result disposition and follow-on workstream design. It is not a subtractable Discipline #13b component.

Update the pre-ablation prediction framing accordingly: "Surface A: predicted 40-60% (ablation will measure); Residual: predicted 40-60% (Surface B + LC-004 gradient, undifferentiated by this ablation)."

**Amendment B (non-blocking):** Add one sentence to §4 explicitly citing LC-002 precedent by name and stating the structural distinction: "Unlike LC-002 (where smoke-test's n_classes=5 clobber eliminated the n_classes=11 modulo mechanism under study), LC-011's floor-lock mechanism is per-class and present at any n_classes value. Smoke-test is therefore appropriate per Discipline #10."

**Amendment C (non-blocking):** Add one sentence to §6.2 (B14.5 V2 interaction) noting that Option B floor-lock recovery infrastructure is already live (soft-disabled) and that Run 1/Run 2/Run 3 telemetry will populate `floor_lock_detected` and `floor_lock_recompose` fields in `recompose_attempts`. The math note should instruct gamora to cross-reference the `floor_lock_detected=TRUE` rate from telemetry against the convergence_status=FAILED rate from the classes table — these should be consistent, and any discrepancy is a diagnostic signal worth noting.

---

## Action Items

- [ ] **gamora (BLOCKING before run execution):** Amend math note §5 per Amendment A. Two-way Discipline #13b attribution formula replacing current three-way formula. Run 2 relabeled as observational context.
- [ ] **gamora (non-blocking, amend before tagging):** Amend math note §4 per Amendment B (LC-002 precedent citation).
- [ ] **gamora (non-blocking, amend before tagging):** Amend math note §6.2 per Amendment C (Option B soft-disable cross-reference).
- [ ] **gamora (before Run 2 execution):** Confirm telemetry destination for lever-acceptance logging (separate sidecar vs `recompose_attempts` table fields). If appended to `recompose_attempts`, confirm nullable fields + coordinate star-lord schema version increment.
- [ ] **gamora (post-ablation):** Note B14.5 V2 / Option B soft-disable status in the attribution conclusion section of the math note (§11 or equivalent). LC-011 runs are baselining the pre-Option-B-enabled state.
- [ ] **knight-rider (P2 planning):** Note the 42% mage/controller FAILED rate as a generation-attempt multiplier (1.7×) in P2 QD archive cell-filling estimates for mage/controller archetypes.
- [ ] **Matt (if needed):** Discipline #18 candidate registration note (generation-side precondition for joint-gate) is informational; no decision required at this stage.

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-011-ablation-design.md` — primary subject (§1-§7 reviewed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-21-jack-ryan-gate1-w0-7-lc-011-ablation-design.md` — Gate-1 dispatch
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md` — LC-002 precedent (smoke-test BLOCK + amendment log)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-009-ablation-design.md` — LC-009 precedent (Option C; canonical decision tree §9)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (lines 50-218 — MAX_ITERATIONS, MODIFIER_SEARCH_FLOOR, LEVER_FLOOR_LOCK_WORKING_MODIFIER, Option B soft-disable constants)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (W0.10 boss-AI leash-reset fix; W0.10.5 empirical-close artifact; LC-011 pending section)
- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` (2026-05-19 Option A/B entries; 2026-05-21 Discipline #18 candidate registration)
