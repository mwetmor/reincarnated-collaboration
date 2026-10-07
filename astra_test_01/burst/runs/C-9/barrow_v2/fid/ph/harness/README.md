# BV2F lane PH — the v1-parity harness (P1–P11)

Charter: `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` (§ 9, § 12 Gate-1 folds govern).
Plan: `…-barrow-v2-fidelity-run-architecture.md` § 4 Phase 0.4. Calibration: `../calibration.md`, `../calibration.json`.
Owner: galadriel (lane PH). Writes only under `fid/ph/`. Every row's docstring states its metric, threshold, v1 source,
negative control and constructed failure; read the file before trusting a number.

## Run order (from this directory; python3 with numpy, scipy, Pillow, matplotlib; ffmpeg for P9's film check)

```
./run_godot_queue.sh capture      # P3/P4/P6 renders: renders/v159 (godot/ph_capture.gd), renders/v1 (v1's capture_painted.gd, read-only)
./run_godot_queue.sh life         # P9 in-engine pairs: renders/life_v1, life_v1_nowind (RED), life_v159
./run_godot_queue.sh perf         # P10: renders/perf_v1, perf_v1_burn (RED), perf_v159
python3 p1_density.py             # -> ../results/p1.json
python3 p2_lineage.py             # -> p2.json         (a new level: --spec its lineage.json, schema in the docstring)
python3 p3_residual.py            # -> p3.json         (needs renders/v1, renders/v159)
python3 p4_texture.py             # -> p4.json         (needs renders/v159 for the model classes)
python3 p5_seams.py               # -> p5.json
python3 p6_geometry.py            # -> p6.json         (--part invention | iou)
python3 p7_p8_floor_heather.py    # -> p7_p8.json
python3 p9_p10_life_perf.py       # -> p9_p10.json     (needs renders/life_*, perf_*)
python3 p11_pairs.py build        # -> p11/judge_<set>/ (pairs + JUDGE.md: the ONLY thing the judge sees), p11/keys/<set>.json
python3 p11_pairs.py score <set> <answers.json>      # v0.1 directional test (superseded, R-C9-168; kept for its evidence)
python3 p11_abx.py build          # P11 v2 ABX: p11/abx_<set>/ (50 trial images + JUDGE.md), keys p11/keys/abx_<set>.json
python3 p11_abx.py score <set> <answers.json>        # answers {"trial_NN": "A"|"B"}; put them at p11/answers/abx_<set>.json
python3 calibrate.py              # -> ../calibration.json + the table in ../calibration.md
```

Every Godot run goes through `heavy_lock.py C-9` after the 21 GiB disk gate (`run_godot_queue.sh` enforces both).
Renders and judge PNGs are gitignored (`astra_test_01/.gitignore: *.png`); they regenerate from the commands above
(P11 pairs are seeded: `build` reproduces the same pairs and key).

## Files
| file | row |
|---|---|
| `common.py` | shared: paths, Lab, radial spectrum, GLB AABB |
| `p1_density.py` | P1 displayed texel density |
| `p2_lineage.py` | P2 lineage chain to the painting sha |
| `p3_residual.py` | P3 rendered-vs-painting residual per class |
| `p4_texture.py` | P4 per-class Lab histogram + spectrum shape (cellularity discarded, reported) |
| `p5_seams.py` | P5 overlap MAD + stitched seam visibility |
| `p6_geometry.py` | P6 invention check + silhouette IoU |
| `p7_p8_floor_heather.py` | P7 clean floor on the painting; P8 heather from painted tufts |
| `p9_p10_life_perf.py` | P9 life (sway, water flow, floe drift, trail coverage); P10 p99 frame time |
| `p11_pairs.py` | P11 v0.1 directional pair test (superseded by ABX, R-C9-168) |
| `p11_abx.py` | P11 v2 blind ABX: generator, key, scorer (accuracy + repeat reliability), power table |
| `calibrate.py` | assembles calibration.json and the table |
| `godot/ph_capture.gd` | paint-frame render + per-group shadow-only masks (a level extending barrow_full.gd) |
| `godot/ph_life.gd` | static two-frame life pairs, floe checker marker, perf loop |
| `run_godot_queue.sh` | the Godot runs, locked and disk-gated |

## For later phases (the fid level)
P1: add the level's surfaces to `SETS` (projection ppm from its frame; bakes from the painting at the game camera).
P2: lane PT emits `fid/pt/lineage.json` in the documented schema; `p2_lineage.py --spec` scores it.
P3/P4/P6b: `ph_capture.gd` takes any scene extending `barrow_full.gd` with `lvl.frame.paint`, `model_meshes`, `_heather_mmi`.
P6a: declared openings come from `layout_v2.json` models[].opening (Phase-1 rule, W-7); `bvp_declared()` projects them.
P11: point `SETS` at the level's play-camera PNG stills; regenerate; the conductor spawns the judge.
