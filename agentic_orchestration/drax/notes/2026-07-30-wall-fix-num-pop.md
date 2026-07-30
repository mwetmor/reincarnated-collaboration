# WALL-FIX + NUM-POP — the wall was never dark, and the numbers were never readable

> **Cell:** WALL-FIX + NUM-POP. **Agent:** drax (presentation seam).
> **Conductor:** gandalf (LR/presentation session). **Date:** 2026-07-30.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` Scope 6 · Scope 7 ·
> the WALL-READ landing block. **Diagnosis executed:** `galadriel/notes/2026-07-30-wall-read.md`.
> **Inherited:** godot `2c48854` LOCAL (ahead 4). **Shipped:** godot `ec9acbc` LOCAL (ahead 5,
> NOT pushed). Prior cells this session: AMB-REFIT · AMB-RISE · CAM-LOCK · AMB-HUE.

---

## §0 — What this cell says in two sentences

Matt asked why the inside of the walls is black. Galadriel answered it: a second, untextured wall
was built in front of the bricks. **This cell takes that wall away by giving it the kit's own
brick** — measured, not eyeballed — **and makes the damage numbers land like hits instead of like
text**, because the measurement says the old ones were six pixels tall at the camera Matt watches.

---

## §1 — WALL-FIX: the material, and why it is sourced rather than declared

`wr2_playback.gd::_dress_wall_faces()` built four `BoxMesh` slabs at `albedo (0.115, 0.118, 0.132)`
with no texture, seated at the kit wall's exact `WALL_H`, filling the 0.750 m R-WR1-21 band. R-WR1-21
is a requirement about **where the obstruction face sits**, not what it is made of. The band is a
0.750 m thickening of the wall, so it now looks like the wall thickening.

**The brick is lifted off the built wall mesh, not read out of the kit table.** One line would have
done the latter. The thing that has to match is not the kit's *intent*, it is what the wall standing
behind this slab is *actually wearing* at the moment the slab is built — including which material
path that particular wall took (`_apply_single_tex`'s `StandardMaterial3D.albedo_texture`, or the
occlude/south `ShaderMaterial`'s `stone_tex`). The north wall is read because it is the plain path;
south wears the void dissolve and east the occlude shader. **If it cannot be sourced, the band keeps
the old flat albedo and pushes a warning naming why** — a missing texture prints as absent, not as a
guess.

Run log, boss room: `brick sourced off 'SM_Bld_Base_Wall_01': tex=Brick_Small_01.png`.

### 1.1 The UV judgment, declared — and one route killed by measurement

**Godot's `BoxMesh` packs its six faces into a 3 x 2 UV ATLAS.** Probed, not recalled
(`tmp/wallnum_boxuv.gd`): u lands on {0, ⅓, ⅔, 1}, v on {0, ½, 1}. So the obvious route —
`uv1_scale` on the authored UV — would tile each face's own sixth of the map: six different slices
of brick, none of them coursing. That route is dead on the measurement, not on taste.

**World-space triplanar** is used instead. It sidesteps the box's UV entirely, locks the coursing to
world coordinates — so it is continuous across all four slabs *and* around the four corner pilasters
with no seam to author — and it lets the period be stated in **metres**, which is the only unit in
which "match the wall" is a checkable claim. `uv1_blend_sharpness = 8.0` keeps the box corners crisp.

**The period is the wall module's own, measured at runtime off the mesh** (`tmp/wallnum_uvprobe.gd`
took the same reading offline first):

| kit | wall world span | UV span | **period** | branch |
|---|---|---|---|---|
| dark-fantasy (**the boss room, the room WR3 renders**) | 2.5000 × 3.0057 m | 1.07783 × 0.99719 | **2.3195 × 3.0142 m/tile** | TILING |
| dark-fortress / dwarven-dungeon | 2.5000 × 3.0057 m | 1.07783 × 1.05678 | 2.3195 × 2.8442 m/tile | TILING |
| dungeon-realms | 2.5000 × 3.0057 m | 0.11773 × 0.40951 | **21.23 × 7.34 m/tile** | **ATLAS — refused** |

So the band courses at the *same size* as the masonry it thickens: the seam that matters is the
slab's top against the wall-top cap, and the real kit brick seen through the doorway. **Phase is not
matched and cannot honestly be** — the wall's phase is authored per 2.5 m bay in the module's UV, the
slab's is world-locked. Course *size* is the readable quantity; course *phase* at a 0.750 m step-out
is not something a crypt would have either.

**⚑ NOT copied: the wall-top cap's `world_uv_period = 1.125`.** Its own comment claims it matches the
wall face; the measurement says the wall face runs 2.32 m/tile. That is the **cap's** number, tuned
for a 0.45 m band viewed edge-on from above. The slab stands in the wall's plane, so it takes the
wall's number. (The cap/face period divergence is recorded here as a finding; not this cell's to
resolve, and invisible until someone looks for it.)

**⚑ ATLAS KITS REFUSED, with the reason named.** `dungeon-realms` occupies a small UV island inside a
4096 atlas. World-UV tiling across an atlas walks the sampler over the palette-swatch strip and
renders the **rainbow quilt** — `kit_replica_level.gd`'s own pillar-quilt lineage, and the void-cap's
defect #2. An implausible period (> 6 m/tile) is detected and that kit's band falls back to a solid
texture at the wall island's *measured mean colour*, which is the same answer
`_build_walltop_cap_mat()` already gives an atlas-only kit. It carries the wall's VALUE without
inventing coursing the module does not have, and it warns.

### 1.2 The acceptance number galadriel specified

Measured at the CAM-LOCK camera, frame 0128, with the slab region **auto-located as the
BEFORE-vs-AFTER change mask** (so the patch cannot be a flattering crop):

| | mean luma | **\|grad\|** |
|---|---|---|
| band BEFORE | 13.22 | **0.274** |
| band AFTER | 39.87 | **2.445** |
| masonry control, same frame, auto-located | 99.02 | **4.328** |

**8.9× the texture energy, 3.0× the value, against a masonry control of 4.328 in the same frame.**
Declared honestly: the band lands at 57 % of the control's `|grad|`, not 100 %. Three reasons, all
geometric — much of the mask is further from the camera than the control patch, the two side faces
sit at grazing incidence, and the mask includes the corner pilasters. The band was at 6 % of the
control before. (Galadriel's 0.04 / 6–7 figures were taken at 1080p on a different patch; `|grad|` is
a per-pixel step and does not transfer across resolution. The within-frame control is the comparison
that holds.)

### 1.3 Pilasters

Given the same brick. The old pair's face/pilaster albedo relationship was 1.26×; the pilaster tint
is set to **1.08**, not 1.26 — on a *textured* face a 26 % lift reads as a second stone, and the
corner now reads from silhouette and coursing rather than from being a slightly-less-black rectangle.
Judgment, declared, veto-open at the eye.

### 1.4 Kerb, geometry, cull

Kerb HELD (accepted instrument, unflagged). Geometry HELD — nothing moved, only the material.
Roughness moved 0.92/0.85 → **0.9**, which is the kit wall's own value: same stone, same answer to
light. `cull_back` kept (default) per the `walltop_occlude` CHANGE-5 lesson.

---

## §2 — The rider (WALL-READ §4): the azimuth that did not survive translation

`kit_replica_level.gd::_south_mat_common()` hard-coded `ring_center = Vector3(0,0,0)` while
`walltop_void_radial.gdshader` resolves position through `MODEL_MATRIX` — **world space**. Exact for
the single-room 17.5 m L7 stage, whose centre *is* the world origin. Wrong for every room `wr1_level`
translates to x = 0 / 47.5 / 100.0 / 157.5: the boss room measured "due south" from a point 157.5 m
away and got no blackout at all.

Fixed to the **room's own root, recorded at `build_level()`**. Every path that never calls
`build_level` (the corridor `prepare_tissue()` route) keeps `Vector3.ZERO` — the exact constant it
replaces — so that path is behaviour-preserved by construction.

**Behaviour preservation at the origin is MEASURED, per the WR1-ROOMS §7.1 precedent:** the L7 stage
re-rendered at the R-6 camera, applied vs reverted, **0 of 921,600 pixels, max channel diff 0**, and
the two PNGs are byte-identical (`398421737359c331…`). Not "believed unchanged" — the same claim the
frozen room has earned six times before.

**⚑ Consequence now visible, flagged not fixed:** with the slab textured, the boss room's south wall
is observable for the first time. WALL-READ §4 predicted it renders as an **unshaded flat plate** —
neither correctly blacked nor correctly lit — because the shader is `render_mode unshaded` and the
blackout sector now evaluates correctly but the *lighting* path was never authored for a non-blacked
south wall. This cell fixed the azimuth, which is what the rider asked. Whether the south wall should
now blackout in every room (it will) or be re-thought for a multi-room level is a **design question
for Matt / BEAUTY-CORNER**, not a bug to patch quietly.

---

## §3 — NUM-POP: the numbers

Matt: *larger, bold, POP, fun anime-style font — "really show the feel of combat with the numbers."*

### 3.1 The complaint, measured first

Old treatment at the player_lock camera: `font_size 40 × pixel_size 0.012 × _caption_k 0.46959` =
a 0.225 m glyph. Measured on the same hit, same frame 0128, both renders:

| | glyph bbox | ink px |
|---|---|---|
| BEFORE | **6 × 14 px** | **30** |
| AFTER | **46 × 101 px** | **~2,350** |

**7.7× linear, 76× ink area.** The old damage number was 1.1 % of frame height. It could not be read;
Matt is describing an arithmetic fact.

### 3.2 Size is DERIVED, not tuned

Stated as a **fraction of frame height** (8.5 % dealt / 10.5 % received, em box) and solved backwards
through the live camera's own projection, per label, at that label's own depth. Consequence, and it
is the point: the same on-screen size at **both** cameras and at any resolution —

- `player_lock`: 37.89 px/m → `font_size 135`, outline 27
- `arena_full` (the grading camera of record): 13.67 px/m → `font_size 373`, outline 75
- both → **61 px em, 8.5 % of frame** — verified in both renders, not asserted

**⚑ `_caption_k` is deliberately NOT applied to the numbers.** That constant exists to *hold* the
caption layer at its accepted screen pixels across the CAM-LOCK lens change. The damage numbers are
the one layer Matt has now ruled must not hold. **Every other caption keeps the hold, untouched;
the bottom banner STANDS (Matt-ruled).**

### 3.3 The pop

Under-size (0.35) → **1.40× overshoot** → settle to 1.0 over **0.150 s**, ease-out on both halves,
`TRANS_BACK` on the settle for the small dip that reads as weight. Alpha snaps in over 0.045 s (was
0.08) so the number arrives *with* the impact instead of fading up after it. The rise is HELD at its
accepted 2.1 / 2.6 m but now eases OUT — fast off the hit, slowing into the fade. Three tweens, one
property each, per the existing two-writers-on-one-value discipline.

Measured envelope at 30 fps, one hit: **f120 pre-spawn · f121 h=57 px (peak) · f123 h=45 (settled) ·
f140 h=45 rising and fading**. Sampled overshoot reads 1.27× because the 0.055 s peak lasts 1.65
frames and the sampler lands past it — the authored value is 1.40.

Outline is now a **ratio** of the derived size (0.20) at **full black**, not a fixed 7 — a fixed 7
would have gone from a 17 % rim to a 4 % hairline the moment the numbers grew.
`render_priority 4 / outline_render_priority 3` puts the number in front of the tag layer.

### 3.4 Font — LOCAL ONLY. No network fetch was made.

Searched the whole `~/Games` tree. **The Fantasy Warrior HUD pack ships sprites only — no `.ttf`, no
`.otf`, no bitmap font.** Neither does any other Synty pack in the corpus. The repo's only shipped
typefaces are three OFL faces in `polygon-interface-fantasy-menus`, each with `OFL.txt` beside it.
Their digits were measured (ink coverage inside the digit box at fixed cap height; mean stroke
run-length across the digit band):

| face | weight | digit ink | stroke | verdict |
|---|---|---|---|---|
| **LT Museum Bold** | 700 | **48.3 %** | **39.9** | **chosen — the local maximum** |
| Ortica Bold | 700 | 36.2 % | 31.6 | |
| Alegreya Sans Medium | 500 | 32.4 % | 22.8 | |

Wrapped in a `FontVariation` for two reasons, both load-bearing:
- **`fallbacks`** — LT Museum has **no U+25C6**. The received-marker diamond would have gone to
  `.notdef` the instant the font was swapped. Caught by checking the cmap *before* shipping, not by
  seeing tofu in a frame. The marker reads exactly as it does today.
- **`variation_embolden = 0.08`** — free weight on an already-700 face, no second file.

**⚑ IT IS A PLACEHOLDER AND IS LOGGED AS ONE ON EVERY RUN:**
`NUM-POP font: LTMuseum-Bold.ttf (local, OFL — PLACEHOLDER, not an anime display face)`.
It is a display *serif*. It carries the size, weight, rim and pop faithfully; it does not carry the
anime register Matt asked for, because nothing on this disk does.

### 3.5 ⚑ SHORTLIST REQUEST — one Matt pick + one download authorisation

All four are **SIL Open Font License 1.1**, free for commercial use and redistribution, available
from Google Fonts. Named for what their digits actually do:

| font | register | why it fits hit numbers | risk |
|---|---|---|---|
| **Bangers** | comic-book / shonen impact caps | condensed, very heavy, slight lean — the closest thing to a manga SFX face in the OFL set; digits stay narrow so 4–5 digit numbers do not eat the frame | slight lean can read as motion-blur at small size |
| **Luckiest Guy** | American-cartoon chunky | maximum ink, rounded terminals, big friendly counters that survive a thick outline; the safest "reads instantly" pick | wide digits — a 5-digit number gets long |
| **Titan One** | rounded arcade-display | heaviest counters of the four, near-square digits, superb with a dark rim; reads as game-UI rather than as prose | least "anime", most "arcade" |
| **Bowlby One SC** | ultra-fat display | the most weight per pixel; if Matt wants the numbers to feel *heavy* rather than *fast*, this is it | counters can close at small sizes; needs the size we now ship |

**Conductor lean (mine, veto-open): Bangers first, Luckiest Guy as the safe fallback.** Bangers is the
one whose silhouette a player would read as *anime combat*; Luckiest Guy is the one that will never
fail a legibility check. Swapping is **one constant** (`NUM_FONT`) — every other number in the
treatment is derived and does not move.

**No font was downloaded. Nothing was fetched. Awaiting Matt's pick + authorisation.**

### 3.6 What did NOT change

Numbers are the same per-hit trace values the decomposer already emitted. **Zero invented values,
zero fight semantics moved.** The telegraph pip, the strike-verdict label and the AI-state tags are
untouched — Matt said the captions are mostly fine, and mostly fine means HELD.

---

## §4 — Guards, and one honest non-zero

| guard | result |
|---|---|
| collision check at cell start | clean — no foreign uncommitted tracked work |
| `project.godot` sha256 start = end | `6bef17eb…ace8a` — **NO DELTA** |
| ref mp4 `tmp/wr2/wr3_after_pre_boss_B_74000802.mp4` | `910063d1…` **intact** |
| `walltop_occlude.gdshader` / `walltop_void_radial.gdshader` / `wr1_level.gd` / `run_wr2_playback.sh` | sha256 unchanged — **kit shaders READ as source, not modified** |
| protected dirs (`tmp/vmur* l7race wr2 ambfit ambrise ambhue camlock wr1 pclight`) | `find -newer` cell-start marker → **0 files, all nine** |
| traces | READ-ONLY (JSONL opened for read; census only) |
| engine tree | **zero writes by this cell.** One foreign file appeared (`.pytest_cache/v/cache/nodeids`, 19:11) — **not mine**, no pytest was run here; recorded rather than claimed |
| L7 frozen stage | 0/921,600 px, byte-identical PNG (§2) |
| godot commit | `ec9acbc` **LOCAL, ahead 5, NOT pushed** |

**⚑ Beyond-wall check, declared not smoothed.** CAM-LOCK established that beyond the wall line is
pure black by construction. Sampled every 10th frame: **10,236 px that were exactly (0,0,0) in BEFORE
are non-zero in AFTER — at mean luma 0.69/255, p95 1.4, max channel 5.** Localised
(`plates/PLATE_voidcheck_newlylit_magenta.png`): a **thin rim hugging the wall silhouette**, not a
spread into the void. It is the frozen glow post-process responding to a wall that is now correctly
brighter — physically right, arithmetically non-zero, visually nothing. This is an LSTAT-2-class
**authorised delta**: making the wall brighter *is* the cell.

---

## §5 — Deliverables (M-EYE — motion first)

All under `~/Games/reincarnated-godot/tmp/wallnum/` (OUTBASE pattern; nothing written to any
protected dir). Seed 74000802, `wr3_after` / pre / boss / B, the hit-dense opening window (the
densest 5 s in the trace: 14 damage events, ticks 0–90), 170 frames @ 30 fps, carrying the refit +
risen + **purple** ambient and the locked camera.

1. **`clips/WALLNUM_BEFORE_top_AFTER_bottom.mp4` — THE ONE TO WATCH.** Same frames, stacked. Black
   band above, brick below; six-pixel numbers above, popping numbers below.
2. `clips/WALLNUM_playerlock_AFTER_hitwindow.mp4` — the AFTER alone, clean.
3. **`plates/PLATE_numbers_before_vs_after.png` — the fastest read in the cell.** One hit, one frame,
   3× zoom: the 6-px smudge beside the bold outlined **202**, and the black band beside the brick, in
   the same picture.
4. `plates/PLATE_wall_black_vs_brick.png` — the wall alone, same frame, both builds.
5. `plates/PLATE_numpop_zoom_strip.png` — the pop envelope across consecutive frames.
6. `plates/PLATE_voidcheck_newlylit_magenta.png` — the §4 non-zero, located rather than argued.
7. Judge-camera smoke: `frames/wallnum_JUDGE_*.png` — the grading camera of record still reads, and
   the derived size lands on the same 61 px em there.

**NOT a full watch re-render** — per the brief. That comes after Matt's verdicts, one render carrying
everything accepted.

---

## §6 — Reproducibility

- `scripts/wr2_playback.gd` — `_source_kit_brick()` / `_shell_mat()` / `_num_px_per_m()` /
  `_float_number()`; `scripts/kit_replica_level.gd` — `_room_world_center`
- `tmp/wallnum_uvprobe.gd` + `.tscn` — the per-kit wall UV period measurement
- `tmp/wallnum_boxuv.gd` + `.tscn` — the BoxMesh 3×2 UV-atlas probe that killed the `uv1_scale` route
- Renders: `OUTBASE=tmp/wallnum CAM=player_lock FRAMES=170 bash scripts/run_wr2_playback.sh wr3_after pre boss B 74000802 wallnum_AFTER`
- L7 byte-identity: `tmp/wallnum/l7/frames/l7_{BEFORE,AFTER}.png`

---

## §7 — At Matt's eye

1. **The wall.** Does the band read as continuous masonry from inside? The course *size* matches the
   wall by measurement; the *phase* does not and cannot. If the step-out reads as a second wall
   rather than a thicker one, the lever is the pilaster tint and the period, both one constant.
2. **The numbers.** 8.5 % / 10.5 % of frame height is the anime register; it is also large. One
   constant each if it is too much or not enough.
3. **The font.** §3.5 — one pick, one download authorisation. Nothing was fetched.
4. **The south wall** (§2) — now observable, and it will render as an unshaded flat plate in every
   translated room. Design call, not a patch.

*The wall stood where it always stood. What was taken away was the thing put in front of it — and
what went up in its place is the wall's own brick, cut to the wall's own course, measured off the
wall itself.*
