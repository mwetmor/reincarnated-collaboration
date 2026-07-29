# PROVISION-CAL · rider PC-LIGHT-V2 — the wall-top fork, measured

**Agent:** drax (presentation seam) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-07-28
**Status:** **COMPLETE** — plates rendered, numbers reported, fork NOT ruled (§8)
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

All four rendered through the unchanged `tmp/pclight/light_rig.gd` at settle 90, R-6, 1280×720.
Variant deltas are applied by `tmp/pclight/setvar.py`, a scoped regex switcher, so a variant is
never a hand-edit and cannot drift between renders.

### 3.1 What each variant IS

| | delta from A | one property? | mechanism |
|---|---|---|---|
| **A** | — (the accepted PC-LIGHT state, uncommitted +56/−9) | control | — |
| **B** | `Key.light_energy` **0.0 → 0.06** (colour already cold, staged) | yes, 1 value | directional sky-leak |
| **C** | wall-cap `black_point` **0.0 → 0.20** | yes, 1 shader uniform | the void-cap's own outer-lip floor |
| **D** | both of the above | 2 values, disjoint surfaces | composite |

**Why C is a material property and not a light.** Because §2.1 measured that a light cannot do it.
The wall-cap slabs are `render_mode unshaded`; a 2.0-energy directional sun moves them **1.5 %**.
The rider left the mechanism to my call and forbade props; the only remaining channel into the
wall-top surface is the void-cap material itself. `black_point` is the uniform that sets the value
of the cap's outer lip — the exact 38.4 % of wall-top pixels that measure at or under luma 12 in A.
Both cap paths (`_build_void_mat`, `_build_void_cap_occlude_mat`) route through the single
constructor `_build_walltop_cap_mat`, so this is one edit at one site.

> **A scoping catch, kept because the assert caught it and my reading had not.** `black_point`
> appears **twice** in the builder. The second (`_south_mat_common`, line ~806) is the SOUTH WALL
> FACE material on a different shader — not a wall top. An unscoped replace would have made C a
> two-surface change and quietly invalidated the one-property claim. The switcher is scoped to the
> body of `_build_walltop_cap_mat`.

**The value 0.20 was picked against a gate declared BEFORE any C frame was rendered:**
*wall tops must stop containing a pure-black region (`wt_under12 < 5 %`, down from 38.4 %) while
not becoming the brightest thing in frame (`wt_mean` below the shipped room's own p95 of 68.5).
Take the SMALLEST black_point on a coarse ladder that clears both.* The ladder, all three rendered:

| black_point | wt_mean | wt_mod | wt_under12 | gate |
|---|---|---|---|---|
| 0.00 (= A) | 31.03 | 65.47× | 38.4 % | fails |
| **0.20** | **38.44** | **4.23×** | **1.0 %** | **clears — selected** |
| 0.30 | 41.07 | 3.17× | 0.2 % | clears (not smallest) |
| 0.40 | 43.36 | 2.64× | 0.1 % | clears (not smallest) |

### 3.2 ★ WTMASK — the rider's headline table

56,250 px, full resolution. **Higher `wt_mean` = wall tops carry more value. `wt_mod` = p95/p05
across the wall tops; it falls when the band stops being half-black.**

| | **wt_mean** | Δ vs A | wt_p05 | wt_p50 | wt_p95 | **wt_mod** | **wt_under12** |
|---|---|---|---|---|---|---|---|
| BEFORE (defect) | 31.51 | +1.5 % | 1.2 | 38.1 | 65.3 | 53.88× | 38.3 % |
| **A** as-fixed | **31.03** | — | 1.0 | 38.0 | 65.5 | **65.47×** | **38.4 %** |
| **B** cold sky-leak | **31.04** | **+0.03 %** | 1.0 | 38.0 | 65.5 | **65.47×** | **38.4 %** |
| **C** wall-top light | **38.44** | **+23.9 %** | 15.5 | 40.0 | 65.5 | **4.23×** | **1.0 %** |
| **D** B+C | **38.45** | **+23.9 %** | 15.5 | 40.0 | 65.5 | **4.23×** | **1.0 %** |

**The rider asked directly whether B lights the wall tops on its own. It does not.** B moves the
wall-top mean by **0.01 luma out of 31.03** — 0.03 %, one two-hundredth of a display level — and
moves `wt_p05`, `wt_p50`, `wt_p95`, `wt_mod` and `wt_under12` by **nothing at all** to the
reported precision. Sky light does land on wall tops first in a physical room; in this room the
wall tops are not in the lighting pass, so it lands on them not at all.

The 58-pixel `Topper_*` sub-population is the only wall-top surface B touches: **43.60 → 45.61
(+4.6 %)**. Four corner-pillar caps, 0.10 % of the mask.

**D is therefore not redundant, and it is not optional** — B and C act on disjoint surfaces, so a
composite is the only variant that can carry both a cold room rim and lit wall tops.

### 3.3 Contrast cost vs A

LSTAT-2 (mask-locked to `before00`, the metric the predecessor cell steered by). The counter-gate
of predecessor §2.2 is reproduced unchanged: **legibility `u12 < 15 %`, key `p50` in 25–45.**

| | **LSTAT-2 contrast** | **cost vs A** | p50 | mean | u12 | gate |
|---|---|---|---|---|---|---|
| **A** | **7.63×** | — | 24.8 | 31.2 | 11.1 % | clears (p50 marginal, as shipped) |
| **B** | **6.83×** | **−10.5 %** | 26.9 | 32.7 | 7.1 % | clears |
| **C** | **7.56×** | **−0.9 %** | 24.8 | 31.3 | 11.0 % | clears (p50 marginal, as A) |
| **D** | **6.83×** | **−10.5 %** | 27.0 | 32.8 | 7.1 % | clears |

**C's contrast cost is 0.9 % — essentially free**, and it is 0.9 % rather than 0 % only because
some wall-cap pixels fall inside the BEFORE-derived LSTAT-2 room mask. **D costs exactly what B
costs**: C adds no measurable contrast cost on top of it (6.83× either way).

LSTAT-1, still reported and still given no weight (predecessor §3.2): A 5.16× · B 4.86× ·
C 5.08× · D 4.81×. It ranks D as identical to the original defect. It is wrong for the reason
established in the predecessor cell.

### 3.4 The spatial number, per variant

The predecessor's §3.1 test: freeze the 82 cells of the 16×9 map that BEFORE rendered as the
daylit plateau (cell mean > 60), read the same cells after.

| | min | max | max/min | **p90/p10** |
|---|---|---|---|---|
| BEFORE | 60.3 | 105.0 | 1.74× | **1.22×** |
| **A** | 14.8 | 106.7 | 7.21× | **2.62×** |
| **B** | 16.2 | 107.1 | 6.61× | **2.45×** |
| **C** | 14.8 | 99.4 | 6.72× | **2.52×** |
| **D** | 16.2 | 99.8 | 6.16× | **2.36×** |

> **Instrument caveat, stated because it cuts against C.** The 16×9 cell map averages only pixels
> over luma 12 **per frame**, so it carries the LSTAT-1 hazard. C's `max` falling 106.7 → 99.4 is
> not the room's brightest cell getting darker — C cannot darken anything, it is a monotone lift.
> It is cap pixels *crossing the 12 threshold from below* and joining a cell they were previously
> excluded from, pulling that cell's mean down. **Read the WTMASK table (3.2) and the LSTAT-2 table
> (3.3) for C; this one is reported for continuity with the predecessor, not for C's verdict.**

### 3.5 D composes cleanly — measured, not assumed

Per-pixel test of whether D is exactly A plus B's delta plus C's delta:

```
| D - (A + (B-A) + (C-A)) |    max 1/255   mean 0.0049   pixels with error > 2:  0  (0.0000%)
```

Zero pixels diverge by more than one display level over the whole 1280×720 frame. The overlap
between B's changed pixels (510,495) and C's changed pixels (69,036) is **6,922 px (1.4 % of B's,
10 % of C's)** — glow spill and the shaded toppers, the only surfaces both deltas can reach.
**D is a clean composite; the rider's "only if it composes cleanly" condition is met.**

---

## §4 — Determinism

Per the rider, a determinism check on at least A, abbreviated, using the predecessor's own
instrument — including its §4.2 correction that **run-to-run identity at a fixed settle does not
clear the accumulator lockout; the settle count is the axis the accumulator lives on.**

| test | result |
|---|---|
| `v2_A` vs `afterA` — the predecessor cell's frame, **different session, different process** | **byte-identical**, sha256 `992a1ccf…` |
| `v2_A` vs `v2_A_s40` — **settle 90 vs settle 40** (the discriminating test) | **0 differing px**, same sha |
| `v2_A_restored` — A re-rendered after six intervening builder edits and seven renders | **byte-identical**, same sha |
| `v2_B` vs `s14` — B re-produced from the predecessor's parked variant | **byte-identical**, sha `12beadd1…` |
| `v2_C` vs `v2_C020` — C re-rendered from the ladder step it was selected from | **byte-identical**, sha `8091a8f5…` |

**Verdict: LOADS-CLEAN / no accumulator, and settle-invariant.** Variant A's sha now has **seven
independent Godot processes** behind it across two sessions. No SDFGI was enabled on any variant.
The positive control that validated this instrument in both directions is the predecessor's §4.2
and is not re-run here (abbreviated per the rider).

Variant sha256 prefixes, for anyone reproducing: **A** `992a1ccfba93` · **B** `12beadd132d4` ·
**C** `8091a8f53e41` · **D** `21cbd8e8818e`.

---

## §5 — Plates

All under **`/Users/admin/Games/reincarnated-godot/tmp/pclight/REVIEW2/`**. Same camera, same
render settings, same resolution for every frame. Kept local and untracked — they show Synty
textures and the `/Assets/Synty/` licence rule forbids a shared remote.

| file | what |
|---|---|
| `A_as_fixed.png` | variant A, labelled with both stat sets |
| `B_cold_skyleak.png` | variant B |
| `C_walltop_light.png` | variant C |
| `D_composite.png` | variant D |
| **`COMPARE_4UP_ABCD.png`** | **the 4-up sheet — A \| B \| C \| D, stats burned in.** The composition plate |
| **`WALLTOP_DETAIL_4UP.png`** | **the fork at a scale where it is visible** — native pixels at 3× nearest over the near SE wall run. The crop was **not chosen by eye**: it is the 360×150 window maximising the count of pixels where C differs from A by >4 levels (integral-image search, stride 10), so the plate cannot be accused of being framed to flatter a variant |
| `WALLTOP_MASK.png` | the WTMASK footprint overlaid in red on A — **the mask is auditable, not asserted** |
| `STATS_TABLE.png` | every number in this rider, as an image |

Raw frames `tmp/pclight/frames/v2_*.png` · masks `tmp/pclight/masks/mask_{top,caps,topper}.png` ·
per-variant stats `tmp/pclight/{stats,wt}_v2_*.json` · render logs `tmp/pclight/v2_*.log`.

**No aesthetic verdict is offered, here or anywhere above. The fork is Matt's call.**

---

## §6 — Findings, logged

- **★ V-1 — the wall tops are outside the lighting system.** `walltop_void.gdshader` is
  `render_mode unshaded` and its header says so on purpose. **No light — no energy, no colour, no
  position, no count — can change the wall-top slabs.** Measured, not inferred: a 2.0-energy
  directional sun plus a 0.45 fill moves them **1.5 %**, and that is an upper bound because the
  brighter room also spills more glow. Anyone who later reads "the wall tops need light" as a
  lighting task will burn a cell on it. It is a **material** task.
- **★ V-2 — Matt's question and the S14 sky-leak are NOT the same mechanism.** Gandalf's read was
  that sky light lands on wall tops first, which is true of a physical room and false of this one.
  **B moves the wall tops by 0.03 %.** The two questions are independent and can be ruled
  independently — which is also why D exists and composes to within 1/255.
- **V-3 — "unlit" measures as bimodal, not dim.** In A the wall-top band is 38.4 % pure black
  (the void-cap's outer half, `black_point = 0.0`) against an inner half at luma 38–65 — which is
  *brighter* than the shipped room's median floor pixel (24.8). The wall tops are not dark. They
  are **half-black, and constant**: they do not respond to the fire, so they read as not
  participating. If Matt's "I also kind of like the contrast" is about that hard black edge, C is
  precisely the property that removes it, and 0.20 removes 97 % of it (38.4 % → 1.0 %).
- **V-4 — C touches a design-owned constant, and this note is not proposing it.** `black_point`,
  `split_frac` and `feather` are the walltop-void design's own knobs (shader authored 2026-06-21,
  with a Matt ruling of 2026-06-22 attached to the same file's occlusion behaviour). C is a
  **measurement variant produced to answer a question**, not a recommendation, and it is not
  committed. If the fork rules toward lit wall tops, whether the mechanism should be `black_point`
  or `split_frac` (widen the lit band, keep the outer lip at true black so the wall top still
  dissolves into the background) is a **design call that belongs to gandalf/Matt, not to me** —
  both are one property, and I measured the one that addresses the measured deficit.
- **V-5 — the twin file, restated.** `scripts/walltop_level.gd` still carries the byte-identical
  copy of the old lighting block (predecessor L-1). Untouched by this rider. It does **not** carry
  a copy of the cap material, which is built only in `kit_replica_level.gd`.
- **V-6 — an instrument hazard, caught by an assert.** `black_point` appears twice in the builder;
  the second is the south wall FACE material on a different shader. An unscoped edit would have
  made C a two-surface change while still being described as one property. The variant switcher is
  scoped to `_build_walltop_cap_mat`. Named because the failure mode is silent.

---

## §7 — Repo state (PC-T3 discipline)

**Nothing is committed in `reincarnated-godot`.** The working tree is left in **state A**, verified
two ways: `git diff --stat` returns **`+56 / −9`** on the one tracked file, and
`git status --untracked-files=no` returns **exactly one line** — `M scripts/kit_replica_level.gd`.
`v2_A_restored`, rendered *after* the restore, is **byte-identical to A** (sha `992a1ccf…`), so
the restore is proven at the pixel level rather than by inspection of the diff.

**UNTRACKED, new — this rider's instrument** (`tmp/` is scratch, none of it is repo product):
`tmp/pclight/mask_rig.gd` · `mask_rig.tscn` · `shootmask.sh` · `wt_stats.py` · `setvar.py` ·
`make_plates_v2.py` · `masks/` (3 PNG) · `frames/v2_*.png` (9) · `REVIEW2/` (8 PNG) ·
`wt_v2_*.json` · `stats_v2_*.json` · `v2_*.log`.

`project.godot` unmodified. `AGENT_STATE.md` in `reincarnated-godot` deliberately not written, for
the predecessor's reason: it would leave a second tracked modification in a repo this work is
instructed not to commit. **This note is the record.**

---

## §8 — Summary

| | |
|---|---|
| **Question** | do the wall tops want light, and is that the same mechanism as the S14 cold sky-leak |
| **★ Mechanism answer** | **no** — the wall-top caps are `render_mode unshaded`; lights cannot reach them, and a 2.0-energy sun moves them 1.5 % |
| **★ Does B light the wall tops?** | **no — +0.03 %** (31.03 → 31.04 mean), zero change in p05/p50/p95/modulation/black-fraction |
| **What C buys** | wall-top mean **+23.9 %**, pure-black fraction **38.4 % → 1.0 %**, modulation 65.47× → 4.23× |
| **Contrast cost vs A** | **B −10.5 %** (7.63× → 6.83×) · **C −0.9 %** (7.63× → 7.56×) · **D −10.5 %** |
| **Does D compose?** | **yes** — max residual **1/255**, zero px above 2, across the whole frame |
| **Counter-gate** | all four clear the predecessor's legibility + key gate |
| **Determinism** | **CLEAN** — A byte-identical across 7 processes / 2 sessions, settle-invariant |
| **Repo** | not committed; working tree left in state A, verified by re-render |
| **Owed to Matt** | the fork itself. Four plates, one sheet, one detail plate, one table. **No recommendation is offered.** |

---

**Signed:** drax (presentation seam), 2026-07-28.
Evidence: `/Users/admin/Games/reincarnated-godot/tmp/pclight/REVIEW2/`.

---

# §9 — FINAL (cell PC-LIGHT-FINAL) — ruled, applied, committed

**Appended 2026-07-28 by drax.** Closes cells PC-LIGHT + PC-LIGHT-V2.

## 9.1 The ruling

**Matt, two rounds, final: variant B** — the S14 cold sky-leak — **with cold "daylight grey" upper
walls, and NO warm glow on wall tops.** Verbatim: *"warm belongs only where fire lives"* — warm
stays reserved for the floor pools and future **motivated** corner torches, which are race-brief
dressing and not this cell. **Variant C (wall-top `black_point` lift) is NOT adopted. Wall caps
stay dark — Matt likes the contrast.**

So of the fork this rider measured, the ruling takes **B and refuses C**, which also means **D is
off the table**. `black_point` is left at **0.0 at both of its sites**; nothing from §3.1's C
mechanism is in the tree. Finding **V-4** (C touches a design-owned constant) is therefore moot,
and **V-3**'s hard black outer lip is now a *ruled* property of the crypt rather than an open
question.

## 9.2 Applied state

One property on top of the accepted state-A fix, exactly as §3.1 defined B:

```
key.light_energy   0.0 -> 0.06        (light_color already cold (0.55, 0.66, 0.95))
```

Everything else in state A is unchanged. `black_point` 0.0 · `fog_density` 0.015 ·
`glow_hdr_threshold` 1.25 — all untouched, per §4.4 of the predecessor.

## 9.3 Verify — the fork, at R-6, settle 90

| | plate B (this rider) | **PC-LIGHT-FINAL re-render** | agrees |
|---|---|---|---|
| LSTAT-2 contrast p95/p05 | 6.83× | **6.833×** | ✓ |
| cost vs state A (7.63×) | −10.5 % | **−10.44 %** | ✓ |
| p50 | 26.9 | **26.887** | ✓ |
| mean | 32.7 | **32.739** | ✓ |
| room ≤ luma 12 | 7.1 % | **7.149 %** | ✓ |
| LSTAT-1 (no weight) | 4.86× | **4.863×** | ✓ |

Counter-gate clears: `u12` 7.1 % < 15 %, `p50` 26.9 ∈ [25, 45].

**Determinism (abbreviated, per the brief).** Three fresh processes this session — settle 90,
a second settle 90, and **settle 40** (the discriminating axis per the predecessor's §4.2 method
note) — all return **sha256 `12beadd132d4…`**, which is also `v2_B`'s and `s14`'s sha from the two
earlier sessions. **Five processes, three sessions, one sha. LOADS-CLEAN, settle-invariant.**

## 9.4 Twin disposition — FIXED, and it earned its own measurement

**The old block was not intentional in the twin. It was propagated.** But `scripts/walltop_level.gd`
is **not a dead twin**: it is THE level-content seam, consumed by **`playshell.gd` (the live
play-shell)**, the PNG harness `build_walltop_void_test.gd`, and two probes. So this was a change to
the stage a player actually walks around in, and it was not made by copy-paste.

- **The defect was really there.** Twin BEFORE, same R-6 camera: room p50 **100.3**, contrast
  5.35×, **0.0 %** under threshold — the same daylit plateau CEILING-1 describes.
- **The values port exactly**, because the two rooms are dimensionally identical: `FLOOR_EDGE`
  17.5, `WALL_H` 3.005743, pillars at the same `half + WALL_THICK` corners. Verified, not assumed.
- **★ It was re-measured WITH THE KING IN FRAME**, because the only live Matt ruling on this
  scene's photography — **2026-06-22**, `glow_hdr_threshold` 1.0 → 1.25 — was made against *the
  king's LIT white-plate gauntlet under the 2.0-energy key this change deletes*. A lighting cell
  that only rendered the empty room would have invalidated a live ruling and not known. New rig
  `tmp/pclight/twin_rig.gd`; king mask 28,109 px, rendered and depth-resolved (the WTMASK
  technique of §1.2), not projected.

| twin, R-6 | BEFORE | AFTER | |
|---|---|---|---|
| room p50 | 100.3 | **31.4** | the plateau goes |
| room contrast (mask-locked) | 5.35× | **5.75×** | +7.5 % — *see the caveat below* |
| **walked-floor p90/p10** (86-cell frozen set) | **1.51×** | **2.44×** | **+62 %** |
| walked-floor max/min | 2.43× | **6.80×** | 2.8× more range |
| KING mask mean luma | 141.55 | **109.79** | still **3.5×** the room's median pixel |
| KING p05 | 93.1 | **50.5** | |
| **KING pixels ≤ luma 12** | 0.0 % | **0.0 %** | **the king does not go dark** |
| KING modulation p95/p05 | 2.53× | **4.46×** | shaped by light, no longer flat-lit |

**★ Read the SPATIAL number on the twin, not p95/p05 — and this is stated because it cuts against
the flattering figure.** The twin's mask-locked contrast moves only +7.5 % where the fork's moved
+42 %. That is not a weaker fix; it is a squeezed ratio. The king's near-clipping white plate pins
p95 in **both** frames, and this room's floor stone is lighter than the fork's, which lifts p05 —
so both ends of `p95/p05` are held by things that are not the defect. CEILING-1 is an **evenness**
defect and evenness is spatial: on the identical-86-cell test the twin goes **1.51× → 2.44×**, the
same class of win as the fork's 1.22× → 2.62×.

**The 2026-06-22 glow ruling is over-served, not broken.** King pixels over luma 200, by hue:
near-neutral (the white plate) **633 → 199**, teal-emissive (the blade) **110 → 77**. The ruling
asked for *less* bloom on the lit gauntlet; deleting the key moves it further in the ruling's own
direction, while the genuinely-emissive blade still halos. **`glow_hdr_threshold` left at 1.25.**

**Twin determinism — the lighting is clean; the KING free-runs.** Twin frames *with* the king
differ run-to-run (max channel delta 198, **76 % of differing pixels inside the king mask**). With
`--noking`, the same stage is **byte-identical across three processes and settle-invariant**
(sha `fe9d95e2…`). So the divergence is the king's unpinned animation / cape / aura phase in my
rig — **not an accumulator, and not introduced by the lighting.** The king stats above are robust
to it: across three animation phases, mask mean 109.79 / 110.26 / 107.79 (2.3 % spread), p05
50.5 / 51.0 / 50.8, `≤12` **0.0 % in all three**.

> **METHOD NOTE (standing).** Any future check-9 on the play-shell stage must run **`--noking`**
> or pin the king's pose. Otherwise it will read nondeterministic for a reason that has nothing
> to do with what it is testing — the same class of error as the fixed-settle trap in the
> predecessor's §4.2, one level up.

## 9.5 Owed, named rather than silently skipped

- **The four sconces still have no fixture mesh**, and the fix has now put them in **both** files.
  Prop work, out of a lighting-only scope. This is exactly where Matt's *"future motivated corner
  torches"* are expected to land — the mounts are already at the four corner pillars.
- **The twin runs the fork's values against a different floor albedo.** They repair the defect
  there (§9.4), but a twin-specific tune is owed if the play-shell becomes a judged surface.
- **L-3 / the room is still empty** — untouched, and no lighting change addresses it.

## 9.6 Repo

**Committed and pushed** in `reincarnated-godot`: **`8caa733`** — `scripts/kit_replica_level.gd`,
`scripts/walltop_level.gd`, `AGENT_STATE.md`. The PC-T3 "nothing is committed" discipline of §7
was scoped to the measurement cells; this cell was authorised to land it. `AGENT_STATE.md` is now
written, since there is finally a commit to explain it.

Instrument and plates stay **untracked** under `tmp/pclight/` — they show Synty textures and the
`/Assets/Synty/` licence rule forbids a shared remote. New this cell: `twin_rig.gd` ·
`twin_rig.tscn` · `shoottwin.sh` · `make_plates_final.py` · `masks/mask_king.png` ·
`REVIEW_FINAL/{FINAL_B_shipped,TWIN_AB,KING_MASK}.png`.

---

**Signed:** drax (presentation seam), 2026-07-28. PC-LIGHT · PC-LIGHT-V2 · PC-LIGHT-FINAL closed.
