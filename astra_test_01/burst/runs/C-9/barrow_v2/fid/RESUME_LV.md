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
- [x] H-LV-P1-2 DISPOSED by R-C9-176 (option 1: Ph1 sub-cap 4 → 6, +$0.40). BV2F-LV-hall sheet (2 calls: 1 + retry; Phase-1 images now 6/6) → Tripo $0.40 (fal total $1.20) → ONE build, body + shallow porch, uniform **32.4 m** (× 16.51 × 13.12) so the porch's own opening is **4.55 × 4.75 m** (measured on an orthographic elevation, `lv/tools/lv_measure_blender.py` → `lv/models/measure/hall_*`); porch 1.29 m proud, ridge/finials 13.12 m vs body roof 11.82 m. Gable = BVP collapsed-end build, uniform at the body depth (10.95 m).
- [x] layout v7b: `lv/layout_v7b.json` from `lv/tools/make_layout_v7.py` (copy of v6 + `BV2F-LV` changes), **validator copy-run 66/66 PASS** (`lv/v7b/validator_v7b.json`): R10 porch 1.67 m / gable 1.57 m; R11 door 4.55 × 4.75, porch 13.12 > roof 11.82 + 0.5. Hall kit placed by search (front wall 2.25 m beyond the disc hull, v6 heading). Re-run: `python3 lv/tools/make_layout_v7.py && python3 lv/tools/validate_layout_v7.py lv/layout_v7b.json`. — v7a: ⚑ **HALT H-LV-P1-1 (v7a infeasible without bending R10 / R-C9-148).** Proof `lv/v7a_feasibility.py` → `lv/v7a_feasibility.json`: anchors fixed (R1), floor = the MINIMAL disc hull + 1 m (most permissive R4 floor), R5 zero overlap, R10 ≤ 3.0 m for porch + gable; hall 18–36 m × 6.5–8 m + 6 m gable on p06's ray + grown porch on the start-facing wall, every 2° of heading. Positive control: v6's heading 222° FEASIBLE (gap 0.47 m). **Every heading with the gable at the screen lower-right end (92–180°) is INFEASIBLE; best = 12.39 m (θ 180°, screen straight down), vs the 3.0 m limit.** Cause: the oracle puts p06 screen lower-LEFT of p04 (sketch A draws it lower-right), so a door serving p04 and a gable on p06's ray force the hall's axis lower-left. No relaxed constraint was applied (R12 lane not even required). Ruling needed: v7b only at M1, OR which rule bends (R10 for p06 ≥ 12.4 m / gable off p06's ray / floor bulge). LV stopped; no images, no fal spent.
- [x] DEV-12 proposal (conductor ask): `lv/DEV12_proposal.json` (2 substitutions + class list with v1 tints cited `barrow_full_layout.json` tints_srgb; 6 provisional new tints).
- [x] 1.3 guide + ID/class render + declared openings. M0(a) folded: `lv/tools/sculpt_v7.py` is a copy of v6 `sculpt_v2.py` with one change, which removes v6's −7.8 m west moat between the beach and the shore ice. The result is one sea level, with the wreck beached in the ice (`make_layout_v7.py` imports it). v7b validator 66/66.
  - Level of v1's engine: `barrow_full/godot/scenes/bv2f_barrow_v2.tscn` + `scripts/bv2f/bv2f_level.gd`, which extends barrow_full.gd (v1 camera, sun, pen, rig, bounds); frame = the Level node = sim (x, z, y), DEV-4.
  - Data: `data/bv2f/level.json` from `lv/tools/bv2f_level_prep.py`. It has a class raster at 16 px/m, class-tinted ground meshes, models via adopt_prop with use_tex off and the class tint, and dark curtains in the declared dark openings.
  - Tints: v1's own values for v1's classes (`barrow_full_layout.json` tints_srgb). New tints are provisional DEV-2 (`lv/DEV12_proposal.json`, now including `ash`).
  - Rendered ONLY through `v1tools/godot_run.sh` (capture_blockout + capture_ids, 2×2 sections of 5888×4352 + 64 px pad; ID instrument worst 0.003 px; section-overlap MAD 0.2–0.8/255).
  - Stitch: `lv/tools/lv_guide_stitch.py` → `lv/guide/guide_v7b.png` (11,776×8,704), 99 tiles (`guide/tiles/`, 9×11, 1536×1024 / 1280×768), `ids_v7b.png`, `class_v7b.png`, `guide_manifest.json` (shas, id table, class shares).
  - Declared openings for PH (P6a overlay): `lv/guide/declared_openings.json` (`lv/tools/lv_openings.py`).
  - Re-run: `python3 lv/tools/make_layout_v7.py && python3 lv/tools/bv2f_level_prep.py && bash lv/tools/lv_guide_run.sh && python3 lv/tools/lv_guide_stitch.py && python3 lv/tools/lv_openings.py`.
  - Known: the sea-cave mouth is hidden behind the v6 cave_cliff placement in the guide (cliffs not rebuilt in Phase 1). Ground class edges step at 6 px.
- [x] 1.4 M1 packet `lv/M1/` (README lists each file): 12 stills (`barrow_full/godot/tools/bv2f/m1_stills.gd`, v1 camera + zoom) beside sketch A, the top-down map, the guide + class sheet, the divergence table, and the walkable greybox launcher (`Walk barrow_v2 v7b.command`).
  - The exported .app is NOT built: disk is at 22 GiB, and the mirror + import + export needs about 5 GB, which would cross the 21 GiB gate. The script is ready in `barrow_full/godot/tools/bv2f/build_app_v7b.sh` (builds outside the repo).
- Budget used Phase 1: Astra 6/6 (BV2F-LV-wreck 2, -barrow 2, -hall 2); fal $1.20/$8.
- NEXT: the conductor runs Gate-2 + PH P6 on the guide (against the layout_v7b polygons), then sends M1 to Matt.

## R-C9-177: M1 held; v7c + check (a)
- [x] (a) check (a) tool `lv/tools/lv_check_openings.py --render`.
  - It runs capture_ids through `godot_run.sh` with the level's opening probes in two modes: `BV2F_PROBES=with` (everything drawn) and `only` (the probes alone).
  - Results go to `lv/guide*/check_a.{json,md}`. A door facing away from the camera scores 0.
  - **v7c PASS** (6/6). **v7b FAIL** (the great door faces away; the cave is 3.7 % visible).
  - ID instrument fix: v1's capture_ids has only 256 distinct colours, so the level now groups instanced slots and blobs (one id each; 48 ids in v7c).
  - **The earlier v7b `ids_v7b.png` (308 ids) has colour collisions and is SUPERSEDED.** The v7b guide image itself is fine.
- [x] (b) layout v7c, `LV_VARIANT=v7c python3 lv/tools/make_layout_v7.py` → `lv/layout_v7c.json`; validator 66/66 (`lv/v7c/validator_v7c.json`).
  - Hall on the p02–p04 (NE) edge, found by search: wall 3.5 m beyond the hull; door faces 240.6° (SW, toward the camera and p04); porch hull gap 0.81 m; door 11.2 m from p04.
  - Gable: its own building, BVP's build at uniform 8 m, on p06's ray with a hull gap of 0.92 m; its breach faces 250°.
- [x] (c) sea cave (v7c): the cave_cliff instance is TRIMMED (it stood as a 13.5 m wall in front of the mouth).
  - 6 cliff-foot rocks are cleared from the mouth's front.
  - The dark curtain now sits on the terrain face. Mouth visibility is 54.8 % of unoccluded. The stair is unchanged.
- [x] (d) stills re-framed on the hero object, him at the disc edge (`lv/tools/lv_m1_spec.py`; `m1_stills.gd` `aim_uv`): 14 stills per variant.
- [x] (e) guide + ID re-rendered for v7c only → `lv/guide_v7c/` (99 tiles, ids/class maps, declared_openings.json). M1 packet rebuilt (v7c, plus a v7c|v7b|sketch sheet for the hall and gable).
- Data: one dir per variant, `barrow_full/godot/data/bv2f/{v7b,v7c}/` (env `BV2F_VARIANT`, default v7c). No .app export (disk); the .command launcher is kept.
- Re-run v7c: `LV_VARIANT=v7c python3 lv/tools/make_layout_v7.py && python3 lv/tools/validate_layout_v7.py lv/layout_v7c.json && python3 lv/tools/bv2f_level_prep.py lv/layout_v7c.json && LV_VARIANT=v7c bash lv/tools/lv_guide_run.sh && LV_VARIANT=v7c python3 lv/tools/lv_guide_stitch.py && LV_VARIANT=v7c python3 lv/tools/lv_openings.py && LV_VARIANT=v7c python3 lv/tools/lv_check_openings.py --render`
- [x] R-C9-178 (PH P6 findings), v7c only.
  - Braziers get a primitive stand-in (no GLB). Standing stones and grave markers are seated on the terrain; outcrops keep the generator's own seating.
  - cliff_faces moved out of the terrain face. Outcrops 3, 6, 7, 9, 12 and 13 dropped: centre outside the paint envelope (`layout_v7c.json` `v7c_r178`).
  - Check (a): one faces-camera rule (`lv_openings.faces_camera`); the probe numbers stand (hall door 6.35 m²; PH's 8.22 is the curtain box).
  - Guide/ID re-rendered (43 ids), check (a) 6/6, validator 66/66, v7c stills and M1 sheets refreshed. Next: PH re-measure.
- [x] R-C9-180 W2: `lv/placed_fit_v7c.json`, from `barrow_full/godot/tools/bv2f/export_fit.gd` with `BV2F_VARIANT=v7c`.
  - Contents: per-instance fit scale and anisotropy (max/min axis), plus each instance's scene footprint and height, for PH's P6′. The level now tags every placement with `bv2f_fit` metadata.
  - Honest anisotropy: the kit-v3 heroes are 1.00. These exceed 1.10, all v6-era per-axis fits that Phase 1 left unchanged:
    - circle stones 1.7–4.6; standing stones 2.1–2.4; grave markers 1.98;
    - outcrops 1.15–1.77, except outcrop 14 at 1.08;
    - beams: palisade 8.9–14.1, logs 4.5–10.1.
  - Placements unchanged until P6′.
- [x] W4: `lv/M1/M1_cover.jpg` (`lv/tools/lv_m1_cover.py "<P6' text>"` refills the slot) + README top.
- [x] R-C9-181 (P6′ RED fix): 142 instances changed.
  - Uniform scale for 31 box instances; 111 beams made procedural; logs re-seated.
  - Slots derived from the models; no x,y position moved this round (z only: logs, circle stones).
  - placed_fit_v7c.json refreshed: max anisotropy 1.001; longhall `r11_regions` porch 13.12 vs body 12.14.
  - Guide/ID re-rendered; check (a) 6/6; validator 66/66; v7c stills and sheets refreshed; cover P6′ slot left empty.

---

# PHASE 1′ — ART-FIRST BLOCKOUT (Matt R-C9-185; charter v1.0 § 15 GOVERNS)

**The arena spec is retired for the scene.** No anchors, no discs, no layout_v2/v7 validator, no exit lanes, no clean-floor rule, no site rotation. Build barrow_v2 **the way v1 was built**: author the layout directly in v1's camera-aligned frame with v1's own layout practice (`barrow_full/tools/make_layout.py` → `barrow_full_layout.json` — read both first; mirror their structure), then the v1 blockout (`barrow_full.gd` greybox recipe: real models in flat `hero_grey`/class tints, primitives darker, four flat ground tints + new classes, one sun 55° upper-left, ink on).

**Target:** a COMPACT site about v1's footprint (~55–65 m across) composed from **sketch A literally** (`barrow_v2/sites/BV3r2-A.png`; spawn sheet only for where things are, not as constraints):
- W: the wreck heeled and half-sunk in shore ice, prow up (kit-v3 wreck), broken ribs, snapped mast; ice floes and open sea beyond.
- SW: the sea cave in the cliff face with the straight open-sided stair climbing from a sea-level ledge to the clifftop (R-C9-148's stair, sketch-A placement).
- N: the barrow mound with the monumental carved door (kit-v3 barrow front), the stream running down from it to the frozen mere (NW).
- Centre: the start, a small broken weathered stone ring nearby (v1's stones, uniform scale), snow floor.
- E: the burnt hall **as sketch A draws it** — long side and great door facing the start, palisade around — kit-v3 hall (uniform scale).
- SE: the fallen gable as its **own** ruin (kit gable), palisade, bare trees.
- Cliffs/crags along the S coast as modular instances (uniform scale, rotation only), shrub/heather zones as tint only (no plants).
**Judge the composition at the play camera**, screen by screen: every hero (wreck, cave+stair, barrow door, mere, ring, hall door, gable) should read in a v1-zoom screen with neighbours visible, as v1's screens did. Distances are chosen for that, not for any arena.
**Rules that still bind:** principle 3 (every real model ONE uniform scale, anisotropy ≤ 1.10; procedural pieces at true dims); no plants in the guide; v1 tools only through `fid/v1tools/godot_run.sh`; v1 files read-only, new files only in the allowlisted bv2f paths; budget 0 images (if a kit piece is genuinely missing, HALT to me — ≤ 2 images from reserve need my ruling).
**M1′ packet** (`fid/lv/M1p/`): one cover screen (≤ 3 asks, one recommendation each), 10–14 play-camera stills each beside the matching sketch A area, a labelled map, the guide sheet, a `.command` walk. Report check (a) (entrances visible from the camera) as INFO only.
**Ask PH** (via files/hand-back to me) for P6′ presence/placement/scale vs YOUR blockout as geometry of record (extent retired).

## Phase 1′ state
- [x] read v1's make_layout.py + barrow_full_layout.json; `lv/art/layout_bv2art.json` in v1's (u, v) frame from `lv/tools/make_bv2art.py` (sketch A px → (u, v) at 24 px/m); kit inventory `lv/art/kit_inventory.json` (nothing MISSING); `lv/art/frame_grid.bv2art.json`
- [x] blockout level (`data/bv2f/art/`, `BV2F_VARIANT=art`, now the default) + guide/ID/class via godot_run.sh → `lv/guide_art/` (25 tiles, 5×5); declared openings; placed_fit_bv2art.json (max anisotropy 1.0001)
- [x] composition pass at the play camera: 12 hero-framed stills; hero coverage 7/7 PASS (`lv/M1p/hero_coverage.*`); check (a) INFO 6/6 visible
- [x] M1′ packet `lv/M1p/` (README lists each file). Next: PH P6′ presence/placement/scale vs layout_bv2art.json + placed_fit_bv2art.json + guide_art/ids_art.png; Gate-2; M1′ to Matt.
- Note: `lv/guide_art/tiles/` holds stale 9×11-grid tiles from a first stitch (my `rm` was denied; untracked PNGs). The real tiles are in `lv/guide_art/tiles_5x5/`.

## Phase 1′ additions (re-scope Gate-1 folds, charter § 15.1, R-C9-186) — GOVERN
- **FIRST STEP (I-5):** (a) kit inventory against sketch A's features, each marked {kit-v3 / R-C9-155 build (cavecliff, staircliff, cliffplain, crag) / v1 piece (stones, groves) / procedural (palisade, stream) / MISSING}; (b) a top-down 2D footprint fit at current scales into ~55–65 m. Hall 32.4 m + barrow front 25.8 m + wreck 13 m is tight: a UNIFORM kit rescale is allowed (no door-size rule binds now) — record scale per instance. MISSING items or a non-fit → HALT to me.
- **Frame:** write `fid/v1tools/`-compatible `frame_grid.bv2art.json` (via `--frame-grid`/`$BV2F_FRAME_GRID`); author bv2art in v1's camera-aligned frame; do NOT inherit `bv2f_level.gd`'s sim→R_y(47°) Level frame (DEV-4 retired).
- **Emit** `declared_openings.json` (every doorway/opening the scene is meant to have) and a `char`/`ash` class in the class map (P6a needs both), plus `placed_fit_bv2art.json` (per-instance scale + anisotropy).
- **DONE (W-3):** P6′ presence/placement/scale PASS vs layout_bv2art.json; hero-coverage table from the ID render of the M1′ stills (7 heroes: wreck, cave+stair, barrow door, mere, stone ring, hall door, gable — each in ≥ 1 still with ≥ 1 neighbour hero visible); measured footprint (u and v world-metre extent) vs ~55–65 m; declared openings + char class emitted; then Gate-2; then M1′.
- **M1′ cover asks (≤ 3, one recommendation each):** include "burnt hall: closed sides except the great door (recommended) or open-sided ruin".
- [x] P6′ presence fix (PH §§ 21–22): crag #2 and log #3 moved onto the beach shingle; slope stone #4 moved into the envelope. Re-rendered: guide/ID, placed_fit_bv2art, hero coverage 7/7, stills, M1′ sheets. Next: PH re-run.

## R-C9-188/189 (Matt M1′ pass): the sea-cave route, the hall closed, walkability — state
- [x] **Route** (`lv/tools/make_bv2art.py` ROUTE + `route_geometry`): rock SHELF flat at −5.0 (sea −6), flush with the cave floor, from the mouth to the stair foot, 6.2–8.4 m wide; STRAIGHT stair across the S face, 28 risers 0.179 m / 27 treads 0.27 m = 33.5°, 5.5 m wide (≥ 5.25 clear), open to the sea, flush top landing (plate at 0) onto the clifftop; cave mouth 6 × 7 m clear under a procedural rock hood (brow 1 m thick, top +3; cheeks; back) — in the `cliff_faces` id (no new id, v1's ID order kept). Walk surface: terrain HeightMapShape3D south of v −8.5 (v1's box floor north of v −9, its box under the start still centred at the origin), the stair a ramp through the nosings, the landing a plate. Bounds run −9.5..+3 with inner lip walls (open at the landing).
- **Where:** the stair TOP stays at sketch A's stair top (path end); the flight runs EAST down the face to the shelf and the cave (mouth u 6.4). Sketch A's own cave spot (u ≈ −9) needs the 3 m brow drawn inside the pilot tiles — the cave sits at the stair's foot instead (reported).
- [x] **Hall closed** (`HALL_PANELS`, `bv2f_level.gd _build_hall_panels`): the kit build's +X gable end (SE, toward the fallen gable) was an open burnt frame — a plank panel in the build's local metres closes it (rides the hall's uniform scale). Long sides closed (model views). The burnt ROOF stays open between rafters (sketch A draws it so) — reported, not a side.
- [x] **Walkability** `lv/tools/lv_walkability.py` + `barrow_full/godot/tools/bv2f/walk_check.gd` → `lv/walk/` (walkability.md/json, route_topdown.png, route_play.png): PASS 8/8 — continuous (559/559 samples), stair 33.48°, shelf 0°, max dz 0.033 m vs v1 step height 0.103 m (capsule r 0.35, floor_max_angle 45° default, no step-up in knight.gd), stair ≥ 5.25 m, shelf ≥ 6.15 m, mouth 7.00 m headroom, v1's knight driven cave → clifftop in 17.6 s.
- [x] **Pilot guard** `lv/tools/lv_pilot_guard.py --before <ref copy>` → `lv/art/pilot_guard.json`: SAFE — every changed heightfield/class cell, block, curtain, hood box and dropped cliff face projects at guide y ≥ 2599.6 (pilot ends at 2560).
- ⚑ **HALT (pilot tiles):** `lv/tools/lv_pilot_tiles.py` → `lv/art/pilot_tiles.json`: 7/9 identical; **r01_c02 and r02_c02 moved, ONLY at the guide knight** (all pilot-window diffs inside x 3303–3512, y 1690–1854 = him at the start). Control: the SAME current scene rendered twice (`lv/guide_art/ctl_s01/` vs `s01/`) differs by 2939 px there — his idle pose depends on frame timing (frozen capture: physics-callback animation, timing-dependent physics steps before freeze_pose). Not geometry. Ruling needed: accept / repaint those 2 chunks; and whether to make the guide knight's pose deterministic (changes those 2 tiles once more). PT's pinned guide copy is untouched.
- Refreshed: guide/ID/class (godot_run.sh), declared openings (cave 6 × 7 m), placed_fit_bv2art (89 inst., max aniso 1.0001), check (a), M1′ stills + hero coverage, stills/map/guide sheets.
- [x] **R-C9-191** (HALT disposed: the pilot paints from PT's pinned copy, no repaint; route accepted). The guide's scale knight is now DETERMINISTIC: `bv2f_level.gd freeze_pose` freezes him on ONE fixed frame (idle clip, t 0, off the AnimationPlayer; tree + foot-lock IK set aside). Proof: three s01 renders pixel-identical. Full guide re-rendered via godot_run.sh; new pins `lv/art/guide_pins_phase3.json` (guide, ids, class, 25 tiles). Pilot vs PT's pinned copy: r01_c02 + r02_c02 differ ONLY at the knight (9573 px, bbox 3303,1690–3518,1864); ids/class there 0 px — recorded KNOWN AND INERT. PT's copy untouched. Standing by.

## PHASE 1″ (Matt R-C9-204/206, plan R-C9-205) — coast, water, paths, cave + stair → M1″
- [x] **Cliff kit** (`lv/briefs/BV2F-LV-{cliffcol,cliffcape,cavearch,seastack}`; identity = sketch A crops bvm_rocks/bvm_cliffs): 4 Astra images (1 call each, 0 retries) → Tripo ×4 ($1.60; fal ledger 2.80 / phase cap 5.20) → reduce → ONE uniform scale (lv_build normalise; cape yaw_fix +90). Cave mouth measured on the build (`lv/tools/lv_kit2_measure.py` → `lv/kit2/cave_mouth.json`).
- [x] **make_bv2art.py Phase 1″** (+ `bv2pp_coast.py`): plateau 0; W shingle beach 10 m (6 m N) down to shore ice −4.2, wreck re-seated there; sea −4.5; curving S lip (bays/headlands), crest +1.5..+3.4 → sea cliffs 6.3–7.9 m; kit columns/capes 1 m proud of the snow + a rock skirt behind (raw heightfield face not drawn), talus, 3 stacks. Route in sketch A's order (cave W, stair E): cave arch 7.3 m clear at its lip (knoll ~4 m over the clifftop), sea-worn shelf (irregular edge, boulders, rime), 33 rough rock-cut treads in a notch (kit columns on the cut wall), open sea side, flush landing. Mere: organic outline, 24 cracked plates over dark water; stream: channel + snowy banks + ice; sea ~65 % ice (shore-fast / plates / floes, 36 tagged to bob). Paths removed (class + geometry). Slope stone #7 removed (it stood on the new stair).
- [x] bv2f_level.gd: slab groups (one id per group), trimesh colliders for the kit (cave: walls only above its rubble), smooth ground normals, heightfield walk floor everywhere.
- [x] Walkability PASS 8/8 (stair 34.17°, shelf 0°, max dz 0.034 m vs step 0.103, stair ≥ 5.45 m, shelf ≥ 6.25 m, mouth 7.34 m, knight cave → clifftop 22.4 s). Guide/ID/class re-rendered (godot_run.sh); declared openings; check (a) PASS 6/6; placed_fit 102 inst., max aniso 1.0001; hero coverage (M1″ heroes) 8/8.
- [x] **M1″ packet** `lv/M1pp/`: cover (3 asks), stills A/B (8, beside sketch A; 04/05 = cave + stair), cross-sections, map, guide. Pilot tiles: all 9 are repainted from this guide per R-C9-205 (no pin to hold).
