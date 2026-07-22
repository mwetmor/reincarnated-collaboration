# E5 CANDIDATE EXHIBIT — numbers only

**Date:** 2026-07-22 · **Executor:** elrond · **Purpose:** R1 ruling exhibit (camera fork). E5 NOT served (§8-C).

NOTE: numbers only. No axis naming, no interpretation. The conductor names axes from the loadings CSV.

## Reproduction check (vs 2026-07-22-legb-gate-report.md)

**Result: PASS — all values match record**

- B3 congruence          PASS | got=0.7836 want=0.7836 tol=0.0005 delta=0.0000
- rotation_deg           PASS | got=58.5364 want=58.5400 tol=0.1000 delta=0.0036
- reflection             PASS | got=True want=True
- n_fit                  PASS | got=265 want=265
- n_retained             PASS | got=17 want=17
- anchor_n               PASS | got=46 want=46
- s_star                 PASS | got=0.8117 want=0.8117 tol=0.0005 delta=0.0000
- E4 basis reconstruct   PASS | max_abs_err=4.938e-08 (<1e-6)

## Recomputed headline numbers

- fit population (record-class, atlas_coords non-null): **265 kits**
- retained dimensions (parallel-analysis, 1000 nulls): **17**
- anchor (record-class gateA members common to E5 fit AND E4 served): **46** (floor 40)
- B2 transform: rotation **58.54°**, reflection **True**, optimal scale s* **0.8117** (DISCLOSED, NOT applied)
- **B3 congruence = 0.7836** (threshold >= 0.85 -> FAIL)
- plane diameter (E5 17-dim retained space) = 5.6058
- corpus.db md5 = `bebc933b0bf9bcab5988bbc16bcc55b4` (unchanged; read-only)

- anchor displacement (E4->E5-aligned, n=46): min=0.0375 median=0.4368 max=1.4830 mean=0.5076

## Files

- `exhibit-side-by-side.png` — 224430 bytes
- `exhibit-delta-arrows.png` — 199178 bytes
- `e5-candidate-coords-aligned.csv` — 18633 bytes
- `e5-candidate-loadings.csv` — 2221 bytes

## Exact reproduction command

```
cd /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts
python3 atlas_e5_exhibit_2026_07_22.py
```

Deterministic: SEED=%d, all randomness pinned. corpus.db opened read-only (uri mode=ro). Imports `atlas_legb_refit_2026_07_22` verbatim (no math changed).

## Constraint attestation

- READ-ONLY on corpus.db and every store — zero mutations.
- NO serving artifacts emitted: no atlas-edition5.json, nothing under serving/vendor/Glance paths, no served-coordinate filenames.
- The B2 alignment reproduced here is identical to the B3 gate test (translation + rotation + reflection, NO scale).
