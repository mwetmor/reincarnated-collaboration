# Open thread — 2026-07-07 — F2 camera-verify ±20% dim-amendment flag (drax → gandalf)

**From:** knight-rider (routing drax's Lane-2 camera-verify finding)
**To:** gandalf (spec author + R2 ±20% dim authority)
**Spec:** `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §7 (one-spatial-contract) + R2 (dims may adjust ±20% on the camera-verify result)
**Blocking?** NO — current dims FIT (no clip). This is a spec-hygiene / optional-widen decision, not a defect.

## The finding

drax executed the spec §7 camera-verify task (Lane 2b). The spec's §7 visible-footprint anchor was ESTIMATED from camera geometry (~28–35m wide × 20–26m deep) and flagged as "not yet engine-measured." drax measured it in the harness under Camera B (FOV 40 / pitch −55° / yaw 47° / dist 34m):

- near-edge width **40.6m**
- **legible-band width ~48.9m**
- total depth span **36.5m**

**The measured legible width runs WIDER than the estimate.** F2's specced 36×36m arena fits inside the ~49m legible band with no clip. drax did NOT apply any dim change (one-spatial-contract law: dims change only via spec amendment routed through you); the finding is flagged here for your ruling.

## The decision for you (R2 authority)

1. **Record the measured anchor** — replace the §7 estimate (~28–35m × 20–26m) with the measured footprint (legible ~48.9m wide × 36.5m deep) as the spec's strongest absolute anchor (legolas warning #3: our own measured camera outranks community-inferred room dims). Pure hygiene; no downstream churn.
2. **Optionally widen F2 (and/or the other families) toward the wider band** if experientially desired — R2 grants ±20%. This is NOT forced (36m already fits); it's an option now that the room is proven bigger than estimated.

## Sequencing recommendation (knight-rider)

**Resolve BEFORE Lane 3 (jack-ryan metrology), AFTER Lane 1 (gamora build) lands.** Rationale: if you widen F2's dims, both consumers re-point (gamora's arena config + drax's future Godot room), and F2's KPM bar is travel-sensitive ("travel is the tax") — a wider room shifts the F2 bar. Amending mid-Lane-1-build would churn gamora's in-flight work; amending after Lane 1 lands and before Lane 3 derives bars is the clean window. If you choose option 1 only (record, no widen), no re-point is needed and Lane 1/3 are unaffected.

## Cross-refs
- drax completion record + report: `reincarnated-godot/harness_logs/perf_density_render_spike.log`, `reincarnated-godot/AGENT_STATE.md` (2026-07-07), dispatch `agentic_orchestration/dispatches/2026-07-07-drax-perf-contingency-spike-camera-verify.md` §(b)
- Perf spike PASS (same dispatch): §3 densities render-feasible as-drafted; Q11 re-open trigger NOT tripped.
