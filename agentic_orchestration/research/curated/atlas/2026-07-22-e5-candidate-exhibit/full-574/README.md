# E5 CANDIDATE EXHIBIT — FULL 574 corpus — numbers only

**Date:** 2026-07-22 · **Executor:** elrond · **Purpose:** R1 camera-fork ruling — Matt sees the FULL 574 real-kit corpus in BOTH cameras before ruling. **E5 NOT served (§8-C: E4 remains truth).**

Numbers only. NO island/cluster/build-family naming (Matt-gated). Color/annotate only by ratified vocabulary: court (k=5), corpus_class, game.

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

## Coverage table (of the 574 real kits = kit_master view)

kit_master = 267 record + 299 annex + 8 in-view system. E4-placed = stored `atlas_coords` OR frozen-E1 CA projection from the 14-field cell_key. E5-placed = 265 fit-basis (axis-deriving) + supplementary CA projection.

| corpus_class | total | E4-placed | E5-placed | both | neither |
|---|---|---|---|---|---|
| record | 267 | 265 | 265 | 265 | 2 |
| annex | 299 | 292 | 292 | 292 | 7 |
| system | 8 | 4 | 4 | 4 | 4 |
| **TOTAL** | **574** | **561** | **561** | **561** | **13** |

- E4-placed breakdown: **468 stored** atlas_coords + **93 projected** (frozen-E1 CA supplementary from cell_key).
- **Neither** = no stored coords AND no 14-field cell_key → unplaceable in either camera. Record's 2 = the pre-registered unprojectable degenerate kits (`d2-teleport-sorc`, `poe1-blood-magic-kit`; no cell_key at all).
- Delta arrows are drawn ONLY for the **561 kits placed in BOTH** cameras (record full-strength; annex/system thin/faint).

## Top-10 movers (kits in BOTH cameras, by E4→E5-aligned displacement)

| rank | kit_id | corpus_class | court | Δ (plane units) | E4 (x,y) | E5-aligned (x,y) |
|---|---|---|---|---|---|---|
| 1 | poe2-perfect-strike-01 | record | fire | 2.2878 | (-0.818, 0.316) | (0.069, -1.793) |
| 2 | d2-impale-zon | record | physical | 2.1385 | (-1.215, 0.148) | (-0.569, -1.891) |
| 3 | d2-zealot | record | physical | 1.7963 | (-0.201, 0.210) | (-0.123, -1.585) |
| 4 | d2-maul-bear | record | physical | 1.6887 | (-0.454, 0.151) | (-0.271, -1.528) |
| 5 | poe2-titan-hotg | record | physical | 1.6414 | (-0.757, 0.123) | (-0.485, -1.495) |
| 6 | le-tempest-strike | record | lightning | 1.6232 | (-0.007, 0.249) | (-0.054, -1.374) |
| 7 | d2-kicksin | record | physical | 1.5927 | (-0.097, 0.289) | (-0.178, -1.301) |
| 8 | poe1-wild-strike | record | fire | 1.5601 | (0.019, 0.175) | (-0.130, -1.378) |
| 9 | d2-sacrifice | record | physical | 1.5482 | (-0.418, -0.227) | (-0.300, -1.771) |
| 10 | d2-frenzy-barb | record | physical | 1.4830 | (-0.070, 0.077) | (-0.128, -1.405) |

- Displacement over BOTH-placed (n=561): min=0.0212 median=0.4657 max=2.2878 mean=0.5390.
  - record (n=265): median=0.4596 max=2.2878.
  - annex/system supplementary (n=296): median=0.4715 max=1.3719.

## Method notes

- **Supplementary projection = V-2 machinery** (ratified): the record class DERIVES the axes; the wider corpus projects **supplementary** (standard MCA supplementary-point / CA transition-formula projection). Supplementary rows NEVER influence the axes — the 574 were never re-fit; the 265-kit record fit basis is byte-identical to the reproduction gate.
- **Annex places from SHARED vocabulary only.** The v2.0 six-block side-car (gb_* geometry-bands) populate ONLY the 267 record-class kits — annex/system have NONE, BY DESIGN. So annex/system project from the pre-v2.0 register coords (14-field cell_key) + element_primary; their gb_* blocks are passive. This is EXPECTED and rendered visually distinct (smaller hollow/faint markers), not hidden.
- **E4-side projection IS recoverable** for annex/system via the frozen E1 basis (`atlas_frozen_basis_reconstruct.FrozenBasis.project_point_xy`), which projects a supplementary point from the 14-field cell_key (register coords; the frozen basis has no bands/element). Stored `atlas_coords` used where present.
- **B2 alignment** reused verbatim from the reproduction gate = the identical B3 test transform (translation + rotation + reflection, **NO scale**; s* disclosed, not applied). Both panels share axis limits → directly comparable.

## Carried-forward caveat (from exhibit v1)

- The fused rare bucket **`gb_width/other-rare` tops BOTH candidate dims** (dim1 loading **+1.86**, dim2 loading **+2.48**). This is rare-category MCA leverage: a low-population fused level dominating the leading axes is part of why the refit is **not servable-grade** (it, with the 0.7836 congruence < 0.85, is why §8-C keeps E4 as truth). The candidate camera shown here is a diagnostic, not a proposed replacement.

## Files

- `side-by-side-574.png` — 316961 bytes
- `delta-arrows-574.png` — 700031 bytes
- `e5-candidate-coords-574.csv` — 54278 bytes

## Exact reproduction command

```
cd /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts
python3 atlas_e5_exhibit_574_2026_07_22.py
```

Deterministic: SEED=20260722, all randomness pinned. corpus.db opened read-only (uri mode=ro). Imports `atlas_e5_exhibit_2026_07_22` + `atlas_legb_refit_2026_07_22` verbatim (no math changed). corpus.db md5 = `bebc933b0bf9bcab5988bbc16bcc55b4` (unchanged; read-only).

## Constraint attestation

- READ-ONLY on corpus.db and every store — zero mutations.
- NO serving artifacts: no atlas-edition5.json, nothing under serving/vendor/Glance paths, no served-coordinate filenames. All files under this full-574/ exhibit dir.
- Reproduction gate (8/8) gates the renders: any mismatch → HALT, no renders.
- No island/cluster/build-family naming (Matt-gated). Vocabulary shown: court, corpus_class, game.
