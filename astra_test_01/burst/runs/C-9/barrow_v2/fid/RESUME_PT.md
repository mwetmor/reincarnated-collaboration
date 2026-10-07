# BV2F lane PT (drax) — RESUME

**Charter:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 4, 5 (Phase 0 rows 0.1, 0.3), 6, 10. Plan § 1 (W1–W10) is the v1 mechanism.
**Phase:** 0 (no image spend, $0). Write scope: see the Gate-1 fold note below. Do NOT edit anything under `barrow_full/` (v1 is the positive control).

## Phase 0 tasks
> **Gate-1 folds (charter § 12, R-C9-163) GOVERN this file.** Write ONLY under `fid/pc/` (0.1), `fid/v1tools/` (0.3), and this file. Record the shas of `barrow_full/paint/barrow_full_painted.png` (`eecb4266…`) and every file in `barrow_full/godot/data/painted/` BEFORE and AFTER each run into `fid/pc/control_shas.json`; `git status --porcelain -- astra_test_01/burst/runs/C-9/barrow_full/` must show nothing new from you. Any v1 tool whose default output is a v1 directory gets its output redirected by argument/env, or is not run; if neither is possible, HALT and report.

### 0.1 Positive control — re-render v1 at HEAD, reproduce its RECORDED numbers (W-2)
Write each target as {record file, field, tool + args, configuration}, tolerance from the record's own spread — in `fid/pc/targets.json` BEFORE measuring. Do not search for an instrument that reads a remembered number. Known records:
- ID self-test: `take/take_report.json` (+ `capture_ids.gd`).
- rendered-vs-painting residual (unlit 15.5, lit 40.7): `take/build_plan.md:~215` — find the tool + args that produced it.
- heather share on painted tufts: `take/build/overlay_check.json` `precision_drawn_on_painted` (0.4653 / 0.4476) and `take/build/painted_prep.json` `tuft_cells_covered_share` (0.4379). The plan's "52%" is WITHDRAWN (ledger prose). Report the reproduced value; the P8 threshold is re-derived from it.
- frame time: `barrow_full_layout.json` `frame_cost_ms` (8.55–21.31 by configuration) — name the configuration that matches the shipped level and reproduce that one. The plan's "10.9–12.4 ms" is WITHDRAWN.
Also: v1 play-camera stills at 1920×1080 of 6 named views (start, barrow door, mere, stone ring, outcrop field, shore) to `fid/pc/v1_stills/` + `views.json` (PH's positive-control crops). A target that misses its record = HALT.

### 0.3 Two-tier freeze (B-1) — after 0.1
- **Tier A, byte-identical:** `conductor_scripts/{guided_paint.py, guided_stitch.py, wave.sh, refs_guard.py, cfg_t10bf.json}`, `barrow_full/tools/{heather_instances.py, hero_surface.py, t5_06b_bake.py, make_layout.py}`, `nb_t8/scripts/t5_06a_surface.py`.
- **Tier B, minimal patches:** `capture_blockout.gd`, `capture_ids.gd` (hard-coded GUIDE/GRID/window/scene, e.g. `capture_blockout.gd:26,34-35,71,111`, `capture_ids.gd:23,47`), `paint_world_prep.py:34,43-46`, `take_from_paint.py`, `t10bf_drive.sh` (CFG, prefix, `$C/` calls → frozen copies; exit 7 on usage limit = DEV-15). Each patch is committed as a diff `fid/v1tools/patches/<file>.diff` against the v1 source, touching only allowlisted constants/paths listed in `fid/v1tools/ALLOWLIST.md`. Path-relative tools (`HERE`/`ROOT`) get roots by arg/env or pinned cwd — leave Tier A byte-identical.
- Where two v1 copies exist (`capture_*.gd` in `app/tools` vs `godot/tools`; `t5_06b_bake.py`), establish from records which v1 ran; cite evidence.
- `SHA256SUMS`: two shas per file — the v1 source **read from git at a pinned commit** (`git show <commit>:<path> | shasum -a 256`; record the commit), never computed from the copies — and the shipped file's.
- `verify.sh`: checks the shipped shas AND that the driver's command lines reference only `fid/v1tools/` paths (fails if any v1-original path appears). Prove it goes RED: one tampered copy, one driver line pointing at an original.
- Proof of the freeze: run 0.1's ID self-test once through the patched tools with v1's own frame/grid config; it must reproduce the unpatched result.

## Constraints
Heavy lock for every Godot/Blender run: `python3 runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>`. Disk gate: halt heavy work below 21 GiB free (`df -h /System/Volumes/Data`). Keys via `source ~/.zshrc`, never printed. Matt runs deletions. Never work around a permission denial.
Git: commit only your own paths: `git add -- <new paths>`, `git status --porcelain -- <paths>` before, `git commit --only <paths>`, `git show --stat HEAD` after, `git -C` cross-repo. Never `git add -A`. Do NOT edit or commit `ledger.json` (conductor only); HALTs go in this RESUME + your hand-back. Do not push (conductor releases).

## State
- [ ] 0.1 positive control — IN PROGRESS (switched here on the conductor HOLD below)
- [~] 0.3 frozen toolchain — **ON HOLD (conductor, Gate-1 B-1 BLOCK-narrow: two-tier freeze fold coming). Copies + SHA256SUMS + verify.sh exist in `fid/v1tools/` UNCOMMITTED; do not commit until revised 0.3 instructions land here.** PROVENANCE.md / frame_grid.json not written.

### 0.3 findings so far (uncommitted work in `fid/v1tools/`)
- 10 tools + reference (`make_layout.py`, `cfg_t10bf.json` — the latter carries v1's `geo`/`rules`/`refs` brief, W3) copied mirroring source dirs; `SHA256SUMS` 12 files; `verify.sh` exit 0 on HEAD, exit 1 on a tampered copy and on an unlisted file (scratch tests).
- **Duplicates are byte-identical**: `capture_blockout.gd` app/=godot/ `f630f564c1fd`; `capture_ids.gd` app/=godot/ `7e6e16369489`; `t5_06b_bake.py` barrow_full/tools = nb_t8/scripts `28b2dc11dcd1`. v1 ran the `godot/` copies (`take_report.json` `regenerate`: `Godot --path godot ... tools/capture_ids.gd`; `app/` is gitignored, `barrow_full/.gitignore:7`) and `barrow_full/tools/t5_06b_bake.py` (`bake_report.json:3` records sha `28b2dc11…` = nb_t8; `bake_heroes.py:36` asserts identity).
- **HEAD ≠ as-run for 4 tools (all non-functional for v1's outputs or re-run):**
  - `t10bf_drive.sh` HEAD `8c2c32ec21a5` (174512232, disk gate 20) was committed AFTER painting. As run: `e2f5f37d68a0` (816fd84b8, 41 GiB guard) 02:33Z–06:00Z, then `4ba9b86c6544` (32d068af9, 25 GiB) from the 06:00:49Z restart (ledger N-C9-DRIVE-STALL). Diffs = disk-guard constant + comment only.
  - `capture_blockout.gd` guide rendered by `feaa1c94f1ff` (e0462ab03); HEAD `f630f564c1fd` (111c85f5d) adds `--painted` (default false) only.
  - `take_from_paint.py` first take `8c745b812ad6` (46181364c); HEAD `17998c5a986a` (3b8a4fbfd) changed the tuft density base line and tufts.json was re-made with it in that commit → HEAD is v1's final.
  - `paint_world_prep.py` built by `21ca10b2c89a` (111c85f5d); HEAD `b77325d07621` (5f96ba0fe) adds `web()`/`--web` only; `main()` unchanged.
- Hard-coded frame/grid (for the held PROVENANCE): guided_paint.py:25,26,31,32 (stride 1280×768, canvas 1536×1024), :35,:44,:46 (256/1536×1024 in brief text); guided_stitch.py:12; t10bf_drive.sh:6 (cfg), :20,:22,:27 (prefix T10BF), :12 (disk); capture_blockout.gd:26-35 (GUIDE 5376×3328, PLAY, TOP, GRID_U/V walk grid) + scene `res://scenes/barrow_full.tscn` :71; capture_ids.gd:23,131,132,145,149,151 (5376×3328, 100.617553710938, 80.3076); paint_world_prep.py:34-46 (paths, sha prefix, PPM, PITCH 52.9535, yaw 47), :387 (snow 768/1024); take_from_paint.py:39-42 (paths, sha prefix), :276 RES 10, :404 GRES 20, :345/:395 px filter sizes; heather_instances.py:39 STEP; hero_surface.py:32,37. All other frame values are read from `barrow_full_layout.json` `frame` (two layout copies differ: root `3c9a47c9ac23` read by take_from_paint/heather_instances; `godot/data/` `abe8256fad68` read by paint_world_prep). Python tools resolve `BF` from their own location (`dirname(dirname(__file__))`), so a copy run in place points at `fid/v1tools/barrow_full`, not v1.

### 0.1 recorded values (sources)
- ID self-test: `take/ids/ids.json` `instrument_check` worst camera-vs-formula **0.004 px** over 86 placements; `take_report.json` `cell_formula_check` 0.0007 px.
- Unlit/lit: `take/build/mini_overlay.json` summary **unlit 15.5, lit 40.7** (ledger N-C9-PAINTED-LIGHT-RULING).
- Heather (Gate-1 W-2: as RECORDED, three different quantities): `take/build/overlay_check.json:1781` as_painted whole-window `precision_drawn_on_painted` **0.5221** (the "52%", commit 111c85f5d "precision 0.52"); same block `coverage` **0.3407**; `take/build/painted_prep.json:127` heather `tuft_cells_covered_share` **0.4379**.
- Frame time: `take/build/painted_captures.json:234-236` exported app **10.93 / 10.97 ms windowed, 12.40 ms fullscreen**. Note: commit 5f96ba0fe (trail polish) records the restaged desktop app at **12.8–12.9 ms fullscreen**, i.e. v1-at-HEAD was already outside 12.4 by its own record.
Next step: 0.1 — run the v1 instruments at HEAD on a COPY (no writes into barrow_full/), heavy lock.
