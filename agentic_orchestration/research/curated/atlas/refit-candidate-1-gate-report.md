# Atlas REFIT CANDIDATE 1 — Gate Report (comparison experiment; NOT an Edition)

**Date:** 2026-07-16 · **Executor:** elrond · **Script:** `agentic_orchestration/research/scripts/atlas_refit_candidate_2026_07_16.py`
**Fork of:** `atlas_derivation_2026_07_14.py` (Edition-I pipeline) · **Prereg (unchanged method):** `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` (v1.1, PINNED)
**Artifact:** Refit-Candidate-1 — emitted ALONGSIDE Edition III (served truth; Matt comparison pending). Unratified comparison artifact.
**Seed:** 20260714 (unchanged; all randomness pinned). **NUMBERS ONLY — interpretation is gandalf's.**

---

## Stage 0 — verification

- **Snapshot marker:** `atlas-prereg-2026-07-14` PRESENT in `corpus_schema_meta`. OK.
- **Active set N = 628** (combat-kit ∧ cell_key NOT NULL ∧ negative=0). Re-derived from predicate (fetch == COUNT == 628). OK (== recon-expected 628; Edition-I fit was 469, +159).

### Stage 0.PA — PULL pre-assert (function=pull earns a fit column)
- **function=pull active count = 10** (per-field parse, cell_key pos 5) >= FUSE_MIN=10 → pull survives Greenacre fusing and earns its own indicator column (its fit2reg image becomes real; un-maskable in the ghost field). ZERO MARGIN (== FUSE_MIN).
- pull kits (10): d3-wizard-black-hole, d3-zbarb, d4-spiritborn-vortex, di-cyclone-monk-pvp, di-cyclone-strike-monk-base, la-destroyer-gravity-force, la-destroyer-gravity-impact, la-destroyer-gravity-training, la-destroyer-rage-hammer, la-destroyer-vortex-gravity

### Stage 0.ME — MELEE per-field parse (delivery vs range; LIKE-collision diagnostic)
- **delivery=melee active count = 31** (per-field, pos 1) — >= FUSE_MIN=10 → EARNS a fit column organically. Naive `LIKE '%|melee|%'` = 271 (over-counts via range=melee=271 collision — NOT used).
- **FLAG:** delivery=melee earns a fit column → the MELEE ghost-image collapse (delivery=melee had NO meso ghost image in Edition-I/II/III, masked-like) may PARTIALLY CLOSE in the refit. Reported, not engineered — the ghost-field module un-masks MELEE and reports the delta.
- **Negatives:** 38 total `negative=1` in canon_corpus; 37 are combat-kit with cell_key (projectable supplementary set for Gate B); 1 is a system-record (`vs-golden-egg-scaling`, per A.5 note — outside combat denominator, not projectable). Reconciliation: charter's "38 graveyard" = corpus count; fit-relevant projectable-negative count = 37.

- **Survivor-key SHA256** (628 active rows, ordered by kit_id): `922f3cc58c4ba401c9b4e07a4835d76879a6c50eb5c087df3b263156e012f9d8`
- **Structural:** all 628 active rows are exactly 14 pipe-delimited positions. OK.

### Stage 0a — Gate-A label table
- Loaded **86 rows** byte-verbatim into `atlas_gateA_labels_refit_candidate_1` (refit-suffixed table — Edition-I's `atlas_gateA_labels_2026_07_14` left untouched). Group counts: WHIRLWIND 15 · TOTEM-SENTRY 24 · TRAP-MINE 23 · CHANNELED-BEAM 9 · AURA 8 · MINION-PET 7. OK.
- All 86 labelled kits present in the active set (628). OK.

### Stage 0b — franchise rollup [A2]
- **21 distinct game codes** in active set, all in-map. No orphans. OK.
- **franchise_rollup materialized as lookup dict (kit_id -> franchise); 13 franchises** (Edition-I 11 + LostArk + mcd): Diablo 159 · PoE 121 · mcd 94 · LostArk 62 · gd 38 · le 34 · TitanQuest 24 · vs 21 · Torchlight 20 · chronicon 17 · hot 16 · undecember 11 · Hades 11.
- Rollup map (game -> franchise): chronicon->chronicon · d2->Diablo · d3->Diablo · d4->Diablo · di->Diablo · gd->gd · hades1->Hades · hades2->Hades · hot->hot · la->LostArk · le->le · mcd->mcd · poe1->PoE · poe2->PoE · tl1->Torchlight · tl2->Torchlight · tli->Torchlight · tq->TitanQuest · tq2->TitanQuest · undecember->undecember · vs->vs

### Stage 0c — rare-category fusing (Greenacre, n<10)
- The prereg (§1) fuses n<10 levels into a register-parent bucket; the prereg names no per-level parent, so per brief the fused level is **"other-rare"** per coordinate. Map computed ONCE, applied identically across all four families:
  - **delivery** -> other-rare: line(2), other(2)
  - **geometry** -> other-rare: melee_arc(1), fork(1), ground_slam(2), ricochet_bounce(2), teleport(3), beam_channel(3), self_buff(5), ring(9), line(9)
  - **function** -> other-rare: fear(7), blind(7)
  - **economy** -> other-rare: spend+cooldown(1), spend+finite(1)
- **Note:** fusing applies to MCA/MDS/Leiden/LCA *input levels* (stability measure). Gate-A labels come from the frozen CSV by kit_id, independent of fused levels — fusing does not alter group membership (e.g. geometry=aura fuses in the MCA input, but the AURA group is defined by kit_id in the label table).
- **POST-FUSE pull survival:** function=pull is PRESENT in the fused input (earns a fit column). delivery=melee EARNS a fit column.

---

## Stage 1 — diagnostics (pre-decomposition)

### 1.1 Per-coordinate normalized entropy (0–1; <0.1 flagged, NOT dropped)

| coord | levels (post-fuse, non-mask) | mask n | entropy |
|---|---|---|---|
| movement | 3 | 101 | 0.928 |
| delivery | 8 | 6 | 0.642 |
| amp | 3 | 26 | 0.710 |
| geometry | 13 | 32 | 0.921 |
| treatment | 2 | 6 | 0.332 |
| function | 9 | 6 | 0.591 |
| defense | 5 | 100 | 0.897 |
| economy | 8 | 42 | 0.844 |
| proxy | 3 | 0 | 0.653 |
| range | 4 | 0 | 0.815 |
| tempo | 3 | 1 | 0.933 |
| commit | 3 | 26 | 0.542 |
| activation | 2 | 6 | 0.666 |
| dependency | 3 | 6 | 0.694 |

### 1.2 Pairwise association — Cramér's V + normalized MI, BH-FDR q=0.05 (78 pairs)

- **74 of 78 pairs FDR-significant** (q=0.05).
- **Near-duplicate candidates (V>0.8 AND FDR-sig):** NONE (retained for v1 per prereg §3.2; demotion is Edition-II).

Top 15 pairs by Cramér's V:

| a | b | Cramér's V | MI(norm) | p | FDR-sig |
|---|---|---|---|---|---|
| delivery | geometry | 0.532 | 0.509 | 3.00e-205 | Y |
| economy | activation | 0.468 | 0.214 | 5.95e-26 | Y |
| economy | dependency | 0.452 | 0.232 | 7.74e-46 | Y |
| treatment | function | 0.416 | 0.350 | 2.63e-21 | Y |
| geometry | dependency | 0.364 | 0.165 | 5.74e-26 | Y |
| geometry | commit | 0.363 | 0.174 | 7.00e-26 | Y |
| geometry | proxy | 0.358 | 0.192 | 3.68e-25 | Y |
| movement | commit | 0.336 | 0.179 | 1.71e-25 | Y |
| delivery | commit | 0.331 | 0.165 | 8.62e-24 | Y |
| movement | geometry | 0.331 | 0.135 | 6.78e-18 | Y |
| delivery | range | 0.330 | 0.199 | 7.76e-36 | Y |
| geometry | range | 0.324 | 0.174 | 9.89e-29 | Y |
| movement | defense | 0.291 | 0.093 | 3.26e-17 | Y |
| economy | commit | 0.286 | 0.153 | 3.73e-16 | Y |
| movement | function | 0.282 | 0.097 | 6.36e-14 | Y |

### 1.3 Category frequency tables post-fuse (the exact input the decomposition sees)

- **movement:** full-move=275, rooted=143, walk=109, blank=95, unknown=6
- **delivery:** at-target=350, projectile=111, self-origin=85, melee=31, aura-pulse=16, beam=14, orbit=11, blank=6, other-rare=4
- **amp:** flat=407, spiky=161, var=34, blank=26
- **geometry:** ground_targeted_circle=109, melee_strike=88, circle=69, single_target=65, multi_projectile=52, totem=50, chain=45, other-rare=35, blank=32, cone=23, vortex_pull=17, dash_attack=16, whirlwind=15, aura=12
- **treatment:** damage=584, control=38, blank=6
- **function:** none=407, knockback=54, hard-stop=50, stun=34, hex=28, other-rare=14, expose=14, taunt=11, pull=10, unknown=6
- **defense:** tank=224, evade=105, blank=96, mitigate=89, glass=74, absorb=36, post-cutoff-deferred=4
- **economy:** spend=183, free=118, cooldown=93, generator-spender=93, reserve=47, unknown=42, finite=35, self-cost=15, other-rare=2
- **proxy:** solo=476, light=90, heavy=62
- **range:** melee=271, ranged=231, dual=110, mid=16
- **tempo:** high=264, med=261, low=102, blank=1
- **commit:** instant=493, wind-up=65, channel=44, blank=26
- **activation:** active=514, triggered=108, unknown=6
- **dependency:** one-shot=454, build→spend=104, apply→detonate=64, unknown=6

---

## Stage 2 — four method families

### 2a — MCA (Greenacre-corrected, MFA block-weighted)
- Indicator matrix: 628 rows × 69 columns (14 MFA blocks; masks passive = zero-inertia rows within block).
- MFA block first-singular-values (weights): movement=14.320, delivery=14.241, amp=15.396, geometry=10.085, treatment=8.587, function=12.960, defense=13.095, economy=12.529, proxy=13.273, range=15.814, tempo=16.202, commit=12.064, activation=13.408, dependency=13.827
- **Parallel analysis** (1000 column-permutation nulls): retain **17 dimensions** (leading dims whose **Greenacre-corrected inertia** exceeds the 95th-pct null, per prereg §4).

| dim | raw eig | Greenacre-adj inertia | Greenacre-adj %% | null-95 (corrected) | retained |
|---|---|---|---|---|---|
| 1 | 0.25678 | 0.21976 | 5.15 | 0.10474 | Y |
| 2 | 0.19595 | 0.15983 | 3.75 | 0.09337 | Y |
| 3 | 0.19369 | 0.15764 | 3.70 | 0.08914 | Y |
| 4 | 0.17622 | 0.14074 | 3.30 | 0.08635 | Y |
| 5 | 0.16907 | 0.13387 | 3.14 | 0.08404 | Y |
| 6 | 0.15355 | 0.11907 | 2.79 | 0.08205 | Y |
| 7 | 0.14070 | 0.10695 | 2.51 | 0.08021 | Y |
| 8 | 0.13271 | 0.09947 | 2.33 | 0.07862 | Y |
| 9 | 0.12337 | 0.09081 | 2.13 | 0.07695 | Y |
| 10 | 0.12233 | 0.08985 | 2.11 | 0.07537 | Y |
| 11 | 0.11480 | 0.08292 | 1.94 | 0.07385 | Y |
| 12 | 0.11303 | 0.08131 | 1.91 | 0.07230 | Y |
| 13 | 0.11023 | 0.07875 | 1.85 | 0.07078 | Y |
| 14 | 0.10453 | 0.07358 | 1.73 | 0.06874 | Y |
| 15 | 0.10100 | 0.07040 | 1.65 | 0.06662 | Y |
| 16 | 0.09761 | 0.06736 | 1.58 | 0.06465 | Y |
| 17 | 0.09380 | 0.06396 | 1.50 | 0.06265 | Y |
| 18 | 0.08877 | 0.05951 | 1.40 | 0.06111 | n |
| 19 | 0.08509 | 0.05628 | 1.32 | 0.05946 | n |
| 20 | 0.08214 | 0.05369 | 1.26 | 0.05792 | n |

- **CATPCA twin** (ordinal spline on tempo+commit only): implemented as MCA with tempo/commit replaced by their register-ordinal integer score (single quantified column each), other coords nominal.
  - CATPCA retained **17 dims**; ARI(CATPCA k-means vs MCA k-means, k=19) = **0.179** (divergence-as-diagnostic per prereg §2).

### 2b — Gower dissimilarity → classical (Torgerson) MDS
- Gower matrix 628×628 (equal coordinate weights; masks = missing per Gower). Classical MDS eigen-scree below.
- **Parallel analysis** (1000 nulls): retain **6 dimensions**.

| dim | eigenvalue | inertia %% | null-95 | retained |
|---|---|---|---|---|
| 1 | 18.04198 | 10.91 | 11.99054 | Y |
| 2 | 14.00875 | 8.47 | 11.05053 | Y |
| 3 | 12.51251 | 7.56 | 10.40369 | Y |
| 4 | 10.63760 | 6.43 | 9.48143 | Y |
| 5 | 9.53457 | 5.76 | 8.88617 | Y |
| 6 | 8.80903 | 5.32 | 8.40337 | Y |
| 7 | 7.86388 | 4.75 | 7.98218 | n |
| 8 | 7.14308 | 4.32 | 7.57872 | n |
| 9 | 6.31707 | 3.82 | 7.11923 | n |

### 2c — Leiden communities (CPM, kNN k=10)
- Leiden-CPM available (leidenalg + python-igraph). kNN k=10, 100 seeds/resolution, resolution sweep 0.5–2.0 step 0.1. Edge weight = 1−Gower (similarity).

| resolution | median #clusters (per-seed) | consensus #clusters |
|---|---|---|
| 0.5 | 168 | 204 |
| 0.6 | 184 | 228 |
| 0.7 | 209 | 250 |
| 0.8 | 299 | 308 |
| 0.9 | 444 | 447 |
| 1.0 | 628 | 628 |
| 1.1 | 628 | 628 |
| 1.2 | 628 | 628 |
| 1.3 | 628 | 628 |
| 1.4 | 628 | 628 |
| 1.5 | 628 | 628 |
| 1.6 | 628 | 628 |
| 1.7 | 628 | 628 |
| 1.8 | 628 | 628 |
| 1.9 | 628 | 628 |
| 2.0 | 628 | 628 |
- **No ≥3-step non-degenerate plateau;** modal non-degenerate consensus count = 204; consensus taken at resolution 0.5.

### 2d — Latent Class Analysis (BIC-selected, k=2..12)
- stepmix categorical LCA, 50 starts/k. Masks enter as explicit levels (stepmix has no passive category — reported deviation from MCA's passive treatment; noted, not silent).

| k | loglik | #params | BIC | AIC | sABIC | entropy R² |
|---|---|---|---|---|---|---|
| 2 | -9397.6 | 139 | 19690.8 | 19073.3 | 19249.5 | 1.000 |
| 3 | -8939.7 | 209 | 19226.0 | 18297.5 | 18562.4 | 0.992 |
| 4 | -8605.4 | 279 | 19008.2 | 17768.7 | 18122.4 | 0.994 |
| 5 | -8336.0 | 349 | 18920.4 | 17370.0 | 17812.4 | 0.994 ⭐ |
| 6 | -8124.1 | 419 | 18947.7 | 17086.2 | 17617.4 | 0.991 |
| 7 | -7983.2 | 489 | 19116.8 | 16944.4 | 17564.3 | 0.994 |
| 8 | -7871.8 | 559 | 19344.9 | 16861.5 | 17570.1 | 0.982 |
| 9 | -7803.5 | 629 | 19659.4 | 16865.0 | 17662.4 | 0.964 |
| 10 | -7703.4 | 699 | 19910.1 | 16804.8 | 17690.9 | 0.969 |
| 11 | -7610.7 | 769 | 20175.7 | 16759.4 | 17734.2 | 0.975 |
| 12 | -7530.6 | 839 | 20466.5 | 16739.3 | 17802.8 | 0.976 |
- **BIC-selected k = 5** (⭐).

### 2e — cross-family agreement (ARI)
- Common k = 204 for k-means witnesses (non-degenerate Leiden consensus count if available, else LCA-BIC k, else 6). ARI matrix (note: a degenerate Leiden partition scores ~0 vs all others by construction — reported for transparency):

| | MCA-kmeans | MDS-kmeans | Leiden | LCA |
|---|---|---|---|---|
| MCA-kmeans | 1.000 | 0.182 | 0.345 | 0.030 |
| MDS-kmeans | 0.182 | 1.000 | 0.325 | 0.027 |
| Leiden | 0.345 | 0.325 | 1.000 | 0.031 |
| LCA | 0.030 | 0.027 | 0.031 | 1.000 |

---

## Stage 3 — the four gates

### Gate A — group recovery
- **Gate statistic:** derived clustering = k-means(k=6) on the retained MCA basis (the candidate map per prereg §4). ARI computed on the labelled subset (n=86).
- **ARI (MCA-basis k-means vs frozen labels) = 0.451** — threshold ≥ 0.6 → **FAIL**.
- Secondary witness ARIs (reported, non-gating): Leiden(consensus)=0.235 · LCA(BIC-k=5)=0.248.

| group | n | silhouette (retained MCA space) | ≥0.2 |
|---|---|---|---|
| WHIRLWIND | 15 | 0.609 | Y |
| TOTEM-SENTRY | 24 | 0.531 | Y |
| TRAP-MINE | 23 | 0.288 | Y |
| CHANNELED-BEAM | 9 | 0.397 | Y |
| AURA | 8 | 0.716 | Y |
| MINION-PET | 7 | 0.499 | Y |
- Silhouette ≥0.2 for **6 of 6** groups. Large-group failures: NONE. Sub-threshold groups: NONE.
- **[A3] silhouette rule** (≥5/6 AND all four large clear AND permitted-failure∈{AURA,MINION-PET}): **PASS**.

**GATE A: FAIL** (ARI 0.451; silhouette-rule PASS).

- **[R2] Supplementary graveyard projection:** 37 projectable negatives fetched (combat-kit ∧ cell_key ∧ negative=1) == recon-expected 37; 37 projected into the NEW 17-dim retained space via the same CA supplementary transition formula (zero mass; corpses cannot bend the refit axes).

### Gate B — negative geography
- Projected 37 negatives (supplementary, zero mass). intrinsic-red pooled k=12; extrinsic-tuning k=7.
- **POOLED intrinsic-red (k=12):** mean pairwise dist = 1.9261; null mean = 2.1072 (10000 draws from active). p(tight, lower-tail) = 0.2339; p(dispersed, upper-tail) = 0.7662.
- Threshold p<0.05 (clustered tighter than random). **GATE B: FAIL** (p_lower=0.2339).
- **[secondary, NON-gating] extrinsic-tuning (k=7):** mean pairwise = 2.1173; null mean = 2.1073; p_lower = 0.5368; p_upper = 0.4633.
- Per-law breakdown DESCRIPTIVE ONLY (all underpowered; not gating):
  - intrinsic-red: n=12 projectable
  - extrinsic-tuning: n=7 projectable
  - extrinsic-itemization: n=7 projectable
  - extrinsic-no-lever: n=4 projectable
  - extrinsic-split-scaling: n=3 projectable
  - extrinsic-content-mix: n=3 projectable
  - system-evidence: n=1 projectable

### Gate C — franchise mixing
- PERMANOVA on `franchise_rollup` (retained MCA distances, 999 perms): **R² = 0.1683**, pseudo-F = 10.368, p = 0.001.
- **[A4] PERMDISP companion:** F = 2.607, p = 0.004.
- **PERMDISP SIGNIFICANT (p<0.05)** → R² NOT self-interpreting. Reporting both numbers; **GATE C: gandalf rules** (R²=0.1683 vs ≤0.15; dispersion heterogeneity present).

**GATE C: gandalf rules** (R²=0.1683, threshold ≤0.15; PERMDISP p=0.004).

### Gate D — stability
- **Plane diameter [A5]** = max pairwise Euclidean distance among 628 active points in the 17-dim retained space = **5.2946**. All displacement % use this denominator.
- **(i) Bootstrap** 1000× at 90% subsample, Procrustes-aligned: median per-kit displacement = 0.1194 = **2.26% of plane diameter** (threshold ≤10%) → **PASS**.
- **(ii) Leave-one-franchise-out** (Procrustes congruence vs full fit on retained kits):

| held-out franchise | congruence | ≥0.85 |
|---|---|---|
| Diablo | 0.982 | Y |
| Hades | 0.998 | Y |
| LostArk | 0.952 | Y |
| PoE | 0.983 | Y |
| TitanQuest | 0.999 | Y |
| Torchlight | 0.997 | Y |
| chronicon | 0.999 | Y |
| gd | 0.997 | Y |
| hot | 0.999 | Y |
| le | 0.987 | Y |
| mcd | 0.968 | Y |
| undecember | 0.999 | Y |
| vs | 0.992 | Y |
- **(iii) inverse-√franchise-size reweighted refit** vs unweighted: Procrustes congruence = 0.990 (threshold ≥0.85) → **PASS**.

**GATE D: PASS** (bootstrap PASS; LOFO PASS; reweight PASS).

---

## §amendments
- NONE. All pinned parameters executed as specified.

- **Basis draft ALWAYS emitted** (comparison artifact; gates=evidence) → `refit-candidate-1-basis-draft.json` (frozen=false; gates A=False B=False C=None D=True; all_pass=False).
- Fit snapshot: `refit-candidate-1-fit-cellkeys.csv` (628 active cell_keys — refit ghost-field rebuild input).

---

## Gate summary — EVIDENCE for Matt's adoption decision (NOT emission blockers)

| gate | verdict | headline |
|---|---|---|
| A group-recovery | FAIL | ARI=0.451 |
| B negative-geography | FAIL | intrinsic-red k=12 |
| C franchise-mixing | gandalf-rules/uncomputed | R²=0.1683 (PERMDISP p=0.004) |
| D stability | PASS | boot=2.26% diam |

**ALL FOUR PASS: NO** — Refit Candidate 1 emits regardless (comparison artifact; gates are evidence). Any FAIL is reported in red ink for the adoption decision.

**Pull/melee feature-column status:** function=pull active=10 (earned column=True); delivery=melee active=31 (earned column=True).
