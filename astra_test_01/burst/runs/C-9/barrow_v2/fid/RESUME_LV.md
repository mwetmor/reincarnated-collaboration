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
- [x] **R-C9-208** (M1″ held, 0 images): stair re-laid ACROSS the face, built out seaward of the lip (cliff-kit wall behind, open to the sea, 24 risers × 2–3 rough blocks, 33.3°, 5.4 m clear); cave in a rock HEADLAND (clifftop +5.6 over it) with a dark plane 2.6 m inside the arch; sea ice = broken pack (merged Voronoi plates of every size/freeboard, snow rims, pressure ridges, brash, varied leads; ~70 %); mere = continuous ice ground with thin cracks + seams, stream ice 2 cm cracks; raw heightfield faces hidden, the cliff skirt and stair side are continuous ribbon walls (no slats). Walkability PASS 8/8, check (a) PASS, hero coverage PASS, placed_fit max aniso 1.0001; M1″ stills incl. 09 close stair + cave.
- [x] **R-C9-209/211 + P6′ 761a48353**: stair broken into rough boulder steps (3–5 per row, staggered fronts, varied height, cracks, snow lips) with rock spurs/boulders both sides; shelf = wave-cut platform east of the pilot line (t ≥ 4: lobes/bays, ragged rim, low ribs, frozen potholes, boulders), its M1″ outline kept west of it (pilot pin); separate RNG so nothing else moves. Fallen ring stones re-seated on the terrain; wreck in a shore-ice cradle (beach no longer clips it), hidden-by-design 34.4 % of vertices below the ice top (layout). Walkability PASS 8/8 (shelf ≥ 6.2 m), check (a) PASS, hero coverage PASS, placed_fit 1.0001. Pilot tiles: 3 identical, 6 moved (wreck + stones) → `lv/art/pilot_tiles_209.json`; PT re-pins.
- [x] **R-C9-212**: whole shelf natural (rounded W end, lobes/bays, ragged rim, rubble ribs, potholes, boulders; back runs under the face); headland face behind the shelf = rock-kit columns/capes (no ribbon wall there). Walkability PASS 8/8, check (a) PASS, hero PASS. Pilot tiles: r00 identical, 6 moved → lv/art/pilot_tiles_212.json.
- [x] **R-C9-212..223 pass** (0 images): cave section CARVED from one rock mass (`lv/tools/bv2pp_carve.py`: terrain SDF eroded, minus a sea-cut COVE in the existing cliff, the CAVE in its back wall (7.2 m clear, tunnel to a dark end), the iced LANDING (tide_ice), the STAIR as a 5.3 m groove cut in the cove's east wall with a low broken lip; tidal wet band + rime + icicles + cove ice; shelf + route kit removed; walk height `terrain_walk_h.f32`); ring = 6 even positions, 4 standing (lean, snow caps) + 2 fallen low blocks with drifts; treads exported `lv/art/stair_treads.json` (PT snow); stream dropped; river down the coast (narrow, cracks only); mere ~300 m² with reed islands, cracks over the whole polygon (cause of the old two-edge cut: the R-C9-208 headland's box ease buried the mere's SE ice); mere -> sea one graded field (ice/ice_mid/shore_ice, widening leads); barrow larger, kerbed (v1 profile), kerb stones. Walk 8/8, check (a), hero coverage PASS. Pilot tiles all moved -> `lv/art/pilot_tiles_223.json`.

---

# HANDOVER — state at 8ab6484c7 (drax LV stands down; a fresh LV lane continues from here)

## Where things stand (R-C9-212 .. R-C9-223, all in commit 8ab6484c7)
| Ruling | State |
|---|---|
| R-C9-212/213/214 cave section carved, subtractive | DONE: one eroded rock mass (`bv2pp_carve.py`); sea-cut COVE in the existing cliff (coast outside it unchanged); CAVE in the cove's back wall (lip clear 7.18 m, tunnel 5.5 m to a dark plane); iced LANDING (`tide_ice`) >= 5.6 m deep; STAIR = 5.3 m groove in the cove's east wall, 24 risers 0.25 m / 0.38 m treads (33.3 deg), low broken uncut lip (0.5 m); tidal `wet_rock` band below high water (SEA_Z+1.6), `rime` line, icicle slabs, cove ice; shelf + all route kit pieces removed. Left-shoulder push NOT done (R-C9-214 superseded it). |
| R-C9-215/216 ring + treads | DONE: 6 even positions on the old ring's centre/mean radius; 4 standing (v1 stones, lean 2.5-4.5 deg, snow caps), 2 fallen as low procedural blocks (<= 0.42 m proud) + snow drifts, no buried volume. Tread tops = `snow` class; outlines/heights exported `lv/art/stair_treads.json` (uv) for PT's 3D snow. |
| R-C9-218/220/222/223 water | DONE: barrow stream DROPPED; RIVER (`RIVER_UV`) down the coast, narrow (hw 0.7, widens 1.2 into the mere), continuous ice + thin cracks/seams, no block ice. MERE ~301 m2 (`MERE_SHAPE`), reed islands (shrub-class tussocks), cracks over the whole polygon. |
| R-C9-221 mere -> sea | DONE: beach cells within 7 m of the mere (v > 6.8) become one graded ice field: classes ice -> `ice_mid` -> shore_ice down the slope, crack lines widening into dark leads (`trans_leads`), reed islands + snowy low rocks; meets the legacy sea pack seamlessly. |
| R-C9-222 barrow | DONE: kerbed dome (v1 profile `(1-rho^2)^0.35`, kerb over outer 8 %), centre px (828,-84) semi 17 x 10.4 m rise 6.5, runs off the top edge; kit-v3 front 15 m wide (uniform); kerb stones (v1 stones) round the visible arc; slope stones inside the mound/mere dropped. |
| P6' 6c00e6d53 fallen stones | superseded by R-C9-216 (fallen = low blocks). PH should re-run P6'. |
| Pilot | ALL 9 pilot tiles changed -> `lv/art/pilot_tiles_223.json` (before = M1''-pass render). Conductor: the pilot is repainted from this guide. |

## Known issues (open)
1. RIVER mostly above the paint window's top edge (v > 22.37); only ~4 m shows. Fix = route it lower/further east of the shore, or shrink the mere's NW lobe.
2. Stair GROOVE treads still read as light stripes in the flat-tint guide (tread tops snow vs risers rock at 0.2 m voxels). Options: finer voxel step in the groove (0.1 m), more tread-front wobble, or blocky tread breakup in the SDF.
3. MERE edge cut straight near the cove: the carved block's footprint (CARVE t/s box) overlaps the mere's S edge; its top faces take the class raster but the box edge shows. Fix = shrink CARVE["s"][0] (inland bound, now -12) or clip the footprint to an organic mask.
4. MERE ~301 m2 vs ruled 400-500 m2 (kept smaller so the coast-side river fits in frame). Needs a Matt/conductor call with item 1.
5. Cove reads partly enclosed from the camera (back wall tall under the headland); check (a) PASS on the mouth (21.5 m2 visible, 100 % of unoccluded).
6. `lv/guide_art/tiles/` holds stale 9x11 tiles (rm denied earlier; Matt runs deletions).

## How to rebuild (all from `barrow_v2/fid/lv/`; heavy lock + disk gate >= 21 GiB for every Godot step)
1. LAYOUT + terrain + carved mass: `python3 tools/make_bv2art.py` -> `art/layout_bv2art.json`, `../../../barrow_full/godot/data/bv2f/art/{level.json, terrain_h.f32, terrain_walk_h.f32, classes.png, classes_png.bin, carved_<class>.f32}`, `art/stair_treads*.json`. Composition constants at the top (ROUTE, CARVE, MERE_SHAPE, RIVER_UV, CHANNELS, MOUND/BARROW, RING_STAND). The carve (SDF + marching tetrahedra, numpy only) is `tools/bv2pp_carve.py` (cove/cave/stair cutters, classes per triangle); coast/ice geometry helpers `tools/bv2pp_coast.py`. Random streams: `prng` (legacy, keep its draw order), `rng209` (route), `rngw` (water) — new features should get their own stream so nothing else moves.
2. Godot side: `barrow_full/godot/scripts/bv2f/bv2f_level.gd` (`_build_carved`, `_build_slabs`, `_build_ribbons`, tilt support `tilt_up_local`, walk height from `walk_file`, guide-knight fixed pose `freeze_pose`).
3. GUIDE/ID/CLASS: `LV_VARIANT=art bash tools/lv_guide_run.sh s00 s01 s10 s11 && LV_VARIANT=art python3 tools/lv_guide_stitch.py` (frozen Tier-B tools via `fid/v1tools/godot_run.sh`) -> `guide_art/` + `guide_art/tiles_5x5/`. Pilot shas: `shasum -a 256 guide_art/tiles_5x5/guide_r0[0-2]_c0[0-2].png`; geometric pre-check `tools/lv_pilot_guard.py --before <copy dir>`.
4. Openings / checks: `LV_VARIANT=art python3 tools/lv_openings.py`; check (a) `LV_VARIANT=art python3 tools/lv_check_openings.py --render`; placed_fit `python3 tools/lv_placed_fit.py`.
5. WALKABILITY: `python3 tools/lv_walkability.py` (drives `barrow_full/godot/tools/bv2f/walk_check.gd`) -> `walk/walkability.md|json`, `route_play.png`, `route_topdown.png`. Bars: continuous, stair <= 35, landing <= 10, riser <= 0.103 m (v1 step = capsule r 0.35 x (1-cos 45)), stair >= 5 m, landing >= 5 m, mouth ~7 m, knight driven cave -> clifftop.
6. STILLS + M1'' sheets: `python3 tools/lv_m1pp_spec.py`; then in `barrow_full/godot`: `BV2F_VARIANT=art [M1_IDS=1] python3 ../../../C-7/conductor_scripts/heavy_lock.py C-9 -- Godot --path . --resolution 640x360 --script tools/bv2f/m1_stills.gd -- --out ../../barrow_v2/fid/lv/M1pp/stills_raw --spec ../../barrow_v2/fid/lv/M1pp/stills_spec.json` (ID pass first, normal pass last); `M1DIR=M1pp python3 tools/lv_hero_coverage.py`; `python3 tools/lv_m1pp_packet.py` -> `M1pp/M1pp_{cover,stills_A-C,section,map,guide}.jpg`. Quick 2D check: `PLAN_PPM=12 python3 tools/lv_plan2d.py u0 v0 u1 v1`.

## Must know
- The heavy lock is shared with other runs (JOIN-1 etc.); Godot steps can queue for many minutes.
- `*.f32`, `*.bin`, `classes.png`, `ext/`, `models/` under `data/bv2f/` are git-ignored (regenerable by step 1 / lv_build normalise); PNGs under astra_test_01 are ignored too.
- New guide classes (provisional tints in make_bv2art): `tide_ice`, `wet_rock`, `rime`, `ice_mid` — PT/PH palette needs them.
- Never edit ledger.json; commits `git commit --only`; the conductor pushes.

---

# CONDUCTOR BRIEF for the fresh LV lane (R-C9-226) — the Phase 1″ close-out. GOVERNS.

Read the handover section above first (tools, re-run steps). Then fix exactly these, against `barrow_v2/sites/BV3r2-A.png` (sketch A, look of record), 0 images:

1. **COVE / CAVE / STAIR (the failing section).** In pass 8ab6484c7 the cove is a large flat ice pool cut into smooth snowy slopes; the walls are not rock, the cave mouth is not visible, the stair reads as plank stripes. Target, as sketch A draws it (crop around the cave, lower-middle): a **vertical eroded rock-column cliff** exactly like the cliff east of the cove (same rock-kit pieces/material, snow on ledges), with a **shallow** sea-cut cove (≤ 6–8 m deep into the cliff line, never a big basin). The **cave** is a dark wave-worn arch at the cove's back wall, **clearly visible from the camera** (check (a) on the mouth + a still); the sea and floes reach into the mouth; the **landing** is small — a ~6 m flat tide-iced ledge cut at the mouth just above the water; the **stair** is cut between rock columns on the cove's right wall from the landing to the clifftop, **individual stone treads** (each its own block: snow class on top, rock class on the front) so it can never read as stripes/planks, 5 m clear, low broken uncut lip on the sea side. Everything else about the coast outside the cove stays. Matt's rule: SUBTRACTIVE — carved from the existing rock mass, nothing added.
2. **MERE SIZE** back to Matt's ruling R-C9-220: **400–500 m²**, irregular, plated, cracks to the whole polygon. Do NOT trade it for the river — move the composition instead (see 3).
3. **RIVER IN FRAME**: sketch A's river is visible in the scene's upper-left, running down alongside the coast (a little inland from the ledge, roughly parallel) into the mere. It must lie **inside the painted window** for a clear stretch (it may enter from the top-left edge). Narrow ribbon, flat ice with thin cracks, NO block ice (R-C9-223), seamless into the mere.
4. **REED ISLANDS** are reeds, not flat olive patches: small raised snow/earth hummocks in the ice with reed/shrub class tufts on them (the 3D reed cards come from the painted tufts later).
5. **No straight edges**: the mere's edge near the cove (cut straight), and the **hall's ash yard** (a big rectangle) → irregular trampled-ash shape as in sketch A.
6. Keep: v1-size barrow with kerb stones; 6-stone circle (4 standing, 2 fallen low blocks); no barrow stream; seamless mere → sea ice transition; stair_treads.json export for PT's DEV-22.
7. **Stills sheet**: regenerate the M1″ sheets with CORRECT captions and the MATCHING sketch-A crop beside each still (the last sheet had stale captions and ring crops beside the cave stills). One close still of the cove/cave/stair beside sketch A's cave; one wide; the mere + river beside sketch A's upper-left.
8. Report: walkability, check (a), hero coverage, P6′-ready exports, the 9 pilot-tile shas.

---

# LV lane (fresh, R-C9-226) — state: brief items 1-8 DONE (0 images)

| Item | What changed |
|---|---|
| 1 cove/cave/stair | NEW `lv/tools/bv2pp_cove.py` (replaces bv2pp_carve's builder; marching tets reused): the cliff mass is VERTICAL ROCK COLUMNS (jittered-Voronoi plan cells ~1.7 m, vertical cracks, per-column snow-capped tops stepping at the edges, wave notch at high water). Shallow sea-cut COVE (back wall 5.0 m in; 7.2 m in at the stair's foot alcove); CAVE = dark arch in its back wall (7.16 m clear at the lip, tunnel 2.6 m to a dark plane, axis angled inland so its roof knoll misses the stone circle); sea + floes in the cove's W part reach into the mouth's W side; iced LANDING ~5.3 m deep in front of mouth + stair foot (5 m bar forces mouth-width + stair-width long). STAIR climbs INLAND (up-screen, risers face the camera, as sketch A) in a cleft between column walls from the cove's back-right corner: 17 risers 0.253 / 0.39 treads = 32.7 deg, 5.3 m band; every tread 3-4 separate stone slabs (`stair_treads` rock + `stair_snow` caps, bare stone nosing). The sea-side lip no longer applies (no sea side on an inland flight). ⚑ Space forced the cove ~9 m EAST of sketch A's cave (cave mouth uv (-1.7,-7.4), stair top (8.6,-3.7)): an up-screen 5 m stair needs ~6 m inland run, which ends inside the stone circle anywhere west of it. Cover ask 2. |
| 2 mere | explicit `MERE_POLY`, organic, scaled to 440 m2 on land (N lobe runs off the window top like the barrow); shore N of the wreck moved W (`SHORE_UV`). |
| 3 river | `RIVER_UV` enters the window's top-left (u ~-28), runs down ~3 m inland of the beach into the mere. |
| 4 reeds | `reed_islands` = stepped snow hummocks; `reed_tufts` (shrub) clumps on/around them. |
| 5 straight edges | carve footprint is now an organic mask (2 m blend), no box; mere far from it; ash yard irregular (lobed + opened/closed noise); mere->sea field's S limit and the shore wiggle de-straightened; old-shelf floes dropped whole near the cove (no clip line). |
| 6 kept | barrow + kerb, 6-stone circle, no barrow stream, graded mere->sea, `art/stair_treads.json` (now one entry per tread STONE cap). Pack ice re-rolled by the coast move: gaps x0.8 + fewer dropped floes -> 68 % ice. |
| 7 sheets | `M1pp/M1pp_{cover,stills_A,stills_B,stills_C,section,map,guide}.jpg`; spec carries a hand-picked sketch-A pixel of the SAME feature per still (`lv_m1pp_spec.py`). |

Checks: walkability PASS 8/8 (`walk/walkability.md`); check (a) PASS 6/6 (cave 17.4 m2 visible, 98.6 %); hero coverage PASS 8/8 (`M1pp/hero_coverage.md`); placed_fit 91 inst, max aniso 1.0001; declared_openings refreshed. Pilot tiles: all 9 changed (shas in the hand-back / `shasum -a 256 guide_art/tiles_5x5/guide_r0[0-2]_c0[0-2].png`).

New tools: `lv_guard_lock.py` (heavy_lock drop-in with pt_godot's timeout / script-error / log-cap guards; used by walkability, placed_fit, and `HEAVY_LOCK=` for godot_run.sh); `lv_quickview.py` (no-Godot software view, check only).
Open: (a) the landing is still ~60 m2 (5 m bars); (b) still 12's river is narrow at play zoom; (c) the circle's S stones now stand ~2 m from the knoll's edge; (d) stale `lv/guide_art/tiles/` + scratch dirs (Matt deletes).

## R-C9-227 + R-C9-228 (conductor/Matt M1'' notes) — DONE, 0 images
- 227(1) river = open dark water (`river_water` slabs, class sea), hw 0.5, no cracks/ice, a few bank reeds; meets the mere ice. (2) mere: Voronoi net dropped (its rngw draws kept) -> 7 random-walk branching veins incl. 2 seams (stream 2271). (3) pack: own stream 2272 -- plate weights x lognormal, gap x lognormal, edge roughness varied, 16 % rubble zones; old-shelf floes' gaps varied (2274); 71 % ice.
- 228(1) NO cove: `CARVE.cove.parts = []`, cliff kit continuous again (kit skip only where carve mask > 0.45); cave = arch worn into the corner of the face and the stair gully, facing the camera (`cave_t` 12.3, s -1.5, axis (-0.6,-0.8), cut 4 m through the face front); stair in a natural gully climbing inland from s -4.6; small iced ledge = gully floor + mouth floor (`landing_fn`), 1.45 m proud -- its size is set by the 5 m route bar (cover ask 2). (2) wreck cradle outline noisy/rounded + 5 thin cracks (`cradle_cracks`).
- Checks: walkability 8/8, check (a) 6/6 (cave 23.3 m2), hero coverage PASS, placed_fit 96 inst 1.0001. Sheets `lv/M1pp/`.

## R-C9-229 (conductor review of 5274b2dbb) — DONE, 0 images
(1) kit fills up to the carve (a piece slides back to fit; the bare skirt wall left of the cave is gone); `gully_rock` group: seastack kit pieces in both gully walls (W ones kept off the cave tunnel), two on the knoll over the arch, one flanking the mouth (trimesh colliders). (2) treads 2-4 stones of very different lengths, fronts set back 0-0.14 m unevenly; snow only in irregular patches (some stones bare); `stair_treads.json` = the patches. (3) ledge outline lobed/ragged (front + mouth lobes), 6 rocks (`ledge_rocks`). (4) mere->sea field: random-walk cracks widening W into leads + rubble (`trans_rubble`), stream 2291. Walk 8/8, check (a) 6/6, hero PASS, fit 109 inst 1.0001.
Open: carved column tops round the arch still angular; ledge rocks are stepped tiers.

## R-C9-230 — DONE: clifftop left of the cave lobed/notched (lip wiggled for t < ~7 only, pack ice still laid out against the passed lip0), 4 slumped rim rocks, kit gap-filler re-fit; east kit unchanged. Walk 8/8, check (a) PASS, hero PASS. Pilot: r00_c00-c02 + r01_c00 identical; r01_c01, r01_c02, r02_c00-c02 changed.

## R-C9-231 (P6' 78a2f41bd) — DONE: slope_stone_0 (dropped inside the kerb) removed from the layout of record; gully_col_e_1 (74 % in the wall) dropped. Walk PASS, check (a) PASS, hero PASS; all 9 pilot shas unchanged vs 1f9eb1dc7.

## R-C9-234 (conductor, on Matt's choice "Fix my 7, then gates") -- blockout fixes for the pilot area, 0 images
Base: LV 368cdf791 / geo v4. All changes in `lv/tools/make_bv2art.py` (section "R-C9-234"); every new draw has its OWN stream
(2341-2353) and every legacy stream keeps its draw count -- proof: all 52 non-kerb placements (cliffs, talus, stacks, gully
rock, ring, wreck, hall, gable, crags...) are byte-identical vs 368cdf791; pack slab counts unchanged (fast/plates/floes).
| Item | What changed |
|---|---|
| (2) reeds | octagon pads gone: islands are the GROUND raised in low lobed, elongated domes (`isl_rho`), snow on them; reed beds = clumps of thin tall blades (new class `reed`, pale straw, provisional tint) on a straw ground patch, on the islands, along the mere's W/N/S edges and the river's banks. `art/reed_beds.json` (islands + clumps) for PT's DEV-21. |
| (3) shingle | beach foot ragged (width -0..1.8 m low noise, `BW`; the foot's bays are shore ice, `bay_ice`); snow drifts over the stones (`drift`); classes from smooth bilinear fields (no 25 cm stair-steps); wreck cradle edge smooth. The pack is still laid against the passed beach (`beach0`). |
| (4) mere -> sea | ONE graded field `wG`/`b_f`: ground eases from the mere's ice to the beach foot along b (no land strip, no crease); classes ice -> ice_mid -> shore_ice by b with noisy soft limits; leads widen with b (capped, prism spans both end heights); margin islands = land showing through the ice. |
| (5) sea ice | pressure-ridge square pillars -> low irregular 5-8-sided lumps (fewer, 5-28 cm proud); every floe/plate drawn with corners worn round (one corner-cut pass; legacy outline kept for rims/brash draws). |
| (6) barrow | front LOBE (v1 profile, kerbed) round the door, unioned with the big dome; a cutting the portal's width to the build's front face, the lobe kept out of the build's own footprint (glb verts), dry-stone walls (`barrow_cutting` slabs); eases to 0 within 1.6 m of the mere. Kerb re-run round the union (kerb_stone ids renumbered). `barrow_front.burial_by_design` declared (its back/roof under the mound by design). |
| (7) wreck | `wreck_mast` slot: procedural mast stub (6.2 m, 0.38, leaning 16 deg up-screen right) + fallen spar from the gunwale onto the ice. |
| extra | river = ground `sea` class along its channel (the stepped prisms were the top-left zig-zag notch); fallen ring stones = weathered lumps (same footprint/height; PT's 2_1 "greybox remnant"). |
New tools: `lv_pilot12_sheet.py` (before|after sheets of the 12 P11 views), `lv_p6prime_run.py` (PH's own P6' harness, output redirected to `lv/art/p6prime_lv/`, PH's record untouched). Stills: `M1pp/pilot12_{before,after}/`, `M1pp/pilot12_sheet_{A,B,C}.jpg`, spec `M1pp/pilot12_spec.json`.

## R-C9-238 (conductor review of aab3357eb) -- one more blockout pass, 0 images
| Item | What changed (make_bv2art.py, "R-C9-238") |
|---|---|
| (a) shingle | the noise bands are gone: ONE continuous shingle beach (ragged foot, ice bays kept); snow only as a thin ragged rim at the top + SMALL wind-shaped drifts (tapering tongues, wind from the W/NW) in the lee of the wreck and the margin's rocks + ~70 small scallops (own stream 2381/2382). |
| (b) leads | the branching-tree lead prisms are dropped (their draws still run, so the rubble stays): the margin is broken into FLOES (Voronoi, ~4 m by the mere -> ~1.6 m at the sea, warped edges), the leads are the gaps BETWEEN them (closed by the mere, opening narrow -> wide toward the sea, some edges shut), floes rounded into pancakes where b > 0.42; each floe one ice tone. Drawn in the ground as the NEW class `lead` (sea tint) -- its own id `ground_lead` (a second `ground_sea` mesh left those pixels unassigned in the class map). |
| (c) steps/ripples | the written terrain is 8 px/m (`HF_OUT`): a cubic spline through the 25 cm grid clamped to each cell's min/max (no overshoot); all placements/classes still read the 25 cm grid (nothing moved). The margin's teeth were a sign flip on the 25 cm land mask (sd_shore smoothed) and a crease at the mere's edge (profile now leaves the ice with zero slope). |
| (d) wall end | the cutting's walls are runs of separate irregular stones (5-8 sides, 0.35-0.75 m) whose tops follow the mound; each wall ends in a falling run of low stones + 2 tumbled ones (own stream 2387). |
Gates: walkability PASS 8/8, check (a) PASS 6/6, P6' PASS (`lv_p6prime_run.py`; placements identical to aab3357eb), placed_fit max aniso 1.0001, class map 0 unassigned px. Stills: `M1pp/pilot12_before_238/` (= aab3357eb), `M1pp/pilot12_after/`, `M1pp/pilot12_238_sheet_{A,B,C}.jpg`; tiles `art/pilot_tiles_238.json`.

## R-C9-239 (narrow pass on d779796d3: three residuals, nothing else changed) -- 0 images
(1) mound cutting edges: the build's footprint is now a SOFT edge (blurred distance, 1.5 m ease) instead of a hard 25 cm mask; the cutting's sides ease over 1.8 m (smoothstep) and its mouth over 0.8 m -- no sawtooth diagonal; the dry-stone wall tops follow the eased mound. (2) the margin's floe gaps close within ~1.3 m (noisy) of the field's own edge -- the dark sawtooth wedge along the shingle foot by the wreck is gone (the same rule also closes two small edge gaps at the far NW, tile 0_0). (3) shingle drifts = 3 overlapping soft ellipses shrinking downwind (rounded head, scalloped tail), no points. Placements and every other slab group identical to d779796d3; walkability 8/8, check (a) PASS, P6' PASS, placed_fit 1.0001, class map 0 unassigned. Stills `M1pp/pilot12_before_239/` (= d779796d3) | `M1pp/pilot12_after/`, sheets `M1pp/pilot12_239_sheet_{A,B,C}.jpg`; tiles `art/pilot_tiles_239.json` (2_1, 2_2 identical).

## R-C9-244 (pilot repaint 3 blockout, from 5a07c024f) -- 0 images
(a) HEATHER (v1 practice: shrub zones x patch noise, class `shrub` = PT's ground_shrub): zones = the mound's flanks/top + a band round its foot, outside the stone circle, the cliff tops, the shingle back; two-scale clump noise (~40 % cover in a zone's core, snow between); only on snow/mound cells on land; never the mere (+1.2 m), the river, the margin, the cutting/door approach, the stair cleft/pad, the start (3 m). Cover (class raster): pilot window 76 m2 of 459 m2 snowy land = 16.5 %; whole paint window 142 m2 / 1564 m2 = 9.1 %. (b) the standing stones' snow-cap prisms removed (clean-cut tops; fallen-stone base drifts kept). (c) floe-edge cubes: pressure-ridge lumps, rubble-zone pieces and brash are irregular low shards (`shard()`, streams 2352/2445/2444); legacy draws AND legacy outlines kept for the brash mask, so nothing after the pack moves. (d) mound: lobe rise 6 -> 7 m and only the build's front 1.8 m kept clear (its back/roof under the mound, burial_by_design, terrain-hidden 0.37); a stone kerb band (class rock) on the union's kerbed rim; heather on the mound. Placements identical to 5a07c024f. Gates: walk 8/8, check (a) 6/6, P6' PASS, fit 1.0001, class map 0 unassigned. Sheets `M1pp/pilot12_244_sheet_*`, tiles `art/pilot_tiles_244.json`.

## R-C9-257 (pilot repaint 4: the shore-ice bay at the shingle foot, from 03306a599) -- 0 images
The flat pale "bay" at 0_1/0_2 (plate x~1250-1400, y~1792) was the wreck's shore-ice CRADLE cut into the shingle east of the stern; its shingle-side edge lay on the row-1/row-2 paste strip. On the beach, at the stern half only (wl > 0.5 m, eased), the cradle now holds only deep on the slope (d_shore > ~5.3 m, noisy) or within ~0.5-1.3 m of the hull: its edge there now projects at plate y ~1850-2000 (row 2 only), the shingle running down to it. The ice is no flat plate: soft tone patches (shore_ice/ice_mid) and stones frozen into its ragged shingle-side edge (streams 2571-2574). Placements and every slab group but cradle_cracks identical to 03306a599; wreck terrain-hidden 0.3255 (was 0.3251). Gates: walk 8/8, check (a) 6/6, P6' PASS, fit 1.0001, class map 0 unassigned. Sheets `M1pp/pilot12_257_sheet_*`; tiles `art/pilot_tiles_257.json` (1_0, 2_0, 2_1, 2_2 byte-identical). Note: the `LV_DBG_NPZ` debug dump hook was added to make_bv2art.py (off by default).

## R-C9-259 (narrow: the curtain right of the stern, from 7c3940b51) -- 0 images
Cause: the beach's SOUTH flank (where the `west` beach region meets the cliff-side `south` sea region by the junction) ended in a vertical face from mid-slope shingle (~-2 m) to the sea floor; R-C9-257's smaller cradle exposed more of it. Fix: beach cells near that flank ease down to the shore-ice level over ~3 m (steep shingle slope; only > 1.5 m from the shore line, so the beach top and the cliff do not move), the sea-region cells next to it sit at shore-ice level (apron, d_lip > 1.6 m), and boulders (rock blobs) lie on the slope (stream 2591). Placements and every slab group identical to 7c3940b51. Gates: walk 8/8, check (a) 6/6, P6' PASS, fit 1.0001, class map 0 unassigned. Sheets `M1pp/pilot12_259_sheet_*`; tiles `art/pilot_tiles_259.json`.

## R-C9-283 (Phase 3' cave-front ice, from b5894d440) -- 0 images
(1) The honeycomb was the OLD SHELF's Voronoi cells (`old_shelf_ice`, slab group `cove_ice`; one seed spacing 2.6 m, one shrink). Every cell lying wholly below the pilot (plate y > `PILOT_SAFE_Y` 2640) is replaced by natural floes built like the pilot pack (fine cells merged by a lognormal-weighted coarse partition, 0.3-30 m2; leads 3-55 cm of varied width; rough worn edges; corners rounded; freeboard varied; own stream 2831), filling exactly the replaced cells' ground (122.5 -> 95.9 m2 of ice). The 5 cells that reach into the pilot rows stay byte-identical (their straight Voronoi edges remain, inside the pilot's pinned guide). The cave mouth's ledge rule and the ledge itself are unchanged. (2) The zig-zag "plank" at 0_3 was a snow-heaped RIM (`ice_rims`: a chain of thin raised quads along a floe edge). Every rim run wholly below the pilot is now one broad low soft drift (tapered lens 0.45-0.8 m wide, 2.5-4.5 cm proud; stream 2832); rims inside the pilot unchanged. Placements identical; the 9 pilot guide tiles byte-identical (checked by sha); changed guide tiles (row,col): (3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(4,3) -> `art/tiles_283.json`. Gates: walk 8/8, check (a) 6/6, P6' PASS, fit 1.0001, class map 0 unassigned. Stills `M1pp/cave_front_{before,after}/` (spec `M1pp/cave_front_spec.json`), sheet `M1pp/cave_front_283_sheet.jpg`. Before stills built by running b5894d440's make_bv2art.py from a scratch copy (outside the repo, scratchpad old_make.py).

## R-C9-289/290 AUDIT (STEP 1; rebuild waits for the conductor's go) -- base 67fc4b80b
`lv/tools/lv_ice_audit.py --tag 67fc4b80b` -> `lv/art/ice_audit.json` + `lv/M1pp/ice_audit_map.jpg` (red = stacked ice cells, yellow = slivers sitting on ice, magenta = straight-edged items, blue = R-C9-290 cave-top boxes; green grid = pilot chunks). Run on the 67fc4b80b level (regenerated from that commit's make_bv2art.py; the map's background guide is the uncommitted R-C9-285 render, positions identical).
WORKING TREE NOTE: `make_bv2art.py` carries UNCOMMITTED R-C9-285 edits (all rims -> drifts; cradle_cracks emptied = the wreck's "ropes/stick"). The rim part is superseded by R-C9-289 (the rebuild removes rims entirely); the cradle_cracks removal stands. The level data on disk is 67fc4b80b's (regenerated for the audit). M1pp/wreck_285_{before,after}/ stills exist (uncommitted).

## R-C9-294 (GO on the audit): ice rebuild B (Phase 3') + surgical A (pilot) + cave top C -- from 67fc4b80b, 0 images
- make_bv2art.py "R-C9-294" (after the slab assembly): pilot items (projected into plate x<4096,y<2560 + 24 px) are LOCKED byte-identical unless wholly inside ONE A rect (+14 px pad), where rims/ridges/brash/rubble/seams are removed (seams -> paint-class snow lines on the mere ground); ALL cradle_cracks removed (their own rects, +48 px measured shading reach). Phase 3': all old sea-ice items dropped; ONE partition (fine 0.6 m cells merged by a weighted coarse field with a low-frequency SIZE field; outline rounded x3, inset 0.06-0.9 m, worn 0-4 cm; fast +0.30-0.40 / plates +0.18-0.28 / floes +0.10-0.20 over the sea; 17-ish flush drifts cut OUT of their floe at its height (`ice_drifts`, class snow); brash only in open water). Thresholds: floe >= 0.6 m2, width 2A/P >= 0.45 m, no straight stretch >= 1.2 m (every vertex within 3 cm of the chord), leads >= 0.10 m; brash >= 0.04 m2, width >= 0.075 m, >= 0.08 m clear of floes.
- bv2pp_cove.py: R-C9-290 erosion (drop_scale 0.5, top blur 0.45 m + dome, round-intersection shoulders r 0.45 m, snow only where up > 0.8) gated by `erode_ok` = outside the pilot or inside the C rects (+90 px margin), judged at the old tops.
- Proof `tools/lv_ice_proof.py` -> art/ice294_proof.json PASS (no new stack; drifts flush; thresholds; heights). Pilot allowlist `tools/lv_pilot_allowlist.py --ref-guide <67fc guide> --ref-class <67fc class>` -> art/pilot_allowlist_294.json PASS (0 changed px outside A + C + crack rects; class map too). Changed tiles art/tiles_294.json: Phase 3' 3_2 (cave-top erosion east of the pilot; ALREADY PAINTED), 0_3,1_3,2_3,3_3,0_4,1_4,2_4,3_4,4_4; pilot 0_0,0_1,0_2,1_2,2_2 inside the allowlist only.
- Gates: walk 8/8, check (a) 6/6, P6' PASS, fit 1.0001, class 0 unassigned. Stills M1pp/ice294_{before,after}/ (12 views, spec ice294_spec.json), sheets M1pp/ice294_sheet_{A,B}.jpg.
- Left untracked (superseded R-C9-285 work, for Matt's cleanup list): M1pp/wreck_285_spec.json, M1pp/wreck_285_{before,after}/.
