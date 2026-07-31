# INTEGRATE-PREP — the font Matt picked, the daylight he was promised, a wolf's shadow, and six skies

> **Cell:** INTEGRATE-PREP (Part 1 Bangers swap · Part 2 walltop Option A · Part 3 WOLF-SHADOW
> portrait · Part 4 SKY-OPTIONS board). **Agent:** drax (presentation seam).
> **Conductor:** gandalf (LR/presentation session). **Date:** 2026-07-30.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` — Scope 10 (font
> ruling, walltop question) · Scope 11 (walltop Option A, sky ruling HELD, werewolf shadows) ·
> the BEAUTY-CORNER and WALLTOP-READ landing blocks.
> **Consumed:** `galadriel/notes/2026-07-30-walltop-read.md` (the diagnosis Part 2 executes).
> **Inherited:** godot `5b05947` LOCAL (ahead 6). **Shipped:** godot `ec40cdc` LOCAL (ahead 7,
> NOT pushed).

---

## §0 — What this cell says in four sentences

The placeholder font is retired and the swap moved exactly one thing, which is a measurement and
not a hope. The walltop daylight Matt was promised now exists, painted into the cap's ramp with
`unshaded` intact, and its chroma landed on the S14 sky-leak's own direction. The werewolf stands
in the room under both lamp geometries, posed from existing infrastructure, with its projection
ratios re-derived for its own height rather than inherited. And **"22.8" is located: it is
`SKY_ENERGY_REF`, the value already shipping** — so Matt's lean is for the status quo, and the
board now shows him what the status quo is a lean against.

⚑ **Two guard catches this cell, both reported rather than discovered later:** a headless
`--import` silently deleted a `[rendering]` line from `project.godot` (restored, hash back to
start), and the **frozen L7 stage moved for the first time this session** — by design, because the
ruling applies to every room that has wall caps.

---

## §1 — Part 1: the BANGERS swap

**Shipped:** `Bangers-Regular.ttf` + `OFL.txt` carried byte-identically from the staging area into
`Assets/fonts/bangers/` (sha `4160a731…` / `630dd5a3…`, start = end). `NUM_FONT` flipped. The
PLACEHOLDER log line retired.

**⚑ THE FONT DID NOT LOAD ON THE FIRST RENDER, AND MY OWN FALLBACK CAUGHT IT.** Godot had not
imported the `.ttf`, so `load()` returned null and `_num_font_get()` fired its warning —
*"display font not found … falling back to the project default"* — instead of silently rendering
the wrong face. That warning exists because NUM-POP anticipated exactly this. Import run, verified,
re-rendered.

**The swap moved ONE thing, and that is measured, not asserted.** Re-running NUM-POP's own digit
instrument on both faces at **equal cap height**:

| face | ink in digit box | mean stroke | 4 digits, as multiples of cap height |
|---|---|---|---|
| LTMuseum-Bold (placeholder) | 41.1 % | 52.6 px | 2.88× |
| **Bangers-Regular (shipped)** | **52.1 %** | **59.7 px** | **2.46×** |

Bangers is **27 % more ink and 15 % narrower**, and both differences run the safe way for the two
risks the brief named: a fixed-ratio outline eats proportionally *less* of a thicker stroke, and
narrower numerals overlap *less* at stacked hits.

**The sizing needed no compensating constant, for a measured reason:** both faces require the
**same pixel size for the same cap height** (271 px for a 200 px cap). The render confirms the
arithmetic — the new run solves to **`font_size 135, outline 27`, identical to the accepted state's
log line**. Derived-em sizing and the pop envelope are untouched; `NUM_EMBOLDEN` held at 0.08
(Bangers is nominally weight 400 against LT Museum's 700, but the ink measurement says it is the
heavier face in practice, so re-tuning it would have been a second variable).

**⚑ U+25C6 VERIFIED, NOT ASSUMED.** Bangers' cmap read directly: 597 glyphs, **no diamond** — the
brief's suspicion was correct. The `FontVariation.fallbacks` chain serves it, the same chain that
has carried the marker since NUM-POP. The log now names the provider on every run, because a
missing fallback would be invisible until someone noticed a tofu box.

**⚑ ONE INSTRUMENT DISCARDED BY ITS OWN CONTROL.** I built an analytic outline model to predict
counter closure at `outline_ratio 0.20`. It reported the counters fully closed — **for the
currently accepted face as well**, which Matt has already looked at and approved. A model that
fails on the known-good case cannot adjudicate the new one, so it was thrown away rather than
quoted, and the question was answered at the render instead (plate: counters open, outline intact).

---

## §2 — Part 2: WALLTOP OPTION A — the daylight authored into the ramp

**What galadriel established and this cell executes:** the lighter band and the void are two halves
of one painted strip; the remembered daylight was never delivered anywhere (the S14 Key moves
510,495 px of the frame and **0.00 % of cap pixels**), because no light reaches an unshaded surface.

**`render_mode unshaded` STAYS** — stated in the source, at length, so nobody later reads it as an
oversight. Relighting the cap would trade a *guaranteed* dissolve for a merely motivated one, which
is the trade the design already refused. The daylight is therefore **paint**.

**Two light budgets, one of them refused a gradient on purpose:**
- **SKY** — uniform across the cap. A horizontal surface under a directional sky is evenly lit;
  grading it would misstate where the light comes from.
- **ROOM BOUNCE** — inner lip only. The fire-lit room below lights the wall's inner edge and
  nothing lights its outer edge. That is the one honest gradient this surface has, and it puts the
  warm term exactly where Matt's standing ruling allows it (*"warm belongs only where fire lives"*).
  Independently peelable at `bounce_level = 0.0`.

**Chroma picked against a measured direction, and it landed on it.** galadriel measured the S14
sky-leak at linear **0.296 : 0.442 : 1.000** and the old cap at 1.98 : 1.45 : 1.00 — the exact
opposite ordering. Shipped `WALLTOP_SKY_TINT` sRGB (0.49, 0.59, 0.85) at `sky_level 0.62`:

| cap band (the SAME 279 masked px in both frames) | linear R:G:B | L p50 |
|---|---|---|
| BEFORE — legacy warm constant | **2.029 : 1.509 : 1.000** | 50.98 |
| **AFTER — daylight** | **0.303 : 0.402 : 1.000** | **40.81** |

**My BEFORE reproduces galadriel's independent measurement (2.029 vs her 1.98)** — two different
masks, built by two agents from two conventions, agreeing to 2 %. That agreement is what licenses
the AFTER number.

**⚑ I DIVERGE FROM HER RECOMMENDED VALUE METRIC, AND SAY SO.** Her §8 asked that the two walltop
bands "land in the same decade" (cap 52.0 vs lit slab 14.8). Shipped lands at 40.81 vs 11.93 — a
3.4× ratio, still not the same decade. That metric was written for **lever 2** (make the cap
shaded); Matt ruled **Option A** (paint the daylight), and painted daylight from an open sky
*should* out-read a torch three metres below. The metric her fix implied is not the metric his
ruling implies. Her **chroma** metric — the one that discriminates daylight from grey — is met
decisively. `walltop_sky_level` is one constant if his eye disagrees.

**⚑ THE DISSOLVE GUARANTEE IS STRUCTURAL, NOT TUNED.** Everything added multiplies the *tint*; the
outward `lum` ramp is untouched, so at the outer lip `ALBEDO = stone × black_point = stone × 0.0`
— exactly zero whatever the tint is. Measured: **2 px of 259,384 pure-black pixels moved, by 1/255
in blue**, against a **6,587 px per-launch noise floor in the same pair**. Not separable from noise.

**⚑ THE WHOLE-FRAME DIFF WAS UNINTERPRETABLE, AND A NULL TEST IS WHAT PROVED IT.** My first reading
showed 93,778 px changed across every row and "329 guarantee violations" — which would have been
alarming if reported as-is. Two contaminants: **glow** (a post-process that spreads the cap's change
far past the cap, and can lift previously-black pixels the shader never touched) and the
**per-launch GPU particle seed** (the flag CAM-LOCK narrowed). Both handled: the pair re-rendered
with `--noglow`, and a **NULL TEST** (identical config, two launches) run for attribution:

| threshold | null (noise only) | ablation | ratio |
|---|---|---|---|
| delta > 8 | 7,818 px | 19,376 px | 2.48× |
| delta > 25 | 3,909 px | 9,530 px | 2.44× |
| **delta > 60** | **1,654 px** | **894 px** | **0.54× — ablation BELOW the null** |

At high amplitude the ablation is *quieter* than the null. So the whole-frame diff attributes
nothing, and only the masked cap-band measurement above is evidence. Reported because a number I
cannot attribute is not a result.

**Opt-in by default (`sky_level = 0.0`).** This shader has consumers beyond the two cap builders
(`scenes/kit_replica_r2_dwarven.tscn`, and `build_walltop_void_test.gd` — the v8 reference-frame
harness Matt judged in June). At 0 the fragment stage is arithmetically identical to the pre-ruling
shader, so none of them move a pixel; the daylight is switched on explicitly in
`_build_walltop_cap_mat()`, **in both twins**, sharing one `_apply_walltop_daylight()` helper so
the plain cap and the occlusion-aware twin cannot drift into a half-daylit room.

**⚑ DECLARED, NOT TAKEN:** galadriel §6.2 flagged the cap's `world_uv_period 1.125` against the
wall face's measured 2.32 m/tile — visibly 2× finer coursing, part of why the band reads as a
different material. It is one constant in a file I am authorised to touch. **Not taken**: it is a
*masonry* change, not a *daylight* change, on a wall band Matt has just accepted, and this cell
moves one variable. Routed, with its number, for whoever takes the band next.

---

## §3 — Part 3: WOLF-SHADOW

**Body:** `SK_Chr_Werewolf_01.fbx` — the registered L6 body, 52-bone Synty SK rig (confirmed at
run: `skel_bones=52`), UE-named, 0.0000° mean AND max rest-Δ, R-PC-4 caster.

**Loaded through `VHCaster`, not by path — three reasons, all load-bearing:** it carries the R-PC-8
exclusion of `SM_Werewolf_01.fbx` (so this probe cannot pick up the forbidden body by a typo); it
carries `MODEL_FORWARD_YAW`, the 180° facing defect Matt's eye caught on the race strips and which
the 0.0000° retarget metric was structurally blind to — **in a silhouette test, facing is the entire
subject**, and a fresh loader would have silently re-introduced it; and it carries the R-PC-7 albedo
repair by *not* applying a material_override.

**POSE METHOD (declared, per the brief):** the retargeted base-locomotion **WALK clip seeked to
stride phase 0.34 and frozen** (`pause()`), plus **`vh_arm_raise` blended at 0.55** to lift the
forelimb clear of the torso so the claw spread is outside the body line. Both are existing,
Matt-reviewed assets driven through their existing API. **No bone was rotated by hand and no clip
was authored.** Bind pose refused per the brief; an idle was also refused, because it folds the
limbs against the torso — the worst possible state for a silhouette.

**⚑ THE PROJECTION RATIOS ARE RE-DERIVED FOR THIS BODY, NOT INHERITED.** BEAUTY-CORNER measured
5.11× for a 1.85 m armoured humanoid. The werewolf is frozen at **1.80 m** (R-PC-8 — this cell does
not resize the ruled body to make a number tidy), so:

| condition | lamp | ratio | what it delivers |
|---|---|---|---|
| (a) wall torch | 2.30 m | **4.60×** | mass and gait; the far end smeared along its own length |
| (b) skylight pool | 15.0 m | **1.136×** | ears, muzzle, claw spread, back fur line hold proportion |

Printed per run from the constants actually in force, so a label cannot drift from its render.

**⚑ A FRAMING I GOT WRONG, AND THE FIX IS GENERAL.** The first camera stood broadside to the shadow
axis — textbook — and **rendered the inside of a wall**. The subject stands in a corner, so at the
derived radius *both* perpendiculars are through masonry (|z| = 19.4 m against a half-edge of
18.75). Geometry that is correct about the SUBJECT can still be wrong about the ROOM. Fixed by
choosing the perpendicular nearer the room's middle and then **pulling the radius in per sample
until the eye is genuinely inside** — which also keeps every frame of the orbit legal rather than
only the first.

---

## §4 — Part 4: the SKY-OPTIONS board, and "22.8"

**⚑ "22.8" IS LOCATED. It is `kit_replica_level.gd::SKY_ENERGY_REF := 22.8`** — the skylight energy
reference, and the **×3 rung of the energy ladder BEAUTY-CORNER solved E4's intensity on** (base
7.6: ×1 → pool peak 95, ×3 → 117, ×6 → 124; ×3 is the last rung that is still a pool rather than a
second sun). It survives on disk as that ladder's own render, **`tmp/beauty/SKY_22.8.mp4`**, beside
its sibling **`SKY_45.6.mp4`** — almost certainly the pair Matt was looking at when he named it.

**Consequence, and it matters for how his ruling should be framed: his lean is for the intensity
that is already shipping.** Tile **B** of this board *is* the current state. He is not choosing a
change; he is being asked to confirm a value against alternatives he has not yet seen.

**The board's one rule: every variant is the same skylight wearing a different look.** Same room
(3 — the boss room the watch renders), same seeded motif (**oculus-ring**, the circle he has already
seen and liked), same azimuth, pool, mask rotation, camera and beauty stack. **Only temperature and
intensity move.** If the motif varied too, a preference for one tile would be uninterpretable.

| | SUBTLE (11.4) | ASSERTIVE (22.8) |
|---|---|---|
| **COLD PALE** (0.620, 0.740, 1.000) | A | **B ← shipped + Matt's named lean** |
| **NEUTRAL OVERCAST** (0.880, 0.900, 0.930) | C | D |
| **WARM DAWN** (1.000, 0.870, 0.680) | E | F |

Neutral overcast is in the grid as the **control**: without a no-opinion tile, "cold" and "warm" are
only being judged against each other.

**The seeded per-room energy spread is preserved under an override**, not replaced by a flat number
(`energy × room_draw / SKY_ENERGY_REF`) — so room 3 keeps its own 0.9075 draw and the board shows a
level the shipped system can actually produce. Every tile carries its parameters **on-frame**: a
contact sheet with the numbers in a side document is six pretty pictures.

**⚑ AN OBSERVATION THE BOARD MAKES BY ITSELF:** the warm-dawn tiles (E/F) **nearly dissolve into the
twelve orange sconces**. That is the separation argument — the mechanical reason for a cold
shaft — rendered as a picture rather than argued in prose. It is a finding, not a recommendation;
Matt rules.

**NO VARIANT SHIPS.** Both override hooks mean "use the constant" when unset. SKY-2 (circle-up,
shutter-slits, dust, parallax) is chartered and **FROZEN** until his ruling; not built.

---

## §5 — Guards

| guard | result |
|---|---|
| collision check at cell start (`git status`) | **clean** — tracked tree empty; untracked scratch only |
| `walltop_void_radial.gdshader` / `walltop_occlude.gdshader` | `2710fc11…` / `d29a01be…` — **unchanged** |
| all `vfx/ambient/pp/*.tres` (Matt-accepted rise + hue) | rollup `53be166b…` — **byte-identical start to end** |
| kit textures `Brick_Small_01` / `Floor_Tiles_01` | `5692f885…` / `e28e6bcc…` — **unchanged** |
| ref mp4 `tmp/wr2/wr3_after_pre_boss_B_74000802.mp4` | `910063d1…` — **intact** |
| traces | **READ-ONLY** — zero fight/trace semantics moved |
| engine tree | **never opened** — zero writes |
| protected dirs (eleven) | **no evidence touched** — see the finding below |
| godot commit | **LOCAL, ahead 7, NOT pushed** |
| **declared authorised surfaces** | `NUM_FONT` constant · `walltop_void.gdshader` · both `_build_walltop_cap_mat()` twins + pass-throughs · sky-variant override params · new probe scenes in `tmp/integ/` |

### 5.1 ⚑ GUARD CATCH 1 — `project.godot` was silently edited by Godot's own importer

The end-of-cell hash did not match the start hash (`6bef17eb…` → `a76d666a…`). The headless
`--import` run needed for the font **deleted a `[rendering]` section**:

```
-[rendering]
-mesh_lod/lod_change/threshold_pixels=1.0
```

That is a deliberate LOD-popping setting, not noise, and nothing in this cell authorised touching
it. **Restored via `git checkout`; hash back to `6bef17eb…` exactly.** Re-verified afterwards that
both the font load and the walltop state still fire correctly (they do — the `.import` sidecar is a
separate file). Recorded because the only reason this was caught is that the guard hashes a file
nobody expected to move.

### 5.2 Protected dirs — thousands of "newer" files, zero evidence touched

`find -newer` reported 1,058 newer files in `tmp/beauty`, 2,715 in `tmp/ambrise`, 4,655 in
`tmp/wr2`. **All of them are Godot import sidecars generated by that same `--import` scan**
(`.import`, `.uid`, `.translation`). Verified three ways: by extension census (1,056 `.import` +
2 `.uid` in `tmp/beauty`, zero other files); by `git ls-files` (all untracked — newly generated,
nothing overwritten); and by mtime on every prior cell's deliverable mp4 (`tmp/camlock` 18:02/18:20,
`tmp/ambhue` 18:50, `tmp/beauty/clips` 20:03 — all **before** this cell started at 20:12).
The one write into a protected dir that BEAUTY-CORNER flagged (`tmp/wr2/pl_audit.json`) did **not**
recur: this cell's audit wrote to `tmp/integ/pl_audit.json`, and `tmp/camlock/pl_audit.json` is
untouched at 18:14.

### 5.3 ⚑ GUARD CATCH 2 — the frozen L7 stage MOVED, by design, for the first time this session

Every cell since AMB-REFIT has reported the L7 stage byte-identical (`398421737359c331…`), including
across a day boundary. **This cell breaks that**, and the reason is the ruling itself: the L7 stage
is built through `kit_replica_level.gd`, it has wall caps, and Matt ruled the wall caps.

| | value |
|---|---|
| L7 stage sha | `398421737359c331…` → **`5f92aa9130389183…`** |
| px changed | **127,657** of 921,600, max channel delta 41 |
| LSTAT-2 stage mean luma | 23.317067 → **22.898919** (**−0.418148, −1.79 %**) |
| changed-region chroma | linear R:B **5.122 → 2.083** (the caps going cold) |

**The attribution is total and needs no null test**, precisely because prior cells proved this
render byte-stable across launches and days — so 100 % of the delta is this cell's. Declared as an
**authorised LSTAT-2 delta, not smoothed**, on the BEAUTY-CORNER E3 precedent (a ruled visual change
is *supposed* to move the datum; LSTAT-2 exists to catch the unintended kind). Peelable with one
flag (`walltop_daylight = false`) if the conductor wants the datum restored instead.
Measured in `tmp/integ/l7/`, **not** by writing into the protected `tmp/beauty/l7/`.

---

## §6 — Deliverables — `~/Games/reincarnated-godot/tmp/integ/`

**THE DECISION SURFACE, FIRST (Matt's held ruling):**
1. **`plates/PLATE_SKY_OPTIONS_board.png`** — the six-tile board, parameters on every frame, tile B
   outlined gold as his named lean *and* the shipped value.
2. **`clips/SKYOPTIONS_cycle_ABCDEF.mp4`** — the same six cycling, ~2.6 s each, labels visible.

**THE WOLF (M-EYE motion):**
3. **`clips/WOLF_torch_4.60x_orbit.mp4`** — slow orbit, wall-torch condition.
4. **`clips/WOLF_skylight_1.14x_orbit.mp4`** — slow orbit, skylight condition (the detail read).
5. `plates/PLATE_wolf_shadow_two_conditions.png` · `plates/PORTRAIT_wolf_torch.png` ·
   `plates/PORTRAIT_wolf_skylight.png`

**THE TWO SWAPS:**
6. **`plates/PLATE_walltop_before_after.png`** — before/after at a wall-adjacent camera, glow off,
   with the boxed zoom and the chroma numbers.
7. **`plates/PLATE_numbers_bangers_swap.png`** — same seed/leg/camera/frame 0121, numerals only.

**INSTRUMENTS + MEASUREMENT ARTEFACTS:** `wolf_probe.gd` / `.tscn` / `run_wolf_probe.sh` ·
`sky_probe.gd` / `.tscn` / `run_sky_probe.sh` · `walltop_check.py` (the mirrored cap-band mask) ·
`lstat_rig.gd` (copied out of the protected dir) · `l7/l7_daylightON.png` · `frames/` · `logs/`.

**Peels:** `--no-walltop` (whole ruling) · `--skylevel <f>` (the value ladder) ·
`walltop_bounce_level = 0.0` (the warm inner lip alone) · `NUM_FONT` (one constant).

---

## §7 — At Matt's eye

1. **THE SKY BOARD.** Six labelled options; his lean (B) is the shipped state. One ruling unfreezes
   SKY-2. Note E/F: a warm shaft does not separate from the sconces.
2. **THE WALLTOP.** Chroma is decisively cold and on the S14 direction. The band is still 3.4×
   brighter than the lit surface beside it — deliberate under Option A (painted daylight from an
   open sky out-reads a torch), and one constant if he wants it quieter.
3. **THE WOLF.** Anatomy reads under the skylight at 1.14×; at a wall torch 4.60× the silhouette
   carries mass and gait but smears. Same finding as the armoured probe, same cause: geometry.
4. **THE L7 DATUM MOVED** (§5.3) — authorised and declared, peelable if the conductor prefers.

*I asked a whole frame what my change had done and it gave me a confident, contaminated answer.
The null test said the loudest pixels in that answer were not mine at all. The mask was the only
honest instrument in the room, and it was galadriel's, turned inside out.*
