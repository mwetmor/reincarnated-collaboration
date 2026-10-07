# BV2F lane PT (drax) — RESUME

**Charter:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 4, 5 (Phase 0 rows 0.1, 0.3), 6, 10. Plan § 1 (W1–W10) is the v1 mechanism.
**Phase:** 0 (no image spend, $0). Write only under `runs/C-9/barrow_v2/fid/pt/`, `fid/v1tools/` and this file. Do NOT edit anything under `barrow_full/` (v1 is the positive control).

## Phase 0 tasks
### 0.1 Positive control — re-render v1 at HEAD, reproduce its recorded numbers
Targets (with recorded sources — find and cite each source file/ledger entry in your report):
- ID self-test pass (`capture_ids.gd`, `take/take_report.json`)
- unlit-vs-painting mean diff **15.5** (±0.5) (N-C9-PAINTED-LIGHT-RULING; lit was 40.7)
- heather **52%** on painted tufts (±2 pts) (`paint_world_prep.py`, `heather_instances.py`)
- frame time **10.9–12.4 ms** on the desktop walk
Any miss = HALT (write `halts[]`-shaped note in your hand-back; conductor appends) — the baseline is not what we think.
Also save for galadriel (PH): v1 play-camera stills at 1920×1080 of 6 named views (start, barrow door, mere, stone ring, outcrop field, shore) to `pt/control/v1_stills/`, plus a `views.json` with camera positions. PH uses these as the positive-control crops.

### 0.3 Freeze the v1 toolchain
Copy byte-identical to `fid/v1tools/` and write `fid/v1tools/SHA256SUMS` + `PROVENANCE.md` (source path, sha, which v1 burst/ledger entry used it):
`conductor_scripts/guided_paint.py`, `conductor_scripts/guided_stitch.py`, `conductor_scripts/t10bf_drive.sh`, `capture_blockout.gd`, `capture_ids.gd`, `barrow_full/tools/{take_from_paint.py, hero_surface.py, t5_06b_bake.py, paint_world_prep.py, heather_instances.py}` (+ `make_layout.py` as reference).
- **Two copies exist** of `capture_blockout.gd` / `capture_ids.gd` (`barrow_full/app/tools/` and `barrow_full/godot/tools/`), and of `t5_06b_bake.py` (`barrow_full/tools/`, `nb_t8/scripts/`). Establish from the ledger/burst records which one v1 actually ran; if they differ, record both shas and the evidence. Do not guess.
- Write `fid/v1tools/verify.sh` (exit non-zero on any mismatch). Every later BV2F script calls it first.
- Only frame and grid become parameters, and only via a separate config (`fid/v1tools/frame_grid.json` schema), never by editing the copies. List every hard-coded frame/grid constant in each tool (file:line) in `PROVENANCE.md` so the parameterisation is auditable.

## Constraints
Heavy lock for every Godot/Blender run: `python3 runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>`. Disk gate: halt heavy work below 21 GiB free (`df -h /System/Volumes/Data`). Keys via `source ~/.zshrc`, never printed. Matt runs deletions. Never work around a permission denial.
Git: commit only your own paths: `git add -- <new paths>`, `git status --porcelain -- <paths>` before, `git commit --only <paths>`, `git show --stat HEAD` after, `git -C` cross-repo. Never `git add -A`. Do NOT edit or commit `ledger.json` (conductor). Do not push (conductor releases).

## State
- [ ] 0.1 positive control
- [ ] 0.3 frozen toolchain
Next step: start 0.3 (cheap), then 0.1.
