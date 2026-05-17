# Dispatch — 2026-05-16 — gamora — Combined post-cascade evaluation regen (wind_controller Decisions 2+3 evaluation + MS coherence re-check + element pool-cull validation)

**From:** knight-rider (authored per Matt directive Day-4 close: "Option A" for combined wind_controller + MS regens; EXTENDED per Matt Day-4 close: "include the element adjustments" — element pool-cull + selector hard-floor outputs roll into same regen. Net: collapses 3-4 separate regens into 1 combined post-cascade pass.)
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** QUEUED — fires after ALL of: (a) your in-flight Gate 3b sim consumption returns; (b) drift-14 audit cascade completes (legolas Track A `2026-05-16-legolas-track-a-pool-vfx-catalogue-coverage-audit.md` + gandalf Track B authoring + IF Track B recommends, rocket selector hard-floor amendment). Rocket DPS-floor already returned clean (`rocket/v1.3-wind-controller-dps-floor @ 2d22486`). All cascade items must land BEFORE this regen fires — regenning before any cascade item lands wastes the regen.
**Estimated effort:** 1 session (~2-3h); single regen + multi-dimensional analysis pass (MS coherence + wind_controller DPS-floor evaluation + element-pool-cull validation in one regen)

**Gate-1 bypass rationale:** Matt-directed (Option A explicitly confirmed); single-seam (gamora simulation); reversible (analytical regen — does not modify production data); follows Discipline #2 + R11(b) Principle 6 standards.

**Acceptance summary:** Single fresh V2-mode regen consuming the FULL Day-4 cascade state: (a) rocket DPS-floor template change for wind_controller + (b) rocket MS schema-defaults (player 8.0 / fast 7.5 / trash 5.75 / AI_SPEED_MULTIPLIER 0.719) + (c) gamora's own Gate 3b sim consumption (kiting math + 3-band distance state) + (d) **element pool-cull adjustments per Drift-14 audit cascade** (gandalf Track B output; possibly rocket selector hard-floor amendment if Track B recommends). Per-class modifier table + per-class Segment C metrics + wind_controller-specific report + **element-pool-cull validation report** (does the culled pool emit cleanly through engine? do canonical-pair-leak metrics improve at LLM-bound paths?). Recommendation on Decisions 2/3 (clamp gate; strong_outlier_compatible tag) per gandalf sequencing framework. MIGRATION.md cross-reference. Tag.

---

## Why this dispatch exists

Per Matt's Option A confirmation (Day-4 close):

> "Let Gate 3b complete its current regen; queue a SECOND combined regen after rocket DPS-floor lands for the wind_controller validation. Net: 2 regens total (Gate 3b kiting + combined post-cascade for MS coherence + wind_controller Decisions 2/3 evaluation in single pass), saves 1-2 vs original plan."

Your prior wind_controller V2 anomaly investigation classified the anomaly as Kit-design-structural-compound (Factor A archetype-level inflation + Factor B strong-outlier target slot). Gandalf's Decision-1 (rocket DPS-floor) just shipped (tag `rocket/v1.3-wind-controller-dps-floor @ 2d22486`); jack-ryan's V2 calibration confirmed Segment C (target=0.50 CONVERGED, excl. flag_tier='review') as cleanest anchor at 0.3273. Math note §6 estimate: wind_controller modifier drops 3.51 → ~2.0-2.8 at target=0.50 with the 3-floor template change.

This dispatch empirically validates whether that estimate holds + measures Decisions 2/3 activation conditions.

## Cross-seam contract change?

**Round-trip: not applicable** — analytical regen consuming existing upstream contracts; no new emission fields; no schema changes; balance-loop convergence math IS the consumer. Per R11(b) Principle 6.

## What this dispatch produces

### Step 1 — Fresh V2-mode regen (full Day-4 cascade)

Run V2 mode regen consuming the FULL Day-4 cascade state:
- Rocket DPS-floor (3-floor wind_controller constraint; tag `2d22486`)
- Rocket MS schema-defaults (player 8.0; fast 7.5; trash 5.75; AI_SPEED_MULTIPLIER 0.719)
- Your Gate 3b sim consumption (kiting math + 3-band distance state; tag pending Gate 3b return)
- Existing star-lord cascade (Stage B export-DTO + V2.4 telemetry + Stage 3 cipher migration)
- **Element pool-cull adjustments** per Drift-14 audit cascade (gandalf Track B + IF Track B recommends, rocket selector hard-floor amendment)

Seed: pick a fresh seed (e.g., 1011) for clean cross-seed baseline. Document seed used.

LLM cost estimate: ~$1 per the prior V2 regen pattern. **Per Matt: single regen replaces what would have been 3-4 separate regen passes** (Gate 3b validation already in flight as Regen 1; this is Regen 2 covering MS + wind_controller + element-pool-cull in one shot).

### Step 2 — Per-class modifier table + Segment C metrics

Per the jack-ryan V2 calibration analysis methodology:
- Per-class final modifier
- target_winrate
- room_winrate at convergence
- modifier_flag_tier (V2.4 schema field; "review" = clamp-gate-flagged outlier)
- Convergence status

Compute Segment A (all 10), Segment B (excl. flag_tier='review'), Segment C (target=0.50 CONVERGED, excl. flag_tier='review' per jack-ryan version-gating clarification). Compare to jack-ryan's prior Segment C anchor (0.3273).

### Step 3 — Wind_controller-specific report

Per-occurrence wind_controller analysis:
- Modifier at target=0.50 (if generated in this regen)
- Modifier at target=0.60 (if RNG strong-outlier slot assignment happens; may not in 1 seed)
- Compare to historical pre-DPS-floor V2 wind_controller (3.51 / 3.625 at target 0.50 / 0.60)
- Kit shape verification: confirm 3-floor constraint applied (≥4 DPS skills; ≥1 AOE DPS; ≥1 Tier 1-2 DPS)

If wind_controller didn't get strong-outlier target in this regen + Decisions 2/3 activation requires multi-target observation, surface for follow-on regen.

### Step 3b — Element pool-cull validation report (NEW)

Per Matt directive (regen-batching extension): the element pool-cull adjustments per Drift-14 audit cascade should be empirically validated in this regen.

Surface in the report:
- **Pool composition delta:** pre-cull pool size vs post-cull pool size (from rocket source-of-truth + gandalf Track B cull-list)
- **Engine emission cleanliness:** does the culled pool emit cleanly through generator → exporter → consolidated JSON? Any orphan-element references in fixtures? Any selector failures (e.g., a kit demands an element from culled pool)?
- **Canonical-pair-leak metric improvement:** per legolas Track A pool-VFX-coverage audit, certain pool entries were flagged canonical-pair-leak-risk. Re-run the LLM-bound paths smoke (per star-lord Stage 3 22-test no-leak guard pattern); compare canonical-pair-leak counts pre-cull vs post-cull. Expectation: substantial reduction.
- **If rocket selector hard-floor amendment shipped:** does it activate cleanly? Any over-rejection (selector cannot satisfy archetype-required-elements)?

If any of the above fails: surface for routing (do NOT auto-fix; the cascade is upstream of this regen). This is empirical-validation only.

### Step 4 — Decisions 2 + 3 evaluation per gandalf framework

Per gandalf Decision-2/3 sequencing:
- **If wind_controller modifier stays ≥3.0 at target=0.50** → activate Decision 2 (clamp gate as reject-and-regenerate; kit re-roll, 3 attempts max) AND/OR Decision 3 (strong_outlier_compatible archetype tag = false for wind_controller)
- **If wind_controller modifier drops <2.5 at target=0.50** → Decisions 2 + 3 stay HELD (DPS-floor sufficient)
- **In-between (2.5-3.0)** → surface for Matt-decision; data-dependent

For Decision 3 specifically: even if wind_controller behaves at target=0.50, the strong-outlier-compatible question depends on target=0.60 behavior — may need explicit instrumentation (force wind_controller into the 0.60 slot for one verification fight).

### Step 5 — Recommendation + tag + completion record

Surface recommendation per branch outcome above. File math note if compiling Decisions 2/3 evaluation needs structured analysis (otherwise inline in completion record).

Intermediate tag: `gamora/v1.3-combined-post-cascade-evaluation-regen` (or seed-specific suffix per your convention).

## Out of scope (explicit)

- **NO clamp-gate-as-rejection logic implementation** (Decision 2 activation = separate gamora dispatch knight-rider authors if recommended)
- **NO strong_outlier_compatible archetype tag implementation** (Decision 3 activation = separate rocket dispatch knight-rider authors if recommended)
- **NO additional wind_controller balance-pass beyond DPS-floor validation**
- **NO other-archetype balance investigations** (this regen is wind_controller-focused; surface any anomalies in other archetypes for follow-on but do not investigate)
- **NO new telemetry emission fields** (if regen surfaces need, surface + stop per R11(b))
- **NO live DB migration** (regen output stays in analytical-mode storage)
- **NO V2 calibration epoch declaration** (Matt-decision; this dispatch informs but does not declare)
- **NO ARPG pixel-scale / visual-scale work** (separate workstream)
- **NO MS cascade item touchpoints** (those are landing in their own dispatches)

## Required reading

- Rocket DPS-floor dispatch + math note: `~/Games/reincarnated-engine/design/notes/wind-controller-dps-floor-2026-05-16.md` (especially §5 pool-exhaustion analysis + §6 expected modifier drop)
- Your prior wind_controller V2 anomaly investigation: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wind-controller-v2-anomaly-2026-05-16.md`
- Jack-ryan V2 calibration analysis: `agentic_orchestration/qa/analyses/2026-05-16-v2-calibration-analysis.md` (Segment C anchor + version-gating clarification + V1-vs-V2 inversion finding)
- Your Gate 3b dispatch completion record (when returns) for kiting math + 3-band distance state context
- Decisions-log MS supersession entry (committed earlier today: `2f61865`)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #2 smoke, #3 right-tool, #10 empirical inspection, #13a/b

## Acceptance criteria

- [ ] V2-mode regen completed with full cascade state (DPS-floor + MS defaults + Gate 3b sim consumption)
- [ ] Seed documented; LLM cost reported
- [ ] Per-class modifier table + per-class Segment C metrics
- [ ] Wind_controller-specific report (modifier + kit-shape verification + comparison to pre-DPS-floor)
- [ ] Decisions 2/3 recommendation per gandalf framework branches
- [ ] If activation recommended: separate dispatch authoring surfaced for knight-rider routing (do NOT execute activation in this dispatch)
- [ ] MIGRATION.md cross-reference (if applicable)
- [ ] Intermediate tag cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, recommendation (Decisions 2/3 activate / hold / data-dependent), wind_controller modifier delta vs pre-DPS-floor, any cross-archetype anomalies surfaced

## Tag policy

- **Intermediate tag:** `gamora/v1.3-combined-post-cascade-evaluation-regen` (or seed-suffixed variant)
- **Milestone tag:** none. V2 calibration epoch declaration milestone tag is separate Matt-approved decision.

---

## Completion record

**Completed:** _<date>_
**Seed:** _<seed>_
**LLM cost:** _<USD>_
**Per-class modifier table:** _<see attached doc / inline / N/A>_
**Wind_controller modifier:** _<value at target=X>_; comparison to pre-DPS-floor 3.51/3.625: _<delta>_
**Segment C metric:** _<value vs jack-ryan's prior 0.3273>_
**Decisions 2/3 recommendation:** _<activate / hold / data-dependent + branch>_
**Cross-archetype anomalies surfaced:** _<list or "none">_
**Intermediate tag:** _<tag @ hash>_
**Notes for knight-rider:**
