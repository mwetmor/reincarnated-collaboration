# Leg-B (Edition-V) — Path-B refit + four-gate report

**Date:** 2026-07-22 · **Executor:** elrond · **Script:** `atlas_legb_refit_2026_07_22.py`
**Prereg:** `2026-07-22-leg-b-edition-next-preregistration.md` (BINDING, §13 fold)
**Seed:** 20260722 (all randomness pinned). **NUMBERS ONLY — conductor names axes from loadings.**
**Trigger:** STEP 1 vocabulary arm FIRED (19 absent levels >=20); expression arm did NOT. STEP 2 element_primary = ADMIT-AS-AXIS-INPUT (max mechanical V=0.555 vs `function`).

---

## STEP 3 — Path-B refit (B1)
- **Fit population:** record-class, atlas_coords 14-field = **265 kits** (record-267 minus 2 unprojectable degenerate kits d2-teleport-sorc/poe1-blood-magic-kit; annex+negatives supplementary-only).
- **Feature set (21 blocks):** 14 register coords (AXIS, coords 1-3 locked) + 6 geometry-band coords (primary skill_ordinal=0; 257/265 kits carry a band, rest passive) + element_primary (ADMIT; 165/265 non-null, rest passive).
- **Supplementary/validation-only (NOT axis input):** court + six-block overlays.
- **Rare-category fuse (Greenacre n<10 -> other-rare, once, all families):** delivery[aura-pulse,beam,line,orbit]; economy[spend+cooldown,spend+finite,summon-uptime]; function[blind,knockback]; gb_cadence[builder_spender]; gb_motion[blink_translate,chain_hop,fork_split,inward_pull,lane_place,leap_arc,ricochet_return]; gb_range[long,screen,short]; gb_speed[instant,slow]; gb_width[narrow]; geometry[aura,beam_channel,cone,dash_attack,line,ricochet_bounce,ring,self_buff,vortex_pull,whirlwind]; treatment[control]
- Indicator matrix: **265 rows × 87 columns** (21 MFA blocks; masks passive).
- MFA block weights (first singular value): movement=9.479, delivery=9.533, amp=9.806, geometry=6.996, treatment=5.644, function=8.536, defense=9.238, economy=8.527, proxy=9.279, range=10.076, tempo=10.361, commit=6.819, activation=9.034, dependency=8.600, gb_delivery=7.689, gb_range=7.109, gb_motion=6.347, gb_width=4.843, gb_speed=3.643, gb_cadence=6.158, element_primary=7.036
- **Parallel-analysis retention** (1000 column-permutation nulls, Greenacre-corrected inertia, NOT Kaiser): retain **17 dimensions**.

| dim | raw eig | Greenacre-adj inertia | Greenacre-adj %% | null-95 | retained |
|---|---|---|---|---|---|
| 1 | 0.27367 | 0.23663 | 5.25 | 0.12753 | Y |
| 2 | 0.26614 | 0.22910 | 5.08 | 0.11623 | Y |
| 3 | 0.21030 | 0.17384 | 3.86 | 0.10714 | Y |
| 4 | 0.19257 | 0.15654 | 3.47 | 0.10085 | Y |
| 5 | 0.18321 | 0.14748 | 3.27 | 0.09588 | Y |
| 6 | 0.15543 | 0.12086 | 2.68 | 0.09174 | Y |
| 7 | 0.14417 | 0.11021 | 2.44 | 0.08782 | Y |
| 8 | 0.14103 | 0.10726 | 2.38 | 0.08485 | Y |
| 9 | 0.13340 | 0.10011 | 2.22 | 0.08173 | Y |
| 10 | 0.12826 | 0.09534 | 2.11 | 0.07915 | Y |
| 11 | 0.12327 | 0.09071 | 2.01 | 0.07642 | Y |
| 12 | 0.11563 | 0.08368 | 1.86 | 0.07416 | Y |
| 13 | 0.11253 | 0.08084 | 1.79 | 0.07177 | Y |
| 14 | 0.10889 | 0.07753 | 1.72 | 0.06950 | Y |
| 15 | 0.10539 | 0.07436 | 1.65 | 0.06736 | Y |
| 16 | 0.09899 | 0.06860 | 1.52 | 0.06513 | Y |
| 17 | 0.09475 | 0.06481 | 1.44 | 0.06332 | Y |
| 18 | 0.08860 | 0.05936 | 1.32 | 0.06143 | n |
| 19 | 0.08574 | 0.05684 | 1.26 | 0.05949 | n |
| 20 | 0.08368 | 0.05504 | 1.22 | 0.05768 | n |
- **CATPCA twin** (ordinal tempo+commit): ARI(CATPCA vs MCA k-means, k=19) = 0.226 (divergence-as-diagnostic).
- **Gower→MDS** retention (1000 nulls): retain **4 dims**.
- **Leiden-CPM** (kNN k=10, 100 seeds, res 0.5-2.0): consensus count = 91 at res 0.5.
- **LCA** (stepmix, BIC k=2..12): selected **k=4**.
- **Cross-family ARI** (common k=91): MCA-kmeans~MDS-kmeans=0.087 · MCA-kmeans~Leiden=0.294 · MCA-kmeans~LCA=0.041 · MDS-kmeans~Leiden=0.210 · MDS-kmeans~LCA=0.033 · Leiden~LCA=0.043

## STEP 3 — B2 Procrustes anchor (translation+rotation+reflection, NO scale) + B3 congruence
- **Anchor = record-class gateA members** common to E5 fit AND E4 served plane: **46** (floor 40).
- **B2 transform (2D plane):** rotation angle = 58.54°, reflection = True, optimal scale s* = 0.8117 (DISCLOSED, NOT applied — E4 distance semantics preserved).
- **B3 congruence coefficient (2D plane, anchor n=46, post-transform) = 0.7836** — threshold ≥ 0.85 → **FAIL**.

- Anchor max-mover table (top 8 by post-anchor displacement):

| kit_id | Δ (plane units) | E4 (x,y) | E5-aligned (x,y) |
|---|---|---|---|
| d2-frenzy-barb | 1.4830 | (-0.070, 0.077) | (-0.128, -1.405) |
| poe1-mjolner | 1.4538 | (0.053, 0.625) | (-0.157, -0.814) |
| d2-horker | 1.1649 | (-0.142, 0.207) | (0.461, -0.789) |
| poe2-twister | 1.1538 | (0.643, -0.954) | (0.257, 0.134) |
| d2-auradin | 0.9905 | (0.418, -0.067) | (0.278, -1.048) |
| poe1-lightning-conduit | 0.7418 | (-0.414, 0.434) | (-0.131, -0.252) |
| poe2-minion-infernalist | 0.7141 | (-0.566, -0.546) | (-0.985, 0.033) |
| le-fire-aura-spellblade | 0.6895 | (0.381, -0.626) | (0.034, -0.030) |

## EXECUTION HALTED

**HALT:** B3 congruence 0.7836 < 0.85 (§8-C — refit-candidate-1 rotation precedent). Rotation 58.54°, reflection True, s*=0.8117 disclosed above; E5 NOT served, E4 remains truth.

The refit produced a plane that does not congruently anchor to E4's camera on the 46 record-class gateA members. Per §7 no-tuning-until-pass, elrond does NOT tune; conductor rules (§8-B/§8-C options).
