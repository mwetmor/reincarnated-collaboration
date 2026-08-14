# SB-1 Cell CLK-1 — THE CLOCK CELL · BOTH SUSPECTS WALKED

**Cell ID:** `SB1-CELL-CLK-1` · **Date:** 2026-08-13 · **Author:** drax (presentation seam)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — row **CLK-1-0** is the charter;
**A2f-2** (the fracture + the conductor's blend hypothesis) is the founding document.
**Base:** the A2f landing `drax/notes/2026-08-13-sb1-a2f-density-landing.md` § 2.
**Godot repo:** `bf39491` → `6eff089`, **two commits, pushed as they landed (PL-7);** the third
(this note) lands in the collaboration repo.

---

## ⚑ VERDICT

**THE CONDUCTOR'S HYPOTHESIS IS DEAD. BOTH OF A2f's NAMED CANDIDATES ARE ACQUITTED. THE CLOCK THAT
WAS LOOSE IS A THIRD ONE NOBODY HAD NAMED — A ONE-TIME RENDERER TRANSIENT AT ENGINE FRAMES 18..25 —
AND FG-10 NOW RETURNS *ONE DISTINCT STATE* ON EVERY LEG OF A FIVE-LEG MATRIX.**

| candidate | verdict | the measurement that decided it |
|---|---|---|
| **Conductor's blend-window hypothesis** | ⚑ **REFUTED, TWICE** | the disagreeing frames contain **no `play()` at all**, and every frame inside a 0.18 s blend window **agrees** |
| **(a) `AnimationPlayer` phase** | ⚑ **ACQUITTED AT THE BONE** | 6 passes: bone-pose digest **bit-identical ×6**, PNGs in **3 distinct states** |
| **(b) `GPUParticles3D` sim phase** | ⚑ **ACQUITTED BY PROBE** | hide **every** particle system every frame → **4 distinct states in 6 passes** |
| **(c) a one-time RENDERER warm-up** | ⚑ **CONVICTED BY PROBE DELTA** | 151 frames × 4 passes: the *only* frames that ever disagree are **18..25**; 26..150 bit-identical. Excluded by a tick-frozen preroll → **1 state** |

⚑ **AND THE NUMBER MATT NEEDS INVERTS A2f's SENTENCE.** A2f routed this up as *"isolating it changes
what every body looks like in every future frame."* Measured against the sha-pinned clip Matt
watched: **the clock fix moves the picture by 0.14 of 255 — 0.06 % of full scale.** What moves the
picture is the **warm-up preroll**, at **+5.01**, and it moves it by re-drawing the **smoke and spark
field** from a different phase — a different draw of a distribution A2e § 0 had already declared was
one draw. **No body, no geometry, no palette, no cut layout.** (§ 3.2.)

| item | commit | what |
|---|---|---|
| **1** | `e81a827` | **CONVICT** — the correlation instrument, the pose digest, the two bisect switches |
| **2** | `6eff089` | **FIX** — locomotion phase seeked from the tick; a measured warm-up preroll; FG-10 raised from one leg to five |
| **3** | *(collab)* | this note + evidence stills. **NO MP4. NO MANIFEST. Nothing promoted.** |

---

## 0 · THE PROBE STILL FIRED AT HEAD BEFORE ANYTHING WAS TOUCHED

GL-6 first: baton `kc2-baton-v1-E-s09-cp150-20260809_052836.json` recomputed from bytes =
`d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa`, 1,065,632 B — **MATCH**.

Then the defect, re-verified at `bf39491` **before a line moved** (`PROBE_PASSES=4`, d-close,
rate 17): **2 distinct states, disagreeing frames 18,19,20,21,22,23,24,25.** 82 s for four passes.
The cell opens on a live defect, not on a remembered one.

---

## 1 · ITEM 1 — CONVICT

### 1.1 ⚑ THE CONDUCTOR'S HYPOTHESIS, TESTED FIRST AND KILLED FIRST

The hypothesis: the band is a **blend window** after a mid-span `play(p, BLEND_S)`.

It is testable **without rendering anything**, because a body's locomotion state is a pure function
of the tick — so the frames at which `play()` fires are computable from the wire. That is
`scripts/kc2_clk1_probe.gd`: walk the clip's own frame→tick law, print every state change.

**d-close** (t0 = 1600, dt = 0.408333 ticks/frame, `BLEND_S` = 0.18 s = **5.40 frames**):

| | frames |
|---|---|
| `play()` fires at | **10, 32, 35, 40** |
| visibility flips at | *(none)* |
| covered by a 5.40-frame blend window | 10–16, 32–45 |
| **RENDERED DISAGREEMENT** | **18–25** |

⚑ **The band contains ZERO `play()` calls, and every frame inside a blend window AGREES.** The two
sets are disjoint. The hypothesis predicts disagreement exactly where the pixels are identical.

**b-ring** is the second nail: over the same 46-frame window from t0 = 1570 there are **zero `play()`
calls and zero visibility flips** — and A2f measured a band at 18–25 there anyway. A scene with no
state changes cannot be disagreeing because of a state change.

The residue the charter asked me to account for (bands of 8–10 frames against a 5.4-frame blend)
**dissolves rather than resolves**: there is no blend in the band to be wide or narrow.

### 1.2 ⚑ CANDIDATE (a) — ACQUITTED AT THE BONE, NOT BY ARGUMENT

`--phaselog on` prints per rendered frame: the mixer's own `current_animation_position` for the
bodies on the board, **and a SHA-256 over every visible body's local bone pose** — the exact quantity
that becomes a silhouette.

**Six passes of the identical span:**

| quantity | result |
|---|---|
| phase log (mixer clock, 45 frames × 5 bodies) | **IDENTICAL ×6** — `0d6218525ff18159` |
| bone-pose digest stream (all visible bodies, 45 frames) | **IDENTICAL ×6** — `f9c8f9e65de714ab` |
| **rendered PNGs** | **3 DISTINCT STATES** — `9d15c830`×3, `28cd67dd`×1, `db3bc049`×2 |

**The animation layer writes the same skeleton, bone for bone, on runs whose pixels differ.** The
phase also reads exactly `(f−1)/30` s — a clean function of the frame index. Candidate (a) is not
the clock.

*(The first cut of this instrument logged the first four bodies in `actor_order` and printed
`0.000000000/act0` forever: four INACTIVE players, off the board in this window. An instrument
measuring its own idle list. The picks now happen after the first `apply_tick`.)*

### 1.3 ⚑ CANDIDATE (b) — ACQUITTED BY PROBE, AND IT GOT *WORSE*

`--fx off` walks the tree every frame and hides **every** `GPUParticles3D` — smoke bed haze, three
spark emitters, the ember trail.

| bisect | passes | distinct states |
|---|---|---|
| `--fx off` (no particles at all) | 6 | **4** |
| `--anim off` (no `AnimationPlayer` at all) | 3 | **3** |
| shipped configuration | 6 | 3 |

**Removing the suspect does not remove the defect.** Both named candidates are out.

### 1.4 ⚑ AND THE FIRST BISECT WAS A SHAM, WHICH THE DIGESTS THEMSELVES REPORTED

The first bisect passed its flags through an unquoted shell variable — and **zsh does not
word-split**, so Godot received one argument `"--fx off"`, no flag matched, and twelve "bisect"
renders were twelve more runs of the **shipped** configuration.

It was caught because the digests came back as *the same three states* rather than as new ones. ⚑ **A
bisect whose switch does nothing is indistinguishable, by verdict, from a bisect that exonerates** —
the only thing that separated them here was that the exact 64-bit digests had been seen before.

### 1.5 ⚑ WHAT IS CONVICTED: A ONE-TIME RENDERER TRANSIENT, BOUNDED BY MEASUREMENT

A **151-frame** span, rendered **four** times:

```
distinct states: 2       frames that ever disagree: 18,19,20,21,22,23,24,25
```

**Frames 26 through 150 are bit-identical on every pass.** The transient is one-time, it is over by
frame 26, and it never returns.

Three further properties, each measured:

* **It is indexed by the ENGINE frame, not by the trace.** The same band appears on b-ring (t0 1570)
  and d-close (t0 1600), and A2f saw it at rate 11 too. Observed support across all runs: **[16, 25]**.
* **It is NOT a time shift.** Fit `B[f] − A[f] ≈ α·(A[f+1] − A[f])`: **α ≈ −0.002, 0.0 % explained**.
  Nothing about the scene is early or late.
* **Its pixel signature is a shader, not a scene.** At frame 20, 56.0 % of pixels differ;
  **86.8 % of channel samples are within ±1**, 2.23 % ≥ 8, 0.39 % ≥ 32; mean signed **+0.26/channel**
  and *rising with source intensity*; the large differences sit on high-contrast **body silhouettes**,
  and even the static floor grid differs. Broad, sub-LSB, multiplicative, healing exactly.

⚑ **THE SUB-MECHANISM IS NAMED, NOT PROVEN (GL-12).** That signature is what **asynchronous
shader-pipeline specialisation** looks like — the same geometry drawn through an ubershader and then
through a specialised pipeline, with the switch happening on a background thread. I did not prove it
and I am not going to claim it. What is **proven** is the operational fact the fix rests on: the
transient is confined to the first 26 frames of the process and the frames after it reproduce
exactly.

---

## 2 · ITEM 2 — FIX · commit `6eff089`

**NO DESIGN CHANGE.** Same three clips, same state machine, same thresholds, same pose grammar. What
moved is *which clock measures when-in-phase*, and *which frames get captured*.

### 2.1 The locomotion phase is now a pure function of the tick (NOTE-68 / GL-18)

| file:line | what |
|---|---|
| `scripts/kc2_motion.gd:67` | `_state_start` — per actor, per leg, the tick that leg's clip state BEGAN |
| `scripts/kc2_motion.gd:189` | `_build_state_starts()` — computed **once** from the wire: the start knot of the maximal run of consecutive legs sharing a state class |
| `scripts/kc2_motion.gd:211` | `state_for_speed()` — the classification in **one** place, so the driver and the phase anchor cannot form two opinions |
| `scripts/kc2_motion.gd:221` | `clip_phase_s(aid, leg, tick_f)` — pure in its arguments |
| `scripts/kc2_motion.gd:299` | `an.seek_phase(clip_phase_s(aid, leg, tick_f))` — on **every** tick, not only on state changes |
| `scripts/kc2_body_anim.gd:182` | `seek_phase()` — `player.seek(fposmod(phase_s, len_s), true)`, the in-tree precedent from `_sample()` |

⚑ **This is not a new semantics — it is the old one, measured from the right clock.**
`set_state()` calls `play(p, BLEND_S)` (`kc2_body_anim.gd:149`) and `play()` restarts a clip at zero,
so *"phase = time since this state began"* has always been the rule. Before, that time was counted in
**process steps**; now it is read in **trace seconds**.

⚑ **CALLBACK MODE STAYS `IDLE`, DELIBERATELY.** `ANIMATION_CALLBACK_MODE_PROCESS_MANUAL` would have
been the purist's answer — the mixer would advance only when seeked — and it would have **frozen the
`BLEND_S` crossfade mid-mix**, which *is* a change to what a body looks like. HALT-rather-than-change
applies to purity too. The consequence is stated in the code: the rendered phase is `seek target +
one process step`, a **constant** on every body and every frame rather than an accumulating history.
The difference that matters is that drift can no longer *persist* — a dropped frame used to shift a
body forever; now the next tick puts it back.

### 2.2 A tick-frozen warm-up preroll — `scripts/kc2_cpb_clip.gd:70`

`PREROLL_FRAMES := 60`. Sixty frames are rendered **at the shot's first tick** — the trace does not
advance, so no trace time is consumed and the deliverable starts on the tick it always did — and
`prune_preroll` (`scripts/run_kc2_cpb_clip.sh:83`) deletes them before any encode or comparison.

**60 = 2.4× the measured end of the transient (frame 25).** FG-10 is the falsifier: if the transient
ever outruns the preroll, the gate fires and this constant is wrong.

⚑ **THIS IS AN EXCLUSION, NOT A REPAIR, AND THE NOTE SAYS SO WHERE THE CODE SAYS SO.** The renderer
still has a non-reproducible first second. This cell measured its bound and refuses to capture inside
it.

### 2.3 ⚑ THE PREROLL IS ONLY FREE BECAUSE OF THE SEEK — PROVEN, NOT ASSERTED

The claim in the code comment is falsifiable, so it was falsified. **Declared temporary working-tree
operation** (NOTE-69): with both states committed first, `an.seek_phase(...)` was replaced by `pass`,
two renders were taken, and the file was restored from a byte copy (`git status` clean afterwards).

| preroll 0 vs preroll 60, same shot, 45 shot frames | mixer-phase mismatches | pose-digest mismatches |
|---|---|---|
| **WITH the fix** (`6eff089`) | **0 / 45** | **6 / 45** |
| **WITHOUT the fix** (falsification) | **45 / 45** | **45 / 45** |

Worked example at shot frame 22, body `w160_a000`, without the fix:
`run@0.000000012` at preroll 0 versus `run@0.600000036` at preroll 60 — **the same trace tick, two
different bodies.** With the fix both read the same number to nine decimals.

⚑ **AND THE SIX FRAMES THAT DO DIFFER ARE THE CONDUCTOR'S BLEND WINDOW.** Frames 0–5 =
`ceil(0.18 s × 30 fps)` = the entry crossfade that `_ready`'s first `apply_tick` opens. It was real;
it was simply never the defect. **The preroll completes it before capture too** — so a captured frame
no longer contains a process-clocked crossfade tail at all.

### 2.4 FG-10 stopped probing one quarter of what it passes

A2f's gate rendered **one** (shot, cadence) pair and certified a clip made of **four**. The probe is
now a matrix (`scripts/run_kc2_cpb_clip.sh:137`) over every pair the render promotes, plus an
anti-overfit leg on a tick window no shot renders (`--tick0`, `kc2_cpb_clip.gd:250`). `PROBE_ONLY=1`
runs the gate alone.

### 2.5 The smoke asserts the new law — 69 → 71 checks, 0 FAIL

`state_digest` could **never** have caught this defect: it hashes visibility, position, leg, clip
*name* and yaw, and the phase is in none of those. Two new rows (`kc2_motion_smoke.gd:435`) read the
mixer's own clock:

| row | result |
|---|---|
| `CLK-1 locomotion phase == f(tick)` — mixer position vs the wire-derived phase | **PASS** — 14 (body, tick) samples, worst \|mixer − wire\| = **0.000000000 s** |
| `CLK-1 locomotion phase survives a round trip` — tick → 3000 → 120 → tick | **PASS** — worst drift **0.000000000 s** |

The second row is the one with teeth: **process-clocked phase cannot pass it, because nothing ever
rewound a clip.**

---

## 3 · ITEM 3 — EVIDENCE. NO CLIP.

### 3.1 THE PROBE TABLE — FIVE LEGS, `PROBE_PASSES=4`, RATE 17 AT HEAD

`PROBE_ONLY=1 PROBE_PASSES=4 bash scripts/run_kc2_cpb_clip.sh`

| leg | shot | cadence | tick window | **BEFORE** (`bf39491`) | **AFTER** (`6eff089`) | digest-of-frame-digests |
|---|---|---|---|---|---|---|
| 1 | d-close | undulating | 1600.00 | **2 states**, frames 18–25 | ⚑ **1 state, none disagree** | `0253761a43b374b9…` |
| 2 | d-close | stationary | 1600.00 | *(never probed at A2f)* | ⚑ **1 state, none disagree** | `e4f3fa66bf8f0530…` |
| 3 | b-ring | undulating | 1570.00 | **3 states**, frames 18–25 *(A2f)* | ⚑ **1 state, none disagree** | `504b6d8b4c0929ff…` |
| 4 | b-ring | stationary | 1570.00 | *(never probed at A2f)* | ⚑ **1 state, none disagree** | `bb1c8950277bdf43…` |
| 5 | **b-ring, ANTI-OVERFIT** | undulating | **1660.00** — a window no shot renders and this cell does not otherwise touch | *(never rendered by anyone)* | ⚑ **1 state, none disagree** | `5c9fbb6e1f788cdf…` |

**5 legs × 4 passes × 46 frames = 920 rendered frames, ONE distinct state per leg, ZERO disagreeing
frames anywhere.** Full receipt banked beside the stills at
`galadriel/captures/2026-08-13-sb1-clk1-clock/clk1-fg10-probe.txt`; FG-12 prune receipts at
`…/clk1-fg12-prune-receipts.txt`.

⚑ **Two of these five legs had never been probed at all.** A2f's gate rendered `d-close/undulating`
and certified a four-segment clip. Legs 2 and 4 are the stationary halves it passed unmeasured.

**And the reference measurements that make the AFTER column mean something** — all at `bf39491`,
before a line moved:

| span | passes | distinct states | frames that ever disagree |
|---|---|---|---|
| d-close, 46 frames | 4 | 2 | 18–25 |
| d-close, 46 frames, `--phaselog` | 6 | 3 | — |
| d-close, 46 frames, `--fx off` | 6 | **4** | — |
| d-close, 46 frames, `--anim off` | 3 | 3 | — |
| **d-close, 151 frames** | 4 | 2 | **18–25 and nothing else** |

### 3.2 ⚑ THE vs-A2e VISUAL DELTA — AND IT INVERTS A2f's SENTENCE

**Reference:** `galadriel/captures/2026-08-13-sb1-a2e-cpbprime/cpbprime-cadence-ab.mp4`, digest
**recomputed from bytes before a frame was read** — `e2f6a03cc490…`, 43,727,767 B, **MATCH**.
**Tool:** `agentic_orchestration/drax/tools/kc2_clk1_vs_a2e.py`. Segment bounds read from the A2e
MANIFEST, not retyped.

⚑ **THE REFERENCE IS H.264 CRF-12, SO A DECODED FRAME IS NOT THE FRAME THAT WAS RENDERED, AND
QUOTING THE RAW DIFFERENCE AS "THE FIX'S DELTA" WOULD INFLATE IT.** Every row below reports the
**codec floor** beside it — the same rendered frames encoded with the A2e settings, decoded, and
differenced against themselves. Only what stands above that floor is scene change.

**Two segments compared, both fade-free** (the encode fades A's last shot and B's first, and an
encoder ramp is not a scene difference). Between them they cover **both cadences and both shots**.

| leg (all at `CUT_PER_REV` **11**, the A2e article) | frames | mean \|Δ\|/channel vs A2e | codec floor | **above floor** | ≥8 | ≥32 | max |
|---|---|---|---|---|---|---|---|
| **CONTROL** — no fix, preroll 0 *(≡ `a1ece3a` behaviour)* · B/d-close | 173 | 1.3612 | 0.9639 | **+0.40** | 2.50 % | 0.24 % | 218 |
| **DECOMPOSITION** — no fix, preroll 60 · B/d-close | 173 | 6.3757 | ~0.95 | **+5.42** | 31.02 % | 1.47 % | 239 |
| ⚑ **SHIPPED** — fix + preroll 60 · B/d-close | 173 | **6.5205** | 0.9541 | **+5.57** | 31.34 % | 1.66 % | 242 |
| ⚑ **SHIPPED** — fix + preroll 60 · A/b-ring | 320 | **2.5779** | 0.7997 | **+1.78** | 8.53 % | 0.78 % | 247 |

**The control lands 0.40/channel above the codec floor.** That is A2e's own clock jitter (its frames
were one random draw) plus whatever separates `a1ece3a` from HEAD-at-rate-11 — and it is small, which
also confirms that A2f's rate raise and comment sweep changed no pixels.

### ⚑ THE ATTRIBUTION, AND IT IS NOT WHAT A2f PREDICTED

A2f routed this up as *"isolating it changes what every body looks like in every future frame."*
**True — and the locomotion seek is not what does the changing.** The three legs decompose it:

| component | mean \|Δ\| per channel | share of the change |
|---|---|---|
| H.264 CRF-12 codec floor | 0.95 | *(not a change)* |
| A2e's own clock jitter + `a1ece3a`→HEAD residual | **+0.40** | *(not mine)* |
| ⚑ **THE WARM-UP PREROLL** — 60 extra frames of particle simulation | **+5.01** | **97 %** |
| ⚑ **THE LOCOMOTION SEEK** — the fix everyone was afraid of | **+0.14** | **3 %** |

**The clock fix moves the picture by 0.14 of 255 — 0.06 % of full scale.** The thing that moves the
picture is the warm-up, and it moves it by re-drawing the **smoke and spark field from a different
phase**.

Measured directly, without a codec in the path — my own preroll-0 render against my own preroll-60
render, both with the fix disabled, so the *only* difference is 60 frames of process:

```
mean |delta| per channel 5.7132        frame 39: 69.4 % of pixels differ, max 238
4x4 mean|delta| grid, top -> bottom:     0.05   1.38   0.59   0.03
                                         4.10  10.06   7.72   2.19
                                         8.30  23.49  16.54   6.41
                                        10.35  45.28  26.39  11.00
```

⚑ **The change is in the LOWER CENTRE OF THE FRAME — the smoke bed and the spark ring — and the top
quarter is untouched (0.03–1.38).** It is a **different draw of the same distribution**, in exactly
the layer A2e § 0 already declared was *"one draw from a distribution"*. No body, no geometry, no
palette, no cut layout.

### WHICH FRAMES, AND IS IT CONFINED TO THE OLD JITTER BAND?

**No — and it was never going to be.** The old band was where two *runs* disagreed; the fix changes
the *article*, everywhere.

| leg | per-frame mean \|Δ\| range | worst frames | band 16–25 vs rest |
|---|---|---|---|
| SHIPPED B/d-close | 5.05 → **10.64** | **34–41** (peak f39) | 7.71 vs 6.45 — **ratio 1.20** |
| SHIPPED A/b-ring | 1.99 → **4.08** | **87–100** (peak f91) | 3.45 vs 2.55 — **ratio 1.35** |
| DECOMPOSITION (no fix, pr60) | 5.01 → 10.31 | 32–42 | 7.46 vs 6.31 — ratio 1.18 |

The band runs **20–35 % hotter** than the rest of the segment — the residue of A2e's own jitter draw
sitting inside it — but the change is spread across every frame. The worst-frame clusters sit on the
spin's high-motion phase (period 0.36 s = 10.8 frames), where any difference is amplified by contrast.

### 3.3 EVIDENCE STILLS — TEMP/EVIDENCE CLASS, NO MP4, NO MANIFEST

`agentic_orchestration/galadriel/captures/2026-08-13-sb1-clk1-clock/evidence/` — **six PNGs, 960×540,
3.9 MB total; the captures tree is unchanged at 6.7 G.** **UNTRACKED, per the captures tree's own
class-E convention** (A2e's MANIFEST: *"artifact_class = E — owner-eye. UNTRACKED, never
committed."*) — they were staged, then unstaged when I checked the convention rather than assumed it.
The two receipts sit beside them, same class. No MP4, no MANIFEST, nothing promoted; FG-9's deliverable path was never entered.

| file | what |
|---|---|
| `before-pass1-f20.png` / `before-pass2-f20.png` | **the defect** — two renders of the same tick at `bf39491` |
| `before-diff-f20-amplified-x12.png` | their difference at ×12: the whole scene, edges everywhere, mean \|Δ\| **1.03**/channel |
| `a2e-reference-Bdclose-f039.png` | the A2e clip Matt watched, at the worst frame of the comparison |
| `clk1-fixed-Bdclose-f039.png` | the same tick, fixed build, rate 11 |
| `fix-delta-Bdclose-f039-amplified-x8.png` | their difference at ×8 — the haze, and the bodies inside it |

**The "after" has no still, because it has no picture:** four passes of every one of the five probe
legs are **byte-identical**, so the amplified difference is a black rectangle. The number is the
evidence: **0 differing pixels, 920 frames.**

---

## 4 · LAWS

**GL-6** — baton digest recomputed from bytes **BEFORE anything was touched**:
`d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa`, 1,065,632 B — **MATCH**.

**GL-12 — TWO ABSENCES DECLARED, NEITHER FILLED.** (i) The convicted transient's **sub-mechanism** is
NAMED, NOT PROVEN — the signature fits asynchronous shader-pipeline specialisation and I did not
confirm it. (ii) The **particle phase is still process-clocked** — acquitted as the cause, unfixed as
a clock, because `GPUParticles3D` has no seek API to anchor it with. Both are written into the code
where a reader will meet them, not only here.

**GL-13** — the pinned rectangle untouched. **GL-15** — one ongoing-damage read, unchanged: bed +
haze, the 24-node cut pool, 3 burst emitters, one wire bit.

**GL-17 / ADR-006** — no assets copied, no mesh edited, **no acquisitions of any kind**. Three new
files, all authored: one GDScript probe, one Python comparator, this note.

**GL-18 — ⚑ THE ARTIFACT-LEVEL CLOCK CLAIM, WITHDRAWN AT A2f, IS RESTORED — FOR THE CAPTURED SPAN,
ON FIVE LEGS, WITH THE EXCLUSION STATED IN THE SAME BREATH.** Every frame the harness keeps is a
function of the tick. The first 26 frames of the *process* are not, and are therefore never kept.

**R-A1-1** — re-asserted at HEAD with the fix in the tree: **5,123 nodes walked, 0 text/canvas nodes.**

**D-14** — everything ran **classic**, off the factory spine.

**PL-5** — floor-checked before frames: captures **6.74 G of 10 G**, disk free 25.5 G. The captures
tree grows by the evidence stills only (see § 3.3) and carries **no MP4 and no MANIFEST**.

**FG-9 / FG-12** — nothing was promoted; `PROBE_ONLY=1` stops the harness at the gate. **1,441
intermediate PNG (1.87 G) pruned**, receipt with per-directory counts and regenerate commands at
`galadriel/captures/2026-08-13-sb1-clk1-clock/clk1-fg12-prune-receipts.txt`.

**FG-10** — raised from ONE leg to **FIVE**, and from certifying a quarter of what it passes to
covering every (shot, cadence) pair the render promotes plus an untouched window.

**CL-2 / PL-7** — three commits, one per item; the two godot commits pushed as they landed.
⚑ **One CL-2 irregularity, declared:** `kc2_cpb_clip.gd` carries item 1's bisect switches AND item
2's `--preroll` / `--tick0` knobs. They are one file, and splitting them would have meant committing
an intermediate state that never parsed. The split is by FILE, and the commit message says so.

**Containment** — godot **229 untracked at open and 229 at close**; the one dirty tracked file
(`tmp/br2watch/measure/census.json`, modified 2026-08-02) is **not mine and was not touched**.

**UNTOUCHED** — camera, `WEAPON_SCALE` 1.95, grip, palette constants, `CUT_PER_REV` **17**, epoch
bands, spin 0.36. Verified at close.

⚑ **TWO TEMPORARY WORKING-TREE OPERATIONS, BOTH DECLARED, BOTH RESTORED FROM BYTE COPIES TAKEN
BEFORE THE EDIT, BOTH AFTER THE STATE THEY MODIFIED WAS COMMITTED** (NOTE-69):
1. `an.seek_phase(...)` → `pass`, for the § 2.3 falsification. Restored; `git status` clean.
2. `CUT_PER_REV` 17 → 11 **and** the seek disabled, for the § 3.2 comparison against the A2e article.
   Restored; `git status` clean and the constant re-verified at 17.

---

## 5 · SELF-ATTACK SURFACES (ranked, veto-open)

1. ⚑ **THE MECHANISM IS EXCLUDED, NOT REPAIRED, AND THE BOUND CAME FROM ONE IDLE MACHINE.** The
   renderer's first 26 frames are still not reproducible; I measured how long that lasts and stepped
   around it. If the transient is thread-scheduling dependent — which is exactly what its signature
   suggests — then a busier or slower host could push it past frame 60 and the gate would fire on
   someone else's machine and not on mine. **I did not test under load.** The mitigation is that
   FG-10 fires rather than lies, and the constant is one edit.
2. ⚑ **THE SUB-MECHANISM IS UNPROVEN AND I NAMED IT ANYWAY.** "Asynchronous shader-pipeline
   specialisation" is inference from a pixel signature. I did not read a Godot log, toggle a setting,
   or reproduce it in isolation. If it is something else — a compute-pass race, a driver artefact —
   the preroll could be masking a defect that can recur mid-clip rather than only at startup.
3. ⚑ **THE GATE PROBES 45 FRAMES AND CERTIFIES 320.** The b-ring shot is 320 frames long; the
   longest span I ever rendered repeatedly is 151 (clean from 26 to 150). A transient at frame 200
   would pass every leg of the matrix. This is the same shape of hole as A2f's one-leg gate, one
   level along, and I am naming it rather than waiting to be asked.
4. ⚑ **I SPENT 97 % OF THE VISUAL CHANGE ON A WARM-UP AND MATT HAS NOT SEEN IT.** The seek is nearly
   free (+0.14/channel); the preroll costs **+5.01**, concentrated in the smoke bed and spark ring.
   My defence is that the FX draw was never a ratified article — A2e § 0 says so in its own words —
   and that 60 extra frames of simulation is a *different sample of the same distribution*, not a
   different design. **But it is 2 % of full scale in the lower-centre of every frame, and it is a
   judgement I made rather than one I was given.** The lever is one constant: a preroll of 26 would
   clear the measured transient with no margin and cost proportionally less; a preroll of 0 would
   cost nothing and reproduce nothing. A2g's canon-frame clip is where the eye should settle it.
5. **THE FIX ALSO CHANGES THE POSE IN EVERY FRAME, AND THAT PART IS THE 3 %.** Bodies no longer all
   restart their locomotion clip at shot frame 0; each is anchored to when its state began in trace
   time. Strictly more correct — a body that has been running for three seconds should not restart
   its run cycle because the camera started rolling — and now quantified rather than feared.
6. **THE MIXER STILL SELF-ADVANCES ONE PROCESS STEP.** Callback mode stays `IDLE` because `MANUAL`
   would freeze the `BLEND_S` crossfade mid-mix. So the rendered phase is `seek target + 1/30 s` —
   constant, not history, and stated in the code — but it is one step of the old clock still in the
   picture.
7. **THE BLEND TAIL IS STILL PROCESS-CLOCKED.** The preroll completes the ENTRY blend, but d-close
   opens four more inside the captured span (frames 10, 32, 35, 40). They are deterministic under `--fixed-fps` and the
   matrix legs cover those exact frames — asserted, not assumed — but a dropped frame would desync
   them and the seek would not correct the outgoing clip.
8. **THE PARTICLE PHASE IS STILL PROCESS-CLOCKED** (GL-12 above). It is why preroll 0 and preroll 60
   differ in **every** frame rather than in six.
9. ⚑ **MY FIRST BISECT WAS A SHAM AND I VERY NEARLY BANKED IT.** Twelve renders with a dead switch,
   caught only because the digests were *the same three states I had already seen*. Had the run
   landed on unfamiliar values I would have written "both candidates exonerated" from twelve runs of
   the shipped configuration. **A no-op switch and an exoneration produce the same verdict.**
10. **PREROLL 60 COSTS 240 FRAMES PER FULL CLIP RENDER AND BUYS NOTHING VISIBLE.** ~2 s of render per
   shot, spent on frames that are deleted.
11. **I TOOK A2f's RATE-11 REPRODUCTION ON TRUST.** I did not re-run the ratified-rate falsification;
    the exoneration of the rate raise remains A2f's measurement, not mine.
12. **Twenty unlicensed editor addons still stand in the tree; the helmet is still a tepid "ok."**
    Both untouched.

---

## NOTES (continuing from NOTE-70)

**NOTE-71 — TEST THE CONDUCTOR'S HYPOTHESIS FIRST, AND TEST IT WHERE IT IS CHEAPEST TO KILL.** The
blend-window hypothesis was falsifiable **without rendering a single frame**, because the quantity it
depends on — which frames call `play()` — is a pure function of the tick and computable headless.
Twenty seconds of headless walk beat an hour of render forensics, and the answer was not "probably
not" but *the two sets of frames are disjoint.* **Before you go looking for a mechanism in pixels,
ask whether the hypothesis makes a claim you can check in the wire.**

**NOTE-72 — A BISECT SWITCH THAT DOES NOTHING IS INDISTINGUISHABLE FROM AN EXONERATION.** An
unquoted `$MODE` in zsh does not word-split; Godot got one argument `"--fx off"`, matched no flag,
and twelve "bisect" renders re-ran the shipped build. The verdict a dead switch produces — *"the
defect survives with the suspect removed"* — is the same sentence a real acquittal produces.
**Make the bisect prove it bit: the switch must change something you can see even when the defect is
absent.** Here it was luck (the digests were old friends); it should have been a row.

**NOTE-73 — WHEN A DEFECT'S BAND SITS AT THE SAME FRAME INDEX ON TWO DIFFERENT TICK WINDOWS, IT IS
NOT ABOUT THE TICK.** b-ring at t0 1570 and d-close at t0 1600 both disagreed at frames 18..25. That
single coincidence, available from A2f's own table, indexes the defect to PROCESS STARTUP and
excludes every tick-driven layer at once — before a single bisect is run. **Read the frame numbers
before you read the pixels.**

**NOTE-74 — "SEEDED, NOT SEEKED" HAS A THIRD CASE: NEITHER, AND NOT YOURS.** NOTE-68 said the tick
must be the only clock and every layer must be seeked from it. CLK-1 found a layer that cannot be
seeked at all — a renderer warm-up owned by the engine, not by the scene. **The honest move for a
clock you do not own is to MEASURE ITS BOUND AND REFUSE TO CAPTURE INSIDE IT**, name the exclusion as
an exclusion, and leave the gate armed as the falsifier of your own bound. A workaround declared to
the frame is worth more than a repair claimed to the layer.

**NOTE-75 — FIX THE CLOCK YOU CAN OWN EVEN WHEN IT IS NOT THE CULPRIT, BECAUSE IT IS WHAT MAKES THE
WORKAROUND FREE.** The locomotion seek was ACQUITTED of causing the defect and it is still the
load-bearing half of the repair: without it, sixty warm-up frames advance every body two seconds
into its clip and the warm-up is paid for with the pose (measured: 45/45 mismatches without, 0/45
with). **An exoneration is not a reason to leave a clock loose.**

---

*Landed by drax, presentation seam, 2026-08-13. Both suspects walked; a third was convicted by probe
delta. Nothing promoted, no clip rendered, the canon camera untouched. HALTED after evidence.*
