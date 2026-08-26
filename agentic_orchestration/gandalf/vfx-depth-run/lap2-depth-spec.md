# Lap-2 depth spec — Whirlwind (wind), Cathedral B-arm

**Author:** gandalf (SPEC-AUTHOR, named sub-agent) · **Date:** 2026-08-25 · **Charter:** `notes/2026-08-25-vfx-depth-run-charter.md` R-20 (SPEC unblocked) · § 4 loop stage 4.
**Builder:** drax · **Measurer:** galadriel · **Target file:** `~/Games/reincarnated-godot/scripts/wwcr_whirlwind.gd` (+ `wwcr_stage.gd` for recipient response) · **Venue:** Cathedral, `run_wwcr_stage.sh --capture=seq`, encode-then-prune law (R-18c).
**⛔ Informed-side. Consumes audit-key material (registry family IDs, lap-1 pass logs). NEVER visible to a blind seat.**

---

## § 0 — Intent

The owner's question at the judging camera is: **does it read as a powerful physical event with consequences?** Right now it does not. Both blind passes, independently, converged on the same sentence: the render implements the *sweep* and omits the *consequence* — "a UI-like annotation: one flat teal geometric sector rotating regularly around a rooted caster, affecting nothing, leaving nothing" (X-1 dim 10). This spec buys consequence first, palette second, lifecycle third, in the union order of the two ranked lists.

**Binding constraints on every line below:** Tier-1 identity law (the reference is fire; we are wind — principles transfer, content does not) · charter R-20e (the reference's ignition cast is *unobservable*; FF-09/FF-10 enter at modest wind magnitude, never as "whirlwind ignites per-victim burning") · N-2 standing law (every acceptance criterion is stated at the judging camera in perceptual terms) · W1 F-2 (`mi.scale` is a no-op under `BILLBOARD_ENABLED`; size variation rides count/emission/geometry) · charter R-17f (no bar built on registry F4/F5 matrix columns).

---

## § 1 — Treatments, in priority order

### T-1 · Recipient state response — *the statues become bodies*
**Families:** FF-09. **Rank:** X-1 #1, X-2 #1 (both passes, independently).

**What the player sees.** Each skeleton the blade sweeps past is knocked — it lurches away from the caster, its stance breaks for a beat, and it settles back; the four mobs do this at different moments as the arc comes round to each of them.

**Implementation guidance.** `wwcr_whirlwind.gd` already emits `contact(target, point)` and `wwcr_stage.gd` already connects it (`wwcr_stage.gd:611`). Land the response in the **stage**, not the effect: replace the counting lambda with a handler that pushes the struck mob into a short scripted flinch — a transform-level impulse (lean away from the caster on the contact bearing + a small positional shove, both critically damped back to rest), NOT an animation import. Magnitude ~0.12–0.20 m of shove and ~6–10° of lean at full channel weight, weight-scaled by `_w` as 4a is. Per-mob refractory window (~0.35 s) so a mob struck twice in one revolution does not double-impulse into a jitter.

**Wind-native, C-2 compliant:** this is a *knock-flinch*, not a death, not a burn, not a persistent state. Nobody falls. Magnitude is explicitly **"judged by Matt's eye at the lap gate"** — the falsifier, pre-registered: if the mobs read as *rag-dolled* or *sliding on ice*, the shove is too high; if they still read as statues, too low.

**Acceptance criterion (judging camera).** For each mob the blade contacts — **the blind passes counted five skeletons in scene; drax verifies the actual in-reach contact count N at build time from the `contact` signal, and N parameterises every mob criterion in this spec** — within 0.15 s of its first contact frame: silhouette centroid displaces **≥ 8 px** and/or the silhouette principal axis tilts **≥ 4°**, sustained **≥ 4 frames**, returning to within **2 px** of its rest pose by **1.0 s**. All N contacted mobs respond at least once inside the sustain window. Baseline for comparison: the mob ROIs in the current B-arm are pixel-identical across contact (X-2 dim 8).

---

### T-2 · Attached wind-residue persistence — *the effect leaves the caster*
**Families:** FF-10. **Rank:** X-2 #1 ("the reference effect is *on the victims*, the render's is only *on the caster*"), X-1 #1 adjacent.

**What the player sees.** A struck skeleton keeps a curl of disturbed air on it after the arc has gone — a brief shimmer of pale, fast quanta spiralling up off its shoulders and guttering out about a second later. For a moment three of the four carry it at once, so the ring of them reads as *recently hit*, not as scenery.

**Implementation guidance.** On `contact`, attach a small short-lived quantum emitter to the struck mob's node (parented to the mob, so it tracks if T-1 moves it). 4–7 quanta, staggered spawn, each rising 0.3–0.6 m with a tangential curl inheriting the blade bearing's sign (same derivative trick 4a uses — the sign cannot disagree with the rotation). Lifetime **0.7–1.4 s**, spread across the quanta so they do not extinguish together. Reuse `_soft_radial_texture()`; ADD blend; the apex colour of § 2.

**C-2 magnitude discipline.** This is *air still moving where a body was struck*, not a status effect. It must be **gone by 2.0 s after the effect ends** — nothing in this spec commits the skill to persistent per-victim state, because the reference clip's ignition cast is unobservable and the identity question is not ours to settle. Magnitude judged by Matt's eye at the lap gate.

**Acceptance criterion.** At `t = contact + 0.5 s`, the struck mob's ROI contains **≥ 120 px²** of pixels exceeding the local scene-ambient median luminance by **≥ 15%** (differenced against the `set_vfx_visible(false)` control render, § 3). Residue attributable to a given mob persists **≥ 0.6 s** and **≤ 1.6 s** past its contact frame. **≥ N−1 of the N contacted mobs** carry residue simultaneously on at least one frame of the sustain window. Zero residue pixels at effect-end + 2.0 s.

---

### T-3 · Luminance-dominant apex, deep tail, saturated body — *the arc stops being a pastel decal*
**Families:** FF-01, FF-02, FF-12, protocol A-1 (contrast relationship). **Rank:** X-1 #2 + #6, X-2 #2 + #5.

**What the player sees.** The leading edge of the arc is a near-white blaze that is plainly the brightest thing in the room; behind it the ribbon deepens through a strong teal into a dark blue-green that reads as *shadowed moving air*, and the floor and the near flank of whichever skeleton the edge is passing brighten as it goes by.

**The palette translation — my C-1 ruling, stated plainly because it is load-bearing.** X-2 named the defect as *"cool effect on warm scene vs hot effect on cool scene"* and it is tempting to read that as "make the effect warm." **That is the wrong fix and I am ruling it out.** The reference's arrangement worked because the **effect owned the high-luminance end and the scene owned the low**; teal against maroon-magenta is already near-complementary and is a *gift*, not a problem. Our defect is the **value ordering**: we handed the luminance to the scene. Restore the ordering, keep the hue. Precedent, and it is exact: D2's Blizzard and PoE's Ice Nova both put a **white** apex on an unambiguously cold effect, because apex is a statement about luminance, not about temperature.

Current wind is `Color(0.72, 0.95, 0.82)` — HSV S ≈ 0.24, a **pastel**, uniformly applied. Target ramp along the trail's age axis (guidance values; drax may tune within the criterion):

| Band | Colour | HSV | Role |
|---|---|---|---|
| Apex — leading edge / outer tip | `Color(0.92, 1.00, 0.98)` | S ≈ 0.08, V ≈ 1.00 | the wind-native "hot core" |
| Body — mid trail | `Color(0.24, 0.90, 0.74)` | S ≈ 0.73, V ≈ 0.90 | the element's saturated register |
| Tail — oldest samples | `Color(0.05, 0.26, 0.34)` | S ≈ 0.85, V ≈ 0.34 | disturbed air falling into shadow |

**⚠ A dark tail is impossible under additive blending — this is the technical crux of T-3.** `_ribbon_mat` is `BLEND_MODE_ADD` (`wwcr_whirlwind.gd:475`); ADD can only lighten, and adding a low-saturation teal onto a warm mid-value floor produces a washed neutral, which is precisely why the current arc has neither hue contrast nor value contrast. So: **split the ribbon into two co-located surfaces built from the same `_hist`** (anchoring and `physical-cause` preserved, both still rebuilt from where the blade actually is):
- `TrailRibbonCore` — ADD, the newest ~35% of the age range, apex→body colours, `emission_energy_multiplier` raised until criterion (a) passes.
- `TrailRibbonBody` — MIX/alpha, the remaining age range, body→tail colours, **darkening** as it ages rather than only alpha-fading.

**FF-12 sub-part (T-3b).** The contact sparks already carry `OmniLight3D` (range 1.1, energy 1.6·k). Add one **arc light** riding the ribbon apex — a single `OmniLight3D` positioned at the newest history sample, range ~2.5–3.5 m, energy scaled by `_w` and gust-modulated by T-4. Shadows off (C-1 house rule already in force in this file).

**Guard note — TRAIL-BOUNDED.** `set_element()` asserts exactly two tinted surfaces (`wwcr_whirlwind.gd:307`). This spec adds tinted families (core/body split, shed quanta, recipient residue), so the assert **must be amended, not deleted or bypassed**. Amend it to a **named allow-list of five** — `TrailRibbonCore`, `TrailRibbonBody`, `ContactSpark`, `ShedQuantum`, `RecipientResidue` — each entry carrying a one-line justification, **and restate the clause the count was standing proxy for:** *no tinted surface may be CONTINUOUS or PERSISTENT at or beyond `R_ENGAGE`.* Scuffs stay neutral (`SCUFF_COLOR` untouched, R-9 hue-vs-value ruling intact); shed quanta are discrete and brief; residue is actor-attached and ≤ 1.6 s. That keeps the guard a guard — it still fails loudly on the Eye-of-Reckoning failure it was written to catch. **Flagged as a reasoning-boundary call, veto-open: if the conductor or Matt reads a five-entry allow-list as the guard's dissolution, T-3 halts rather than proceeds.**

**Acceptance criteria.**
- **(a) Luminance dominance.** Brightest 1% of effect-region pixels ≥ **2.2×** the median luminance of an annular scene sample (Cathedral floor + walls, effect region excluded). *Currently < 1.0 — the arc is dimmer than the room.*
- **(b) Internal range.** Within the effect region, P95 luminance ÷ P20 luminance ≥ **4.0**.
- **(c) Saturation.** Effect-region mid-band HSV S ≥ **0.55** (currently ≈ 0.24).
- **(d) Apex rides the leading edge.** Intensity-field peak sits within the leading **25%** of the arc's angular extent on **≥ 80%** of sustain frames.
- **(e) Cast light (FF-12).** At least one non-effect surface — floor within 1.5 m of the arc, or a mob's near flank — shows **≥ 8%** luminance lift correlated with arc proximity, differenced against the vfx-off control.

---

### T-4 · Lifecycle phases + arrhythmic gust texture — *an event, not a loop*
**Families:** FF-11, FF-08. **Rank:** X-2 #3 + #9, X-1 #7.

**What the player sees.** The spin *starts* with a pale ring-snap at the caster's waist height; while it holds, the arc surges and eases like wind rather than ticking; when it ends, the ribbon does not switch off — it breaks into fragments that scatter and gutter out after the arc itself is gone.

**Implementation guidance.** The state machine already exists (`WINDUP → RISING → SUSTAIN → FALLING → IDLE`) and is *visually undifferentiated*. Give each phase a distinct read:
- **Onset accent** (at RISING start): one-shot pale ring-pop at `SWEEP_Y`, expanding ~0.6·`R_ENGAGE` → ~1.05·`R_ENGAGE` over 0.12–0.18 s, apex colour, ADD. This is the translated principle behind the reference's flash-halo (X-1 residual), not a copy of it.
- **Sustain:** a **gust stream** — a seeded Poisson event process (exponential inter-arrival intervals, **CV = 1.0 by construction**, squarely inside the 0.45–1.15 authoring band), rate ~8–14 events/s scaled by `_w`. Each gust briefly surges apex emission (~1.3–1.7×) and fires a burst of T-5 shed quanta. **Use a dedicated seeded `RandomNumberGenerator`**, not the global RNG — renders must stay bit-reproducible and independent of other draw consumers (this file already reasons about RNG sequence position at `wwcr_whirlwind.gd:652`).
- **Contact ticks stay phase-locked.** Blade passes are physical truth; do not randomise hits. The arrhythmia lives in the *gust/shed* stream, which is what the reference corpus's CV was measured on.
- **Decay:** during FALLING the trail **breaks up** rather than dimming uniformly — oldest history samples convert to drifting quanta; last quanta outlive the ribbon's final frame.

**Acceptance criteria.**
- **(a) Onset.** A frame inside the first 0.30 s where effect-region luminous area ≥ **1.6×** the sustain-window mean, lasting **6–12 frames**.
- **(b) Temporal texture.** Measured event-interval **CV ∈ [0.45, 1.15]** over the sustain window; the FF-08 trip-flag (CV < 0.25 **+** single spectral tone > 1000× median) must **not** fire. *Current arc: CV ≈ 0.10, a metronome.*
- **(c) Decay.** No single frame-to-frame drop in effect-region luminous area **> 35%** at effect end; last quanta persist **≥ 0.35 s** past the ribbon's final frame.
- **(d) Phase structure.** ≥ **4** segmentable regimes in the effect-region area-vs-time curve.

---

### T-5 · Shedding + cross-section variation — *the arc stops being the same shape twice*
**Families:** FF-04, FF-03. **Rank:** X-1 #4 + #8, X-2 #6 + #8.

**What the player sees.** The edge throws off flecks of pale air that fly tangentially and die at different moments, and the ribbon itself is never the same width twice — it thins and thickens as it comes round, so no two revolutions match.

**Implementation guidance.** Shed quanta spawn off the **ribbon apex** (not the engagement ring — that is 4a's scuffs, which stay neutral and stay put in their own lane), on the T-4 gust stream, with tangential velocity inheriting the blade bearing derivative and exponential drag, exactly as 4a does. **W1 F-2 binds:** `mi.scale` renders nothing under `BILLBOARD_ENABLED`. Size spread must come from **distinct `QuadMesh.size` values across the pool** (build the pool with, say, 5 size classes) or from count — never from a runtime scale write. Cross-section: modulate `TRAIL_INNER_FRAC`'s effective width per history sample with a low-frequency noise term keyed on `_spin`, so the width profile does not repeat per revolution. Keep the existing `TRAIL_SAMPLES` open-arc guard — the arc must stay an arc, not close into a ring.

**Acceptance criteria.**
- **(a) Census.** Mean **≥ 6** distinct connected components per frame during sustain (currently 1–2), with component-area spread **IQR/median ≥ 0.5**.
- **(b) Non-repetition.** Arc width profile at matched rotational phase across consecutive revolutions differs by **≥ 8% RMS**. *Currently ≈ 0 — X-2 cites cf_100 vs cf_115 as identical.*

---

### T-6 · Environment aftermath — *the floor remembers*
**Families:** FF-06. **Rank:** X-1 #3, X-2 #4.

**What the player sees.** Where the sweep passed, the tile is scoured — faint dust-scrubbed arcs accumulate under the engagement radius as the spin goes on, and they are still there when the effect is over and the room is quiet.

**Implementation guidance.** Wind-native translation of the reference's blood/char: **abrasion, not burning.** Accumulate low-alpha decal quads on the floor plane at the engagement radius on blade passes — neutral `SCUFF_COLOR` family (R-9 intact), alpha ~0.10–0.18, **no lifetime expiry** within the capture window. Additive is wrong here; MIX, slightly darker than tile. They must appear *progressively*, not all at once.

**Acceptance criteria.** At clip end, the floor region under the engagement annulus differs from the pre-effect frame in **≥ 2,500 px²** with mean |ΔL| ≥ **6/255**. *Currently pixel-identical (X-1 dim 5: c0208 identical to c0001).* Marked area is monotonic non-decreasing during sustain, and changes by **≤ 5%** between effect-end and clip-end.

---

### B-1 · Build requirement (not a treatment, but the criteria depend on it)

The current seq window is `0.20 → 3.70 s`, which **ends at effect-off**. T-4(c) and T-6 are measured in the aftermath and cannot be measured in a window that has none. **Extend `_seq_to` to give ≥ 1.5 s after the effect reaches IDLE.** The capture plan is already parameterised (`wwcr_stage.gd:180-186`), so this is a re-invocation, not a re-authoring. Encode-then-prune law (R-18c) applies. **Render two artifacts:** treatment-ON, and a `set_vfx_visible(false)` control over the identical window — the control is the differencing baseline that T-2 and T-3(e) require, and it already exists in the file as the occlusion gate's valid baseline (`wwcr_whirlwind.gd:246`).

### Cut line, if the wave runs short

Land in numbered order. **T-1 → T-3 → T-4 is the irreducible core**: consequence, figure-ground, and event-shape. A lap that lands only those three has moved the owner's question. T-2, T-5, T-6 are the next three and each is independently landable. Do not part-land T-3 — the two-surface split and the guard amendment go together or neither goes.

---

## § 2 — Parked for lap-3 (named, not trimmed — charter § 2 fallback discipline)

- **FF-05 volumetric embedding** — ground haze in the engagement annulus that the spin visibly stirs; both passes ranked it mid (X-1 #5, X-2 #7) and it is the largest single remaining gap after this lap.
- **Smoke / atmospheric layer** above the engagement ring — the reference's smoke is fire's byproduct; the wind translation (lifted dust column) needs its own design pass, not a rushed analogue.
- **Arc angular span** — X-2 #10: the reference's caster swirl is a full radially-smeared 360°, ours a hard-edged 90–120° crescent. Widening it collides with the `TRAIL_SAMPLES` open-arc guard's stated reason and deserves a deliberate ruling, not a constant bump.
- **Caster travel signature** — X-1 #9; partly animation/gameplay seam, and X-1 flagged the caveat itself.
- **Inter-layer interaction** — X-2 #9: layers that light and occlude each other rather than co-existing.
- **FF-07 camera somatic response** — correctly true-negative on this exemplar (neither clip shakes); enters at the Demonic Leap held-out case per R-10.
- **Recast / burst event structure** — X-1/X-2 disagree and the substrate cannot settle it (R-20e); do not build on an unobservable.
- **4a scuff entrain-magnitude retune** — N-2 deferred it as subsumed by this spec; revisit only if T-5 fails to carry the outer radius.

---

## § 3 — Measurement plan (galadriel)

| Criterion | Instrument |
|---|---|
| T-1 (centroid / axis) | per-mob ROI silhouette tracking; centroid + principal-axis fit, treatment vs vfx-off control |
| T-2 (residue) | per-mob ROI luminance-threshold differencing vs control; lifetime census per attached emission |
| T-3 a/b/c | effect-region percentile luminance + HSV statistics; annular scene sample as the ambient reference |
| T-3 d | intensity-field peak tracking vs motion direction (FF-01's registered detection route) |
| T-3 e | cast-light differencing on adjacent surfaces, treatment vs control |
| T-4 a/c/d | effect-region luminous-area-vs-time curve, phase segmentation |
| T-4 b | `frame_forensics*.py` event-interval CV + spectral tone (the trip-flag law's own instrument) |
| T-5 a | connected-component census per frame |
| T-5 b | silhouette width profile at matched rotational phase, revolution-over-revolution |
| T-6 | floor-region pre/post differencing; per-frame marked-area accumulation curve |

**Notes.** Camera is static in this venue, so the G-5 pan-null gap does not bite this lap. Every criterion above is stated in image space at the ratified pin (23.1627 m stand-off, 52.95° pitch, 47.0° yaw, 31.786° vertical fov, k = 0.665, 1920×1080); meters appear only as implementation guidance, per the N-2 standing law. For scale intuition only: ≈82 px/m at the caster's ground plane, from the 4a block's measurement — **do not convert criteria through it**, measure in image space directly.

---

## § 4 — Sign-off

Seven families served (FF-01, FF-02, FF-03, FF-04, FF-06, FF-09, FF-10, FF-11, FF-12 + protocol A-1); FF-05 and FF-07 named and parked with reasons. Both passes' #1 is T-1/T-2; their #2 is T-3; their #3 is T-4 — the priority order is the union of the ranked lists, top-down, with nothing reordered by taste.

**Two calls are mine and both are veto-open.** First, the palette ruling: *the fix for a cool effect on a warm scene is not a warm effect — it is restoring the effect's ownership of the high-luminance end, which teal can do and currently does not.* Second, the TRAIL-BOUNDED amendment: the guard survives as a **named allow-list plus an explicit no-continuous-tinted-surface-at-`R_ENGAGE` clause**, because a bare count was only ever a proxy for that clause, and a proxy that blocks correct work while still admitting the failure it was written against is worse than the clause stated outright. If either reads wrong to the conductor's DRIFT-CRITIC pass or to Matt's eye, the affected treatment halts rather than proceeds.

**Signed:** gandalf, SPEC-AUTHOR, 2026-08-25.

---

## § 5 — Conductor DRIFT-CRITIC review (pre-build gate)

**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC** (conductor session, distinct context from the § 4 author). Verdict: **APPROVED FOR BUILD, as amended.**

- C-1..C-6 all hold: wind identity preserved everywhere (abrasion not burning, knock-flinch not death, teal kept); R-20e honored (residue ≤ 2.0 s, recast structure parked as unobservable); every criterion image-space at the ratified pin; CV = 1.0 by construction with contact ticks correctly left phase-locked; cut line makes one-wave scope honorable; no F4/F5 bars, no camera writes.
- **Author call 1 (palette: luminance ordering, not hue warming) — SUSTAINED.** Correct read of X-2 #2; D2 Blizzard / PoE Ice Nova precedent exact; the alternative dissolves wind identity.
- **Author call 2 (TRAIL-BOUNDED → five-name allow-list + restated no-continuous-tinted-at-`R_ENGAGE` clause) — SUSTAINED.** The count was a proxy; the clause is the guard. Build condition: the clause lands as enforced check where mechanically checkable (residue lifetime, quantum discreteness), comment-documented where not — and the amendment ships in the same commit as the two-surface split, per the spec's own "together or neither" line.
- **Conductor amendment (factual):** mob-count criteria re-based from a hardcoded 4 to build-time-verified N — both blind passes counted five skeletons; the spec's "4" was unsourced. T-1/T-2 criteria now read "all N" / "≥ N−1".
- Both § 4 calls remain **veto-open to Matt** at the lap gate alongside the R-20e magnitude judgments.

**Signed:** gandalf, DRIFT-CRITIC / RUN-CONDUCTOR, 2026-08-25.
