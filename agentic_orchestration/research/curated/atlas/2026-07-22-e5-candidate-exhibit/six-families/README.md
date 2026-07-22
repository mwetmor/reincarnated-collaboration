# E5 CANDIDATE — SIX NAMED BUILD-FAMILIES — numbers only

**Date:** 2026-07-22 · **Executor:** elrond · **Purpose:** Matt's PRIMARY family exhibit — see the six build-families we ALREADY KNOW OF (the gateA-ratified island families) in both cameras, colored by family. NO element, NO court, NO new names.

> **E5 CANDIDATE — NOT SERVED (§8-C: E4 remains truth)**

> **NO SILENT CONFLATION.** The archipelago-mock 'core' census conflated gateA-RATIFIED members with tau-PROPAGATED proposals (the 44 proposals ran ~1/3 precision). This exhibit separates them: RATIFIED render solid (marker + solid hull); PROPAGATED render faint/hollow + dashed hull-extension. Treat propagated as hypotheses, not membership.

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

## Membership source (ratified lists RECOVERED — yes)

- **RATIFIED source:** corpus.db atlas_gateA_labels_2026_07_14 (86 rows) — verified byte-identical to archipelago-mock gateA_seed=True set (0 disagreements across all six families).
- **PROPAGATED source:** archipelago-mock tau-cores (`family` set) MINUS ratified.
- **Recovered counts** (ratified + propagated) match the archipelago-mock report's stated ratified truth EXACTLY: WHIRLWIND 15+0 · CHANNELED-BEAM 9+0 · MINION-PET 7+0 · AURA 8+2 · TOTEM-SENTRY 24+22 · TRAP-MINE 23+20. Ratified total **86**, propagated total **44**.

## Placement census (into the CURRENT 574 corpus)

> **Corpus-drift note:** the archipelago was cut on the Edition-I **469-kit** corpus; current is **574**. Members are matched by kit_id into the 574 real-kit `kit_master` view; a member present in E1-469 but absent from the 574 view is UNPLACEABLE and reported (not fabricated).

| family | ratified placed/total | rat both-cam | propagated placed/total | prop both-cam | annex+system members |
|---|---|---|---|---|---|
| **WHIRLWIND** | 15/15 | 15 | 0/0 | 0 | 8 |
| **CHANNELED-BEAM** | 9/9 | 9 | 0/0 | 0 | 3 |
| **MINION-PET** | 7/7 | 7 | 0/0 | 0 | 7 |
| **AURA** | 8/8 | 8 | 2/2 | 2 | 4 |
| **TOTEM-SENTRY** | 24/24 | 24 | 22/22 | 22 | 14 |
| **TRAP-MINE** | 22/23 | 22 | 20/20 | 20 | 16 |
| **TOTAL** | **85/86** | — | **44/44** | — | **52** |

- **Unplaceable (corpus-drift casualties, 1):** `chr-crown-proc-engine` (TRAP-MINE ratified). `chr-crown-proc-engine` is corpus_class=`system` and NOT in the 574 real-kit `kit_master` view (system-records are excluded from the real-kit universe), so TRAP-MINE ratified places 22/23. All other 128 members place in BOTH cameras.

## Per-family E5 dispersion + centroid shift (SAME metric as the lassos exhibit README — comparability)

`shift` = centroid displacement E4→E5-aligned (plane units; frac of plane span = 3.6751). `spread` = RMS radius about centroid on each plane; `spread_ratio` = spread(E5) ÷ spread(E4) (>1 = the family SPREADS/splinters under the candidate angle; <1 = TIGHTENS). Computed over **RATIFIED-CORE** members placed in BOTH cameras (ratified-anchored; propagated excluded from the metric).

| family | n (ratified core) | shift | shift/span | spread E4 | spread E5 | spread_ratio |
|---|---|---|---|---|---|---|
| **AURA** | 8 | 0.1956 | 0.053 | 0.2410 | 0.3278 | 1.360 |
| **TOTEM-SENTRY** | 24 | 0.1883 | 0.051 | 0.2694 | 0.3462 | 1.285 |
| **WHIRLWIND** | 15 | 0.6248 | 0.170 | 0.3768 | 0.4451 | 1.181 |
| **TRAP-MINE** | 22 | 0.5781 | 0.157 | 0.3786 | 0.4167 | 1.101 |
| **MINION-PET** | 7 | 0.9006 | 0.245 | 0.3415 | 0.3021 | 0.884 |
| **CHANNELED-BEAM** | 9 | 0.3280 | 0.089 | 0.2806 | 0.2418 | 0.861 |

- **Migrate (centroid shift ≥ 20% of plane span):** MINION-PET → 0.25 span
- **Spread / splinter (E5 RMS radius ≥ 1.30× E4):** AURA → ×1.36
- **Tighten (E5 RMS radius ≤ 0.77× E4):** none

## Standing caveats

1. **Conflation (headline):** propagated ≠ ratified. The 44 tau-propagated proposals ran ~1/3 precision (global-τ umbrella defect over multi-cluster families — TOTEM-SENTRY and TRAP-MINE are the archipelagic families that absorbed nearly all proposals: +22 and +20). Solid hull = trust; dashed hull = candidate.
2. **Annex/system members carry NO six-block gb_* data (design-NULL).** **52 of the 129 placed members are annex/system-class** and therefore place from the SHARED pre-v2.0 register coords + element_primary ONLY (their gb_* geometry-band blocks are passive). MINION-PET is **entirely annex-class (7/7)** — none of its members carry six-block data, so its placement is register-driven, not geometry-driven. WHIRLWIND ratified is 8 annex / 7 record; AURA propagated includes 1 system. This is EXPECTED (annex/system never got the v2.0 side-car) and is why annex/system family placements are lower-resolution than record-class ones.
3. **Rare-bucket leverage (carried from exhibit v1):** the fused rare level `gb_width:other-rare` tops BOTH candidate dims (dim1 +1.86, dim2 +2.48). A low-population fused level dominating the leading axes is part of why the refit is not servable-grade (with the 0.7836 < 0.85 congruence, §8-C keeps E4 as truth). The candidate camera here is a diagnostic, not a proposed replacement.
4. **E5 supplementary projection is V-2 machinery:** the 265-kit record fit DERIVES the axes (byte-identical to the reproduction gate); every family member is placed as a supplementary point (annex/system + non-fit record) or read from the fit basis (fit-member record). Supplementary rows NEVER bend the axes.

## Files

- `six-families-side-by-side.png` — 381626 bytes
- `six-families-delta-arrows.png` — 466736 bytes
- `six-families-membership.csv` — 12617 bytes

## Exact reproduction command

```
cd /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts
python3 atlas_e5_sixfam_2026_07_22.py
```

Deterministic: SEED=20260722, all randomness pinned. corpus.db opened read-only (uri mode=ro). Imports `atlas_e5_exhibit_2026_07_22`, `atlas_e5_exhibit_574_2026_07_22`, `atlas_e5_lassos_2026_07_22`, `atlas_legb_refit_2026_07_22` verbatim (no recompute/placement/geometry math changed).

## Constraint attestation

- READ-ONLY on corpus.db and every store — zero mutations, zero serving artifacts.
- Reproduction gate (8/8) gates the renders: any mismatch → HALT, no renders.
- Membership recovery HALTS if corpus.db ratified disagrees with the mock gateA_seed set (it does not: 0 disagreements). Ratified vs propagated never silently merged.
- Only the SIX ratified family names are used (WHIRLWIND · CHANNELED-BEAM · MINION-PET · AURA · TOTEM-SENTRY · TRAP-MINE). Nothing else named. No court/element anywhere on the plots.
