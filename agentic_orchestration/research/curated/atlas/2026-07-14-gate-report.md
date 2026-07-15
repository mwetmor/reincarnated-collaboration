# Atlas Derivation — Gate Report

**Date:** 2026-07-14 · **Executor:** elrond · **Script:** `agentic_orchestration/research/scripts/atlas_derivation_2026_07_14.py`
**Prereg:** `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` (v1.1, PINNED)
**Seed:** 20260714 (all randomness pinned). **NUMBERS ONLY — interpretation is gandalf's.**

---

## Stage 0 — verification

- **Snapshot marker:** `atlas-prereg-2026-07-14` PRESENT in `corpus_schema_meta`. OK.
- **Active set N = 469** (combat-kit, cell_key NOT NULL, negative=0). OK (== 469).
- **Negatives:** 38 total `negative=1` in canon_corpus; 37 are combat-kit with cell_key (projectable supplementary set for Gate B); 1 is a system-record (`vs-golden-egg-scaling`, per A.5 note — outside combat denominator, not projectable). Reconciliation: charter's "38 graveyard" = corpus count; fit-relevant projectable-negative count = 37.
- **Survivor-key SHA256** (469 rows, ordered by kit_id): `fa0be0dec6d88f7c92ec52dac4979d5eab185b37f8fc197e7e9c3df379abfb3b`
- **Structural:** all 469 active rows are exactly 14 pipe-delimited positions. OK.

### Stage 0a — Gate-A label table
- Loaded **86 rows** byte-verbatim into `atlas_gateA_labels_2026_07_14`. Group counts: WHIRLWIND 15 · TOTEM-SENTRY 24 · TRAP-MINE 23 · CHANNELED-BEAM 9 · AURA 8 · MINION-PET 7. OK.
- All 86 labelled kits present in the active set. OK.

### Stage 0b — franchise rollup [A2]
- **19 distinct game codes** in active set, all in-map. No orphans. OK.
- **franchise_rollup materialized as lookup dict (kit_id -> franchise); 11 franchises**: Diablo 156 · PoE 121 · gd 38 · le 34 · TitanQuest 24 · vs 21 · Torchlight 20 · chronicon 17 · hot 16 · undecember 11 · Hades 11.
- Rollup map (game -> franchise): chronicon->chronicon · d2->Diablo · d3->Diablo · d4->Diablo · di->Diablo · gd->gd · hades1->Hades · hades2->Hades · hot->hot · le->le · poe1->PoE · poe2->PoE · tl1->Torchlight · tl2->Torchlight · tli->Torchlight · tq->TitanQuest · tq2->TitanQuest · undecember->undecember · vs->vs

### Stage 0c — rare-category fusing (Greenacre, n<10)
- The prereg (§1) fuses n<10 levels into a register-parent bucket; the prereg names no per-level parent, so per brief the fused level is **"other-rare"** per coordinate. Map computed ONCE, applied identically across all four families:
  - **delivery** -> other-rare: line(2), other(2)
  - **geometry** -> other-rare: melee_arc(1), fork(1), ground_slam(2), ricochet_bounce(2), teleport(3), beam_channel(3), self_buff(5), aura(8), line(8), ring(9)
  - **function** -> other-rare: fear(3), blind(7)
  - **economy** -> other-rare: spend+cooldown(1), spend+finite(1)
- **Note:** fusing applies to MCA/MDS/Leiden/LCA *input levels* (stability measure). Gate-A labels come from the frozen CSV by kit_id, independent of fused levels — fusing does not alter group membership (e.g. geometry=aura fuses in the MCA input, but the AURA group is defined by kit_id in the label table).

---

## Stage 1 — diagnostics (pre-decomposition)

### 1.1 Per-coordinate normalized entropy (0–1; <0.1 flagged, NOT dropped)

| coord | levels (post-fuse, non-mask) | mask n | entropy |
|---|---|---|---|
| movement | 3 | 6 | 0.867 |
| delivery | 7 | 6 | 0.682 |
| amp | 3 | 2 | 0.728 |
| geometry | 12 | 8 | 0.919 |
| treatment | 2 | 6 | 0.354 |
| function | 8 | 6 | 0.591 |
| defense | 5 | 10 | 0.866 |
| economy | 8 | 42 | 0.813 |
| proxy | 3 | 0 | 0.733 |
| range | 3 | 0 | 0.975 |
| tempo | 3 | 0 | 0.904 |
| commit | 3 | 2 | 0.366 |
| activation | 2 | 6 | 0.697 |
| dependency | 3 | 6 | 0.624 |

### 1.2 Pairwise association — Cramér's V + normalized MI, BH-FDR q=0.05 (78 pairs)

- **56 of 78 pairs FDR-significant** (q=0.05).
- **Near-duplicate candidates (V>0.8 AND FDR-sig):** NONE (retained for v1 per prereg §3.2; demotion is Edition-II).

Top 15 pairs by Cramér's V:

| a | b | Cramér's V | MI(norm) | p | FDR-sig |
|---|---|---|---|---|---|
| economy | activation | 0.616 | 0.322 | 4.80e-33 | Y |
| delivery | geometry | 0.467 | 0.524 | 5.32e-98 | Y |
| delivery | range | 0.401 | 0.202 | 4.17e-28 | Y |
| delivery | commit | 0.350 | 0.246 | 7.62e-21 | Y |
| geometry | commit | 0.346 | 0.225 | 1.45e-17 | Y |
| geometry | proxy | 0.337 | 0.167 | 1.18e-16 | Y |
| geometry | range | 0.292 | 0.110 | 5.48e-12 | Y |
| geometry | dependency | 0.273 | 0.130 | 3.62e-10 | Y |
| treatment | function | 0.268 | 0.138 | 1.10e-06 | Y |
| geometry | tempo | 0.266 | 0.109 | 1.19e-09 | Y |
| movement | defense | 0.261 | 0.082 | 4.40e-12 | Y |
| movement | geometry | 0.251 | 0.096 | 2.27e-08 | Y |
| economy | proxy | 0.242 | 0.084 | 2.32e-08 | Y |
| treatment | defense | 0.239 | 0.130 | 4.75e-06 | Y |
| delivery | tempo | 0.231 | 0.070 | 1.25e-08 | Y |

### 1.3 Category frequency tables post-fuse (the exact input the decomposition sees)

- **movement:** full-move=275, walk=108, rooted=80, unknown=6
- **delivery:** at-target=230, projectile=107, self-origin=85, beam=14, aura-pulse=12, orbit=11, blank=6, other-rare=4
- **amp:** flat=317, spiky=116, var=34, blank=2
- **geometry:** ground_targeted_circle=102, circle=69, totem=50, other-rare=42, multi_projectile=41, single_target=38, melee_strike=37, chain=28, dash_attack=16, whirlwind=15, vortex_pull=12, cone=11, blank=8
- **treatment:** damage=432, control=31, blank=6
- **function:** none=311, hard-stop=44, hex=28, stun=27, knockback=20, expose=12, taunt=11, other-rare=10, unknown=6
- **defense:** tank=215, mitigate=84, evade=66, glass=66, absorb=28, blank=6, post-cutoff-deferred=4
- **economy:** spend=182, cooldown=61, free=48, reserve=47, unknown=42, generator-spender=37, finite=35, self-cost=15, other-rare=2
- **proxy:** solo=332, light=75, heavy=62
- **range:** melee=192, ranged=169, dual=108
- **tempo:** high=221, med=184, low=64
- **commit:** instant=418, channel=33, wind-up=16, blank=2
- **activation:** active=376, triggered=87, unknown=6
- **dependency:** one-shot=359, apply→detonate=60, build→spend=44, unknown=6

---

## Stage 2 — four method families

### 2a — MCA (Greenacre-corrected, MFA block-weighted)
- Indicator matrix: 469 rows × 65 columns (14 MFA blocks; masks passive = zero-inertia rows within block).
- MFA block first-singular-values (weights): movement=13.067, delivery=12.719, amp=13.219, geometry=9.509, treatment=7.758, function=11.118, defense=12.172, economy=11.305, proxy=12.095, range=13.428, tempo=14.185, commit=8.395, activation=11.937, dependency=11.149
- **Parallel analysis** (1000 column-permutation nulls): retain **14 dimensions** (leading dims whose **Greenacre-corrected inertia** exceeds the 95th-pct null, per prereg §4).

| dim | raw eig | Greenacre-adj inertia | Greenacre-adj %% | null-95 (corrected) | retained |
|---|---|---|---|---|---|
| 1 | 0.20730 | 0.17090 | 4.55 | 0.10318 | Y |
| 2 | 0.17870 | 0.14313 | 3.81 | 0.09526 | Y |
| 3 | 0.16477 | 0.12976 | 3.45 | 0.08953 | Y |
| 4 | 0.15081 | 0.11648 | 3.10 | 0.08517 | Y |
| 5 | 0.13488 | 0.10150 | 2.70 | 0.08160 | Y |
| 6 | 0.13315 | 0.09988 | 2.66 | 0.07892 | Y |
| 7 | 0.13091 | 0.09779 | 2.60 | 0.07647 | Y |
| 8 | 0.12051 | 0.08817 | 2.35 | 0.07417 | Y |
| 9 | 0.11668 | 0.08465 | 2.25 | 0.07221 | Y |
| 10 | 0.10741 | 0.07619 | 2.03 | 0.07042 | Y |
| 11 | 0.10540 | 0.07436 | 1.98 | 0.06853 | Y |
| 12 | 0.10018 | 0.06966 | 1.85 | 0.06677 | Y |
| 13 | 0.09877 | 0.06840 | 1.82 | 0.06512 | Y |
| 14 | 0.09507 | 0.06509 | 1.73 | 0.06345 | Y |
| 15 | 0.09089 | 0.06138 | 1.63 | 0.06185 | n |
| 16 | 0.08913 | 0.05982 | 1.59 | 0.05995 | n |
| 17 | 0.08685 | 0.05781 | 1.54 | 0.05826 | n |

- **CATPCA twin** (ordinal spline on tempo+commit only): implemented as MCA with tempo/commit replaced by their register-ordinal integer score (single quantified column each), other coords nominal.
  - CATPCA retained **14 dims**; ARI(CATPCA k-means vs MCA k-means, k=16) = **0.175** (divergence-as-diagnostic per prereg §2).

### 2b — Gower dissimilarity → classical (Torgerson) MDS
- Gower matrix 469×469 (equal coordinate weights; masks = missing per Gower). Classical MDS eigen-scree below.
- **Parallel analysis** (1000 nulls): retain **5 dimensions**.

| dim | eigenvalue | inertia %% | null-95 | retained |
|---|---|---|---|---|
| 1 | 12.79344 | 10.87 | 8.72515 | Y |
| 2 | 10.09513 | 8.58 | 7.95726 | Y |
| 3 | 8.10039 | 6.89 | 7.40977 | Y |
| 4 | 7.29115 | 6.20 | 6.99362 | Y |
| 5 | 7.03326 | 5.98 | 6.55915 | Y |
| 6 | 6.18279 | 5.26 | 6.21514 | n |
| 7 | 5.79914 | 4.93 | 5.85372 | n |
| 8 | 5.25645 | 4.47 | 5.49991 | n |

### 2c — Leiden communities (CPM, kNN k=10)
- Leiden-CPM available (leidenalg + python-igraph). kNN k=10, 100 seeds/resolution, resolution sweep 0.5–2.0 step 0.1. Edge weight = 1−Gower (similarity).

| resolution | median #clusters (per-seed) | consensus #clusters |
|---|---|---|
| 0.5 | 132 | 153 |
| 0.6 | 146 | 185 |
| 0.7 | 170 | 194 |
| 0.8 | 254 | 261 |
| 0.9 | 377 | 378 |
| 1.0 | 469 | 469 |
| 1.1 | 469 | 469 |
| 1.2 | 469 | 469 |
| 1.3 | 469 | 469 |
| 1.4 | 469 | 469 |
| 1.5 | 469 | 469 |
| 1.6 | 469 | 469 |
| 1.7 | 469 | 469 |
| 1.8 | 469 | 469 |
| 1.9 | 469 | 469 |
| 2.0 | 469 | 469 |
- **No ≥3-step non-degenerate plateau;** modal non-degenerate consensus count = 153; consensus taken at resolution 0.5.

### 2d — Latent Class Analysis (BIC-selected, k=2..12)
- stepmix categorical LCA, 50 starts/k. Masks enter as explicit levels (stepmix has no passive category — reported deviation from MCA's passive treatment; noted, not silent).

| k | loglik | #params | BIC | AIC | sABIC | entropy R² |
|---|---|---|---|---|---|---|
| 2 | -6695.2 | 127 | 14171.5 | 13644.4 | 13768.4 | 0.994 |
| 3 | -6459.4 | 191 | 14093.5 | 13300.7 | 13487.3 | 0.985 ⭐ |
| 4 | -6308.9 | 255 | 14186.2 | 13127.8 | 13376.9 | 0.991 |
| 5 | -6183.7 | 319 | 14329.5 | 13005.4 | 13317.0 | 0.960 |
| 6 | -6112.3 | 383 | 14580.3 | 12990.6 | 13364.7 | 0.949 |
| 7 | -6028.9 | 447 | 14807.2 | 12951.8 | 13388.5 | 0.943 |
| 8 | -5956.0 | 511 | 15054.9 | 12933.9 | 13433.1 | 0.961 |
| 9 | -5896.9 | 575 | 15330.4 | 12943.8 | 13505.4 | 0.949 |
| 10 | -5826.6 | 639 | 15583.4 | 12931.2 | 13555.4 | 0.960 |
| 11 | -5761.1 | 703 | 15846.1 | 12928.2 | 13614.9 | 0.961 |
| 12 | -5708.4 | 767 | 16134.3 | 12950.8 | 13700.0 | 0.967 |
- **BIC-selected k = 3** (⭐).

### 2e — cross-family agreement (ARI)
- Common k = 153 for k-means witnesses (non-degenerate Leiden consensus count if available, else LCA-BIC k, else 6). ARI matrix (note: a degenerate Leiden partition scores ~0 vs all others by construction — reported for transparency):

| | MCA-kmeans | MDS-kmeans | Leiden | LCA |
|---|---|---|---|---|
| MCA-kmeans | 1.000 | 0.109 | 0.234 | 0.026 |
| MDS-kmeans | 0.109 | 1.000 | 0.217 | 0.023 |
| Leiden | 0.234 | 0.217 | 1.000 | 0.025 |
| LCA | 0.026 | 0.023 | 0.025 | 1.000 |

---

## Stage 3 — the four gates

### Gate A — group recovery
- **Gate statistic:** derived clustering = k-means(k=6) on the retained MCA basis (the candidate map per prereg §4). ARI computed on the labelled subset (n=86).
- **ARI (MCA-basis k-means vs frozen labels) = 0.668** — threshold ≥ 0.6 → **PASS**.
- Secondary witness ARIs (reported, non-gating): Leiden(consensus)=0.279 · LCA(BIC-k=3)=0.349.

| group | n | silhouette (retained MCA space) | ≥0.2 |
|---|---|---|---|
| WHIRLWIND | 15 | 0.551 | Y |
| TOTEM-SENTRY | 24 | 0.513 | Y |
| TRAP-MINE | 23 | 0.283 | Y |
| CHANNELED-BEAM | 9 | 0.367 | Y |
| AURA | 8 | 0.581 | Y |
| MINION-PET | 7 | 0.461 | Y |
- Silhouette ≥0.2 for **6 of 6** groups. Large-group failures: NONE. Sub-threshold groups: NONE.
- **[A3] silhouette rule** (≥5/6 AND all four large clear AND permitted-failure∈{AURA,MINION-PET}): **PASS**.

**GATE A: PASS** (ARI 0.668; silhouette-rule PASS).

### Gate B — negative geography
- Projected 37 negatives (supplementary, zero mass). intrinsic-red pooled k=5; extrinsic-tuning k=6.
- **POOLED intrinsic-red (k=5):** mean pairwise dist = 2.4404; null mean = 1.8549 (10000 draws from active). p(tight, lower-tail) = 0.9638; p(dispersed, upper-tail) = 0.0363.
- Threshold p<0.05 (clustered tighter than random). **GATE B: FAIL** (p_lower=0.9638).
- **[secondary, NON-gating] extrinsic-tuning (k=6):** mean pairwise = 2.0944; null mean = 1.8470; p_lower = 0.8139; p_upper = 0.1862.
- Per-law breakdown DESCRIPTIVE ONLY (all underpowered; not gating):
  - <NULL>: n=12 projectable
  - extrinsic-tuning: n=6 projectable
  - intrinsic-red: n=5 projectable
  - extrinsic-itemization: n=5 projectable
  - extrinsic-split-scaling: n=3 projectable
  - extrinsic-no-lever: n=3 projectable
  - extrinsic-content-mix: n=2 projectable
  - system-evidence: n=1 projectable

### Gate C — franchise mixing
- PERMANOVA on `franchise_rollup` (retained MCA distances, 999 perms): **R² = 0.0757**, pseudo-F = 3.750, p = 0.001.
- **[A4] PERMDISP companion:** F = 1.767, p = 0.066.
- PERMDISP non-significant (p≥0.05) → R² is pass-interpretable. Threshold R²≤0.15 → **GATE C: PASS**.

**GATE C: PASS** (R²=0.0757, threshold ≤0.15; PERMDISP p=0.066).

### Gate D — stability
- **Plane diameter [A5]** = max pairwise Euclidean distance among 469 active points in the 14-dim retained space = **4.4145**. All displacement % use this denominator.
- **(i) Bootstrap** 1000× at 90% subsample, Procrustes-aligned: median per-kit displacement = 0.1591 = **3.60% of plane diameter** (threshold ≤10%) → **PASS**.
- **(ii) Leave-one-franchise-out** (Procrustes congruence vs full fit on retained kits):

| held-out franchise | congruence | ≥0.85 |
|---|---|---|
| Diablo | 0.970 | Y |
| Hades | 0.995 | Y |
| PoE | 0.968 | Y |
| TitanQuest | 0.997 | Y |
| Torchlight | 0.995 | Y |
| chronicon | 0.993 | Y |
| gd | 0.992 | Y |
| hot | 0.996 | Y |
| le | 0.984 | Y |
| undecember | 0.999 | Y |
| vs | 0.969 | Y |
- **(iii) inverse-√franchise-size reweighted refit** vs unweighted: Procrustes congruence = 0.985 (threshold ≥0.85) → **PASS**.

**GATE D: PASS** (bootstrap PASS; LOFO PASS; reweight PASS).

---

## §amendments
- NONE. All pinned parameters executed as specified.

- Not all gates PASS (A=True B=False C=True D=True) → basis draft NOT emitted (per decision rule).

---

## Gate summary

| gate | verdict | headline |
|---|---|---|
| A group-recovery | PASS | ARI=0.668 |
| B negative-geography | FAIL | intrinsic-red k=5 |
| C franchise-mixing | PASS | R²=0.0757 (PERMDISP p=0.066) |
| D stability | PASS | boot=3.60% diam |

**ALL FOUR PASS: NO**
