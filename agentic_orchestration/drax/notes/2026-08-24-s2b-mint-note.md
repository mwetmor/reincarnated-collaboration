# Mint note — S2B tranche 2

**Author:** drax (presentation seam, `reincarnated-godot/`)
**Date:** 2026-08-24
**Dispatch:** `agentic_orchestration/dispatches/2026-08-24-drax-s2b-mint-tranche-2.md`
**Law of record:** `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` (STATUS: SEALED)
**Gate procedure of record:** `galadriel/notes/2026-08-24-s2-minted-gate-procedure.md` (§§ 1.2, 1.3, 1.5, 1.9)
**Receipts:** `reincarnated-godot/harness_logs/s2b_e1_2026-08-24/gate.json` · 152 PNG · godot working tree

> **STATE OF THIS NOTE.** §§ 0–5 are **E-0 + E-1 + the two unblocked C-8 items**. **§ 6 is
> ROWS 1 AND 2, MINTED** (tag `drax/v0.1-s2b-rows-1-2`, `7960304`). **Rows 3–7 are NOT
> STARTED** — § 6.9. § 7 records why the rows originally halted and is retained as history.
>
> ### ⚑ A-1 COMPLIANCE — THIS PRE-REGISTRATION IS **PARTIAL**, AND IT IS NOT BACK-DATED
>
> **jack-ryan's Gate-1 landed while I was mid-execution**, and its amendment **A-1**
> requires the E-0/E-1 section to be written **before the first cathedral capture**, adding:
> *"If a cathedral arm has already been captured, state that in the note and mark the
> pre-registration as partial rather than back-dating it."*
>
> **Cathedral and arena arms were already captured when A-1 landed.** So, stated plainly:
>
> - **NOT pre-registered:** the expected structured-content fraction and the refutation
>   margin. Both were derived from the captures. **§ 1.5's adequacy verdict was therefore
>   authored after its result was known, which is exactly the cost A-1 names.** I do not get
>   to claim otherwise, and the mitigation is § 1.8 — the three A-2 sensitivity proofs,
>   which are *falsifiable after the fact* in a way a prediction is not.
> - **Genuinely pre-registered**, because they were authored into `s2_stage_env.gd` and
>   `s2b_e1_gate.py` **before any structured arm rendered**: the **two-cohort C-3 partition**
>   (never pooled), the derive-don't-declare rule for stage geometry, and the
>   omit-the-hero-VFX policy with its three stated reasons.
> - **Amendment A-7 also landed after I had already committed and pushed the
>   `stock_vfx_enabled` flip inside this tranche's tag.** Disclosed in § 5.

---

## 0 · Pre-execution refutation surface

The dispatch names seven refutation conditions. Three are evaluable now; four are
row-scoped and cannot be evaluated before the rows exist.

| # | Refutation condition | Applies? | Disposition |
|---:|---|---|---|
| 1 | Cathedral stage does not materially raise structured-content fraction ⇒ E-0 has not done its job | **NO — but not cleanly.** | Structured content rises **0.304 % → 23.440 %** (cathedral, **77.1×**) and **→ 45.111 %** (arena, **148.4×**). The stated test passes decisively. **A DIFFERENT failure was found instead and is § 1.4.** |
| 2 | Two rows converge in authoring | row-scoped | Not evaluable pre-mint. |
| 3 | A "must NOT" clause cannot be honored without unreadability | row-scoped | Not evaluable pre-mint. |
| 4 | Acceptance criteria pass without the effect reading as its archetype | row-scoped | Not mine to judge (galadriel's). |
| 5 | Building to T-A requires reopening a § 1 design-law ruling | **NO** | Nothing in E-0/E-1 touched a § 1 ruling. No HALT to Matt. |
| 6 | **Seven rows prove too large to hold a consistent instrument across — use the circuit-breaker** | **⚑ FIRES, EARLY** | **§ 7.** Three new defects of the tranche-1 class surfaced during E-0/E-1, one of them in a LANDED MINT. |
| 7 | A scaffold value ships without a Discipline #40 declaration | **NO** | § 5 is the register. |

---

## 1 · E-0 — THE STAGE FIX, AND THE HONEST ANSWER TO "DOES IT FIX THE S AXIS"

### 1.1 The instrument was calibrated before it was believed

A reimplementation of somebody else's metric that has never been checked against their
published numbers is a plausible number. So `scripts/s2b_stagemetrics.py` ports HLF
**verbatim** from galadriel's `register-metrics.mjs` (960-px-wide resize → grayscale →
% px with luma > 204) and then re-measures **her own anchor captures**, which are still
on disk:

| anchor corpus | n | published HLF | my HLF (max over lifecycle) | reproduces? |
|---|---:|---:|---:|---|
| `11_lift_capture_*` (register-2 graybox) | 100 | **14.4 %** | **14.342 %** | ✅ |
| `12_cathedral_capture_*` (register-2 cathedral) | 100 | **9.35 %** | **9.451 %** | ✅ |

**My HLF is her HLF**, to within 0.06 pp on both anchors. And the calibration returned a
fact neither of us had stated: **the published anchors are lifecycle MAXIMA, not means.**
The cathedral corpus means 7.41 %, the graybox 9.59 %. Comparing a mean against them
would have understated every stage by ~2 pp.

### 1.1a ⚑ AND THE GRADIENT OPERATOR WAS WRONG — CAUGHT BY GATE-1, NOT BY ME

My first pass swept the operator against galadriel's **0.218 % / 4,514 px**, landed on
`sobel@10 = 0.2699 %`, and **declared a 1.24× offset**. Gate-1 **A-2(ii)**, carrying
galadriel's **Amendment G-4**, corrects the target:

> *"the correct target is **0.304 %, Sobel |∇| > 10, § 1.9a**. Both figures are real and
> measure the same frame with different operators; § 2.0's is forward-difference and has no
> cathedral counterpart, so it cannot found the instrument while the bars are
> Sobel-denominated. ... **a known value restated without its operator is not a known
> value.**"*

Re-swept against the correct target, the divisor is **decided rather than chosen**:

| Sobel normalisation | bare stage |
|---|---:|
| **raw (none)** | **0.3038 %** ← reproduces **0.304 %** |
| ÷2 | 0.2914 % |
| **÷4 (what I shipped first)** | **0.2699 %** |
| ÷8 | 0.2247 % |

**This is a FOURTH instance of this tranche's own hazard, inside my own instrument.**
0.2699 % is a perfectly plausible number that matched **neither** published operator — and
*declaring an offset made the mismatch look handled.* The operator of record is now named
in full: **3×3 Sobel, unnormalised, ITU-R 601-2 luma, full frame resolution, |∇| > 10.**

**Every structured-content and GLF number below is re-derived on it.**

### 1.2 ⚑ THE 9.35 % ANCHOR IS ~80 % HERO VFX, AND THAT CHANGES WHAT IT IS AN ANCHOR *FOR*

The cathedral corpus is a scripted lifecycle: braziers burn from frame 0, the pentagram
charges at sim-frame 30 and the fire column erupts at 52, stopping at 320. Measuring HLF
*along* that lifecycle decomposes the anchor:

| window | frames | HLF |
|---|---|---:|
| pre-ignition — **stage + braziers only** | 1–8 | **1.71 – 2.50 %** |
| hero burn — **the published anchor** | 9–80 | **6.32 – 9.45 %** |
| post-stop settle | 90–100 | 2.84 – 3.96 % |

**Roughly 7 of the anchor's 9.35 points are the fire column.** The room contributes
~1.7–2.5, and *that* is set-dressing flame too, not architecture. The boss-arena corpus
decomposes the same way (pre-ignition 0.36–0.56 %, peak 4.12 %).

So "9.35 % cathedral" is **not a statement about a stage**. It is a statement about a
stage *carrying a set-dressing-scale HDR fire pillar* — and a gate stage must not carry
one, because it is a non-authored emitter (galadriel HALT 1/2) and non-deterministic
(method defect #2). Expecting a 2,036 px weapon ribbon to reach it is a category error.

### 1.3 What was built

`scripts/s2_stage_env.gd` — one builder, three recipes, so a row cannot be staged
differently by accident and the cohort label travels with the geometry that produced it.

- **`bare`** — the tranche-1 stage, moved **verbatim**, not rewritten. Re-lighting it
  would have converted E-1 from a re-capture into a re-mint.
- **`cathedral`** — the ordered recipe. Pack geometry + the lift rig transferred 1:1 from
  `dark_fantasy_cathedral.tscn`.
- **`arena`** — see § 1.4.

Three derivations replaced three declarations, and each replaced one because the
declaration was wrong or unsafe:

1. **Arena centre.** `render_cathedral.gd` hand-copies `(0.06, 0.508, −32.15)` into a
   comment. Taken at face value the stage framed the caster **on a terrain outcrop**. The
   builder now reads the largest `Ritual_Circle` mesh's AABB off the live scene. *(XZ was
   right to 0.000 m; the Y was off by 1.085 m.)*
2. **Floor height** — derived from meshes whose footprint contains the arena centre, not
   assumed from a prop origin.
3. **Off-stage cull** — `Demo_Cathedral_01.tscn` is a six-section **showcase diorama**,
   not a room, and `render_cathedral.gd` hid two sections by name. I could have extended
   that hand-list to four names. I did not: galadriel accepted the tranche-1 C-8
   declaration *"specifically because it was derived by ancestry rather than hand-listed"*,
   and a section name-list is the same enumeration-in-place-of-a-rule. **The rule is "the
   stage is what the camera frames"** — a 26 m radius derived from the ratified camera's
   ~24.7 × 44.0 m footprint. It culled **6,561 meshes and kept 834**, and it will keep
   working the day the pack ships a seventh section.

**C-8 on the new geometry:** the pack cathedral ships **zero particle emitters** and
**29 OmniLights, of which 1** survives the arena-radius filter. The arena recipe carries
**4** static brazier OmniLights. All are `INHERITED-BY-DESIGN`, enumerated by
`s2a_census.gd` at every mark, and shipped inside the `C8_DECLARATION` block alongside the
row. **The lift recipe's own hero VFX are omitted and the omission is declared**, for the
three reasons in § 1.2.

### 1.4 ⚑ THE MEASUREMENT SAID TO BUILD A THIRD RECIPE, SO I DID

E-0 ordered the cathedral wired in **and measured**. Wired in, it passes the stated test
(0.304 % → 23.440 %). Measured, it fails a test nobody had thought to state:

> **`Demo_Cathedral_01.tscn` is not a room.** Its `Ritual_Circle` marker sits on an
> **outdoor terrace at a cliff edge**. Framed from the ratified combat camera (27.85 m up,
> 34 m back) the caster stands correctly at frame centre **on a rock outcrop**, with the
> nave up-and-right and terrain filling the foreground. **The terrain then occludes 81 %
> of `melee_strike`'s authored pixels** — 13,802 on the arena, **2,589** on the cathedral,
> a ratio of **0.188**.

Shipping only the ordered stage would have honored the letter of E-0 against its purpose.
So `arena` is the same pack and the same lift rig in **a room the camera can photograph** —
lifted from `render_boss_arena.gd`, which already builds one at register-2 parity and which
galadriel's corpus already carries 100 captures of. Changed: sized from **our camera's
footprint** rather than the sim's 30×30; centred on the origin so the room comes to the
actors; **two pillar rings at 7.5 m and 13.0 m**, because galadriel asked literally for
*"walls, arches and pillars for VFX light to fall on"* and a 20 m-distant wall catches
nothing from a 2 m crescent. 320 floor tiles, 72 walls, 20 pillars, 4 braziers, 4 skull
piles. No flame particles.

### 1.5 ⚑ HLF DOES NOT SURVIVE THE FIX — AND THE REASON IS NOT GEOMETRY

**This is the number knight-rider asked for, and it is a "no".**

| stage | structured content | vs bare | HLF (control) | HLF (effect ON) | max luma, effect ON |
|---|---:|---:|---:|---:|---:|
| **bare** | **0.304 %** | — | 0.0015 % | 0.0064 % | **242** |
| **arena** | **45.111 %** | **148.4×** | 0.0000 % | **0.0000 %** | **195** |
| **cathedral** | **23.440 %** | **77.1×** | 0.0000 % | **0.0000 %** | **193** |

The HLF cut is a **cliff at luma 204**, and on both structured cohorts the effect peaks at
193–195 — *below it*. And lowering the cut does not rescue it, which is what proves the
problem is not a threshold choice:

| cut | bare | arena |
|---:|---:|---:|
| >204 | 0.0064 % | 0.0000 % |
| >180 | 0.0326 % | 0.0008 % |
| >150 | 0.0779 % | 0.0156 % |
| >120 | 0.1256 % | 0.0938 % |

**At every cut the structured stage reads LOWER than the bare one.** The lift env's filmic
tonemap (exposure 0.95, white 8.0), raised contrast and fog attenuate the same effect from
242 down to 195. So the two cohorts sit on **different transfer functions**, and HLF is
non-comparable *across* them — a sharper version of galadriel's § 1.9 finding, in a
direction nobody had named: not stage-vs-stage but **tonemap-vs-tonemap**.

**Verdict: the stage fix does NOT make HLF comparable, and no amount of stage work will.
HLF asks "is this frame bright". The S axis needs "does the effect's light fall on the
room."**

### 1.6 GLF — the instrument E-0 actually produced

The question galadriel's own § 1.9 wording asks is measurable, and it was **unaskable on a
bare stage because there was no room to fall on.** `GLF` = of the effect's authored pixels,
the fraction landing where the **control frame** carries environment geometry (∇ > 10,
dilated by 1). The control decides what counts as structure, so an effect cannot
manufacture its own denominator.

| row (peak mark) | **bare** | **arena** | **cathedral** |
|---|---:|---:|---:|
| `melee_strike` @ swing | **0.034** | — | — |
| `melee_strike` @ contact | **0.194** | **0.676** | 0.515 |
| `ground_targeted_circle` @ impact | — | **0.717** | 0.250 |
| `aura` @ steady | **0.114** | **0.700** | 0.279 |
| `whirlwind` @ sustain | — | **0.835** | 0.712 |

**On the arena stage 68–84 % of every effect's light lands on environment geometry. On the
bare stage it is 3–19 %, and even that is the ACTORS' OWN SILHOUETTES — the only structure
a bare floor has.** `aura` separates **0.114 → 0.700 (6.1×)** and `melee_strike` at contact
**0.194 → 0.676 (3.5×)**. That is the axis the S score has been missing.

**Recommendation to galadriel and knight-rider: score S on GLF + mean added luma on
structure, against the `arena` cohort. Report HLF, mark it non-comparable, and stop
comparing it to 9.35 %** — § 1.2 shows that number was never measuring what it was being
asked to measure.

### 1.7 C-3 uniformity — per cohort, never pooled, and the finer cohort is the real one

Pooled across all 76 arms: arena spread **0.8716**, cathedral **2.4192**. Neither is
tranche 1's 0.000 — and pooling is why.

A bare floor is a *constant*: one albedo, one plane, no occluders. A pack stone floor under
pillar shadows is not, and the four rows place their actors differently, so a screen-fixed
band samples different shadowing per row. **Pooling measures the roster.** The question
galadriel's check exists to answer — *does any ARM diverge from its siblings* — lives per
row:

| cohort | `melee` (18) | `gtc` (16) | `aura` (12) | `whirlwind` (30) |
|---|---:|---:|---:|---:|
| **arena** | **0.0000** | **0.0000** | **0.0000** | 0.8716 |
| **cathedral** | **0.0000** | **0.0000** | **0.0000** | 2.4192 |

**Three of four rows reproduce galadriel's 0.000 receipt exactly, on both new stages.**
The whirlwind's spread is not albedo divergence — that stage **moves the caster at 3.5 m/s
from t = 2.20**, dragging its shadow through the sample band. An archetype property, named.


### 1.8 ⚑ A-2 SENSITIVITY PROOFS — the instruments are tested, not believed

Gate-1 **A-2** is binding and it is the amendment that carries the tranche:

> *"The claim 'the instruments now exist and are proven' is true of tranche 1's instruments
> and **FALSE of this tranche's**. ... Each gets a **known-negative that must move the
> number**."*

with Discipline #75 cl. 2 as the standard: *"all five probes were checked, in the sense
that their authors read them and believed them; four of five returned values in a plausible
range, **which is what suppressed the check**."*

Three of A-2's five instruments were exercised by E-0/E-1. Receipts in
`harness_logs/s2b_e1_2026-08-24/sensitivity.json` (`scripts/s2b_sensitivity.py`):

| # | Instrument | Known-negative | Result | |
|---|---|---|---|:--:|
| **ii** | structured-content derivation | reproduce **0.304 %** on the bare stage, **naming the operator** | **0.3038 %**, error **0.0002**; divisor decided by sweep, not chosen | ✅ |
| **i** | cathedral / arena stage | stage number must **not depend on the effect**, and must differ from bare by the margin | effect contributes **+0.037 to +0.603 pp** against stage content of 23–45 pp (**0.16–2.6 %**); bare→stage **77.1× / 148.4×** | ✅ |
| **iii** | CIEDE2000 (replacing hue angle) | **both legs** — known-identical → ≈ 0 **and** known-different → large | identical **ΔE = 0.0000**; different (`fire\|water`) **ΔE = 18.70** | ✅ |

**On (iii) I did not compare a file with itself**, which would prove only that subtraction
works. The known-identical pair is **`gtc_fire_descend` vs `gtc_fire_erupt` at `03-impact`
— two different arms of a pre-registered RT-8 parameter** that galadriel independently
found render **byte-identical** at 7 of 8 marks. A negative control produced by *the whole
pipeline*, not by the arithmetic.

**On (i) I did not claim exact equality**, which would have been the flattering answer and
is also false: an effect genuinely adds edges of its own. The honest bar is that the stage
number is **dominated by the stage**, and it is, by a factor of ~40–600.

**And (ii) is the proof that earned its cost** — it is the leg that caught § 1.1a. Without
it, `0.2699 %` ships, looks reasonable, and is measured in units nobody owns.

**A-2's items (iv) C-2 yaw assert and (v) cross-row separation, and the two instrument
fixes, are NOT proven here** — they belong to rows that are not started. Under **A-3** those
seven receipts are the scheduled checkpoint that replaces the circuit-breaker; **three are
now banked, four are owed before rows 3–7.**

### 1.9 ⚑ A-6 ANTI-TUNING CLAUSE, RECORDED BEFORE ANY ROW IS MEASURED

A-6 requires this said in the mint note *before* the cross-row separation is measured, and
it is said here so it cannot be added afterwards:

> **A negative cross-row separation result is a FINDING ROUTED TO GANDALF ABOUT L-29's FOLD.
> It is NOT a licence to differentiate the effects until the number passes.** A threshold on
> an acceptance criterion creates pressure to author artificial distinctness, which would
> corrupt the archetype semantics T-A locked. § 75.5 cl. 5.6 inverted: **do not change the
> artifact to suit the instrument.**

The same clause already governed E-0/E-1 in practice: `melee_strike` loses 81 % of its
authored pixels on the cathedral stage (§ 1.4) and **no effect was retuned to recover it** —
the stage was indicted instead, which is where the fault was.

---

## 2 · E-1 — the four minted rows, RE-CAPTURED

Re-captured on both structured stages: `melee_strike`, `ground_targeted_circle`, `aura`
(via `s2a_stage.gd --stage=`) and `whirlwind` (via `wwcr_stage.gd --stage=`). 152 PNG.

**Each row gets `fx=on` AND `fx=novfx` per stage, not the one arm the dispatch allows.**
For a *look* one arm suffices; for a *measurement* it does not, because every number here
is a difference against a matched control and tranche-1 method defect #3 was precisely a
ratio missing a control on one side (6.383 → 0.998 once rebuilt). The marginal cost is one
render; the alternative is a number with one leg.

### 2.1 The receipt that this is a re-capture and not a re-mint

Fixing the control defect in § 3.1 required editing `s2a_ground_circle.gd`. So the claim
"nothing about these effects changed" is **verified, not asserted**: all `fx=on` arms were
re-rendered across the edit and compared byte-for-byte.

> **46 of 46 `melee` / `gtc` / `aura` fx-on frames: BYTE-IDENTICAL. Zero differing pixels.**

*(The `whirlwind` fx-on frames were **not** identical, and that is § 3.2.)*

### 2.2 R-axis delta against structured geometry — surfaced, not tuned

| row | authored px, arena | authored px, cathedral | ratio |
|---|---:|---:|---:|
| `melee_strike` | 13,802 | 2,589 | **0.188** |
| `ground_targeted_circle` | 88,761 | 83,221 | 0.938 |
| `aura` | 23,621 | 21,860 | 0.925 |
| `whirlwind` | 6,452 | 5,773 | 0.895 |

Against the **arena** stage, three of four rows hold 89–94 % of their bare-stage
readability, and mean added luminance on structure sits at 28–30 — **the effects survive
structured geometry.** galadriel's § 2.0 anticipated that an additive effect with
near-perfect contrast *by construction* might not; measured, it largely does.

The `melee_strike` 0.188 outlier is **the cathedral stage's terrain occluding the effect**,
not the effect failing (its arena figure is 13,802 vs the bare stage's 12,076 — it gains).
**No effect was tuned to rescue any number.**

---

## 3 · ⚑ THREE NEW DEFECTS OF THE TRANCHE-1 CLASS, FOUND IN E-0/E-1

Each produced a **plausible number before it produced a correct one**. That is the
signature the dispatch turned into standing pre-flights, and it is why § 7 stops here.

### 3.1 `s2a_ground_circle.fire()` un-stripped its own control ⇒ `authored_px = 0`

The stage strips a control by setting `gc.visible = false` at **build** time. `fire()` set
`visible = true` at **run** time. Result: `e1_arena_gtc_ctl_*` and `e1_arena_gtc_fx_*` came
out **byte-identical**, and the gate reported **`authored_px = 0`** — which reads
perfectly plausibly as *"the circle is invisible against structured geometry"*, an R-axis
finding, and is nothing of the kind. **The control was contaminated with the effect.**

**This is tranche-1 method defect #1 through a third door: I inspected the flag I set
rather than the state that ships.** It never fired before because tranche 1 had **no
novfx arm on this row** — its RT-8 parameters were matched against *each other*, so nothing
ever asked this effect to be absent. E-1 is the first arm that did.

**Fixed** (`suppress_vfx()`), with the byte-identity receipt in § 2.1. gtc's true figure is
**88,761** authored px.

### 3.2 ⚑ `wwcr_stage.gd` NEVER RECEIVED THE TRANCHE-1 CLOCK PIN — AND IT AFFECTS A LANDED MINT

Two runs of **identical, unmodified** code produced frames differing by **144–1,028 lit px**
(threshold 12, max channel delta 241) — **including at `00-pre`**, before the channel
begins, so it is not the effect drifting.

`s2a_stage.gd` pins every `AnimationPlayer` to the stage clock. **`wwcr_stage.gd` did not.**
The rig and mob `AnimationPlayer`s ran on real frame time while the whirlwind was stepped
at a fixed 1/60 s. **That is tranche-1 method defect #2 exactly** — *"a control must control
everything that moves"* — and the drift is the same order of magnitude as the 404–573 px
that were entirely animation phase in tranche 1.

I found that defect, fixed it in the file where I found it, wrote it up as a standing
pre-flight, **and left its sibling alone.** A discipline applied only where it was
discovered has been *described*, not adopted.

**Back-ported. Verified: 0 differing pixels across two independent runs, on all 10 marks.**

> **⚑ CONSEQUENCE BEYOND MY SEAM, AND NOT MINE TO RULE ON.** The `whirlwind` clean-room mint
> (tag `drax/v0.1-s2-whirlwind-cleanroom-1`, godot `1692d6e`) was captured on this stage
> **before this fix**. Its ON/OFF diffs carry animation phase. **Whether that moves the
> WW-AB verdict is galadriel's call.** Routed to knight-rider.

### 3.3 The `wwcr` novfx control is not pose-matched before `T_BEGIN`

`00-pre` (t = 0.20, before the channel starts) diffs **83 px**, mean added **−6.1** (the fx
arm is *darker*), tight to the caster. A small silhouette difference from the whirlwind
re-seating the blade at bind time.

**Reported, not fixed.** Repairing it reaches inside a minted effect's rest/bind behaviour,
which E-1 forbids. `melee` and `gtc` both return **exactly 0**; `whirlwind` does not, and
the failing receipt ships as a failing receipt.

### 3.4 And a fourth, in my own instrument, in the opposite direction

My first gate table set each row's determinism `post` mark to its **last** mark, returning
`gtc 07-late = 56,984` and `ww 09-off = 3,973`. I was briefly willing to read those as the
new stages breaking determinism. **They are the archetypes' specified residue** — gtc's
persists to ~3.54 s (bbox x[783–1377] y[431–827], a ring at both cast sites); whirlwind's
is its neutral never-tinted scuff layer. Localising the pixels is what settled it.

**A plausible number can be a FALSE ALARM as well as a false pass**, and this one would have
sent me hunting a defect that does not exist. `post` now means *"a mark at which the
archetype is specified to have returned to zero"*, and where there is none the receipt is
**N/A with its reason** rather than a `false` that misrepresents an archetype property as
an instrument fault.

---

## 4 · RT-2 RE-MEASURED ON CIEDE2000 — MY TRANCHE-1 FINDING IS REFUTED

galadriel's § 1.3 rules hue-angle inadmissible: hue is undefined at zero chroma and
`neutral` renders at C\* = 2.83. Her sharper point is the one that lands:

> *"He was computing a perceptual colour difference and labelling it as hue degrees. His
> instrument was closer to right than his units; **the label** is what made `neutral|wind`
> look like a 3-degree catastrophe."*

Re-derived independently (`scripts/s2b_rt2_ciede.py`), on rendered pixels, across four
marks, on **two mask definitions** because the authored mask is element-dependent:

| pair | ΔE2000 @ swing | ΔE2000 @ contact | ΔE added | transfer ratio |
|---|---:|---:|---:|---:|
| **`fire\|earth`** | **7.28** | **6.50** | 7.83 | 0.829 |
| `neutral\|water` | 12.19 | 7.35 | 8.74 | 0.842 |
| `neutral\|wind` | 8.97 | 7.92 | 8.75 | 0.905 |
| `fire\|water` | — | 18.70 | 20.57 | 0.909 |

- **`fire|earth` is the minimum on every one of the four marks**, and **mask choice never
  moves it**. **My `neutral|wind` "3.0°" is refuted** — it is third.
- **Third independent measurement, same verdict.** galadriel got 7.38; I get **7.27–7.28 at
  the swing marks** (agreeing with her to 0.1) **and 6.50–6.54 at the contact marks**.
- ⚑ **New, and it sharpens routed finding #2 for rocket: the collapse is TIGHTEST AT
  CONTACT** — the instant the effect is largest, brightest, and the player is looking. The
  published 7.38 is the *trail*; the moment that matters reads **6.50**.
- **`neutral|water` at 7.35 is absent from both prior matrices** and is tighter than
  `neutral|wind`.
- **Fork test (§ 1.3): transfer ratio spans 0.805–1.053, mean |transfer| 1.66 ΔE. No
  systematic compression ⇒ FAITHFUL TRANSMITTER. RT-2 does NOT fire. The surface class is
  exonerated; the PALETTE is indicted. Routes to rocket (X-3).**

---

## 5 · `KingRig.stock_vfx_enabled` — flipped, with the opt-in surface DERIVED

knight-rider's ruling executed: **default `true` → `false`**, presentation scenes opt in.

His condition was *"if the opt-in surface turns out to be materially larger than a handful
of scenes, stop and tell me."* Derived rather than estimated: **14 files reference
`KingRig`; 8 construct one.**

- **Opt in (7, all presentation):** `playshell.gd` (the surface a player sees) +
  `shoot_king_closeup` / `shoot_king_head_refine` / `shoot_king_sword_refine` /
  `shoot_king_sword_grip` / `shoot_sword_fix` / `shoot_sword_sweep` (beauty-shot renderers
  whose entire purpose is to photograph the rig as it presents — the decorative VFX are
  *signal* there).
- **Take the new default (7):** gate stages and geometry probes. Which is the point.

**Seven against an estimate of four — a handful, not materially larger.** The arithmetic he
described holds and the flip proceeds; **the count is reported rather than rounded to the
estimate it was checked against.** All 12 edited scripts parse clean.

### ⚑ A-7 — I SHIPPED THIS INSIDE THIS TRANCHE'S TAG, AND GATE-1 SAYS IT SHOULD NOT BE

Amendment **A-7** landed **after** I had committed and pushed. It rules the flip **out of
this dispatch's scope and tag**, for two reasons I accept:

> *"(a) it is not load-bearing for this tranche — tranche 1 already achieved
> `non_authored_emitter_count: 0` on **21/21 arms with the default still `true`**, via the
> declarative export, so the confound is already controlled; (b) it changes scenes **none of
> the seven rows exercise**, so it would ship untested inside a tag whose gate measures VFX
> mint quality — one tag, two unrelated changes, one receipt."*

**Both are correct and the flip is in `drax/v0.1-s2b-e0-stage-fix` anyway.** Stated rather
than tidied away. I have **not** deleted or moved the pushed tag — that is destructive and
not mine to do unasked — so **whether to revert-and-reland as its own change is
knight-rider's call.** Reverting would not clean the existing tag either; it would only add
churn. **The disclosure is the honest remedy available to me.**

**A-7's substantive requirement WAS met**, and it is the part that mattered: *"as written it
is a bare hand-list ... a threshold with no derivation, which makes the escape hatch
undecidable"* (#76 cl. 1). The set is now **derived mechanically** by
`scripts/s2b_kingrig_optin_derive.sh`, with a **stated governing predicate**:

> a construction site **opts in** iff the scene exists to **photograph or play** the rig as
> it presents; it **takes the new default** iff the scene exists to **measure** something,
> in which case the stock VFX are a confound.

Derived result: **15 construction sites — 7 opt in, 1 sets `false` explicitly, 7 take the
new default.** That predicate is what makes knight-rider's own *"materially larger than a
handful"* condition decidable for the first time.

### Discipline #40 register — E-0/E-1

| Value | Class | Basis |
|---|---|---|
| `STAGE_RADIUS_M = 26.0` | **A — AUTHORED** | Derived from the ratified camera's ~24.7 × 44.0 m footprint; a rule, not a hand-list. |
| `CEILING_CUT_M = 7.5` | **A — SCAFFOLD** | Roof cull for an interior shot at a 27.85 m camera. Standard 2.5D solve; count declared (283–288 meshes). |
| `LIGHT_KEEP_RADIUS_M = 18.0` | **A — SCAFFOLD** | Carried from `render_cathedral.gd`'s 16 m, widened to the stage radius' neighbourhood. |
| `A_W/A_D = 40 × 50 m` | **A — AUTHORED** | Camera footprint + margin, in whole 2.5 m modules. |
| `A_RING_INNER/OUTER = 7.5 / 13.0 m` | **A — SCAFFOLD-WITH-PENDING-DECISION** | Pillar rings placed outside this tranche's largest row footprint (~4 m). **Not ratified by anything.** If a T2/T3 row reaches further, this moves. |
| `C3_BOX = (140,840,520,1010)` | **A — AUTHORED** | Ground band away from caster and every footprint; fixed in screen space so the same region is interrogated in every arm. |
| `stock_vfx_enabled = false` | **A — AUTHORED** | § 5. Supersedes the Class-R default that existed only to preserve prior behaviour. |
| `sobel@10` structured operator | **R — REPLICATED** | Chosen by sweep against galadriel's published 0.218 %; offset (1.24×) declared. |
| lift env / key / rim / fill | **R — REPLICATED** | Transferred 1:1 from `dark_fantasy_cathedral.tscn`. |
| `arena` recipe geometry | **R — REPLICATED** | Modules, placement grammar and lift rig from `render_boss_arena.gd`. |

---

## 6 · ROWS 1 AND 2 — MINTED

**Tag:** `drax/v0.1-s2b-rows-1-2` (`7960304`). **Receipts:**
`harness_logs/s2b_rows12_2026-08-24/{gate.json,selfbuff_vs_aura.json,render.txt,arm_cost.txt}`.
**Rows 3–7 remain NOT STARTED** — see § 6.9.

> ### ⚑ A-1, DONE PROPERLY THIS TIME
> § 1's pre-registration was **PARTIAL** and I said so: the E-0 adequacy verdict was
> authored after its result was known. That is not repairable retroactively. It **is**
> avoidable prospectively, so **every bar rows 1–2 are judged against was committed at
> `6dbe19f` before a single frame of the scored corpus had been read** — the effect
> code, the capture script and the gate, with no output. **Pre-registration you can check
> with `git log` beats pre-registration you assert.**

### 6.0 Determinism — and a pre-flight that does NOT apply, said rather than faked

Tranche-1's third pre-flight is *"`00-pre`/`08-post` must diff to exactly 0 with the
effect disabled."* **It does not apply to `totem`.** The delegate **manifests** and its
**arm moves** in the `novfx` arm too, because a control that deleted the body would
measure the body — the defect the whirlwind gate hit from the other direction. A
`00-pre`/`08-post` zero is impossible here and claiming one would be false.

**Substituted the stronger check I happened to have.** The corpus was captured **twice**
end-to-end (the first pass exposed a mark-placement defect, § 6.4). Comparing the two:

| cohort | frames | byte-identical |
|---|---:|---:|
| row 1 `self_buff`, marks unchanged | 108 | **108** |
| row 2 `totem`, marks changed between passes | 150 | **150** |
| **total** | **258** | **258** |

Two independent full runs, both stages, both rows, **zero drift**.

---

### 6.1 ROW 1 — `self_buff` (§ 3.1.3) · FIELD-CARRIED · `magical-cause` · `sustained`

**Scope:** `buff-decal` sub-shape **only**. `transformation` is out **by ruling** —
L-29(8) leaves the split deliberately unexecuted, and the two sub-shapes make **opposite
demands on one property**: a transformation *replaces* the silhouette, a decal *must not
touch it*. Matt's deserving list § 5 Class-A item 2.

| item | value |
|---|---|
| **Layers → nodes** | (a) floor decal = `Decal` (soft-radial plane) + `DecalRing` (`ImmediateMesh`); (b) body-adjacent emitters = `MotePool`, 9 billboards |
| **Takes the tint** | decal · ring · motes — **3 kinds, hue only** |
| **Must NOT move** | radius, alpha, count, size. `set_element()` re-applies the alpha **constants** rather than reading alpha off the incoming colour, so a palette entry cannot leak an opacity change in through the tint path |
| **Lifecycle** | `sustained`, constant intensity. **Windup N is spec-faithful** (3 of 4 candidates, a coherent `motion_signature_attested = NULL`) — **not invented** |
| **Elements** | fire / water / earth / wind. `neutral` deliberately absent — § 4.2.3's element-agnosticism argument is about *physical weapon strikes*; a `self_buff` is a magical state and its pool carries element |
| **RT-2** | **n/a** (A-4) |

**⚑ THE GOVERNING PROPERTY — *does not obscure the character* — MEASURED AT UNITY.**

| stage | trail px inside buff | trail px without buff | **retention** |
|---|---:|---:|---:|
| cathedral | 3,467 | 3,424 | **1.0126** |
| arena | 16,376 | 16,412 | **0.9978** |

Four matched arms (`on` / `trailoff` / `control` / `ctrloff`), because a retention ratio
has a numerator **and** a denominator and each needs its own control — the two-arm
version of this measurement returned **6.38** on `aura` and was wrong. **112 skills, the
largest occlusion risk in T-A, and a tranche-1 `melee_strike` staged on top is as
readable inside the buff as outside it on both stages.**

**C-5:** 4,191–4,567 px = **0.22 % coverage**, above our own 535 px `p_trail` floor and
far below the 67 % `x_attr` ceiling. A `sustained` effect lives closest to the ceiling
*because it is on during everything else*; 0.22 % is the ceiling solve.

**Tier-1 — the pass shape is coverage HELD and hue MOVED, and both halves are measured:**

| stage | coverage spread | min mask Jaccard | min hue sep |
|---|---:|---:|---:|
| cathedral | 0.0789 | 0.8984 | **15.77°** |
| arena | 0.0689 | 0.9330 | **14.24°** |

Jaccard as well as area, because **equal area is not equal coverage** — two masks of the
same size over different pixels would pass an area test and fail the claim.

**The INVERTED contact test (anti-tamper):** step **0.0009** / **0.0085** against a 0.05
bar. `magical-cause` is correct here and adding a contact response would score better on
a criterion that does not live on this row — **in the direction that looks like
diligence**, on the row the rubric calibrates against.

### 6.2 ⚑ Row 1's sweep reproduces receipt (v) — independently, on a new instrument

Coverage invariance vs mask floor, cathedral:

| floor | 2 | **4** | 6 | 8 | 12 | 16 |
|---|---:|---:|---:|---:|---:|---:|
| spread | 0.1311 | **0.0789** | 0.0834 | 0.1096 | **0.1765** | 0.2241 |
| min Jaccard | 0.8194 | **0.8984** | 0.8775 | 0.8608 | **0.8275** | 0.7923 |

**At `sa_gate.py`'s inherited 12 this row reports a materially worse invariance —
manufactured by the threshold.** Same finding as receipt (v), second instrument, new row,
arrived at without looking for it.

⚑ **And note the shape, because it is the counterpart to R-4's result:** this objective
has a **genuine interior optimum** at floor 4. The yaw instrument's was **monotone** and
its argmin was wherever the ladder stopped. **Three instruments now: two with real
optima, one degenerate. The transferable lesson is not "erosion is bad" — it is that the
sweep has to be LOOKED AT, because the same constant behaves in opposite ways in
instruments built in the same batch.**

### 6.3 Cross-row: `self_buff` vs `aura` — asked for by nobody, owed anyway

Both are caster-centred sustained fields, adjacent in L-29, and `aura` is already minted.
That is the rows-4/6/7 fold-boundary risk **one tranche earlier**, on an instrument that
already exists at zero capture cost. Not measuring it because § 5 did not name it would
be *"the register that stayed empty because nobody opened the file,"* on my own row.

| cohort | separation (min cross-row) | noise (max within-row) | **ratio** |
|---|---:|---:|---:|
| cathedral | 7.2236 | 1.7201 | **4.20×** |
| arena | 7.0557 | 2.7610 | **2.56×** |

**Within-cohort only, never pooled** — receipt (v)'s first run printed `PASS = True` at
1.40× precisely because its two legs straddled the bare/arena cliff. The floor is read
off `xrow.json`'s `floor_chosen`, **not re-picked for this question**; a floor re-chosen
per question is a floor nobody derived. **The anti-tuning clause was committed at
`6dbe19f` before the number existed**, and the separators are **designed** — 1.15 m
footprint vs 3.40 m field, interrupted ring vs continuous radius declaration — **not
adjusted after measuring**.

---

### 6.4 ROW 2 — `totem` (§ 3.1.4) · PAYLOAD-CARRIED (attack only) · two-layered · composite

| item | value |
|---|---|
| **Phases** | `summon` 0.30–0.75 → `delegate-active` → `anticipation` 1.05–1.50 → `impact` 1.50–1.80, repeated at 2.10/2.55. Three disjoint windows, one mark each; the delegate **persists** between them |
| **Layers → nodes** | manifestation (`magical-cause`) = `ManifestSigil` + `ManifestColumn`; delegate = `DelegateScaffold` (**#40 scaffold**); attack (`physical-cause`) = `SlamPayload` + per-body `SlamImpact` |
| **Takes the tint** | `slam_payload` + `slam_impact` — **the attack, and only the attack** |
| **Must NOT take it** | manifest sigil, manifest column, delegate body — **that set IS the P = 4 ceiling** |
| **Lifecycle** | `sustained` presence with `burst` sub-events |
| **Elements** | fire / water / earth on the attack; the **same three** on the manifestation, so the untinted claim **can fail** |
| **RT-2** | **n/a** (A-4) |

**⚑ THE P = 4 CEILING IS PROVEN, NOT ASSERTED.** L-30 says Tier-1 recolours what the
totem *throws*, never what it *is*, and that "P = 4 is that ceiling, not a mark-down."
Rendered as a code invariant **and** as a falsifiable measurement:

| stage | manifest px fire / water / earth | Jaccard | hue sep |
|---|---|---:|---:|
| cathedral | 8,657 / 8,657 / 8,657 | **1.0** | **0.000°** |
| arena | 8,402 / 8,402 / 8,402 | **1.0** | **0.000°** |

**Byte-identical masks.** The Tier-1 path provably cannot reach the manifestation. And
the attack **does** tint: **16.9°–17.1°** minimum separation.

**⚑ THE ANTICIPATION BEAT — the row's selected property, and the only thing in the pool
that teaches it.** Legible at the gameplay camera **0.40 s before the strike**, which is
**2.2× `ground_targeted_circle`'s 0.183 s telegraph**:

| mark | t | to strike | arm raised | changed px | legible |
|---|---:|---:|---:|---:|---|
| `03a-antic-early` | 1.100 | **0.400** | 0.33 | 2,274 | **yes** |
| `03b-antic-mid` | 1.233 | 0.267 | 0.875 | 3,705 | yes |
| `03-anticipation` | 1.333 | 0.167 | 0.998 | 4,140 | yes |

Reported as a **lower bound**: it is already legible at the first mark inside the window.

**It needed a PIXEL leg, and that is the reason the number exists at all.** The beat
lives on the delegate's **body**, a non-emissive scaffold, so it produces **zero authored
pixels** in the `fx`/`novfx` diff every other row is measured by — **the standard
instrument cannot see this row's selected property.** An arm angle read back from the
transform *re-reads the value it just wrote*, which is exactly the defect the C-2 yaw
assert was built on pixels to avoid. Both legs are reported.

**L-19 two-layered, run twice, expecting opposite answers — both correct:**

| layer | 03-anticipation | 04-slam-contact | verdict |
|---|---:|---:|---|
| slam (`physical-cause`) | **0 px** | 3,345 px | **appears at contact from zero** |
| manifestation (`magical-cause`), arm-matched | 8,657 px | 8,657 px | **step exactly 0.000000** |

**Slam discrimination: 4/4 contacts** — two of four bodies per slam, by construction,
because *an archetype whose hit response fires on everything nearby is not a delegate
strike, it is a nova*.

**Discipline #40 — the delegate body is a declared scaffold.** Primitives, shaded,
**deliberately non-emissive**. A Synty rig would have looked better and **misrepresented
the ceiling** — a plausible-looking delegate is how a model-pipeline dependency gets
quietly marked solved — and a *glowing* placeholder would have entered the C-8 census as
an emitter this row does not own, which is the whirlwind-blade defect pre-empted rather
than repeated. Routes to spec § 5 Class-A item 3, **conditional**, model pipeline.

---

### 6.5 ⚑ THREE DEFECTS IN MY OWN GATE — and the first one is a new failure direction

**1. THE GATE CONVICTED A CORRECTLY-AUTHORED EFFECT, AND I WAS ONE STEP FROM ACTING.**

Attack hue separation first read **4.5–4.8°** for `fire|earth`. That reads exactly like
the failure mode this dispatch names by hand — *"highly readable AND had lost its element
tint — additive blown to cream … more dangerous because nothing in the frame
complains."* I had the diagnosis, the prior, and the fix (drop the payload emission).

**It was not that. Zero authored pixels were clipped.** The mask I was measuring at
`04-slam-contact` is **~80 % manifestation** (8,402 of 10,561 px on arena) — **and the
manifestation is untinted BY DESIGN, because it is the P = 4 ceiling.** The separation
was being **diluted by the very invariance the row is built on**. Isolated by set
difference against the per-element manifest arms that already existed, the same frames
give **17°**.

⚑ **This is the mirror image of every other defect this run has caught.** Every one so
far was a plausible number that **flattered**. This was a plausible number that
**convicted** — and the damage would have been permanent and invisible: **a correct
effect detuned until a broken instrument approved of it, with a commit message
explaining how diligent I was being.** A gate is not safe merely because it is strict.

**2. A ratio with a zero denominator, printed as a finite number.** The slam leg reported
`step_frac = 3345.0`, i.e. `(3345 − 0) / max(0, 1)`. **#64 FRAME FORM: a quantity whose
denominator is zero is not a fraction.** Now stated as *"appears at contact from zero,"*
which is the stronger claim anyway.

**3. The manifestation leg's control did not control the arm.** Comparing
`03-anticipation` (arm **raised**) against `04-slam-contact` (arm **at rest**) measures
the arm occluding the column, not the manifestation's response to contact. It returned
**+0.0765**, **passed** the 0.10 bar, and would have shipped as "flat enough." The
arm-matched pair returns **exactly 0**. Same class as tranche 1's un-pinned animation
clock — *a control that failed to control something that moves* — **except this one
passed, which is worse.**

**And a fourth, in the stage wiring rather than the gate:** two of twenty mechanical
`str.replace` edits **silently no-op'd on an indentation mismatch and reported success**
— the A-7 predicate defect one lap later. Both were in the `C8_DECLARATION` key, and
`layer` is an axis the totem run **varies**, so fix-a's own rule would have been breached
**inside the instrument fix-a exists to be.** Caught by verifying **all twenty** edits
against the file instead of the one I happened to notice.

### 6.6 The mark-placement defect that forced the second capture pass

My first mark table sampled the anticipation window **once**, at 0.167 s before the
strike. The lead time derived from it would have been **0.167 s** — **not a property of
the beat, a property of where I put the mark**, against a declared 0.45 s. It would have
been read as the measurement. Three samples now span the window and the headline is the
**earliest mark at which the raise is legible at the camera**, which is what *"the player
must read that the totem is about to act"* actually asks.

### 6.7 Frame-retention insurance

`transfer_function`, camera, seed and module counts travel in `STAGE_META` on **all 34
arms**. **PNGs are not committed** — Synty licence — so retention is **on-disk plus
committed per-arm metadata**. Whether that must survive a machine loss is **Matt's**, at
`canonical/matt_decision_needed/2026-08-24-vfx-frame-retention-vs-synty-licence.md`. **No
workaround built** (KR R-7).

### 6.8 Measured arm cost on STRUCTURED stages

**8.58 s/arm** (n = 34, range 7.49–10.37), vs **4.39** on bare. 34 arms = **292 s**.
**Capture is still not the cost of a row; authoring is** — R-8 stands, and structured
stages roughly double an arm without changing the conclusion.

### 6.9 Rows 3–7 — NOT STARTED

Stage 3. Nothing blocks them: A-2 is discharged (all seven receipts, plus R-3/R-4/R-5),
A-4/A-5/A-6 are folded, the separation instrument is sound, and jack-ryan's pre-declared
Gate-2 BLOCK is satisfied in advance. **Row 3 (`circle`) carries the restored A-10 windup
donor** (D3 · Condemn, `burst`, windup **Y**) and **row 5 (`melee_arc`) judges on the A-5
re-anchored criteria**, not the struck ≈ 12 % figure.

---

## 7 · ⚑ WHY I AM STOPPING HERE — TWO INDEPENDENT REASONS

**1. Gate-1 landed mid-execution, and its amendments re-scope the rows I have not written.**
It is **PASS-WITH-FINDINGS with ten BINDING amendments**, and four of them change what a row
mint must contain before it can start:

- **A-2 + A-3** — the circuit-breaker is **re-specified**, because as written *"it cannot
  fire"*: tranche-1-class defects are silent by construction, so a breaker that depends on
  noticing one *"is an intention, not a control."* It is replaced by a **scheduled receipt
  gate — A-2's seven sensitivity proofs.** **Three are banked (§ 1.8); four are owed**
  (C-2 yaw assert with a deliberately-wrong arm, cross-row separation with its positive
  control, and the two instrument fixes). **Rows 3–7 do not start until all seven are in
  `gate.json`.** If any fails, the cut is **7 → 4**.
- **A-4** — the dispatch **omits the Tier-1 surface class on four of seven rows**, and the
  consequence it missed is that **this tranche's RT-2 population is `melee_arc` +
  `multi_projectile`** — two TRAIL-BOUNDED rows on one palette, which makes the § 1.3 fork
  test **cross-row for the first time**. Not something to discover mid-mint.
- **A-5** — `melee_arc`'s *"reference coverage ≈ 12 %"* is **the one bar galadriel's § 1.6
  ruled non-portable**, and must be re-anchored to angular extent / radial thickness and
  background-structure retention. *(And A-5 notes the interlock that vindicates E-0 going
  first: **"terrain visible THROUGH the arc" is untestable on a 99.78 %-bare floor because
  there is no terrain.**)*
- **A-6** — the cross-row separation threshold must be **derived**, with a null and a
  positive control, plus the anti-tuning clause I have recorded at § 1.9.

Starting Row 1 before these are folded in would mint against a scope Gate-1 has already
amended.

**2. The circuit-breaker condition has fired, and I am using it rather than pushing
through.** The dispatch installs a HALT-and-surface after the first two rows *"if any NEW
instrument defect of the tranche-1 class appears — a measurement that produced a plausible
number before it produced a correct one."* **Four appeared during E-0/E-1 alone** (§§ 3.1, 3.2, 3.4 and — caught by Gate-1 rather
than by me — the wrong gradient operator at § 1.1a), plus a real un-fixed control defect
(§ 3.3) and a hand-copied constant that framed the caster outside the building (§ 1.3).

**§ 3.2 is the one that matters most, and it is why the breaker is worth its cost here:
it is not in new work. It is in a LANDED, GATED MINT.** The instrument that captured
`whirlwind` was missing the exact fix I had already written, documented and elevated to a
standing pre-flight — and nobody, me included, checked whether the sibling stage had it.
Seven rows minted on instruments nobody re-audited is seven rows to re-mint.

**E-0 going first bought exactly this.** All five defects were found on a stage fix and a
re-capture, before a single tranche-2 effect node existed.

---

## 8 · Routed findings

| # | Finding | To | Class |
|---|---|---|---|
| 1 | **`whirlwind`'s clean-room stage was missing the AnimationPlayer clock pin.** Two runs of unmodified code differ by 144–1,028 px. The LANDED WW-AB mint's captures carry animation phase. Fixed forward; the landed verdict is not mine to move. | **galadriel / knight-rider** | **WARN — touches a landed mint** |
| 2 | **The 9.35 % cathedral HLF anchor is ~80 % hero VFX** (pre-ignition 1.71–2.50 %). It is not a stage number and should not be used as one. **HLF is non-comparable ACROSS TONEMAPS**, not merely across stages: the same effect peaks at 242 on the bare env and 195 on the lift env, either side of the 204 cut. | **galadriel** | **Instrument correction** |
| 3 | **Proposed S-axis instrument: GLF** (fraction of authored pixels landing on control-frame geometry) + mean added luma on structure. Separates `aura` 0.114 → 0.700 (6.1×) and `melee_strike`@contact 0.194 → 0.676 (3.5×) between bare and arena. Operationalizes § 1.9's own wording. | **galadriel** | Proposal |
| 4 | **`Demo_Cathedral_01.tscn` is a showcase diorama, not a room.** Its ritual circle is on an outdoor terrace; at the ratified camera terrain occludes 81 % of `melee_strike`. **Recommend the `arena` recipe as the S-axis cohort of record.** | **knight-rider / galadriel** | Recommendation |
| 5 | **RT-2 minimum re-confirmed as `fire\|earth` on a third independent measurement**, and it is **tighter at CONTACT (6.50) than at the trail (7.28)** — the moment the player is looking. `neutral\|water` (7.35) is a fourth pair absent from both prior matrices. My tranche-1 `neutral\|wind` 3.0° is **refuted**. | **rocket (X-3)** | WARN — widens finding #2 |
| 6 | **`s2a_ground_circle.fire()` overrode its own control strip** — the row's novfx control was contaminated for as long as one existed. Fourth exhibit of *"inspect the artifact that ships, not the one you authored"*, and the first where the artifact was a **control**. | **jack-ryan** | Support for the discipline candidate |
| 7 | **The `wwcr` novfx control is not pose-matched before `T_BEGIN`** (83 px at `00-pre`). Reported, not fixed — the repair reaches inside a minted effect. | **knight-rider** | FINDING |
| 8 | **A pooled C-3 uniformity spread cannot mean on a textured stage what it meant on a bare one.** Pooled it measures the roster; per row within cohort, three of four rows return **0.000** on both new stages. | **galadriel** | Method note |

**Not escalated to Matt.** No § 1 design-law ruling required reopening; no sealed binding
moved; the sealed spec was **not** patched — § 8 routes to gandalf via knight-rider, as at
tranche 1.
