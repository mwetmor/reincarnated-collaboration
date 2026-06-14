# Mobility lock-edge re-calibration — PENDING (non-blocking; gated on gamora's displacement histogram)

**Type:** lock-edge re-calibration item (gandalf seam — gandalf owns the lock; Discipline #17 first-deployment-calibration).
**Date:** 2026-06-13
**Author:** gandalf
**Status:** PENDING — does NOT block the W-D close or the oracle v1.6 amendments. Carried as the (d) LOCK-EDGE home for Axis-1 mobility-half in the oracle § 6.4 discrimination accounting.
**Authority for the deferral:** Matt-ratified W-D close (`agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md` D1); gamora math note `reincarnated-engine/src/reincarnated/simulation/math/wd-six-axis-measure-build-2026-06-13.md` § 10.4.

---

## The finding (gamora § 10.4, Discipline #17)

The Axis-1 **mobility-half** is **WIRED + MEASURED** (Bucket-A satisfied — a real spatial reduction, not a default) and the raw signal **orders the kits correctly**: K4 = 64.4 > K2/K5 ≈ 62 > K1 = 56.9 > K3 = 55.5 > K6 = 50.4 m/min. **K4 is the highest-displacement kit, as expected.**

The defect is the **bin EDGE**, not the instrument: the lock's mobility threshold (`high ≥ 30 tiles/min`, lock § 3.1) bins **all six** kits `fast`, because in spatial combat the player accrues 50–64 m/min just CLOSING to mobs (baseline navigation), far above the 30 edge. The 30/min edge was calibrated for **1D**, where displacement comes from movement *skills* (teleport-spam), not baseline closing. This is exactly the first-deployment-on-spatial-telemetry calibration the lock § 0 anticipated as a gate dependency.

**Category:** (d) LOCK-EDGE mis-threshold. NOT a measurement bug. NOT a live obligation (oracle § 6.4 — the instrument works; only the edge mis-classifies).

## Why this is PENDING and not done now

Re-calibrating the edge responsibly requires the **full spatial displacement distribution** — not just the six kit means. To set an edge that *separates* a mobile kit from a static one on spatial telemetry, I need gamora's **per-kit displacement histogram** (the spread, not just the mean) so the new edge lands in the genuine gap between the static cluster (K1/K3/K6 closing-only) and the mobile signature (K4, and the AOE-repositioners K2/K5). Setting an edge off six point-means alone would risk a new mis-calibration in the other direction. I do NOT re-derive the edge in-seam off insufficient data (Discipline #11 — diagnose, don't assume).

**Empirical criterion that gates "edge re-calibrated":** the full displacement histogram lands → I set the edge in the static/mobile gap → K4 bins `mobile`, K1/K3/K6 bin `static`, and the AOE-repositioners (K2/K5) bin per their genuine displacement signature → the Axis-1 composite (range-half CONFIRM + mobility-half) discriminates K4 from the static kits. Substrate evidence, not assertion.

## The ask to gamora (routed via KR — non-blocking)

Emit the **per-kit spatial displacement histogram** (distribution, not mean) from the W-D run — or a re-emit if not already captured — as the calibration input. The instrument already accumulates `total_player_displacement` (math note § 10.4 / Priority-2 build); the histogram is the per-tick or per-fight distribution over that accumulator across the N=9 seeds.

## Composition with the oracle

This item is the named (d) LOCK-EDGE home in oracle § 6.4's discrimination accounting. § 6.4 stays open-pending-W-F **cleanly** with this carried as a tracked-deferred path. The mobility-half re-discriminates once the edge re-calibrates on spatial telemetry; until then Axis-1 discriminates on its **range-half** (CONFIRM) and the composite is bounded by the weaker (mobility) half per the structural-read composite rule.

---

**Signed:** gandalf, 2026-06-13
**For:** carrying the Axis-1 mobility-half lock-edge re-calibration as a PENDING (d)-LOCK-EDGE item, gated on gamora's full displacement histogram. Non-blocking on the W-D close + oracle v1.6.
