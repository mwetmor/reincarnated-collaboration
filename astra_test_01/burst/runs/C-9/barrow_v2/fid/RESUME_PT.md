# BV2F lane PT (drax) — RESUME

> **§ 15 HEADER (R-C9-185/186):** the run is ART-FIRST on a compact sketch-A site; frame = `frame_grid.bv2art.json` through the same Tier-B config path (no re-freeze); DEV-1/6/7/16 restated in charter § 15.1 (DEV-6 snow-field change, if needed, is a DEV-9 patch amendment + re-verify). PT stands by until Phase 2′.

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
- [x] 0.1 positive control — T1 PASS (byte-identical); T2 unlit PASS 15.5 (lit 36.2 informational, R-C9-166); T3 PASS exact (0.5221 / 0.3407 / 16 chunks; 0.4379); stills x6 + views.json in `pc/v1_stills/` (PNGs gitignored by astra_test_01/.gitignore:1, on disk, shas in results.json); **T4 MISS: 11.08 / 11.22 ms vs 10.93 / 10.97 windowed (same configuration: render 1726x971) → HALT H-C9-BV2F-PT-2 proposed.** control shas before == after; barrow_full status unchanged.
- [x] 0.3 two-tier freeze — bf188cb9f (+ proofs 1f73c6775). verify.sh green; RED x3; DEV-15 dry-run exit 7; freeze proofs byte-identical (python via v1run.py, GD by absolute --script + --frame-grid).

## HALT H-C9-BV2F-PT-2 — CLOSED by R-C9-169 (T4 re-based at HEAD as informational; P10 p99 <= 16.7 ms binds). Phase-3 flag: HEAD pck 1.1 GB vs v1 320 MB — the desktop build ships only the barrow_v2 level's data.
0.1 T4 frame time at HEAD 11.08 / 11.22 ms vs record 10.93 / 10.97 ms (painted_captures.json:234-235), same window/render configuration (1920x971 / 1726x971); record repeat spread 0.04 ms → MISS by 0.11-0.29 ms (1.0-2.6%). targets.json pre-registered the 12.40 fullscreen row assuming render 1920x1080; the app opened windowed 1726x971, so the windowed rows are the matched record. HEAD carries the post-v1 kits (pck 1.1 GB vs 320 MB; trail polish recorded +0.4-0.5 ms). Not bisected. **Conductor must rule:** accept as re-based (informational, like lit) or bisect.
- **R-C9-180 (Gate-2 W1, § 13 W-4):** T1–T3 re-measured at pin f1aa715ac and at barrow_full HEAD d4c59061f (LV additions only, 8 new bv2f paths): both PASS, pin == HEAD identical (T1 0.004 px + byte-identical take; T2 unlit 15.5, lit 36.2; T3 0.5221 / 0.4379, 0 painted files differ). `pc/results_phase1_close.json`, `pc/control_shas_phase1_close.json` (before == after == Phase 0).
- **R-C9-187 (Gate-2 F-1):** T1–T3 at pin f1aa715ac and barrow_full HEAD 550682c73 (additions only, bv2f paths): both PASS, identical (0.004 px + byte-identical take; unlit 15.5; 0.5221 / 0.4379; 0 painted files differ). `pc/results_phase1p_close.json`, `pc/control_shas_phase1p_close.json`.
## Phase 2' PREP (R-C9-188/189) — done, NO image spend; awaiting conductor geo review + release
- Pins (e9dabc263): `pt/pilot/pins.json` — guide 1883a1bb1e2e pinned as a COPY `pt/pilot/guide_art_pinned.png` (gitignored png; sha recorded) + the 9 pilot tiles; `python3 fid/pt/tools/pilot_pins_check.py` (exit 1 = a pin moved → repaint per R-C9-189). Run it before release.
- DEV-12 filled per R-C9-189 (`v1tools/DEV12_substitutions.json`, 2 entries); cfg_check.py now also requires `_guide_sha256` == the guide's sha.
- Pilot cfg: `pt/pilot/cfg_bv2a_pilot.json` (prefix BV2A, cols/rows 3, guide = pinned copy, refs = v1 IMAGE 2 only, rules = v1 + DEV-12, geo = draft, chunk_notes = DEV-10). cfg_check OK.
- geo draft: `pt/geo_bv2art_draft.txt` (conductor reviews).
- DEV-10: generator `pt/tools/chunk_notes.py` (ID render + id_table only) → `pt/pilot/chunk_notes.json` (9 notes); painter field = Tier-B `guided_paint.py` (one marked line; Tier-A v1 copy kept); driver calls the Tier-B copy. verify.sh green (22 files), driver RED re-proven.
- Dry run (`pt/pilot/dryrun/`): PATH shim on `zsh …/wave.sh` only (no Astra), fake HOME logs: verify OK → cfg_check OK → 0_0 staged (canvas == pinned crop) → brief → refs_guard OK → simulated usage-limit → exit 7; tampered rules → exit 9 before staging. Side effects (left, not committed): `briefs/C-9/BV2A-0_0.task.json`, `artifacts/CS9-guides/BV2A-0_0_canvas.png` + manifest entry (the real run re-stages identically).
- DEV-16: the take's ID table has 29 ids (≤ 256) → NOT OPENED (confirm at the take).
- To rule: (1) the pilot window CONTAINS the wreck (0_1,1_1,0_2,1_2) and the barrow front (2_0) — R-C9-189 W-5 schedules the DEV-3/11 plate A/B for the first chunk with the wreck/cave, which is this pilot; (2) cols/rows = 3 → 2_1 and 2_2 are painted without v1's top-right paste (3_0/3_1 not yet painted) — the cost of a kept origin pilot; (3) DEV-10 notes ON in the cfg, but DEV-10's with/without A/B does not fit the 18-image cap — run with notes, or drop `chunk_notes` for v1's brief.
- **R-C9-190 applied:** cfg geo = geo of record `pt/geo_bv2art.txt` (sha 5aa045dc33b8; cfg_check pins `_geo_file`/`_geo_sha256`); no hero plates (DEV-3/11 A/B → first Phase-3' cave chunk); DEV-10 notes OFF (no `chunk_notes`); 2_1/2_2 without top-right paste accepted. Prompt proof `pt/pilot/prompt_diff/` (pt/tools/brief_preview.py, frozen tools, no write to briefs/): pilot 0_0 brief == v1 0_0 brief with only geo + DEV-12 (2 substitutions) + cfg identity fields swapped; IMAGE 2, caps, retry clause identical.
- **Release gate:** conductor releases the first pilot burst after LV's sea-cave hand-back AND `python3 fid/pt/tools/pilot_pins_check.py` green. Burst: `bash fid/v1tools/tierB/conductor_scripts/t10bf_drive.sh fid/pt/pilot/cfg_bv2a_pilot.json` (absolute paths).
Next step: STAND BY — Phase 0 closed (R-C9-173); no PT work until the conductor resumes PT for Phase 2.

### 0.3 findings (first-layout notes; superseded by v1tools/PROVENANCE.md)
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
### 0.1 progress
- Method: APFS clone (`cp -Rc`, ~0 disk) of barrow_full at HEAD in the session scratchpad (`.../scratchpad/v1c/C-9/barrow_full`); v1 tools run unmodified there. `fid/pc/targets.json` + `control_shas.json` (before) committed before any measurement.
- **T1 PASS**: capture_ids.gd → worst 0.004 px over 86 placements; ids.png sha `ed9cfcd207c1` and ids.json **byte-identical** to v1's. take_from_paint.py → take_report.json, plates.json, tufts.json, density_uv.png, ground_uv.png, splat_world.png all **byte-identical** to v1's; cell formula 0.0007 px.
- **T2: unlit 15.5 PASS (per piece identical: 12.6/15.0/15.2/19.1); lit 36.2 vs recorded 40.7 → MISS** (door 35.9 vs 40.9, grave 34.2 vs 43.6, ring 42.7 vs 46.3, log 32.1 = 32.1). See `fid/pc/results.json`.
- control_shas before == after; barrow_full git status unchanged.

## HALT H-C9-BV2F-PT-1 — DISPOSED by R-C9-166 (lit informational; resume)
**0.1 T2 lit residual misses its record: 36.2 vs 40.7 (±0.5).** Unlit (the charter-gated number) reproduces exactly. The lit path (blockout ramp under the blockout sun, `mini_overlay.gd`) depends on `paint_stack.gd`/`barrow_full.gd`, changed by 17 commits after the record (3b8a4fbfd → HEAD; 111c85f5d replaced paint_stack.gd). Not bisected.
**Conductor must rule:** (a) is lit a gating target (charter row 0.1 names only unlit 15.5; my targets.json registered lit as gating)? (b) if gating: bisect the lit path (≈1 Godot run per candidate commit, $0) or re-base the lit record at HEAD. T3, T4 and the stills are NOT run; resume order T3 → stills → T4 from the clone (re-clone first if barrow_full has moved).
Next step: await ruling.

---
# Phase 0 Gate-2 folds owed by PT (charter § 13; jack-ryan `qa/findings/2026-10-07-bv2f-phase0-gate2.md` W-1, W-2) — before the FIRST BV2F paint burst
- **W-1:** `verify.sh` fails any `^+` patch line that neither carries `BV2F` nor sits inside the marked block; add a RED test for an added override line. Record shas of `verify.sh`, `ALLOWLIST.md`, `patches/*` in `PROVENANCE.md` (the conductor puts them in the ledger milestone).
- **W-2:** (a) a cfg check the driver calls before staging: the executed cfg's `rules` == v1's `rules` with the DEV-12 substitution table applied (write the table now as `v1tools/DEV12_substitutions.json`, empty of site content until LV's Phase-1 class list lands — then fill it, listing every v1-site noun and its replacement), and `refs` == v1's + DEV-11 entries; (b) record `lane/run_burst.py` sha at the pin in PROVENANCE (or declare it out of scope with a reason); (c) route Godot `.gd` copies through a sha-checking runner, or make lane scripts assert every `--script` path is under `fid/v1tools/`.
- Stills: PT's six v1 stills are in `fid/pc/v1_stills/` (done).
State: [x] W-1 [x] W-2(a) [x] W-2(b) [x] W-2(c) — commit dcf7cbc6a, same pin 0f8f73697 (no re-pin; Tier-B shipped shas changed by comment-only BV2F markers; re-proofs byte-identical). verify.sh green.
- **Open for LV/conductor:** `v1tools/DEV12_substitutions.json` is EMPTY (= v1 rules verbatim) until LV's Phase-1 class list lands; then fill `{"v1": ..., "v2": ...}` entries and re-run `cfg_check.py`. GD tools must now be run via `v1tools/godot_run.sh <project> tierB/...gd -- args`.
