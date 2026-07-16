# Refit Candidate 1 vs Edition III (Edition-I fit) — comparison report

**Date:** 2026-07-16 · **Executor:** elrond (numbers only — gandalf synthesizes the reading).
**Artifact:** `atlas-refit-candidate-1.json` (unratified comparison artifact) vs the FROZEN Edition-I fit that Edition III serves. This is a COMPARISON EXPERIMENT, not an Edition — "Edition IV" appears NOWHERE.
**Fit sets:** Edition-I fit = 469 active (frozen, pre-C3 keys). Refit = 628 active (live keys). Shared actives = **469** (all 469 Edition-I kits are a subset of the refit's 628; 0 dropped). New in refit = **159**.

> **Red-ink headline (gate evidence for adoption):** Edition-I froze on A+C+D (+F-1). Refit gates: **A FAIL · B FAIL · C gandalf-rules (PERMDISP-significant) · D PASS.** Gates are EVIDENCE for the decision, not emission blockers. See §7.

## §1 — Procrustes congruence + RMS displacement (469 shared actives)

- **Plane (dim1×dim2) Procrustes disparity M² = 0.78127 → congruence √(1−M²) = 0.4677** (1.0 = identical up to rotation/scale/reflection).
- Standardized-frame plane diameter = 0.2047. **RMS displacement = 0.0408 = 19.94% of plane diameter; median = 0.0329 = 16.05%.**
- **Full retained-space congruence** (first 14 shared dims of E1's 14 vs refit's 17): √(1−M²) = 0.8595 (M²=0.26127).

**Top-20 movers on the plane** (Procrustes-standardized displacement — frame-invariant; E1 (x,y) is E1's served raw plane, refit (x,y) is the **Q-ALIGNED** plane matching the emitted artifact):

| kit_id | E1 (x,y) | refit aligned (x,y) | disp (std) | % diam | gateA |
|---|---|---|---|---|---|
| tq2-whirlwind-rogue | (1.111, -1.490) | (1.082, -0.442) | 0.1040 | 50.8% | WHIRLWIND |
| di-whirlwind-barb | (1.058, -1.562) | (0.997, -0.585) | 0.1029 | 50.2% | WHIRLWIND |
| le-frost-claw | (0.797, 0.635) | (-0.713, 0.124) | 0.0975 | 47.6% | — |
| hot-dragons-breath | (0.867, 0.388) | (-0.375, -0.188) | 0.0864 | 42.2% | — |
| ud-flamethrower-channel | (1.390, -0.321) | (0.426, -0.337) | 0.0852 | 41.6% | CHANNELED-BEAM |
| ud-whirlwind-str | (1.007, -1.361) | (0.836, -0.806) | 0.0811 | 39.6% | WHIRLWIND |
| poe1-arc | (0.341, 0.886) | (-0.068, -0.406) | 0.0810 | 39.6% | — |
| poe1-incinerate | (1.389, 0.047) | (0.497, -0.056) | 0.0802 | 39.2% | CHANNELED-BEAM |
| ud-cwc-spin-caster | (0.914, -0.954) | (0.237, -0.508) | 0.0797 | 38.9% | WHIRLWIND |
| hot-exterminator-burn | (0.967, 0.344) | (-0.009, -0.357) | 0.0794 | 38.8% | — |
| le-warpath-vk | (1.023, -1.283) | (0.670, -0.844) | 0.0791 | 38.6% | WHIRLWIND |
| di-ray-of-frost-wizard | (1.029, -0.531) | (0.116, -0.305) | 0.0786 | 38.4% | CHANNELED-BEAM |
| d3-call-of-the-ancients | (-1.158, -0.527) | (-0.415, -0.163) | 0.0781 | 38.2% | — |
| d2-bvc | (0.711, -1.211) | (0.661, -0.518) | 0.0778 | 38.0% | WHIRLWIND |
| poe2-tempest-bell | (-0.599, -0.326) | (0.269, 0.433) | 0.0774 | 37.8% | — |
| di-draw-quarter-crusader | (-0.041, -0.742) | (-0.355, 0.248) | 0.0760 | 37.1% | — |
| tq-shield-charge-conqueror | (-0.041, -0.742) | (-0.355, 0.248) | 0.0760 | 37.1% | — |
| poe1-edc | (0.296, 0.776) | (-0.325, -0.362) | 0.0753 | 36.8% | — |
| poe1-earthshatter | (-1.105, -0.054) | (-0.243, 0.272) | 0.0752 | 36.7% | — |
| poe1-freezing-pulse | (0.267, 0.776) | (-0.238, -0.418) | 0.0748 | 36.5% | — |

## §2 — Axis identity + plane_alignment (item A′ ruling): did PERFORM/DEPLOY + EMBODY/LAUNCH survive?

**plane_alignment (the ruling's amended item A → A′):** the raw refit plane is compared to Edition-I orientation on the 469 shared actives, then aligned by an **in-plane orthogonal Procrustes map Q (rotation+reflection, NO scaling, NO translation)**. This isolates the already-arbitrary MCA/SVD orientation convention; distances/spreads/congruence/gates/plane-inertia are all Q-invariant.

- **Q = [[-0.459389, -0.888235], [-0.888235, 0.459389]]**
- **rotation_deg = -117.3477° · det(Q) = -1.0** (det −1 ⇒ a reflection component; the refit plane rotated ~117° + reflected vs Edition-I).

**RAW same-index corr matrix (E1 rows × refit cols) — BEFORE alignment:**

| | refit dim1 (raw) | refit dim2 (raw) |
|---|---|---|
| **E1 dim1 (PERFORM↔DEPLOY)** | +0.0446 | -0.6697 |
| **E1 dim2 (EMBODY↔LAUNCH)** | -0.0452 | +0.4277 |

- RAW: same-index dim1 corr = **+0.0446** (|·| < 0.10 — the reflection-only tripwire that HALTed item A); dim2 = +0.4277; the LARGEST entry is OFF-diagonal (|E1_dim1 × refit_dim2| = 0.6697). sum|diag| = 0.4723 < sum|anti| = 0.7148 ⇒ **ANTI-diagonal dominant** (axes rotated/swapped).

**POST-alignment corr matrix (E1 rows × aligned-refit cols) — AFTER Q:**

| | refit dim1 (aligned) | refit dim2 (aligned) |
|---|---|---|
| **E1 dim1 (PERFORM↔DEPLOY)** | +0.6364 | -0.4012 |
| **E1 dim2 (EMBODY↔LAUNCH)** | -0.4003 | +0.2692 |

- POST: the largest entry is now ON the diagonal (E1_dim1 × aligned_dim1 = **+0.6364**); sum|diag| = 0.9055 > sum|anti| = 0.8015 ⇒ **DIAGONAL-DOMINANT** (assert PASS — the ruling's sanity gate + HALT condition).
- **Disclosed structural finding:** the aligned dim2 tracks E1_dim2 only weakly (**+0.2692**), BELOW its off-diagonal (-0.4003) — the refit's second axis does NOT survive the ~117° rotation cleanly. Diagonal dominance holds for the matrix as a whole (mass + max-entry on-diagonal) but not per-row for row 2. This is the honest geography signal, not smoothed.
- Edition-I axis names (ratified): dim1 **PERFORM ↔ DEPLOY**, dim2 **EMBODY ↔ LAUNCH**. The refit basis carries NO ratified axis names (comparison artifact). Report-printed aligned coords match the emitted JSON points exactly (max L1 mismatch = 1.13e-07 — same Q, one frame).

## §3 — Inertia + retained-dimension comparison

| quantity | Edition-I | Refit Candidate 1 |
|---|---|---|
| active N (fit) | 469 | 628 |
| retained dims (parallel analysis) | 14 | **17** |
| plane (dim1+dim2) corrected inertia % | 8.36 | **8.903** |
| dim1 corrected inertia % | (see E1 loadings) | 5.154 |
| dim2 corrected inertia % | (see E1 loadings) | 3.749 |
| plane diameter (retained space) | (E1 frozen) | 5.2946 |

- Refit retained 17 dims vs Edition-I's 14 (parallel-analysis 95th-pct-null threshold, same rule). Plane explanatory power 8.903% vs 8.36%.
- Refit per-dim corrected inertia %: 5.15, 3.75, 3.70, 3.30, 3.14, 2.79, 2.51, 2.33, 2.13, 2.11, 1.95, 1.91, 1.85, 1.73, 1.65, 1.58, 1.50.

## §4 — Lost Ark landings (62 LA kits — all NEW in the refit fit)

- **62 LA active kits** entered the fit (62). Of these, **6 are Destroyer skill-grain** (`la-destroyer-*`) and **56 are class-grain** (other LA classes). (The brief's recon framing was 4 Destroyer skill-grain + 58 class-grain; the corpus actually carries 6 Destroyer + 56 class-grain — reported as-is.)

**Destroyer skill-grain kits — 5 nearest active neighbors each (plane distance; aligned coords):**

- **la-destroyer-gravity-compression** @ (0.486, 0.570) [gateA —] → gd-righteous-fervor-dervish (0.079), la-summoner-master-summoner (0.089), gd-savagery-warder (0.100), la-destroyer-gravity-force (0.127), gd-belgothian-blademaster (0.142)
- **la-destroyer-gravity-force** @ (0.575, 0.660) [gateA —] → la-summoner-master-summoner (0.089), la-artillerist-firepower-enhancement (0.108), la-destroyer-gravity-compression (0.127), la-machinist-evolutionary-legacy (0.128), la-sorceress-igniter (0.139)
- **la-destroyer-gravity-impact** @ (0.706, 0.736) [gateA —] → la-sorceress-igniter (0.065), la-artillerist-barrage-enhancement (0.080), la-machinist-evolutionary-legacy (0.106), la-artillerist-firepower-enhancement (0.147), la-destroyer-gravity-force (0.152)
- **la-destroyer-gravity-training** @ (1.011, 0.913) [gateA —] → la-destroyer-rage-hammer (0.082), la-aeromancer-wind-fury (0.263), la-reaper-hunger (0.267), la-striker-esoteric-flurry (0.267), la-deathblade-remaining-energy (0.267)
- **la-destroyer-rage-hammer** @ (0.955, 0.852) [gateA —] → la-destroyer-gravity-training (0.082), la-deathblade-remaining-energy (0.263), la-reaper-hunger (0.263), la-striker-esoteric-flurry (0.263), la-destroyer-gravity-impact (0.275)
- **la-destroyer-vortex-gravity** @ (0.065, 0.509) [gateA —] → la-machinist-arthetinean-skill (0.073), la-scrapper-ultimate-skill-taijutsu (0.090), la-sorceress-reflux (0.117), la-deadeye-pistoleer (0.141), d2-frenzy-barb (0.144)

**Class-grain LA (56 kits) summary:**
- Centroid (aligned x,y) = (0.734, 1.011); RMS spread about centroid = 0.453 (plane diameter = 5.295 → spread = 8.6% of diameter).
- gateA groups appearing among class-grain LA kits' 5-nearest neighbors (labelled kits only): TRAP-MINE×1.
- Class-grain LA kits carrying a gateA label themselves: none.

## §5 — The 10 pull kits at honest coordinates (do they cohere?)

- **10 pull kits** (the run's reason for being) at their refit ACTIVE **aligned** coordinates:

| kit_id | aligned (x, y) | gateA |
|---|---|---|
| d3-wizard-black-hole | (0.175, 0.312) | — |
| d3-zbarb | (0.008, 0.196) | — |
| d4-spiritborn-vortex | (0.662, 1.112) | — |
| di-cyclone-monk-pvp | (-0.291, 0.415) | — |
| di-cyclone-strike-monk-base | (0.197, 0.894) | — |
| la-destroyer-gravity-force | (0.575, 0.660) | — |
| la-destroyer-gravity-impact | (0.706, 0.736) | — |
| la-destroyer-gravity-training | (1.011, 0.913) | — |
| la-destroyer-rage-hammer | (0.955, 0.852) | — |
| la-destroyer-vortex-gravity | (0.065, 0.509) | — |

- Pull-kit centroid (aligned x,y) = (0.406, 0.660). **Mean pairwise distance = 0.6664; max = 1.3936; RMS spread about centroid = 0.4995** (all Q-invariant). Plane diameter = 5.295 → mean pairwise = 12.6% of diameter.
- Cohesion context: a random draw of 10 active kits has mean pairwise = 0.8018 ± 0.1780 (2000 draws). The pull kits' mean pairwise (0.6664) sits at the **23.8 percentile** of that null (lower = tighter/more cohesive than random).

## §6 — Fuse-table delta (Edition-I 469 vs refit 628)

Levels that FUSE (n<10) per coordinate — the ones that lose an independent fit column:

| coord | Edition-I fused (n) | Refit fused (n) | delta |
|---|---|---|---|
| movement | — | — | — |
| delivery | line(2), other(2) | line(2), other(2) | — |
| amp | — | — | — |
| geometry | melee_arc(1), fork(1), ground_slam(2), ricochet_bounce(2), teleport(3), beam_channel(3), self_buff(5), aura(8), line(8), ring(9) | melee_arc(1), fork(1), ground_slam(2), ricochet_bounce(2), teleport(3), beam_channel(3), self_buff(5), ring(9), line(9) | un-fused (earns column now): aura |
| treatment | — | — | — |
| function | fear(3), blind(7) | fear(7), blind(7) | — |
| defense | — | — | — |
| economy | spend+cooldown(1), spend+finite(1) | spend+cooldown(1), spend+finite(1) | — |
| proxy | — | — | — |
| range | — | — | — |
| tempo | — | — | — |
| commit | — | — | — |
| activation | — | — | — |
| dependency | — | — | — |

- **pull** (function): fused in Edition-I? N/A — pull absent from the 469 fit vocabulary — **un-fused in refit (n=10, earns a column)**. This is the load-bearing change enabling the pull un-mask in the ghost field.
- **melee** (delivery): delivery=melee earns a column in the refit (n=31); Edition-I's 469 fit had delivery=melee below the line / masked → MELEE ghost-image collapse. Refit un-masks it.

## §7 — Gates A–D: Edition-I vs Refit Candidate 1 (PASS/FAIL both columns)

| gate | Edition-I | Refit Candidate 1 |
|---|---|---|
| A group-recovery | **PASS** (ARI=0.668) | **FAIL** (ARI=0.451) |
| B negative-geography | FAIL (intrinsic-red k=5; → Finding F-1) | **FAIL** (intrinsic-red k=12) |
| C franchise-mixing | **PASS** (R²=0.0757; PERMDISP p=0.066) | **gandalf-rules** (R²=0.1683; PERMDISP p=0.004 SIGNIFICANT) |
| D stability | **PASS** (boot=3.60% diam) | **PASS** (boot=2.26% diam) |

- Edition-I froze on **A+C+D+F-1** (Gate B reclassified as the non-downgradable Finding F-1: "kit death is not geography"). The refit's Gate-B intrinsic-red pool GREW from k=5 to k=12 (the 37 negatives are unchanged; more of them project cleanly into the 17-dim refit space).
- **The refit does NOT clear the Edition-I freeze bar** on its own gate profile: Gate A dropped below 0.6 (0.451) and Gate C's franchise-mixing R² more than doubled AND its PERMDISP went significant (dispersion heterogeneity — R² no longer self-interpreting; gandalf rules). Gate D (stability) is the one clean PASS, and is marginally tighter than Edition-I.
- These are EVIDENCE for Matt's adoption decision, per the charge — not emission blockers. The refit emitted regardless.

## §8 — Ghost-field deltas (Edition-III served vs refit)

| quantity | Edition-III | Refit Candidate 1 |
|---|---|---|
| register | v1.3 | v1.3 (byte-identical lattice) |
| meso_feasible | 11160 | 11160 |
| meso_sealed (L1+L2) | 1314 (756+558) | 1314 (756+558) |
| depth_sum_check (exact denom) | 767411820 | 767411820 |
| lit_cells | 202 | 202 |
| pull-lit cells | 4 | 4 |
| pull fit column | MASKED (no fit column) | **HONEST (un-masked)** |
| melee fit column | MASKED (ghost-image collapse) | **HONEST (un-masked)** |
| melee-lit cells | 0 (no ghost image) | 0 |
| unmapped_pending_curation | 114 | 114 |
| off_plane_corpus N | 94 | **26** |

- **Lattice byte-identical** (denominators / feasible / sealed / depth_sum all unchanged — the SPACE did not move; only the FIT projection of it did).
- **Pull masked→honest:** in Edition-III the pull meso cells projected on their other 6 core coords (masked-like, no `pull` column). In the refit they land at honest coordinates. Example pull-lit tuples and their coordinate shift:

| pull-lit core tuple | refit honest (aligned x,y) |
|---|---|
| FREE-MOVE·ZONE·damage·pull·solo·active·one-shot | (0.186, 0.308) |
| ROOTED·ZONE·damage·pull·solo·active·build→spend | (0.712, 0.986) |
| ROOTED·ZONE·damage·pull·solo·active·one-shot | (0.379, 0.631) |
| WALK·NOVA·control·pull·solo·active·one-shot | (-0.562, 0.457) |

- **MELEE un-mask:** delivery=melee had NO meso ghost image in Edition-I/II/III (masked-like). The refit gives MELEE meso cells honest coordinates (1674 feasible MELEE cells now placed). melee-lit = 0 (live corpus MELEE-meso lighting under the refit lit-map). The ghost-image collapse partially closes at the geometry level; the lit census is a separate question.

**Census note — off_plane_corpus honesty correction (fit-relative re-derivation, 2026-07-16).** The `off_plane_corpus N` cell above reads **94 → 26** because the Edition-III-served value (94) was a *carried-over fit-relative fact* that went false when the refit's stage predicate (combat-kit ∧ cell_key NOT NULL ∧ negative=0 → 628) ADMITTED all 94 gear-grain `mcd-` kits as on-plane points. Honest refit off-plane N = **26** — the mcd rows that carry no cell key and thus never entered the fit (0/26 overlap with points). The emitted `off_plane_corpus.disclosure` now states the grain fact for Matt's eyes: **the 94 gear-grain mcd kits are ADMITTED at kit grain by this refit's stage predicate — the E1-era deferred grain ruling is thereby exercised implicitly and remains OPEN for Matt; 26 mcd rows remain off-plane.** By contrast `unmapped_pending_curation` (114) is NOT stale — it is a *lit-map census* (kits lacking a `fit2reg_movement` mapping, movement=blank, absent from the lit-lattice census) re-derived from the refit's own lit_map to the byte-identical 114; all 114 are nonetheless plotted on-plane points ("unmapped" = not in the lit-map, NOT off-plane), and the emission now carries an `unmapped_pending_curation_disclosure` field saying exactly that so the plate cannot be misread. The **TRUE 159 new-actives split** (refit 628 vs Edition-I 469; 0 dropped): **94 mcd gear-grain + 62 Lost Ark (56 class-grain + 6 Destroyer skill-grain) + 3 pull re-keys (d3/di/d4)**.

## §9 — Six condensation (gateA) centroid shifts (Edition-I → refit)

Centroids computed over each group's LABELLED kits. E1 = E1's served raw plane; refit = the **Q-aligned** plane. Aligned-frame shift = displacement in the §1 Procrustes-standardized frame (comparable units, scale removed).

| group | n | E1 centroid | refit aligned centroid | aligned-frame shift | % diam |
|---|---|---|---|---|---|
| WHIRLWIND | 15 | (0.819, -1.082) | (0.647, -0.627) | 0.0675 | 33.0% |
| TOTEM-SENTRY | 24 | (-0.731, -0.352) | (-0.276, -0.311) | 0.0464 | 22.7% |
| TRAP-MINE | 23 | (-0.098, 0.217) | (-0.368, 0.028) | 0.0114 | 5.6% |
| CHANNELED-BEAM | 9 | (1.141, -0.272) | (0.511, -0.304) | 0.0628 | 30.7% |
| AURA | 8 | (0.346, -0.428) | (0.668, -0.478) | 0.0190 | 9.3% |
| MINION-PET | 7 | (-0.191, -0.999) | (0.226, -0.794) | 0.0523 | 25.5% |

- The aligned-frame shift isolates how much each condensation's CENTER moved after the global rotation/scale is removed — i.e. genuine structural drift of that build-family's location, not a framing artifact.

## §10 — Beyond-horizon census on the refit plane (ALIGNED; ALL 628 actives)

**Hulls (computed-not-constant, both variants — aligned refit ghost field):**
- meso-only hull: 21 vertices (over 11160 aligned feasible cells). charted hull (meso feasible ∪ drill-in sub-feasible): 25 vertices (over 11187 points incl. the 27-vertex drill-in reach envelope).

**Beyond-horizon membership — ALL 628 actives vs each hull:**
- **N beyond meso-only hull = 13** (Edition-era baseline: 14 — computed over Edition-III's 469 actives; here over all 628 in the aligned refit frame).
- **N beyond charted hull = 0** (Edition-III baseline: 0).

**Full beyond-meso-hull kit list (13)** (position aligned; overshoot = signed distance beyond the nearest hull face; octant/bearing = outward direction, 0°=+x EAST/PERFORM, 90°=+y):

| kit_id | aligned (x,y) | overshoot | octant | bearing° | gateA | franchise |
|---|---|---|---|---|---|---|
| la-soulfist-robust-spirit | (1.013, 1.627) | 0.2356 | NE | +60.4 | — | LostArk |
| la-soulfist-energy-overflow | (0.957, 1.567) | 0.1553 | NE | +60.4 | — | LostArk |
| la-arcanist-empresss-grace | (0.923, 1.499) | 0.0796 | NE | +60.4 | — | LostArk |
| la-arcanist-order-of-the-emperor | (0.923, 1.499) | 0.0796 | NE | +60.4 | — | LostArk |
| tl1-alchemist-summoner | (0.669, -1.007) | 0.0232 | SE | -43.2 | — | Torchlight |
| la-deathblade-surge | (0.942, 1.414) | 0.0152 | NE | +60.4 | — | LostArk |
| la-reaper-lunar-voice | (0.942, 1.414) | 0.0152 | NE | +60.4 | — | LostArk |
| la-scrapper-shock-training | (0.942, 1.414) | 0.0152 | NE | +60.4 | — | LostArk |
| la-souleater-full-moon-harvester | (0.942, 1.414) | 0.0152 | NE | +60.4 | — | LostArk |
| la-striker-deathblow | (0.942, 1.414) | 0.0152 | NE | +60.4 | — | LostArk |
| tq2-whirlwind-rogue | (1.082, -0.442) | 0.0118 | SE | -30.8 | WHIRLWIND | TitanQuest |
| di-whirlwind-barb | (0.997, -0.585) | 0.0115 | SE | -30.8 | WHIRLWIND | Diablo |
| ud-whirlwind-str | (0.836, -0.806) | 0.0067 | SE | -43.2 | WHIRLWIND | undecember |

**Full beyond-CHARTED-hull kit list: NONE** — the charted hull (meso + EAST drill-in) contains every active in the aligned frame.

**Per-quadrant overshoot breakdown (beyond meso-hull):**

| quadrant | n | max overshoot | at kit | bearing° |
|---|---|---|---|---|
| EAST-N | 9 | 0.2356 | la-soulfist-robust-spirit | +60.4 |
| EAST-S | 4 | 0.0232 | tl1-alchemist-summoner | -43.2 |

**Per-octant (direction) overshoot breakdown (beyond meso-hull):**

| octant (direction) | n | max overshoot | at kit | bearing° |
|---|---|---|---|---|
| NE | 9 | 0.2356 | la-soulfist-robust-spirit | +60.4 |
| SE | 4 | 0.0232 | tl1-alchemist-summoner | -43.2 |

**Coverage verdict — does the EAST-half pinned drill-in cover the overshoot?**

- **P-DF-1 (evidence):** verdict **PASS** — S_max = 1.9082 (drill-in reach along û) vs K_max_beyond_horizon = 1.1547 (max beyond-hull active along û); û = [0.8438, -0.5367]; n_beyond_horizon_kits = 13. S_max > K_max ⇒ the EAST drill-in EXTENDS PAST the beyond-horizon reach along û.

- **Beyond-meso-hull overshoot by side of the pin:** EAST (x≥0, the pinned side) = 13 kits; WEST (x<0, NOT coverable by the EAST-half pin) = 0 kits.
- **Directions the pinned region does NOT cover** (direct input to gandalf's drill-in-expansion decision):

  - **NONE.** Every beyond-meso-hull overshoot is on the EAST (pinned) side, and the charted hull (meso + EAST drill-in) contains every active — the EAST-half drill-in covers the overshoot; no uncovered direction remains.

- NO recommendations — numbers only (gandalf synthesizes whether the candidate plate needs a drill-in-expansion pass before Matt's comparison).

---

**Provenance:** all numbers computed by `refit_candidate_1_comparison_2026_07_16.py` from `atlas-coordinates-active.csv` (Edition-I frozen, 469), `refit-candidate-1-coordinates-active.csv` (refit, 628), `atlas-refit-candidate-1.json`, `atlas-edition3.json`, and `refit-candidate-1-basis-draft.json`. Gate values quoted from the respective gate reports. Edition III and every served artifact were READ-ONLY throughout.

---

## §11 — Interpretation + the adoption fork (gandalf closes the package — ELICITOR: options + tradeoffs + lean stated; **Matt rules**)

*Everything above this section is numbers (elrond). Everything below is synthesis (gandalf). Where a number is cited, the section that computed it is named.*

### 11.1 What is actually being decided

Not "which plate looks better." The fork is: **does the served fit track the corpus, and on what terms?** Edition III fits the 469-active corpus frozen at Edition I; the corpus is now 628 actives. The 159 new: **94 mcd gear-grain + 62 Last Ark (56 class-grain + 6 Destroyer skill-grain) + 3 pull re-keys d3/di/d4** (§8 census note; corpus.db-derived, 0 dropped). The lattice is byte-identical both sides (depth Σ 767,411,820). Only the FIT moved — so every difference on the candidate plate is exactly one of: (a) orientation convention, (b) new citizens, (c) genuine rearrangement of shared citizens.

### 11.2 Two effects, decomposed (why the plates are comparable at all)

- **(a) is removed by construction.** The refit plane came out rotated −117.35° + reflected vs Edition-I orientation (§2; raw same-index corr 0.045). The Q-alignment (in-plane orthogonal Procrustes, no scaling/translation — RATIFIED Matt 2026-07-16) strips the maximal convention-attributable difference and is disclosed on-plate. What remains after Q is **irreducible real change**.
- **(b)+(c) quantified:** plane congruence **0.468** vs full-14-dim congruence **0.860** (§1). Read together: *the deep structure mostly held; the 2-D camera angle and the passenger manifest changed.* Corroboration: P-DF-1 — the drill-in doctrine's falsifiable east-frontier prediction — **passes in both frames** (refit S 1.908 > K 1.155, n=13; E3 S 2.841 > K 1.874, n=14). The frontier direction is fit-stable.
- **Disclosed caveat:** aligned dim2 tracks E1's dim2 only weakly (+0.269 vs cross-term −0.400, §2) because the refit's dims 2/3 are a near-tie (3.749% vs 3.70%, §3) — **eigen-fragility**. The candidate's N–S reading is softer than E1's was. Adoption inherits that.

### 11.3 The honesty ledger (what the refit fixes)

Edition III, as served, renders a corpus that no longer exists: (1) **159 real corpus rows appear nowhere on it** — the refit plots every stage-admitted row; (2) **pull=10 survives FUSE_MIN natively; delivery-melee=31 is a real column** (§5, §6) — E3 carries both as bolted-on honest-coordinate glosses; (3) **aura un-fuses** — a 13th promoted geometry level at drill-in grain (§6); (4) **self-consistency** — census, frontier, hulls, drill-in all re-derive from the refit's own fit. Where a carried census ledger silently violated that (`off_plane_corpus`), the verify gate caught it, the honest re-derivation landed (§8 census note), and the three-class fact rule (atlas MIGRATION) + standing asserts at both emission and render seams now pin the class.

### 11.4 The contamination ledger (what adoption would ratify) — including the Gate-C ruling §7 assigns

1. **The refit does not clear the Edition-I freeze bar on its own gate profile** (§7): A **FAIL** (ARI 0.451 vs E1's 0.668 — group-recovery floor broken) · B **FAIL, worsened within FAIL** (intrinsic-red k 5→12: the 37 negatives are unchanged, but more of them project *cleanly* into the 17-dim refit space — Finding F-1, "kit death is not geography," erodes further) · C **not clean** (ruled below) · D **PASS, tighter than E1** (2.26% vs 3.60%). Stability is not the problem; **identity is.**
2. **Gate-C ruling (gandalf, as §7 assigns):** R² doubled (0.0757→0.1683) AND PERMDISP went significant (p=0.004 — dispersion heterogeneity), so R² is no longer self-interpreting as a pure location effect: part of the franchise signal may be "new franchises spread differently" rather than "new franchises sit elsewhere." **Ruled: C = NOT CLEAN for adoption purposes under either reading** — location effect and dispersion effect BOTH trace to the same root, the grain composition: gear-grain rows condense tight (the mcd southeast cluster is visible on the plate), class-grain rows spread wide. Whether franchise identity structures the map's positions or its variances, it now structures the map.
3. **The root — grain:** 150/159 (94.3%) of the corpus growth is grain-questionable (94 gear-grain + 56 class-grain; the clean 9 are the 6 Destroyer skill-grain rows ≈ kit grain + 3 pull re-keys). The refit is a *faithful fit of a corpus whose grain ruling was never made*. Gate degradation is the statistical shadow of exactly that.
4. **The grain ruling is now exercised-but-open.** E1-era deferred the mcd ruling; the refit's stage predicate admitted all 94 mechanically; the emission discloses this on-plate (`off_plane_corpus.disclosure`). Adopting the candidate as-is would **launder an unmade ruling into served truth.**

### 11.5 The entanglement (the load-bearing insight)

The adoption fork is two questions wearing one coat. **Q-grain (upstream):** are gear-grain mcd rows and class-grain LA rows legitimate atlas citizens at kit grain — admit, exclude, or re-grain (decompose LA classes toward kit grain; roll mcd gear-skills up)? **Q-fit (downstream):** should the served fit refresh to the current corpus? Q-fit cannot be answered ahead of Q-grain: if the ruling re-grains or excludes, the 628-corpus is not the corpus, and this candidate is a fit of an intermediate state — adopting it buys a second refit and a second serving cutover. If the ruling admits as-is, the gate degradation stops being "contamination" and becomes **the true shape of the grown domain** — and E3 becomes a nostalgic map of a smaller world.

**Genre precedent:** this is the Diablo III auction-house lesson and PoE's league-to-core ratification discipline in miniature. D3 served an undecided economy ruling and had to amputate served truth later, at full price. GGG gates league mechanics through explicit ratification into core precisely so the served game never embodies a ruling nobody made. When an unresolved content ruling leaks into the served surface, unwinding it costs more than deciding it up front ever would.

### 11.6 The fork, decision-shaped (**Matt rules**)

**Option 1 — ADOPT as Edition IV now.** Honest to corpus-as-is; every admitted row on-plane; pull/melee/aura native. Requires: §7 sim-falsification WAIVER (E1 froze with sim evidence; the candidate has none), display-name map, serving cutover, glance re-vendor. Cost: a gate profile below the E1 freeze bar becomes the served baseline; the franchise-shadowed geography is what design reads; the grain ruling gets made implicitly, by default.

**Option 2 — KEEP E3 SERVED · RULE GRAIN · REFIT ONCE (gandalf's lean).** The candidate's highest value is as the **grain ruling's evidence exhibit**, not as Edition IV. It is the empirical demonstration of what admission does to the map — gate profile below the freeze bar, franchise effect, density 3.1 vs 2.3 pts/u² — which is precisely the substrate evidence the ruling needs (substrate-led discipline: recognize → validate against substrate evidence → commit; the candidate IS the validation instrument). Sequence: Matt rules mcd grain + LA grain → corpus re-staged per ruling → ONE refit on the ruled corpus → that candidate faces adoption with clean provenance AND a planned sim-falsification pass, so Edition IV needs no waiver. Cost: E3 stays stale a while longer (mitigable with one honest "corpus has grown; refit pending grain ruling" gloss on the served plate); a second refit's compute is trivial.

**Option 3 — ADOPT NOW, RULE LATER.** Staleness is the worse sin; serve the honest-to-corpus map today, correct grain in a v-next. Risk: TWO serving cutovers (E3→E4→E4′), and in the interim every downstream consumer calibrates against the franchise-shadowed geography. Unwinding served truth is costlier than never serving the undecided.

**Lean: Option 2.** One sentence of why: **adoption should ratify a ruling, not substitute for one.** Flip condition: if Matt rules Q-grain = "admit as-is," the candidate already IS the fit of the ruled corpus, the gate profile is the domain's true shape rather than contamination, and re-deriving would be ceremony — adopt (with the §7 waiver explicit, or a fast sim-falsification pass to retire it).

**Standing-directive note:** *"run the full Tier 3 with Last Ark and Pull/Gravity"* is SATISFIED by this experiment — LA + pull/gravity are in the candidate. The directive ordered the comparison; it did not pre-decide adoption or grain. At the grain ruling, the live LA question is narrower than in/out: class-grain rows as-is vs decomposed toward kit grain.

### 11.7 If adoption fires (Option 1 or 3) — mechanical checklist

§7 waiver recorded in decisions-log · display-name map (Refit-Candidate-1 → Edition IV) · serving cutover + glance re-vendor (separate wave, gandalf's verify gate) · eigen-fragility caveat (11.2) carried into the Edition-IV banner · MELEE v1.4 register gap remains Matt-gated (unchanged by adoption) · any hull-law refinement (alpha-shape / occupancy gloss) lands on BOTH plates or neither.

### 11.8 Render CHANGED-observations, dispositions (closes galadriel's demoted-smoke table)

| Observation | Disposition |
|---|---|
| mcd- emission tension | **RESOLVED — emission defect** (stale E3 `off_plane_corpus` carryover; honest 26 + grain-admission disclosure emitted; three-class fact rule in MIGRATION; standing asserts both seams) |
| density 3.1 vs 2.3 pts/u² | **REAL** — 159 new actives; dense-clustered, not wide-ranging (charted hull −24%; r50 0.502 vs 0.656) |
| meso-beyond profile NEUTRAL:10+WW:3 (was WW:10+CB:3+N:1) | **REAL** — frontier composition shift; NE overshoot all-LA; charted-hull beyond-N = 0 (§10); drill-in expansion NOT NEEDED |
| 1 lit cell outside points frame | **DISCLOSED BY DESIGN** — points-only bounds law; clip line renders 287 = 1 lit + 286 unlit; the cell (x=−1.658) sits west of live mass |

---

**Signed:** gandalf — the map serves the ruling; the ruling does not hide inside the map.
