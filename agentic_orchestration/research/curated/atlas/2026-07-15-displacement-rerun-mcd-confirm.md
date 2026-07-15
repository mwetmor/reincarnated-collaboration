# Displacement Field — Edition-II drill-in slate CONFIRMATION re-run (post-MCD-growth)

> **STATUS:** CURRENT — authored elrond 2026-07-15 on gandalf's confirmation-gate commission
> (Matt-approved). Re-runs the frozen-Edition-I displacement decomposition over the GROWN corpus
> (survivors + 94 keyed MCD rows) to CONFIRM or report a shift in the pre-registered Edition-II
> drill-in slate. Honors the freeze: NO re-fit; new points project INTO the frozen 14-dim basis
> via the established masked-like / lighting-census-current discipline; NEW files only.
>
> **PRE-REGISTRATION (untouched, DO NOT MODIFY):**
> `2026-07-15-displacement-field-drill-in-slate.md` (memo + prediction P-DF-1) +
> `atlas-displacement-field-edition1.csv`/`.json` (455 rows), commit `c7804393`.
> **THIS re-run (new artifacts):** `atlas-displacement-field-edition1-rerun-mcd.csv` (455 rows +
> origin/beyond_horizon cols) + `.json` (rows + regions + mcd census + gate diagnosis).
> **Emitter:** `scripts/displacement_field_edition1_rerun_mcd_2026_07_15.py` (imports the original
> emitter wholesale — frozen machinery byte-identical; adds only mcd projection + census).
> Basis: Edition-I (frozen). Register-ref: feasibility-cuts-register-v1.1.

---

## 0. Verdict (decisive)

**SLATE HOLDS — UNCHANGED, and mcd-INVARIANT by construction.** The grown corpus produces a
per-region ranking *byte-identical* to the pre-registration: max |grown − survivor-only| over all
8 regions on both mass and n = **0.0**. Slate #1 (**ES / EAST-EMBODY → geometry×commit**, mean|Δ|
0.380/0.377), #2 (EN same pair), and the documented alternate (WN-inner mass-first) are untouched.
Geometry remains the **universal #1 promotable coordinate in all 8 regions**. Prediction P-DF-1 is
unaffected.

**The load-bearing reason this is a HOLD and not a re-confirmation on new data:** the corpus grew in
*row count* (469 → 563 keyed combat-kit rows) but added **zero points to the displacement plane.**
All 94 keyed MCD rows satisfy the SQL predicate the ghost/displacement emitters use
(`row_class='combat-kit' AND negative=0 AND cell_key IS NOT NULL`) — that is the predicate the MCD
curation log verified 94/94 — but they are **rejected by a second, deeper gate the emitter applies
after the fetch**: the register-meso core-tuple crosswalk (`kit_core_tuple` via `fit2reg_*`). None
of the 94 lights a ghost cell. The slate therefore *cannot* move; there is no new mapped mass to
move it. This is a real, honest finding about the MCD data shape — reported below, not papered over.

## 1. Freeze proof (survivors reproduce byte-perfectly)

The re-run imports the original emitter's `build_frozen_fit` / `kit_present_terms` /
`kit_core_tuple` / `aggregate_regions` verbatim and reconstructs every survivor row. Runtime guard
asserts each survivor against the pre-registration CSV on all load-bearing numeric fields:

| Anchor | Pre-registration | Re-run |
|---|---|---|
| Survivor displaced rows | 455 | **455** |
| Survivor reproduction worst \|Δ\| | — | **0.00e+00** (exact) |
| Ghost hull (galadriel r4/r5 ghostHullWorld) | 22 vtx / 7128 pos / east 1.2581 | **22 / 7128 / 1.2581** |
| Survivor beyond-horizon (22-vtx hull, ON⇒INSIDE) | 14 | **14** (ids match r5 census verbatim) |
| r_split (median lit radius) | 0.434249 | **0.434249** |
| Top-3 by \|Δ\| | le-warpath-vk / ud-whirlwind-str / di-whirlwind-barb | **identical** |

The frozen basis, fuse_map, and col_std loadings are the frozen ones; nothing is refit.

## 2. Per-region ranking — GROWN corpus (== survivor-only, since 0 mcd entered)

Ranked by aggregate |Δ| mass; #1 promotable coordinate (the 7 non-core coords a drill-in can
promote; `_coredilution`/`_coresub` excluded from the promotable ranking):

| Rank | Region | Poles | n | Σ\|Δ\| | mean\|Δ\| | #1 promotable | #1 PAIR |
|---|---|---|---|---|---|---|---|
| 1 | WN-inner | DEPLOY×LAUNCH | 113 | 28.27 | 0.250 | geometry (16.96) | geometry+economy |
| 2 | EN-outer | PERFORM×LAUNCH | 102 | 24.88 | 0.244 | geometry (19.77) | geometry+economy |
| 3 | **ES-outer** | **PERFORM×EMBODY** | 57 | 21.66 | **0.380** | geometry (12.98) | **geometry+commit (7.44)** |
| 4 | WS-outer | DEPLOY×EMBODY | 70 | 19.10 | 0.273 | geometry (15.07) | geometry+economy |
| 5 | **ES-inner** | **PERFORM×EMBODY** | 42 | 15.85 | **0.377** | geometry (9.84) | **geometry+commit (5.07)** |
| 6 | EN-inner | PERFORM×LAUNCH | 34 | 8.21 | 0.241 | geometry (4.08) | geometry+commit |
| 7 | WS-inner | DEPLOY×EMBODY | 25 | 6.27 | 0.251 | geometry (3.56) | geometry+economy |
| 8 | WN-outer | DEPLOY×LAUNCH | 12 | 3.04 | 0.253 | geometry (1.95) | geometry+commit |

Every figure matches the pre-registration table (§3 of the original memo) to the emitted decimal.
**Geometry is #1 promotable in all 8 regions** (grown AND survivor-only). The EAST-EMBODY quadrant
(ES-outer 0.380, ES-inner 0.377) remains the sharpest-error-density locus, geometry+commit its
unambiguous #1 pair. The slate's pre-registered ordering is intact.

## 3. Sensitivity segment (required)

Because **no** per-region ranking shifted, the excluding-mcd re-computation is a formality — but I
ran it as the control anyway. Grown regions vs survivor-only regions: **max |Δ| over all regions on
mass and n = 0.0.** There is no mcd-driven shift to attribute to low-confidence keys, because there
is no mcd contribution to the plane at all. Verdict: **slate holds on the full corpus; nothing is
mcd-sensitive** (the stronger statement — mcd cannot even reach the sensitivity surface).

## 4. Where the 94 keyed MCD kits land — they DON'T (gate diagnosis)

This is the substantive data-steward finding. The MCD curation log's claim "all 94 already satisfy
the displacement/ghost predicate" is true **at the SQL level** and false **at the plane level** —
the two are not the same gate, and the gap is structural, not a curation error.

**Two independent gates reject the MCD rows at the register-meso core-tuple crosswalk:**

| Gate | Slot | Raw cell_key value | # MCD blocked | Cause |
|---|---|---|---|---|
| **Primary (all 94)** | `movement` (core slot 0) | `blank` | **94 / 94** | `fit2reg_movement` maps only {full-move, walk, rooted}; `blank`→None. MCD is **classless twin-stick action-RPG** — a weapon/artifact carries no per-kit movement stance (no full-move / walk-cast / rooted-channel signal in the source prose), so `movement` was honestly left `blank`. Structurally identical to the `attr_val`-NULL the curation log already documents ("classless → no attribute axis"), EXCEPT `movement` is one of the 7 CORE meso slots the ghost/displacement join hard-requires. |
| **Secondary (26 of 94)** | `delivery` (core slot 1) | `melee` | **26 / 94** | `fit2reg_delivery` has no `melee` image (maps projectile/orbit/beam/line/self-origin/aura-pulse/at-target); `melee`→None. The MCD melee weapons. Survivors never serialize `melee` at the delivery slot (they carry it at the RANGE slot). |

**Counterfactual (what-if only; DB never mutated):** if `movement` were assigned any register value,
**68** of the 94 would map to a lit cell; **26** (the melee-delivery weapons) would STILL be
unmapped by the independent delivery gate. So a movement fix alone is necessary-but-not-sufficient
for full MCD inclusion, and it would require *inventing* a movement value the source does not
support — which the never-invent discipline forbids. The MCD rows are correctly out.

**MCD region distribution:** N/A — 0 of 94 map to a lit cell, so there is no region/quadrant
distribution to report. (Had they mapped, the census machinery is in place; it emitted the empty set.)

## 5. Beyond-horizon + coresub on MCD (verified, not assumed)

- **MCD beyond the 22-vertex ghost horizon: 0** — verified two ways. (a) 0 MCD reach the plane, so
  trivially 0 are beyond it. (b) The census-confirming reason the task anticipated: the 14 survivor
  beyond-horizon kits are **all `commit=channel`**; the commit distribution over ALL 94 keyed MCD is
  **instant 58 · blank 24 · wind-up 10 · channel 2** — overwhelmingly instant-commit, only 2 channel
  (and neither of those 2 maps anyway). Even under the counterfactual movement fix, no instant-commit
  MCD kit carries the geometry×channel-commit east pull that puts a kit beyond the horizon. **Confirmed:
  none — as expected, verified not assumed.**
- **coresub (term C) on MCD: max = 0.0, nonzero-count = 0.** Vacuously (0 mapped), and structurally as
  predicted: an MCD kit's *position* and its *lit cell* would both derive from the SAME fresh live
  cell_key — there is no separate pre-C3 "frozen position key" for MCD (they were never in the frozen
  fit), so the frozen-key-vs-live-key drift that produces nonzero coresub on 70 survivors cannot arise
  for MCD. **coresub-on-mcd ≈ 0 confirmed.**

## 6. Consequence for Edition-II + the curation record

1. **The confirmation gate PASSES: proceed with the pre-registered slate unchanged.** The MCD growth
   does not perturb the drill-in plan. Slate #1 = ES→geometry×commit; #2 = EN same pair; alternate =
   WN-inner mass-first. P-DF-1 stands.
2. **MCD's absence from the plane is a data-shape fact to record, not a bug to fix now.** The 94 keyed
   MCD rows are the *combat-metadata* surface (proxy/geometry/function/etc. keyed from prose); they are
   not *meso-placeable* until MCD acquires a `movement` core value AND the `melee` delivery is admitted
   to the register-meso vocabulary. Both are Edition-II vocabulary-pass decisions (gandalf/Matt own the
   vocabulary; elrond re-keys once the vocabulary exists) — the SAME class of deferral as the 6
   `pull_pending_vocab` kits (which await `pull` becoming a function level). I recommend adding
   `movement=blank` (classless-gear) and `delivery=melee` to the Edition-II vocabulary-pass docket as
   the two gates that would admit up to 68 of the 94 MCD weapons to the displacement plane.
3. **No correction owed to the MCD curation log's numbers** — its counts are right; only the phrase
   "already satisfy the displacement/ghost predicate" over-reaches by conflating the SQL predicate with
   plane-membership. The distinction is now documented here and in the emitter's inline rationale.

---

**Signed:** elrond (data steward), 2026-07-15. Method + emission reproducible via
`scripts/displacement_field_edition1_rerun_mcd_2026_07_15.py` (frozen inputs read-only; survivors
byte-reproduced; no re-fit; new files only). Idempotent (re-run → identical MD5).

**Tracker-delta:** adds the post-MCD-growth CONFIRMATION re-run of the Edition-II drill-in slate — a
new frozen-Edition-I analytical artifact confirming SLATE HOLDS (mcd-invariant), geometry-universality
intact, and documenting the two-gate (movement=blank + delivery=melee) structural exclusion of the 94
keyed MCD rows from the meso displacement plane. Consumed by Edition-II §5 drill-in planning +
vocabulary-pass docket. Pre-registration artifacts untouched; ghost/basis artifacts untouched;
r5/r6 captures untouched.
