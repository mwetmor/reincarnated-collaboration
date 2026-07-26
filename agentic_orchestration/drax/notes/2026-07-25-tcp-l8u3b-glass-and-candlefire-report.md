# TCP-L8-U3b — the globe becomes glass as it empties, and the candles are lit

**Agent:** drax (presentation seam) · **Dispatch:** `2026-07-25-drax-l8u3b-glass-and-candlefire.md`
**Clock started:** 2026-07-26T01:36:39Z (epoch 1785029799)
**Clock closed:** 2026-07-26T02:23:24Z — **46 m 45 s of authoring, unbroken, no stall.**
**Floor:** `~/Games/mcp-lab/l8ui/`, extending `ui3/` as `ui3b/`. Arm 3 byte-identical at close.
**Status:** COMPLETE

---

## §1 — FIRST_INTENT (banked verbatim, before any work, TCP-32)

> Banked at 2026-07-26T01:37Z, after reading the dispatch and nothing else. Not edited afterward.

```
FIRST_INTENT — drax, arm 3b, before opening a single file.

What I think I am going to do:

1. Copy ui3/ to ui3b/ so arm 3 stays intact and addressable. Not a branch, not an
   in-place edit — a physical copy, because §4.1 says arm 3 must still render and the
   cheapest proof of that is that its files were never touched. I will re-render ui3/
   at the end from its own untouched scenes to prove it.

2. Glass. My first instinct is that this is a SHADER problem, not a sprite problem.
   The empty region of the orb currently reads as an opaque amber disc that grows and
   glows as health drains. Matt wants that same growing region to read as glass. Glass
   in 2D at UI scale is: low alpha on the body + a bright specular streak + a rim that
   stays opaque + something visible THROUGH it. The "something visible through it" is
   the part I expect to be the whole cost, because right now there is nothing behind
   the orb — it composites onto the HUD background. If nothing is behind it, low alpha
   just looks like a faded disc, not glass. So I expect to have to put a backdrop
   behind the orb, or fake the see-through with a darkened inner shadow.

3. I predict the alpha ramp is trivial (one lerp driven off the same health scalar that
   already drives fill height) and the READ is hard. That is the arm-1 lesson repeating:
   the mechanism is minutes, the legibility is hours.

4. Candles. Three wicks per cluster, two clusters, six flames. My instinct is
   CPUParticles2D or GPUParticles2D with a small additive Glow_0N sprite, one emitter
   per wick, plus a second larger very-low-alpha glow as the halo. I expect to spend
   more time MEASURING the wick pixel positions than building the flames. I expect the
   flames to be visually cheap and to cost almost nothing in frame time at UI scale,
   which is gandalf's suspicion too, and I am uneasy that I agree with him before
   measuring.

5. On §2's open question (Frame_Orb_01_Glass as material rather than mask): my honest
   first read is that it is probably still wrong, because a vertical gradient reaching
   all four canvas edges has no orb in it — it is a rectangle of gradient. As a material
   you would have to mask it to the orb anyway, and then you are back to needing a
   circular mask, which is the thing it failed to be. But I have not looked at
   Frame_Orb_02_Glass and I will look at both before I say that in the report.

6. Biggest risk I can name in advance: the legibility instrument (§4.3). It measures
   contrast/legibility on an opaque surface. If I make the surface translucent the
   instrument may report a legibility collapse that is REAL for the instrument and FALSE
   for the eye, because glass is supposed to be low-contrast. I do not get to change the
   instrument. So I may have to ship a number that looks like a regression and argue in
   words that it is not. I would rather pre-register that now than discover it and be
   accused of excusing it after the fact.

7. On gandalf's registered prediction (§1, component-family law says this cell is cheap):
   I think he is HALF right and I am registering my counter now. The candles are a new
   family by any honest reading — particles are not sprites, they are a different node
   class with a different lifecycle — but they are TINY. The glass is not a new family
   at all and I still think it is where the hours go. So I predict: law survives, but
   only because the new-family cost happened to be near zero, which is a weak pass, not
   a strong one. If the flames had been a big family the law would have been tested
   properly and it will not be tested properly here.

8. What I will NOT do: invent the second branch of Matt's "either." Gandalf said he
   won't and neither will I. I build lit candles. If I have an opinion about the
   alternative I will put it in the report as a HALT item, not in the build.
```

---

*(everything below this line was authored after the work)*

---

## §2 — The two rulings, realised

### 2.1 — The globe becomes glass as it empties

**The change is one line of intent and a page of optics.** Arm 3 wrote the empty region
as an opaque body — `COLOR = vec4(rgb, a)` with `a` the analytic disc mask, so fluid and
void were equally solid. Arm 3b makes **alpha a function of the fluid boundary**. The
geometry is untouched: same analytic disc, same `r = 194/512` derived from the ring's
opaque-at-every-angle annulus, same containment guarantee. Arm 3's R-9 is not re-derived,
it is *called*.

**★ The measurement that decided the material, and it reverses my own banked prediction.**
FIRST_INTENT §5 said the glass sprite was "probably still wrong" as a material. It is
right, and the reason is exactly the property that made it wrong as a mask. Measured in
12 radial shells about the fill disc's centre:

```
Frame_Orb_01_Glass    alpha, inner (r < 0.5R) ..... 0.364
                      alpha, rim  (r 0.85-1.0R) ... 0.525      a +44% RISE toward the edge
                      luminance falls 0.57 -> 0.47 over the same span
```

A silhouette is binary. **This is a THICKNESS MAP** — alpha rising where a sight-line
passes through more glass. Arm 3 wanted a silhouette, got a thickness map, and called it
*"a fine texture and a useless mask."* That verdict was right for masks and exactly
inverted for materials: a thickness map is the single most useful thing you can be handed
when the ruling is "make it glass," and it replaces an analytic Fresnel I would otherwise
have invented. The sprite's **alpha** is now sampled as optical thickness; arm 3 sampled
only its RGB.

**A second correction to arm 3, from the same probe.** Its header calls this sprite's
alpha *"a VERTICAL GRADIENT."* Regressing luminance on y alone inside the disc gives
**R² = 0.6728** — a third of the signal is not explained by height — and horizontal
gradient energy is **77.5%** of vertical (0.00176 vs 0.00227). It has real 2D structure.
"Vertical gradient" was true enough to reject it as a mask and not true enough to reject
it as a texture.

**`Frame_Orb_02_Glass`, since §2 named it:** alpha mean 0.443 vs 0.444, R²-on-y 0.6736 vs
0.6728, the same rim rise. **Statistically interchangeable.** It differs only in a
tighter, higher specular (hot centroid at globe-radii (+0.432, −0.613) vs (+0.499,
−0.452); 1,343 hot px vs 3,149). Orb_01 is kept because the *rim* is Orb_01, and mixing
families gives a globe whose highlight disagrees with its own metal.

### 2.2 — The candles are lit

**Count verified independently of gandalf's.** `SPR_DarkFantasy_Greeble_Candles_01` is a
three-candle cluster, placed once per globe, twice per HUD. **2 × 3 = 6. Exact.**

**Wick positions, measured — and the obvious instrument failed.** A column-top profile
CANNOT segment this cluster: the sprite is drawn in perspective, the short right candle's
shoulder sits directly under the tall centre one, and a whole-sprite column scan returns
**one** raised group, not three. That failure is logged rather than hidden, because it is
the same class of mistake arm 3's §7 already paid for once — reaching for a bbox where
the thing wanted is not a bbox property.

The signature that separates them is **colour**: the wicks are the only compact dark blobs
in a pale sprite. Connected components of {α > 0.5 AND luminance < 0.30}, filtered to
aspect 0.55–2.2 and fill > 0.45 (which rejects the seven long thin facet-shadow seams),
gives exactly three, verified by overlay before use:

```
centre (tall)   512-canvas tip (247.4,  24)   ->  frac (0.4833, 0.0469)
left  (medium)  512-canvas tip (150.2, 146)   ->  frac (0.2935, 0.2852)
right (short)   512-canvas tip (360.7, 205)   ->  frac (0.7045, 0.4004)
```

**⚠ THE KIT SHIPS CANDLES AND SHIPS FIRE AND NEVER JOINS THEM.** All three wicks are dark
unlit stubs — that is literally how this cell *found* them. The only flame in either pack
is `FX_FireSheet_01`, in the FX folder, which nothing in the Greeble family references.
Joining them is the whole of the work.

**Three layers, each with a job the others cannot do.** HALO (`Glow_05`, the pack's only
true soft radial falloff — every other `Glow_0N` is a hard-edged low-poly polygon) ·
FLAME (`FireSheet_01`, per-wick phase, additive) · EMBERS (`GPUParticles2D`, the only
optional layer, and the one that makes §1's particle question answerable at all).

**⚠ The second branch of Matt's "either" is not invented.** gandalf declined to guess and
so do I. It is HALT **H-13**, below.

---

## §3 — THE SEAT FORK, resolved by measurement rather than by taste

Translucency is only visible against something. Arm 3's own finding is that the orb has no
`_Background` **because its backing is the tray** — `Frame_Hotbar_04_Background`'s lobes,
at 0.95–0.99 column coverage, tinted PLATE α 0.96. Glass over that is smoked glass.

So `plate_punch.gdshader` removes the plate **inside exactly the fill disc**. The punch
radius is the fill radius; the ring's opaque annulus is r = [185.5, 203.5]; 194 is its
mid-line, so every pixel of the punch's boundary has ring metal over it **at every angle**.
The hole cannot show a seam. **R-9 reused verbatim on a second problem with no new
measurement** — and that reuse is itself evidence for §1's law.

**Both branches were built and both were measured.** `translucency.py` defines
translucency operationally: render the identical HUD state over three different 3D
backgrounds and take the per-pixel spread of the globe across them. **An opaque surface
scores 0 by construction, whatever colour it is.**

| | mean spread | median |
|---|---:|---:|
| **arm 3** (opaque void) | **0.00** | 0.00 |
| **arm 3b, PUNCH=0** (arm 3's seat kept) | **1.36** | 1.00 |
| **arm 3b, PUNCH=1** (seat removed) | **33.96** | 32.00 |

Arm 3 scoring exactly 0.00 is the instrument validating itself. **PUNCH=0 scores 1.36 —
a 25× gap.** The smoked-glass branch is not translucent in any measurable sense; it is a
slightly desaturated opaque disc. **PUNCH=1 ships.** That is not my preference, it is the
only branch that satisfies the ruling, and the number is what says so.

---

## §4 — ★ MATT'S SENTENCE IS A TESTABLE CLAIM, AND TESTING IT FOUND A CONFLICT WITH R-5

> *"as the health level lowers, the globe should become translucent like glass"*

That claim has a truth value. Shipping a picture captioned "looks like glass" would be
precisely the move standing law **L-Q** exists to prevent — ratifying a cause nobody
measured. So it was measured, and **the first answer was NO.**

**The conflict, stated structurally.** R-5 VOID-FILLS-BRIGHT ramps the danger term
0.10 → 0.42 → 0.86 across CALM/WARN/CRIT. If that term *also* closes the glass, then below
the critical threshold the vessel gets **less** see-through exactly as the ruling wants it
getting **more**. They are the same variable pulled in opposite directions.

Swept (`glow_opac` = how much the danger glow closes the glass):

| glow_opac | life 1.0 | 0.70 | 0.50 | 0.30 | 0.13 | 0.04 | monotone? |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.44 | 0.0 | 12.2 | 21.1 | 35.4 | 23.9 | 25.1 | **NO** (−33%) |
| 0.28 | 0.0 | 12.5 | 23.7 | 39.9 | 34.3 | 36.0 | **NO** (−14%) |
| 0.12 | 0.0 | 12.7 | 26.3 | 44.3 | 45.1 | 47.1 | YES |
| 0.00 | 0.0 | 13.0 | 28.2 | 47.7 | 53.1 | 55.5 | YES |

**`emissive` was swept too (0.98 / 0.72 / 0.55) and moves NONE of these numbers** — which
localises the conflict entirely in alpha and rules out clipping as the cause. That
negative result is worth as much as the positive one; without it I would have spent the
lap tuning brightness.

**The resolution is principled, not a fudge: R-5's name is VOID-FILLS-*BRIGHT*.** Opacity
was never in that rule. Arm 3 got it for free because everything was opaque. Moving the
danger channel onto brightness and hue is therefore **faithful to R-5 rather than a
weakening of it.**

**⚠ And then the `stain` term (§5.2) re-opened it, so the sweep was run twice and both
passes are kept.** `stain` adds a flat 0.143 to void alpha at every life level, which
re-exposed the WARN→CRIT step at 0.12: a **2.6%** dip at life 0.13 — monotone by *median*
(28 → 32 → 36) while the *mean* dipped.

| glow_opac, with `stain` | 1.0 | 0.86 | 0.70 | 0.50 | 0.30 | 0.13 | 0.04 | monotone? |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0.12 | 0.0 | — | 10.2 | 20.7 | 34.9 | 34.0 | 35.6 | **NO** (−2.6%) |
| **0.08 (shipped)** | 0.0 | 1.19 | 10.23 | 21.39 | 35.97 | **36.63** | **38.36** | **YES** |
| 0.05 | 0.0 | 1.20 | 10.28 | 21.87 | 36.80 | 38.65 | 40.46 | YES |

**Recorded in full because tuning one constant, adding a second feature, and not
re-running the sweep is exactly how a validated result quietly stops being true.**

**★ FINAL VERDICT ON THE RULING: SATISFIED, AND PROVEN.** Translucency rises
**monotonically** from 0.00 at full health to 38.36 at 4% health. Matt's sentence is not a
description of the picture; it is a property of the build, and it is measured.

---

## §5 — Three defects found, two of them inherited from arm 3 and shipped for three arms

### 5.1 ★ Arm 3's faceting term was not faceting

`orb_fill.gdshader` sets `facet_ref = 0.29`, captioned *"measured mean luminance of
`Frame_Orb_01_Glass` ink."* The number is correct **for the whole sprite** (0.4566 over all
ink at cut 0.02; 0.29 is lower still because the faint outer skirt is dark and enormous).
It is the **wrong statistic for that shader**, which samples only the 95% window inside the
fill disc. Measured over exactly that window:

```
mean 0.5250   p05 0.3459   p50 0.5398   p95 0.6073   min 0.2513   max 0.6375
```

So arm 3's `gl = lum / 0.29` ran in **[0.87, 2.20]** against a clamp of **[0.55, 1.55]** and
**was pinned at its ceiling over 85.2% of the disc.** Arm 3's faceting was a flat 1.19×
brightening with a little darkening at the extreme rim. **Three arms shipped a term that
did not do its job**, and it was invisible because a constant multiply looks like a
deliberate exposure choice.

Fixed two ways at once: the reference is the in-disc mean, and the term is now a **signed
deviation** about it rather than a ratio into a clamp — so "no facet" is exactly 1.0 and the
amplifier has something to amplify. This is why arm 3b's globes have visible low-poly
faceting and arm 3's do not.

**This is arm 3's own §7 pattern recurring:** "the measurement was right and my conclusion
from it was wrong." Here the measurement was right *for a different region than the one
used*, which is a subtler version and worth naming separately.

### 5.2 The translucency silently broke R-6, and the fix is what glass does

With the void made see-through, the **energy** globe at 41/300 mana came out **grey**. Its
`void_col` alpha is a constant 0.22 (R-5 is life's channel and must not be lent to energy —
arm 3's rule, correctly), so the empty region carried almost no hue and the stone behind
dominated. **An empty rage globe and an empty mana globe became the same grey disc**, and
"which resource is this" is a question you answer by colour at a glance. R-6 —
*six economies, one vessel* — was broken by a change that never mentioned it.

The fix is not a fudge, it is what glass does: **a vessel is stained by what it holds.** The
empty half keeps a wash of the fluid's hue and a little of its opacity. It also costs
translucency *uniformly* across all life levels, which is why it re-opened §4's
monotonicity rather than distorting its shape.

### 5.3 ★ A defect the flames EXPOSED, not one they caused

Arm 3 sites the ailment frame at offset_top −376, bottom edge at h−272. The left candle
cluster's flames top out at h−323. **The ailment plate has always covered the top of the
left candles by 51 px** — it is an opaque `Frame_Bar_02_Background` at α 0.96 — and while
the wicks were unlit stubs nobody could tell, because there was nothing bright up there to
lose. Lighting them made it visible on the first isolated render:
`out3b/T3_flameonly.png` shows **three flames on the right globe and one on the left.**

Matt asked for VFX on each of the **six** candles. Four of six is not that. The correction
is **derived, not typed**: the frame is raised until its bottom clears the tallest flame's
own computed top, using the same `WICKS[0]` and `FLAME_H` the flames are built from. With
flames off, arm 3's exact −376 is used, so the arm-3 comparator is unaffected.

**The general form is worth keeping: adding a bright element is a free audit of everything
that occludes it.** Nothing else on this HUD has been tested that way.

### 5.4 Two API-default defects, both the same class as arm 3's `_place()` note

- **`ParticleProcessMaterial.scale_*` multiplies the TEXTURE'S NATIVE SIZE, not pixels.**
  `GlowDot_01` is 256×256, so `scale_min = fw * 0.05` — a number that reads like "5% of the
  flame width" — asks for **187 px per ember**. The first render was two 200-px white blobs
  where six candles should have been (`out3b/T1_crit.png`, kept).
- **`Control.get_global_rect()` returns the UNSCALED size.** The assembly lives inside a
  Control at scale 0.62, so a punch radius taken that way is 61% too large and eats the
  ironwork. Mapping the local rect through `get_global_transform()` is correct under any
  ancestor scale, including 21:9 where the anchoring differs.

---

## §6 — ★ §1's REGISTERED PREDICTION: THE LAW PREDICTED THIS LAP. It is a PASS, and a weak one, and I said so in advance

**TCP-52 ①** — authored from arm 3's log — states: *polish is fixed per COMPONENT FAMILY;
registers amortise legibility and type but NOT geometry; each new frame family pays its own
full integration, scaling with layer count.* The dispatch registered the prediction that
**this cell adds no new component family and is therefore cheap.**

**THE PREDICTION HELD.**

| | arm 3 | arm 3b |
|---|---:|---:|
| authoring wall | ~66 min (26m27s + 9m stall + ~40m) | **46 m 45 s, unbroken** |
| passes | 34 | 47 |
| sprites vendored | 70 | **4** |
| cumulative vendoring | 158 / 3,573 = 4.42% | **162 / 3,573 = 4.53%** |
| substrate-measurement share | **44%** | **17%** |
| new component families | 3 frame families measured | **0** |

**The mechanism is visible in the numbers, not just in the total.** Substrate measurement
— the category the law says is *not* amortised — fell from 44% to 17%, and it fell
precisely because no new frame family was introduced. Every geometry fact this lap needed
already existed: the ring's opaque annulus (arm 3), the lobe centroids (arm 3), the fill
radius (arm 3), the assembly placement (arm 3). **The one new geometry campaign was the
three wick tips, and it cost four passes.** Meanwhile R-9 was *reused verbatim on a
completely different problem* — deriving the punch boundary — at zero cost, which is the
amortisation half of the law doing exactly what it claims.

**★ AND I REGISTERED THE CAVEAT BEFORE STARTING, SO IT COUNTS.** FIRST_INTENT §7 predicted:
*"law survives, but only because the new-family cost happened to be near zero, which is a
weak pass, not a strong one."* That is what happened. The candles ARE a new node class —
particles are not sprites, `GPUParticles2D` has a different lifecycle and a different
material system — and by any honest reading that is a new family. **It cost almost nothing
only because it is TINY.** Had it been a large family the law would have been tested
properly, and it was not.

**So: PASS, with the strength of the test stated.** The law's amortisation half is
directly evidenced again (a third independent instance: R-9 serving a second problem). Its
per-family half is **not tested this lap** and remains resting on arm 3's three families.
**Arm 4 introduces at least two more and is where it gets tested.**

**One thing the law does not predict, and this lap surfaces it.** Arm 3b's *instrument*
category tripled (6% → 19%) and a **new category appeared: sweep, at 13%.** Neither is
about component families at all. **Deepening an existing family is cheap in geometry and
expensive in VALIDATION**, because a deepening changes a surface's *behaviour* and
behaviour has to be swept where appearance only has to be looked at. I offer that as a
candidate amendment rather than a finding: **the law predicts BUILD cost and is silent on
PROOF cost, and on this lap proof cost 32% of the passes.**

---

## §7 — ★ WHAT THE FLAMES COST: below the measurement floor. And L7-V ④ does NOT survive the change of medium — not because it is refuted, but because it becomes untestable

**Instrument, and its failure, stated first.** `RenderingServer.viewport_get_measured_
render_time_gpu()` returns **0.0000 for every case including the deliberately expensive
ones** — the Metal backend does not implement the GPU timer. Reporting those zeros as "the
GPU cost is zero" would have been a fabricated result. Wall-clock frame time with **vsync
disabled** is the instrument of record instead.

**⚠ The bench lied once before I caught it.** `_next()` contains `await`, so calling it from
`_process()` returned at the first await while `_process` kept ticking with the index
already incremented. The result was 13 rows in which every even row carried the odd row's
data — 0.1483/0.1483, 0.1889/0.1889, in exact pairs. **The pairing is what gave it away;
a lag of one case without pairing would have looked like a plausible set of numbers.**

**The floor.** Four independent flames-OFF control runs: 6.3485, 6.3301, 6.3413, 6.3470 →
range 0.0184 ms, sd 0.0079. Frame-to-frame sd ~0.30 ms over 120 samples → SE 0.027 ms.
**Conservative floor: 0.03 ms**, on a 6.34 ms frame.

Two full bench runs, 1920×1080, Forward+/Metal, Apple M2, 40 warm frames discarded, 120
sampled. Δ is against the pooled flames-OFF control (6.3417 ms):

| case | wall ms | Δ ms | vs floor |
|---|---:|---:|---|
| no HUD at all | 6.0436 | −0.298 | **the whole HUD costs 0.298 ms** |
| **ARM 3 HUD** (opaque, unlit) | 6.3455 | +0.004 | **below floor** |
| arm 3b, flames OFF | 6.3417 | — | control |
| flames + halos, 0 embers (12 additive sprites) | 6.3560 | **+0.014** | **below floor** |
| 36 particles | 6.3635 | +0.022 | below floor |
| 144 particles | 6.3715 | +0.030 | at floor |
| 576 particles | 6.3846 | +0.043 | just above |
| 2,304 particles | 6.3864 | +0.045 | just above |
| 144 @ ×0.25 area | 6.3689 | +0.027 | below floor |
| 144 @ ×4 area | 6.3548 | +0.013 | below floor |
| 144 @ ×16 area | 6.3596 | +0.018 | below floor |
| 144 @ ×64 area | 6.3861 | +0.044 | just above |
| **2,304 @ ×16 area** | **6.4433** | **+0.102** | **3.4× floor** |

**★ gandalf's suspicion was RIGHT about the flames and WRONG about the translucency, and
both halves are worth having.** The flames sit at +0.014 ms — below the floor, as he
suspected. But *"the translucency is the whole cost"* is refuted at frame level: **arm 3's
opaque HUD and arm 3b's glass HUD are indistinguishable (+0.004 ms, below floor).** Glass
is free. His suspicion has a second, lap-cost reading, and §6 tests that one — where he is
also wrong, because the translucency was cheap to build and expensive only to *prove*.

**On §1's secondary question — the honest answer is the one the dispatch pre-blessed.**

- COUNT swept 36 → 2,304 (**64×**): +0.022 → +0.045 = **+0.023 ms**
- AREA swept ×0.25 → ×64 (**256×**): +0.027 → +0.044 = **+0.017 ms**

**Neither axis leaves the measurement floor across its entire swept range.** I cannot
reproduce L7-V ④'s discrimination here — not because count is expensive or area is cheap,
but because **the discriminating experiment does not have a signal in this medium.** The
one case that clearly rises is the one where count AND area are both extreme (2,304 @ ×16 =
36,864 area-units), which is *consistent* with cost ∝ total emitted area but does not
separate the two factors.

**★ THE RESULT FOR THE SERIAL-CONTENT PIPELINE, stated plainly: UI VFX BUDGETS AT ZERO.**
Six lit candles with 144 embers cost 0.030 ms — 0.5% of a frame — against a whole HUD at
0.298 ms and a 3D scene at 6.04 ms. To make UI particles measurable I had to ask for 384
embers on a 5-pixel wick. **The constraint on UI VFX is authoring effort and legibility,
not frame time**, and any future cell that reasons about UI VFX cost should reason about
those two instead.

---

## §8 — The legibility instrument, unmodified, fourth arm running

§4.3 requires the instrument to carry forward unchanged and to be repaired *explicitly and
as its own logged pass* if translucency breaks it. **It did not break it. No repair was
made.** Every computing function is imported from `legibility2` via `legibility3`; nothing
in either file is edited. The only addition is a fourth region set and a fourth plate path.

**⚠ FIRST_INTENT §6 pre-registered a worry about this, and the worry was MISCONCEIVED.** I
banked: *"the instrument measures contrast on an opaque surface … I may have to ship a
number that looks like a regression and argue in words that it is not."* Wrong, and the
reason rehabilitates the instrument rather than excusing a number: **`legibility2` does not
measure the surface.** It solves the HUD's per-pixel alpha from a black plate and a white
plate, composites over a bank of real gameplay frames, and measures the *composite*
against each region's own background. **A translucent surface is measured exactly as the
eye sees it.** Arm 2 built better than I gave it credit for.

The ONE region whose box moves is `ailments`, because the widget moved (§5.3). Measuring it
through arm 3's box would measure the air the row used to occupy.

### state = critical (worst case over qualifying real backgrounds)

| region | arm 3 opaque+unlit | arm 3b glass+lit | delta |
|---|---:|---:|---:|
| life_vessel | 12.17:1 | **9.52:1** | **−2.65** |
| energy_vessel | 7.82:1 | 7.72:1 | −0.10 |
| skill_bar | 12.12:1 | 12.12:1 | **+0.00** |
| t4_slot | 13.90:1 | 13.90:1 | **+0.00** |
| target_frame | 11.27:1 | 11.27:1 | **+0.00** |
| minimap | 15.30:1 | 15.30:1 | **+0.00** |
| ailments | 14.18:1 | **8.27:1** | **−5.90** |

### state = healthy

| region | arm 3 | arm 3b | delta |
|---|---:|---:|---:|
| life_vessel | 10.25:1 | **10.61:1** | **+0.36** |
| energy_vessel | 7.78:1 | **8.46:1** | **+0.67** |
| all four others | — | — | **+0.00** |

**Three things to read here, and I will not soften the first.**

1. **Translucency costs 2.65 contrast points on the life vessel at critical.** That is real,
   it is the price of the ruling, and it is the worst number in this report. It still passes
   at 9.52:1 — **3.2× the 3.0:1 threshold** — on every qualifying background, and the number
   at critical is still *better than arm 3's healthy* (10.25). But it is a cost and it is
   named.
2. **The ailment row drops 5.90**, entirely because §5.3 moved it off the dark tray and over
   the play area. 8.27:1 still passes at 2.8× threshold. **Attributable to a fix, not to the
   glass.**
3. **★ Four of seven regions are bit-identical between the arms.** `+0.00`, not "+0.00 to
   two decimals" — the same value. **That is a containment proof**: this cell demonstrably
   touched the two globes and the ailment frame and nothing else. It is the cheapest and
   strongest evidence that arm 3b is a continuation and not a redesign, and it is exactly
   what §4.1 asked for.

**And at healthy the glass WINS on both vessels.** A translucent vessel over a bright
background picks up contrast an opaque one cannot.

---

## §9 — Artifacts, and the moving artifact (§4.5)

**★ THE MOVING ARTIFACT — `~/Games/mcp-lab/l8ui/out3b/mov/`**

| file | what it is |
|---|---|
| `glass_and_candlefire.mp4` | **12 s, 1920×1080, 30 fps, one continuous take.** 0–2.5 s flames idle at full health · 2.5–9.5 s a continuous sweep 1.00 → 0.02 · 9.5–12 s hold at critical |
| `glass_and_candlefire_strip.mp4` | the same take, cropped to the assembly |
| `candles_idle.mp4` | 3.2 s, one cluster at 3×. **The flames cannot be judged at 1:1** — six flames on a 67-px ornament — and pretending otherwise would repeat arm 3's own register mistake |

Rendered through Godot's Movie Maker (`--write-movie` + `--fixed-fps 30`), so the clip is
**deterministic**: fixed dt per frame regardless of render time, which is the only way a
`TIME`-driven flipbook produces the same movie twice. Real-time screen capture would not.
The AVI master was transcoded and removed; the MP4s are the deliverable.

**The sweep is linear in LIFE FRACTION, not in surface height**, because a globe's surface
moves faster per point of HP near the top and bottom of a disc than at its middle (arm 2
measured 1.32× in the critical band), and sweeping height linearly would hide exactly the
acceleration the design is built on.

**Stills still ship and do not substitute.** 262 PNG in `out3b/`.

```
~/Games/mcp-lab/l8ui/
  ui3b/  orb_glass.gdshader · plate_punch.gdshader · flame.gdshader
         palette3b.gd · hud_glass.gd · hud_glass.tscn        (249 changed lines vs ui3/)
  kit3b/ 4 PNG
  ITERATION_LOG_ARM3B.md
  wick_probe.py · candle_probe.py (the failed instrument, kept) · glass_probe.py
  translucency.py      ← Matt's sentence as a testable claim
  bench3b.gd/.tscn     ← the VFX cost bench
  legibility3b.py      ← arm 2's instrument, fourth arm, unmodified
  capture3b.gd/.tscn · shoot3b.sh · ab3b.py · video3b.gd/.tscn · iter3b.sh
  out3b/
    AB3B_candles.png          ← THE CANDLE A/B. arm 3 vs arm 3b, 4.6x
    AB3B_orbs.png             ← THE GLASS A/B, life vessel
    AB3B_orbs_energy.png      ← the same, energy vessel
    AB3B_full.png             ← whole screen, both states
    DRAIN_STRIP.png           ← THE HEADLINE STILL: 7 points of the sweep in one row
    FINAL_16x9_* (9 states) · FINAL_21x9_* (3) · FINAL_ALPHA_* (4)
    FINAL_ARM3_* (6)          ← arm 3 re-rendered from ui3/ AS IT SITS. Exit predicate 6.5
    FINAL_DRAIN_* (7) · FORK_p{0,1}_{stone,bloom,dark} (6)
    FINAL_CANDLE_{lit,unlit}.png · PROBE_regions3b.png
    T1_crit.png               ← the 200-px ember blowout, kept
    T2_noflame.png T4_crit.png ← before the rim light, kept
    T3_flameonly.png          ← THREE flames right, ONE left. The occlusion, kept
    mov/                      ← the moving artifact
```

**Vendoring census (§4.2).** Arm 2: 88. Arm 3: 70. **Arm 3b: 4.** Cumulative **162 / 3,573
= 4.53%** (from arm 3's 4.42%). **A depth pass on an existing family consumes 4 sprites
where a full integration of a new one consumed 70** — a 17.5× ratio, and the strongest
single number in this report for the component-family law.

**★ And a correction to the dispatch's own §3 inventory, offered as a fact.** It lists
23 + 10 = 33 FX files. Verified by sha256 over all 33: **six are byte-identical across the
two packs, so the real inventory is 27 DISTINCT ASSETS.** And the collisions are
**cross-numbered**:

```
Source Glow_02    == Menus Glow_04         Source Glow_03  == Menus Glow_05
Source Glow_04    == Menus Glow_03         Source Glow_06  == Menus Glow_06
Source GlowDot_01 == Menus Glow_Dot_01     Source FireSheet_01 == Menus FireSheet_01
```

**A NAME IS NOT AN IDENTITY ACROSS PACKS.** Vendoring "Glow_05" without saying which pack
picks a different sprite in each. This is not a criticism of the inventory — the inventory
is what let me find it — but any future census that counts files is over-counting assets
by up to 18% in this folder.

---

## §10 — Ceiling list (new; arm 3's C-1…C-7 stand unchanged)

| # | the design wants | the pack has | verdict |
|---|---|---|---|
| **C-8** | **a lit candle** | `Greeble_Candles_01/02` with three and two **unlit** wicks (measured: dark stubs, luminance < 0.30), and `FX_FireSheet_01` in a different folder that nothing references | **CEILING, solved in software.** The kit ships candles and ships fire and never joins them. There is no lit-candle asset in either pack. Named here because the dispatch's fallback explicitly invites *"the pack cannot express a lit candle and here is the sprite that fails"* — and the honest answer is that it **can**, but only if you find the flipbook in the FX folder and measure its 5×4 grid yourself. |
| **C-9** | **a soft glow** | exactly ONE: `Glow_05`. `Glow_01/02/07`, `GlowDot_01`, `Glow_Small_01` are hard-edged low-poly polygons; `Glow_03` is a lozenge | **NEAR-CEILING.** One soft falloff across 27 distinct FX assets. Any effect needing two differently-shaped soft glows must reuse it at two scales. **This also partly answers arm 3's C-7** (no soft beam for the minimap cone): the pack has a soft *dot* and no soft *wedge*. |
| **C-10** | **a glass MASK for the orb** | `Frame_Orb_01_Glass` / `_02_Glass`, both thickness maps | **CEILING CONFIRMED, and re-labelled.** Arm 3 called these useless. They are useless as masks and excellent as materials. The ceiling is real — there is no orb silhouette in the pack — but arm 3b's fill boundary is analytic anyway, so the ceiling has no cost. **Downgrading it from a ceiling to a labelling error would be wrong; it is a ceiling that happens not to bind.** |

---

## §11 — HALTs to Matt (ADDED; none of the standing ones re-decided)

The six standing HALTs and arm 3's **H-7…H-12** are open and untouched, including H-7 (what
the portrait depicts) and H-8 (what the level counts), which are story questions gandalf
has taken back. Adding:

- **★ H-13 — THE SECOND BRANCH OF THE "either".** *"can we please **either** add VFX to each
  of the 6 candles on the globes?"* The sentence never says "or". gandalf declined to guess
  and asked you; I have declined too. **The stated branch is built and is in the video.**
  If the alternative was *"…or remove the candles"*, or *"…or use the other candle sprite"*,
  or *"…or put the VFX somewhere else"*, it is a different cell and I would rather build the
  right one than guess. **This is the only item on this list that blocks nothing — the ship
  is complete without it.**
- **H-14 — the R-5 / glass trade, now that it is a number.** §4 shows R-5's opacity ramp and
  your translucency ruling are the same variable pulled opposite ways. I resolved it by
  moving the danger channel entirely onto BRIGHTNESS (`glow_opac` 0.44 → 0.08), which I
  argue is faithful to R-5's own name. **The cost is that a critical globe is now
  see-through where it used to be a solid wall of amber.** The video is the place to judge
  it. If you want the wall back, the constant is one line and the sweep table in §4 tells
  you exactly what it costs in translucency.
- **H-15 — is the HUD a window or a panel?** §3's punch removes the tray's backing inside
  the globes so the dungeon reads through them. **That is a statement about what the HUD
  IS**, and it will apply to every future translucent element, not just these two. Measured,
  it is the only branch that satisfies the ruling (25× on background-sensitivity), so I
  shipped it — but the *principle* is yours, not mine.
- **H-16 — the ailment row's new home.** §5.3 raised it 59 px to stop it covering the left
  candles. It now sits over the play area rather than partly over the tray, and pays 5.90
  contrast points for it (still passing at 8.27:1). The alternative is to move the candles
  or shrink the row. **R-7 says ailments live WITH the life vessel and I have kept that;
  where exactly "with" puts them is a composition call at the boundary of your ruling.**

---

## §12 — Rulings (veto-open, with reasoning)

Arm 3's **R-1, R-2, R-4, R-6, R-7, R-9, R-10, R-11** are retained unmodified. **R-5 is
retained and amended, and the amendment is flagged rather than absorbed.** New:

- **★ R-5a (AMENDMENT) · VOID-FILLS-BRIGHT means BRIGHT, not OPAQUE.** The danger channel is
  carried by luminance and hue. Opacity was never in the rule; arm 3 got it for free because
  everything was opaque. Stated as an amendment rather than a new rule because it does not
  change what R-5 *says*, only what was silently assumed alongside it. **HALTed as H-14
  anyway, because a rule that has run three arms should not be amended by the agent who
  benefits from amending it.**
- **★ R-12 (NEW) · A REJECTION IS SCOPED TO THE USE IT WAS MADE FOR.** Arm 3 measured
  `Frame_Orb_01_Glass`, concluded "useless", and the conclusion was correct **for masks**. It
  is the ideal material. Before re-using a prior rejection, check whether the new use is
  judged by the same statistic — and if it is not, re-measure. **The generalisation: an
  asset verdict is a (asset, use) pair and filing it under the asset alone loses the half
  that makes it true.**
- **R-13 (NEW) · MEASURE THE REGION THE SHADER SAMPLES, NOT THE REGION THE FILE CONTAINS.**
  §5.1. Arm 3's `facet_ref` was a correct whole-sprite statistic used where a windowed one
  was needed, and it silently disabled a term for three arms. **A statistic and its domain
  travel together or the statistic is wrong.**
- **★ R-14 (NEW) · TURNING SOMETHING ON IS A FREE AUDIT OF EVERYTHING THAT OCCLUDES IT.**
  §5.3. The ailment plate had covered the left candles since arm 3 and was undetectable
  while they were unlit. **Every dark, static element on a HUD is hiding this class of
  defect right now**, and lighting things is the cheapest way to find them.
- **R-15 (NEW) · IF A CLAIM IS ABOUT BEHAVIOUR, BUILD THE INSTRUMENT BEFORE THE OPINION.**
  "It looks like glass" is unfalsifiable; "the globe's colour varies by 34 RGB levels across
  three backgrounds and by 0.00 in arm 3" is not. `translucency.py` took four passes and it
  found a structural conflict with R-5 that no amount of looking would have surfaced.
- **R-16 (NEW) · RE-RUN THE SWEEP AFTER THE NEXT FEATURE LANDS.** §4. `glow_opac` was
  validated at 0.12, then `stain` was added, and 0.12 stopped being monotone. **A constant
  validated against a build is not validated against the next build**, and the failure is
  silent because the old number still looks deliberate.

---

## §13 — Exit predicate (§6)

| # | predicate | status |
|---|---|---|
| 1 | §5.1–§5.7 present | **✔** §1 FIRST_INTENT banked verbatim before work · §2 both rulings realised at arm 3's states · §§3–4 + §8 the A/B and the measurements · §9 the moving artifact · §6 iteration log + the registered-prediction verdict · §7 what the flames cost · §§11–12 HALTs + rulings · §14 read-list · §12/header clock |
| 2 | substrate sha + 0444, **start AND end** | **✔** `crypt_substrate.tscn` = `d45db0f5…de1966`, mode `-r--r--r--`, verified at 01:37Z and at close. Identical. |
| 3 | `mcp-lab/project/` and `evidence/l5/` untouched, **per-file, not by directory listing-hash** | **✔ ZERO files modified in either.** `find -newermt "2026-07-26 01:36:39"` returns **0** for `project/` (across all files) and **0** for `evidence/l5/` (81 files). `project/scene_before.tscn` sha `d45db0f5…de1966`, mode 0444 — **and it is byte-identical to the l8ui substrate, which is presumably why the dispatch names both.** No `.DS_Store` caveat this lap: arm 3 had four, arm 3b has none. |
| 4 | `user://` clean | **✔** 84 files under `user://tcp-l8ui`, **all 84 under Godot's own `shader_cache/`**. Files NOT under `shader_cache/`: **0**. Zero files written by my code. |
| 5 | **arm 3's `ui3/` intact and renderable, proven by re-rendering it as the A/B's inputs** | **✔ — and proven twice over.** (a) `shasum` over every file in `ui3/` at clock start and at close: **IDENTICAL, zero bytes changed.** (b) `out3/`, `kit3/`, `ui/`, `ui2/`: **0 files** with mtime after clock start. (c) `capture3b.gd --arm=3` re-rendered arm 3 from `ui3/` as it sits — six `FINAL_ARM3_*` stills, and they are the A/B's left column and the legibility table's arm-3 row. **Every arm-3 number in §8 comes from a render made this lap.** |

**Fallback status:** not invoked. No blocker. **Ceiling-findings: three (§10), which is a
PASS under L-G.** **Refutation count: one of my own banked predictions (FIRST_INTENT §5)
and one of gandalf's stated suspicions (§7), both reported as PASSes.**

---

## §14 — Read-list declared

**Complete, in order, one unbroken segment, nothing unattested.**

The dispatch · `agentic_orchestration/drax/notes/2026-07-25-tcp-l8u3-compositional-depth-report.md`
(arm 3's report, in full) · arm 3's code on disk: `ui3/hud_deep.gd`, `ui3/palette3.gd`,
`ui3/orb_fill.gdshader`, `capture3.gd`, `shoot3.sh` · `legibility3.py` lines 1–155 (to see
how it patches `legibility2` without editing it) · `vendor_kit3.sh` header · arm 3's
`FINAL_16x9_stone_{critical,healthy}.png` **as pictures**, cropped to the globes at 2× ·
the four candle sprites **as pictures** · `FireSheet_01` and five `Glow_0N` **as pictures** ·
my own probe outputs.

**I did NOT read:** arm 1's or arm 2's reports, gandalf's earlier dispatches, or the six
reference `.webp` sheets. Deliberately. This cell has two rulings and both are about
material and motion, not composition; the reference sheets are a composition source and
re-reading them would have re-opened arm 3's settled questions. **If that was the wrong
call it is a stated wrong call, not an omission.**

**I did NOT re-read my own arm-3 report's §13 (what steered me) before writing §15 below**,
so §15 is not an echo of last lap's answer.

---

## §15 — What this dispatch did wrong (gandalf asked; this is the answer)

**First, the two convictions from arm 3, and whether the fixes worked.**

1. **Ordered-critique-as-work-order.** §2 is one paragraph, unenumerated, with both branches
   live. **IT WORKED, AND IT WORKED IN THE HARDEST POSSIBLE WAY:** the paragraph raised the
   glass sprite as an open question, I formed the *opposite* view of gandalf's implied one
   in FIRST_INTENT §5 ("probably still wrong"), measured it, and was refuted by my own probe.
   **A numbered list would have produced agreement; a paragraph produced a measurement.**
   This is the single strongest evidence in three arms that the fix is right.
2. **L-Q, ratifying an unmeasured cause.** Not committed here. §0 says *"Wick positions are
   yours to measure — I am not handing you coordinates I got by looking"*, and that sentence
   is why `candle_probe.py`'s failure was mine to find and fix in four passes instead of a
   handed-over number being silently wrong. **The self-denial is load-bearing.**

**Now the things it does wrong instead. Three, and the first is the real one.**

**★ 15.1 — §1 PRE-REGISTERS A PREDICTION AND THEN NAMES THE VERDICT THAT COUNTS AS
INTERESTING.** *"If it comes back expensive, the law is wrong or incomplete, and that is
worth more than the HUD."* and *"A refutation is a PASS."* Both true, both well-meant, and
together they put a **thumb on the scale in the direction of refutation.** A cell that knows
refutation is the prized outcome has an incentive to find the lap expensive — to categorise
generously, to count a pass twice, to let the sweep sprawl. **I do not think I did that, but
I cannot prove I did not, and that is the problem.** The registration is right; the
editorialising about which result is worth more should not have been in the same section.
**A pre-registration should say what will be measured and how, and stop.**

**★ 15.2 — §1 REGISTERED A PREDICTION ABOUT *COST* AND NEVER SAID WHICH COST.** The
component-family law is about **build effort**. §1's own "sealed suspicion" —
*"the flames are too cheap to measure and the translucency is the whole cost"* — reads
naturally as **frame time**. Those are different quantities with different instruments and
they gave **opposite answers**: at frame time the translucency is free and the flames are
free; at lap cost the translucency was cheap to build and expensive to *prove*. I answered
both because I noticed the ambiguity, but the dispatch never resolves it, and a cell that
picked one would have reported a defensible half-truth **and gandalf would have had no way
to tell which half.** The word "cost" needs a unit every time it is registered.

**15.3 — §4.3 assumes the instrument is at risk and thereby aims the search at it.**
*"If translucency breaks the instrument, say so and repair it explicitly."* Reasonable, and
it planted a hypothesis I banked in FIRST_INTENT §6 and then had to spend a pass
disproving. **The instrument was never at risk** — `legibility2` measures the composite over
real backgrounds, so translucency is exactly what it was built for (§8). The clause is
harmless in outcome and it is still a steer: it made me *expect* a regression, and an agent
expecting a regression is an agent primed to accept one. **The neutral form is "report what
the instrument says and whether you changed it," with no forecast about which.**

**15.4 — the launch prompt, the channel gandalf says he cannot self-audit.** He predicted
one sentence pointing at the file. **It was one sentence pointing at the file**, and it
contained no steer. Recorded because last lap this channel carried a defect and this lap it
did not, and a fix that worked deserves the same attention as one that failed.

**And one thing it did unusually right, since a critique that only subtracts is not
useful.** §0 states *"Matt's is better and mine is withdrawn"* about gandalf's own drafted
fix, **with the reason** — that his version would have re-imposed the genre default on top
of my invention. Naming a withdrawn alternative and why it lost is the most useful sentence
in the file: it told me what NOT to drift toward, which a bare instruction cannot do. The
red-liquid-line fix would have been my own second instinct, and I would have reached for it
at exactly the moment §4's monotonicity conflict appeared.

---

**Signed:** drax, 2026-07-26. Presentation seam.
