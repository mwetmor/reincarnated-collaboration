# C-9 session handoff: post-ship disk cleanup of the barrow arena work

> **STATUS:** CURRENT (working-memory, session pointer). **Author:** gandalf (C-9 RUN-CONDUCTOR). **Date:** 2026-10-25.
> **Supersedes as the session pointer:** `2026-10-13-c9-arena-session-handoff.md`. Its open list, launch command and standing constraints still hold; this note adds only what happened after it.
> **Ledger:** R-C9-398.

## 1. What happened this section

Matt asked: *"Is there anything related to graphic arts session that we can delete to free up space at this point?"*

**Survey.** Free space was 26 GiB. The large folders under `astra_test_01/burst/runs/C-9/` were `barrow_full/` (17 GB) and `barrow_v2/` (8 GB). Every candidate was gitignored, and none was tracked. I sorted them into three groups.

**Deleted (Matt chose "Delete all three", about 7.1 GB):**

| Item | Size | Why it was safe |
|---|---|---|
| `barrow_full/pc_arena/build/BarrowArena-Windows-x64/` | 2.6 GB | An exact unpacked copy of the zip. The zip was checked against its saved sha256 (`f93490a5…207c`, match) and passed `unzip -t`. |
| `barrow_full/pc_arena/{.godot,kc2,models,data,scripts,scenes,barrow_v2}` | 3.2 GB | The Windows build's working copy. `tools/build_pc_arena.sh` re-syncs it from `godot/`. |
| `barrow_full/app/` | 1.3 GB | The 2026-09-29/30 Mac apps ("C-9 Barrow blockout", "C-9 Barrow painted"), replaced by the web routes and the arena. `tools/build_app*.sh` rebuilds them. Nothing tracked cites the folder. |

**Kept:** `pc_arena/build/BarrowArena-Windows-x64.zip` and its `.sha256` (which `audio_review/AUDIO_VERIFICATION.json` cites), `build/logs/`, `build/SFX_and_Sound_Selections/`, `export_presets.cfg` and `project.godot`.

**Who ran the delete.** My `rm -rf` inside the repo was **refused by the permission system**. I did not try another route. Matt ran the one-line `! cd … && rm -rf … && df -h /` himself. Free space went from **26 to 33 GiB** (it read 32 GiB at close, with the separate JOIN-1 job writing at the time).

**Kept on purpose, with reasons:**
- **`barrow_full/web_painted/` (2.2 GB):** still a live input. The arena's `level.json` files (site_ph3, site_ph4, the pilots, v7b) and `godot/data/barrow_v2_sw/section.json` load `stone_tall/mid/short.glb` and kit GLBs from `web_painted/models/barrow/`. It looks like a build copy, but deleting it would break the arena.
- **The `barrow_v2/fid/` painting work files (about 7.7 GB: 2.2 GB untracked plus 5.5 GB ignored; the largest is `pt/site4/root/work/bakes` at 1.7 GB):** these are the re-bake inputs for any repaint, such as the NE snow slope.
- **`barrow_full/godot/.godot` (1.4 GB):** the import cache. It regenerates, but the next launch then re-imports slowly.
- **`barrow_full/web_arena/` (1.5 GB):** the source of the current public build.
- **A 2.6 GB scratchpad of another session** (`/private/tmp/claude-501/…/ac232ef8…`): not ours. A JOIN-1 Godot run (KC2 conductor, `heavy_lock` JOIN1-J0F-port-emit) was live during the survey.

## 2. Docs updated

- **Canon:** `canonical/reap-die-rise-game/painted-2d-pipeline/painted-site-scene-and-arena-pipeline.md` v1.1. §11 adds the post-ship cleanup rule: rebuildable copies versus folders that only look like build copies, `git grep` the path before deleting, verify a zip before removing its unpacked twin, and the conductor prepares the list while Matt runs the delete.
- **Ledger:** R-C9-398.

## 3. Open, unchanged from the 2026-10-13 handoff

1. **Matt's ratifications:** DEV-30, and WARN-1 (the solver fallback, plus a same-seed native-vs-GDScript probe).
2. **The whirlwind smoke is missing** (R-C9-396).
3. **The public build is not confirmed on a phone yet.** The export is about 650 MB.
4. **Monsters as live 3D rigs.**
5. **Small items:** the NE snow slope, the slow-return probe spots, and the slash, which is presentation only.
6. **The T34 quiet-window frame-rate run.**
7. **A Mac restart** would free about 12 GB more.
8. **Untracked files of unknown owner** in `barrow_full/godot` (`data/bv2f/stair_snow/`, `tools/probe_burn_cost.gd`, `tools/probe_eor_q.gd`). Leave them alone.

**Further cleanup, if Matt asks:** once he rules the barrow_v2 painting final with no more repaints, its work files (about 7.7 GB) could go through a build-safe manifest. That needs his explicit word, because those files are the re-bake inputs.

**Local play** (unchanged):
```
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_full/godot && /Applications/Godot.app/Contents/MacOS/Godot --path . res://scenes/bv2f_arena.tscn
```

**Rebuild the Windows zip** (it re-creates the deleted working copy): `astra_test_01/burst/runs/C-9/barrow_full/tools/build_pc_arena.sh`.
