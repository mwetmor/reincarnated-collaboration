# WALLTOP-READ — the lighter band on top of the walls, and why the daylight never lands on it

> **Cell:** WALLTOP-READ. **Agent:** galadriel. **Conductor:** gandalf (LR/presentation session).
> **Date:** 2026-07-30. **Contract:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` Scope 10.
> **Question (Matt, verbatim intent):** *"why is there a lighter shadow on the top of the walls
> before the dark void shadow? We had agreed on daylight on top of the walls before the void
> shadow at the edges."*
>
> **Mode: READ-ONLY.** `~/Games/reincarnated-godot` was not written to — drax holds the
> single-writer lock under BEAUTY-CORNER. **No render was taken this cell.** Every number below
> comes from reading scene SOURCE and from pixels in frames that already existed. Writes are
> confined to `agentic_orchestration/galadriel/`.
>
> **Survey-mode discipline:** §0–§7 are FINDINGS. §8 is the only section carrying a
> recommendation, and it is marked as such.

---

## §0 — The answer in one paragraph

The lighter band is the **wall-top void cap** — `_make_walltop_cap()` in `kit_replica_level.gd`,
wearing `walltop_void.gdshader`. That shader's first line of render state is
**`render_mode unshaded`**, and its own header says why: *"Rendered UNSHADED so the gradient is
fully controllable (lighting can't lift the outer black back up)."* So the band is not a shadow
and not a light: it is the constant `stone_tex × stone_tint(0.66, 0.58, 0.48)`, ramped to pure
black across the outer half of the cap by `split_frac 0.50 / feather 0.14 / black_point 0.0`.
The two things Matt is describing — *a lighter band, then the dark void* — are the **two halves
of one 0.45 m shader**, authored that way. The S14 cold sky-leak he is remembering is real and is
in the render path, but it is a `DirectionalLight3D`, and **no light of any kind reaches an
unshaded surface**. The walltop has never received daylight, in any harness, on any day.

**And the picture carries the inversion plainly:** in the same frame, the walltop surface that
*is* lit reads **L = 14.8**; the walltop surface that *cannot be* lit reads **L p50 = 52.0**.
The unlit band is **3.31× brighter than the lit one**. That is the whole complaint in one ratio.

**Hypothesis verdicts: H1 REFUTED · H2 REFUTED · H3 REFUTED · H4 REFUTED.** A fifth, not on the
conductor's list, survives and is named **H5 — unshaded by construction** (§2).

---

## §1 — What the frame actually contains, band by band

Read at the CAM-LOCK/`player_lock` camera Matt is watching:
`tmp/wallnum/frames/wallnum_AFTER_0128.png`, going outward from the room toward the void. Bands
are identified **by the WALL-FIX BEFORE/AFTER ablation**, not by colour — the cap is the run that
did *not* change when drax textured the slabs. Mask validation plate:
`captures/2026-07-30-walltop-read/PLATE_bandmask_validation.png` (magenta = cap, green = slab top).

| band (outward →) | what it is | mean sRGB | L mean / p50 / p95 | WALL-FIX Δ |
|---|---|---|---|---|
| slab INNER face | the R-WR1-21 band, now brick (drax) | (114.9, 64.9, 33.1) | 73.2 | max 142 |
| **slab TOP face** — the LIT walltop | `StandardMaterial3D`, brick triplanar | (13.5, 14.4, **22.7**) | **14.8** / 14.9 / 17.9 | **max 21, mean 16.3, 100 % of px** |
| **the LIGHTER BAND** — the cap | `walltop_void.gdshader`, **unshaded** | (**55.7**, 48.1, 38.9) | **49.1** / **52.0** / **65.5** | **max 1, 0.00 % of px > 2** |
| void beyond | env residue | (0.4, 0.3, 0.2) | 0.28 | — |

Two readings settle two hypotheses on that table alone:

- **H2 (the slabs' own top faces) is REFUTED.** The slab tops are the band *below* the lighter
  one — they are the **cool navy** strip, and they moved by mean 16.3/255 on **100 %** of their
  pixels when WALL-FIX landed. The lighter band moved by **max 1/255 on 0 % of its pixels**. It
  predates WALL-FIX entirely and is untouched by it.
- **H3 (glow-rim misread) is REFUTED by two orders of magnitude.** The declared beyond-wall glow
  rim measures **mean 0.55/255, max 2** (my re-measure of drax's own newly-lit set). The lighter
  band measures **mean 49.07/255, max 66**. **89.2× apart.** Different object.

**Geometry corroborates the identity independently.** Calibrating px/m per column off the slab
top's known 0.750 m depth (34.7–37.3 px/m at this camera), the lighter band's projected world
depth is **0.375–0.389 m** across clean columns. The cap's own arithmetic predicts
0.225 m (lit half, `CAP_DEPTH 0.45 × split_frac 0.50`) + 0.1125 m (wall half-thickness, the cap
seats from the wall centreline) + feather ≈ **0.34–0.40 m**. It is the cap, at the cap's size.
It is emphatically not a 0.750 m slab top.

---

## §2 — H5: the mechanism, read off the shader

`scripts/walltop_void.gdshader`, render state line, verbatim:

```
render_mode unshaded, cull_disabled, blend_mix, depth_prepass_alpha;
```

and the fragment stage, verbatim:

```
vec3 stone = texture(stone_tex, v_uv).rgb * stone_tint;
float fade = smoothstep(split_frac - feather, split_frac + feather, v_t);  // 0 inner .. 1 outer
float lum  = mix(1.0, black_point, fade);   // 1 lit .. black_point
ALBEDO = stone * lum;
```

There is no light term. `ALBEDO` is written and, under `unshaded`, is what ships to the
tonemapper. The parameters, from `_build_walltop_cap_mat()`
(`kit_replica_level.gd:1610` — and character-for-character the same function at
`walltop_level.gd:598`):

| parameter | value | consequence |
|---|---|---|
| `stone_tint` | `(0.66, 0.58, 0.48)` | a **warm** grey multiplier |
| `split_frac` / `feather` | `0.50` / `0.14` | lit inner half, straight boundary at mid-cap |
| `black_point` | `0.0` | outer half ramps to **pure black** |
| `world_uv_period` | `1.125` m/tile | (see §6 — 2× finer than the wall face's measured 2.32) |

So the band Matt is pointing at, and the void immediately outside it, are **one shader doing
exactly what it was written to do**. The design intent is sound in its own lineage — dissolve the
wall edge into void so the viewer cannot tell wall from open space. What it cannot do, by
construction, is accept daylight.

---

## §3 — The discriminating ablation: the S14 daylight does not touch the walltop

The PROVISION-CAL bank contains the exact A/B. Seven plates resolve to **two** render states by
sha256 — a clean natural experiment, same camera, same geometry, lighting-only:

| state | files |
|---|---|
| **Key = 0.00** (no sky-leak) sha `992a1ccfba933b34` | `frames/v2_A.png` · `frames/afterB.png` · `REVIEW/02_AFTER_crypt.png` |
| **Key = 0.06** (S14 cold sky-leak, Matt-ADOPTED 2026-07-28) sha `12beadd132d4ea05` | `REVIEW/04_VARIANT_cold_skyleak.png` · `frames/s14.png` · `frames/v2_B.png` · `frames/final_B.png` |

Switching the sky-leak on moves **510,495 of 921,600 pixels**. Where it moves them:

| surface | n px | max Δ | mean Δ | px with Δ > 1 |
|---|---|---|---|---|
| **WALLTOP CAP band** | 7,502 | **1** | **0.054** | **0.00 %** |
| interior wall face (brick) | 112,366 | 10 | 3.321 | 53.29 % |
| floor | 348,652 | 14 | 5.800 | 89.37 % |

**The S14 "daylight" lands on the floor, reaches the wall faces, and delivers 0/255 to the wall
tops — on 0.00 % of cap pixels.** This is the measurement the cell turns on. Matt's memory of the
agreement is accurate; the agreement was ruled on a mechanism that never reached the surface it
was ruled about.

### 3.1 The same result at the widest lighting delta the project has

CEILING-1's false sun → the crypt is the largest lighting change in this codebase's history
(`Key` 2.00 warm → 0.06 cold, lighting-only, same R-6 camera):

| | walltop cap (n = 7,735) | floor (control, n = 348,652) |
|---|---|---|
| Key 2.00 warm false sun | L p50 **53.19** | L p50 **93.27** |
| Key 0.06 cold S14 | L p50 **52.12** | L p50 **26.67** |
| **relative move** | **−2.0 %** | **−71.4 %** |

The room's entire lighting identity was replaced. The floor moved 71 %. **The band moved 2 %** —
and that 2 % is bloom spill from surroundings 3.5× brighter, not direct light (mean Δ 1.798 on the
cap vs 66.724 on the floor, a **37× ratio of response**). Declared rather than rounded to zero.

---

## §4 — H1 refuted: this is not a harness split. There is nothing to port.

The WALL-READ finding does not repeat here, and it is worth saying so plainly because it was the
conductor's lead hypothesis and mine.

1. **`walltop_level.gd` is not a different treatment.** It loads the same
   `res://scripts/walltop_void.gdshader` (`VOID_SHADER`, line 51) and its
   `_build_walltop_cap_mat()` sets the *same* `stone_tint (0.66, 0.58, 0.48)`, `split_frac 0.50`,
   `black_point 0.0`. `kit_replica_level.gd` line 81 loads the same shader with the same
   constants. `grep -rn "walltop_void.gdshader" scripts/` returns exactly these two consumers
   plus the `.tscn` emitter. **There is no walltop-daylight function anywhere to port.**
2. **The cap IS built in `wr2_playback`'s render path.** The wallnum run log shows
   `wr1_level` → `kit_replica_level` building all four rooms, and `_build_walls_and_caps()` builds
   a cap per bay unconditionally. The band Matt is looking at is proof of it.
3. **The sky-leak Key IS in the wr2 path.** `wr1_level.gd:201` sets
   `lvl.include_global_lighting = (i == 0)`; room 0 constructs the `Key` directional, and a
   `DirectionalLight3D` is scene-global — it lights room 3 (the boss room WR3 renders) regardless
   of which room built it. Nothing is missing from the harness.
4. **The picture is the same in both harnesses.** `ZOOM_pclight_S14_walltop.png` (kit_replica,
   R-6, 2026-07-28) and `ZOOM_wallnum_walltop_bands.png` (wr2_playback, player_lock, 2026-07-30)
   show the identical warm-grey band before the void.

---

## §5 — H4 refuted: the band is not crushed daylight. It is a constant, and it proves itself twice.

H4 asked whether the S14 treatment is present but reading grey under the current stack (AMB-HUE's
42.7 % dimming, filmic tonemap). Two independent measurements say no.

**(a) Cross-stack invariance.** Between the two frames below, the room changed from 17.5 m to
37.5 m, the camera changed, the ambient went warm → purple (−42.7 % luma), four sconces became
twelve, and two days passed:

| frame | cap n px | L p50 | L p95 |
|---|---|---|---|
| pclight `04_VARIANT_cold_skyleak`, 2026-07-28, kit_replica / R-6 | 7,735 | **52.12** | **65.63** |
| wallnum `AFTER_0128`, 2026-07-30, wr2_playback / player_lock | 203 | **51.98** | **65.47** |

**0.3 % apart at p50, 0.2 % at p95.** A surface that responds to light does not do that. *(The
wallnum n is small — 17 clean columns survive the flame/UI/particle rejection at that camera. It
is the agreement with the 7,735-pixel pclight set that carries the claim, not the 203 alone.)*

**(b) Chroma.** If the band carried the S14 daylight it would carry the S14 daylight's colour.
Linear R:G:B ratios:

| | ratio R : G : B |
|---|---|
| **predicted UNLIT** = `stone_tex` linear mean × `stone_tint(0.66,0.58,0.48)` | **1.864 : 1.446 : 1.000** |
| measured lighter band, wallnum | **1.976 : 1.445 : 1.000** |
| measured lighter band, pclight | **2.044 : 1.488 : 1.000** |
| S14 sky-leak `light_color (0.55, 0.66, 0.95)` | **0.296 : 0.442 : 1.000** |
| measured **slab top** — the LIT walltop surface beside it | **0.503 : 0.544 : 1.000** |

The band is **warm and matches the tint prediction to 6 % in R and 0.1 % in G**. The daylight is
**cold** — the exact opposite ordering. And the surface immediately inboard of the band *is* cold,
i.e. it is receiving the room's cool light budget. The band is not crushed daylight. It is the
tint constant, arriving at the display unmodified.

---

## §6 — Two findings the survey turned up on the way (not answers to today's question)

1. **The band is the one warm surface in the room that no fire makes.** Matt's own standing
   ruling (2026-07-28, quoted in `kit_replica_level.gd`): *"warm belongs only where fire lives."*
   `stone_tint (0.66, 0.58, 0.48)` is warm, unshaded, and rings the entire room perimeter. After
   AMB-HUE completed the cool-room / warm-source split, this band is the last element left on the
   wrong side of it — and it predates the ruling, so nothing violated anything; it was simply
   never swept.
2. **Cap/face brick period divergence, confirmed from the other end.** Drax flagged
   (`wall-fix-num-pop.md` §1.1) that the cap's `world_uv_period = 1.125` does not match the wall
   face's measured 2.32 m/tile. Confirmed here from the pixels: the band's coursing is visibly
   ~2× finer than the masonry below it, which is part of why it reads as a *different material*
   rather than as the top of the wall. One constant, and it belongs to whoever takes the band.

---

## §7 — What a render would have added, and what it would not

- **Would settle:** the predicted appearance of a *lit* cap (§8 arithmetic). I predict from the
  neighbouring surface rather than from a render, and say so.
- **Would settle:** whether the E4 skylight (`SKY_COLOR (0.620, 0.740, 1.000)`, energy ≈ 7.6),
  which BEAUTY-CORNER is landing right now, changes the walltop picture. It cannot lift the cap
  — `unshaded` is categorical — but it will change everything around it, so the *contrast* Matt
  is objecting to may read differently in the very next watch. Flagged so nobody is surprised.
- **Would NOT settle anything already closed.** §3's ablation, §5's cross-stack invariance and the
  shader source are three independent legs on one conclusion.

**Reproducibility:** `galadriel/pipeline/…` is not the home this cell used — the probe sits with
its evidence at
`agentic_orchestration/galadriel/captures/2026-07-30-walltop-read/walltop-read-probe.py`
(`python3 walltop-read-probe.py`; absolute paths, no args). Raw output: `probe-output.txt`.
Plates: `PLATE_walltop_band_two_stacks.png` (the fastest read) · `PLATE_bandmask_validation.png`
(masks over the raw frame, so no crop can flatter) · `PLATE_pclight_capmask.png` ·
`ZOOM_wallnum_walltop_bands.png` · `ZOOM_pclight_S14_walltop.png`. No file in
`reincarnated-godot` was written; band masks are walked per-column from the void, not hand-drawn.

---

## §8 — RECOMMENDATION *(the only non-findings section; clearly separated per survey-mode)*

**Fix class: LIGHTING → BEAUTY-CORNER integration surface.** Named function:
`_build_walltop_cap_mat()` (`kit_replica_level.gd:1610`, twinned at `walltop_level.gd:598`) and
the `render_mode` line of `scripts/walltop_void.gdshader`.

**But `unshaded` cannot simply be deleted, and this is the load-bearing part of the
recommendation.** The measurement predicts the result: the lit walltop surface sitting 0.1 m
inboard of the cap, under this exact lighting stack, reads **L = 14.8**. A cap made lit at the
current Key = 0.06 would land at approximately that value. **Deleting `unshaded` alone converts
the lighter band into the navy band — it retires Matt's complaint and does not deliver his
ruling.** Daylight is not the absence of a constant; it is a light budget the walltop does not
currently have.

Three levers, escalating, for gandalf and Matt to choose between — none of them mine to pick:

1. **Cheapest, inside the existing design (dressing-grade):** `stone_tint` warm → cold, e.g. the
   sky-leak's own `(0.55, 0.66, 0.95)` family. One constant, both twins. Buys the register fix in
   §6.1 and turns the band from *warm stone* into *cold sky on stone*, which is nearer Matt's
   sentence than what ships. It is still a constant, not light. **Peelable, zero risk.**
2. **The honest mechanism (lighting-grade, and the one I would put in front of Matt):** make the
   cap **lit** — drop `unshaded`, keep the outward `lum` ramp as an albedo multiplier so the
   dissolve-into-void at the edge survives byte-for-byte in shape — **and give the walltop a
   motivated light that reaches it.** The Key at 0.06 will not do it (§3: it delivers 0/255 to a
   surface that *can* receive it). Candidates already in the tree: raise `Key` for a walltop-only
   light layer, or aim BEAUTY-CORNER's E4 skylight (`SKY_COLOR (0.620, 0.740, 1.000)`, energy
   ≈ 7.6 — cold pale, exactly the register) so the shaft grazes the wall tops on its way in. The
   second is thematically free: light from the living world breaking into the crypt should touch
   the crypt's rim first.
3. **⚑ Route-to-Matt, do not do quietly:** `Key = 0.06` is a **ruled constant** — variant S14,
   PC-LIGHT-V2 plate B, Matt-ADOPTED 2026-07-28, with its cost measured (contrast 7.63× → 6.83×).
   Raising it to make the walltop daylit **re-opens that ruling**, and the earlier dose-response
   says a directional is a flattener at any energy. If lever 2 is taken, it should be taken as a
   **walltop-scoped light**, not by turning the room's adopted Key up.

**Sequencing:** this is the same surface BEAUTY-CORNER is standing on right now (shadows, fog,
E4 skylight, player-light bake-off). It should be folded into that cell's integration pass rather
than chartered separately — and, per the WALL-READ precedent, it should be settled **before** the
integrated hand-off watch, because the wall tops ring every frame of the `player_lock` camera and
they are the boundary every one of those three elements will be judged against.

**Acceptance metric, already instrumented:** the walltop band's L p50 should stop reading
**52.0 while the lit surface beside it reads 14.8**. Whatever ships, the two walltop bands should
land in the same decade — and the band's linear chroma ratio should stop reading **1.98 : 1.45 :
1.00** (warm) and start reading below 1.00 in R:B (cold). Both numbers come straight back out of
`walltop-read-probe.py`.

---

*The Mirror shows twelve fires burning in a room, and a pale ribbon running the whole way round
the top of its walls — and the ribbon is not lit by any of them. It was painted that colour and
told to hold it, so that the darkness past it would stay obedient. What Matt calls a lighter
shadow is neither lighter nor a shadow: it is the only thing in the room the light was never
allowed to touch.*
