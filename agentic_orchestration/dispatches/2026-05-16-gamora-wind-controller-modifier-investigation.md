# Dispatch — 2026-05-16 — gamora — wind_controller modifier 3.51 anomaly investigation (V2-HP-carryover-specific pure-control archetype dynamics)

**From:** knight-rider (authored per star-lord regen recovery cross-seam flag #2 — surfaced 2026-05-16 Day 4)
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4 explicit "author 2 gamora dispatches" directive
**Status:** PENDING — ACTIVE
**Estimated effort:** 1-2 sessions (~3-6 hours); math-before-code investigation per Discipline #1; analytical work + finding-filing primary deliverable; mitigation execution only if root cause is unambiguous + fix is small + within your seam.
**Acceptance:** Math note describing the empirical picture of wind_controller (class_0009) under V2 HP-carryover; root-cause hypothesis with evidence; comparison against pre-V2 behavior + the doppelganger gate re-run HIGH-signal verdict (which used pre-B6+V2 substrate); mitigation path proposed (in-scope to ship if small AND unambiguous; otherwise file findings + queue follow-on); findings file at `agentic_orchestration/qa/findings/2026-05-16-gamora-wind-controller-modifier-rootcause.md`.

---

## Context — what star-lord discovered

Per star-lord's regen recovery findings (`agentic_orchestration/qa/findings/2026-05-16-star-lord-full-regen-post-b6-v2.md`):

> **Anomaly: wind_controller (class_0009) modifier = 3.51** — binary search converged correctly (room_winrate = 0.528), but required extreme modifier inflation under V2 HP-carryover semantics. This single class inflates the cohort mean substantially.

**The numerical context:**

| Cohort | mean \|mod-1.0\| |
|---|---|
| V1 calibration epoch (pre-B6, pre-V2) — historical baseline | 0.799 |
| V2 smoke (5-class) | 0.3175 |
| Prior 001005 regen (pre-B6, pre-V2 substrate) | 0.7523 |
| **001006 all-11 (post-B6, post-V2)** | **0.457** |
| 001006 CONVERGED non-experimental (n=8) | 0.629 |
| **001006 excl. wind_controller anomaly (n=7)** | **0.270** |

The 001006 0.457 → 0.270 (ex-anomaly) gap shows wind_controller's modifier 3.51 is **a single-class outlier substantially inflating the cohort mean**. 3.51 is an order of magnitude above the typical modifier range (0.09-0.52 per the calibration epoch).

**The interesting puzzle:**

Per the earlier gamora doppelganger gate re-run (committed findings; HIGH-signal verdict), the pure-control archetypes (wind_controller, earth_controller, fire_controller, water_controller) all landed in the **30-50% mirror-match WR band** at ENCOUNTER-level — HIGH signal indicating "thematic damage is solved at a different layer" per the ailment-damage-signatures memory note framework.

But that was on substrate generated at `b15ecb2` (pre-B6, pre-V2). Now on substrate generated at HEAD (post-B6, post-V2) under V2 sequential-room semantics, wind_controller's CONVERGENCE behavior is fine (room_winrate 0.528, well-centered on V2's 0.50 target) but **requires modifier 3.51 to achieve it.** Different empirical signal entirely.

The hypothesis space:
- **(a) V2 HP-carryover specifically penalizes pure-control archetypes** — pure-control kits have low DPS density; under HP-carryover semantics, the cumulative cost of clearing 3 encounters compounds against them more than V1 encounter-independent semantics. Binary search compensates by inflating the modifier.
- **(b) B6 pre-work + V2 interaction creates the anomaly** — B6 pre-work shifted rage/physical archetype tier ranges (per `rocket/v1.3-b6-energy-type-tiers @ 639ac3d`); the wind_controller's tier stayed at mana baseline (5.75 → tier 50). Maybe the wind_controller's specific kit composition under post-B6 substrate generation produced a low-DPS-density outcome that V2 then penalizes.
- **(c) Per-fight randomness or seed-specific outcome** — could be 001006-seed-specific; doesn't reproduce on fresh seeds.
- **(d) Other** — surfaced during investigation.

## What this dispatch does

This is a **math-before-code investigation** (Discipline #1). Three nested questions:

### Q1 — Reproduce + characterize empirical picture

1. Query telemetry DB for season_001006 wind_controller (class_0009): per-encounter HP curves; per-room outcomes; per-class skill composition; comparison to other pure-control archetypes in the same regen
2. Compare to season_001005 wind_controller (pre-B6, pre-V2 substrate): per-encounter behavior; modifier landing; doppelganger HIGH-signal context
3. Empirical question: is the wind_controller's modifier 3.51 specifically related to (a) V2 HP-carryover penalizing its DPS density, (b) post-B6 generation producing a different kit, (c) seed-specific outcome, or (d) other?

### Q2 — Investigate the V2-HP-carryover-specific dynamics for pure-control

If Q1 lands on hypothesis (a), characterize how V2 HP-carryover specifically interacts with pure-control archetype kit composition:
- How does cumulative HP attrition across N=3 encounters compound for pure-control vs other archetypes?
- Does the wind_controller's specific kit composition (knockback + chill + low-damage primary) produce a degenerate case under V2 semantics?
- Is this an archetype-class-level concern (all wind_controllers degenerate) OR a per-class kit-composition issue (this specific seed's wind_controller has a degenerate kit)?

### Q3 — Compare against pre-V2 doppelganger HIGH-signal evidence

The doppelganger gate re-run HIGH-signal verdict suggested pure-control archetypes were architecturally healthy (no ailment-damage-signatures needed). Now wind_controller's modifier 3.51 suggests V2 specifically broke something for this archetype. Reconcile:
- Is the prior doppelganger evidence still valid post-V2? (Both can be true if doppelganger is encounter-level + V2 introduces room-level dynamics.)
- Does the ailment-damage-signatures deferral need re-litigation post-V2-anomaly? (Per the ailment-deferral entry's "indefinite deferral" framing + the "design-polish queue" routing, the deferral was based on doppelganger HIGH-signal at encounter-level — the V2-room-level wind_controller anomaly is a distinct empirical surface.)

## What to produce

Math note + findings file. Specifically:

1. **Empirical picture** — Q1 reproduction; per-encounter HP curves; kit composition analysis; cross-class comparison
2. **Q1 resolution** — hypothesis (a) / (b) / (c) / (d) with evidence
3. **Q2 resolution** — V2-HP-carryover-specific dynamics characterization (if Q1 lands on (a))
4. **Q3 resolution** — reconciliation with doppelganger HIGH-signal; ailment-deferral-revisit recommendation if warranted
5. **Mitigation proposal** — one of:
   - **(a)** Generation-side fix (rocket dispatch territory if so — e.g., wind_controller kit composition adjustment)
   - **(b)** Simulation-side fix (your seam — e.g., V2 HP-carryover semantic refinement for pure-control)
   - **(c)** Per-fight variance tuning (small mitigation; preserves the architectural commitments)
   - **(d)** Accept as known-anomaly + flag in calibration-epoch addendum (no fix; just document)
   - **(e)** Other path surfaced during investigation
6. **Recommendation for knight-rider** — does the ailment-damage-signatures deferral need re-litigation?

## What this dispatch does NOT do

- **No re-running the regen.** Use existing telemetry DB for season_001006 + season_001005.
- **No modifications to generation seam.** If Q1 lands on hypothesis (b), file findings + queue rocket dispatch; do NOT touch rocket's seam.
- **No re-litigation of cipher-width or form-bias decisions.** This investigation is bounded to the wind_controller anomaly + its V2 dynamics.
- **No new ailment-damage-signatures dispatch.** If your investigation surfaces that the ailment deferral needs re-litigation, file as a finding; knight-rider authors the re-litigation dispatch if warranted.
- **No full B14.5 V2 redesign.** Even if mitigation surfaces, it's bounded to the wind_controller anomaly; V2's broader convergence semantics remain operative.

## Required reading

- `agentic_orchestration/qa/findings/2026-05-16-star-lord-full-regen-post-b6-v2.md` (star-lord's regen recovery findings — the empirical basis for this investigation)
- `agentic_orchestration/qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md` (your own prior doppelganger HIGH-signal findings — the encounter-level evidence to reconcile against)
- `agentic_orchestration/dispatches/2026-05-16-gamora-b10-v2-sequential-room.md` (your own B10 V2 dispatch + math note + completion record)
- `reincarnated-engine/src/reincarnated/simulation/math/b10-v2-sequential-room-convergence.md` (your own V2 math note)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 entries (calibration epoch `c000d7d`; ailment-deferral `680a3f1`; engine-balance-stewardship `5d51b5a`; movement-speed + spatial-data committed this turn at `303258c`)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_ailment_damage_thematic.md` (ailment-damage-signatures memory note — design-polish-queue framework; relevant if Q3 surfaces re-litigation)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code; primary discipline for this investigation), #11 (attribution: cite star-lord findings + V1 calibration-epoch baseline + doppelganger HIGH-signal verdict), #12 (semantic-shifting: V2 HP-carryover is a semantic shift relative to V1; the wind_controller anomaly may surface as a semantic-shift-induced edge case), #13b (outcome attribution opacity: the anomaly's cause is uncertain; framing as hypothesis-pending-investigation is the right discipline)

## Acceptance criteria

- [ ] Math note filed at `reincarnated-engine/src/reincarnated/simulation/math/wind-controller-modifier-rootcause.md` (or equivalent)
- [ ] Q1 reproduction + characterization complete (per-encounter HP curves; kit composition; cross-class comparison)
- [ ] Q1 / Q2 / Q3 each have explicit resolution (or noted as "couldn't resolve, here's what's needed")
- [ ] Mitigation proposal with rationale (one of (a)-(e) above)
- [ ] Recommendation on ailment-deferral re-litigation (warranted Y/N with reasoning)
- [ ] Findings file filed at `agentic_orchestration/qa/findings/2026-05-16-gamora-wind-controller-modifier-rootcause.md`
- [ ] If shipping mitigation in-session: smoke test + intermediate tag + MIGRATION.md if cross-seam-visible
- [ ] Knight-rider notified at completion with mitigation status + ailment-deferral-revisit recommendation + cross-seam implications

## Cross-seam considerations

- **Rocket:** READ-ONLY for this investigation. If Q1 lands on hypothesis (b), file findings + queue rocket dispatch via knight-rider; do NOT modify rocket's seam.
- **Star-lord:** READ-ONLY (star-lord's telemetry + findings are your data source). If the investigation reveals telemetry insufficient for the diagnostic (e.g., need additional v2.1 fields beyond the post-fix state), file finding; do NOT modify star-lord's seam.
- **Gandalf:** secondary reviewer if the investigation surfaces ailment-deferral re-litigation (gandalf has design-instinct lineage on the deferral question); knight-rider routes if you flag.
- **Knight-rider:** notify at completion; if your recommendation includes ailment-deferral re-litigation, knight-rider drafts the re-litigation dispatch.
- **Drax:** out of seam.

## Tag policy

- If shipping mitigation in-session: intermediate tag `gamora/v1.3-wind-controller-modifier-fix` at the commit closing the fix.
- If no mitigation in-session (analytical findings only): no tag.
- **Milestone tag:** none from this dispatch. Standard ADR-003 protocol.

---

## Completion record

**Completed:** 2026-05-16
**Math note path:** `reincarnated-engine/src/reincarnated/simulation/math/wind-controller-modifier-rootcause.md`
**Findings file path:** `agentic_orchestration/qa/findings/2026-05-16-gamora-wind-controller-modifier-rootcause.md`
**Q1 resolution (hypothesis a/b/c/d):** Primary (a), secondary (b-partial), partial (c-partial). V2 HP-carryover semantics compound against wind_controller's low DPS density (25% of kit is damage-producing). The s001006 generator produced a lower-DPS-density kit than s001005 (contributing secondary factor). The specific modifier magnitude 3.51 is seed-specific (c-partial), but the direction of inflation is structural. Hypothesis (d) not surfaced.
**Q2 resolution:** Room-level convergence arithmetic with 2/6 guaranteed-zero slots (boss + mini-boss) forces the 4 swing slots to average 0.75 room WR. Wind_controller's low DPS density causes long fight durations → high per-encounter HP cost → severe HP-carryover compounding across N=3 sequential encounters → collapsed room WR at moderate modifiers. Binary search pushes to 3.51 to drive magic rooms to ceiling (1.0). The modifier inflation is mechanically correct behavior; it is the balance loop's accurate compensation for a structurally DPS-sparse kit under V2 room semantics.
**Q3 resolution + ailment-deferral re-litigation recommendation:** Doppelganger HIGH-signal verdict (encounter-level 0.487 WR) is fully reconciled with V2 modifier anomaly (room-level). These measure different mechanics — encounter-level 1v1 vs room-level sequential survival with HP carryover. Both are correct. Ailment-deferral re-litigation: NOT recommended. Ailment-damage-signatures are flavor-tier (5-10% of skill magnitude); the V2 gap requires structural DPS density fixes, not flavor ticks. Indefinite deferral stands.
**Mitigation path proposed (a/b/c/d/e):** (d) Accept as known anomaly + calibration-epoch addendum. Two queued follow-on items: (1) rocket dispatch for minimum DPS floor in pure-control archetype templates (requires Matt sign-off); (2) future gamora dispatch for modifier clamp gate operationalization [0.15, 2.5] (requires Matt sign-off on reject-and-regenerate behavior).
**Mitigation shipped in-session (Y/N):** N — analytical findings only. No code changes.
**Intermediate tag (if any):** None (analytical dispatch; no tag per dispatch tag policy).
**Notes for knight-rider:** (1) Ailment-deferral stays indefinite — no action needed. (2) Calibration-epoch addendum should document: pure-control modifier may exceed 2.5 under V2 in extreme seeds (observe-only); boss/mini-boss ROOM WR = 0.0 for all classes in high-difficulty seasons is expected behavior. (3) Two follow-on items queued above require Matt routing before dispatch authoring. (4) No commit-coordination friction with parallel V2.1 emission-gap-fix dispatch (zero code changes in this dispatch). (5) The modifier 3.51 is outside the [0.15, 2.5] observe-only clamp; `would_pass_clamp: false` is already recorded in the class JSON — no additional instrumentation needed.
