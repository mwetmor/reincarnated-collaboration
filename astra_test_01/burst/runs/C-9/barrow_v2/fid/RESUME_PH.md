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

## State (keep current at every commit)
- [x] harness P1–P11 built: `fid/ph/harness/` (README has the run order). Results in `fid/ph/results/`.
- [x] calibration: `fid/ph/calibration.md` / `.json`. Rulings R-C9-167 and R-C9-168 are folded in calibration.md § 7.
- [x] P6a: the ground truth was re-derived from layout v5 + the zone map + Matt's sheet (calibration.md § 9) before re-scoring (§ 10). Judge G misses item_17 (it sits on the brazier disc), catches 08/11 and the stamp, and gives 1 material "yes" -> acceptance NOT met -> fallback (a), conductor triage by eye per chunk (R-C9-169). v0.1 sees both invented features with 15 material flags.
- [x] P4 new classes mapped (wood, shingle, sea, shore ice): ADVISORY now, BINDING in Phase 3 vs the W-B distribution.
- [x] P8 FINAL: bar 0.4476 = v1's minimum chunk (PT reproduced all 16 exactly, T3).
- [x] P11 v2 ABX BINDING (R-C9-171): 159 40/40, half-density 37/40, 158 36/40, all FAIL correctly; answers in `p11/answers/`. Generator fixed for future sets: different-X repeats, X_OVERLAP 0.25, content control, an UNDERPOWERED flag, PT stills in the pool. The calibration sets are NOT rebuilt.
- [x] P10 for R-C9-159 (informational): p99 13.55 ms, PASS (`renders/perf_v159`). The Godot queue is empty.

## Next / re-run
0a. When the P6a judge answers arrive: `python3 p6_judge.py score <answers.json>`; record the result in calibration.md § 8 and copy the answers to `fid/ph/p11/answers/p6_judge.json`.
0. When the ABX answers arrive: copy them to `fid/ph/p11/answers/abx_<set>.json`, then `python3 calibrate.py`, then commit.
1. A fresh level: `./run_godot_queue.sh all`, then every row script, then `calibrate.py`.
2. P11 for the fid level: point SETS at its play-camera stills (>= ~12, with ID-render class masks `<still>.classes.png/.json`), run `python3 p11_abx.py build`, and check that no set is UNDERPOWERED before handing it to a judge.

---
# Phase 0 Gate-2 folds owed by PH (charter § 13) — before the first W-A chunk is judged
- **G2-B1 overlay tooling:** a P6a triage tool that, per v0.1 candidate inside a declared dark structure, renders the crop with the **layout-projected declared-opening overlay** (from LV's declared-opening list for v7; from layout v5 for the BVR truth set) and the distance (m) to the nearest declared opening; writes `results/p6a_triage_<window>.jsonl` rows {chunk, candidate px, crop sha, overlay sha, nearest declared id, distance m, verdict, evidence, reader}. Match radius = declared opening's half-width + 1.0 m. Also build the § 9 truth set re-rendered with the overlay in place of the zone map, judge-ready (JUDGE.md + items, key outside) — the conductor spawns a fresh judge.
- **G2-B2 P11 v1 GREEN:** on the FIXED generator build (i) **v1 vs v1** (record-time `section_v1cam/v1ref/` stills vs PT's HEAD stills `fid/pc/v1_stills/`; 40 trials) and (ii) **v1 vs half-density** (40 trials, content-controlled). Judge-ready dirs; tell the conductor. Record results in `calibration.json` incl. the v1 cell. UNDERPOWERED (< 40) = VOID.
- **W-3 P8:** re-instrument to like-for-like (per-chunk vs v1's per-chunk distribution, or whole-window vs whole-window with a v1-justified tolerance); add a graded constructed RED near the bar (e.g. 1 m shift). Record as re-instrumentation.
- **I-4:** clear the stale lines in calibration.md.
- **Phase 1 support:** when LV's guide + ID render land, run P6 geometry agreement against the **layout_v7 polygons**.
State: [x] G2-B1 tool (`harness/p6_overlay.py` triage/record; BVR demo jsonl) [x] G2-B1 judge set (`fid/ph/p6_overlay_judge/`, awaiting judge) [x] G2-B2 sets (`fid/ph/p11/abx_g2_v1rec_vs_v1head/`, `abx_g2_v1_vs_halfdensity/`, 40 trials each, awaiting judges) [x] W-3 (P8 per chunk, graded RED) [x] I-4 — calibration.md § 11.
R-C9-175 recorded (calibration.md § 12): P11 v1 GREEN 22/40 PASS, half-density 33/40 FAIL, both judges valid. P6a overlay judge: acceptance not met, so the conductor reads candidates by eye under § 13. P11 counts from W-A on.
Phase 1 P6 vs layout_v7c DONE (calibration.md § 13, `results/p6_phase1_v7c.json`, `harness/p6_phase1.py`). Containment 1.0 everywhere (placement agrees); rendered IoU median 0.457 is below the ruled 0.513, which needs a ruling (shape fill). Missing: braziers (GLB), rock_outcrop_3. Buried: standing_stones, cliff_faces, grave_markers. Check (a) PASS stands (hall door area +30% vs LV; breach/hull not separable).
Next, when the triage inputs exist: run `p6_overlay.py triage` with LV's v7 declared-opening list and dark-structure ID mask; run P6b against the layout_v7 polygons.
