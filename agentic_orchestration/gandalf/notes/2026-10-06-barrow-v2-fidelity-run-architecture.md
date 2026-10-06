# barrow_v2 at v1 fidelity, then the w151–160 arena inside it: forensic and autonomous-run architecture

**STATUS:** CURRENT (working design; a proposal for the fresh C-9 conductor session, not yet a ruling).
**Authored:** 2026-10-06, by a Claude Code session at Matt's request ("review … what worked in barrow_v1 and what didn't work in barrow_v2 and design an architecture for an autonomous run …").
**Truth of record:** `astra_test_01/burst/runs/C-9/ledger.json` (rulings through R-C9-160). Where this note and the ledger disagree, the ledger wins.

**Read with:**
- `2026-10-06-c9-phase2-session2-handoff.md` (§2 look and rules, §6 constraints);
- `2026-10-06-c9-phase2-session-record.md` §3 (the eight attempts).

**Evidence base:** three read-only forensics run this session. Every number below is cited to a file or ledger entry. The forensics were:
- v1 (`barrow_full/`);
- the v2 attempts (`barrow_v2/`, the `barrow_v2_sw` level);
- the KC2 runtime and w151–160 plumbing (`reincarnated-godot/kc2_runtime`, `kc2_play`).

---

## 0. The answer in one paragraph

**v1 worked because of one invariant.** The play camera is a fixed-direction orthographic camera (pitch 52.95354°, yaw 47°, `barrow_full.gd:44-45`). Under such a camera, **one painting at the game camera is the complete in-game view of every static surface** (`take/build_plan.md` §1). v1 exploited that literally:
1. A blockout of the right shapes was rendered once at that camera.
2. It was painted over **once**, ground and objects together, at full plate density (100.6 px/m), by a painter told to keep every silhouette.
3. That single painting was cut by geometry.
4. Every static surface wears the painting, **unlit**.
5. Only moving things are real and lit: him, heather placed *from the painted tufts*, the snow, and the snowfall.

**v2's last attempt (R-C9-159) broke that invariant in four places at once:**
- ground painted alone at **half** density;
- every model painted separately from **4-view sheets** and **lit a second time**;
- heather from procedural noise;
- the site **seen 47° off sketch A's composition**.

**The attempt before it (R-C9-158) was actually v1's method, run outside v1's engine.** Matt's complaints about it (seams, painted plants, no life, the boat) were real but local. The fix was to *move 158's method into v1's engine*. Instead, the method itself was replaced.

**The run below therefore restores v1's pipeline byte-for-byte and moves it into v1's engine.** It records every unavoidable deviation, and gates each phase on measured v1-parity before Matt sees it. Two pilot windows come first, then the whole site (~90–99 chunks, not 48). Only after Matt walks the finished level does the KC2 sim run inside it, using a 3D presenter over the sealed runtime.

---

## 1. What worked in v1 (the mechanism, with numbers)

| # | v1 fact | Evidence |
|---|---|---|
| W1 | **Fixed-direction ortho camera.** "It pans with him, but it never turns." Projection is valid for every static surface, and unpainted backs are never on screen | `take/build_plan.md` §1; `painted_world.gd:27` |
| W2 | **The greybox was the shape of record.** Real models in flat `hero_grey`, primitives in darker grey, ground in four flat tints (snow / path / ice / shrub), one sun at 55° upper-left, ink on | `barrow_full.gd:14-19, 379-410`; `captures/guide_preview.png` |
| W3 | **A literal brief.** *"Paint OVER the render: every object keeps EXACTLY its silhouette, position and size … One thin warm dark-brown ink line on every contour, the SAME weight everywhere."* One reference image, for **"palette, light, snow, stone carving and painted hand ONLY -- NOT its layout"** | `conductor_scripts/cfg_t10bf.json` (`geo`, `rules`, `refs`) |
| W4 | **Full density, small canvases, one hand.** 5376×3328 at 100.6 px/m; 4×4 canvases of 1536×1024 on a 1280×768 stride (256 px overlaps). Neighbour context = the left, top and top-right painted strips pasted in. Partition-of-unity stitch | `make_layout.py:65`; `guided_paint.py:22-35`; `guided_stitch.py:2-33` |
| W5 | **Ground and objects painted together**, in one light by one hand, so they share everything | the stitched `paint/barrow_full_painted.png` |
| W6 | **The take is cut by geometry, not colour.** An ID render gives 54 plates. 29 primitives + 33 birches + the ground wear the painting **by projection**; 25 real models are **baked from the same painting through the game camera** (one cell, `t5_06b_bake.py`), with one 1024² texture **per instance** | `take/take_report.json`; `build_plan.md` §2–§5 |
| W7 | **Static surfaces are unlit.** Lit plates measured 40.7 mean difference from the painting, unlit 15.5 ("the painted light lit a second time") | `painted_world.gd:87-108`; N-C9-PAINTED-LIGHT-RULING |
| W8 | **Life comes from real, lit, moving layers.** His two-sun light; a 3D snow trail; 1,700-particle snowfall; **977 heather sprays placed FROM the painted tufts and tinted by the paint under them** (52% on tufts) with gust wind | `barrow_heather.gd`; `paint_world_prep.py:125-133, 276+`; `snow_field.gd` |
| W9 | **Gate order.** Blockout → Matt walks it (R-C9-86) → paint → take → build → overlay acceptance → Matt's look (R-C9-89: *"Hard to believe it is real 3D"*) | rulings R-C9-75, 86, 89 |
| W10 | **Cheap.** 28 Astra images in 16 bursts, 59.5 lane-minutes, $0 fal for the level | ledger T10BF-* |

**v1's own flaw, and why it matters here.** The rocks stayed "tiered cakes" because the greybox's stacked slabs were painted faithfully (R-C9-151). Matt still loved the level. **Coherence (one hand, one light, one painting) beat shape accuracy.** The greybox's shapes *are* the painting's shapes. **So v2 needs better shapes in the guide, not the guide dropped.**

## 2. What did not work in barrow_v2 (all eight attempts, reduced to causes)

| Cause | Attempts | What it did |
|---|---|---|
| **C1. Coupling to the 2D arena** | #4, #5 (R-C9-151..156) | Forced geometry-by-rule before art, and flat zone maps with no shapes. The painter invented doors chunk by chunk (BVP T1/T2), crammed the floor and blocked lanes |
| **C2. Primitive or sculpt-blob greybox as the guide** | #3 (R-C9-148/149a) | "Man-made and square". The same mechanism as v1's tiered cakes, at site scale |
| **C3. Leaving v1's engine** | #7 (R-C9-158) | No heather wind, no moving water, no snow trail. Plants (2,465 heather in the guide) were painted rather than 3D |
| **C4. Splitting the one painting** | #8 (R-C9-159) | Ground painted **alone** at **50.3 px/m**, each Astra image covering 4× v1's ground. Each model painted from its own **4-view sheet**, blended by facing⁴ (`v2sw_model_bake.py`) → blotchy, cellular bakes in a different hand from the ground |
| **C5. Lighting the painting twice** | #8 | Model bakes run through `PaintStack.world_material` and the dynamic sun: *"NOT unlit as v1's heroes"* (`barrow_v2_sw.gd:643-669`) |
| **C6. Rotating the composition away** | #8 | layout_v2 and sketch A are composed for a **yaw-0** camera (layout_v2.json:21-38). The level keeps that frame and turns *only the camera* to 47° (`barrow_v2_sw.gd:11`). Every door, the cave mouth and the coast, composed to face sketch A's view, is seen 47° off-axis. This is very likely part of the "cramped cave view" |
| **C7. Shape distortions in the kit** | #6–#8 | Per-axis non-uniform normalisation (barrow 1.9× vertical) plus per-slot stretch (longhall 24 → 35.2 m). The wreck was built from **eye-level** sheets, but at 53° the hull interior dominates, hence "a pale tub" |
| **C8. Scale and composition never judged at the play camera** | #2–#8 | Sketch A is a whole-site, *not-to-scale* illustration. At true scale, a 19×13 m screen holds one wall of cliff or one hull, where v1's screens held several small, readable things (2.7 m stones, heather, part of the mound) |
| **C9. Reference confusion in the painter** | #7 | Each chunk received a 384×256 crop of sketch A enlarged 4×, mixed across anchors by inverse-distance weighting (`bvp_paint.py:59-71`). That is a blurry, wrong-scale second "truth" per chunk (cf. R-C9-67: two truths → the painter alternates) |
| **C10. Re-inventing instead of replicating** | #6→#8 | Each round changed several variables at once, so no result isolated a cause. The R-C9-159 over-correction is the clearest case: 158 was v1's method in the wrong host, and 159 changed the method instead of the host |

**Corrections to the 10-06 handoff** (from code):
1. v1 and v2sw both use 1536×1024 canvases on a 1280×768 stride. "2816×3328" is v2sw's whole guide, not a tile.
2. v2sw heather came from noise sampling (`section_sw_build.py:607-637`), not from a layout density map.
3. layout_v2's `version` field reads 3; "v6" is ledger-only.
4. The whole site is **~85–99 v1-size canvases**, not 48. The paint envelope (floor + half-screen margin) is 113.0 × 103.9 m = 11,776 × 8,704 px, 5.3× v1's window. The 48 figure covers only the floor's bounding box.

## 3. Design principles for the run

1. **One painting is the world.** Every static surface (ground, models, rocks, cliffs, ice, the sea's base colour) wears **one** stitched painting at ≥ 100.6 px/m. Projection is used for primitives and terrain; **game-camera bakes from that painting** for real models. **No other painted texture enters the level.**
2. **Unlit statics, lit movers.** Exactly v1's two-sun law. Only characters, heather, snow relief, snowfall, water motion layers and VFX are lit or animated.
3. **The greybox is the shape of record, so its shapes must be good.**
   - Real models for every structure and every rock mass, **uniformly scaled**.
   - Class tints for materials.
   - **No plants in the guide**, only v1's shrub-zone tint. The heather is then derived from the painted tufts.
4. **Replicate literally; deviate only on the record.**
   - v1's tools are copied byte-identical and checked by sha256 at every run, as v1 itself did with `t5_06b_bake.py`.
   - Every departure is an entry in a **deviation register** with a reason and a measured A/B.
   - No new pipeline stage without a Matt gate.
5. **Compose for the play window, not the whole-site sketch.** Matt judges 12–16 play-camera *screens*, plus the map.
6. **Measure parity before Matt looks.**
   - An automated **v1-parity harness**, calibrated so v1 passes and R-C9-159 fails, gates every phase.
   - Matt's eye stays final; the harness only decides what is worth his time.
7. **Change one variable at a time, and only on the pilot.**
8. **Keep it sequential (R-C9-156).** The arena phase starts only after Matt passes the finished level.

## 4. The run, phase by phase

**Roles:**
- **gandalf** is RUN-CONDUCTOR. He conducts and does not build.
- Lanes:
  - **drax-LV** — level, models, greybox;
  - **drax-PT** — paint, take, build, life;
  - **galadriel-PH** — parity harness and blind test;
  - **drax-AR** — Phase 4, joint with the Sim Session's drax.
- **jack-ryan** runs Gate-1 on the charter and Gate-2 at each phase close.

**Matt gates:**
- **M0** — questions asked asynchronously at launch;
- **M1** — greybox walk and screens;
- **M2** — pilot look;
- **M3** — full-site walk;
- **M4** — arena play.

Everything between gates is autonomous.

### Phase 0: re-baseline and the parity harness (no image spend)

- **0.1 Positive control.** Re-render v1 at HEAD and reproduce its recorded numbers: ID self-test, unlit-vs-painting 15.5, heather 52% on tufts, frame time 10.9–12.4 ms.
- **0.2 Frame fix (C6).** Place the barrow_v2 site in v1's world rotated by the camera yaw, with `world = R_y(47°) · sim`, sign verified, so the play camera sees sketch A's composition.
  - The camera, heather card basis (`barrow_heather.gd:43-45`), suns, snow and pen stay **untouched**. This is v1's own practice: its layout was authored in camera-aligned (u, v).
  - Proof: the layout's anchors and features rendered at the play camera, overlaid on sketch A's screen positions (not to scale, so judge topology and orientation only).
  - Phase 4 applies the same fixed transform between sim and world.
- **0.3 Freeze the v1 toolchain.** Copy these with sha manifests:
  - `guided_paint.py`, `guided_stitch.py`, `t10bf_drive.sh`;
  - `capture_blockout.gd`, `capture_ids.gd`;
  - `take_from_paint.py`, `hero_surface.py`, `t5_06b_bake.py`;
  - `paint_world_prep.py`, `heather_instances.py`.

  Parameterise only the frame and grid.
- **0.4 Parity harness (galadriel-PH).** The table below lists each metric and its threshold. Thresholds are taken from v1, with R-C9-159 and R-C9-158 as negative controls. **A metric that cannot tell v1 from 159 is discarded, not tuned.**

| ID | Metric | Pass |
|---|---|---|
| P1 | Displayed texel density on every static surface at the play camera | painted px/m ≥ 100.6 (ratio ≤ 1.05) |
| P2 | Provenance: the source of every static texel | 100% from the one stitched painting |
| P3 | Lighting audit: static surfaces on LAYER_PAINTED and unlit; lit-vs-painting residual | ≤ v1's 15.5 |
| P4 | Per-class texture statistics (snow, rock, wood, ice, water edge) vs v1 crops: Lab histogram distance and radially-averaged power spectrum, plus a **cellularity** detector (spectral peak at 6–20 px period) | within v1's own chunk-to-chunk spread; 159's bakes must fail |
| P5 | Seams: overlap MAD (v1: 2.7–13.1/255) **and** stitched seam visibility (gradient energy on the seam line ÷ off-seam baseline) | ≤ v1's distribution; failures go to seam repair |
| P6 | Geometry agreement: per-object ID silhouette vs painted class map; **invention check** (dark openings and structures per chunk vs the layout) | IoU ≥ v1's median; inventions = 0 |
| P7 | Clean floor measured **on the painting**: R13 tuft and clutter density on the walkable floor; the five lanes clear | as validator R12/R13 |
| P8 | Heather: share placed on painted tufts, tinted from the paint | ≥ 50% (v1 52%) |
| P9 | Life: heather sway visible; water motion; floe bob with **rest-pose UVs** (no texture swimming); snow trail across the whole floor | film check |
| P10 | Desktop performance on the walk film | p99 ≤ 16.7 ms |
| P11 | **Blind pair test:** a fresh judge gets 20 same-class crop pairs (v1 vs v2) at play zoom | identification ≤ 65% (calibration: v1 vs 159 ≈ 100%) |

### Phase 1: design freeze and the blockout (M0, M1)

- **1.1 M0, asked at launch** (one recommendation each):
  - (a) Water: **one sea level, with the wreck beached on the shore ice** (recommended; it removes the spit and the −1.3 m lagoon liberty), or a lagoon at two levels?
  - (b) The wreck: **a model designed to be read from 53° above** (deck, ribs, prow and snapped mast visible from the top) at about 12–14 m, rebuilt from a top-down sheet.
  - (c) Play zoom: **v1's 19 × 13 m window** (recommended for parity), or layout_v2's GD zoom of 25.4 × 17.9 m. A zoom *out* does not break projection, because ortho scale only changes sampling, so this can be an in-game toggle later.
  - (d) The run image cap: the ledger shows 1,251 of 1,500 used, and this run needs about 200–250 more. Raise it to about 1,750.
- **1.2 Model kit v3 (drax-LV):**
  - Rebuild only what C7 broke: the barrow front, the longhall at true proportions, and the wreck.
  - Uniform scale only (≤ 10% per-axis tolerance).
  - Tripo multiview at the game pitch, **including a 53° top view in the sheet**, for any model whose top is what the player sees.
  - Cliffs and crags stay modular instances. Each instance gets its own bake (W6), so "one model at many yaws" stops being a reason to paint models separately.
  - Budget: ≤ $8 fal.
- **1.3 The class-tinted guide (drax-LV):**
  - v1's guide recipe exactly (W2): flat tints, one sun, v1's pen.
  - v1's **own tint values** for shared classes (snow, path, ice, shrub). This also fixes the "dark-streak" path.
  - New, distinct tints for the new classes: rock, wood, shingle, shore ice, sea, stream.
  - Models in flat class tints, not their Tripo textures. No plants.
  - Rendered at 100.6 px/m over the full 11,776 × 8,704 envelope as 1536 × 1024 tiles.
- **1.4 Screens and walk (M1).** 12–16 play-camera stills: the start, each door approach, each disc, the cave top, the wreck, the mere. Also a labelled top-down map and a walkable greybox app. Matt walks it as at R-C9-86. **No painting before M1.**

### Phase 2: the pilot, two grid-aligned v1-size windows (M2)

**Choose the final 9 × 11 grid first.** The pilot windows are 4 × 4 sub-blocks of it, so passed pilot chunks are kept, and their neighbours later receive them as pasted context.

**The windows:**
- **W-A, "home ground":** the start, the stone circle, the mere (p05), the stream, and the barrow front and door (p02).
  - This is v1's own register: snow, stones, ice, heather and a barrow.
  - **If W-A fails parity, the replication is wrong, not the content.** Stop and run the forensic; do not touch W-B.
- **W-B, "the coast":** the wreck (p01), shore ice, the sea, the cliff, and the cave and stair (p03). This is the hard, new content.

**Painting**, exactly as v1 (W3–W4): the left/top/top-right paste and the same caps.

**Brief:** v1's `rules` verbatim, plus the new classes in `geo`.

**References:**
- **IMAGE 2 is v1's own reference** (the T10C concept: palette and hand only).
- **Deviation DEV-3:** sketch A crops are attached only to chunks that contain a hero (wreck, hall, cave, gable). They are attached at **true scale** and labelled *"what this object looks like, subject only, NOT its size or place"*. They are never enlarged by inverse-distance weighting (C9).

**Per-chunk notes:** generated from the ID render, never written by hand. Each note says *"exactly one dark doorway at px (x, y)"* and lists the objects present. This closes the BVP double-door failure mode.

**Then:**
- the take, bake and build into the barrow_full level;
- heather derived from the painted tufts;
- snow;
- animated water over the painted sea, keeping R-C9-159's shader but with its base = the painting;
- floes bobbing with frozen projection UVs.

**Run the harness.** Then jack-ryan Gate-2. Then M2: stills and a film of W-A and W-B, **each beside v1 at the same zoom**.

**Budget:** about 32 chunks, about 56–64 Astra images.

### Phase 3: the whole site (M3)

- **Paint the remaining ~60–70 chunks** with the frozen pipeline, under v1's wavefront driver. A chunk is ready when its left, top and top-right neighbours are done.
- **Per-chunk auto-QA:** P5–P7 on arrival, with the invention check first.
- **Seam repair:** a canvas centred **on** a failing seam, both sides pasted, the centre blended. At most one repair per seam, capped at 15% of chunks.
- **Colour drift over 11 rows:** measured against the pilot windows' class statistics (P4). A low-frequency master transfer is used only if P4 drifts. Note that R-C9-159's σ = 40 transfer made 3 of 10 seams *worse* (DEV, measured).
- **The full take and build:**
  - per-instance bakes;
  - heather of roughly 4–5k sprays;
  - a snow field resized to the 85 m floor;
  - the painting as one desktop texture (11,776 × 8,704 fits under the 16,384 limit; VRAM-compressed).
- **Close-out:** a desktop app and a walk film, then jack-ryan Gate-2, then **M3, Matt walks the level**.
- **Budget:** about 130–150 Astra images, including repairs.
- **Elapsed time:** v1's rate (3.7 lane-minutes per chunk) gives about 6 lane-hours. With the wavefront that is about 3 h of wall-clock, plus usage-limit halts.

### Phase 4: the w151–160 arena inside barrow_v2 (joint with the Sim Session; starts after M3)

**What the forensic shows is ready:**
- The KC2 runtime is pure GDScript and vendorable by SHA (`kc2_runtime/README.md:17-33`).
- The barrow_v2 anchors **equal** the sealed pack's sg1 anchors, in the same sim frame (`layout_v2.json` anchors; validator R1).
- The sim is deterministic at 12.25 Hz, and presentation is event-driven (`kc2rt_view_contract.gd:30-60`).
- **Every kit has a GLB** with clip manifests.

**The steps:**
- **4.1 Geometry of record.** The barrow_v2 floor polygon (4,225 m², 736 vertices) becomes a **new arena geometry**, ruled by the Sim Session as a registered divergence:
  - `kc2play_arena.gd:42` gates on the Crucible trace's sha;
  - the `north_gate_is_north` check is at `kc2play_session.gd:94-99`.

  The flat-floor rule (validator R5: height exactly 0 on all 16,897 floor samples) means sim (x, y) maps to world (x, 0, y), then through the Phase 0.2 rotation.
- **4.2 Vendor `kc2_runtime`** into `barrow_full/godot` by SHA: no edits, purity scan green, `GRADED_RULES` / arm M0 as sealed (`kc2play_session.gd:37-42`).
- **4.3 The 3D presenter (drax-AR).** It re-implements `kc2p_monster.gd`'s mapping on AnimationPlayer:
  - position from the snapshot with knot interpolation;
  - scale = true_size `factor`;
  - `cast_start` → the cast clip, released on the tick;
  - `death` → hold, then fade;
  - p05 `emerge` warped to its window;
  - `hit` → flash;
  - facing from the step bearing, otherwise toward the player.

  **No pixel decides a hit.**
- **4.4 The player.** The REFERENT-v1 warlord in barrow_full's rig. `knight.gd`'s local `move_and_slide` and strike logic become **intents** (`move_target_m`, `channel_held`, `skill_pressed`). The sim samples his position and the view snaps on `position_correction` (the F1 rider).
- **4.5 Enemy bodies:**
  - EN-E2 humanoids go from about 290k triangles to ≤ 25k, with a LOD. EN-E3/E4 are already 40–50k.
  - All get the character render path (two-sun light, 1.1 px hull pen, char-light b).
  - The 170 unmapped roster records are ruled by KC2: kit-map or token.
- **4.6 Deliveries in 3D:**
  - Door intros are keyed to the derived `EV_*` events: `spawn` with `spawn_point_id`, `wave_flip`, and the ambush `spawn_t_s`.
  - **Bodies appear at their sim positions; nothing walks out of a door ahead of the sim.**
  - DV's 2D flipbooks are reused as camera-facing quads. Under a fixed camera this is exact for screen-aligned effects. Ground effects (the mere's cracks) become decals.
- **4.7 Proofs:**
  - PLAY in barrow_v2 reproduces the ORACLE event stream for w151–160 under the registered divergences, headless, using the existing G3 tools;
  - 0 frames over 16.7 ms at the w160 peak.

  Then jack-ryan Gate-2, then **M4: Matt plays w151–160 in barrow_v2**.

**Constraint:** **desktop only.** The native contact solver ships `macos.arm64` only and refuses to fall back under graded rules (`kc2play_session.gd:162-168`). A web build needs a wasm build plus a shadow bit-equality run (KP-234), which is a separate decision.

## 5. Autonomy rules (the guard-rails that answer this phase's failure history)

| Rule | Answers |
|---|---|
| v1 tools by sha; the deviation register; no new stage without Matt | C4, C10 (the 159 over-correction) |
| Every metric has a positive control (v1) and a negative control (159) | instruments that "return cleanly after they stopped answering the question" |
| Stop at the first failing gate, run a forensic, change one variable, re-run on the pilot only | C10 |
| Matt sees only harness-passing work, *or* a decision request | Matt's attention; R-C9-160 |
| barrow work never waits on or races KC2; Phase 4 starts after M3 | C1, R-C9-156 |
| Per-lane `RESUME.md` current at every commit; driver HALT exit 7 on usage limit | the Oct 3→6 usage-limit stall |
| Caps: Astra about 250 for the run (needs the M0(d) raise); fal ≤ $10; heavy lock; disk gate 20 GiB (lanes halt at 21); Matt runs deletions | handoff §6 |
| `git commit --only`; `git status --porcelain` before, `git show --stat HEAD` after; `git -C` cross-repo; the ledger committed by the conductor | CLAUDE.md, handoff §6 |

## 6. Deviation register (seeded; every entry needs a reason and a measurement)

| DEV | Departure from v1 | Why it can't be avoided |
|---|---|---|
| DEV-1 | Grid 9 × 11 (≈ 90–99 canvases) instead of 4 × 4 | The site is 5.3× v1's window |
| DEV-2 | New material classes and tints (rock, wood, shingle, shore ice, sea, stream) | v1 had no coast and no buildings |
| DEV-3 | Sketch A identity plates on hero chunks, at true scale | v1's concept has no wreck, hall or cave |
| DEV-4 | Site rotated into v1's camera (`R_y(47°)`) | Sketch A and layout_v2 are composed at yaw 0; v1's engine is hard-wired to yaw 47 |
| DEV-5 | Animated water over the painted sea; floes bob with rest-pose UVs | Matt, R-C9-159(4) |
| DEV-6 | Snow field resized to the 85 m floor | v1's field is 47.2 m |
| DEV-7 | Desktop painting texture at 11,776 × 8,704 (web tiling later) | Size |

## 7. Expected cost (estimates, to be re-based after the pilot)

| Phase | Astra images | fal | Agent time |
|---|---|---|---|
| 0 | 0 | 0 | about half a day |
| 1 | 0–4 (wreck and model sheets) | ≤ $8 | about 1 day, plus Matt's walk |
| 2 | about 56–64 | 0 | about 1 day |
| 3 | about 130–150 | 0 | 1–1.5 days |
| 4 | 0 | 0 | 2–4 days, joint with the Sim Session |
| **Total** | **about 190–220** | **≤ $8** | **about 6–8 working days with 5 Matt gates** |

## 8. Fresh-session prompt (paste as the first message of the conductor session)

```
You are gandalf, RUN-CONDUCTOR for Run C-9 Phase 2 (Reincarnated), focus: barrow_v2 at barrow v1's
fidelity, then the w151-160 arena inside it.
Read your operating procedure skill (reincarnated-gandalf-operating-procedure) and run its
session-start protocol. Then read, in order:
  1. agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-architecture.md
     (THE PLAN: forensic, principles, phases 0-4, parity harness, deviation register)
  2. agentic_orchestration/gandalf/notes/2026-10-06-c9-phase2-session2-handoff.md (sections 2 and 6)
  3. astra_test_01/burst/runs/C-9/ledger.json, rulings R-C9-144..160
  4. astra_test_01/burst/runs/C-9/barrow_full/take/build_plan.md (v1's mechanism, section 1)
Look at sketch A (barrow_v2/sites/BV3r2-A_spawns.png), v1's painting
(barrow_full/paint/barrow_full_painted.png), and the R-C9-159 sheets (barrow_v2/section_v1cam/look/).
Then:
  (a) Draft the run charter from the plan (phases, lanes, caps, Matt gates M0-M4, deviation
      register) and route it to jack-ryan for Gate-1.
  (b) Put the four M0 questions (plan section 4, Phase 1.1) to me with AskUserQuestion, one
      recommendation each.
  (c) On my answers, launch Phase 0 (no image spend): positive control on v1, the frame fix
      (site rotated into v1's camera), the frozen v1 toolchain with sha manifests, and
      galadriel's parity harness calibrated v1 = pass / R-C9-159 = fail.
Conduct; don't build. Spawn fresh drax/galadriel lanes pointing at RESUME files.
Record every ruling in the ledger. Keep me posted briefly; I am on my phone (Remote Control).
