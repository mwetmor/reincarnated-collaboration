# BV2F lane PH (galadriel) — RESUME

> **§ 15 HEADER (R-C9-185/186):** the run is ART-FIRST. P6′ now runs against `fid/lv/layout_bv2art.json` (extent component retired); P7 retired; frame = `frame_grid.bv2art.json`; DEV-4 retired; DEV-1/6/7/16 restated in charter § 15.1. The layout_v7/v7c next steps below are SUPERSEDED. Next for PH: I-4 constructed 1.5 m-shift RED on bv2art, then P6′ on LV's blockout; W-4(2) the minimum pilot window for a 40-trial P11.

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
Phase 1 P6 RE-MEASURED on LV's fixed v7c (d4c59061f; calibration.md § 14): no missing or buried objects; containment 1.0; IoU median 0.46 < 0.513, attributed per object (under-fill dominates; placement 0); check (a) re-read with LV's probes: exact; hall-door explanation accepted. Earlier pass: (calibration.md § 13, `results/p6_phase1_v7c.json`, `harness/p6_phase1.py`). Containment 1.0 everywhere (placement agrees); rendered IoU median 0.457 is below the ruled 0.513, which needs a ruling (shape fill). Missing: braziers (GLB), rock_outcrop_3. Buried: standing_stones, cliff_faces, grave_markers. Check (a) PASS stands (hall door area +30% vs LV; breach/hull not separable).
Next, when the triage inputs exist: run `p6_overlay.py triage` with LV's v7 declared-opening list and dark-structure ID mask; run P6b against the layout_v7 polygons.

## P6′ (R-C9-180, charter v0.4 § 14)
- [x] Pre-registered: calibration.md § 15 (`45fb5eaac`).
- [x] Calibrated: § 16 (`48dab5e17`). v1 PASS; one RED per component.
- [x] Run on v7c: § 17. **P6′ = RED**: presence (2 yard logs half buried), scale (137/148 instances > 1.10), extent (R11, from the combined hall+porch build). Placement PASS. Reported, NOT adjusted; this is a HALT for an LV fix (charter § 14).
- Re-run after LV's fix: `cd fid/ph/harness && python3 p6prime.py v7c`. The bars are frozen in `results/p6prime_calibration.json`; do not re-run `calibrate` unless re-registering.
- [x] Re-run on the R-C9-181 refit (9601add8a): **P6′ = PASS** on all four components (calibration.md § 18). Bars unchanged. Hidden-by-design accepted only for circle_stones #2, #4, #5 (declared in 9601add8a). The calibration REDs still fail under the same readings. IoU 0.472 reported against 0.635.
- [x] R-C9-182: R11 porch region pre-registered (§ 19, `904ac6dc0`), then measured (§ 20). Ruled region: PASS (13.117 vs body 12.273). Constructed RED: FAIL. Registered 1.287 m reading: 5.10 m, FAIL (non-binding). Cover clause: the tall part sits 4.8–8.1 m behind the outer face; the porch is 5.10 m at the door. I-R1 and I-R2 folded (§§ 17, 18).

## § 15 art-first (R-C9-185/186)
- [x] I-4 constructed 1.5 m-shift RED on bv2art: FAIL, 5 of 10 objects below the bar (calibration.md § 21).
- [x] P6′ on the bv2art blockout (frozen bars): placement PASS, scale PASS; **presence RED**, reported, not adjusted (HALT for an LV fix):
  - crag #2 and log #3 sit wholly below the sea surface;
  - slope stone #4 is at the frame edge (13 px in frame).
  - Re-run: `python3 harness/p6prime_art.py`.
- [x] Re-run after LV fix 550682c73: P6′ = PASS (presence, placement, scale; § 23).
- [x] W-4(2): the minimum pilot window is 3 × 3 (cols 0–2, rows 0–2; 40 trials, 10 repeats). The home ground's extent decides it (§ 22). The conductor rules the pilot.

## Phase 2′ pilot (R-C9-188/189)
- [x] (1) Run plan: `fid/ph/pilot_run_plan.json` (calibration.md § 24).
- [x] (2) P11 still spec: `fid/ph/pilot_p11_spec.json`, 12 stills plus class masks; verified 40 + 10.
- [x] (3) Sea-cave walkability verified independently (calibration.md § 25): PASS 8/8, step height 0.1025 m derivation confirmed; REDs (0.6 m riser, 1 m gap) FAIL in PH's analysis and in LV's tool.
- [x] PT's pilot inputs landed (776e265f0 + 47bb1a054).
- [x] R-C9-192 pilot harness run: `ph/harness/pilot_harness.py [rows]` -> `ph/results/pilot/*.json`; calibration.md § 26. FROZEN bars.
  P1 FAIL (bakes barrow_front 1.711, wreck 1.391, cliff_faces_0 1.234: 1024² bake on hero-sized silhouettes) · P2 PASS 20/20 at 47bb1a054 (HEAD's tool moved at b69a5d6d1: lineage tool_sha stale for the next build) · P3 PASS 12.46 (RED fails) · P4 FAIL (ice every chunk 0.61-0.67 vs 0.126: paler, less blue; snow 0_2/1_2 cooler) · P5 PASS · P6a 5 unmatched candidates, all open sea in 0_2 (auto-fail by § 11 rule; conductor reads by eye: `results/p6a_triage_pilot.jsonl`, `triage/pilot/`) · P6′ PASS · P8 PASS min 0.4884 (RED fails); DEV-18: 30.9% of painted tuft px on not-flat ground without 3D heather · P11 set `p11/abx_pilot_v1_vs_pilot/` 40+10, judge-ready.
  P9: sway 5.967 PASS (no-wind RED fails) · water flow 0.000 FAIL (no water mesh: static painted sea plane) · trail 1.000 PASS. P10: p99 16.05 ms PASS (burn RED fails). Godot: `harness/run_pilot_godot.sh` + life_sea run; `python3 pilot_harness.py p9p10`.
- [x] R-C9-194: P6a conductor verdicts folded (5 × MATERIAL; P6a PASS); P4 forensic done (calibration.md § 27: guide identical, the PAINT transfer differs; sketch A mere nearer the pilot's ice, ΔE 11.0 vs 23.7).
- [ ] PT rebuilding the pilot (bake res, water, terrain heather): on hand-back re-run `pilot_harness.py p1 p2 p8 p9p10` (+ `run_pilot_godot.sh` and the life_sea view uv:-29,-5.5), and P3 (DEV-18 changes heather). P2: point PILOT_COMMIT at PT's hand-back commit.
- [x] R-C9-195: pilot P11 VOID x2 (27/40 inc 0.50; 24/40 inc 0.40); answers saved `p11/answers/abx_pilot_judge{1,2}.json`; void-rule analysis calibration.md § 28 (guesser inc mean 0.50, P(valid) 5.5%; no judge reaches valid+PASS > ~5% on the fixed generator) -- for Gate-2 / a ruling; no bar change.
- DEV-18 heather/snow-on-terrain adopted by R-C9-193 AFTER this baseline: re-run `pilot_harness.py p3 p8` and the P9 runs on the rebuilt pilot when PT lands it.

## R-C9-194 rebuilt pilot (0b72461db) -- DISK HALT (conductor, /System/Volumes/Data 18 GiB < 21)
- [x] Measured (calibration.md § 29, `ph/results/pilot2/`): P1 PASS (1.000; DEV-19 bakes 117.6-163.1 px/m, painting-bound), P2 PASS 20/20 at 0b72461db, P3 PASS 11.53 (informational), P8 PASS min 0.5302 with self-moving water excluded (as delivered 0_2 = 0.000: the heather mask captured the animated sea), P9 trail PASS 1.000.
- [x] P9c instrument finding: calibrated floe_drift is blind to texture motion (hard shared window); sub-pixel tapered version in pilot_harness (self-test rest 0.15-0.25 / world 1.26-2.00) -- not calibrated to bind; needs a ruling.
- [ ] HALTED: no Godot run made. On resume (disk >= 21 GiB): `harness/run_pilot2_godot.sh` (life_sea, life_sea_floered, life, life_nowind, perf, perf_sea, perf_burn -> ph/renders/pilot2/), then P9 (`PH_PILOT_RENDERS=renders/pilot2 PH_PILOT_OUT=results/pilot2 pilot_harness.py p9p10`), `floe_drift_subpx` on life_sea vs life_sea_floered, P10. ph_life.gd pilot hooks are untested.
- Ask to PT: capture heather_mask/render_guide with water time held.

## R-C9-196 (resumed; disk 24-29 GiB)
- [x] P8 on PT's fixed mask (8df01abcd): PASS min 0.5302 (exclusion withdrawn, env-gated off).
- [x] Renders done (`ph/renders/pilot2/`, PNG pairs only): P9 sway 6.104 PASS (no-wind RED fails); P9 flow 1.524 > 0 and 9x noise, but < frozen 2.064 (clause (b)) -> FAIL on the frozen bar, flagged (paint_mix 1.0 vs 159's 0.75); trail PASS; P10 p99 16.54 (start) / 15.18 (sea) PASS, burn RED fails.
- [x] P9c re-instrumented (`floe_drift_v2`, ph_life marker R const / G noise, `--floe-red`): self-test rest <= 0.007, RED = motion; pilot RED 0.643 FAIL; rest-pose 0.528 2-D (vertical: waterline occludes the bobbing silhouette) / 0.015 horizontal. Non-binding; ruling needed (PH recommends (b): depth-test-off marker shot). calibration.md § 30.

## R-C9-197 (PT 9c53bc067)
- [x] P9c pre-registered (§ 31, 3888c0d74) + A1 (depth-test-off drew nothing -> sea hidden for marker shots; 96509f727), then measured (§ 32): rest-pose 0.010 PASS, swimming RED 1.766 FAIL -> P9c SHOWN; binding is the conductor's call.
- [x] P9 flow 1.551 (paint_mix 0.75) < 2.064 -> FAIL on the frozen bar (paint_mix was not the driver; open water vs v159's surf). P10 PASS p99 16.20 / 14.49 ms.
- Runner: `harness/run_p9c_godot.sh p9c flow perf` -> ph/renders/pilot3/.

## PT 8fd69fafc (foam)
- [x] P9 flow same mask 3.444 PASS (own-mask 1.914: foam leaks into floe/heather exclusions; marker-floe mask 4.092); P10 start run1 17.32 FAIL / repeat 16.03 PASS (ruling); sea 13.87; P2 20/20. calibration.md § 33.
