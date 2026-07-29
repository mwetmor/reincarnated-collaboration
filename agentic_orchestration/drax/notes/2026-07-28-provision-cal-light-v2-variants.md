# PROVISION-CAL · rider PC-LIGHT-V2 — the wall-top fork, measured

**Agent:** drax (presentation seam) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-07-28
**Status:** **IN PROGRESS**
**Predecessor:** `2026-07-28-provision-cal-light-datum.md` (cell PC-LIGHT — defines LSTAT-1/2, the
R-6 camera, the counter-gate, and variant S14). Read it first; every instrument named here is
defined there.

**The fork this note exists to measure.** Matt eye-checked the PC-LIGHT after-plate (PASS), then
opened a question the cell had not asked: *the wall tops are unlit, and I am genuinely unsure
whether they should be — I also kind of like the contrast.* Gandalf's read: that question and the
cell's parked S14 cold sky-leak may be the same mechanism, because sky light lands on wall tops
first.

**This note does not rule the fork.** It produces the plates and the numbers. Per the rider, no
recommendation stronger than reporting what each variant measures is offered anywhere below.

---

## §1 — Instruments

### 1.1 Carried forward, unchanged

**LSTAT-2**, the mask-locked contrast metric, mask frozen to `frames/before00.png`'s lit set
(72,175 sampled px). **R-6 camera**, unmoved: dist 34 · fov 24 · yaw 47 · pitch −50 · aim_h 1.0 ·
1280×720. Tool `tmp/pclight/light_stats.py`, rig `tmp/pclight/light_rig.gd`, settle 90.
LSTAT-1 is still printed by the tool and is still given no weight (predecessor §3.2).

### 1.2 New — WTMASK, the wall-top mask stat

Tool `tmp/pclight/wt_stats.py`. Mask generator `tmp/pclight/mask_rig.gd` + `shootmask.sh`.

**The mask is a RENDER, not a rectangle and not an analytic projection.** The same stage, the same
R-6 camera, the same depth buffer — with the wall-top meshes forced flat **white** via
`material_override` and every other mesh forced flat **black**, ambient/fog/glow off and the
tonemapper set LINEAR so white stays 255. A pixel is in WTMASK iff its red channel exceeds 128 in
`masks/mask_top.png`. Rendering rather than projecting is what resolves **visibility**: the near
(S/E) caps are partly hidden by the room's own geometry, and an analytic projection of the cap
boxes would have put pixels in the mask that the camera cannot see. The mask is registered to the
measured frames by construction.

**Group `top` = `WallCap_*` (28 meshes) + `Topper_*` (4).** That is the literal wall-top surface:
the 28 wall-cap slabs seated at `y = WALL_H + CAP_LIFT + CAP_THIN/2 ≈ 3.09`, plus the four
corner-pillar cap modules. **56,250 px at 1280×720 = 6.10 % of frame.**

**Full resolution, no stride.** LSTAT-1/2 sample stride-3 because they measure a 70 %-of-frame
room. WTMASK is a thin ring; a stride-3 sample would drop the near-wall bands almost entirely.

Reported per frame: `wt_mean` (are they lit) · `wt_p05/25/50/75/95` · `wt_min/max` ·
**`wt_mod` = p95/p05 inside the mask** (is there shape across the wall tops, or is the band one
flat value) · `wt_under12` (% reading as black) · `wt_dark50`.

Instrument control, run before any variant (L-N — clear the instrument first): the mask must be
capable of reading a *difference*. It is — see §2.2, where it separates the 28 caps from the 4
toppers and returns opposite verdicts for them on the same frames.

---

## §2 — What the mask found BEFORE any variant was authored

### 2.1 ★★ The wall tops are not lit by lights, and cannot be

`scripts/walltop_void.gdshader` — the material every `WallCap_*` routes through — declares

```
render_mode unshaded, cull_disabled, blend_mix, depth_prepass_alpha;
```

and its own header states the reason: *"Rendered UNSHADED so the gradient is fully controllable
(lighting can't lift the outer black back up)."* **The wall-top slabs are excluded from the
lighting pass by design.** Their value is `stone_tex × stone_tint × mix(1.0, black_point, fade)`,
a pure authored constant per fragment.

This is not read off the source and asserted — it is **measured**, on frames that already existed:

| WTMASK, group `top` (56,250 px) | BEFORE (Key **2.0** warm + Fill 0.45) | A (as-fixed, Key 0) | Δ |
|---|---|---|---|
| wt_mean | 31.51 | 31.03 | **−1.5 %** |
| wt_p50 | 38.1 | 38.0 | −0.3 % |
| wt_p95 | 65.3 | 65.5 | +0.3 % |
| wt_under12 | 38.3 % | 38.4 % | +0.1 pt |

**Deleting a 2.0-energy directional sun and a 0.45 fill moved the wall tops by 1.5 %** — and even
that 1.5 % is an upper bound, because BEFORE's much brighter room spills more glow onto the band.
The whole PC-LIGHT re-author, 9 property values and 4 new omnis, is invisible on this surface.

**Corollary, which is the rider's first question answered:** a lighting variant cannot be the
mechanism for variant C. Whatever C is, it has to reach the caps through the only channel that
reaches them — the void-cap material itself.

### 2.2 The mask separates two populations, and the instrument is validated by that

| group | px | BEFORE | A | B (S14) | light-reachable? |
|---|---|---|---|---|---|
| `caps` — `WallCap_*` | 56,192 (**99.90 %**) | 31.46 | 31.01 | 31.03 | **NO** — unshaded |
| `topper` — `Topper_*` | 58 (**0.10 %**) | 76.25 | 43.60 | 45.61 | **yes** — normal spatial mat |

The four pillar toppers *are* shaded and move exactly as a lit surface should (−43 % when the sun
is deleted, +4.6 % when S14's sky-leak is added). They are **58 pixels**. WTMASK is 99.9 % caps,
so the whole-mask number is the caps' number.

That split is also the instrument's own positive control (L-N): a metric that returned "no change"
on every group would be an unvalidated NO. It returns a large change on the toppers and ~zero on
the caps, **from the same frames through the same code path.**

### 2.3 What "unlit" measures as, precisely

The wall tops are **not uniformly dark.** In A the band is bimodal by construction — the void
shader splits every cap at `split_frac = 0.50` with a `feather` of 0.14, inner half lit stone,
outer half driven to `black_point = 0.0`:

| A, WTMASK percentiles | 1.0 | 3.1 | 38.0 | 53.1 | 65.5 |
|---|---|---|---|---|---|
| | p05 | p25 | p50 | p75 | p95 |

**38.4 % of wall-top pixels sit at or under luma 12 — pure black — and the rest sit at 38–65,
which is *brighter* than the shipped room's own median floor pixel (24.8).** So the measured
content of "the wall tops are unlit" is not a dim band. It is a band with a **hard black outer
half** that does not respond to anything happening in the room, next to a lit-stone inner half
that also does not respond. What is missing on the wall tops is not level; it is **participation**.

---

## §3 — Variants

*(appended per variant)*

---

## §4 — Determinism

*(appended)*

---

## §5 — Plates

*(appended)*
