# BV2F lane LV (drax) — RESUME

**Charter:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 4, 5 (Phase 0 row 0.2), 6, 7 (DEV-4), 10. Plan § 2 C6 and § 4 Phase 0.2.
**Phase:** 0 (no image spend, $0). Write only under `runs/C-9/barrow_v2/fid/lv/` and this file. Do NOT edit `barrow_full.gd`, `barrow_v2_sw.gd`, `layout_v2.json` or any v1 file in Phase 0.

> **Gate-1 folds (charter § 12, R-C9-163) GOVERN this file.** Nothing goes into `barrow_full/godot` in Phase 0 (it builds the live Barrow page); the GDScript twin, if needed, lives in `fid/lv/`. **0.2 is decided mechanically (I-2):** the cyclic order of the six anchor bearings (from the start, on screen) matches sketch A's, each within ±15°; report the table.

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
Git: `git add -- <new paths>`, `git status --porcelain -- <paths>` before, `git commit --only <paths>`, `git show --stat HEAD` after. Never `git add -A`. Do NOT edit/commit `ledger.json` (conductor only); HALTs go in this RESUME + hand-back. Do not push.

## State
- [x] 0.2 frame fix + proof DONE (deliverables in lv/; report lv/frame_report.md). world = R_y(+47)·(x,z,y); sign tests ALL PASS (T3 exact to 1e-12 px; yaw -47 and yaw 0 rejected).
- ⚑ **HALT-for-ruling (I-2):** mechanical I-2 = **FAIL on p03 only** (Δ +59.4°; cyclic order MATCHES; other five ≤ 12.7°; similarity-fit rotation −3.2°). No yaw passes all six (best 34.3° at yaw 26.5); cause is pack p03 (8.23, 32.06, SE of start) vs sketch A's SW patch — data, not frame. Conductor rules. Also: hall/great door/gable ~90° off sketch A (layout door faces NW). LV stopped; Phase 1 not started.

---

# PHASE 1 — design freeze + blockout → M1 (opened R-C9-173; charter v0.3 §§ 5 Phase 1, 7, 12, 13)

**Inputs that govern:** R-C9-162 (M0: one sea level, wreck beached in shore ice; wreck rebuilt to read from 53°; zoom = v1's 19×13 m), R-C9-165 (hall/wreck/stair composition items), R-C9-148 (stair angled across the face, cave in the south face under p03), R-C9-154 (door sizes), R-C9-155 (clean floor, exit lanes, one great door), layout_v2 v6 + `tools/validate_layout_v2.py` R1–R13.
**Budget:** ≤ 4 Astra images (BV2F-prefixed bursts only, heavy lock, usage-limit = exit 7 HALT), ≤ $8 fal (Tripo ≈ $0.40/build; per-lane fal ledger `fid/lv/fal_spend_BV2F.json`). No painting in Phase 1.
**Write scope:** `fid/lv/` and this file; the barrow_v2 level may add NEW files in `barrow_full/godot/` only under `scenes/bv2f_*.tscn`, `scripts/bv2f/`, `data/bv2f/`, `tools/bv2f/` (list them in `fid/lv/barrow_full_allowlist.txt`). **Every v1 file is read-only** — the level EXTENDS v1 scripts. `git status --porcelain -- barrow_full/` must show only allowlisted new paths. `layout_v2.json` (v6) stays as record: write the new layout as `fid/lv/layout_v7*.json`, validated by the same validator (copy-run, R9 text noting sim-camera yaw).

## 1.2 Model kit v3 (only what C7 broke; uniform scale ≤ 10% per-axis)
- **Wreck (M0(b)):** heeled, half-sunk in shore ice, broken ribs, dragon prow, snapped mast (sketch A, `barrow_v2/sites/BV3r2-A.png`, look of record), ~12–14 m, **designed to read from 53° above** (deck, ribs, prow, mast visible from the top). One Astra concept sheet that includes a 53° top view → Tripo multiview → prep. Hull diagonal on screen as in sketch A (R-C9-165), beached at one sea level (no lagoon, no spit).
- **Barrow front + monumental door** (R-C9-154: clear opening ≥ 6.5 m H × 5 m W) and **longhall at true proportions** (no per-slot stretch; one great door ≥ 4.5 × 4.5 m in a porch rising above the roofline; collapsed SW end = the fallen gable on p06's ray, R-C9-148).
- Cliffs/crags stay modular instances (each instance will get its own bake later, W6).
- refs_guard on every prompt; no franchise/studio/artist names.

## Hall orientation — prepare BOTH for M1 (R-C9-165)
- **v7a (RECOMMENDED):** sketch A orientation — hall running screen upper-left → lower-right, the great-door wall facing the start, gable at its lower-right end on p06's ray.
- **v7b:** v6's orientation (axis 222.99°, door faces NW).
Both must keep validator R1–R13 green (exit lane door → p04 ≥ opening width; discs clear; open lines to (0,0)). If v7a cannot pass the validator, report why and stop — do not bend a rule.

## 1.3 Class-tinted guide (v1 recipe exactly, W2)
- Flat tints, one sun at v1's angle, v1's pen; **v1's own tint values** for snow / path / ice / shrub (read them from `barrow_full.gd` / v1 guide, cite file:line); new distinct tints for rock, wood, shingle, shore ice, sea, stream, **and a `char` class for charred timber/ash** (needed by the P6a overlay protocol, charter § 13).
- Models in flat class tints (not their Tripo textures). **No plants.** Path NOT a dark streak (v1's path tint).
- Rendered through the **frozen Tier-B tools** (`fid/v1tools/`, verify.sh first; run via `v1run.py`) at 100.6 px/m over the full paint envelope (≈ 11,776 × 8,704) as 1536 × 1024 tiles on the 9 × 11 grid, plus the matching ID render (per-object + class map) — for v7a only unless Matt picks v7b at M1.
- Also emit the **declared-opening list** (id, plate px, width/height m) from the layout for PH's P6a overlay.

## 1.4 M1 packet (Matt is on his phone: a few sheets + one short film, not directories)
- 12–16 play-camera stills at v1's zoom, v1 camera (pitch 52.95354°, yaw 47, frame `world = R_y(+47)·sim`): the start, each door approach (p01–p06), each spawn disc, the cave top + stair, the wreck, the mere. **Each still beside sketch A's matching area** (not to scale), and for the hall views v7a | v7b side by side.
- A labelled top-down map of v7a.
- A walkable greybox desktop app of v7a (v1's controls/camera), as at R-C9-86.
- The R-C9-165 divergence table (anchor bearings vs sketch A) as one line per anchor.
- Put the packet in `fid/lv/M1/` (sheets ≤ 2000 px wide, jpg) with `M1_README.md` listing each file in one line.

## Done when (Phase 1 DoD, charter § 5)
Validator R1–R13 green on v7a (and v7b); PH's P6 geometry agreement on the guide judged against the **layout_v7 polygons** (not the guide's own class map); Gate-2; then M1. Report to the conductor before M1 — the conductor sends the packet to Matt.

## Phase 1 state
- [x] 1.2 wreck sheet → Tripo → prep: BV2F-LV-wreck (2 image calls: 1 + 1 retry) → cells (object-cut, the painter ignored the 512 grid) → Tripo $0.40 → reduce 40k → UNIFORM normalise (`lv/tools/lv_normalise_blender.py`, yaw_fix −90): **13.0 × 4.63 × 7.46 m** (incl. mast). → `barrow_full/godot/data/bv2f/models/wreck.glb`. Reads as a ship from 53° (`lv/models/stills/wreck_gamecam.png`).
- [~] 1.2 barrow front: BV2F-LV-barrow (2 image calls) → Tripo $0.40 → uniform 25.8 m: **25.8 × 18.05 × 13.05 m, door opening measured 5.81 W × 6.67 H m** (≥ 5.0 × 6.5, R-C9-154) on `lv/models/stills/barrow_front.png`. → `data/bv2f/models/barrow.glb`.
- ⚑ **Astra Phase-1 sub-cap REACHED: 4/4 images used** (2 bursts × 2 calls; each sheet took its one allowed retry). No image left for a hall sheet.
- [x] barrow front placed in v7b (uniform; lane p02 widened to the measured 5.81 m opening + 0.5).
- ⚑ **HALT H-LV-P1-2 — the hall kit at TRUE proportions cannot satisfy R10/R11 in v7b without bending a rule, and the Phase-1 Astra sub-cap (4) is spent, so it cannot be rebuilt.**
  - Kit (BVP builds, ONE uniform scale each; `lv/models/stills/{hall,porch,gable}_dims.json`): body 30.0 × 10.17 × 10.51 m; porch 13.24 × **11.74 deep** × 10.97 m (opening 4.51 × 4.73 m — BVP's porch build is a deep gatehouse; v6 hid this by squashing it to 3.0 m, C7); gable 10.17 × 10.15 × 3.31 m.
  - Generator `lv/tools/make_layout_v7.py` searches wall offset × gable slide × porch station (v6 heading kept, R-C9-174). Result `lv/layout_v7b.json` + `lv/v7b/validator_v7b.json`: **64/66 PASS; FAIL R10** (p06 gable 13.25 m from the floor; limit 3.0) **and FAIL R11** (porch 10.97 m not ≥ hall 10.51 + 0.5).
  - Cause: the porch must cover the body's OWN door (0.21 L SW of centre — else a second visible doorway, R-C9-155 "exactly one great door"); that puts the 11.7 m-deep porch on the straight p04–p06 edge, forcing the wall 13.75 m out, and the gable (the hall's own SW end, on the same wall, on p06's ray, R-C9-148) goes with it.
  - Experiments (not v7b; `lv/v7b/exp_*.json`, uncommitted): body 28.5 m → R11 passes, R10 13.5 m; dropping the door-cover constraint → R10 4.3 m (28.5) / R11+R12+R4 fail (30). No variant is green.
  - Everything else in v7b is green: wreck (13.0 m, diagonal, bow NW, open hull to the camera, 1 m off the floor; one lane ice slab dropped per R12), barrow front, M0(a) unchanged-in-layout.
  - **Conductor options:** (1) RECOMMENDED: +2 Astra images (Phase-1 sub-cap 4 → 6) for ONE hall+porch sheet at true proportions with a SHALLOW (4 m) porch on the long wall (brief ready in `lv/tools/lv_sheets.py` `hall`), Tripo $0.40; (2) a C7 exception: the v6 per-axis porch for M1 only; (3) relax R10 for p06 to ~13.5 m.
- [ ] layout v7b, validator green (BLOCKED by H-LV-P1-2) — v7a: ⚑ **HALT H-LV-P1-1 (v7a infeasible without bending R10 / R-C9-148).** Proof `lv/v7a_feasibility.py` → `lv/v7a_feasibility.json`: anchors fixed (R1), floor = the MINIMAL disc hull + 1 m (most permissive R4 floor), R5 zero overlap, R10 ≤ 3.0 m for porch + gable; hall 18–36 m × 6.5–8 m + 6 m gable on p06's ray + grown porch on the start-facing wall, every 2° of heading. Positive control: v6's heading 222° FEASIBLE (gap 0.47 m). **Every heading with the gable at the screen lower-right end (92–180°) is INFEASIBLE; best = 12.39 m (θ 180°, screen straight down), vs the 3.0 m limit.** Cause: the oracle puts p06 screen lower-LEFT of p04 (sketch A draws it lower-right), so a door serving p04 and a gable on p06's ray force the hall's axis lower-left. No relaxed constraint was applied (R12 lane not even required). Ruling needed: v7b only at M1, OR which rule bends (R10 for p06 ≥ 12.4 m / gable off p06's ray / floor bulge). LV stopped; no images, no fal spent.
- [x] DEV-12 proposal (conductor ask): `lv/DEV12_proposal.json` (2 substitutions + class list with v1 tints cited `barrow_full_layout.json` tints_srgb; 6 provisional new tints).
- [ ] 1.3 guide tiles + ID/class render + declared-opening list
- [ ] 1.4 M1 packet
