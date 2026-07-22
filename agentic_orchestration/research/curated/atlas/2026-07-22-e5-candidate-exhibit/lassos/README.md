# E5 CANDIDATE — BUILD-FAMILY LASSOS — numbers only

**Date:** 2026-07-22 · **Executor:** elrond · **Purpose:** camera-fork ruling input — Matt SEES build-families as enclosing hulls on both cameras.

> **E5 CANDIDATE — NOT SERVED (§8-C: E4 remains truth)**
>
> **EXHIBIT-ONLY — families UNNAMED; island cut + naming remain gated (Matt hold)**

Clusters carry NEUTRAL LETTER labels (A, B, C…). Legends are numbers-only + RATIFIED mechanical vocabulary (court k=5; `gb_*` register tokens from the six-block side-car). NO thematic / archetype / island names. Canonical island-cut + naming remain GATED (Matt hold).

## Reproduction gate (vs 2026-07-22-legb-gate-report.md) — runs FIRST

**Result: PASS — 8/8 match record**

- B3 congruence          PASS | got=0.7836 want=0.7836 tol=0.0005 delta=0.0000
- rotation_deg           PASS | got=58.5364 want=58.5400 tol=0.1000 delta=0.0036
- reflection             PASS | got=True want=True
- n_fit                  PASS | got=265 want=265
- n_retained             PASS | got=17 want=17
- anchor_n               PASS | got=46 want=46
- s_star                 PASS | got=0.8117 want=0.8117 tol=0.0005 delta=0.0000
- E4 basis reconstruct   PASS | max_abs_err=4.938e-08 (<1e-6)

## Method — clustering (HDBSCAN-first, silhouette-k-means fallback)

HDBSCAN (`sklearn.cluster.HDBSCAN`) is attempted first per cut (noise stays UNLASSOED — honest). If it under-resolves for legibility — a single hull over > 55% of points (giant blob) OR fewer than 5 clusters — we fall back to k-means with silhouette-selected k in [5, 10] for that cut (task-sanctioned fallback). Both the chosen method and the rejected HDBSCAN result are recorded. All deterministic (SEED=20260722).

**CUT A (E4-carryover)**

- HDBSCAN(min_cluster_size=10, min_samples=5) → k=6, noise=299, largest hull=21% of points, sizes=[41, 50, 25, 13, 119, 14].
- **Chosen: HDBSCAN** (k in legible range, no giant blob).
- Rationale: HDBSCAN gave k=6 (noise=299) with no giant blob (largest hull = 21% of points) -> legible; used as-is.

**CUT B (E5-native)**

- HDBSCAN(min_cluster_size=10, min_samples=5) → k=2, noise=13, largest hull=76% of points, sizes=[51, 201].
- **Chosen: k-means k=5** (silhouette=0.4795). Silhouette sweep: k5:0.479 k6:0.475 k7:0.445 k8:0.387 k9:0.366 k10:0.379. sizes=[60, 55, 95, 27, 28].
- Rationale: HDBSCAN rejected (largest HDBSCAN hull = 76% of points (> 55% giant-blob gate); HDBSCAN k=2 < 5 (below legibility floor)). Fell back to silhouette k-means: best k=5 (silhouette=0.4795 over k in [5,10]).

## CUT A — E4-carryover families (cut on the E4 SERVED plane)

Clustered on the E4 served plane using ALL **561** kits placed in BOTH cameras (record + annex/system supplementary). Each cluster's hull is drawn on the E4 panel and the SAME MEMBERSHIP's hull on the E5-aligned panel → shows how E4's families reorient under the candidate angle.

| cluster | n | class split | court composition % | top-3 gb_* register tokens (record) |
|---|---|---|---|---|
| **A** | 119 | annex=69 record=49 system=1 | physical 13% fire 9% cold 6% lightning 7% chaos-poison 6% NULL 60% | `gb_range:melee`(22), `gb_delivery:melee_arc`(20), `gb_motion:point_strike`(16) |
| **B** | 50 | annex=22 record=28 | physical 18% fire 4% cold 2% lightning 16% chaos-poison 12% NULL 48% | `gb_delivery:projectile`(17), `gb_motion:fan_spread`(9), `gb_delivery:zone`(6) |
| **C** | 41 | annex=24 record=16 system=1 | physical 22% fire 5% cold 2% lightning 2% chaos-poison 5% NULL 63% | `gb_delivery:aura`(5), `gb_range:self`(5), `gb_delivery:zone`(4) |
| **D** | 25 | annex=10 record=15 | physical 8% fire 24% cold 8% lightning 8% chaos-poison 12% NULL 40% | `gb_delivery:zone`(5), `gb_delivery:projectile`(5), `gb_motion:straight_line`(3) |
| **E** | 14 | annex=10 record=4 | physical 7% fire 7% cold 7% lightning 7% NULL 71% | `gb_delivery:zone`(2), `gb_motion:ground_place`(1), `gb_width:wide`(1) |
| **F** | 13 | annex=7 record=6 | physical 38% chaos-poison 8% NULL 54% | `gb_delivery:melee_arc`(3), `gb_range:melee`(3), `gb_delivery:summon_delegate`(2) |

### How CUT-A families reorient under E5 (numbers + register tokens only)

`shift` = centroid displacement E4→E5-aligned (plane units; frac of plane span). `spread_ratio` = RMS radius on E5 ÷ RMS radius on E4 (>1 = the family SPREADS / splinters; <1 = TIGHTENS). Families named by letter + top register tokens ONLY.

| cluster | n | shift | shift/span | spread E4 | spread E5 | spread_ratio | top gb_* tokens (record) |
|---|---|---|---|---|---|---|---|
| **A** | 119 | 0.661 | 0.18 | 0.147 | 0.438 | 2.97 | `gb_range:melee`, `gb_delivery:melee_arc`, `gb_motion:point_strike` |
| **B** | 50 | 0.551 | 0.15 | 0.101 | 0.195 | 1.93 | `gb_delivery:projectile`, `gb_motion:fan_spread`, `gb_delivery:zone` |
| **D** | 25 | 0.485 | 0.13 | 0.110 | 0.386 | 3.51 | `gb_delivery:zone`, `gb_delivery:projectile`, `gb_motion:straight_line` |
| **E** | 14 | 0.400 | 0.11 | 0.054 | 0.279 | 5.20 | `gb_delivery:zone`, `gb_motion:ground_place`, `gb_width:wide` |
| **F** | 13 | 0.291 | 0.08 | 0.088 | 0.552 | 6.30 | `gb_delivery:melee_arc`, `gb_range:melee`, `gb_delivery:summon_delegate` |
| **C** | 41 | 0.059 | 0.02 | 0.176 | 0.340 | 1.93 | `gb_delivery:aura`, `gb_range:self`, `gb_delivery:zone` |

- **Migrate (centroid shift ≥ 20% of plane span):** none
- **Split / spread (E5 RMS radius ≥ 1.30× E4):** Cluster F (melee_arc/melee-heavy) → spread ×6.30; Cluster E (zone/ground_place-heavy) → spread ×5.20; Cluster D (zone/projectile-heavy) → spread ×3.51; Cluster A (melee/melee_arc-heavy) → spread ×2.97; Cluster C (aura/self-heavy) → spread ×1.93; Cluster B (projectile/fan_spread-heavy) → spread ×1.93
- **Tighten (E5 RMS radius ≤ 0.77× E4):** none

## CUT B — E5-native families (cut FRESH on the E5 CANDIDATE plane)

Clustered on the E5-candidate-aligned plane using **RECORD-CLASS ONLY (265 axis-deriving fit members)**. Rationale HONORED: annex/system E5 placements derive from SHARED older vocabulary only (no six-block `gb_*` data) — cutting families from those draped placements would MANUFACTURE structure, so they are excluded from this cut. Hulls drawn on the E5 panel; the same memberships are echoed (dashed, hollow) on the E4 panel. Unlassoed (noise) record kits: **0** (drawn as small × marks — honestly outside every hull).

| cluster | n | class split | court composition % | top-3 gb_* register tokens (record) |
|---|---|---|---|---|
| **A** | 95 | record=95 | physical 26% fire 19% cold 9% lightning 22% chaos-poison 20% NULL 3% | `gb_delivery:projectile`(46), `gb_delivery:zone`(25), `gb_motion:fan_spread`(25) |
| **B** | 60 | record=60 | physical 22% fire 30% cold 18% lightning 5% chaos-poison 22% NULL 3% | `gb_delivery:zone`(31), `gb_motion:ground_place`(22), `gb_cadence:cooldown`(11) |
| **C** | 55 | record=55 | physical 49% fire 13% cold 5% lightning 20% chaos-poison 11% NULL 2% | `gb_range:melee`(54), `gb_delivery:melee_arc`(53), `gb_motion:point_strike`(41) |
| **D** | 28 | record=28 | physical 50% fire 29% cold 4% lightning 11% chaos-poison 7% | `gb_cadence:cooldown`(26), `gb_delivery:summon_delegate`(25), `gb_delivery:zone`(2) |
| **E** | 27 | record=27 | physical 41% fire 15% cold 11% lightning 15% chaos-poison 15% NULL 4% | `gb_cadence:channel`(22), `gb_delivery:motion`(17), `gb_motion:orbit_fixed`(15) |

## Files

- `lassos-e4-carryover.png` — 558987 bytes
- `lassos-e5-native.png` — 578785 bytes
- `lasso-membership.csv` — 42219 bytes

## Exact reproduction command

```
cd /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts
python3 atlas_e5_lassos_2026_07_22.py
```

Deterministic: SEED=20260722, all randomness pinned (HDBSCAN + KMeans). corpus.db opened read-only (uri mode=ro). Imports `atlas_e5_exhibit_2026_07_22`, `atlas_e5_exhibit_574_2026_07_22`, `atlas_legb_refit_2026_07_22` verbatim (no recompute/placement math changed). corpus.db md5 = `bebc933b0bf9bcab5988bbc16bcc55b4` (unchanged; read-only).

## Constraint attestation

- READ-ONLY on corpus.db and every store — zero mutations, zero serving artifacts.
- Reproduction gate (8/8) gates the renders: any mismatch → HALT, no renders.
- EXHIBIT-ONLY lassos: NEUTRAL letter labels, numbers-only legends, RATIFIED vocabulary only (court k=5; `gb_*` register tokens). NO thematic / archetype / island names. Canonical island-cut + family naming remain GATED (Matt hold).
- CUT B excludes annex/system (no six-block data) — draped placements are NOT cut into families, avoiding manufactured structure.
