# BV2F lane LV (drax) — RESUME

**Charter:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 4, 5 (Phase 0 row 0.2), 6, 7 (DEV-4), 10. Plan § 2 C6 and § 4 Phase 0.2.
**Phase:** 0 (no image spend, $0). Write only under `runs/C-9/barrow_v2/fid/lv/` and this file. Do NOT edit `barrow_full.gd`, `barrow_v2_sw.gd`, `layout_v2.json` or any v1 file in Phase 0.

## Phase 0 task: 0.2 the frame fix (DEV-4)
Problem (C6): layout_v2 and sketch A are composed for a **yaw-0** camera (`layout_v2.json` ~L21-38); R-C9-159 kept that frame and turned only the camera to 47° (`barrow_v2_sw.gd:11`), so every door, the cave mouth and the coast are seen 47° off sketch A's composition.
Fix: place the site in v1's world **rotated by the camera yaw**: `world = R_y(47°) · sim` (sim (x, y) → world (x, 0, y) on the flat floor, then rotated). Camera, heather card basis (`barrow_heather.gd:43-45`), suns, snow and pen stay untouched — v1 authored its own layout in camera-aligned (u, v).
Deliver:
1. ONE function/module holding the transform (`fid/lv/frame.py` + a GDScript twin if needed), with the sign **proven** by a two-anchor test (e.g., p02 must appear screen-up of the start; p01 screen-left) — tests in `fid/lv/test_frame.py`, output recorded.
2. A play-camera render (overhead of the whole site at v1's pitch/yaw, unpainted, markers only is fine) of the six anchors + floor polygon + key features (wreck, cave mouth/stair, hall door, gable, barrow door, mere, stream, coastline), and a side-by-side overlay against sketch A's screen positions (`barrow_v2/sites/BV3r2-A_spawns.png`, not to scale — topology and orientation only). Save to `fid/lv/frame_proof/`.
3. A short `fid/lv/frame_report.md`: the transform, the test output, the overlay, and any feature whose orientation still disagrees with sketch A.
Also note (for Phase 1, do not do yet): R-C9-162 M0(a) removes the west lagoon (-1.3 m) and its spit — one sea level, wreck beached in shore ice. List in the report which layout_v2 entries and validator rules that will touch.

## Constraints
Heavy lock for Godot runs: `python3 runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>`. Disk gate 21 GiB. Matt runs deletions. Never work around a permission denial.
Git: `git add -- <new paths>`, `git status --porcelain -- <paths>` before, `git commit --only <paths>`, `git show --stat HEAD` after. Never `git add -A`. Do NOT edit/commit `ledger.json`. Do not push.

## State
- [ ] 0.2 frame fix + proof
