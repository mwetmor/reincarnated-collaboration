# TCP-L7-V — mode (ii) VFX DESIGN ARRIVAL — report

**From:** drax (presentation seam) · **To:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l7v-vfx-arrival.md`
**Floor:** `~/Games/mcp-lab/l7vfx/` (created by this cell) · **Verdict: PASS with two ceilings found.**

---

## §0 — TL;DR

The brief was *"make the crypt feel inhabited."* I parsed the substrate before reading any
description of it and found that the room is **empty** — 296 nodes, every one of them floor,
wall or corner post — and that it contains **one warm OmniLight at (0, 2, 0) that nothing in
the room makes.** The answer I arrived at is therefore not "add atmosphere": it is **give that
light a source.** A campfire on the bare floor at the centre, four smaller fires at the corner
posts, and the air and ground disturbance a fire causes.

Two ceilings found, both of which I consider more valuable than the clip:

1. **CEILING-1 (scene, not tool).** The substrate is lit as a *daylit exterior court*, not a
   crypt: a 2.0-energy directional key through a roof it does not have, giving a median lit
   pixel of **88/255** and only 4.66× contrast. Additive firelight cannot own a room it cannot
   out-shout. Every "make it feel lit-by-fire" technique is capped by this, and no VFX authoring
   fixes it — only a lighting change to the stage would, which R-5 forbids.
2. **CEILING-2 (camera, not tool).** At the ARPG camera's −50° pitch, **a vertical effect is
   always seen against the floor, never against the sky.** Smoke's entire contrast budget is
   |smoke − floor|, and this floor is mid-grey — the worst case. The plume I authored at i5 was
   *invisible*. The fix was not more alpha, it was **moving the volume onto the ground plane.**

Both were found by measurement, not by taste, and both are stated with the measurement attached.

**And one result that is bigger than either, and that I went looking for only because the dispatch
told me to declare a tolerance:**

3. ★★ **GLOW IS INNOCENT. SDFGI is the accumulator.** The shipped clip renders with the
   substrate's **glow ON**, 673 GPU particles and 5 animated lights, and re-renders **120/120
   byte-identical — the MP4s share a sha256.** I then isolated the features one at a time:
   glow, glow+SSAO, glow+SSIL, glow+volumetric-fog are **all** byte-identical; **glow+SDFGI is
   0/30**, with an exact fingerprint match for the 0/90 the harness recorded. The lockout's causal
   element is SDFGI. §2.3's *"Most VFX wants glow, so decide whether this cell buys glow at the
   price of a tolerance"* has been charging cells for something glow does not cost — and the
   original misattribution is **in a code comment I wrote myself** (§3).

**The tolerance I declared, correctly and in advance, turned out to be unnecessary.** I report that
as a falsified pre-registration, because TOLERANCE.md §3 pre-committed me to.

---

## §0.5 — Evidence index (§3.3)

| § | artefact | path |
|---|---|---|
| 3.3 | **THE ANSWER, AS MOTION** — 4.0 s @ 30 fps, 120 frames, step mode, play camera | `mcp-lab/harness/out/l7v_after/l7v_after.mp4` (+ `.gif`, `frames/`) |
| 3.3 | film-strip, 12 timestamped thumbs | `mcp-lab/harness/out/l7v_after/l7v_after_strip.png` |
| 3.3 | the same world **without** the pass, same camera, same settings | `mcp-lab/harness/out/l7v_before/` |
| 3.3 | **`__box` still, AFTER** — 1920×1080, fov 20 / yaw 47 / pitch −50 / dist 50 | `mcp-lab/l7vfx/evidence/BOX_STILL_after.png` |
| 3.3 | `__box` still, BEFORE, and the A/B plate | `…/BOX_STILL_before.png`, `…/box_ab.png` |
| 6 | iteration ladder — BEFORE ǀ i1 ǀ i6, same frame, same camera | `mcp-lab/l7vfx/evidence/iteration_ladder.png` |
| 3 | determinism, run A vs run B | `mcp-lab/l7vfx/evidence/determinism_rerun.json` |
| 4 | cost account, raw | `mcp-lab/l7vfx/evidence/cost.json` |
| 3.1 | FIRST_INTENT, banked before recon | `mcp-lab/l7vfx/FIRST_INTENT.md` |
| 3.2 | tolerance, timestamped before the first frame | `mcp-lab/l7vfx/TOLERANCE.md` |
| — | **the pass itself** | `mcp-lab/l7vfx/vfx/crypt_vfx.gd` |
| — | stage loader (absolute-path, no `res://` coupling) | `mcp-lab/l7vfx/vfx/stage_lib.gd` |
| — | capture clip (serves both A and B) | `mcp-lab/l7vfx/clips/l7v_crypt.gd` |
| — | cost bench | `mcp-lab/l7vfx/bench/bench.gd` |
| — | instruments: geometry derivation, A/B stats, magnifier, plates, exit checks | `mcp-lab/l7vfx/scripts/` |

**The answer in one line:** `CryptVFX` — 12 GPU particle systems, **673 particles**, **5 flickering
omni lights**, **+12 draw calls**. One campfire at the room's centre under the light it explains,
four smaller fires at the corner posts, embers climbing out of a roofless room, and a low
ground-hugging thermal that stops the floor reading as a uniform tile sheet.

---

## §1 — Clock (§3.1, §3.6) and FIRST_INTENT

| | |
|---|---|
| **Authoring clock START** | `2026-07-25T22:30:22Z` (18:30:22 EDT), epoch 1785018622 |
| **FIRST_INTENT banked** | `~/Games/mcp-lab/l7vfx/FIRST_INTENT.md`, before any recon whatsoever |
| **Tolerance declared** | `2026-07-25T22:35:43Z` — see §3, **before the first frame** |
| **Authoring clock CLOSE** | `2026-07-25T23:44:43Z` (19:44:43 EDT) |
| **Total wall** | **1 h 14 m** |

**Split — where the time actually went.** Per TCP-32 the clock includes thinking and reading,
and prior cells found execution is a small single-digit fraction. That held here:

| phase | share | note |
|---|---|---|
| Reading (dispatch, harness source, substrate parse) | **~12 min** | |
| **Design thinking + judging renders** | **~22 min** | the dominant cost, as predicted |
| Writing code | **~22 min** | ~700 lines of GDScript + 4 Python instruments |
| Machine execution (renders + bench, unattended) | **~9 min useful** | **plus 31 min LOST to my own blunder — §9** |

**FIRST_INTENT vs what I shipped — pre-registration scored honestly:**

| # | pre-registered | outcome |
|---|---|---|
| 1 | "Fire that somebody lit… the load-bearing element" | **HELD.** Unchanged from first line to last. |
| 2 | "Air that carries… subordinate" | **HELD but demoted further.** Room-wide motes contributed almost nothing (§6). |
| 3 | "Something that moves with intent, not physics" | **HELD, and became the cheapest win** — light flicker, 3 sines, ~0 cost. |
| 4 | "I predict my first pass will be too fine and I will have to make everything bigger and slower" | **CORRECT.** i1→i4 is exactly this. |
| 5 | "I predict I will buy the glow tolerance" | **CORRECT, but for a reason I had not foreseen** — see §3. |
| 6 | "The cost account will be boring… the risk is lights, not particles" | **HALF WRONG, and the miss is the interesting part** — see §5. |
| 7 | "Not going to make it scary. Inhabited ≠ haunted" | **HELD**, and it is the register-note finding — see §8. |

---

## §2 — The stage, derived (dispatch §2.2 forbade a conductor's description, correctly)

Parsed from the `.tscn` text with `scripts/derive_geometry.py` + `derive_detail.py`, then
**confirmed against the live engine** by `clips/probe_stage.gd` (the engine's own node census and
world AABB, not my parser's).

- **A square stone court, 17.5 × 17.5 m of floor** — a complete 14 × 14 grid of 1.25 m tiles
  spanning −8.75…+8.75, floor top at y = 0. Engine world AABB `(−9.317, −0.093, −9.317)` →
  `(9.317, 3.343, 9.317)`.
- **Checked for an L5-style hole: there is none.** 196 of 196 grid cells occupied, zero missing.
- **Walls** on all four sides — 7 segments per side × (inner at ±8.86, outer at ±9.09) = 56, plus
  28 `WallCap` boxes of 2.5 × 0.16 × 0.45 at y = 3.09. A 0.23 m shell.
- **The room has no ceiling.** Nothing exists above y = 3.17.
- **4 corner posts** at (±8.97, 0, ±8.97) with toppers at y = 3.08.
- **Lights: three.** `Key` DirectionalLight3D energy 2.0 warm, shadows ON, pointing steeply down
  (fwd 0.220, −0.883, −0.415). `Fill` DirectionalLight3D energy 0.45 cool, no shadows.
  **`InteriorPool` OmniLight3D at (0, 2.00, 0), energy 3.4, range 9.0, colour (1.00, 0.85, 0.62),
  no shadows.**
- **Environment:** BG colour, FILMIC tonemap, ambient (0.10, 0.11, 0.14) at 0.35,
  **`glow_enabled = true`, intensity 0.6, bloom 0.12, hdr_threshold 1.25**, and `fog_enabled` with
  a *black* fog (light_energy 0.0) at density 0.015 — a depth-darkener, not a light fog.
- **Materials:** 3 custom wall shaders (`walltop_occlude`, `walltop_void`, `walltop_void_radial`)
  — these are what cut the near walls away so a −50° camera can see into the room. They are
  load-bearing for this cell and any pipeline that loses them loses the shot.

**The two facts the design came from, neither of which is aesthetic:**

1. **The room is empty.** Not sparse — *empty*. Not one prop, not one sarcophagus, not one
   brazier. 288 of 296 nodes are floor/wall/post meshes and the other 8 are lights, environment
   and group nodes.
2. **`InteriorPool` has no source.** A 3.4-energy warm pool sits at head height in the middle of
   a bare room with nothing under it. It is a lighting device that was never made diegetic.

---

## §3 — The tolerance declaration (§3.2, TCP-38 ①) — and a defect in how §2.3 poses the choice

Full text: `~/Games/mcp-lab/l7vfx/TOLERANCE.md`, written `2026-07-25T22:35:43Z`, **before a single
frame was rendered by this cell** (at that moment nothing had been handed to Godot at all).

> **T1 — max per-channel absolute delta ≤ 2**, over all pixels and channels, on every frame.
> **T2 — differing pixels ≤ 1.00 %** of the frame (≤ 9,216 px of 921,600), on every frame.

Derivation, from the harness's own measured numbers rather than from taste: the accumulator noise
floor is **977 px @ max delta 1 = 0.106 %**, and the real-motion scale bar is **150,602 px = 16.3 %
@ max delta 180**. T2 = 1.00 % sits **9.4× above the noise** and **16.3× below the smallest real
signal** — inside a two-decade log gap, marginally conservative of its geometric centre (1.31 %).
T1 = 2 allows exactly **one doubling** of the measured 1-LSB floor, because this clip pushes
emissive additively-blended pixels through the glow path and glow is a blur-and-add. **≥ 3 is not
accumulator noise and I pre-committed to calling it a defect rather than widening the number.**

### ★ The finding: on this stage, §2.3's binary does not exist

§2.3 poses it as a free choice — *"buys glow at the price of a tolerance, or refuses glow to keep
byte equality."* **The substrate ships `glow_enabled = true` in its own `WorldEnvironment`.** So
"refuse glow" is not an option about my particles; it is an instruction to **edit the stage's
authored environment and then judge a lighting model the room does not have.** I refused that and
bought the tolerance — but note the shape of it: **I would owe this tolerance even if my ambient
pass were an empty node.** It is the stage's tolerance, not the effect's.

This is worth propagating to the rest of the lap: **any cell working on this substrate is already
in the divergent regime before it authors anything.** A future dispatch should say "declare your
tolerance" without implying byte-equality is on the table, unless the stage is checked first.

**Measured result vs the declared numbers:**

**120 / 120 BYTE-IDENTICAL. The MP4s share a sha256. The tolerance I declared was not needed —
and finding that out is the most consequential result in this report.**

```
framediff: rerun_identity          out/l7v_after/frames  vs  out/l7v_afterB/frames
  pairs                : 120
  byte-identical       : 120 / 120
  pixel-identical      : 120 / 120
  worst pair           : 0 px changed, max channel delta 0
  scale bar (adjacent frames of the motion, run A): 51,625..68,325 px changed, max channel delta 173
  l7v_after.mp4 sha256 : 5d0b6f94132924b750131946a2aa2b7fbee98efe16abe00bd7c2250cc218e621
  l7v_afterB.mp4 sha256: 5d0b6f94132924b750131946a2aa2b7fbee98efe16abe00bd7c2250cc218e621
```

Manifests are byte-identical apart from `label`, which `shoot_clip.sh` derives from the output
directory name and therefore *must* differ between two runs written to two places. Same inputs.

This **falsifies my own pre-registration**: TOLERANCE.md §4 predicted "inside the tolerance but not
at zero… a small number of differing pixels concentrated on and around the emissive particles."
Zero. I am reporting it as a falsification rather than a success because TOLERANCE.md §3 explicitly
pre-committed me to report a 0/0 outcome and say the tolerance turned out unnecessary.

### ★★ The correction: GLOW IS INNOCENT. SDFGI is the accumulator.

The shipped clip renders with the substrate's **glow ON** (intensity 0.6, bloom 0.12, threshold
1.25), black fog on, filmic tonemap, **673 GPU particles across 12 systems, 5 animated lights** —
and re-renders byte-identically in a separate process. So the standing law cannot be right as
stated. I isolated it, one feature at a time, on this stage, with the shipped clip
(`L7V_PROBE=<feature>`, double-rendered, `framediff`):

| environment | re-render identity | signature |
|---|---|---|
| substrate as authored (**glow on**) | **120 / 120 byte-identical** | — |
| glow **+ SSAO** | **30 / 30 byte-identical** | — |
| glow **+ SSIL** | **30 / 30 byte-identical** | — |
| glow **+ volumetric fog** | **21 / 21 byte-identical** | (21 pairs: one run came in short, see §5's harness note) |
| glow **+ SDFGI** | **0 / 30 — DIVERGES** | 129 px, **max channel delta 1**, bbox `[16, 0, 1275, 716]` — spread over essentially the whole frame |

**The SDFGI signature is an exact fingerprint match for the 0/90 result the harness recorded for
`probe_accum_on`** (max channel delta 1, whole-frame spread). SDFGI is a *progressive cascade that
converges across frames* — a temporal accumulator by construction. Glow is a single-frame
blur-and-add with no feedback path, and it is measured here not to cost byte-identity at all.

**Attribution, and it points at me (TCP-30).** `probe_accum_on.gd` switches glow + SSAO + SSIL +
SDFGI on *together*, so it could never separate them — and **the harness's own `deterministic_env()`
docstring, which I wrote, asserts "glow — bloom threshold crossings amplify tiny deltas" as the
rationale.** I convicted glow in my own code comment; this dispatch's §2.3 inherited the conviction
and turned it into a decision rule that has been making cells trade real visual quality for a
byte-equality glow was never costing them. That is the fourth time this program has convicted the
wrong thing, and this time the wrong conviction is mine.

**What this changes, concretely:** a VFX cell can have glow *and* bit-comparable evidence. The
lockout only needs SDFGI (and whatever else remains untested) off, not glow. I did **not** modify
the harness to correct its docstring — that is out of scope here (§4.4 / R-2) and I am flagging it
as an authorised change someone should make deliberately, with this evidence attached.

**Untested, and I am not extrapolating past it:** auto-exposure; SSAO/SSIL/volfog in *combination*
rather than singly; and cold-shader-cache identity, which the harness README already flags as
unmeasured and which I have not closed.

---

## §4 — Method, and what it cost to reach the stage at all

**R-1 — METHOD: hand-authored GDScript.** Not the installed W-MUR wire (free choice per L-J; a
concurrent cell owns the wire question), not editor-by-hand. Reasoning, and it is specific rather
than habitual: the harness's clip contract *is* a script contract, so a GUI wire would have to
author into a `.tscn` that I then load — inserting a step whose failure modes belong to a
different cell's question. More decisively, **a VFX pass is a parameter search** (ramps, curves,
velocities, ratios), and what I needed most was the ability to change eleven numbers and re-render
in one command. Six iterations happened in ~40 minutes because the whole effect is one text file.
I do not think a wire would have lost — I think **it would have been answering a different
question**, and L-J parks that question elsewhere this session.

**W-PRO was not installed, not looked at, and its swap directory was not opened.**

### The reach of the harness — measured, and it is the one place I nearly had to modify it

`~/Games/mcp-lab/harness/` is a Godot project with **no `.godot/` cache at all**, by design: that
is what makes its captures un-stale-able. The stage, however, lives in another project and needs
6 external resources. So I probed what the harness can actually reach (`clips/probe_stage.gd`):

| probe | result |
|---|---|
| `load()` an absolute-path **`.gd`** as the rig's `--clip` | **WORKS** |
| `extends "<absolute path>.gd"` — a base class outside `res://` | **WORKS** |
| `load()` an absolute-path **`.gdshader`** as an `ext_resource` | **WORKS** (all 3, silently, first try) |
| `load()` an absolute-path **`.tscn`** | parses — but see next row |
| an absolute-path **`.png`** as a `Texture2D` `ext_resource` | **FAILS**: `No loader found for resource … (expected type: Texture2D)`, and **one failed ext_resource fails the whole scene load** |

**Attribution (TCP-30).** This is **not** a harness defect and **not** a Godot defect — it is a
documented property of Godot 4: raw PNGs are expected to arrive as `.ctex` via an import sidecar,
and a project with no `.godot/` cache cannot have one. `Image.load_from_file()` has no such
restriction because it reads bytes rather than resolving a resource. **The harness's own
`load_glb()` helper exists for exactly this reason** — I built it in a previous cell for GLB and
simply had not needed the texture case yet.

**R-2 — the harness was NOT modified, and NOT added to.** No clip file, no asset, no symlink.
`clips/l7v_crypt.gd` lives in my floor and is passed to the shipped `bin/shoot_clip.sh` by
absolute path. Verified by hash at start and end (§9). **This matters more than it sounds:**
putting the stage's 8.8 MB of textures into `harness/` would have forced Godot to create a
`.godot/` import cache there and **destroyed the documented property that makes the harness
trustworthy.** The rule "use, don't modify" turned out to protect something real.

**R-3 — substrate dependencies copied out, textures converted to runtime injection.** The 3
shaders and 3 textures were `cp`-ed out of `mcp-lab/project/` (a read; §2.2 authorises copying the
scene out and the scene is inert without them). In my copy the 3 `Texture2D` ext_resources are
replaced by a `resource_name = "TEX:<file>"` marker on the 28 materials that used them, and
`vfx/stage_lib.gd` re-attaches them at runtime via `Image.load_from_file`. **Nothing else about
the substrate is altered** — geometry, transforms, all 3 wall shaders, every shader parameter,
all 3 lights and the `WorldEnvironment` arrive as authored, confirmed by the engine's own census.

---

## §5 — The cost account (§3.4) — measured, not estimated

**Instrument:** a separate minimal Godot project in my floor (`l7vfx/bench/`), loading the
**identical** `stage_lib.gd` and `crypt_vfx.gd` the capture clip loads, by absolute path, so the
thing benchmarked is byte-identically the thing shipped. **Not the harness** — the capture rig
writes a PNG per frame and that encode swamps the renderer; timing a capture times Pillow. Raw
data: `l7vfx/evidence/cost.json`.

**Three instrument findings first, because a number from a broken instrument is worse than no number:**

1. **`viewport_get_measured_render_time_gpu()` returns 0.000 for every configuration** on this
   stack (Godot 4.6.3 / Metal / M2). It is reported as 0.0 in `cost.json` **and labelled**, rather
   than dropped — a zero from an unwired instrument must never be mistaken for zero cost.
2. **At the shipping resolution the measurement is impossible, and that is itself the headline.**
   At 1280×720 *every* configuration — including the shadow variant with 763 draw calls — measured
   **6.03–6.09 ms**, i.e. all of them pinned at the same presentation cap. **The whole pass,
   shadows included, fits inside the frame budget with room to spare; nothing here is render-bound
   at 720p.**
3. To *rank* the configurations I therefore raised the pixel count until the frame was genuinely
   render-bound — **3840×2160, 9× the pixels, same scene, same camera, same code.** Ratios transfer
   back; absolute milliseconds do not, and I do not present them as if they did.

**Controls:** 45 warm frames before every sample (shader compiles, shadow-atlas allocation and
particle preprocess all land there, never in the sample); 120 sampled frames; median reported, not
mean; **and the whole ladder run twice in opposite order.** The stage is built **once** and shared,
so every configuration is measured against literally the same object rather than an equal one.

> **Thermal control result: `A_stage_only` = 18.854 ms forward, 18.858 ms reversed — 0.021 % drift.**
> Nothing below is thermal.

### The ladder — 3840×2160, MSAA 4×, median of both passes

| configuration | wall ms | Δ vs stage | Δ % | draws | objects | primitives | particles | lights |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **A — stage only (no pass)** | **18.856** | — | — | 334 | 1521 | 14,444 | 0 | 0 |
| D — embers only | 19.004 | +0.148 | +0.8 % | 338 | 1526 | 15,188 | 110 | 0 |
| F — motes only | 19.078 | +0.222 | +1.2 % | 333 | 1522 | 16,164 | 215 | 0 |
| C — flame only | 19.251 | +0.395 | +2.1 % | 338 | 1526 | 16,484 | 304 | 0 |
| E — **smoke only** | 20.331 | **+1.475** | +7.8 % | 335 | 1522 | 14,796 | **44** | 0 |
| G — **lights only** | 20.337 | **+1.481** | +7.9 % | 334 | 1521 | 14,444 | **0** | 5 |
| H — centre fire only (no corners) | 20.762 | +1.906 | +10.1 % | 337 | 1525 | 17,716 | 409 | 1 |
| **B — THE SHIPPED PASS** | **21.238** | **+2.381** | **+12.6 %** | **346** | 1533 | 19,300 | **673** | **5** |
| I — full **+ shadow-casting lights** | 23.705 | **+4.849** | **+25.7 %** | **763** | 2356 | 46,816 | 673 | 5 |

### What the numbers say

**1. The shipped pass costs +12.6 % of frame time when the frame is render-bound, and nothing at
all when it is not.** 673 particles across 12 systems and 5 animated lights buy **+12 draw calls**
(one per system) and **+4,856 primitives**. §3.4 said an ambient pass that costs nothing is a
finding: at 720p, this one does.

**2. ★ Particle COUNT is nearly free. Particle AREA is the entire cost.** This is the finding I did
not predict and it inverts the intuition the whole pass was budgeted on:

- **motes: 215 particles → +0.222 ms**
- **smoke: 44 particles → +1.475 ms**

**Smoke costs 6.6× more than motes while having 5× fewer particles — a ~33× difference in cost per
particle.** The reason is overdraw: motes are 0.115 m sprites, smoke sprites are 1.70 m and grow to
2.1× over life, so a handful of them cover a large fraction of the screen in alpha-blended layers.
**A particle budget expressed as a count is measuring the wrong quantity.** The right budget is
screen-space area × layers, and nothing in the program's vocabulary currently tracks it.

**3. FIRST_INTENT prediction #6 was half right, and the half it got right is smaller than I thought.**
I predicted "the cost risk is not particles; it is lights." Lights *are* expensive — **+1.481 ms
with literally zero extra draw calls and zero extra primitives**, pure fragment-shading cost, which
is a clean confirmation. But they tie with smoke rather than dominating it, and I had smoke filed
as free.

**4. ★ R-12 vindicated with a number: shadows cost 2.3× the scene's draw calls to render nothing.**
Turning shadow-casting on for the 5 fire lights takes draw calls from **346 → 763 (+417)**,
primitives from 19,300 → **46,816 (+27,516)**, and frame time to **+25.7 %** — *double the entire
rest of the pass*. Five omnis × six cube faces × the whole room. And the room is **empty**: within
the fire lights' range there is nothing but the flat floor they stand on, so not one shadow is
cast. **The substrate's emptiness does not merely look sparse — it removes an entire VFX technique
from being able to contribute at all**, and that finding belongs to whoever owns the room, not to
this cell.

**5. The corner fires are the bargain of the pass.** B − H = **+0.476 ms** for all four
(flame + embers + light each), against +1.906 ms for the centre fire alone. They are also the
elements that read best at play distance. R-8 holds on both counts.

**6. Components do not sum to the whole** (parts total +3.72 ms vs +2.38 ms measured for the full
pass) and I am not hiding it: per-configuration fixed overheads get counted repeatedly, and the
overdraw regions of separate systems overlap when they run together instead of stacking. The
per-component numbers rank contributors; they are not additive budgets.

---

## §6 — The iteration loop — six rounds, judged at the play camera every time

The loop is one of the measurements this cell exists to produce, so here it is with the failure
of each round stated rather than smoothed over. **Plate:** `l7vfx/evidence/iteration_ladder.png`
(BEFORE | i1 | i6, same frame index, same camera).

| # | change | what I saw at the play camera | what it cost me |
|---|---|---|---|
| **i1** | first build: 11 systems, 734 particles, 5 lights, room-wide motes | **Three failures at once.** (a) the fire was a clipped white ball, (b) every particle was a *visible hard square*, (c) the room got **brighter and flatter** — long light ranges (11 m / 5.4 m) washed out the contrast that made it read as a room at all. Motes read as confetti scattered over the floor. | 1 render + the magnifier that found the cause |
| **i2** | **procedural soft-falloff sprite**, generated in code; HDR peaks down; light ranges cut to 6.4 m / 3.3 m for *contrast rather than illumination* | Blockiness gone, embers suddenly read as distinct hot points. Flame now a cluster of **separate soft orbs** — still not a body. | 1 render |
| **i3** | emission radius 0.38 → 0.24, amount 62 → 130 | Flame became a coherent body — and **blew out to white again**. | 2 renders (one lost to cold-compile, §4) |
| **i4** | **only a small hot core above the glow threshold**; body deliberately under 1.25; longer life, lower damping | Real flame structure: hot base, tapering tongues. The first frame I would show anyone. | 2 renders + the first true A/B against BEFORE |
| **i5** | smoke, added on the strength of the `ab_stats` measurement (§0 CEILING-1) — a vertical column | **Invisible.** Not subtle — absent. | 1 render, and the finding that paid for the whole round |
| **i6** | **smoke re-authored onto the ground plane** — `radial_accel` spread, upward velocity cut to a quarter, larger and slower | The floor stopped being a uniform tile sheet. Soft warm-then-dark mottling radiating from the fire. Ambient as it should be: **felt, not seen.** | 1 render — **shipped** |

**The single most valuable round was i5, the one that produced nothing visible.** It cost one
render and returned CEILING-2, which is a fact about every future VFX cell at this camera.

**The magnifier discipline.** `scripts/crop.py` exists because I could not diagnose i1 from the
full frame — at the play camera the fire is ~30 px and "it looks wrong" is not a cause. Magnifying
4× showed hard squares immediately. **The judging view stayed the play camera throughout; the
magnifier was only ever used to find causes, never to judge results,** and I flag that distinction
because the dispatch's §1 warning is precisely about the temptation to judge in close-up.

---

## §7 — Rulings, veto-open

Every one of these is mine to be overruled on. Reasoning given, not just the decision.

| # | ruling | reasoning |
|---|---|---|
| **R-1** | **Method: hand-authored GDScript.** Not W-MUR, not editor-by-hand. | The harness's clip contract is a script contract; a wire would have to author a `.tscn` I then load, inserting failure modes that belong to another cell. And a VFX pass is a *parameter search* — six iterations in ~40 min because the whole effect is one text file. Not a claim that a wire loses; a claim it answers a different question, which L-J parks elsewhere this session. |
| **R-2** | **The harness gets nothing — not even a clip file.** | `harness/` has *no `.godot/` cache by design*, and that is what makes its captures un-stale-able. Putting my 8.8 MB of textures in it would force one into existence and destroy that property. Clip + stage live in my floor and are passed by absolute path. |
| **R-3** | **Copy the substrate's 6 dependencies out; convert its 3 texture refs to runtime injection.** | Godot 4 cannot `load()` a raw PNG from any path without an import sidecar, and one failed `ext_resource` fails the whole scene. Injection via `Image.load_from_file` is the same philosophy as the harness's existing `load_glb`. Everything else about the substrate arrives as authored. |
| **R-4** | **The pass is the missing SOURCE of a light the room already has.** | `InteriorPool` (0, 2, 0), energy 3.4, warm — and nothing makes it. Converting a lighting cheat into a fact somebody caused is the highest-value ambient effect available here, and it is derived from the stage rather than from the brief. |
| **R-5** | **Additive-only. The pass adds nodes and writes nothing that was already there.** | `InteriorPool` keeps its authored energy; the `Environment` is untouched; no substrate property is modified. before/after then differ by *exactly* the `CryptVFX` subtree, which is the only thing that makes the cost account mean anything. It also cost me the ability to fix CEILING-1, and I accepted that. |
| **R-6** | **Fix the play camera BEFORE iterating the effect, and never move it again.** dist 34, fov 24, yaw 47, pitch −50, aim_h 1.0. | A 1.8 m figure subtends `1.8 / (2·34·tan 12°)` = **12.5 % of frame height** — squarely ARPG (Diablo-likes run ~12–15 %). Fixing it first is the discipline that stops the camera from being quietly tuned to flatter the effect. **The camera is the judge; you do not move the judge.** |
| **R-7** | **Warm fire. Refuse the cold/green soul-flame the register note pulls toward.** | The substrate's own unexplained light is warm (1.00, 0.85, 0.62). Warm fire *explains* it; green fire *fights* it. Evidence beat register. See §8 — this one had to be actively refused. |
| **R-8** | **Five fires: one centre + four corners.** Not one, not six systems for show. | One fire says *someone passed through*. Five say *someone maintains this room* — which is the stronger and more unsettling reading of "inhabited," and the corner posts are the only arranged feature the room has. Measured: the corner fires are the elements that survive best at play distance (§5). |
| **R-9** | **Buy the glow tolerance.** | Not a choice on this stage — the substrate ships `glow_enabled = true`. Refusing glow means falsifying the stage. §3. |
| **R-10** | **At an ARPG camera, ambient volume belongs on the GROUND PLANE, not in the air.** | Derived, not preferred: at −50° a vertical column is seen against the floor, never the sky. CEILING-2. This is the ruling I would most want propagated to L8 and to any future VFX cell. |
| **R-11** | **Fire sits on the bare floor — a campfire, not a brazier.** | No brazier prop exists and none can be synthesised without inventing game content. A campfire needs no prop, and "someone camped in the tomb" is a *better* inhabited reading than "someone installed fixtures". |
| **R-12** | **No shadow-casting firelight**, despite it being the most tempting "someone is here" signal. | Geometric, then measured: the room is **empty**, so within the fire light's range there is *nothing to cast a shadow of* — only the flat floor it stands on. The cost is real and the benefit is zero. See §5 for the number. |
| **R-13** | **Clip = 4.0 s @ 30 fps** (dispatch minimum 2 s @ 24 fps). | The embers have a 4.2 s lifetime; a 2 s clip would never show one complete its arc, and the arc is the element that carries the effect at play distance. |
| **R-14** | **Room-wide motes: keep, at a much reduced weight — but flagged as the weakest element.** | FIRST_INTENT ranked them third and the world demoted them further. §5 gives their cost and §6 their contribution; I keep them because they cost almost nothing and slightly break the floor's uniformity, and I flag that a veto here would cost the pass very little. |


## §8 — What in the dispatch steered me

gandalf's stated prime suspect was §1's *"death-faith ARPG"* register note. **It did steer me, but
it is not the biggest catch in the dispatch. There is a bigger one, and it is a noun in the brief
itself.**

### ★ STEER-1 — the word "crypt", inside the verbatim brief

§1 is stated to be the entire specification: *"Make the crypt feel inhabited."*

**The substrate is not a crypt.** It is a bare, roofless, sky-lit square stone court: no burials,
no sarcophagi, no niches, no funerary anything, and a 2.0-energy directional key coming down
through the missing roof. Nothing in 296 nodes is a tomb.

The noun does unearned work. "Crypt" primes *dark, enclosed, still, underground* — and it primes
exactly the fog/gloom/green answer I had to talk myself out of. **Had I accepted it, I would have
authored darkness into a room measured at a median lit pixel of 88/255, and then blamed my effect
for failing to read.** The word is a stronger steer than the register note precisely because it
sits in the part of the dispatch declared to be the whole spec, so it reads as given rather than
as framing.

Concretely, this is *why* CEILING-1 is a finding rather than an embarrassment: the gap between
"crypt" and the actual lighting is a fact about the world that the brief's own vocabulary conceals.

**Suggested fix:** in a mode-(ii) brief, name the room by what it *is* in the file, or refuse to
name it at all — *"make this room feel inhabited"* would have cost the dispatch nothing and
removed the whole prime.

### STEER-2 — "death-faith ARPG", the suspect, confirmed but contained

It pulled on exactly one axis: **colour.** Death-faith pulls hard toward pale green / cyan
soul-flame. I felt it, and I know I felt it because I wrote it down in FIRST_INTENT before I could
rationalise it: *"Not going to make it scary… Inhabited ≠ haunted. I am flagging the pull now."*

I refused it on evidence (R-7): the room's own unexplained light is warm, so warm fire explains it
and green fire fights it. **So the register note did not change what I shipped — but it is
load-bearing that I had to actively refuse it, and I only knew to because of the pre-registration.**
Contained, not harmless.

### ★ STEER-3 — a structural limit in FIRST_INTENT that makes the steer test weaker than it looks

**FIRST_INTENT is banked *after* the dispatch is read.** So it can test "did the world change my
mind?" — but it structurally *cannot* test "did the dispatch choose for me?", because the dispatch
is already in the intent. My §1 table scores my pre-registration honestly, and every row of it is
downstream of having read §0–§3.

If the steer question is to have teeth, either (a) **§1's brief should be readable separately from
the rest of the dispatch**, with intent banked from the brief alone before §0/§2/§3 are opened, or
(b) FIRST_INTENT should be banked in **two parts** — one from the brief, one after the constraints.
Right now the instrument is measuring substrate-steer and being read as though it measured
dispatch-steer.

### STEER-4 — §0 taught me what a good arrival looks like, and I went looking for it

§0 says every finding of consequence in L5 came from the arrival, and names *"the floor hole
nobody had specified."* **That primed me to go hunting for a hole**, and I did: I wrote a
floor-grid completeness check into `derive_detail.py` before I had any reason to suspect one. It
came back clean, 196/196.

Then I found a *different* hole — the sourceless light — and made it the design driver. I believe
R-4 is right on the merits and I would defend it independently. But the **framing** of my whole
answer as *"this room's version of L5's floor hole"* is §0's framing, not mine, and I want that on
the record rather than presented as convergent discovery.

### STEER-5 — §2.3 restated a measurement correctly and drew a wrong conclusion from it

The launch note warned that a prior cell had its own measurement restated back at it as a law, and
that the law was wrong. Here the **numbers are restated accurately** (90/90, 0/90, max delta 1 — I
checked them against the README I wrote). What is wrong is the sentence attached to them:
*"**Most VFX wants glow.** So decide first whether this cell buys glow at the price of a tolerance,
or refuses glow to keep byte equality."*

On this stage **there is no second branch** — the substrate ships glow enabled, so refusing it
means editing the stage. The framing presents a choice that the floor has already made. I caught
it only because I parsed the substrate before rendering; **a cell that rendered first would have
"chosen" glow without ever noticing it had no choice**, and would have written a tolerance
declaration that reads like a decision and is actually a rubber stamp. See §3.

### What did NOT steer me, and is worth saying so

- **§3.4's cost framing is genuinely neutral** — *"An ambient pass that doubles frame cost is a
  finding; so is one that costs nothing."* It explicitly licenses both outcomes, so it could not
  pull the measurement. That is well-written and I would keep it verbatim.
- **§2.2's refusal to describe the geometry worked exactly as intended.** I derived it, and the two
  facts the entire design rests on (the room is empty; the light has no source) are things a
  conductor's summary would almost certainly have omitted as uninteresting.
- **§3.3's "ambient VFX that cannot be judged in a still is exactly why the harness exists"** steered
  me toward motion, correctly, and CEILING-2 is a direct dividend of judging in motion at the play
  camera rather than in a hero still.

---

## §9 — Exit predicate (§4), checked mechanically

Script: `l7vfx/scripts/exit_predicate.sh` — the checks are executed, not asserted, and its raw
output is reproduced here.

```
§4.2  SUBSTRATE
  sha  : d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966
  want : d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966   -> SHA MATCH
  mode : -r--r--r--                                                        -> 0444 INTACT
  (verified identically at START, mid-run, and END)

§4.3  mcp-lab/project/
  OK   project/scene_before.tscn                     (byte + mtime identical)
  OK   project/project.godot                         (byte + mtime identical)
  OK   project/scripts/walltop_occlude.gdshader      (byte + mtime identical)
  OK   project/scripts/walltop_void.gdshader         (byte + mtime identical)
  OK   project/scripts/walltop_void_radial.gdshader  (byte + mtime identical)
  whole-tree delta: 15 files REMOVED, all named l5a_* — the live L5a cell tidying
  its own scratch. Zero files added. Nothing I read moved.

§4.4  HARNESS
  -> ALL 17 HARNESS CODE FILES BYTE-IDENTICAL (motion_rig.gd, motion_clip.gd,
     motion_rig.tscn, project.godot, README.md, bin/*.py, bin/*.sh, clips/*.gd)
  -> no clip added, no asset added, no symlink, no .godot/ cache created
  (harness/out/ HAS grown — that is where the rig is DESIGNED to write.)

§4.5  user:// hygiene
  tcp-motion-harness  : shader_cache, vulkan  -> only Godot's own regenerable caches
  tcp-l7v-cost-bench  : shader_cache, vulkan  -> only Godot's own regenerable caches
  (NOT inspected: tcp-l8ui — a concurrent cell's userdata.)

§4.5  the floor stays: 15 MB at ~/Games/mcp-lab/l7vfx/ (39 files)

EXIT PREDICATE: ALL CHECKS PASS
```

**I did have to extend the harness — and the answer is NO, I did not (§4.4), but it was close and
the near-miss is a finding.** Two things came up:

1. **`shoot_clip.sh`'s `--quit-after` slack (`settle + frames + 150`) is calibrated for the demo
   clip and is marginal for a 288-mesh scene with 12 particle systems.** At 1280×720 a *cold*
   shader-compile run consumed it and produced a short capture (118/120, 26/120, 0/120 across
   different runs); at **1920×1080 it failed reproducibly** (20, 53, 13 of 60). **The guard fired
   correctly every single time** — `exit 3` with the exact frame count, never a silent success —
   so the harness never lied, and the fix is a *discipline* (warm the cache with a throwaway run;
   shoot stills short) rather than a code change. I did not touch it.
2. **The rig REFUSES unknown `--` options**, which is correct of it, so the ablation ladder is
   driven through the environment (`L7V_*`) instead. Working around a guard rather than weakening
   it.

### ★ A 31-minute loss, and it was my own TCP-30 failure

The cost bench **never ran for its first 31 minutes.** It died at *parse time* —
`Parse Error: The variable type is being inferred from a Variant value (Warning treated as error)`
— and the process then sat idle with no `--quit-after`. I watched it for half an hour, saw 17 % CPU,
and **built a theory that macOS was throttling the occluded window.** The direct evidence was
sitting in the output file the entire time; I never read it, because my own
`| grep -E '\[bench\]|ERROR' | head -30` filter block-buffered and flushed nothing until the
process ended.

**I convicted the platform from an indirect proxy while the direct evidence was one command away.**
That is precisely the failure mode TCP-30 exists to prevent, committed against myself, in the same
cell in which I corrected the program's misattribution of glow. Logged in full because a cell that
reports only the misattributions it caught in *other* people's work is not reporting honestly.

**Once it actually worked, the entire measurement suite — 3 capture clips, the determinism
double-render, 4 accumulator isolation probes (8 renders), 2 `__box` stills and 2 full 18-block
bench passes — took 9 minutes.**

### A note on §4.3 and a live neighbour

`mcp-lab/project/` is **being written to right now by the L5a cell** — its `l5a_*.tscn`,
`l5a_*.json` and `.godot/` files change every few minutes, and that is correct and expected. So
"the directory is unchanged" is not a checkable proposition and I did not claim it. What I check
instead is the proposition that actually matters: **every file I read is byte-for-byte and
mtime-for-mtime what it was when I started**, with the whole-tree add/remove delta printed
alongside so the L5a writes are visible and separable rather than hidden. The substrate itself is
verified twice over — sha256 *and* mode 0444.

I read exactly 8 files out of that directory and wrote none. No L5a artefact was opened (§10).

---

## §10 — Read-list, including the explicit NOT-read list (§3.5)

### Read

| what | why |
|---|---|
| `dispatches/2026-07-25-drax-l7v-vfx-arrival.md` | the cell |
| `mcp-lab/harness/README.md` | the capture contract, and the measured determinism table §2.3 points at |
| `mcp-lab/harness/motion_rig.gd`, `motion_clip.gd`, `bin/shoot_clip.sh`, `bin/framediff.py` | I had to know the rig's arg handling, its step-mode refusal, and the differ's output fields before I could rely on any of them |
| `mcp-lab/harness/clips/demo_particles_step.gd` | the existing step-mode/`use_fixed_seed` pattern |
| `mcp-lab/harness/out/*/frames/manifest.json` (grep) | to establish that `use_fixed_seed` is *available* on this build (`seed=fixed(20260725)`, not `unavailable`) — a determinism precondition, checked rather than assumed |
| `mcp-lab/project/scene_before.tscn` | the substrate; §2.2 authorises copying it out |
| `mcp-lab/project/scripts/*.gdshader` (3), `…/Texture/…*.png` (3) | its 6 `ext_resource` dependencies — the scene is inert without them |
| `mcp-lab/project/project.godot` | to confirm the renderer the substrate expects (`forward_plus`) so the bench mirrors it |
| `mcp-lab/evidence/L4_KIT_CONSTANTS.md` §7, `evidence/l4/l4b/logs/final_shoot_box.log` | the **exact** `__box` camera, read off a running rig rather than remembered: fov 20.0, yaw 47, pitch −50, dist 50 |

### NOT read — deliberately, and stated because §3.5 asks

| what | why not |
|---|---|
| **`mcp-lab/_swap/`** | **W-PRO's swap directory. Not opened, not listed, not `ls`-ed. L-J.** |
| **Any L5a artefact in `mcp-lab/project/`** | `l5a_*.gd`, `l5a_*.tscn`, `l5a_*.json`, `.godot/`, `addons/` — **not one was opened.** A blind mode-(i) cell is live there and reading its working files would let its answers leak into mine. The `find` inventory I keep for the untouched-proof *names* them; it reads none of their contents, and that distinction is the whole point of taking the inventory that way. |
| **`mcp-lab/l8ui/`** | a concurrent HUD cell's floor. Not listed, not read. |
| **`reincarnated-godot/`** | not mine this cell. Not touched. |
| **`harness/clips/probe_accum_on.gd` — read for its configuration, deliberately NOT re-run** | §2.3 says *"re-run the isolation rather than re-deriving it."* **I did neither — I replaced it, and that turned out to matter.** `probe_accum_on` switches glow + SSAO + SSIL + SDFGI on *together* on the demo sword clip, so re-running it would have reproduced a number that **cannot separate the four** and would have left the glow misattribution standing. Instead I ran the isolation it could not: the *actual shipped clip*, on the *actual substrate*, one feature at a time. That is what found SDFGI (§3). Flagged as a deviation from the dispatch's instruction rather than buried — and the deviation is the reason the correction exists. |
| **Prior L6 / L7 cell reports, and the concurrent wire cell's material** | this is a design *arrival*. Reading another cell's answer to an adjacent question is the fastest way to converge on it by accident. |

---

## §11 — What I would do next, and what I would not

**Would.** (a) Take CEILING-1 to whoever owns the substrate's lighting: this room is lit as a
daylit court and *every* firelight-based ambient pass will be capped by it, so it is a shared
finding, not mine. (b) Propagate R-10 (ground-plane, not air) to the L8 HUD cell and any future
VFX cell before they spend a round discovering it. (c) Put **one prop** in the room — a single
occluder anywhere near the centre would immediately unlock shadow-casting firelight, which R-12
currently has to refuse for want of anything to cast a shadow of.

**Would not.** Chase a better flame. i4→i6 is already into diminishing returns at the play camera,
and the honest reading of §5 is that the elements which survive to the player are the **light
pools, the corner fires and the ember arcs** — none of which get better by refining the flame's
silhouette. Polishing a shape the camera foreshortens into a disc is exactly the close-up trap
§1 warns about.

---

