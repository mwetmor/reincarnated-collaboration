# Dispatch — 2026-05-16 — jack-ryan — V2 calibration analysis (Tier 1 #3)

**From:** knight-rider (authored per gamora wind_controller V2 anomaly investigation return 2026-05-16; recommended jack-ryan calibration analysis routing with Segment C anchor)
**To:** jack-ryan
**Approved by:** Matt at 2026-05-16 Day 4 ("fire jack ryan now")
**Status:** PENDING
**Mode:** Analytical (jack-ryan operates analytical-only per persona; no code authorship)
**Estimated effort:** 1 session (~2-3h)
**Gate-1 bypass rationale:** N/A — jack-ryan IS the Gate-1 reviewer; this dispatch is direct Matt-routed analytical work.

**Acceptance summary:** V2 calibration analysis filed at `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md`. Three segments documented (A/B/C per gamora's framing). Primary anchor: Segment C (target=0.50 CONVERGED, n=8, mean |mod-1.0|=0.3273). Secondary reference: Segment B (excl. flag_tier='review', n=9, mean=0.3743). Comparison to V1 baseline. Modifier-anomaly trend detection across regens using `modifier_flag_tier='review'` rows (V2.4 schema field). Recommendation on V2 calibration epoch declaration: ready / blocked-on-X / requires-Y-data.

---

## Why this dispatch exists

V2 mode (room HP-carryover evaluation) is materially better calibrated than V1 mode. Star-lord's V2 CLI flag + regen completion 2026-05-16 documented:
- V1 baseline: mean |mod-1.0| = 0.799 / 0.876
- V2 (all 10): 0.5994
- V2 (excl. wind_controller flag): 0.3743

Gamora's wind_controller investigation returned 2026-05-16 with a refined three-segment framing:

| Segment | n | mean \|mod-1.0\| | Notes |
|---|---|---|---|
| A. All 10 | 10 | 0.5994 | star-lord MIGRATION.md primary |
| B. Excl. flag_tier='review' | 9 | 0.3743 | star-lord secondary anchor |
| **C. target=0.50 CONVERGED only** | **8** | **0.3273** | **Cleanest balance-loop signal** — separates design-intentional outliers from convergence quality |

V2 calibration epoch declaration is the standing question. Your analysis grounds whether V2 mode can be promoted to primary balance-loop evaluation, and if so, on what basis.

## Cross-seam contract change?

**Round-trip: not applicable** — jack-ryan analytical work produces a `qa/analyses/` doc; no schema or contract change; no production code modified. Per R11(b) Principle 6.

## What this dispatch produces

### Stage 1 — Calibration-segment reproduction + verification

Pull the V2 mode telemetry from season_001010 (and season_001006 for cross-check):
- Per-class final modifier
- target_winrate per class
- room_winrate at convergence
- modifier_flag_tier (V2.4 schema field; "review" = clamp-gate-flagged outlier)
- Convergence status (CONVERGED / INTENTIONAL_OUTLIER / etc.)

Compute each segment's mean |mod-1.0| from raw telemetry. Verify gamora's numbers (0.5994 / 0.3743 / 0.3273). Flag any discrepancy.

### Stage 2 — V1 vs V2 segment-wise comparison

Compare V2 segments to V1 baseline (0.799 / 0.876 per MIGRATION.md). Per segment:
- Magnitude of improvement (ratio + absolute)
- Statistical significance (if your sample sizes support it — 8-10 classes per season is small; flag if significance testing is not warranted at this n)
- Per-class outlier profile (which classes drive each segment's mean?)

### Stage 3 — Cross-regen trend detection via modifier_flag_tier

Star-lord's V2.4 schema persists `modifier_flag_tier` for clamp-gate-flagged classes. Query `class_balance_results` for `modifier_flag_tier='review'` rows across all available V2 regens (currently season_001006 + season_001010 — small sample, but a starting trend).

For each flagged class:
- How many V2 occurrences?
- Modifier magnitude per occurrence
- Cross-occurrence consistency (structural vs seed)
- Comparison to V1 modifier history for the same class (per B14.5 sidecar — 15+ historical V1 seasons available)

Surface: which archetypes appear systematically prone to V2-mode inflation. Gamora's wind_controller analysis is the canonical first instance; identify any siblings.

### Stage 4 — V2 calibration epoch recommendation

Synthesize a recommendation:
- **Ready** — V2 mode can be declared the primary calibration epoch. Anchor segment + rationale.
- **Blocked-on-X** — V2 cannot be declared until X is resolved. X = what specifically (the three Matt-decisions gamora surfaced? more regens for trend confidence? additional flagged-archetype investigations?).
- **Requires-Y-data** — V2 promotion needs Y additional empirical input (more regens / additional archetypes regened / longitudinal modifier_flag_tier accumulation).

Surface Matt-decision points explicitly.

### Stage 5 — File at qa/analyses/

Output path: `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md`

Required content:
- Three segments documented + verified (with raw telemetry citations)
- V1 vs V2 comparison per segment
- Modifier-flag-tier trend findings (sample-size caveats explicit)
- V2 calibration epoch recommendation (Ready / Blocked / Requires-data)
- Matt-decision points
- Cross-references to: gamora math note (`simulation/math/wind-controller-v2-anomaly-2026-05-16.md`), star-lord MIGRATION.md V2 section, B14.5 sidecar analyses

## Out of scope (explicit)

- **NO code authorship.** Jack-ryan is analytical-only per persona.
- **NO new dispatch authoring.** Jack-ryan surfaces recommendations; knight-rider routes follow-ons.
- **NO architectural / discipline-change proposals.** Beyond what flows directly from this analysis. (Discipline-extension candidates remain knight-rider + jack-ryan critique-pair work in their normal channel.)
- **NO B14.5 V2 priority restructuring.** That's gamora + Matt scoping; surface if the data warrants but do not propose.
- **NO follow-on gamora / rocket dispatch authoring.** Three Matt-decisions already surfaced from gamora's investigation; this analysis informs them but does not duplicate them.
- **NO claim of V2 calibration epoch declaration.** Recommend only; Matt declares.

## Required reading

- Gamora wind_controller math note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wind-controller-v2-anomaly-2026-05-16.md`
- Gamora wind_controller dispatch completion record: `agentic_orchestration/dispatches/2026-05-16-gamora-wind-controller-v2-structural-anomaly.md`
- Star-lord V2 CLI flag + regen dispatch completion record + MIGRATION.md V2 section
- B14.5 sidecar analyses (hunter modifier-range parallel case; 15+ historical seasons context)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code; applies to analysis too), #9 (range-check over equality-pin), #10 (empirical inspection over assumption)

## Acceptance criteria

- [ ] Doc filed at `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md`
- [ ] Three segments verified from raw telemetry; any discrepancy with gamora's numbers flagged
- [ ] V1 vs V2 per-segment comparison present
- [ ] modifier_flag_tier trend detection across available V2 regens
- [ ] V2 calibration epoch recommendation present (Ready / Blocked / Requires-data) with Matt-decision points framed
- [ ] Cross-references to gamora math note + star-lord MIGRATION.md + B14.5 sidecar
- [ ] Knight-rider notified with: doc path, recommendation outcome, any new Matt-decision points beyond gamora's three

## Tag policy

- **No git tag** (jack-ryan analytical output; persona convention is qa/findings/ + qa/analyses/ file-timestamp traceability suffices)

---

## Completion record

**Completed:** 2026-05-16
**Doc path:** `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md`
**Recommendation:** Blocked-on-X (three Matt-decisions required; soonest-ready path described in Stage 4)
**Anchor segment:** C (target=0.50 CONVERGED only, n=8, mean |mod-1.0|=0.3273 — verified exact from raw telemetry)

**Notes for knight-rider:**

1. **All three gamora segment numbers verified exact.** No discrepancy. Raw telemetry confirms 0.5994 / 0.3743 / 0.3273 to four decimal places.

2. **New Matt-decision point (X3) surfaced beyond gamora's three.** Sample size adequacy: Matt must decide whether 2 V2 regens is sufficient for epoch declaration or whether a pre-declaration floor of 4-6 V2 regens is required. The per-season Segment C mean varies 30% across 2 seasons (retroactive s1006: 0.2519; s1010: 0.3273). Not a blocking concern if Matt accepts rough calibration benchmarking, but if a tight population estimate is required, more regens are needed first.

3. **New finding: Segment C definition requires explicit version-gating.** For pre-V2.4 seasons (e.g., s1006), applying Segment C naively includes wind_controller (flag_tier=NULL) and inflates the mean to 0.5587. The definition must specify: "target=0.50 CONVERGED AND (modifier_flag_tier IS NULL OR modifier_flag_tier != 'review')." This was implicit in gamora's definition but becomes important when comparing across seasons with different schema versions. Calibration epoch documentation should specify this.

4. **Soonest-ready path documented in Stage 4.** If Matt accepts (a) Segment C as anchor, (b) wind_controller carve-out accept-as-is (no code fix required), (c) 2 V2 regens sufficient — V2 is READY for epoch declaration contingent solely on Matt sign-off. The 59% Segment C improvement over V1 is confirmed.

5. **wind_controller is the only confirmed V2 review-tier archetype.** No siblings confirmed as systematically inflated. water_controller converges cleanly at target=0.50 (mod=1.75, not flagged) but has not been observed at target=0.60. Sibling risk is structurally uncharacterized with 2 V2 seasons.

6. **V1 inversion finding (context for Matt).** wind_controller was among the highest |mod-1.0| archetypes under V1 as well (V1 mean modifier=0.14, so |0.14-1.0|=0.86), but for the OPPOSITE reason: V1 converged it to an extremely LOW modifier. V2 produces an extremely HIGH modifier. The archetype was poorly calibrated under both evaluation modes but in opposite directions. This is relevant framing for the DPS floor and archetype template follow-on items.
