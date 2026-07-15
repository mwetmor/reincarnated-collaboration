# Displacement Field — Edition-II drill-in slate (pre-registration)

> **STATUS:** CURRENT — authored elrond 2026-07-15 on gandalf's commission (Matt-approved).
> Measures the reconstruction error of the 7-core meso instrument (the ghost field) at every
> lit point on the FROZEN Atlas Edition-I plane. Honors the freeze: no re-fit, no basis change,
> new files only. Companion: renderer spec §9.5.3 (the registered prediction this formalizes);
> `atlas-displacement-field-edition1.csv` / `.json` (the data); `scripts/displacement_field_edition1.py`
> (reproducible emission). Basis: Edition-I (frozen). Register-ref: feasibility-cuts-register-v1.1.

---

## 1. Method

**The displacement field.** For every active non-supplementary kit that lands in a LIT feasible
ghost cell:

```
Δ(kit) = kit_position − own_cell_position
```

A KIT projects onto the frozen Edition-I plane with **all 14 coordinates**; a GHOST CELL projects
with **only the 7 core coordinates** (non-core blocks masked; CA renormalized over core-present
levels). Both use the IDENTICAL CA supplementary transition formula
`F(d) = Σ_j rowp_j · col_std_j(d)`; they differ only in which levels are present. The displacement
is therefore exactly the lit-ground trace of meso blindness — what the 7-core instrument cannot see.

**Freeze discipline (verified).** The frozen fit is reconstructed from the durable pre-C3 snapshot
`atlas-frozen-fit-cellkeys-edition1.csv`; it reproduces all 469 active kit positions to 0.00
(≈5e-8 vs the 8-decimal atlas.json — pure rounding). Kit positions are the frozen fit's; cell
positions are READ from `atlas.json → ghost_field.feasible_cells` (the published ghost plane).
The join reuses `ghost_field_edition1.lit_map` crosswalk logic verbatim (REG2FIT + meso
predicates), so the mapping is byte-consistent with the emitted lighting.

**Attribution — exact three-part additive decomposition.** With `w_j = 1/first_sv[block_j]` the
MFA weight of level j and `c_j = col_std_j` the frozen column standard coordinate (== the
`atlas-loadings.csv` values), and splitting present levels into core / non-core:

```
Δ = (A) direct        Σ_{l∈noncore} (w_l·c_l)/W_all      per masked non-core level's pull
  + (B) core-dilution  Score·(1/W_all − 1/W_core)         renorm consequence of masking ALL non-core
  + (C) core-substitution  C_frozencore − C_published     FROZEN-position-key vs LIVE-lighting-key drift
```
where `Score = Σ_{j∈core} w_j·c_j`, `W_all`/`W_core` the present/core weight sums. **Verified:
(A)+(B)+(C) reconstructs every kit's Δ to 0.0 (machine precision).** Normalization: each level's
contribution is its MFA-weighted standard coordinate divided by the kit's TOTAL present weight
`W_all` — the same denominator the kit's own position uses — so contributions are directly
comparable and additive.

Terms (B) and (C) are **not promotable**: no non-core drill-in reduces (C) — it is a curation
signal (frozen fit was built on pre-C3 keys; the LIVE lighting uses post-C3 keys + `other-rare`
fusions). (B) is reduced only *indirectly* by un-masking a coordinate. Only term (A) — the per-
non-core direct pull — is what an Edition-II drill-in can promote away.

**Region binning.** Compass quadrant × radius band. Poles are meaningful (x+=PERFORM / x−=DEPLOY /
y+=LAUNCH / y−=EMBODY), so a quadrant name carries design meaning; the radius split (inner/outer at
the median lit-cell radius, r_split=0.434) separates core-of-genre cells from periphery. Each kit is
binned by its **own cell** position — the anchor Δ is measured *from*. 8 regions. (Alternatives
considered: k-means on cell positions gives non-semantic bins; pure quadrant is too coarse at 4 bins;
lattice neighborhoods over-fragment at 192 lit cells. Quadrant×band is the honest middle — documented
per commission.)

## 2. Counts + sanity anchors (ALL HELD)

| Anchor | Expected | Observed |
|---|---|---|
| Active kits | 469 | 469 |
| Lit cells | 192 | 192 |
| Displaced rows | 455 (469 − 14) | **455** |
| Unmapped-pending-curation | 14 | **14** (identical set to ghost emitter) |
| Ghost x max | 1.25805961 | **1.25805961** |
| Ghost hull | 22 vertices | **22** |
| Beyond-horizon kits | 14 | **14** (10 whirlwind + 3 cone/beam + 1 neutral) |
| Attribution residual | ~0 | **0.0** (all 455 kits) |

**HALT-gate anchor — the beyond-horizon set reproduces independently.** All 14 kits outside the
ghost hull have their +Δx dominated by exactly **commit=channel (+0.395 on x) and geometry∈
{whirlwind +0.334, cone +0.367}** as the top-2 positive-x contributors — including the 1 neutral
`tl1-alchemist-summoner`. `ud-flamethrower-channel` sits at kit_x=1.390 (Δx=+0.569), matching the
commission's expected value. The attribution machinery reproduced this with **no tuning**; the
anchor held on first correct run.

## 3. Region ranking + per-region attribution

Ranked by aggregate |Δ| mass (Σ|Δ| over the region's kits); mean |Δ| and the dominant PROMOTABLE
coordinate shown (the 7 non-core coords a drill-in can promote — `_coredilution`/`_coresub` are
carried in the data but excluded from the promotable ranking):

| Rank | Region | Poles | n | Σ\|Δ\| | mean\|Δ\| | #1 promotable | Best promotable PAIR |
|---|---|---|---|---|---|---|---|
| 1 | WN-inner | DEPLOY×LAUNCH | 113 | 28.27 | 0.250 | geometry (17.0) | geometry+commit (21.3) ≈ +economy/+tempo |
| 2 | EN-outer | PERFORM×LAUNCH | 102 | 24.88 | 0.244 | geometry (19.8) | geometry+economy (25.2) |
| 3 | **ES-outer** | **PERFORM×EMBODY** | 57 | 21.66 | **0.380** | geometry (13.0) | **geometry+commit (17.8)** |
| 4 | WS-outer | DEPLOY×EMBODY | 70 | 19.10 | 0.273 | geometry (15.1) | geometry+economy (19.6) |
| 5 | **ES-inner** | **PERFORM×EMBODY** | 42 | 15.85 | **0.377** | geometry (9.8) | **geometry+commit (13.5)** |
| 6 | EN-inner | PERFORM×LAUNCH | 34 | 8.21 | 0.241 | geometry (4.1) | geometry+commit (5.7) |
| 7 | WS-inner | DEPLOY×EMBODY | 25 | 6.27 | 0.251 | geometry (3.6) | geometry+economy (4.8) |
| 8 | WN-outer | DEPLOY×LAUNCH | 12 | 3.04 | 0.253 | geometry (2.0) | geometry+commit (2.8) |

**Top-3 by mass:** WN-inner, EN-outer, ES-outer. **Top-2 by MEAN |Δ| (sharpest error density):**
ES-outer (0.380), ES-inner (0.377) — the EAST-EMBODY quadrant.

**Two structural findings:**

1. **`geometry` is the universal #1 promotable coordinate in every one of the 8 regions.** The 21-level
   geometry coordinate carries the strongest masked pulls (whirlwind +1.80x/−2.56y, cone +1.98x,
   chain +1.32y, dash −0.91y, totem −1.52x). This is **2D-coherent**: geometry blindness dominates
   reconstruction error everywhere, not only where whirlwind lives. Geometry is the single biggest lever.

2. **The best PARTNER for geometry splits cleanly by quadrant** — and the split is itself signal:
   - **EAST-EMBODY (ES, PERFORM×EMBODY): geometry+commit leads** (17.8 / 13.5). This is the
     beyond-horizon direction. commit=channel (+1.88x, −1.43y) compounds whirlwind's SE pull. **11 of
     the 14 beyond-horizon kits' cells sit in ES** (7 outer + 4 inner); the ES net displacement points
     hard SOUTH and modestly EAST (dx +1.3/+1.8, dy −4.9/−3.9), exactly the channel+whirlwind vector.
   - **DEPLOY + LAUNCH regions: geometry+economy leads** (economy=reserve −1.45y, cooldown −0.95x are
     the masked resource pulls — a different, LAUNCH/deploy-side blindness).

## 4. Pre-registered Edition-II drill-in slate

Ranked list — region → coordinate pair whose local promotion most reduces reconstruction error →
expected effect. This is the pre-registered design pass; Edition-II §5 drill-ins execute against it.

| # | Region | Promote | Rationale | Expected effect |
|---|---|---|---|---|
| **1** | **ES (EAST-EMBODY: ES-outer + ES-inner)** | **geometry × commit** | Highest mean-|Δ| (0.380/0.377); geometry+commit is the unambiguous #1 pair here; 11/14 beyond-horizon kits' cells live here; net displacement is the pure channel+whirlwind SE vector. This is the §9.5.3 registered-prediction target. | Un-masking geometry×commit locally lets ES sub-cells reach the whirlwind/cone/channel SE ground the meso instrument cannot. Dark ground extends SE past the whirlwind kits (see §5). |
| 2 | EN-outer + EN-inner (EAST-LAUNCH) | geometry × commit | The 3 cone/beam channel kits (`ud-flamethrower-channel`, `poe1-incinerate`, `gd-flames-of-ignaffar-purifier`) sit in EN-outer at x≈0.82; geometry+commit is #1 pair inner, #2 outer. Same masked pair, LAUNCH side. | Extends dark EAST toward the cone/beam channel kits at x≈1.39 (the plane's east frontier among the living). |
| 3 | WN-inner + WS regions (DEPLOY side) | geometry × economy | Largest total mass (WN-inner 28.3) but diffuse; geometry+economy leads on the DEPLOY/resource side (reserve/cooldown pulls). Lower mean-|Δ| ⇒ broad, shallow error. | Reduces the resource-economy component of DEPLOY-side displacement; smaller per-cell gain, largest cell count. |

**Slate #1 entry (headline): ES (EAST-EMBODY) → promote geometry × commit.** Highest error density,
sharpest attribution signal, and the exact locus of the beyond-horizon phenomenon.

**Sequencing note.** #1 and #2 are the same coordinate pair (geometry×commit) on adjacent EAST
quadrants — an Edition-II pass could promote geometry×commit across the whole EAST half in one
drill-in and satisfy both. #3 (geometry×economy, DEPLOY side) is a distinct second pass. Geometry
appears in all three: **if only one coordinate is promoted Edition-wide, promote geometry** — it is
the #1 lever in all 8 regions.

## 5. The §9.5.3 registered prediction — formalized as a scorable statement

> **PREDICTION (P-DF-1).** An Edition-II EAST drill-in that promotes geometry×commit in the ES /
> EN quadrants will produce drill-in dark ground (zero-mass supplementary sub-cells) that
> **OVERSHOOTS the 14 beyond-horizon kits to the SE/E** — i.e. the SE-most / E-most drill-in
> sub-cell will project FARTHER from origin along the whirlwind/cone+channel direction than the
> farthest beyond-horizon kit currently sits.

**Mechanism.** Drill-in sub-cells renormalize their CA profile over ~9 present blocks (the 7 core +
the 2 newly-promoted: geometry, commit), while a kit renormalizes over 14. The smaller denominator
gives each promoted level a LARGER share of the sub-cell's position — the same masking asymmetry
that today puts ghost overshoot W/S/N (the 7-core cells overshoot the settled envelope on 3 of 4
compass extremes; only EAST under-reaches, because the strongest EAST pulls are the masked ones).
Promoting geometry+commit inverts the EAST under-reach into an EAST/SE over-reach.

**Scoring procedure (a future Edition-II render executes this — PASS/FAIL is mechanical):**
1. Emit the ES/EN geometry×commit drill-in sub-cells as zero-mass supplementary ground (existing
   §9.2.3 clip-and-disclose machinery handles any that exit the frame).
2. Let `S_max` = max over drill-in sub-cells of the projection along the unit whirlwind+channel
   direction `û = normalize(mean(c_geom=whirlwind, c_commit=channel))` on (x,y).
3. Let `K_max` = max over the 14 beyond-horizon kits of the same projection.
4. **PASS iff `S_max > K_max`** (drill-in dark overshoots the beyond-horizon kits along û).
   Equivalently and more simply: PASS iff at least one drill-in sub-cell lands SE of the SE-most
   whirlwind kit (`di-whirlwind-barb`, cell not kit) OR E of `ud-flamethrower-channel`'s cell.
5. **FALSIFIER:** if every geometry×commit drill-in sub-cell lands strictly INSIDE the current
   beyond-horizon kit envelope along û, the overshoot claim is false — the masking asymmetry does
   not invert as predicted, and interior-aware placement (INTERIOR-1, logged for Edition-III) would
   be re-opened with new fuel.

**Freeze safety (unchanged):** drill-in sub-cells are zero-mass supplementary ground; they cannot
move the frozen basis or the 506 point coordinates; any that exit the frame clip-and-disclose. The
prediction is computable NOW from frozen artifacts (loadings + kit/cell positions) — only the
*render* of it awaits Edition-II.

## 6. Unmapped-pending-curation kits (excluded from displacement, listed per commission)

14 active kits whose LIVE core tuple does not map to a feasible meso cell (identical set to the
ghost emitter's `unmapped_pending_curation`) — all fail on an **unmapped core slot** (a core level
with no register-meso image: MELEE/SUMMON delivery collapse, hybrid treatment, silence function, or
a totem-geometry×solo-proxy that L2 forbids as SUMMON). Excluded from Δ because they have no anchor
cell; flagged here for Legolas re-crawl / curation, not force-mapped:

```
d3-call-of-the-ancients   d3-dashing-strike-monk   d3-lod-archetype        hot-kugelblitz
le-ring-of-shields        le-shift-bladedancer      poe1-totem-hierophant   poe1-vaal-blade-vortex
poe2-archmage-totems      poe2-shaman-bear          poe2-snipe-mirage-deadeye poe2-spiral-volley
poe2-walking-calamity     poe2-whirling-assault-ma
```

These are distinct from the 14 *beyond-horizon* kits (which ARE mapped and displaced) — coincidentally
both sets are size 14. No `would-seal` kits (0) and no unexpected exclusions (`excluded_no_point`=0,
`excluded_no_cell`=0).

## 7. Anomalies + honest caveats

- **Core-substitution (term C) affects 70 of 455 kits** (the rest have C≈0). For these, part of the
  displacement is NOT maskable-coordinate error but **frozen-position-key vs live-lighting-key drift**:
  the frozen fit placed the kit's *position* using its pre-C3 / `other-rare`-fused core levels, while
  its *cell* is lit by the post-C3 LIVE core tuple. Worst cases: `d2-firewall-sorc` / `le-chthonic-
  fissure-warlock` (coresub 0.480 — frozen delivery=`other-rare`, live=BEAM); the C3 treatment re-keys
  (`poe2-poison-pathfinder` etc., frozen treatment=control, live=damage, coresub 0.114). **A drill-in
  does not fix these** — they are a curation signal. Distribution is bimodal (385 kits ≈0; 70 kits
  ≥0.001, of which 57 ≥0.1) — a discrete, identifiable phenomenon, not pervasive noise. The
  beyond-horizon 14 all have coresub≈0, so the slate #1 target is uncontaminated.
- **WN-inner outranks ES on total mass but not on mean.** WN-inner is a large (n=113) diffuse region:
  its geometry+commit / +economy / +tempo pairs are near-tied (21.3 / 21.0 / 20.2), no sharp lever. ES
  is smaller but sharper (higher mean, unambiguous geometry+commit). The slate ranks ES #1 on *error
  density + attribution clarity + prediction alignment*, not raw mass — a drill-in wants a sharp target,
  not a broad shallow one. (If Edition-II prefers mass-first, WN-inner→geometry×commit is the alternate
  #1; documented so the choice is explicit.)
- **`amp` and `defense` contribute ≈0 everywhere** — both load ~0 on the two display axes (amp=var,
  all defense levels ≈0 on x/y per the frozen loadings). They are invisible to the *2-D* displacement
  by construction; they may carry error on retained dims 3–14 (out of scope for this plane-view field).

---

**Signed:** elrond (data steward), 2026-07-15. Method + emission reproducible via
`scripts/displacement_field_edition1.py`. All frozen inputs read-only; no re-fit; new files only.

**Tracker-delta:** adds the Edition-II drill-in slate pre-registration — a new frozen-Edition-I
analytical artifact (per-kit displacement field + three-part attribution + region-ranked
coordinate-pair slate + the formalized, scorable §9.5.3 prediction P-DF-1). Consumed by Edition-II §5
drill-in planning; no engine-side change; ghost/basis artifacts untouched.
