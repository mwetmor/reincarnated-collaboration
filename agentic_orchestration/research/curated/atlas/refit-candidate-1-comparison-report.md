# Refit Candidate 1 vs Edition III (Edition-I fit) — comparison report

**Date:** 2026-07-16 · **Executor:** elrond (numbers only — gandalf synthesizes the reading).
**Artifact:** `atlas-refit-candidate-1.json` (unratified comparison artifact) vs the FROZEN Edition-I fit that Edition III serves. This is a COMPARISON EXPERIMENT, not an Edition — "Edition IV" appears NOWHERE.
**Fit sets:** Edition-I fit = 469 active (frozen, pre-C3 keys). Refit = 628 active (live keys). Shared actives = **469** (all 469 Edition-I kits are a subset of the refit's 628; 0 dropped). New in refit = **159**.

> **Red-ink headline (gate evidence for adoption):** Edition-I froze on A+C+D (+F-1). Refit gates: **A FAIL · B FAIL · C gandalf-rules (PERMDISP-significant) · D PASS.** Gates are EVIDENCE for the decision, not emission blockers. See §7.

## §1 — Procrustes congruence + RMS displacement (469 shared actives)

- **Plane (dim1×dim2) Procrustes disparity M² = 0.78127 → congruence √(1−M²) = 0.4677** (1.0 = identical up to rotation/scale/reflection).
- Standardized-frame plane diameter = 0.2047. **RMS displacement = 0.0408 = 19.94% of plane diameter; median = 0.0329 = 16.05%.**
- **Full retained-space congruence** (first 14 shared dims of E1's 14 vs refit's 17): √(1−M²) = 0.8595 (M²=0.26127).

**Top-20 movers on the plane** (Procrustes-standardized displacement; old/new are raw dim1,dim2):

| kit_id | E1 (x,y) | refit (x,y) | disp (std) | % diam | gateA |
|---|---|---|---|---|---|
| tq2-whirlwind-rogue | (1.111, -1.490) | (-0.105, -1.164) | 0.1040 | 50.8% | WHIRLWIND |
| di-whirlwind-barb | (1.058, -1.562) | (0.061, -1.154) | 0.1029 | 50.2% | WHIRLWIND |
| le-frost-claw | (0.797, 0.635) | (0.217, 0.690) | 0.0975 | 47.6% | — |
| hot-dragons-breath | (0.867, 0.388) | (0.340, 0.247) | 0.0864 | 42.2% | — |
| ud-flamethrower-channel | (1.390, -0.321) | (0.104, -0.533) | 0.0852 | 41.6% | CHANNELED-BEAM |
| ud-whirlwind-str | (1.007, -1.361) | (0.332, -1.113) | 0.0811 | 39.6% | WHIRLWIND |
| poe1-arc | (0.341, 0.886) | (0.392, -0.126) | 0.0810 | 39.6% | — |
| poe1-incinerate | (1.389, 0.047) | (-0.178, -0.467) | 0.0802 | 39.2% | CHANNELED-BEAM |
| ud-cwc-spin-caster | (0.914, -0.954) | (0.343, -0.444) | 0.0797 | 38.9% | WHIRLWIND |
| hot-exterminator-burn | (0.967, 0.344) | (0.321, -0.156) | 0.0794 | 38.8% | — |
| le-warpath-vk | (1.023, -1.283) | (0.441, -0.983) | 0.0791 | 38.6% | WHIRLWIND |
| di-ray-of-frost-wizard | (1.029, -0.531) | (0.217, -0.243) | 0.0786 | 38.4% | CHANNELED-BEAM |
| d3-call-of-the-ancients | (-1.158, -0.527) | (0.336, 0.294) | 0.0781 | 38.2% | — |
| d2-bvc | (0.711, -1.211) | (0.156, -0.825) | 0.0778 | 38.0% | WHIRLWIND |
| poe2-tempest-bell | (-0.599, -0.326) | (-0.509, -0.040) | 0.0774 | 37.8% | — |
| di-draw-quarter-crusader | (-0.041, -0.742) | (-0.057, 0.429) | 0.0760 | 37.1% | — |
| tq-shield-charge-conqueror | (-0.041, -0.742) | (-0.057, 0.429) | 0.0760 | 37.1% | — |
| poe1-edc | (0.296, 0.776) | (0.471, 0.122) | 0.0753 | 36.8% | — |
| poe1-earthshatter | (-1.105, -0.054) | (-0.130, 0.341) | 0.0752 | 36.7% | — |
| poe1-freezing-pulse | (0.267, 0.776) | (0.480, 0.019) | 0.0748 | 36.5% | — |

## §2 — Axis identity (did LAUNCH/EMBODY + PERFORM/DEPLOY survive?)

- After optimal Procrustes alignment of the refit plane into Edition-I's plane frame, the aligned-axis correlations are:

| | refit dim1 (aligned) | refit dim2 (aligned) |
|---|---|---|
| **E1 dim1 (PERFORM↔DEPLOY)** | 0.6364 | -0.4012 |
| **E1 dim2 (EMBODY↔LAUNCH)** | -0.4003 | 0.2692 |

- Diagonal dominance (|r11|,|r22| vs off-diagonal |r12|,|r21|) = the "axes survived in place" signal; a large off-diagonal = axis swap/rotation. (Procrustes has already removed a global rotation/reflection, so residual off-diagonal is structural, not framing.)
- Edition-I axis names (ratified): dim1 **PERFORM ↔ DEPLOY**, dim2 **EMBODY ↔ LAUNCH**. The refit basis carries NO ratified axis names (comparison artifact).

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

**Destroyer skill-grain kits — 5 nearest active neighbors each (plane distance):**

- **la-destroyer-gravity-compression** @ (-0.730, -0.170) [gateA —] → gd-righteous-fervor-dervish (0.079), la-summoner-master-summoner (0.089), gd-savagery-warder (0.100), la-destroyer-gravity-force (0.127), gd-belgothian-blademaster (0.142)
- **la-destroyer-gravity-force** @ (-0.851, -0.207) [gateA —] → la-summoner-master-summoner (0.089), la-artillerist-firepower-enhancement (0.108), la-destroyer-gravity-compression (0.127), la-machinist-evolutionary-legacy (0.128), la-sorceress-igniter (0.139)
- **la-destroyer-gravity-impact** @ (-0.978, -0.289) [gateA —] → la-sorceress-igniter (0.065), la-artillerist-barrage-enhancement (0.080), la-machinist-evolutionary-legacy (0.106), la-artillerist-firepower-enhancement (0.147), la-destroyer-gravity-force (0.152)
- **la-destroyer-gravity-training** @ (-1.275, -0.479) [gateA —] → la-destroyer-rage-hammer (0.082), la-aeromancer-wind-fury (0.263), la-reaper-hunger (0.267), la-striker-esoteric-flurry (0.267), la-deathblade-remaining-energy (0.267)
- **la-destroyer-rage-hammer** @ (-1.196, -0.457) [gateA —] → la-destroyer-gravity-training (0.082), la-deathblade-remaining-energy (0.263), la-reaper-hunger (0.263), la-striker-esoteric-flurry (0.263), la-destroyer-gravity-impact (0.275)
- **la-destroyer-vortex-gravity** @ (-0.482, 0.176) [gateA —] → la-machinist-arthetinean-skill (0.073), la-scrapper-ultimate-skill-taijutsu (0.090), la-sorceress-reflux (0.117), la-deadeye-pistoleer (0.141), d2-frenzy-barb (0.144)

**Class-grain LA (56 kits) summary:**
- Centroid (dim1,dim2) = (-1.235, -0.187); RMS spread about centroid = 0.453 (plane diameter = 5.295 → spread = 8.6% of diameter).
- gateA groups appearing among class-grain LA kits' 5-nearest neighbors (labelled kits only): TRAP-MINE×1.
- Class-grain LA kits carrying a gateA label themselves: none.

## §5 — The 10 pull kits at honest coordinates (do they cohere?)

- **10 pull kits** (the run's reason for being) at their refit ACTIVE coordinates:

| kit_id | (x, y) | gateA |
|---|---|---|
| d3-wizard-black-hole | (-0.357, -0.012) | — |
| d3-zbarb | (-0.177, 0.083) | — |
| d4-spiritborn-vortex | (-1.292, -0.078) | — |
| di-cyclone-monk-pvp | (-0.235, 0.449) | — |
| di-cyclone-strike-monk-base | (-0.885, 0.236) | — |
| la-destroyer-gravity-force | (-0.851, -0.207) | — |
| la-destroyer-gravity-impact | (-0.978, -0.289) | — |
| la-destroyer-gravity-training | (-1.275, -0.479) | — |
| la-destroyer-rage-hammer | (-1.196, -0.457) | — |
| la-destroyer-vortex-gravity | (-0.482, 0.176) | — |

- Pull-kit centroid (dim1,dim2) = (-0.773, -0.058). **Mean pairwise distance = 0.6664; max = 1.3936; RMS spread about centroid = 0.4995.** Plane diameter = 5.295 → mean pairwise = 12.6% of diameter.
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
| off_plane_corpus N | 94 | 94 |

- **Lattice byte-identical** (denominators / feasible / sealed / depth_sum all unchanged — the SPACE did not move; only the FIT projection of it did).
- **Pull masked→honest:** in Edition-III the pull meso cells projected on their other 6 core coords (masked-like, no `pull` column). In the refit they land at honest coordinates. Example pull-lit tuples and their coordinate shift:

| pull-lit core tuple | refit honest (x,y) |
|---|---|
| FREE-MOVE·ZONE·damage·pull·solo·active·one-shot | (-0.360, -0.024) |
| ROOTED·ZONE·damage·pull·solo·active·build→spend | (-1.203, -0.180) |
| ROOTED·ZONE·damage·pull·solo·active·one-shot | (-0.735, -0.046) |
| WALK·NOVA·control·pull·solo·active·one-shot | (-0.148, 0.709) |

- **MELEE un-mask:** delivery=melee had NO meso ghost image in Edition-I/II/III (masked-like). The refit gives MELEE meso cells honest coordinates (1674 feasible MELEE cells now placed). melee-lit = 0 (live corpus MELEE-meso lighting under the refit lit-map). The ghost-image collapse partially closes at the geometry level; the lit census is a separate question.

## §9 — Six condensation (gateA) centroid shifts (Edition-I → refit)

Centroids computed over each group's LABELLED kits. Native = each fit's own raw plane. Aligned-frame shift = displacement in the §1 Procrustes-standardized frame (comparable units).

| group | n | E1 native centroid | refit native centroid | aligned-frame shift | % diam |
|---|---|---|---|---|---|
| WHIRLWIND | 15 | (0.819, -1.082) | (0.260, -0.863) | 0.0675 | 33.0% |
| TOTEM-SENTRY | 24 | (-0.731, -0.352) | (0.403, 0.102) | 0.0464 | 22.7% |
| TRAP-MINE | 23 | (-0.098, 0.217) | (0.144, 0.340) | 0.0114 | 5.6% |
| CHANNELED-BEAM | 9 | (1.141, -0.272) | (0.035, -0.594) | 0.0628 | 30.7% |
| AURA | 8 | (0.346, -0.428) | (0.118, -0.813) | 0.0190 | 9.3% |
| MINION-PET | 7 | (-0.191, -0.999) | (0.602, -0.565) | 0.0523 | 25.5% |

- The aligned-frame shift isolates how much each condensation's CENTER moved after the global rotation/scale is removed — i.e. genuine structural drift of that build-family's location, not a framing artifact.

---

**Provenance:** all numbers computed by `refit_candidate_1_comparison_2026_07_16.py` from `atlas-coordinates-active.csv` (Edition-I frozen, 469), `refit-candidate-1-coordinates-active.csv` (refit, 628), `atlas-refit-candidate-1.json`, `atlas-edition3.json`, and `refit-candidate-1-basis-draft.json`. Gate values quoted from the respective gate reports. Edition III and every served artifact were READ-ONLY throughout.
