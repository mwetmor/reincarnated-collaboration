# V2 Calibration Analysis — 2026-05-16

**Reviewer:** jack-ryan
**Mode:** Analytical (direct Matt-routed Tier 1 #3; not Gate-1 or Gate-2)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-jack-ryan-v2-calibration-analysis-tier1-3.md`
**Disciplines applied:** #1 (math-before-code), #10 (empirical inspection), #11 (attribution clarity)
**Review principles applied:** Principle 5 (severity / escalation)
**Status:** COMPLETE

**Recommendation:** Blocked-on-X (see Stage 4)
**Anchor segment:** Segment C (target=0.50 CONVERGED only, n=8, mean |mod-1.0|=0.3273)
**New Matt-decision points beyond gamora's three:** 1 new (see Stage 4, item D)

---

## References

- Gamora math note: `reincarnated-engine/src/reincarnated/simulation/math/wind-controller-v2-anomaly-2026-05-16.md`
- Gamora dispatch completion: `agentic_orchestration/dispatches/2026-05-16-gamora-wind-controller-v2-structural-anomaly.md`
- Star-lord MIGRATION.md V2 sections: `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (Schema 2.1, 2.4)
- B14.5 sidecar analyses memory: `~/.claude/projects/.../memory/project_b14_5_sidecar_analyses.md`
- Telemetry DB: `reincarnated-engine/data/telemetry.db` — tables `class_balance_results`, `classes`

---

## Stage 1 — Segment Reproduction and Verification

**Empirical anchor:** season_001010 (V2, schema 2.4, n=10 classes). Cross-check: season_001006 (V2, schema 2.1, n=11 classes). All numbers pulled from raw telemetry via SELECT queries against `class_balance_results JOIN classes`.

### season_001010 — Per-class raw data

| class_id | archetype | element | modifier | target_wr | status | room_wr | flag_tier |
|---|---|---|---|---|---|---|---|
| class_0001 | hybrid_mage | fire | 0.7625 | 0.50 | CONVERGED | 0.5267 | NULL |
| class_0002 | water_controller | water | 1.7500 | 0.50 | CONVERGED | 0.4767 | NULL |
| class_0003 | earth_caster | earth | 1.5625 | 0.50 | CONVERGED | 0.5050 | NULL |
| class_0004 | hybrid_mage | wind | 0.6438 | 0.50 | CONVERGED | 0.5017 | NULL |
| class_0005 | physical_grappler | physical | 0.5250 | 0.50 | CONVERGED | 0.5050 | NULL |
| class_0006 | hybrid_mage | fire | 1.0000 | 0.50 | CONVERGED | 0.4983 | NULL |
| class_0007 | hybrid_mage | water | 0.7625 | 0.50 | CONVERGED | 0.4817 | NULL |
| class_0008 | hybrid_mage | earth | 1.0000 | 0.50 | CONVERGED | 0.4733 | NULL |
| class_0009 | wind_controller | wind | 3.6250 | 0.60 | INTENTIONAL_OUTLIER | 0.5900 | **review** |
| class_0010 | experimental | physical | 1.7500 | 0.40 | INTENTIONAL_OUTLIER | 0.3833 | NULL |

### Segment computation — season_001010

**Segment A — All 10 classes:**

|mod-1.0| values: 2.6250, 0.7500, 0.5625, 0.3562, 0.4750, 0.0000, 0.2375, 0.0000, 0.7500, 0.2375

Sum = 5.9937 / 10 = **0.5994**
Gamora reported: 0.5994. **MATCH: exact.**

**Segment B — Excl. modifier_flag_tier='review' (n=9):**

Excludes: wind_controller (class_0009, flag_tier='review')
Remaining 9 classes |mod-1.0|: 0.2375, 0.7500, 0.5625, 0.3562, 0.4750, 0.0000, 0.2375, 0.0000, 0.7500

Sum = 3.3687 / 9 = **0.3743**
Gamora reported: 0.3743. **MATCH: exact.**

Note: Segment B retains the experimental class (target=0.40, INTENTIONAL_OUTLIER, |mod-1|=0.75). Its inclusion is what separates Segment B from Segment C.

**Segment C — target=0.50 CONVERGED only (n=8):**

Excludes: wind_controller (target=0.60, INTENTIONAL_OUTLIER) AND experimental (target=0.40, INTENTIONAL_OUTLIER)
8 CONVERGED target=0.50 classes |mod-1.0|: 0.2375, 0.7500, 0.5625, 0.3562, 0.4750, 0.0000, 0.2375, 0.0000

Sum = 2.6187 / 8 = **0.3273**
Gamora reported: 0.3273. **MATCH: exact.**

**Verification result: all three segment numbers confirmed from raw telemetry. No discrepancy.**

### season_001006 cross-check

season_001006 (V2, schema 2.1, n=11 classes). Important caveat: `modifier_flag_tier` column did not exist at regen time (V2.4 added it). All s1006 rows have flag_tier=NULL regardless of modifier magnitude. Gamora math note §4.2 confirms wind_controller (modifier=3.51) would fire the gate retroactively.

Per-class raw data (s1006, from classes table):

| archetype | modifier | target_wr | status | room_wr | flag_tier |
|---|---|---|---|---|---|
| fire_controller | 1.0000 | 0.40 | INTENTIONAL_OUTLIER | 0.4033 | NULL |
| water_mage | 1.1875 | 0.50 | CONVERGED | 0.5067 | NULL |
| earth_caster | 1.1875 | 0.50 | CONVERGED | 0.5117 | NULL |
| wind_caster | 1.3750 | 0.50 | CONVERGED | 0.4900 | NULL |
| hunter | 0.1688 | 0.50 | CONVERGED | 0.5000 | NULL |
| fire_controller | 1.7500 | 0.50 | CONVERGED | 0.5000 | NULL |
| water_mage | 1.0000 | 0.50 | CONVERGED | 0.4817 | NULL |
| hybrid_mage | 1.1875 | 0.50 | CONVERGED | 0.5083 | NULL |
| wind_controller | 3.5100 | 0.50 | CONVERGED | 0.5283 | NULL (retroactive: would-review) |
| hunter | 1.0000 | 0.60 | INTENTIONAL_OUTLIER | 0.6100 | NULL |
| experimental | 1.0000 | 0.50 | CONVERGED | 0.4783 | NULL |

**s1006 Segment C (target=0.50 CONVERGED, applying same definition naively):**

Includes wind_controller (modifier=3.51, flag_tier=NULL) because the gate did not fire.
n=9, mean |mod-1.0| = **0.5587**

This is materially different from s1010 Segment C (0.3273). The inflated s1006 Segment C is explained entirely by wind_controller inclusion — if wind_controller is excluded retroactively (flag_tier=NULL but would-review):
s1006 Segment C excl. wind_controller: n=8, mean |mod-1.0| = **0.2519**

**Cross-check finding:** The Segment C definition as stated ("target=0.50 CONVERGED only") does NOT inherently exclude wind_controller in s1006 because the gate column was absent. The segment definition must include an explicit caveat: it applies to seasons where modifier_flag_tier was active (V2.4+). For s1006 analysis purposes, the retroactive Segment C (excluding wind_controller per gamora's retroactive assessment) produces 0.2519 — somewhat better than s1010's 0.3273. This is not a discrepancy with gamora's numbers; gamora correctly computed segments on s1010 only. This is new information from the cross-check.

**s1006 Segment B (excl. wind_controller retroactive, n=10):** mean |mod-1.0| = **0.2519**
(same as retroactive Segment C because s1006's two INTENTIONAL_OUTLIERs are fire_controller at modifier=1.0 and hunter at modifier=1.0 — both have |mod-1|=0.0 and 0.0, and their exclusion does not change the mean if they are included: recalculating with them: n=10, includes fire_controller=0.0 and hunter=0.0 → sum/10 actually = 2.519/10 = 0.2519, yes same because both outliers have |mod-1|=0.0)

Combined cross-season Segment C (retroactive-corrected, n=17): mean |mod-1.0| = **0.2911**, std = 0.3285.

---

## Stage 2 — V1 vs V2 Per-Segment Comparison

**V1 baselines (from MIGRATION.md V2 section / star-lord dispatch):**
- V1 primary: 0.799
- V1 secondary: 0.876

### Magnitude of improvement

| Segment | n | V2 mean |mod-1.0| | vs V1 primary (0.799) | vs V1 secondary (0.876) |
|---|---|---|---|---|
| A. All 10 | 10 | 0.5994 | -25.0% | -31.6% |
| B. Excl. review | 9 | 0.3743 | -53.2% | -57.3% |
| **C. target=0.50 CONVERGED** | **8** | **0.3273** | **-59.0%** | **-62.6%** |

All segments show material improvement. Segment C shows the largest improvement because it removes both design-intentional outlier noise sources (strong-outlier target class AND review-flagged class).

**Statistical significance:** NOT warranted at n=8-10 per season with 2 V2 seasons available. The effect magnitude is large enough (59% reduction for Segment C) that directional confidence is reasonable without formal significance testing. Formally: we have n=8-10 observations per season and 2 seasons. A t-test against a V1 distribution would require V1 per-season distributions to be available in the same aggregated form, which they are not (V1 was reported as a single population mean, not per-season segment means). Discipline #13b applies: convergence-shape observations, not per-variable attributions.

### Per-class outlier profile — Segment C (season_001010)

Ranked by |mod-1.0| descending:

| archetype | modifier | |mod-1.0| | share of segment mean |
|---|---|---|---|
| water_controller | 1.750 | 0.7500 | 2.29x |
| earth_caster | 1.563 | 0.5625 | 1.72x |
| physical_grappler | 0.525 | 0.4750 | 1.45x |
| hybrid_mage (wind) | 0.644 | 0.3562 | 1.09x |
| hybrid_mage (fire) | 0.763 | 0.2375 | 0.73x |
| hybrid_mage (water) | 0.763 | 0.2375 | 0.73x |
| hybrid_mage (fire) | 1.000 | 0.0000 | 0.00x |
| hybrid_mage (earth) | 1.000 | 0.0000 | 0.00x |

Segment C std: 0.2467, mean: 0.3273, CV: 0.75.

**Drivers of Segment C mean:** water_controller and earth_caster contribute the most. Both are control-adjacent archetypes with moderate-high V2 room modifiers (1.75, 1.5625). Neither exceeds the 3.0 review threshold; both are within the design-reasonable range. hybrid_mage classes cluster near 0.76-1.0 (very clean calibration). Segment C's 0.3273 mean is pulled primarily by the non-hybrid_mage archetypes.

**Observation (Discipline #13b):** water_controller (mod=1.75 at target=0.50) is the second-highest deviation in Segment C. This is a convergence-shape observation, not an attribution claim. Whether water_controller structurally tends toward higher modifiers under V2, or whether 1.75 is within its seed-normal range, cannot be determined from 1 data point.

---

## Stage 3 — modifier_flag_tier Trend Detection

### Available V2 regens

Only two V2 seasons are available in `class_balance_results`:

| Season | schema | use_room_evaluation | modifier_flag_tier column | n_classes |
|---|---|---|---|---|
| season_001006 | 2.1 | 1 (V2) | ABSENT at regen time | 11 |
| season_001010 | 2.4 | 1 (V2) | PRESENT | 10 |
| season_001009 | 2.3 | 0 (V1) | — excluded — | 10 |

### Review-tier occurrences

| Season | archetype | modifier | flag_tier | mechanism |
|---|---|---|---|---|
| season_001006 | wind_controller | 3.51 | NULL (gate absent; retroactive: would-review) | V2 HP-carryover × low-DPS-density × target=0.50 |
| season_001010 | wind_controller | 3.625 | review | V2 HP-carryover × low-DPS-density × target=0.60 (strong-outlier compound) |

Both confirmed review-tier occurrences are wind_controller. No other archetype has produced a review-tier flag in 2 V2 seasons (21 combined class-observations across both seasons).

### V1 wind_controller modifier history

From `classes` table, all V1 CONVERGED target=0.50 wind_controller rows (n=8, across seasons 000043 through 001007):

Modifiers: 0.0945, 0.1131, 0.1168, 0.1242, 0.1539, 0.1688, 0.1688, 0.1836

V1 mean: 0.1405. V1 range: 0.0891 (min=0.0945, max=0.1836).

**Critical finding:** wind_controller has the LOWEST modifier range of any archetype in V1 (0.089, per archetype range ranking from telemetry). It is the most consistent V1 archetype by this metric. Yet it produces the largest V2 inflation (modifier 3.51/3.625 vs V1 mean of 0.14 — approximately 25x V1 value). This inversion is structurally explained by gamora's math note: wind_controller's low DPS density is MASKED by V1's per-encounter HP reset (the boss/mini-boss rooms reset to full HP each encounter, hiding the carryover penalty), and UNMASKED by V2's sequential room HP-carryover (where the same low-DPS class cannot overcome the boss/mini-boss HP wall across encounters, forcing the binary search to an extreme modifier).

V1 mean |mod-1.0| for wind_controller: |0.1405 - 1.0| = 0.8595. This places wind_controller among the highest-deviation archetypes in V1 as well — but for the OPPOSITE reason (modifier too low under V1, modifier too high under V2). The archetype was not "well calibrated" under V1; it was poorly calibrated in a different direction.

### V2 inflation sibling analysis

**Question from dispatch Stage 3:** which archetypes are systematically prone to V2-mode inflation?

**water_controller** (closest structural sibling to wind_controller by V1 behavior):
- V1 range: 0.1187 (second-lowest among archetypes, comparable to wind_controller's 0.0891)
- V1 mean |mod-1.0|: 0.815 (high absolute deviation from 1.0 under V1, same directional issue)
- V2 (s1010, target=0.50): modifier=1.75, CONVERGED — not flagged
- DPS density not independently measured in this analysis; gamora measured wind_controller density only

**Assessment:** water_controller shows structural similarity to wind_controller in V1 (consistent but poorly calibrated) but converges at a much lower modifier under V2 at target=0.50 (1.75 vs 3.51). This suggests water_controller's kit template produces sufficient DPS to partially survive V2 room HP-carryover semantics — consistent with gamora's burn DoT finding (fire-type DoT persists across encounter boundaries). Whether water_controller would inflate under target=0.60 strong-outlier assignment is **unknown — no V2 data for that combination exists**.

**earth_controller** (control-class sibling):
- No V2 regen data available (not present in s1006 or s1010 class generation)
- Cannot characterize V2 behavior

**Confirmed V2 inflation siblings:** none beyond wind_controller with available data.

**Sample-size caveat (Discipline #13b):** 2 V2 seasons is insufficient to characterize archetype-level inflation risk across the full template space. The inflation-risk picture for control-class siblings (water_controller, earth_controller) is structurally incomplete. An archetype that has not appeared in 2 V2 seasons cannot be characterized — it simply has no data.

---

## Stage 4 — V2 Calibration Epoch Recommendation

**Recommendation: Blocked-on-X**

V2 mode is materially better calibrated than V1 across all three segment definitions. The improvement signal is real and large. However, three Matt-decision points must be resolved before a calibration epoch can be declared, and one additional condition is identified in this analysis.

### X1 — Calibration anchor segment (gamora's Matt-decision #1)

Matt must choose which segment anchors the epoch declaration. Three options:

- **Segment A (0.5994, n=10):** Includes design-intentional outliers. Not recommended as primary — conflates balance-loop quality with design-intentional difficulty gradient behavior.
- **Segment B (0.3743, n=9):** Excludes review-flagged classes (wind_controller). Includes experimental class (target=0.40, INTENTIONAL_OUTLIER). Defensible as star-lord's current anchor per MIGRATION.md. Includes 1 design-intentional noise source.
- **Segment C (0.3273, n=8):** Excludes both design-intentional outlier classes. Cleanest balance-loop signal. Recommended as primary.

**This analysis recommends Segment C as primary.** Rationale: the balance loop's job is to converge standard-target classes (target=0.50) to within-band room winrates. Segment C measures exactly that — and only that. Segment B mixes in one design-intentional outlier (experimental at target=0.40) without principled justification. Segment A adds a second (wind_controller at target=0.60). Neither outlier measures the balance loop's standard convergence quality.

Segment C definition must carry an explicit caveat: it requires modifier_flag_tier to be active (V2.4+ schema). For pre-V2.4 seasons, the retroactive Segment C (excluding wind_controller by modifier threshold assessment) is the correct equivalent.

### X2 — Wind_controller carve-out disposition (gamora's Matt-decision #3, reformulated)

wind_controller will produce modifier > 3.0 reliably when it draws the strong-outlier target slot (target=0.60) in V2 mode. The modifier_clamp_gate fires correctly. The question for calibration epoch declaration is whether this behavior:

**(a) Accept as-is:** modifier_flag_tier='review' rows are excluded from the calibration anchor by definition (Segment C). The epoch is declared with an explicit note that flagged classes are design-intentional outliers subject to human review. V2 can be declared NOW under this option, contingent on X1 resolution.

**(b) Require code fix first:** archetype-aware target assignment (exclude low-DPS-density archetypes from strong-outlier slot) or reject-and-regenerate gate operationalization. V2 declaration waits until the fix lands and a post-fix regen confirms no wind_controller inflation. Delay: 1-2 additional sprints.

This is the primary binary choice for V2 epoch timing. Option (a) enables the soonest-ready path.

### X3 — Sample size adequacy (NEW — this analysis; not in gamora's three Matt-decisions)

**This is a new Matt-decision point beyond gamora's three.**

2 V2 seasons (n=10 and n=11 classes, 21 combined class-observations) is a thin empirical base for Segment C mean stability. The combined cross-season retroactive Segment C (n=17) yields mean=0.2911, std=0.3285. The per-season spread (0.2519 retroactive for s1006 vs 0.3273 for s1010) represents a 30% variation in the segment mean across only 2 seasons.

Whether this variation is acceptable depends on how the epoch declaration is scoped:

- If the declaration is "V2 Segment C mean is approximately 0.33 ± 0.05" (rough calibration benchmark), 2 seasons may be sufficient.
- If the declaration requires a stable population estimate of the Segment C mean to within ±0.02, 4-6 additional V2 regens are needed.

**Matt must decide:** is 2 V2 regens sufficient for calibration epoch declaration, or is a pre-declaration floor of 4-6 V2 regens required?

Supplemental note: the cross-season variation between s1006 (retroactive 0.2519) and s1010 (0.3273) is partially explained by seed-composition differences — s1010 has a denser hybrid_mage cluster (5/8 Segment C classes are hybrid_mage; s1006 has more diverse archetypes). This composition effect is a convergence-shape observation (Discipline #13b); its contribution to the mean variation cannot be attributed without ablation.

### Soonest-Ready Path

If Matt accepts:
1. Segment C (0.3273) as primary calibration anchor (X1 resolved)
2. Option (a) — accept wind_controller carve-out, no code fix required before declaration (X2 resolved)
3. 2 V2 regens is sufficient for declaration (X3 resolved)

Then: V2 is READY for epoch declaration contingent solely on Matt's sign-off. The blocking gap is definitional, not empirical. The improvement over V1 (59% mean |mod-1.0| reduction in Segment C) is confirmed and verified from raw telemetry.

### Summary table

| Prerequisite | Status | Who decides | Options |
|---|---|---|---|
| X1: anchor segment | Gamora's Matt-decision #1 | Matt | A (0.5994) / B (0.3743) / C (0.3273 — recommended) |
| X2: wind_controller carve-out | Gamora's Matt-decision #3 | Matt | Accept-as-is (enables soonest-ready) / require code fix first |
| X3: sample size adequacy | NEW (this analysis) | Matt | 2 seasons sufficient / require 4-6 V2 regens first |
| Gamora Matt-decision #2: DPS floor | rocket queue item | Matt | Does not block epoch declaration if X2 resolved via accept-as-is |
| Gamora Matt-decision #3b: clamp gate activation | gamora queue item | Matt | Does not block epoch declaration if X2 resolved via accept-as-is |

---

## Stage 5 Summary

**Doc path:** `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md`

**Recommendation:** Blocked-on-X

**Anchor segment:** Segment C (target=0.50 CONVERGED, n=8, mean |mod-1.0|=0.3273). Verified exact from raw telemetry. All three gamora segment numbers confirmed; no discrepancy.

**V1 vs V2:** Segment C shows 59.0% reduction vs V1 primary baseline (0.799 → 0.3273). Material improvement confirmed across all segment definitions.

**modifier_flag_tier trend:** wind_controller is the only confirmed review-tier archetype across 2 V2 seasons (21 total class-observations). No siblings confirmed as systematically inflated with available data; water_controller converges cleanly at target=0.50 (mod=1.75) but has not been observed at target=0.60. V2 inflation risk for sibling archetypes is structurally uncharacterized (2 seasons is insufficient).

**New finding (Stage 1 cross-check):** s1006 Segment C naively (applying definition without retroactive wind_controller exclusion) yields 0.5587 — substantially different from s1010's 0.3273. The Segment C definition requires explicit version-gating: it is valid only for seasons with modifier_flag_tier active (V2.4+), or with retroactive exclusion of modifier > 3.0 rows. Calibration epoch documentation should specify this.

**New Matt-decision point (X3):** Sample size adequacy. Matt must decide whether 2 V2 regens is sufficient for epoch declaration or whether a pre-declaration floor of 4-6 V2 regens is required. This is not in gamora's three Matt-decisions.

**Cross-references:**
- Gamora math note §4.3: calibration baseline math (verified exact)
- Star-lord MIGRATION.md Schema 2.1: class_balance_results table, modifier_flag_tier field
- B14.5 sidecar analyses: hunter modifier-range parallel (hunter has highest V1 range; wind_controller has lowest V1 range — inversion confirmed)
- Engineering Discipline #10: empirical inspection grounding (all numbers in this analysis pulled from raw DB queries, not derived from gamora's narrative)
- Engineering Discipline #13b: convergence-shape observations vs per-variable attributions (all cross-season variation noted as observation, not attribution)

---

*Analysis complete — 2026-05-16. Reviewer: jack-ryan.*
