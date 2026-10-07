# BV2F lane PH (galadriel) — RESUME

**Charter:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 4, 5 (Phase 0 row 0.4), 9 (C-1..C-3). Plan § 4 Phase 0.4 (the P1–P11 table) and § 1 (v1 numbers).
**Phase:** 0 (no image spend). Write only under `runs/C-9/barrow_v2/fid/ph/` and this file.

> **Gate-1 folds (charter § 12, R-C9-163) GOVERN this file** — in particular W-1, W-7, I-1, I-2 below.

## Phase 0 task: 0.4 the v1-parity harness, calibrated
Build `fid/ph/harness/` implementing P1–P11 (plan § 4 table). Inputs:
- **Positive control (must PASS every row):** v1 — `barrow_full/paint/barrow_full_painted.png`, `barrow_full/take/`, `barrow_full/godot/` (level `barrow_painted.tscn`), `barrow_full/captures/`. Lane PT will drop fresh v1 play-camera stills in `fid/pc/v1_stills/` (+ `views.json`); use existing captures until they land.
- **Primary negative control (R-C9-159):** `barrow_full/godot/data/barrow_v2_sw/`, `barrow_v2/section_v1cam/look/`, `barrow_v2/tools/v2sw_*`. It must FAIL at least P1 (ground at 50.3 px/m), P2/P3 (model bakes lit through the dynamic sun, `barrow_v2_sw.gd:643-669`; separate per-model paintings), P4 (cellularity — spectral peak at 6–20 px period on the bakes).
- **Secondary negative control (R-C9-158):** `barrow_v2/section_sw/` — negative for P9 only (no heather wind, no moving water, no snow trail); not required to fail quality rows (charter § 9 C-2).
Rules:
- **Quality rows (P1–P6, P11): a metric that cannot separate v1 from R-C9-159 is DISCARDED, not tuned.** Constraint rows (P7–P10) keep a v1 positive control but are not discarded for failing to separate 159 (charter § 9 C-1).
- Thresholds come from v1's own distribution (e.g., chunk-to-chunk spread), never from what 159 happens to score.
- Every metric must prove it can see a failure: for each row, a constructed failing input (e.g., a half-density resample for P1, a lit re-render or synthetic re-shade for P3, a stamped cellular texture for P4, a shifted seam for P5) — an instrument that only ever returns PASS is not an instrument.
- P11 (blind pair test) — build the crop-pair generator and answer key only; the judge is a fresh galadriel instance the conductor spawns with crops only (C-3). Do not judge your own test.
Deliver: `fid/ph/calibration.md` — the table (row × {v1, 159, 158, constructed-fail} → value, PASS/FAIL), each threshold with its v1 source, discarded rows with reason; `fid/ph/harness/README.md` with run commands; machine-readable `fid/ph/calibration.json`.

## Gate-1 folds (binding)
- **Per-row negative control = the attempt that showed that row's defect:** P1–P4, P11 → R-C9-159; **P5 → R-C9-158** (`barrow_v2/section_sw/`, seams); **P6 invention check → R-C9-155 BVP re-test-2 blocks** (find them under `barrow_v2/paint/` or the BVP lane outputs; cite); seeded failure where no real one exists.
- **Constraint rows P7–P10 must each show RED once** (constructed input).
- Rule: **"re-instrumented or discarded; never threshold-tuned."** Record every re-instrumentation in calibration.md. The quality/constraint split freezes at the Phase 0 Gate-2.
- **P2 = lineage chain:** each static texture's input sha → producing tool's manifest → painting sha `eecb4266…`. A shader/layer check alone passes 159 and is not acceptable.
- **P3 = per class**, labelled "rendered-vs-painting residual" (v1 unlit reference 15.5, lit 40.7 — `take/build_plan.md`).
- **P6 (Phase 1 use):** judged against layout_v2 polygons, not the guide's own class map.
- **P4 new classes** (sea, shingle, shore ice): a named nearest v1 class, or the class-agnostic cellularity detector only.
- **P8 threshold** comes from PT's reproduced v1 value (recorded share is ~0.44–0.47, not 0.52).
- **P9 mechanical:** flow > 0 inside the water mask; floe UV drift 0 px on a marker; snow-trail coverage % of floor.
- **P11:** n = 40 pairs, include v1-vs-v1 null pairs, strip PNG metadata and filenames, identical crop sizes; print the pass-probability power table on the row.

## Constraints
Heavy lock for any Godot render: `python3 runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>`. Disk gate 21 GiB. Matt runs deletions. Never work around a permission denial.
Git: `git add -- <new paths>`, `git status --porcelain -- <paths>` before, `git commit --only <paths>`, `git show --stat HEAD` after. Never `git add -A`. Do NOT edit/commit `ledger.json` (conductor only); HALTs go in this RESUME + hand-back. Do not push.

## State
- [ ] harness P1–P11
- [ ] calibration table (v1 pass / 159 fail / constructed fails)
- [ ] P11 pair generator + answer key
