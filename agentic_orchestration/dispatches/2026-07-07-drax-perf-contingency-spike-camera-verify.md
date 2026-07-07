# Dispatch — 2026-07-07 — drax — perf-contingency spike + camera-verify (Lane 2)

**From:** knight-rider
**To:** drax (presentation seam — `reincarnated-godot/`)
**Approved by:** Matt 2026-07-07 (Q11 RATIFIED with named monster-count contingency — this spike IS the contingency, operationalized)
**Estimated effort:** spike (measurement-and-report; compose with the pre-D7 horde-density spike — one spike, two customers)
**Acceptance:** a headroom report that answers, on real Godot render measurement: **can the ratified §3 densities (F2 ~40 concurrent + F4 continuous-lane engaged count) render at or above the 60-FPS floor on the min-spec class (GTX-1650/RTX-3050), plus a mobile-class read?** Deliverable feeds jack-ryan Lane 3 AND is the Q11 re-open trigger check. **PLUS** the non-gating §7 camera-verify: measure the actual visible floor footprint under Camera B, once.

## Context — the contingency, and why this is NOT a Lane-1 blocker

Matt ratified R1–R5 **"assuming no issues on monster count for godot game's playable PC or mobile phone system specs."** That assumption is the standing contingency on the §3 density targets (F1 ~24 · F2 ~40 · F4 continuous 2–4× F1 density). This spike tests it empirically.

**Critical framing:** spike SUCCESS confirms the ratified densities ship as-is. Spike FAILURE is a **Q11 re-open trigger** (§3 populations shrink → §6 bars re-derive on the smaller populations) — it is **NOT a blocker on gamora's Lane-1 sim-side build.** gamora builds the instrument at the ratified densities in parallel; if your spike shows the densities can't render, that feeds back as a spec amendment, and both the sim populations and the derived bars adjust. So fire this in parallel; do not wait on Lane 1, and Lane 1 does not wait on you.

**Genre precedent (verify-don't-invent):** Diablo Immortal ships population-scale density on phones — MultiMesh/LOD-class techniques are the known path. The spike verifies our harness reaches it; it does not need to invent the technique.

## Required reading before starting
- `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §3 (the densities under test: F2 ~40 total / ~20–50 engaged; F4 continuous 2–4× F1, 20–50 engaged, 150+ over window) + §7 (one-spatial-contract + the camera-verify task) + STATUS banner (the contingency + re-open trigger, verbatim).
- `agentic_orchestration/gandalf/notes/2026-07-07-kr-relay-q11-fire-order.md` §2 Lane 2 — your two tasks (perf spike + camera-verify).
- Your own reincarnated-godot AGENT_STATE / notes on the existing harness + the pre-D7 horde-density spike scope (compose the two).
- Camera B params: FOV 40 / pitch −55° / dist 34 m (the locked camera).

## Scope

### (a) Perf-contingency spike — the ratification contingency
- [ ] Synthetic density spike in the existing Godot harness under Camera B (FOV 40 / pitch −55° / dist 34m).
- [ ] Render **F2's ~40 concurrent Synty-class mobs** and **F4's continuous-lane engaged count** (20–50 engaged at any moment). Measure frame cost.
- [ ] Report **headroom vs the 60-FPS floor** on the **min-spec class (GTX-1650 / RTX-3050)** + a **mobile-class extrapolation/read.**
- [ ] **Compose with the pre-D7 horde-density perf spike** (Q5 ruling already governs it) — scope ONE spike to serve both customers if feasible; note where the two customers' needs differ if not.
- [ ] Deliverable: a headroom report (path in your seam's notes) → **explicitly state the pass/fail against the 60-FPS floor + the Q11 re-open-trigger determination** (feasible as-drafted / densities must shrink).

### (b) Camera-verify — non-gating, cheap (spec §7)
- [ ] Measure the ACTUAL visible floor footprint in the harness under Camera B, once. The spec's current anchor (~28–35 m wide × 20–26 m deep) is ESTIMATED from camera geometry, not engine-measured.
- [ ] Report the measured footprint. Per R2, family dims may adjust ±20% on this result — but that is a **spec amendment** routed back through knight-rider → gandalf, NOT a unilateral change and NOT a runtime translation (one-spatial-contract law).

## Cross-seam contract change? (Principle 6 gate)
**NO production contract change** — this is a measurement spike + a footprint measurement, both output as reports. The ONLY cross-seam consequence is a possible **spec amendment** (density shrink from the spike, or ±20% dim adjust from the camera-verify) — which flows back through knight-rider → gandalf (spec author), and if accepted re-points BOTH consumers (gamora sim arenas + your Godot rooms). Do not amend the spec yourself; flag the finding.

## Out of scope
- **NO Godot floor authoring / D6 room build** — that is gated on the Q7 rig unblock, separate. This is a synthetic density stress measurement in the EXISTING harness only.
- **NO engine (`reincarnated-engine/`) changes** — you stay in `reincarnated-godot/`.
- **NO bar derivation, NO sim work** — you measure render feasibility; jack-ryan (Lane 3) ingests your number.
- **NO unilateral spec-dim change** — flag amendments; don't apply them.

## References
- Spec `gauntlet-run-beat-families-spec.md` §3/§7 + STATUS contingency; fire order Lane 2
- Q5 ruling (60-FPS floor, min-spec class) — the pre-D7 horde-density spike this composes with
- Genre precedent: Diablo Immortal population-scale mobile density (MultiMesh/LOD path)
