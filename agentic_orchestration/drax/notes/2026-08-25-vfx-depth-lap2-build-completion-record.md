# VFX-DEPTH LAP-2 — BUILD WAVE COMPLETION RECORD

**Date:** 2026-08-25 · **Agent:** drax (builder) · **Measurer:** galadriel · **Conductor:** gandalf (RUN-CONDUCTOR)
**Spec:** `agentic_orchestration/gandalf/vfx-depth-run/lap2-depth-spec.md`, sealed at collab `8e36bf4a`, DRIFT-CRITIC-approved (§ 5)
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-25-vfx-depth-run-charter.md` R-18..R-21
**Class:** evidentiary note · **Status:** CURRENT
**Venue:** Cathedral, W2 B-arm scene, ratified judging camera (player_lock k = 0.665)

> **What this file is and is not.** Every acceptance criterion in the spec is **galadriel's to measure**. Nothing
> below is a self-certification. Where I ran an instrument of my own it is labelled as **mine**, with its
> segmentation stated, precisely so that a disagreement with her numbers is legible as a difference of
> instrument rather than a contradiction of fact. My eyeball notes are labelled as eyeball notes.

---

## 1. HEADLINE

**7 of 7 landed: T-1 → T-6 plus B-1.** Nothing parked. One **partial refusal** inside T-4 (the onset accent's
*mechanism*, not its requirement — § 5). One **forced re-ordering** (T-3 ahead of T-2 — § 3). Two spec constants
overridden against measurement, both flagged venue-coupled (§ 6).

**N = 3.** Measured from the `contact` signal at build time as ordered. It is neither of the two numbers the
spec carried.

---

## 2. START COMMIT + GUARDED-DIFF SUMMARY (defeat-condition audit)

| item | value |
|---|---|
| **START commit** | `f0e8d6dc5d6512821cb1e9da3411fddae466e0c3` (`drax(G-5): the 3-D tracking-camera null…`) |
| **END commit** | `0821b6a` (+ the B-1 artifacts commit, § 8) |
| **Files touched, ENTIRE wave** | **exactly two** — `scripts/wwcr_whirlwind.gd`, `scripts/wwcr_stage.gd` |
| **Diff** | `wwcr_whirlwind.gd` +1494/−41 · `wwcr_stage.gd` +352/−1 |

Pre-build hashes, verified **byte-identical to the W2 B-arm reproduction manifest** before the first edit —
so this wave's diff is isolable against a known-good baseline with nothing carried in from elsewhere:

```
ce2204524a09bc5ac747b0db3050cdf0bc8e55b832b04c55249f0767d15de8b4  scripts/wwcr_whirlwind.gd
970658bdd49bb1f8ad8c464a3ca9af7d9adf77c198044fb4809d27cae7f35ec9  scripts/wwcr_stage.gd
```

### Commits, granular

| commit | treatment |
|---|---|
| `fb2a697` | T-1 recipient state response (stage-side) |
| `9124bde` | T-3 two-surface split **+ TRAIL-BOUNDED amendment, same commit** |
| `03e6d0c` | T-4 lifecycle phases + seeded gust stream (+ the shed pool) |
| `7300332` | T-2 attached wind-residue persistence |
| `7fb437a` | T-5 cross-section variation |
| `0821b6a` | T-6 environment aftermath |

### ⚑ RATIFIED-CAMERA CODE PATHS: UNTOUCHED, VERIFIED NOT ASSERTED

`git diff f0e8d6d..HEAD -- scripts/wwcr_stage.gd` filtered for `PL_` / `CAM_` / `_playerlock` / `_aim_camera`
/ `_pl_` returns **exactly one line**, and it is a **read**, not a write:

```gdscript
"flinch_shove_px_worst_case": FLINCH_SHOVE_M * 82.0 * sin(deg_to_rad(PL_PITCH_DEG)),
```

It consumes the ratified pitch to report the worst-case projection of the T-1 shove in pixels. No camera
constant, basis, offset, pin or aim function is modified anywhere in the wave.

### PIN VERIFICATION — 12 decimals, verbatim from the B-1 render

```
[wwcr] PL-PIN unscaled offset (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       vs pl_audit.json (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       — |delta| 0.000000000000 m, z_player delta 0.000000000000 m, tol 0.000010000000 m — MATCH
```

Stand-off at k = 0.665: **23.1627407073975 m** — the ratified figure, re-verified after 1,846 lines of change.

---

## 3. ⚑ ONE FORCED RE-ORDERING: T-3 LANDED BEFORE T-2

The dispatch says numbered order. The build conditions say otherwise, and they win because they are narrower:

1. DRIFT-CRITIC § 5 build condition: *"the amendment ships in the same commit as the two-surface split"*.
2. The amendment's allow-list contains `RecipientResidue`, which is **T-2's** family.
3. Therefore a T-2 that landed first would have to add a third tinted family **under the old
   `_tinted_nodes.size() == 2` assert** — i.e. bypass the very guard the amendment exists to preserve.

The remaining order is unchanged: T-1 → T-3 → T-4 → T-2 → T-5 → T-6. The irreducible core (T-1 → T-3 → T-4)
landed first regardless, so the cut line was never at risk.

---

## 4. ⚑ N-VERIFICATION — N = 3, AND MOB0 IS A FREE NEGATIVE CONTROL

Measured from the `contact` signal, emitted in the run log as `[wwcr] LAP2_N`:

| mob | position (x, z) | contacts | first stage frame | stage frames |
|---|---|---|---|---|
| Mob0 | (2.05, 0.55) | **0** | — | — |
| Mob1 | (−1.70, 1.55) | 5 | 78 | 78, 102, 126, 150, 180 |
| Mob2 | (0.35, −2.35) | 5 | 65 | 65, 90, 114, 138, 162 |
| Mob3 | (−2.55, −1.35) | 5 | 65 | 65, 90, 114, 138, 162 |

**`N_mobs_in_scene` = 4 · `N_contacted` = 3 · total contacts = 15.**
So the spec's mob criteria read **all 3** (T-1) and **≥ 2** (T-2).

**Why Mob0 is never struck — geometric, not accidental.** `_tick_contacts` fires a pass when
`fmod(_spin, PI)` wraps, so the bearing at *every* pass is within one stepped frame of ±Z; one frame at
900 °/s is 0.2618 rad = **15.0°**, so the pass bearing lives in a ±15° cone about Z and nowhere else. The
admission test is `dot >= 0.55`, a **56.6°** half-angle. Mob0 sits **75.0°** off +Z and 105.0° off −Z; its best
case is 75.0 − 15.0 = **60.0°**, missing the gate by **3.4°** on every revolution for the whole channel.

**Not fixed, deliberately.** T-4 states it: *"Contact ticks stay phase-locked. Blade passes are physical truth;
do not randomise hits."* Widening the cone or sub-stepping the pass detection changes which bodies the weapon
reaches — a combat-geometry change wearing a VFX lap's clothes.

**And it is worth more than a fourth flinch.** Mob0 is an **in-frame negative control**: same lights, same
pinned clock, same effect region, same venue — and it must show **zero** flinch and **zero** residue. Any T-1 or
T-2 signal measured on Mob0 is instrument error, global frame motion, or bleed from a neighbour, and is
detectable as such *without* the vfx-off control. The control proves the effect moved something; Mob0 proves it
did not move everything.

**⚑ ONE TENSION IN T-1 THAT IS GALADRIEL'S TO MEASURE AND GANDALF'S TO ADJUDICATE, NOT MINE TO RESOLVE.** The
spec sets the refractory at ~0.35 s *and* asks the mob to be back within 2 px of rest **by 1.0 s after its first
contact**. At one flinch per 0.4 s revolution a mob is re-struck ~5 times, so at t+1.0 s it is mid-flinch from a
later strike. Both legs cannot hold simultaneously while the refractory is 0.35 s. What I built satisfies the
return leg for the **isolated impulse** — analytically `x(1.0 s) = 0.000574 m = 0.047 px`, a 40× margin — and
the running clip cannot exhibit it. Flagged rather than silently retuned.

---

## 5. ⚑ REFUSAL — T-4's ONSET ACCENT (mechanism refused, requirement built)

**Refused as written.** The spec asks for *"one-shot pale **ring-pop** at `SWEEP_Y`, expanding ~0.6·`R_ENGAGE`
→ ~1.05·`R_ENGAGE` over 0.12–0.18 s, apex colour, ADD."*

That is a **tinted continuous surface at 1.05 · R_ENGAGE**. The clause T-3 restates two sections earlier *in the
same document* reads: *no tinted surface may be CONTINUOUS **or** PERSISTENT at or beyond `R_ENGAGE`* — not
"and". A brief ring is still a ring. It is also **not on the five-name allow-list**, and a sixth name invented
by the builder to admit his own surface is exactly the dissolution gandalf pre-registered as the veto condition
on the amendment. And of all possible shapes, *a lit tinted ring around the caster at the engagement radius* is
the literal Eye-of-Reckoning failure `wwcr_whirlwind.gd`'s own header says the absence of **is the design**.

**Built instead: the perceptual requirement.** The spec's player-facing sentence is *"the spin starts with a pale
ring-snap at the caster's waist height."* A one-shot burst of **32 discrete quanta** thrown outward across the
same radii over the same ~0.15 s reads as a ring-snap at 82 px/m while being discrete, brief, and already
allow-listed as `ShedQuantum`. Criterion T-4(a) is untouched by the substitution — it measures luminous **area**
over 6–12 frames, a statement about the burst, not about whether the burst is one mesh or thirty-two.

**Open to gandalf.** If the conductor rules the continuous ring in, it is a sixth allow-list entry **plus** a
re-reading of the clause — his call to make explicitly, not mine to make silently by building it.

---

## 6. PER-TREATMENT STATUS

All acceptance criteria are left **measurable**; the numbers below are **my own instruments** (segmentation
stated) plus eyeball notes. galadriel measures.

### T-1 · Recipient state response — **LANDED** (`fb2a697`, `wwcr_stage.gd`)
Critically damped impulse on the mob root: shove along the contact bearing + lean about the perpendicular
horizontal axis, both `_w`-scaled as 4a is, 0.35 s refractory. `wwcr_whirlwind.gd` **byte-unchanged** by T-1 —
the signal is the seam and the recipient owns its own response.

⚑ **A defect measurement caught that arithmetic had missed.** `v0 = x_peak·w0·e` is the **continuous** impulse
inversion; `_tick_flinch` is semi-implicit Euler at `w0·dt = 0.15`, whose discrete peak is **28 % lower**.
Measured 0.157 m against an authored 0.19 m. That under-delivers a perceptual criterion by a whisker (8.96 px
against an ≥ 8 px bar) for a reason no frame could show. The constant is a magnitude **Matt judges by eye**, so
it stays the peak and the **gain is measured off the very integrator that will run the impulse** — v0 = 1, step,
take the peak, divide. Gain `0.029540483`; v0 = 33.85 per metre against the continuous 24.46.

- Authored peak: **0.19 m** shove / **9.0°** lean. Measured max (incl. impulse stacking): **0.217 m / 10.29°**.
- Worst-case projection of the authored peak (motion along the view azimuth, foreshortened by
  sin 52.9535° = 0.7976): **12.44 px** against the ≥ 8 px bar; ≈ 12 frames above the bar against ≥ 4.
- **Eyeball:** the ring of skeletons now lurches in sequence as the arc comes round. Not rag-dolled, not sliding.
  Falsifier pre-registered per spec; Matt's eye at the lap gate.

### T-3 · Luminance-dominant apex, deep tail, saturated body — **LANDED** (`9124bde`)
Two co-located surfaces from one `_hist`, plus the guard amendment, in **one commit**.

- **Core** `TrailRibbonCore`: ADD, **PER_PIXEL + `EMISSION_OP_MULTIPLY`**. ⚑ In `SHADING_MODE_UNSHADED` Godot
  outputs `vec4(albedo, alpha)` and **drops emission entirely** — the mint's `emission_energy_multiplier = 2.0`
  on this material **had never rendered**, a second `mi.scale`. `EMISSION_OP_MULTIPLY` keeps the per-vertex ramp
  on albedo while letting energy reach the HDR range the FILMIC tonemap and glow pass respond to.
- **Body** `TrailRibbonBody`: MIX, **UNSHADED precisely because unshaded cannot emit** — it is shadowed air.
- **T-3b** `ArcLight`: one `OmniLight3D` on the newest history sample, range 2.6 m, energy 2.2·`_w`·gust,
  shadows off (C-1).
- **Ramp derived, not pasted.** The spec's three triples are **not at the wind element's hue** — they sit ~19°
  cyan-ward, the tail a further ~31°. So the ramp is (S,V) pairs **plus per-band hue offsets measured out of
  gandalf's own table**, applied to whatever hue the element hands in. Wind reproduces the table to 4 decimals
  (`apex (0.9200,1.0000,0.9800)` · `body (0.2400,0.9000,0.7400)` · `tail (0.0500,0.2600,0.3400)` at V = 0.34);
  fire/water/earth get the *relationship* rather than wind's colours. Holding hue rigid — my first build —
  rendered a visibly greener body and was obeying the sentence while disobeying the artifact.

⚑ **TWO GEOMETRY/VALUE DEFECTS THE CRITERIA WOULD HAVE FAILED ON SILENTLY:**

1. **The taper collapsed the tail to zero width.** `1 − pow(age, 0.75)` makes the width fraction `age^0.75`,
   which is **0 at the oldest sample**. Correct for a one-surface fade; fatal for a *visible* dark band. Cost two
   rounds of tuning constants that were never the problem — a 2× crop answered it in one glance and should have
   been the first call, not the fourth. Taper now has a floor (`TAPER_MIN_FRAC = 0.45`).
2. ⚑ **THE SPEC'S "DARK" TAIL IS BRIGHTER THAN THE FLOOR IT IS SUPPOSED TO SHADOW.**
   `Color(0.05, 0.26, 0.34)` has Rec.709 luma **0.2213**; the Cathedral's measured non-effect scene median at
   this pin is **0.178**. Under MIX it *lightens* the tile — the exact inverse of the treatment's stated purpose,
   and criterion (b) cannot exceed ~2.8 with it no matter what the apex does. **It stayed invisible for three
   passes because I masked the effect region with `|ΔL|`.** Signed, the frame said it in one line: **four
   pixels** in 1920×1080 got darker. A surface whose entire job is to put a value *below* the floor's into the
   frame was putting nothing below the floor at all, and an absolute-value instrument reported that as a working
   effect. *The check ran, and the check was not the check.* → **V 0.34 → 0.16** (luma 0.104, 0.58× the floor);
   hue and saturation are the spec's, untouched. Licensed by the spec's own *"drax may tune within the
   criterion."* **VENUE-COUPLED** — re-measure, do not re-use, if the venue moves.

**My instrument** (effect geometry = `|ΔL| > 0.10` vs the control; scene = `|ΔL| ≤ 0.004`), at three marks:

| criterion | bar | mine |
|---|---|---|
| (a) brightest 1 % ÷ annular scene median | ≥ 2.20 | **3.4 – 5.2** ✅ |
| (b) P95 ÷ P20 in region | ≥ 4.00 | **2.2 – 3.5** ⚠ short on my segmentation |
| (c) mid-band HSV S | ≥ 0.55 | **0.38 – 0.42** ⚠ short on my segmentation |
| (e) cast-light lift on non-effect surface | ≥ 8 % | **11 – 13 %** ✅ |
| (d) apex on the leading edge | ≥ 80 % frames | by construction (apex = newest sample) |

⚠ **On (b) and (c) I stopped rather than kept tuning, and the reason is a trade I am not authorised to make
unilaterally.** The obvious lever is body alpha; it is already at 0.85, and pushing toward opacity would start
occluding the mobs the ribbon crosses — trading a measured criterion in this spec against the **occlusion gate**
this row must also pass ("localized hit effects preserve the rotating silhouette without obscuring nearby
enemies"). My region mask also includes cast-lit floor, which is inherently unsaturated and drags both numbers
down; galadriel's segmentation may differ materially. T-2 and T-5 quanta (soft-edged, many) also land *after*
these measurements and will pull P20 down further.

- **Eyeball:** the apex is plainly the brightest thing in the room, and the ribbon now deepens through teal into
  a tail that falls into shadow. The pastel decal is gone.

### T-4 · Lifecycle phases + arrhythmic gust texture — **LANDED** (`03e6d0c`)
Onset burst at RISING start (see the § 5 refusal); seeded Poisson gust stream through sustain; FALLING breakup
where the history window contracts with `_w` and **every dropped sample becomes a drifting quantum** rather than
vanishing — which is why criterion (c)'s "no single frame-to-frame drop > 35 %" is reachable at all.

- **Dedicated seeded `RandomNumberGenerator`, seed `20260825`**, as ordered. The global sequence is untouched
  (`_fire_scuff`'s documented no-op `randf()` still holds its position), so this clip's reproducibility is not
  hostage to any future line anywhere that draws once.
- **CV = 1.0 by construction** (exponential inter-arrivals) — a property of the distribution, not a number tuned
  toward. Measured realised CV **0.979**, band [0.45, 1.15]. FF-08 trip-flag (CV < 0.25) does not fire, with
  0.73 of margin.
- One surge variable drives **both** core emission and the arc light, so a gust cannot brighten the ribbon in a
  room that did not notice.

⚑ **THE RATE LOOKED BROKEN AND WAS NOT — and the check is the finding.** Realised 17.6 Hz against a 14 Hz
*ceiling* is impossible for correct thinning, so I ran three more seeds **before touching it**:

| seed | realised rate | CV |
|---|---|---|
| 20260825 | 17.6 Hz | 0.979 |
| 11111 | 14.1 Hz | 0.949 |
| 777777 | 12.9 Hz | 0.998 |
| 424242 | 14.9 Hz | 0.976 |

Expected 12.9 Hz. **n ≈ 35 sampling noise, not a defect.** Four renders, and they stopped me "fixing" a correct
process. Two *real* defects did fall out of looking: `lerpf(8,14,_w) * _w` double-scaled the rate to 5.5 Hz at
half weight; and my interval instrument differenced `_clock` — at 14 Hz against a 1/60 s step two gusts
regularly land in one frame and recorded **dt = 0**. *An instrument quantised coarser than the thing it measures
does not report noise, it reports a different process.*

- **The onset's first build rendered as a DOTTED CIRCLE** — ±0.05 rad jitter against 0.224 rad spacing, one
  size, hard pop-off. Mechanically regular, one step from the "UI-like annotation" X-1 dim 10 convicted the whole
  effect of. Now ±0.09 rad, three size classes, radius/Y/speed/life jitter, and a fade.
- **The fade is verified, not assumed.** `mi.scale` is the known no-op under billboarding (W1 F-2) and a
  per-instance material would be 88 copies, so the fade rides `GeometryInstance3D.transparency`. Measured across
  the burst: mean lit-pixel luminance **0.485 → 0.448 → 0.400 → 0.343**, area 41k → 18k → 5k px. It renders. A
  third imagined line in this file would have been a pattern.
- **Eyeball:** the spin now *starts*, *holds with texture*, and *breaks up*. Four distinct regimes are visible.

### T-2 · Attached wind-residue persistence — **LANDED** (`7300332`)
4–7 pale quanta per flinch, staggered in over 0.15 s, rising 0.30–0.60 m on a tangential curl whose sign comes
from the bearing derivative (4a's trick — it cannot disagree with the rotation), guttering out on lifetimes
spread across **0.70–1.40 s** so they do not extinguish together.

⚑ **ONE DEVIATION FROM THE SPEC'S MECHANISM, AND IT PROTECTS A GATE TWO SEAMS AWAY.** The spec says *"parented
to the mob, so it tracks if T-1 moves it."* **Tracking is right and is built. Reparenting is not:**
`wwcr_stage.gd` registers the C-8 census **by ancestry** — *"everything under this root is AUTHORED, everything
else in the viewport is INHERITED"* — so a quantum moved under a mob would leave the authored subtree and be
enumerated as an **INHERITED emitter**, which is a **HALT condition on galadriel's gate**, halting on a node this
file created. Each quantum therefore carries a **host reference** and recomputes `host.origin + offset + rise`
every frame. It follows the T-1 shove exactly as reparenting would, and the census still tells the truth.

- **C-2 / R-20e as a hard bound.** `RESIDUE_LIFE_MAX = 1.40 s` is **asserted** in `_trail_bounded_check`, with
  the assert message saying *why* rather than what. Last possible spawn is the last contact at t = 3.12 s
  (contacts cannot fire below `_w` = 0.35), so extinction is 3.12 + 0.15 + 1.40 = **4.67 s** against effect-end
  3.40 s — **1.27 s of margin** on the "gone by 2.0 s after effect end" bound, and a later edit cannot spend that
  margin without the guard failing.
- Burst refractory 0.35 s **mirrors the stage's T-1 refractory deliberately**: separate mechanisms in separate
  files, but on different cadences a mob would gutter residue on a beat its body did not answer.
- **Measured:** 46 quanta alive at peak; residue carried by **3 hosts simultaneously** against a criterion of
  ≥ N−1 = **2**.
- **Eyeball:** the ring of skeletons reads as *recently hit* rather than as scenery.

### T-5 · Shedding + cross-section variation — **LANDED** (`7fb437a`; shedding half in `03e6d0c`)
⚑ **The arithmetic *is* the treatment here, and the obvious implementation is a trap.** One revolution is TAU
radians of `_spin`, so `sin(_spin·f)` repeats **every revolution iff f is an integer**. An f of 1, 2 or 3 — what
"add a low-frequency noise term" most naturally becomes — gives a profile beautifully varied *within* a
revolution and byte-identical *between* revolutions: **the exact defect X-2 measured (cf_100 ≡ cf_115),
faithfully reproduced by the line written to fix it.**

Frequencies are non-integer and mutually incommensurate: f₁ = 0.7333 (phase advance 4.607 rad/rev),
f₂ = 1.6180 (3.883 rad/rev mod TAU). Both below 2 — a high-frequency term would ripple the ribbon like a flag.

**Criterion (b) is derived, and the derivation ships as a computed selfcheck key rather than a comment:** per
term the revolution-over-revolution difference is a sinusoid of amplitude 2|sin(φ/2)|; incommensurate terms add
in quadrature; dividing by the **mean width fraction** makes it comparable to the criterion's percentage.
→ **30.83 % RMS against an 8 % bar.** Stronger than measuring two sampled revolutions: it holds for *every*
consecutive pair, and if anyone later rounds a frequency to an integer the number collapses toward zero and says
so in the manifest.

- Inner fraction is **stored per sample**, not recomputed at draw time — the width a sample had is a fact about
  when the blade was *there*; recomputing from the current `_spin` would make the whole arc breathe in unison.
- `TRAIL_SAMPLES` and the open-arc guard are **byte-untouched**: width varies, angular span does not.
- Size spread rides **five distinct `QuadMesh.size` classes** (area ratio 21:1) — `mi.scale` is a no-op under
  `BILLBOARD_ENABLED` (W1 F-2), so a pool of one size with a runtime scale write would render as one size and
  criterion (a)'s IQR/median ≥ 0.5 would be structurally unreachable while the code looked like it varied.
- **Measured:** inner-fraction band [0.727, 0.873] = **2.17:1** widest-to-narrowest; **60 shed quanta alive** at
  peak against a ≥ 6 connected-component floor.

### T-6 · Environment aftermath — **LANDED** (`0821b6a`)
Neutral, unlit, non-emissive MIX marks accumulating on the tile at the engagement radius, four per blade pass,
**no lifetime expiry**. Wind-native translation: **abrasion, not burning**.

⚑ **Guard clause read rather than waved at.** This is the one family that is **persistent at `R_ENGAGE`**. The
clause binds **tinted** surfaces. The scour is neutral (`SCUFF_COLOR` darkened — hue byte-untouched, R-9 intact,
and *value* is exactly what a scour is), unlit, non-emissive, and **never touched by `set_element`**, so it never
enters `_tinted_nodes` and a fire whirlwind scours the same grey. Admissible for precisely the reason the clause
is about tint: an untinted floor mark is a **consequence**, and consequences at the outer radius are what this
archetype is supposed to spend it on. A tinted one would be a decal, and a decal is Eye of Reckoning. It is also
the one family that deliberately breaks the mint's *"brief"* — stated in the file rather than absorbed, because
**a scour that fades is a scour that did not happen**.

⚑ **THE FIRST BUILD PASSED THE AREA LEG AND FAILED THE DEPTH LEG — AND I HAD REASONED MY WAY PAST EXACTLY
THAT.** I wrote *"passes ACCUMULATE"* in the design comment and left it there. They do (MIX over MIX compounds as
1−(1−a)ⁿ) — but at `VALUE_MUL` 0.22 with 3 marks per pass the average tile was covered about **twice**, and two
covers of a mark only 0.046 luma below the tile is **3.5/255** against a 6/255 bar. **5,319 px marked against a
2,500 bar, and the treatment still failed.** The mechanism was right; the *depth* was never solved for.

Solved: `dL = (1−(1−a)ⁿ)·(floor − mark)` at the n = 2 the geometry actually delivers ⇒ mark luma ≤ 0.093, so
`VALUE_MUL` 0.22 → **0.12** (luma 0.072, 0.40× the measured tile), alpha 0.12–0.18, 4 marks/pass, arc spread
0.30 → 0.22 rad so adjacent passes **overlap** instead of tiling. Second finding on the way: every other family
uses `_soft_radial_texture()`, whose `pow(a, 2.1)` spends most of a quad on a dim rim — right for a spark, wrong
for a scour both perceptually (a scrubbed patch has an edge) *and* metrically (rim pixels count as "changed"
while contributing nothing to the mean). T-6 gets its own **plateau falloff**.

**Measured** (ON vs control at identical pose — cleaner than pre/post, since the caster translates):

| mark | darkened px (bar 2,500) | mean \|ΔL\| (bar 6.0/255) |
|---|---|---|
| `00-pre` | **0** — nothing before the effect | — |
| `06-sustain-moving` | 11,924 | **13.2/255** |
| `09-off` (clip end) | **19,143** | **11.2/255** |

Monotonic non-decreasing during sustain falls out of never expiring rather than being checked for. Marks are laid
in **world space**, so the 3.5 m/s translation from t = 2.20 leaves the **path** of the fight rather than a circle
around wherever the caster stopped.

- Like T-3's tail, *"slightly darker than tile"* was authored without the venue's measured floor luminance in
  hand. **VENUE-COUPLED.**
- **Eyeball:** a faint dark swath along the sweep path. Scoured stone, not a smear.

### B-1 · Build requirement — **LANDED** (`95aa77c`, `02e8b37`; artifacts § 8)

---

## 7. THE TRAIL-BOUNDED AMENDMENT, AS LANDED

Shipped in `9124bde`, **the same commit as the two-surface split**, per the spec's "together or neither" line and
DRIFT-CRITIC's build condition.

`_tinted_nodes.size() == 2` is replaced by `_trail_bounded_check()`, which enforces the clause the count was only
ever a proxy for — ***no tinted surface may be CONTINUOUS or PERSISTENT at or beyond `R_ENGAGE`*** — in three
legs, each failing loudly:

1. **Membership** — every tinted family must be on the five-name allow-list, each entry carrying a one-line
   justification in code. **A ceiling, not an equality**: families land across several commits, and a guard that
   fails on a treatment not yet built is a guard that gets commented out.
2. **Continuity** — the two continuous families are blade-generated, so `R_TRAIL = 2.3598 m` is asserted strictly
   inside `R_ENGAGE = 3.5150 m`.
3. **Briefness** — every discrete tinted family's lifetime is asserted under a stated 1.6 s ceiling, so "brief"
   is a **number** and not an adjective. (`ContactSpark` 0.12 s · `ShedQuantum` ≤ 0.90 s · `RecipientResidue`
   ≤ 1.40 s.)

Named **non-members**, so each omission is a decision on the record rather than an oversight: `ScuffPuff` and
`FloorScour` (neutral — R-9 intact), and `ArcLight` / the pooled contact lights (**lights are not surfaces**;
both ride inside `R_TRAIL`).

⚑ **`tinted_count_is_2` is REMOVED from `selfcheck()`, not set to `false`.** The W2 B-arm manifest recorded that
key as the receipt for R-9's assert passing; keeping a key whose property is now *deliberately* untrue would put
a false receipt in the next manifest. Its replacements state what they check:
`trail_bounded_allow_list` · `trail_bounded_clause` · `tinted_all_on_allow_list` ·
`tinted_continuous_inside_r_engage` · `tinted_discrete_life_ceil_s`.

**Runtime receipt from the B-1 render:**
`tinted_surfaces: ["TrailRibbonCore","TrailRibbonBody","ContactSpark","RecipientResidue","ShedQuantum"]` ·
`tinted_all_on_allow_list: true` · `tinted_continuous_inside_r_engage: true`.

---

## 8. B-1 — ARTIFACTS, HASHES, DISK RECEIPT

**Full reproduction manifest:** `~/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-lap2/REPRODUCTION_MANIFEST.md`
⚑ It lives **beside the mp4s it describes**, not in `$TMP` — R-19c / W2b F-3 in force.

### The window

The effect reaches **IDLE** at `T_RELEASE + SPIN_DOWN_S = 2.60 + 0.80 = 3.40 s`. The previous window ended at
**3.70 s** — 0.30 s of aftermath, which is why T-4(c) and T-6 could not be measured at all: they are measured
*in* the aftermath and the window had none. `SEQ_TO = 5.00` gives **1.60 s** past IDLE against the spec's ≥ 1.5 s.

⚑ **`SEQ_TO` is in the INVOCATION, not the source.** `_seq_to` stays 3.70 in `wwcr_stage.gd`. The spec frames
B-1 as *"a re-invocation, not a re-authoring"*, and moving the default would silently move the reproduction
baseline of every corpus captured before this one.

### Artifacts

| arm | path | bytes | sha256 |
|---|---|---|---|
| **treatment ON** | `~/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-lap2/plk06650_cathedral_fxon.mp4` | 3,561,680 | `cc815bcf4efdefa838aec24c3e5ace02120bf7061b7bcfbff332c00cd5158138` |
| **control** (`set_vfx_visible(false)`) | `~/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-lap2/plk06650_cathedral_fxctl.mp4` | 3,046,927 | `fd1b9f653fcf4cd32a3fef264bb3cd0067f51e41e4f88f242dadc9027f810252` |

Both `ffprobe`-verified: **h264 · yuv420p · 1920 × 1080 · 60/1 fps · 288 frames · 4.800 s**.
`FRAME_CENSUS rendered=576 delivered=576` — no shortfall, no stale frame. **Identical window, frame-for-frame.**

The control is rendered **with** the arm, never borrowed: same pose, same rotation, same pinned animation clock,
VFX layers hidden. Diffing against "no whirlwind at all" would measure the caster's pose — which is exactly how
the occlusion gate's original 7.65 % false positive arose.

### Invocation (literal)

```bash
cd ~/Games/reincarnated-godot && git checkout 0821b6a
cp scripts/run_wwcr_stage.sh /tmp/frozen_run_wwcr_lap2.sh     # sha256 94329832…0ea3ed
env REPO="$PWD" ARMS=gate CAPTURE=seq CAM=player_lock PLK=0.665 STAGE=cathedral \
    SEQ_FROM=0.20 SEQ_TO=5.00 SEQ_EVERY=1 SEQ_FPS=60 \
    bash /tmp/frozen_run_wwcr_lap2.sh 2026-08-25-lap2
```

### ⚑ MP4-FRAME INDICES FOR EVERY CONTACT (galadriel cuts her ROI windows from these)

MP4 frame 0 is the first *captured* frame (`t ≥ 0.20 s`), **13 frames after the stage's frame 0**. Handing over a
stage index alone would hand over an off-by-thirteen that looks exactly like a treatment failing its 0.15 s
criterion window — which is why the stage emits both.

| mob | contacts | **MP4 frames** | stage frames |
|---|---|---|---|
| Mob0 | **0** (negative control) | — | — |
| Mob1 | 5 | **65, 89, 113, 137, 167** | 78, 102, 126, 150, 180 |
| Mob2 | 5 | **52, 77, 101, 125, 149** | 65, 90, 114, 138, 162 |
| Mob3 | 5 | **52, 77, 101, 125, 149** | 65, 90, 114, 138, 162 |

### Runtime receipts from the ON arm's FINAL `selfcheck()`

| key | value |
|---|---|
| `tinted_surfaces` | `["TrailRibbonCore","TrailRibbonBody","ContactSpark","RecipientResidue","ShedQuantum"]` |
| `tinted_all_on_allow_list` / `tinted_continuous_inside_r_engage` | **`true` / `true`** |
| `gust_interval_cv_measured` | **0.706** (band [0.45, 1.15] → `gust_cv_in_band: true`) |
| `ff08_trip_flag_would_fire` | **`false`** (trips at CV < 0.25) |
| `xsec_rev_over_rev_rms_pct_predicted` | **30.83 %** against an 8 % bar |
| `xsec_width_ratio_measured` | **2.169 : 1** |
| `shed_alive_max_measured` | **60** (≥ 6 component floor) |
| `residue_hosts_simultaneous_max_measured` | **3** (criterion ≥ N−1 = 2) |
| `residue_life_under_ceiling` | **`true`** |
| `scour_laid_measured` / `scour_expires` | **36** / **`false`** |
| `measured_clears_lower_body` / `arc_is_open` | **`true` / `true`** — the mint's disjoint-band inequality and open-arc guard both still hold |

### DISK RECEIPT — encode-then-prune (R-18c), count-gated

Both prunes fired **only after a COUNT-GATED verification**: decoded packets counted off the stream and compared
against the PNGs that went in — never an existence check, because `ffmpeg` can exit 0 having written a truncated
stream.

| prefix | gate | reclaimed (`$OUT` + `$USERDIR`) |
|---|---|---|
| `plk06650_cathedral_fxctl` | **288 == 288** VERIFIED | 0.742 + 0.742 GiB |
| `plk06650_cathedral_fxon` | **288 == 288** VERIFIED | 0.744 + 0.744 GiB |

**Total reclaimed 2.972 GiB. Free disk 47 GiB at wave open and 47 GiB at wave close — net zero.**

### What is committed and what is not

`REPRODUCTION_MANIFEST.md`, `prune_receipts.txt` and `render_receipts.txt` (1.3 MB) are **committed**. The mp4s
are gitignored (Synty IP, pre-existing rule). ⚑ The raw `render.txt` is **30 MB, of which > 99 % is the per-frame
enumeration of 605 PRE-EXISTING Cathedral/FightSurface emissive meshes** — inherited geometry, not authored by
this effect, byte-unchanged by this wave. It is excluded by a `.gitignore` rule **that carries its own reason and
names its replacement**; the extract states the elision counts in its own footer, so a filtered log cannot later
be mistaken for a complete one.

---

## 9. REFUSALS, DEVIATIONS AND OPEN ITEMS — consolidated for the conductor

| # | item | kind | disposition |
|---|---|---|---|
| 1 | T-4 onset ring as a **continuous tinted surface at 1.05·R_ENGAGE** | **REFUSAL** (mechanism) | Requirement built as an allow-listed discrete burst. gandalf's call if he wants the ring: sixth allow-list entry **plus** a re-reading of the clause. |
| 2 | T-3 **before** T-2 | forced re-order | Compelled by the build conditions themselves (§ 3), not by preference. |
| 3 | T-3 tail **V 0.34 → 0.16** | spec override, measured | Spec's tail luma 0.2213 vs measured floor 0.178 — it *lightens*. **VENUE-COUPLED.** Matt's eye at the lap gate; reverting is one number. |
| 4 | T-6 **`VALUE_MUL` 0.22 → 0.12** ("slightly darker than tile") | spec override, measured | Depth criterion is the binding instrument. **VENUE-COUPLED.** |
| 5 | T-3 ramp carries **per-band hue offsets** (+18.91° / +19.37° / +50.47°) | derivation, not deviation | Measured out of gandalf's own table; wind reproduces it to 4 decimals. Set all three to zero for the rigid-hue reading. |
| 6 | T-2 residue **host-referenced, not reparented** | mechanism deviation | Protects the C-8 census ancestry and galadriel's HALT condition. Tracking behaviour is identical. |
| 7 | T-1 "back to rest by 1.0 s" **vs** 0.35 s refractory | spec-internal tension | Cannot both hold. Isolated-impulse leg satisfied analytically (0.047 px). galadriel measures, gandalf adjudicates. |
| 8 | **N = 3**, Mob0 never contacted (misses the pass cone by 3.4°) | measured fact | Not fixed — T-4 forbids touching contact ticks. Repurposed as an in-frame negative control. |
| 9 | Criteria T-3(b) and T-3(c) short **on my own instrument** | open, for galadriel | Did not push body alpha past 0.85: that trades a measured criterion against the occlusion gate. |
| 10 | `_seq_to` **default left at 3.70** | deliberate | Spec frames B-1 as a re-invocation, not a re-authoring; changing the default would move every prior corpus's reproduction baseline. The extended window is in the invocation and in the manifest. |

**Nothing PARKED. Nothing part-landed. T-3's split and its guard amendment shipped together.**
