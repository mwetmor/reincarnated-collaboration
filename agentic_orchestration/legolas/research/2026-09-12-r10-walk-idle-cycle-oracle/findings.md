# Research — walk & idle cycle anatomy for painted-2D ARPG sprites (R10) + the cycle ORACLE artifacts (R10b) — 2026-09-12

**Mode:** A (analytical). **Commissioner:** gandalf (RUN-CONDUCTOR, Astra burst lane Run C-1).
**Brief:** `agentic_orchestration/gandalf/requests/2026-09-12-legolas-mode-a-walk-idle-cycle-anatomy.md` (R10 + R10b).
**Occasioned by:** Matt's K3 first-loop review — idle chest breathes but head/eyes drift; walk's staff arm rigid, eyes dart frame to frame, head keeps its idle tilt and does not bob/sway with weight transfer.
**Folds into:** SPEC § 6 row **T1** (`gait_oracle.py`, `pose_guide.py`, `visibility_table.py`, `flow_smoothness.py`), the JUDGE/TRANSCRIBE question sets, and the bible.
**Companion:** `sources.json` (same directory). **Reference images (measurement only):** `refs/` with per-file licence sidecars.
**Read but not re-walked, per commission:** `astra_test_01/design/` (HISTORICAL), `burst/runs/`, `burst/briefs/`.

## Grading key (unchanged from R6–R8, 2026-09-11)

| Grade | Meaning |
|---|---|
| **VERIFIED** | Stated in a primary source I read directly, with the numbers/wording quoted. |
| **PRACTITIONER-REPORT** | A real practitioner/production artifact or community-standard practice, published but not measured. |
| **SECONDARY** | Trade-press or community report *about* a primary source I could not open. |
| **UNVERIFIED** | Plausible, named, not evidenced. **Includes my own inference and every derivation below.** |
| **DERIVED** | A number I computed from VERIFIED inputs. The inputs are cited; the arithmetic is mine; the *transfer* to our register is UNVERIFIED. |
| **OBSERVED** | My own first-hand inspection this session. Evidence about *that artifact*, not about the world. |

**Normalisation convention used throughout.** `H` = body height, head-top to sole, in the sprite's own pixels. Where a source gives centimetres I normalise against a **1.70 m** reference stature and say so. Where a source gives a fraction directly I use it. Every `%H` figure below is **peak-to-peak unless marked**.

---

## 0. Summary

1. **⚑ The genre does not author a per-weapon WALK — and two of five shipped ARPGs do not author a player walk at all.** Read from shipped data: Path of Exile has **24 `run_*` clips including `run_staff` and zero `walk` strings**; Torchlight II's player rig has **23 `IDLE_*` including `IDLE_STAFF`, 14 `RUN_*`, and no `WALK`**; Grim Dawn declares a `staff` stance and then points every staff clip at `hero01_sword1h_*`, and shares **one walk file across 7 of 8 stances**; Hades walks only out of combat. **Only Diablo II ships a combat walk, and it ships it on a weapon-invariant beat.** The weapon-carry problem is solved at the *idle* and the *run* everywhere it is solved at all. K3's staff-arm defect is being fought in the one cycle the genre has decided is not worth per-weapon authoring.

2. **The drawn register is deliberately NOT the measured one, and Williams says so in as many words.** *"When we trace off a live action walk… it doesn't work very well… when you trace it accurately, it floats. So we increase the ups and the downs."* This makes a Muybridge-derived amplitude **the right floor and the wrong target** — and it means the K3 "no bob" complaint is the exact failure Williams names. Every amplitude threshold in § 5.4 is therefore asymmetric: a hard floor at roughly the biomechanical value, a soft ceiling well above it.

3. **The real head path IS a figure-8 — and the animation tradition forbids exactly that shape.** Vertical CoM runs at 2 cycles per gait cycle, mediolateral at 1; at Williams' "natural" tempo (≈1.44 m/s) the two amplitudes are **within 2 % of each other (≈2.6 %H)**, so the true path is a near-symmetric 2:1 Lissajous. Ken Harris: *"DON'T MAKE CYCLES OF BODY AND HEAD ACTION IN CIRCLES OR FIGURE 8's… KEEP THE MASS MOSTLY STRAIGHT UP AND DOWN."* The tradition is not ignorant of the biomechanics — it **amplifies the vertical and suppresses the lateral**, deliberately. That reconciliation is what makes both authorities usable at once.

4. **⚑ Several of the numbers the commission asked for are SUB-PIXEL at sprite scale and therefore cannot be gates.** On a 400-px figure: minimum toe clearance = **3.2 px**; the published mocap foot-skate ground truth = **0.24 px/frame**; a veridical idle's head bob = **~0.8 px**. The literature's precision exceeds our medium's resolution. Slip gates must be *relative* (to an expected **0.105 H/frame** planted-sole scroll), and toe clearance must be a JUDGE question, not a gate.

5. **Two idles is the genre norm, the 2.0-second loop is confirmed three times independently, and our lane is building one idle.** D2 ships `NU` (8 f, **0.64 s**, combat-ready) *and* `TN` (16 f, **2.05 s**, relaxed); Grim Dawn ships `AttackIdle` + `LongIdle` + an explicit **transition clip** + 67 fidget slots; Hades ships `Idle` + a `Stop` settle. Hades' NPC house idle is 60 f @ 30 fps = **2.00 s**; D2's town idle is **2.05 s**; practitioner guidance says 2–4 s. **And an idle needs more LOCK assertions than MOTION assertions** — roughly 5 to 2, the inverse of the walk — because K3's defect is that everything moved a little, not that nothing moved.

6. **`G6_seam`'s failure on the walk is a statistic mismatch, not a defect — and the fix is one line.** A walk's frame-to-frame pose change is intrinsically non-uniform (CONTACT→DOWN is a small settle; DOWN→PASSING is a large swing-through), so a *correct* walk has a small minimum-internal distance and a seam that exceeds it. G6-literal is biased against walks by construction; an idle, whose motion is near-uniform, passes. **Proposed `G6c`: compare the seam to its half-cycle homologue** — d(8→1) vs d(4→5), the same phase one step earlier. **Cheapest refuting test: run both statistics on the K3 walk frames the lane already has.** That settles the live L5 case either way.

7. **12 frames beats 8, for two independent reasons that arrived from different centuries.** Williams' canonical beat is 12 frames per step and his key placement on 8s is *"reduced up and down action… this is why cartoon walks are often on 8's"*; Muybridge's native sampling is **12 phases per stride**, so a 12-frame sheet maps 1:1 off the plate and an 8-frame sheet needs an interpolation. Separately: **an 8-frame full cycle at 12 fps is a *cartoon* walk by Williams' own taxonomy** (3 steps/s) — 8 fps is what produces his "natural" walk. **fps is not a free parameter once the frame count is chosen.**

8. **No single facing can validate a cycle — and Muybridge already solved the split.** Sagittal quantities (bob, stride, arm swing, sole slip) are maximal in **profile** and degenerate toward the camera axis; frontal quantities (lateral sway, head-path shape, shoulder/hip counter-rotation) are the reverse. So the gate set must split by facing. **Every Muybridge plate carries profile (0°) + rear (90°) + front-oblique (~60°, i.e. a three-quarter) of the same stride at the same instants** — the 1887 apparatus is laid out along the axes our gate set needs.

9. **The oracle exists in both forms and is public domain; the painted equivalent does not exist at all.** Muybridge plates 2 and 13 are downloaded (**7628 × 6049, PDM 1.0**, licence sidecars written) and plate 2's lateral row exists as a public-domain animated GIF — **sheet and video, same plate, no licence question**. Faithful assembly fps is **8.33** (Muybridge's own 0.120 s interval), *not* the ~3 fps the Commons GIF happens to play at. Meanwhile *painted register × elevated 3/4 × idle AND walk × 8 directions × named open licence* is an **empty set** across nine surveyed sources — the best content matches are the worst licence matches.

10. **The judge-anchor question is already partly answered by licences, before anyone rules on policy.** CraftPix's licence — free tier included — forbids using its assets for *"training, fine-tuning, developing, **testing, validating**, or improving"* AI systems. **"Testing" and "validating" name judge-anchoring.** So generation-reference and judge-anchor are two distinct questions and vendors already treat them differently; CC0 and CC-BY are anchor-safe, CraftPix is not, and public domain is unrestricted on every axis.

11. **Diablo II's weapon-class architecture is our T2 gear-overlay plan, shipped in 2000 — and it corrects my own first reading.** Parsing `AnimData.D2` directly shows **frame count and speed for `NU`/`WL`/`RN` are identical across all 12 weapon classes within a character class**; the `.cof` only re-composites which arm/hand/weapon layers draw. So the staff problem is a **layer** problem on a weapon-invariant beat, not a re-authoring problem. Hades sits at the opposite extreme — every weapon fully re-rendered, **36,992 locomotion sprites vs D2's 768, a ~48× ratio**. Those two bracket the choice the lane has to make.

**And one methodological note I am obliged to report against myself:** my first form of the head-path gate (W-3) was *"enclosed signed area ≈ 0"*. I built it, tested it on synthetic known-good and known-bad paths, and **it was blind to the defect it was named for** — a figure-8's lobes cancel to exactly zero, identical to a perfect straight line, and a head travelling on a diagonal scores a *perfect* axis ratio. It is now three sub-gates. **The check running is not the check passing**, and that is why every threshold in § 5.4 is marked pre-registration-required rather than ready to bind.

---

## 1. The walk cycle, frame by frame

### 1.1 The canonical phase set — and the one thing every tutorial gets wrong

**Primary source, read directly:** Richard Williams, *The Animator's Survival Kit*, "WALKS" chapter, pp. 102–125, scanned excerpt hosted by Carnegie Mellon (`graphics.cs.cmu.edu/nsp/course/15464-s17/lectures/Animators_Survival_Kit_walks.pdf`; also `cs.cmu.edu/~15464-s13/handouts/`). I read all 24 pages as images. Every quote below is transcribed from the page. **VERIFIED.**

Four keys per **step** (= half cycle), in this order:

| # | Phase | What defines it | Body height | Williams, verbatim |
|---|---|---|---|---|
| 1 | **CONTACT** | Heel of the lead foot just touches; legs at widest spread | **MEDIANT** (mid-height) | "I always start off with that contact because it's a dynamic, moving thing." (Milt Kahl, quoted p.116) |
| 2 | **DOWN** | Bent stance leg absorbs the weight | **LOWEST** | "NEXT COMES THE DOWN POSITION — WHERE THE BENT LEG TAKES THE WEIGHT" (p.107) |
| 3 | **PASSING** | Swing leg passes the stance leg; stance leg straight | slightly above mediant | "PASSING POSITION (slightly higher than mid-point) … BECAUSE THE LEG IS STRAIGHT UP ON THE PASSING POSITION, IT'S GOING TO LIFT THE PELVIS, BODY and HEAD SLIGHTLY HIGHER." (p.107) |
| 4 | **UP** | Push-off; ball/toe drives | **HIGHEST** | "The FOOT PUSHING OFF LIFTS The PELVIS, BODY and HEAD UP TO ITS HIGHEST POSITION — THEN The LEG IS THROWN OUT TO CATCH US ON The CONTACT POSITION — SO WE DON'T FALL ON OUR FACE." (p.108) |

> **The correction that matters.** The widespread tutorial claim is *"highest at the passing position."* Williams says the passing position is only **slightly** higher than mediant, and the **maximum is at UP — the push-off, one key LATER.** His own summary line, p.108, verbatim:
>
> **"SO, IN A NORMAL 'REALISTIC' WALK — The WEIGHT GOES (DOWN) JUST AFTER the STEP — JUST AFTER the CONTACT. and The WEIGHT GOES (UP) JUST AFTER the PASSING POSITION."**
>
> **VERIFIED.** Consequence for us: a bob curve whose maximum sits *on* the passing frame is not wrong so much as **one key early**, and at 8 frames per cycle that is a 45° phase error — visible, and closed-form detectable (§ 3.1, gate **W-2**).

**Also VERIFIED from the same pages, and directly relevant to K3's defects:**

- **Arms are opposite the legs.** "IN A NORMAL, CONVENTIONAL WALK, THE ARMS ARE ALWAYS OPPOSITE TO THE LEGS TO GIVE BALANCE and THRUST." (p.107) Restated p.103: "EACH ARM MOVES IN COORDINATION WITH the OPPOSITE LEG, GIVING BALANCE and THRUST."
- **The arm swing peaks at DOWN, not at CONTACT.** "AND JUST TO COMPLICATE LIFE — IN A NORMAL WALK THE ARM SWING IS AT ITS WIDEST ON THE DOWN POSITION (AND NOT ON THE CONTACT POSITION AS WE'D PREFER)." (p.107) Corroborated by his own p.103 panel 2: "OUR ARMS ARE AT THEIR WIDEST POINT." **This is a second one-key phase offset, in the opposite direction from the bob** — arms lead the legs' extremes by one key.
- **Shoulders counter-rotate with the hips, and both level out at PASSING.** "WHEN ARM IS FORWARD The SHOULDER IS FORWARD … WHEN FOOT IS FORWARD The HIP JOINT IS FORWARD"; "HIP and SHOULDER LINE OPPOSE EACH OTHER"; "ON The PASSING POSITION HIPS AND SHOULDERS ARE MORE OR LESS STRAIGHT." (p.120)
- **Body bends at the extremes, straight at passing.** "NOW LET'S BEND THE BODY ON THE EXTREMES / KEEP STRAIGHT ON THE PASSING POSITION." (p.123)
- **Head tilt belongs to the PASSING position.** "OR JUST TILT THE HEAD AND SHOULDERS SIDEWAYS ON THE PASS POSITIONS" (p.113); "LET'S TILT THE HEAD" at pass pos (p.120); "LET'S DELAY THE TILT OF THE HEAD ON THE PASSING POSITION" (p.121).
- **Foot clearance is nearly nil.** "Normally we lift our feet off the ground just the bare minimum. That's why it's so easy for us to stub our toes… WE'RE LESS THAN ONE CENTIMETER AWAY FROM STUBBING OUR TOE EVERY TIME WE TAKE A STEP. WALKING IS NATURALLY ENERGY CONSERVING. WE LIFT OUR FOOT AS LITTLE AS POSSIBLE." (pp.102–103)
- **Heel-first landing.** "OUR FOOT GLIDES DOWN HEEL FIRST FOR A SOFT LANDING." (p.103)

### 1.2 Frames, beat and fps — the table that sets our sheet

**Williams p.110, transcribed verbatim (frames per STEP, at 24 fps). VERIFIED.**

| Frames / step | Williams' label |
|---|---|
| 4 | a very fast run (6 steps a second) |
| 6 | a run or very fast walk (4 steps a second) |
| 8 | slow run or 'cartoon' walk (3 steps a second) |
| **12** | **brisk, business-like walk — 'NATURAL' walk (2 steps a second)** |
| 16 | strolling walk — more leisurely (⅔ of a second per step) |
| 20 | elderly or tired person (almost a second per step) |
| 24 | slow step (one step per second) |
| 32 | "…show me the way…to go home…" |

And p.109: "The FIRST THING TO DO IN A WALK IS SET A BEAT. **GENERALLY PEOPLE WALK ON 12'S — MARCH TIME** (half a second per step, two steps per second)." Corroborated in the same chapter by a second practitioner: Milt Kahl "bought a stopwatch and went downtown in the lunch break and timed people walking — normal walks, people just going somewhere. He said they were *invariably* on twelve exposures — right on the nose. March time." (p.110). **VERIFIED as quotation; PRACTITIONER-REPORT as measurement.**

> **Cross-check against gait science.** 2 steps/second = **120 steps/min cadence**. Normal adult free-walking cadence is ~100–120 steps/min — Williams' "march time" sits at the brisk end of measured normal. The animation tradition and the clinical literature agree on the beat. **DERIVED** (arithmetic mine; both inputs VERIFIED).

**Williams' key placement, verbatim from his charts (p.109). VERIFIED.**

| Beat | CONTACT | DOWN | PASSING | UP | next CONTACT |
|---|---|---|---|---|---|
| on 12s | 1 | 4 | 7 | 10 | 13 |
| on 16s | 1 | 5 | 9 | 13 | 17 |
| on 8s | 1 | 3 | 5 | 7 | 9 |

Note his aside on the 8s row: "REDUCED UP AND DOWN ACTION — SINCE IT'S TAKING PLACE IN A SHORTER TIME. THIS IS WHY CARTOON WALKS ARE OFTEN ON 8'S. BUMP, BUMP, BUMP, 3 STEPS A SECOND." **The shorter the beat, the LESS bob** — the amplitude is not free of the timing.

> **DERIVED — what an 8-frame full-cycle sheet actually is, and the fps it wants.**
> A game sheet's "8-frame walk" is normally a **full cycle = two steps = 4 frames per step.** Mapping Williams' four keys onto it gives exactly **contacts at frames 1 and 5**, downs at 2 and 6, passings at 3 and 7, ups at 4 and 8 — **which is precisely the assumption already written into SPEC § 6 T1 `gait_oracle.py` ("contacts at frames 1/5").** That assumption is correct and now has a primary citation.
> The beat then follows from fps alone:
>
> | Sheet | fps | frames/step | steps/sec | Williams' label |
> |---|---|---|---|---|
> | 8-frame cycle | **8** | 4 | **2.0** | **'natural' / business-like walk** |
> | 8-frame cycle | 10 | 4 | 2.5 | between natural and cartoon |
> | 8-frame cycle | **12** | 4 | **3.0** | **'cartoon' walk — bump, bump, bump** |
> | 12-frame cycle | 12 | 6 | 2.0 | 'natural' walk |
> | 16-frame cycle | 16 | 8 | 2.0 | 'natural' walk |
>
> **The lane's fps is therefore not a free parameter once the frame count is chosen.** An 8-frame cycle shipped at 12 fps is a *cartoon* walk by Williams' own taxonomy, and — by his 8s note — one that should carry *reduced* bob. If the register wants a grounded, weighty walk, either 8 fps on 8 frames or 12 fps on 12 frames is the cheapest correct pairing. **DERIVED; the transfer to a painted ARPG register is UNVERIFIED and is a Matt/gandalf call, not mine.**

### 1.3 (a) The planted sole

**Definition (Williams, VERIFIED).** Over one step, exactly one foot is on the ground from its CONTACT to the following CONTACT — i.e. the planted foot is planted for **all four keys of its step**, and hands off at the contact. At the two contacts both feet touch (double support). Clinical gait puts stance at **60 %** and swing at **40 %** of the cycle, with **double support ~12 %** of cycle time ([orthofixar gait-cycle reference](https://orthofixar.com/basic-science/gait-cycle/), tertiary teaching page — **SECONDARY**; these are the standard textbook figures).

**The measurable version for an in-place cycle.** In a walk-in-place sheet the planted sole does not move in the world; it moves **backward across the canvas at exactly the cycle's scroll speed** while the swing foot moves forward. Two closed-form consequences:

- **Backward-travel constancy.** Planted-sole x-velocity must be constant and equal in magnitude for both feet across their stance halves. Unequal magnitudes = the two legs are walking at different speeds — the "repeats a lead" defect class.
- **Foot-skate.** The published metric, quoted exactly:
  > "We use the same measurement as [Zhang et al. 2018] to estimate the amount of foot skating during motion, i.e. **s = d(2 − 2^(h/H))**, where *d* is the foot displacement and *h* is the foot height of two consecutive poses. To account for differences in motion capture data, we use a **height threshold of H = 3.3 cm**, which produces **an average foot skate of 0.10 centimetres per frame** in the motion capture data."
  > — Ling, Zinno, Cheng & van de Panne, *Character Controllers Using Motion VAEs*, ACM TOG 39(4), Art. 40, July 2020 (SIGGRAPH 2020), § 7.2. **VERIFIED** (fetched, quoted).
  Their Table 1 reports real mocap at **0.10 cm/frame** and synthesised motion at **0.067–0.44 cm/frame**. Normalised to a 1.70 m stature: mocap ground truth = **0.059 %H per frame**; the height threshold H = 3.3 cm = **1.94 %H**. **DERIVED.**

**Swing-foot clearance.** Williams: "less than one centimeter away from stubbing our toe." Measured: **minimum toe clearance (MTC) occurs at or very near mid-swing and is ~10–20 mm**, with one reported adult mean of **14.1 ± 8.3 mm** ([*Minimum toe clearance: probing the neural control of locomotion*, Sci Rep 2017](https://www.nature.com/articles/s41598-017-02189-y); MTC value via the divided-attention treadmill study [PMC4499197](https://pmc.ncbi.nlm.nih.gov/articles/PMC4499197/) — **SECONDARY**, read via search extract not full text). Normalised: **0.6–1.2 %H**, i.e. **0.8 %H** at the 14 mm mean. **DERIVED.**

> ⚠ **SCALE COLLAPSE — the most consequential single finding in § 1.** On a 512-px canvas with a figure ~400 px tall, **0.8 %H is 3.2 px.** MTC is at or below the noise floor of a painted sprite's silhouette, of its anti-aliased edge, and of the matte. **Minimum toe clearance cannot be a gate at our resolution — it can only be a JUDGE question.** The same arithmetic kills the mocap foot-skate threshold outright: 0.059 %H/frame = **0.24 px/frame**. Any closed-form slip gate must be set at the *pixel* floor (§ 3), not at the biomechanical number. This is not a defect in the sources; it is the resolution of our medium meeting the resolution of the literature.

### 1.4 (b) The vertical bob — amplitude and phase

**Measured (biomechanics).**

| Source | Quantity | Value | Grade |
|---|---|---|---|
| Orendurff et al., *The effect of walking speed on center of mass displacement* (PubMed [15685471](https://pubmed.ncbi.nlm.nih.gov/15685471/)), 10 subjects, 0.7–1.6 m/s | vertical CoM excursion | **2.74 ± 0.52 cm** (0.7 m/s) → **4.83 ± 0.92 cm** (1.6 m/s) | **SECONDARY** (search extract; PubMed page returned a cookie wall on direct fetch — recorded as a gap, § 6) |
| Standard clinical teaching ("determinants of gait") | vertical CoG displacement | **5 cm** sinusoid, **two** cycles per gait cycle; **lowest at heel strike / double support, highest at mid-stance** | **SECONDARY** ([orthofixar](https://orthofixar.com/basic-science/gait-cycle/), read directly) |
| Same page | lateral displacement | "amplitude of 6 cm" in one sentence, "length of motion is 5 cm over the weight-bearing limb" in another | **SECONDARY, internally inconsistent — flagged, not averaged** |

**Normalised to 1.70 m: vertical bob = 1.6 % H (slow) → 2.8 % H (fast); clinical 5 cm = 2.9 % H. DERIVED.**

> **A real CONFLICT, reported not averaged.** Clinical gait puts the vertical **maximum at mid-stance**, which is the **PASSING** position. Williams puts it at **UP**, the push-off, one key later (§ 1.1). Both were read directly. Three honest observations:
> 1. They are **one key apart**, which on an 8-frame cycle is one frame (45°) and on a 12-frame cycle is 1–1.5 frames.
> 2. The disagreement is **structural, not sloppy**: the clinical curve is the *centre of mass*, the animator's curve is the *drawn mass* the eye reads, and Williams explicitly says he moves it (below).
> 3. **For gating purposes the safe form is a RANGE, not a point:** the bob maximum must fall on **PASSING or UP** (frames 3–4 and 7–8 of an 8-frame cycle) and the minimum on **DOWN** (frames 2 and 6). Anything outside that window is wrong under *both* authorities. That is the form gate **W-2** takes in § 5.4.

> **THE EXAGGERATION LAW — and it is the reason a Muybridge-derived number cannot be used raw.** Williams, p.106, verbatim:
> > "**GETTING THE WEIGHT.** WE DON'T GET WEIGHT BY A SMOOTH LEVEL MOVEMENT. When we trace off a live action walk (the fancy word is rotoscoping), it doesn't work very well. Obviously, it works in the live action — but **when you trace it accurately, it floats.** Nobody really knows why. **So we increase the ups and the downs — accentuate or exaggerate the ups and downs — and it works.** … **IT'S THE UP AND DOWN POSITION OF YOUR MASSES THAT GIVES YOU THE FEELING OF WEIGHT.**"
>
> **VERIFIED.** This is the single most important sentence in the commission for R10b. **A veridical per-frame table measured off Muybridge is the right FLOOR and the wrong TARGET.** The drawn register deliberately sits above life. Any threshold band we set must therefore be **asymmetric**: a hard floor at roughly the biomechanical value (below it the figure floats — exactly Matt's "no bob" complaint) and a soft ceiling well above it. § 5.4 sets the band accordingly.
>
> And the second-order rule, also VERIFIED (p.105): **"the first thing I always look for is how much up and down action there is on the head. The amount of up and down is the key!"** Williams uses head-bob amplitude as the *primary* character read — little bob = gliding, weightless, "as if on a tightrope"; large bob = heavy, wide-legged. **Our bob amplitude is a character-identity parameter, not only a correctness parameter.**

### 1.5 (c) Lateral head sway — and the rule that reverses the intuition

**Measured (biomechanics).** Mediolateral CoM excursion is of the same order as the vertical: ~4–6 cm total, **maximum over the weight-bearing limb at mid-stance** (SECONDARY, orthofixar, with the internal inconsistency flagged above). Normalised: **~2.4–3.5 %H. DERIVED.**

**Head-specific measured data.** Hirasaki, Moore, Raphan & Cohen, *Effects of walking velocity on vertical head and body movements during locomotion*, Exp Brain Res (1999) — treadmill, 0.6–2.2 m/s: **"At walking speeds up to 1.2 m/s there was little head pitch movement in space and head pitch relative to the trunk was compensatory for trunk pitch. As walking velocity increased, trunk pitch remained approximately invariant, but a significant head translation developed."** **SECONDARY** (abstract read via search extract; the Springer page redirected to an auth wall — recorded as a gap, § 6). The classic head-stabilisation line (Pozzo, Berthoz & Lefort, Exp Brain Res 1990) reports head angular pitch deviation of roughly **4–5°** in locomotion, with the head rotating **opposite** to its linear translation to compensate. **SECONDARY** (same reason).

> **The animator's rule is the OPPOSITE of "sway the head sideways", and it is the rule I would gate on.** Williams, p.123, quoting Ken Harris verbatim:
> > "**A CAUTIONARY NOTE FROM KEN HARRIS: FOR WALKS, DON'T MAKE CYCLES OF BODY AND HEAD ACTION IN CIRCLES OR FIGURE 8'S — IF YOU DO IT WILL LOOK LIKE A BIRD OR PIGEON WALK** (unless you want that.) … **FOR SAFETY KEEP THE MASS MOSTLY STRAIGHT UP AND DOWN.**"
>
> **VERIFIED.** So: lateral sway in a drawn walk is not an amplitude to hit — it is an amplitude to **bound**. The head centroid's trajectory over a cycle should be a **near-vertical line segment traversed twice**, not an ellipse and emphatically not a figure-8. That is closed-form and cheap: fit the head-centroid point cloud over the cycle, take the ratio of its minor to major axis, and take the signed area the closed path encloses. Both should be small. Gate **W-3** in § 5.4.
>
> Where lateral *does* belong, per Williams, is as a **tilt at the passing position** (pp.113, 120, 121) — a rotation of the head/shoulder line, not a translation of the head mass. That distinction is exactly what K3's review was reaching for: the head *keeping its idle tilt* is a **constant** tilt; what is missing is a tilt that **alternates** with the passing positions.

### 1.6 (d) Arm counter-swing

**Measured.** Normal-gait shoulder flexion–extension excursion is reported at **24.6° ± 3.4°**, with healthy group-mean arm-swing amplitudes in the **20–26°** band (**SECONDARY**; surfaced via search over the gait-kinematics literature — I opened Leardini et al., *PLoS One* 8(10):e77168 (2013) and Killeen et al., *Sci Rep* 8:12803 (2018) directly and **neither prints an absolute normative amplitude in degrees**: Killeen reports asymmetry indices and walking speeds of 1.29 / 1.57 / 1.30 m/s only. Recorded as a gap, § 6.)

**DERIVED — what 24.6° means in sprite pixels.** With shoulder-to-wrist ≈ **0.33 H** (standard body-segment proportions), a 24.6° (0.429 rad) excursion moves the hand through an arc of **0.429 × 0.33 H ≈ 0.14 H**, i.e. **~14 %H of fore-aft hand travel, peak-to-peak**. On a 400-px figure that is **≈ 57 px** — an order of magnitude above the noise floor, and therefore **the single most measurable of all the walk quantities at sprite scale.**

**Phase, VERIFIED (Williams):** opposite the same-side leg; **widest at DOWN**, not at contact; shoulder forward when that arm is forward; hip and shoulder lines counter-rotate and level out at PASSING. Grim Natwick, quoted p.125: "While the opposite arm naturally moves with the opposite leg, we'd break the rules eight or ten different ways to make the walk interesting." — i.e. **counter-phase is the norm, deviation is a deliberate character choice**, which is exactly the shape a gate should take (flag, don't forbid).

### 1.7 (e) The weapon arm carrying a staff — what shipped ARPGs actually do

This is the K3 defect ("the staff arm is rigid") and it is the question where the literature is thinnest. What I can evidence:

**Diablo II — the strongest documented case, and it answers the question structurally rather than numerically.** D2 keys every character animation to a **weapon class token**, and the locomotion animation *itself* differs per class. The token set (**SECONDARY**; the Phrozen Keep modding corpus at `d2mods.info`, surfaced via search — the canonical `.cof` tutorial is [here](https://d2mods.info/resources/infinitum/tut_files/dcc_tutorial/chapter2.html)):

`hth` (hand-to-hand) · `bow` · `1hs` (1-hand swing) · `1ht` (1-hand thrust) · **`stf` (staff)** · `2hs` · `2ht` · `xbw` · `1js` · `1jt` · `1ss` · `1st` · `ht1` · `ht2`

and a `.cof` filename is *token · body-part · armour-class · **mode** · **weapon-class***, where mode is `NU` (neutral/idle), `WL` (walk), `RN` (run), `TN`/`TW` (town neutral/walk), `A1`/`A2` (attack), etc.

> **The reading — CORRECTED once the binary was parsed, and the correction is the more useful result.**
> My first reading of the filename scheme was that `stf` being its own weapon class means the staff walk is a wholly distinct animation. **The data says otherwise, and says something better.** Parsing `AnimData.D2` directly (3,558 records, 160 bytes each, read to EOF and cross-checked against an independent text decompile — **VERIFIED**): **frame count and animation speed for `NU`, `WL` and `RN` are IDENTICAL across all 12 weapon classes within a character class.** (Barbarian checked exhaustively: 12 of 12 identical; only `BARNBOW` deviates, speed 256 vs 216.)
>
> So D2's architecture is: **one shared locomotion TIMING skeleton per character class, with per-weapon-class composited LAYER ART hung on it.** The `.cof` re-composites which arm/hand/weapon layers draw and in what order; the beat underneath does not change.
>
> **That is exactly our T2 gear-overlay architecture, shipped in 2000** — and it is a much cheaper answer to the staff problem than "author a separate staff walk." It says the staff-carry defect is a **layer** problem, not a cycle problem: the cycle's timing is weapon-invariant, and what changes per weapon class is which arm art is drawn over it. It still lands on the game tracker's "empty-hands animation set = weapon-class axis" note — but as a *layering* axis, not a *re-authoring* axis.

**Hades — the most transferable painted-2D precedent, and a genuinely surprising one.** Jen Zee (art director, Supergiant), interviewed in MCV/DEVELOP, verbatim:
- "**We relied completely on Photoshop to create 2D assets. The 3D work was modeled and animated with Maya, and post-processed through AfterFX.**"
- "**our animator, Thinh used mocap as a basis for a large chunk of animation in the game!**"
- The game shipped **"32,494 FX animation frames and 942,489 character and enemy animation frames."**
- "At the inception of the project, we'd thought the art style would be painterly. **We ended up pivoting to pen and ink** when the narrative and tone changed drastically during preproduction."

**VERIFIED as quotation** ([MCV/DEVELOP, "Behind the art of Hades"](https://mcvuk.com/business-news/behind-the-art-of-hades-we-value-artistic-integrity-and-excellence-in-artistic-craft-at-supergiant-however-were-first-and-foremost-a-game-design-lead-team/), read directly); the production claims are **PRACTITIONER-REPORT**.

> **Why this matters more than the frame counts I was asked for.** The benchmark painted-2D ARPG did **not** hand-draw its cycles frame by frame. It drove them from **3D animation and motion capture**, and painted over. The cycle's *geometry* came from a rig; the *paint* came from artists. That is the same division our lane is converging on (seed → pose guide → composite), and it is evidence that the division is the shipped norm in this register, not a compromise.

**And the shipped data file settles the weapon-arm question for Hades — in the opposite direction from D2.** Reading `CharacterAnimationsHero.sjson` (731 records) directly (**VERIFIED**), cross-validated against Supergiant's own public statement (a dev-badged account: *"104-frame animation rendered at 32 angles. So that's 3,328 frames for that one short animation"* — which matches `ZagreusBowDash*`'s `NumFrames 104 / NumAngles 32` exactly):

| Clip | Frames | Angles | PlaySpeed |
|---|---|---|---|
| `ZagreusIdle` | **120** | **32** | undeclared (engine default) |
| `ZagreusRun` | **32** | **64** | **60.0** → 0.533 s cycle; footfalls at frames 1 and 16 ⇒ **16 frames/step** |
| `ZagreusRunSprint` | 32 (same art) | 64 | 75.0 → 0.427 s |
| `ZagreusWalk` (House, non-combat) | 60 | 32 | slide-timed, 1 art frame per tick |
| **every weapon run** (Sword, Spear, Shield, Bow, Fist, Arthur) | **32 each** | **64 each** | inherits 60 |
| weapon idles | ShieldIdle 120 · FistIdle 68 · SwordUpdateIdleLoop 58 @ 30 (1.93 s) · GunIdleLoop 170 | — | 32 |
| NPC idles (house norm) | mostly **60** @ **30 fps → 2.0 s** | 8–32 | 30.0 |

> **Two corrections to the commission's own premises, both VERIFIED against the file.** (1) *"Hades uses a limited direction set with a flipped sprite"* — **no.** Idle ships **32 pre-rendered angles**, run ships **64** (5.625° apart), and **no mirror/flip field exists anywhere in the schema.** (2) Hades does **not** composite the weapon arm at all: **every weapon gets its own complete re-rendered run and usually its own idle**, and every Aspect re-renders them again. Base + six weapons = **36,992 rendered locomotion sprites**, roughly **48×** one D2 layer/class/weapon-class set (768).
>
> **So the two benchmark ARPGs sit at opposite ends of the same axis** — D2 composites layers over a shared beat; Hades re-renders everything per weapon. They bracket the choice our lane has to make, and the cost ratio between them is ~48:1.

**Path of Exile 2 — one negative data point, and it is about *reading*, not mechanics.** A player thread on the official forum ("Staff Animation", archived, no GGG reply) objects that "**sorcerer characters in Path of Exile 2 hold their staff like a club, which feels off for this archetype**," asking instead for "a one-handed stance or something more mystical." **TERTIARY** (single player post, read directly). Recorded only because it evidences that a *staff-carry posture that reads as the wrong weapon class* is a defect players notice and name — which is precisely the JUDGE-axis form the question should take for us (§ 5.5, question J-6).

**Grim Dawn — and this is the sharpest answer of the three.** Its player animation table (`anm_malepc.dbr` / `anm_femalepc.dbr`, read directly — **VERIFIED**) declares **9 weapon stances**: `unarmed, sHanded, dHanded, melee2h, spear, staff, ranged1h, ranged2h, dualRanged`. And then:

- **`staffAttackIdleAnim`, `staffLongIdleAnim`, `staffRunAnim` — and the whole `spear*` family — all point at `hero01_sword1h_*`.** Grim Dawn declares a staff stance and then **does not author a single staff clip.** It plays the one-handed sword animation. `melee2h` is the only two-handed stance authored separately.
- **The walk is shared:** 7 of 8 stances point at the *same* file `hero01_walk_a01.anm` (dualRanged uses `walk_b01`). **Two walk clips for the entire character.** The **run** is per-stance (7 distinct files).
- All 2,021 shipped `.anm` files carry **30 fps** in the header, with gameplay events on integer frame indices.

**Torchlight II** (engine log census, `PCS/HUM_M`, **VERIFIED**): **23 `IDLE_*` variants — including `IDLE_STAFF` — 14 `RUN_*` variants, and ZERO `WALK`.** `WALK.SKELETON` exists only on NPCs and pets. **Path of Exile** (`.aoc` read directly, **VERIFIED**): **24 `run_*` clips per class**, one per main/off-hand pair, `run_staff` among them — and **no `walk_*` clip exists at all**. **Last Epoch:** nothing numeric found anywhere (§ 6).

> ⚑ **The structural finding, and I think it is the one that should change what K3 does next.** Across the five shipped ARPGs I could get data for, **not one authors a per-weapon WALK:**
>
> | Game | per-weapon idle? | per-weapon run? | per-weapon walk? | walk at all? |
> |---|---|---|---|---|
> | Diablo II | shared beat, per-class **layers** | shared beat, per-class **layers** | shared beat, per-class **layers** | yes (`WL`, 8 f) |
> | Hades | **yes** (fully re-rendered) | **yes** (fully re-rendered) | no | only a non-combat House walk |
> | Grim Dawn | yes (but staff → sword1h) | yes (7 clips) | **no — one shared walk** | yes, shared |
> | Torchlight II | **yes, 23 of them** | yes, 14 | — | **no walk on the player rig** |
> | Path of Exile | — | **yes, 24** | — | **no walk clip exists** |
>
> **The genre solves the weapon-carry problem at the IDLE and at the RUN. It does not solve it at the walk, because it largely does not ship a walk.** Two of five have no player walk at all; a third shares one walk across every weapon stance; a fourth (Hades) walks only out of combat. **Only Diablo II ships a combat walk, and it ships it on a weapon-invariant beat.**
>
> This does not say our walk is wrong. It says the walk is the **worst possible place** to fight the staff-arm battle — it is the one cycle the genre has decided is not worth per-weapon authoring. If the lane wants a weapon-class-correct staff carry, **the idle and the run are where the shipped precedent puts the effort**, and where a per-weapon mint would be buying something the genre agrees is worth buying.

**What the biomechanics says about carrying something, for whatever it is worth.** Asymmetric and hand-carried loads measurably disturb gait: carrying "removes the option of arm swing to counteract unbalanced loads," and a 3.5 kg load significantly increased asymmetry in stance, loading response, single-limb support, pre-swing and swing durations and step time (**SECONDARY**, the load-carriage gait literature via search; I did not open the primary papers). The transferable point is the direction, not the number: **a carried staff legitimately reduces that arm's swing — it does not legitimately freeze it.** "Reduced" and "rigid" are different, and the difference is measurable (gate **W-5**).

### 1.8 (f) Gaze — does any shipped ARPG animate eyes in a walk?

**I found no evidence that any shipped isometric ARPG animates eyes during locomotion, and I found a structural reason why not.** Two passes, both negative (§ 6).

The structural reason is scale. Diablo II shipped at **640×480**, with sprites pre-rendered from 3D at a fixed elevated three-quarter camera; contemporaneous isometric titles of that class carried character sprites of roughly **50 px tall** (**SECONDARY**, gamedev.net technical discussion via search extract; the thread itself returned 403 on direct fetch). At a 50 px figure the head is ~7 px and the eye is **sub-pixel**. Even at our 400 px figure the head is ~55 px and an eye is ~4 px across. Blink-and-look-around eye animation *is* a documented pixel-art idle technique — the standard trick being to fill the eye with skin colour for a single frame (**PRACTITIONER-REPORT**, pixel-art animation guides) — but that is a *portrait-scale* or *platformer-scale* technique, not an ARPG-locomotion one.

> **The reframe this forces, and I think it is the correct one.** Matt's K3 note that "**the eyes dart frame to frame**" is not a request for animated eyes. It is the observation that **the eyes are NOT locked** — that an unpinned feature is being re-invented per frame, which is exactly R6's "every frame is a fresh render" problem wearing a new face. The gate is therefore not *"do the eyes animate correctly"* but ***"do the eyes move at all beyond the head's own rigid motion"*** — and the answer for a walk cycle should be **no**. Gaze is locked on the path ahead for the whole cycle; the eyes are carried by the head, and nothing else. That is closed-form: the eye region's position relative to the head centroid must be constant to within a pixel or two across the cycle. Gate **W-7**.

---

## 2. The idle, frame by frame

### 2.1 What a base idle contains — the practitioner numbers

There is no peer-reviewed literature on game idle animation. The best available evidence is vendor/practitioner guidance, and I grade all of it **PRACTITIONER-REPORT**. The most numerically specific source I found, read directly, is MoCap Online's *Idle Animation for Games: Design Guide* ([mocaponline.com](https://mocaponline.com/blogs/mocap-news/idle-animation-game-dev-guide)); corroborating shape from Animation Mentor's breathing-loop tutorial and AnimSchool's *Breathing Life into Idle Animations*.

| Quantity | Value | Grade |
|---|---|---|
| Base idle loop length | **2–4 s** ("A 2-second loop is 60 frames; a 4-second loop is 120 frames" at 30 fps); 8–12 s for a loop carrying a full weight shift | PRACTITIONER-REPORT |
| Authoring frame rate | "Idle animations are typically authored at 30 fps for games" | PRACTITIONER-REPORT |
| Breathing rate — relaxed | **15–20 breaths/min** → **3.0–4.0 s per breath** | PRACTITIONER-REPORT |
| Breathing rate — alert | **20–25 breaths/min** → **2.4–3.0 s per breath** | PRACTITIONER-REPORT |
| Breathing rate — combat | **25–30 breaths/min** → **2.0–2.4 s per breath** | PRACTITIONER-REPORT |
| Chest/shoulder vertical travel | **"1–2 cm of vertical travel, no more"** | PRACTITIONER-REPORT |
| Head motion in an idle | "small bobbing of a **few millimetres**" | PRACTITIONER-REPORT |
| Weight transfer foot-to-foot | over a **4–8 s** cycle | PRACTITIONER-REPORT |
| Root bone | **"zero translation and rotation in a standing idle loop"** | PRACTITIONER-REPORT |
| Fidget trigger cadence | **every 30–60 s** | PRACTITIONER-REPORT |
| Fidget variant count | **3–5** minimum; **5–10** in production | PRACTITIONER-REPORT |
| Fidget implementation | additive layers / montages **on top of** the base idle — separate clips, never baked in | PRACTITIONER-REPORT |
| Blend-in from locomotion | **0.2–0.4 s** | PRACTITIONER-REPORT |
| Loop closure | first and last frame must match exactly in pose and position; "any visible pop at the loop point breaks immersion every time the cycle repeats" | PRACTITIONER-REPORT |

**Normalised to body height (DERIVED).** 1–2 cm of chest travel on a 1.70 m figure = **0.6–1.2 %H**; "a few millimetres" of head bob = **~0.2 %H**. On a 400-px figure: chest **2.4–4.8 px**, head **~0.8 px**.

> ⚠ **The idle hits the same scale collapse as § 1.3, and harder.** A veridical idle's head motion is **sub-pixel** at our sprite scale. So a painted-2D idle cannot be "the realistic idle, drawn" — it must be the **exaggerated** idle, for exactly Williams' reason (§ 1.4). But there is a second constraint pulling the other way that does not apply to the walk: **an idle is on screen constantly and loops indefinitely**, so exaggeration that reads as "alive" at 2 s reads as "twitching" at 2 minutes. The band is therefore narrow at both ends, and **narrower than the walk's**. I put a number on it in § 5.4 (gate **I-2**), flagged as the least-evidenced threshold in the whole set.

### 2.2 What is LOCKED in an idle

This is the half of the question the K3 review was actually about ("the idle chest breathes but head/eyes drift"). The practitioner consensus, and the one clause of it that is closed-form:

- **The root is locked.** Zero translation, zero rotation (VERIFIED as a quoted rule from the source above). For a sprite this means: **the sole line and the figure's horizontal centroid do not move across an idle cycle.**
- **The feet are locked.** A standing idle with a weight shift may roll pressure between feet, but neither sole leaves the ground and neither sole translates. **Any sole displacement in an idle is a defect, full stop** — there is no legitimate version of a moving foot in a standing idle, which makes it the cleanest gate in the entire commission (gate **I-1**).
- **The head is nearly locked.** "A few millimetres" — i.e. carried by the chest's rise, not independently animated.
- **The eyes are locked.** See § 1.8 — same finding, same reasoning, and it applies with more force in an idle because there is no locomotion to mask the drift.
- **The weapon hand is locked** relative to its grip. The staff's contact point with the hand is a rigid constraint; the staff's *far end* may describe a small arc if the figure sways, but the grip does not slide along the shaft.

> **The reframe for K3, and I believe it is the finding that most changes what the lane does.** "The chest breathes but the head and eyes drift" describes an idle where **the intended motion is present and the intended STILLNESS is absent.** Every practitioner source frames an idle as *mostly locked with one small moving part* — and our failure mode is the inverse: *everything moves a little because nothing was pinned.* An idle gate set therefore needs **more locked-ness assertions than motion assertions** — roughly 5 locks to 2 motions — which is the opposite proportion to the walk's gate set. That asymmetry is a design input for `gait_oracle.py`'s sibling, not a detail.

### 2.3 Frame counts and fps actually used in shipped ARPGs

**These are read out of shipped data files, not out of articles.** Diablo II's `AnimData.D2` was parsed byte-for-byte (3,558 records × 160 bytes, read cleanly to EOF) and cross-checked against an independent text decompile — the two agree exactly. Hades' `CharacterAnimationsHero.sjson` (731 records) was read directly and cross-validated against a Supergiant developer's own published numbers. **VERIFIED** unless marked.

| Game | Clip | Frames | Dirs | fps | Loop |
|---|---|---|---|---|---|
| **Diablo II** | **`NU` combat idle** | **8**/dir (Druid 6) | 16 | 12.5 (most classes); 9.4 BA; 18.0 PA | **0.64 s** |
| Diablo II | **`TN` town / relaxed idle** | **16**/dir (AI 12, DZ 10) | 16 | 7.8 typical | **2.05 s** |
| Diablo II | **`WL` walk** | **8**/dir (Paladin 10) | 16 | 25.0 (AM/SO/NE/AI) | 0.32 s |
| Diablo II | `RN` run | **8**/dir, all 62 player COFs | 16 | 25.0 (5 of 7 classes) | 0.32 s |
| Diablo II | engine clock | — | — | **25 ticks/s hardcoded**; `AnimSpeed 256` = 100 % of 25 fps | — |
| Diablo II | directions | — | **16 players / 8 monsters** (`monstats2.txt`: dNU=8 on 509 of 610 rows) | — | — |
| **Hades** | `ZagreusIdle` | **120** | **32 angles** | undeclared | 2.0 or 4.0 s |
| Hades | NPC idles (house norm) | **60** | 8–32 | **30.0** | **2.0 s** |
| Hades | `ZagreusRun` | 32 | **64 angles** | 60.0 | 0.53 s |
| **Grim Dawn** | every shipped `.anm` | — | 3D | **30 fps in all 2,021 files** | — |
| **Titan Quest** | `.anm` header | u32 numBones / numFrames / **fps** | 3D | **30** | — |
| **Celeste** (2D benchmark) | idle 9 f @ 0.1 s · walk 12 f @ 0.06 s · runFast 12 f @ 0.05 s | — | — | 10 / 16.7 / 20 | 0.9 / 0.72 / 0.6 s |
| **Shovel Knight** | idle | **2 frames** — *"Our idles are generally all 2 frames with no extra animations! Just a gentle bob."* (Yacht Club) | — | — | — |

> **Three things the shipped data says that the practitioner guidance in § 2.1 does not.**
> 1. **Two idles is the genre norm, and the split is combat-vs-relaxed.** D2: `NU` 8 f / 0.64 s (combat-ready) vs `TN` 16 f / 2.05 s (town). Grim Dawn: `AttackIdleAnim` vs `LongIdleAnim` **plus** an explicit `IdleTransAnim` transition clip **plus** `FidgetAnim1–3` (67 fidget slots on the player record). Hades: `Idle` 120 f + `Stop` 32 f settle. **Our lane has been building one idle. The genre builds two and a transition between them.**
> 2. **The 2.0 s idle loop is real and independently arrived at.** D2's town idle is 2.05 s; Hades' NPC house idle is 60 f @ 30 fps = 2.00 s; the practitioner guidance says 2–4 s. Three sources, one number. **2.0 s is the safest idle-loop target we have in the whole document.**
> 3. **The combat idle is three times faster than the relaxed one** (0.64 s vs 2.05 s in D2). That is not a breath rate — it is a readiness read. If our Keeper is meant to look combat-ready, the relaxed-breathing band of § 2.1 (3.0–4.0 s/breath) is the **wrong** target and D2's 0.64 s is the right one.

Where I could not source a number I say so rather than supplying a plausible one (§ 6).

**Derived guidance for an 8–12 frame painted idle (DERIVED; inputs PRACTITIONER-REPORT).** To land inside the relaxed-breathing band of 3.0–4.0 s per breath with one breath per loop:

| Frames in loop | fps for 3.0 s loop | fps for 4.0 s loop | Comment |
|---|---|---|---|
| 8 | 2.67 | 2.0 | too coarse — the breath reads as a stutter |
| 12 | 4.0 | 3.0 | workable floor |
| 16 | 5.33 | 4.0 | comfortable |
| 24 | 8.0 | 6.0 | smooth |

> **This is a live tension with the walk and it needs a conductor ruling, not a research answer.** A walk at 8–12 fps and an idle at 3–5 fps are *different playback rates in the same sheet*. Either the idle needs **more frames than the walk** to share one fps, or the manifest must carry **per-animation fps** (`E04/NEUTRAL_CONTRACT.md` already lists `fps` per animation, so the contract supports it). If the lane wants one fps across all clips, the honest consequence is: **a 12-frame walk at 12 fps pairs with a 36–48-frame idle**, which is expensive in a lane where every frame is an image call. The cheap alternative is per-clip fps. I state the arithmetic; the choice is gandalf's and Matt's.

### 2.4 Diablo II's animation structure — what the file formats actually encode

**VERIFIED** — I opened the [Diablo II Animation Conversion Extended Tutorial](https://d2mods.info/resources/infinitum/tut_files/dcc_tutorial/chapter2.html) directly for the naming scheme, and the binary `AnimData.D2` was parsed record-by-record for the numbers in § 2.3.

`AnimData.D2` layout, for the record: 256 hash blocks; each **160-byte record** = 8-byte name + `u32 framesPerDirection` + `u16 speed` + 2 pad + **144 per-frame event bytes**. File size 570,304 B ⇒ exactly 1024 + 160 × 3,558. Locomotion records carry **no** event bytes; `AMA1HTH` carries event 1 at frame 8 (the hit frame) and `AMSCHTH` event 2 at frame 11 (the cast trigger). **The gameplay-relevant instants are pinned to integer frame indices** — which is why D2R could rebuild in 3D and still, in the lead designer's words, *"be true to that 25 FPS."*

- **Mode codes** are the animation vocabulary: `NU` neutral/idle · `WL` walk · `RN` run · `TN` town-neutral · `TW` town-walk · `A1`/`A2` attack · plus death, hit-recovery, cast, block, etc.
- **A `.cof` filename is `token · body-part · armour-class · mode · weapon-class`** — so an animation is identified by the **cross product of mode and weapon class**, not by mode alone.
- **Armour class is in the filename too** (`lit` / `med` / `hvy`) — D2 varies the *gait* by armour weight as well as by weapon.
- Frames-per-direction and per-mode animation speed live in `AnimData.D2` / `Animation Data.txt`.
- The paper-doll layering renders each body/armour/weapon part separately and composites at runtime.

> **Two readings, both load-bearing for us.**
> 1. **D2's animation identity is a three-axis product: mode × weapon-class × armour-class.** Our `visibility_table.py` already indexes per-part visibility by *direction*. This says the same table has at least one more axis it does not yet carry, and the game tracker has already spotted one of them ("empty-hands animation set = weapon-class axis"). The armour-class axis is a third.
> 2. **The paper-doll split is the same split as our gear-layer plan (T2 `gear_overlay.py`).** D2 shipped that architecture in 2000 on pre-rendered sprites. It is precedent, not innovation, and it means the *cycle* must be authored on the base body with gear as an overlay — which in turn means **the cycle's geometry must be gear-independent**, a constraint that belongs in the bible before K3 ships.

---

## 3. QA practice — which cycle checks are closed-form and which are judge-only

### 3.1 The practices, sourced and adjudicated

The animation trade has a stable, named set of cycle checks. None of them were invented as software; all are eyeball procedures that happen to have closed-form analogues. I list each with its source grade, then rule on whether *we* can compute it from masks and frames.

| # | Practice | What it is, as practised | Source grade | **Our verdict** |
|---|---|---|---|---|
| Q1 | **Onion-skin / ghosting overlay** | Superimpose neighbouring frames to see spacing and drift | PRACTITIONER-REPORT (CAVE Academy; Anim Mentor; Trau Studios) | **CLOSED-FORM.** Frame-to-frame per-part mask displacement is already in reach via T0-c disjoint palette bins. It is not a gate by itself — it is the *evidence image* every other gate should emit. |
| Q2 | **Foot-slip / "moonwalk" test** | "The planted foot must be dead still relative to the ground. Check it every frame; IK feet drift if you let them" (MoCap Online, walk-cycle guide) | PRACTITIONER-REPORT, with a **VERIFIED** formal metric behind it (Ling et al. 2020, § 1.3) | **CLOSED-FORM — and the single strongest gate available.** Needs the sole line and per-boot masks, both already contracted in T1. |
| Q3 | **Arc / motion-path test** | Trail the hips, head and wrists; the path must be a smooth arc, not a zigzag; "track your arcs… fix any knee pops" | PRACTITIONER-REPORT | **CLOSED-FORM.** Centroid trajectory + second-difference (curvature) continuity. Cheap. |
| Q4 | **Ken Harris's no-circles rule** | Head/body mass must trace a near-vertical path, **not** a circle or figure-8, or it reads as a pigeon walk | **VERIFIED** (Williams p.123, quoted § 1.5) | **CLOSED-FORM, and I have not seen it implemented anywhere.** Minor/major axis ratio + enclosed signed area of the head-centroid loop. This is the cheapest high-value gate in the whole commission. |
| Q5 | **Loop-closure / "pop" test** | First and last frame must match exactly; any pop "breaks immersion every time the cycle repeats" | PRACTITIONER-REPORT | **CLOSED-FORM.** Frame-N→frame-1 distance must be ≤ the median adjacent-frame distance. Note the subtlety: for a *full* cycle the closure is frame 8→1; for a *half* cycle sheet it is frame 8→mirrored-1. |
| Q6 | **Silhouette test** | Render the frame as a black silhouette; the action must still read | PRACTITIONER-REPORT | **CLOSED-FORM for legibility** (O5 already does silhouette at 64 px). **JUDGE-ONLY for "does the action read"** — that is a semantic question about a shape. |
| Q7 | **Squint test** | "Squint at your animation until it's blurry and check if you can still tell what action is happening. If not, push the poses further" | PRACTITIONER-REPORT | **JUDGE-ONLY.** It is a deliberately perceptual instrument; a blur filter plus a classifier is not the same instrument and would be a false proxy. |
| Q8 | **Flipping / pose-to-pose review** | Flip between the four keys to check the poses are distinct and correctly ordered | PRACTITIONER-REPORT | **CLOSED-FORM as key-distinctness** (adjacent-key mask distance must exceed a floor — this is what catches "repeats a lead"); **JUDGE-ONLY as "is this a good pose."** |
| Q9 | **Weight read** | "Does the character bob up and down naturally? Do their hips shift appropriately with each step?" | PRACTITIONER-REPORT | **SPLIT.** Amplitude and phase: closed-form (§ 5.4 W-1/W-2). "Naturally": judge-only. |
| Q10 | **Identity persistence across frames** | Is it the same character in frame 7 as in frame 1? | no source — this check does not exist in the animation trade because in the trade it cannot fail | **CLOSED-FORM**, and already contracted (`identity_vector.py`). **This is the check that exists only because our generator is what it is**, and it has no precedent to borrow from. |

### 3.2 The line, stated once

**Closed-form** reaches everything that is a *number about where pixels are over time*: position, displacement, velocity, amplitude, phase, path shape, loop closure, key ordering, per-part persistence. **Judge-only** begins exactly where the question becomes *"does this read as…"* — weight, intent, character, grace, whether a staff looks like a staff rather than a club.

> **And the boundary has a precedent-shaped warning on it, from R6.** The CHI 2025 taxonomy found **functional implausibility** the most prevalent artifact class (58.7 %) and the *least* reliably caught by humans (64.1 %). The cycle analogue of functional implausibility is **motion that is individually plausible per frame and incoherent as a sequence** — a leg that is planted in frame 2 and swinging in frame 3 without an intervening contact. That is precisely the class a JUDGE looking at frames will miss and a closed-form sequence check will catch. **Weight the gate set toward the sequence, not the frame.**

### 3.3 What has NO published QA practice at all

Recorded honestly, because their absence is itself a finding:

1. **No published QA practice exists for validating a generated sprite cycle**, as opposed to an authored one. Every source above assumes an animator who cannot accidentally redraw the character between frames. Our dominant failure mode is outside the entire literature.
2. **No published per-frame numeric tolerances** for any of Q1–Q9. The trade checks are all *ordinal* ("smoother", "reads better"). Every threshold in § 5.4 is therefore mine, derived from the biomechanics, and must be calibrated on our own anchors before it can bind. **That is a pre-registration requirement, not a caveat** — the same discipline the charter already applies to O3b.

---

## 4. Direction and camera — which facing exposes the stride

### 4.1 The projection, with numbers

**VERIFIED** ([Wikipedia, *Isometric video game graphics*](https://en.wikipedia.org/wiki/Isometric_video_game_graphics), read directly): the game-standard is a **2:1 pixel ratio**, giving axes at **≈26.565° (arctan ½)** to the horizontal — *not* true isometric's 30°/35.264°. Formally it is **dimetric**, with axis separations of ≈116.565°, ≈116.565°, ≈126.870°. Corroborated by a practitioner: "The 2:1 (2x,1y) line is the foundation of isometric pixel art… this is actually an approximation of true isometry (**26.5 degrees rather than the mathematically accurate 30**)… the line pattern is much more conducive to pixel art" ([Pixel Parmesan, *Fundamentals of Isometric Pixel Art*](https://pixelparmesan.com/blog/fundamentals-of-isometric-pixel-art), **PRACTITIONER-REPORT**, read directly). Diablo II "used fixed-perspective 2D… optionally allowed perspective scaling of the sprites in the distance" (VERIFIED, same Wikipedia source); its sprites were pre-rendered from 3D Studio Max models (**SECONDARY**).

### 4.2 The geometry, worked

**DERIVED** — the arithmetic is mine; the projection constants are VERIFIED above. Take an orthographic camera at elevation *e* above the horizontal. A world-vertical displacement Δz maps to screen-y with factor **cos e**; a world-horizontal displacement along the view azimuth maps to screen-y with factor **sin e**.

| Elevation | cos e (vertical retained) | sin e (depth bleeding into screen-y) |
|---|---|---|
| 26.565° (2:1 game iso) | **0.894** | 0.447 |
| 30° (true iso) | 0.866 | 0.500 |
| 35.264° | 0.816 | 0.577 |

Three consequences, in increasing order of importance:

1. **The bob is compressed by ~11 % at the 2:1 camera.** A 2.5 %H world bob reads as 2.2 %H on screen. Small, but it means a threshold calibrated on a profile life reference must be scaled before it gates a 3/4 sprite.
2. **In a facing whose direction of travel lies along the camera azimuth (toward/away), forward motion projects into screen-y at sin e = 0.447 — and swamps the bob.** For a walk-in-place cycle the *body* has no net travel, so this cancels; but the **feet do travel** within the cycle, and their travel is what the gait oracle reads. In a toward/away facing the planted sole's backward travel lands almost half in screen-y, entangled with the bob, and the two feet occlude one another.
3. **In a facing perpendicular to the camera azimuth (screen-lateral / profile), forward-backward foot travel is entirely in screen-x.** Screen-y for the head is then **pure bob**, uncontaminated. Both feet are separated, unoccluded, and at maximum horizontal extent.

> **The ruling this produces.** For **gait QA, use the profile-facing direction** — the one where the character walks across the screen rather than into or out of it. It is the only facing in which head-y is pure bob, the only one in which both soles are simultaneously visible and separated, and the one in which stride length is at maximum screen extent. Every quantity in § 1 that lives in the sagittal plane — bob, stride, arm counter-swing, foot clearance — is at maximum measurability there and at minimum in the toward/away facings.
>
> **Conversely, the frontal-plane quantities invert.** Lateral head sway, step width, and shoulder/hip counter-rotation are **invisible in profile** (they are along the camera axis) and **maximal in the toward/away facings**. So Ken Harris's no-circles rule (Q4) cannot be checked in the profile facing at all — the head's lateral component is projected away.

**The practical consequence for the gate set, stated plainly:** *there is no single facing in which the full cycle can be validated.* The gate set must be **split by facing**:

| Gate family | Best facing | Why |
|---|---|---|
| Planted sole, foot-skate, stride, arm counter-swing, vertical bob amplitude + phase | **profile / screen-lateral** | sagittal plane in the image plane; no depth contamination; feet unoccluded |
| Head-path shape (no circles/figure-8), lateral sway bound, shoulder-hip counter-rotation, step width | **toward or away (front/back)** | frontal plane in the image plane |
| Loop closure, key distinctness, identity persistence, eye lock | **every facing** | these are frame-relational, not geometric |

**On the diagonals.** A practitioner claim surfaced in search that the NE/NW diagonals are the hardest to animate in isometric; I could **not** verify it from a source I opened and I am not reporting it as a finding. What I *can* say from geometry is that the diagonals are the facings in which sagittal and frontal components **mix**, so every gate is attenuated and none is clean — which is a reason to gate the two clean axes and let the diagonals inherit, not a reason to claim they are hardest to draw. **DERIVED.**


---

## 5. R10b — the ORACLE artifacts

### 5.1 A frame-accurate walk + idle reference for measurement — Muybridge

#### 5.1.1 The plates, identified, downloaded, licence-verified

Two plates are in `refs/` with licence sidecars. **Both are Public Domain Mark 1.0** — I read the `license` field out of the Wellcome IIIF manifest myself rather than taking it second-hand. **VERIFIED.**

| Plate | Subject | Wellcome b-number | px | Licence | Local file |
|---|---|---|---|---|---|
| **13** "Walking" | woman — lateral + front + rear, 12 phases each | `b19801555` | **7628 × 6049** | **PDM 1.0** | `refs/B19801555.jpg` |
| **2** "Walking" | man — same layout | `b19801099` | **7628 × 6049** | **PDM 1.0** | `refs/B19801099.jpg` |

Plate numbers are not inferred. Each Wellcome record carries its own *Publications note* citing "Prospectus and catalogue of plates, Philadelphia: J.B. Lippincott, 1887, p. ii, **no. 13** / **no. 2** ('Walking')". Manifest `https://iiif.wellcomecollection.org/presentation/v2/b19801555`; full-size image `https://iiif.wellcomecollection.org/image/B19801555.JP2/full/max/0/default.jpg`.

**Further candidates located but not downloaded** (Boston Public Library + Wellcome, all public domain):

| Need | Plate(s) | Where | Note |
|---|---|---|---|
| Man walking, alternates | 5, 7, 8, 9, 10, 11 | Wellcome `b19801117`, `b19801129`, …; BPL plate 7 at 5000 × 3980 | |
| Woman walking, alternates | 14, 15, 17, 18, 20–25 | Wellcome `b19801567`, `b19801579`, … | **14** is the Prospectus's own worked example |
| **Idle / standing** | **529, 530, 531 "Various poses"** | BPL `commonwealth:70795x30c` (530, 5044 × 3996), `commonwealth:707961925` (531, 4964 × 3976); Wellcome `b20095995` / `b20096008` | ⚠ **There is NO plain standing-at-rest plate in *Animal Locomotion*.** Getty + Cornell catalogue OCR and the BPL subject facet all searched — negative. These are a figure shifting between held poses, which is the nearest thing that exists. |
| **Walking with a long shaft** | **176, 177** "Crossing brook on step-stones, with fishing-pole and basket" | BPL `commonwealth:70795z880` (4996 × 3972) | **The only plates of a figure locomoting while carrying a long shaft** — and it is stepping-stone walking, not level walking. Plates 49 and 552 (cane) are level, but a cane is a support, not a carried stave. |

> **A caution worth carrying: Muybridge mislabelled four plates, and the libraries faithfully reproduce his mislabels.** The 1888 Penn monograph's own ADDENDUM errata: *"Plate 549 should be 'Locomotor Ataxia.' Plate 555 should be 'Muscular Atrophy of Left Leg.' Plate 558 should be 'Stuporous Melancholia.' Plate 559 should be 'Partial Paraplegia.'"* Read per-plate descriptions and intervals from the **catalogue scan** (`archive.org/details/animallocomotion00muyb`, Getty Research Institute, 52 canvases at 3319 × 4638, IIIF live), never from library metadata.

#### 5.1.2 The timing and the camera geometry — from Muybridge's own 1887 Prospectus

**VERIFIED.** The Prospectus is open at `archive.org/details/animallocomotion00muyb`; the Cornell copy `cu31924024580353` prints *"There are no known copyright restrictions in the United States on the use of the text."* Its worked example, for plate 14:

> *"…the quantity of movement illustrated is **two steps, or one stride**. **Twelve successive phases** of that movement were photographed synchronously from each of the three points of view, L, E, and F… **The interval of time between each of the twelve phases was about one-eighth of a second, or according to the chronograph one hundred and twenty one-thousandth parts of a second (0.120″), the complete movement having been accomplished in about one and a half seconds. The number of figures on the plate is 36.**"*

And the apparatus:

> *"A **lateral battery of 24 automatic electro-photographic cameras**"* ~15 m from the track, lens centres 15 cm apart. **E** = 12 cameras *"arranged vertically for a series of 'Rear Foreshortenings'; the points of view being at an **angle of 90°** from the lateral battery."* **F** = 12 cameras *"arranged horizontally for a series of 'Front Foreshortenings'; the points of view **averaging an angle of 60°** from the lateral battery."* Exposure ~1/2000–1/5000 s. Every plate's interval is printed in the catalogue table.

> **Three findings fall straight out of this, and the third one I did not expect.**
>
> **(a) 12 phases per stride is the native sampling — so a 12-frame sheet maps 1:1 and an 8-frame sheet does not.** Muybridge samples one full gait cycle in **12** frames. A 12-frame cycle reads off the plate without resampling; an 8-frame cycle needs a 12→8 interpolation that lands 4 of its 8 frames between exposures. **That is now the second independent reason for 12 frames over 8** — the first being that 12 is Williams' canonical beat (§ 1.2).
>
> **(b) The plate-14 subject was strolling, not marching — which bounds what the plate can tell us.** 12 × 0.120 s = **1.44 s per stride = 0.72 s per step = 1.39 steps/second.** Williams calls **⅔ of a second per step** a *"strolling walk — more leisurely"*; his *'natural'* walk is 0.5 s/step. **Muybridge's reference walk is one tempo band slower than the animation tradition's default** — and by Orendurff (§ 1.4) a slower walk carries **more lateral sway and less vertical bob** than a brisk one. So a bob amplitude measured off this plate is a *low* estimate for a business-like walk, **before** Williams' exaggeration law (§ 1.4) is applied. **Both corrections point the same way: up.**
>
> **(c) Muybridge's F battery sits at ~60° from lateral — which is a three-quarter view.** Every plate therefore carries **profile (L, 0°) + rear (E, 90°) + front-oblique (F, ~60°) simultaneously, of the same stride, at the same instants.** § 4 concluded that no single facing can validate a whole cycle and that the gate set must split between a profile facing and a front/back facing. **A single Muybridge plate supplies exactly that split, synchronised** — and adds a ~60° oblique far closer to our elevated three-quarter camera than either axis. That the 1887 apparatus is laid out along the same axes our gate set needs is the strongest argument in this document for using these plates rather than a modern rig.

#### 5.1.3 The per-frame measurement — ATTEMPTED, NOT ACHIEVED. What failed, and what it would take

The commission asked for a per-frame table of head-top y, hip y, per-sole x/y and arm angle, normalised to body height. **I attempted it on plate 13's lateral row and I am not delivering a table, because the numbers are not good enough to gate on, and a table that looks authoritative and is not would be worse than none.**

**What I did.** Located the photographic block, found the 12 frame gutters from the column profile (spacings 371–403 px — clean), then segmented each figure by three successive methods: global Otsu + vertical morphological opening; a per-row background model with z-thresholding, closing and hole-fill; and a centre-constrained multi-component union.

**What went wrong, measured:**

| Symptom | Measured | What it means |
|---|---|---|
| Apparent stature varies **13.6 % peak-to-peak** across the 12 frames (569–651 px) | a real walk's bob is ~**2–3 %** | the segmentation is moving, not the subject |
| Floor-line detection scatters over **121 px** (sd 35) | should be near-constant for a fixed camera battery | the strongest lower-third edge is sometimes the floor, sometimes a foot |
| Individual frames lose the legs or lose the head | frame 7 returned h=305 of ~600; frame 11 returned top=244 | tone continuity breaks at the shadowed waist and knee |

**Three root causes, all properties of the artifact rather than of the effort:**
1. **The subject's hair is dark and the backdrop is dark.** Every bright-thresholding method finds the *face*, not the crown — so "head-top" is not directly segmentable at all, only "top of lit skin."
2. **The backdrop is a bright measuring grid** whose threads sit at the same luminance as lit skin. Vertical opening suppresses them, but the same opening erodes thin limbs.
3. **A collotype has no flat field.** Exposure varies within and between the 12 frames, so no single threshold holds and Otsu drifts with how much bright floor each frame happens to include.

> **What would actually work, costed honestly.** The backdrop grid is not only the obstacle — **it is Muybridge's own calibration reference, with numbered graduations printed along the track** (legible in the plate: …23, 24, 25, 26, 27…). The correct method is to **rectify each frame against its own grid** and read landmarks in Muybridge's units rather than in scan pixels. That removes the per-frame scale and floor-line problem entirely and is the only route to gate-grade numbers. It is roughly a day of focused work — grid-line detection, per-frame homography, then hand-verified landmarking of 12 frames × 4 landmarks — and it is **a commission of its own, not a subsection of this one.**
>
> **Meanwhile nothing in § 5.4 depends on it.** Those thresholds derive from the modern instrumented gait literature (Orendurff; the MTC studies; Ling et al.), which measured with force plates and marker sets and reports in normalised units already. **Muybridge's value to us is the PHASE STRUCTURE and the three synchronised camera axes, not the amplitudes** — and the phase structure is legible by eye from the plate at a glance.

**In hand and reusable:** both plates, both licence sidecars, the block/gutter geometry, the Prospectus timing. Nothing needs re-fetching if the rectification pass is ever commissioned.

### 5.2 A painted-register sprite sheet with idle AND walk — the search, and its negative result

**Headline: the four constraints do not co-occur anywhere I could find.** *Painted register* + *elevated three-quarter ARPG camera* + *idle AND walk* + *8 directions* + *a named open licence* is an **empty set**. Every candidate drops at least one — and the sharper finding is that **the best content matches are the worst licence matches.** Swept: OpenGameArt (three relevant collections, ~300 entries), Kenney.nl, itch.io, CraftPix free tier, the Universal LPC generator, Poly Haven, Sketchfab, Quaternius, KayKit.

**Every licence string below I read myself on the page.** Licence is the highest-stakes field here and a wrong one is the worst failure mode available, so none of these is second-hand.

| # | Asset | Licence (verbatim, verified by me) | Register | Camera | Dirs | Idle | Walk | Loop video/GIF |
|---|---|---|---|---|---|---|---|---|
| 1 | **KayKit: Character Animations** — Kay Lousberg · [OGA](https://opengameart.org/content/kaykit-character-animations) | **CC0** — *"Free for personal and commercial use, no attribution required. (CC0)"* | rendered 3D (`.gltf`) | **you choose** | any | **✓** | **✓** | **✓** three GIFs served on the page |
| 2 | **Isometric: Mini-Crusader** — Bleed · [OGA](https://opengameart.org/content/isometric-mini-crusader) | **CC-BY 4.0**; attribution string required: `Bleed - http://remusprites.carbonmade.com/` | pre-rendered 3D, reads illustrated (not pixel) | **elevated 3/4 — correct** | **8** | **✓** | **✓** | ✗ (verified negative) |
| 3 | **Isometric Painted Game Assets** — laetissima · [OGA](https://opengameart.org/content/isometric-painted-game-assets) | **CC0** | **genuinely painted** (a commenter: *"looks more like something illustrated with the brush tool in Flash"*) | isometric | 4 | ✗ **no idle** | ✓ | **✓** `…/files/walking.gif` |
| 4 | **Reiner's Tilesets — 2D Humans** — Reiner "Tiles" Prokein · [site](https://www.reinerstilesets.de/graphics/2d-grafiken/2d-humans/) | ⚠ **NOT open — custom freeware.** *"The 2D and 3D graphics are free to use for non commercial and commercial useage."* · *"I just want my name in the Credits in the commercial case."* · **redistribution forbidden:** *"it doesn´t mean that you can upload my raw graphics and meshes to your page, sell them or do something else with it."* No AI/ML clause. | pre-rendered 3D, painterly-soft | **`Isoformat 4:3`**, stated on the page | 8 (two sets at 32) | **✓ `Stopped`** | **✓ `Walking`** | ✗ |
| 5 | **Hand-Drawn Square Characters, 8 Directions** — rgsdev · [OGA](https://opengameart.org/content/hand-drawn-square-characters-animated-8-directions-top-down-free-cc0) | **CC0** (verified twice: OGA field + itch `Creative Commons Zero v1.0 Universal`) | hand-drawn; page states *"No generative AI was used"* | **flat top-down** (wrong camera) | 8 | ✓ | ✓ | ✓ five GIFs |
| 6 | **Isometric Hero and Heroine** — Clint Bellanger · [OGA](https://opengameart.org/content/isometric-hero-and-heroine) | **CC-BY 3.0** | Blender-rendered, pixel-adjacent | isometric, 64×32 base | 8 | Stance, 4 f | **Run**, 8 f (no walk) | ✗ |
| 7 | **HD 8-Directional Top-Down Character Pack 1** — SmallScaleInt · [itch](https://smallscaleint.itch.io/hd-8-directional-top-down-character-pack-1) | ⚠ **an invented "Standard Commercial License":** *"✗ Cannot resell, redistribute, or sublicense the raw asset files themselves"* | 3D pre-render over-painted in Photoshop | top-down | 8 | ✓ ×3 | ✓ Walk/Run/Strafe | ✓ |
| 8 | **8 Directional Knight** — Hormelz · [itch](https://hormelz.itch.io/8-directional-knight) | **CC0** (`Creative Commons Zero v1.0 Universal`) | **pixel art** | 8-dir HD-2D | 8 | ✓ ×3 | ✓ | ✓ |

**Dead ends, recorded so the search is not repeated.** Kenney has **no** isometric *character* packs at all — the isometric line is environment tiles, the character line is 3D models. Poly Haven has **no character category**. The Universal LPC generator is **4-direction** (`DIRECTIONS = ["up","left","down","right"]`, read from `sources/state/constants.ts`), 64 px, pixel, and its `idle` is a **2-pose cycle** — near-useless for motion study; its per-asset licences span CC0 / CC-BY / CC-BY-SA / OGA-BY / **GPL**, and its own README warns that the CC-BY-SA DRM clause makes Steam/iOS release legally murky. Several OGA entries advertised as "painted" (Symel, Stella, Angelee's turnarounds) are pixel art on inspection, and the turnarounds are *rotations*, not locomotion. The OGA population also contains **GPL 2.0** art (the Hex-a-Hop "little girl six direction" asset) — a viral licence on an art pipeline; avoid.

> ⚠ **A licence clause that bears directly on Matt's open judge-anchor question, and it should be in front of him before he rules.**
> **CraftPix's licence — free tier included — forbids AI use by name.** Verbatim, verified by me at [craftpix.net/file-licenses](https://craftpix.net/file-licenses/):
> > *"The Licensed Assets…may not be used, in whole or in part, for the purposes of training, fine-tuning, developing, **testing, validating**, or improving any artificial intelligence (AI), machine learning (ML), deep learning, generative AI, or similar systems."*
>
> **"Testing" and "validating" are named.** So on CraftPix terms, using an asset as a **JUDGE ANCHOR** — showing it to an Astra instance to calibrate a rubric — is prohibited *even though it never conditions a mint.* The refinement Matt is being asked to rule on is therefore **not one question but two**, and the licences already distinguish them:
> - **Generation reference** (third-party pixels condition a mint) — already forbidden by `lane/ref_provenance.py`. Unchanged.
> - **Judge anchor** (third-party pixels are shown to an evaluating model) — **licence-dependent, and at least one major vendor forbids it by name.**
>
> **The clean path, on facts rather than inference:** **CC0** (KayKit, laetissima, rgsdev, Hormelz) carries no such restriction and is **anchor-safe**. **CC-BY** (Mini-Crusader, Bellanger) is **anchor-safe with attribution recorded**. **Reiner's and SmallScaleInt are use-only** — fine to look at, not safe to redistribute, silent on AI. **CraftPix is anchor-unsafe by its own words.** **Public domain (Muybridge) is unrestricted on every axis** — which is a third, independent reason it should be the lane's first-choice oracle.

**Nothing above has been downloaded and nothing enters the lane.** Per the commission and `ref_provenance.py`, these are measurement-only references recorded by URL, author and licence.

### 5.3 The anthropometric spine — the constants every %H figure rests on

**VERIFIED.** Drillis & Contini (1966), reproduced as Figure 4.1 of Winter, *Biomechanics and Motor Control of Human Movement* — I read the figure image directly ([course scan](https://courses.grainger.illinois.edu/me481/sp2021/Anthro-Winter.pdf)). Segment lengths as a fraction of body height **H**:

| Landmark | ×H | Landmark | ×H |
|---|---|---|---|
| Eye height | 0.936 | Head height | **0.130** |
| Chin height | 0.870 | Shoulder width (biacromial) | 0.259 |
| **Shoulder height** | **0.818** | Upper-arm length | 0.186 |
| Elbow height | 0.630 | Forearm length | 0.146 |
| **Hip / greater trochanter** | **0.530** | Hand length | 0.108 |
| Wrist height | 0.485 | Hip width | 0.191 |
| Fingertip height | 0.377 | Foot length | 0.152 |
| Knee height | 0.285 | Foot breadth | 0.055 |
| Ankle height | 0.039 | | |

Two composites used repeatedly below, both arithmetic on the above (**DERIVED**): **shoulder→wrist = 0.186 + 0.146 = 0.332 H**; **shoulder→fingertip = 0.818 − 0.377 = 0.441 H**.

**Step length ≈ 0.41–0.42 H** (**SECONDARY**: the clinical "average step length 72 cm" against a 1.70 m stature gives 0.42 H, and the independent estimator "stride ≈ height × 0.413–0.415" agrees). Stride = 2 steps ≈ **0.83 H**.

> **DERIVED — the scroll rate `gait_oracle.py` needs, as a number.** In a walk-in-place cycle the planted sole must travel backward by exactly one **step length per step**. On an 8-frame full cycle (4 frames per step): **0.42 H ÷ 4 = 0.105 H per frame.** On a 400-px figure that is **≈ 42 px of backward sole travel per frame** — large, unambiguous, trivially measurable. This is the single most concrete number in the document, and it is the reference the planted-sole gate should be written against.
>
> Its corollary kills a threshold before it is written: the published foot-skate ground truth (0.10 cm/frame, § 1.3) normalises to **0.24 px/frame** on that same figure — **sub-pixel**. A slip gate must be **relative** ("planted-sole x-velocity constant to within ±k of the expected 0.105 H/frame"), never absolute.

### 5.4 Threshold RANGES for the T1 gait gates

**Status of everything in these tables: DERIVED, PRE-REGISTRATION-REQUIRED.** The inputs are cited and graded above; the arithmetic is mine; **the transfer of a life-measured band to a painted register is UNVERIFIED and must be calibrated on our own anchors before any of these binds.** Stated as ranges with a named failure direction, in the charter's instrument style (number + threshold + evidence, `null` when unevaluable). `H` = figure height in px, head-top to sole, measured per frame from the mask.

#### Walk

| ID | Rule | Measured quantity | Range | Needs | Failure direction |
|---|---|---|---|---|---|
| **W-1** | Vertical bob present and weighty | peak-to-peak head-top y over the cycle ÷ H | **floor 2.0 %H**, target **2.5–5.0 %H**, ceiling **7 %H** | head-top from mask | **below floor = "it floats"** — Matt's K3 complaint, and Williams' named failure; above ceiling = bouncing |
| **W-2** | Bob phase correct | frame index of head-top y min / max | min on **DOWN** (frames 2, 6 of 8); max on **PASSING or UP** (3–4, 7–8) | frame→phase map | max on CONTACT = inverted cycle |
| **W-3a** | Head path not too wide | minor/major axis ratio of the head-centroid cloud (PCA) | **≤ 0.35** | head centroid, front/back facing | ≈1.0 = circle **or** equal-amplitude figure-8 — both are Ken Harris's "pigeon walk" (§ 1.5) |
| **W-3b** | Name the defect when W-3a fails | closed-path signed area ÷ (A_vert × A_lat) | ≈ **0** ⇒ line or figure-8; clearly non-zero ⇒ **circle/ellipse** | same | **diagnostic only — must not be the primary gate**; see the note below |
| **W-3c** | Lateral at the right frequency | sign changes of head-centroid x over the closed cycle | **2–3** (one lateral oscillation per gait cycle); **≥ 4 fails** | same | ≥4 = lateral locked to the vertical's frequency — the head travels on a **diagonal**, which W-3a cannot see |
| **W-4** | Two bobs per cycle | count of head-top y minima over a full cycle | exactly **2** | head-top | 1 = only one leg is working |
| **W-5** | Arm counter-swing present | peak-to-peak wrist/hand-centroid x ÷ H, profile facing | free arm **8–20 %H**; **weapon arm ≥ 3 %H** | per-arm masks | weapon arm < 3 %H = **rigid** (the K3 defect); free arm < 8 %H = dead arm |
| **W-6** | Arms oppose legs | sign of (wrist-x − hip-x) vs sign of (same-side ankle-x − hip-x) | opposite on **≥ 6 of 8** frames | arm + leg masks | same sign throughout = the "both arms forward" tell |
| **W-7** | Gaze locked | eye-region centroid minus head centroid, per frame | drift **≤ 1.5 px** (≤ 0.4 %H) across the cycle | eye region | anything larger = "the eyes dart" (the K3 defect) |
| **W-8** | Planted sole does not slip | planted-sole x-velocity per frame vs expected **0.105 H/frame** | within **±20 %**, and **equal in magnitude between the two feet within ±10 %** | sole line, per-boot masks | unequal = "repeats a lead"; non-constant = moonwalk |
| **W-9** | One foot planted per phase | count of soles at the ground line per frame | **1**, except at contacts where **2** is permitted | sole line | 0 = floating; 2 off-contact = both feet stuck |
| **W-10** | Swing foot clears | min swing-sole y above ground line ÷ H | **report only, do NOT gate** — veridical MTC is 0.6–1.2 %H ≈ 3 px | sole line | see the § 1.3 scale collapse |
| **W-11** | Loop closes | see **G6c** below | | | |
| **W-12** | Keys distinct | adjacent-frame mask distance | every adjacent pair **> 0.4 ×** the median adjacent distance | masks | a near-duplicate pair = a repeated/duplicated frame |

#### Idle

| ID | Rule | Measured quantity | Range | Failure direction |
|---|---|---|---|---|
| **I-1** | **Feet locked** | per-sole centroid displacement across the loop ÷ H | **≤ 0.25 %H** (~1 px at H=400) | *any* sole motion in a standing idle is a defect — the cleanest gate in the set |
| **I-2** | Breath present but small | peak-to-peak chest/shoulder-line y ÷ H | **0.6–2.0 %H** | below = dead; above = panting. **Least-evidenced threshold here** — the veridical value (0.6–1.2 %H) is ~3 px, so the painted value must be exaggerated, and nobody has published by how much |
| **I-3** | Head nearly locked | head-top y peak-to-peak ÷ H | **≤ 1.2 %H**, and ≤ the chest amplitude | head moving more than the chest = the head is being re-drawn, not carried |
| **I-4** | Head does not drift | head-centroid x over the loop ÷ H | **≤ 0.4 %H**, no monotonic trend | monotonic trend = accumulating drift — the K3 defect |
| **I-5** | Gaze locked | as W-7 | **≤ 1.5 px** | as W-7 |
| **I-6** | Grip locked | weapon-hand centroid → staff-axis intersection, per frame | constant within **≤ 1 px** | the hand sliding along the shaft |
| **I-7** | Root locked | figure horizontal centroid + sole line | **≤ 0.25 %H** | the "zero root translation" rule, made measurable |
| **I-8** | One breath per loop | count of chest-y maxima | exactly **1** (relaxed idle) | 2 = the loop is two breaths, halving the apparent period |

> **On W-3, a correction I made to my own proposal before shipping it — recorded because the failure is instructive.**
> My first form of this gate was *"enclosed signed area ≈ 0"*, reasoning that a straight up-and-down path encloses nothing. I built it and tested it against synthetic known-good and known-bad head paths before writing it down. **It is blind to the exact defect it is named for.** Measured, 8 samples per cycle, amplitudes normalised:
>
> | Synthetic head path | axis ratio | signed area | x sign-changes |
> |---|---|---|---|
> | figure-8 (the *real* head path — see below) | **1.000** | **+0.0000** | 3 |
> | circle ("pigeon walk") | **1.000** | **−2.8284** | 3 |
> | pure vertical line (the ideal) | 0.000 | +0.0000 | 0 |
> | lateral suppressed to 0.35 | 0.350 | +0.0000 | 3 |
> | lateral at the **wrong frequency** (2×) | **0.000** | +0.0000 | **4** |
>
> **A figure-8's two lobes cancel: its signed area is exactly zero — identical to a perfect straight line.** So signed area is a *circle* detector, not a figure-8 detector. And the last row is worse: a head travelling on a **diagonal** (lateral locked to the vertical's frequency) collapses the point cloud to a line and scores **axis ratio 0.000**, passing W-3a cleanly while being plainly wrong. Neither of my first two statistics could see it; only the frequency count can. **Hence three sub-gates, not one.** This is the project's own standing lesson in miniature — *the check running is not the check passing* — and it is why every threshold in these tables is marked pre-registration-required rather than ready to bind.

> **Why the real head path IS a figure-8, and why the drawn one must not be — the two authorities reconciled.**
> Vertical CoM completes **two** cycles per gait cycle; mediolateral CoM completes **one**. A 2:1 Lissajous with comparable amplitudes **is** a figure-8 — and this is published, not inferred: *"The figure-eight shape can originate from the oscillatory CoM trajectories with one-cycle frequency in the mediolateral direction and two-cycle frequency in the superoinferior direction. As walking speed increases, the width of the shape in the mediolateral direction decreases, and the height of the shape in the superoinferior direction increases."* (*Speed- and mode-dependent modulation of the center of mass trajectory in human gaits as revealed by Lissajous curves*, J Biomech 2020 — **SECONDARY**, abstract read via search extract; ScienceDirect returned 403 on direct fetch.)
>
> And the amplitudes are comparable at our target tempo. Williams' march time (2 steps/s) × the 0.72 m clinical step = **1.44 m/s**. Interpolating Orendurff at 1.44 m/s: vertical ≈ **4.5 cm**, lateral ≈ **4.4 cm** — within 2 % of each other, i.e. **≈ 2.6 %H each**. **DERIVED.** So at exactly the tempo the animation tradition calls "natural," the true head path is a near-symmetric figure-8.
>
> **Ken Harris forbids precisely that shape.** This is not the biomechanics contradicting the animators — it is the animators *knowing* the true path and deliberately suppressing its lateral half, because a faithfully traced figure-8 reads as a pigeon walk on screen. It is the same move as Williams' exaggeration law (§ 1.4) in the other axis: **amplify the vertical, suppress the lateral.** Two suppressions and one amplification, all deliberate, all measurable — and together they are the whole difference between a rotoscope and a drawn walk.

> **G6c — a NEW loop-closure statistic, and this one is worth acting on immediately.**
> The lane's existing `g6_seam` compares the seam (frame N→1) against the **minimum** internal frame-to-frame distance; `g6b` against the **median**. The live K3 case is: **the walk fails G6 literal and passes G6b, while the idle passes both.**
>
> **DERIVED explanation — it is a statistic mismatch, not necessarily a defect.** A walk cycle's frame-to-frame *pose change* is intrinsically non-uniform even though its *timing* is uniform: CONTACT→DOWN is a small settle; DOWN→PASSING is a large swing-through. So a correct walk has a wide spread of internal distances and a small **minimum** — while the seam (UP→CONTACT, where the leg is thrown out to catch the fall) is one of the *larger* transitions. **A perfect walk will exceed min-internal at its seam.** An idle, whose motion is small and near-uniform, will not. **G6-literal is biased against walks by construction.**
>
> **The fix costs nothing and is apples-to-apples:** compare the seam to its **half-cycle homologue** — the transition at the same phase one step earlier. On an 8-frame cycle the seam is 8→1 (UP→CONTACT) and its homologue is 4→5 (UP→CONTACT). Gate: **d(N→1) ≤ 1.25 × d(N/2 → N/2+1)**. For an idle, which has no half-cycle symmetry, fall back to the median (g6b).
> **Cheapest refuting test:** compute both statistics on the K3 walk frames the lane already has. If d(8→1) ≈ d(4→5), the seam is fine and G6-literal was mis-measuring it; if d(8→1) ≫ d(4→5), there is a genuine pop. One script run, and it settles the live L5 case either way.

### 5.5 DSG-shaped judge questions for a cycle

Following the R6–R8 transcribe/judge contract: **atomic, closed-vocabulary, presence/count only, never coordinates** (GPT-4V localisation IoU 0.16 — never ask for boxes), with a **declared-absent control** in every transcribe set and a **known-bad control** in every judge batch.

**TRANSCRIBE — per frame, answerable by looking:**
- **T-1** "Is the LEFT boot touching the ground line? yes / no"
- **T-2** "Is the RIGHT boot touching the ground line? yes / no"
- **T-3** "How many boots are touching the ground line? 0 / 1 / 2"
- **T-4** "Which arm is further forward? left / right / neither"
- **T-5** "Is the staff in contact with the ground? yes / no"
- **T-6** "How many hands are on the staff? 0 / 1 / 2"
- **T-7** "Is the figure's head turned away from the direction of travel? yes / no"
- **T-8** *(declared-absent control)* "Is the figure wearing a cape? yes / no" — expected **no**

**JUDGE — per sequence, 1–5, with the known-bad control:**
- **J-1** "Does the figure's weight land? (Does it read as pressing into the ground rather than floating over it?)"
- **J-2** "Do the legs alternate, or does the same leg appear to lead twice?"
- **J-3** "Does the head ride on the body, or does it seem to move on its own?"
- **J-4** "Is the figure the same person in every frame?"
- **J-5** "Does the loop repeat without a visible jump at the join?"
- **J-6** "Does the way the staff is held read as a **staff**, or as a club / a walking cane / a spear?" *(the PoE2 defect turned into a question — § 1.7)*
- **J-7** "Are the eyes looking in one consistent direction throughout, or do they shift?"
- **J-8** *(known-bad control)* a mirrored or repeated-lead variant drawn from `known_bad_factory.py` — a judge that passes its control voids the batch.

**Deliberately NOT asked of the judge**, because a gate answers it better and the judge answers it worse: bob amplitude, sole slip, arm-swing amplitude, frame counts, loop-seam magnitude. **Deliberately NOT asked of the gates**, because no closed form exists: J-1, J-6, and the "does the action read" half of the silhouette test.

### 5.6 The pose-guide spec — per-phase foot/sole table (first-party by construction)

**This table is my own construction from the VERIFIED phase rules of § 1, expressed in the anthropometric constants of § 5.3. It contains no third-party pixels and no traced reference — `lane/ref_provenance.py` has nothing to refuse.** Origin at the figure's root (mid-hip projected to the ground line); +x = direction of travel; step length **S = 0.42 H**. An 8-frame full cycle, profile facing, LEFT leg leading.

| Frame | Phase | LEFT sole (x, y) | RIGHT sole (x, y) | Head-top y | Notes |
|---|---|---|---|---|---|
| 1 | **CONTACT** (L heel strikes) | (+S/2, 0) **plant begins** | (−S/2, 0) **plant ends** | mediant | both soles down; legs at max spread |
| 2 | **DOWN** | (+S/4, 0) planted | (−3S/4, ~0.02 H) swinging up | **minimum** | L knee bends; **arms at their widest** |
| 3 | **PASSING** | (0, 0) planted | (0, +0.01 H) passing, min clearance | slightly above mediant | L leg straight; hips + shoulders level; head tilt applied |
| 4 | **UP** (push-off) | (−S/4, 0) planted, heel lifting | (+S/4, ~0.02 H) swinging forward | **maximum** | L ball/toe drives |
| 5 | **CONTACT** (R heel strikes) | (−S/2, 0) **plant ends** | (+S/2, 0) **plant begins** | mediant | mirror of frame 1 |
| 6 | **DOWN** | (−3S/4, ~0.02 H) swinging up | (+S/4, 0) planted | **minimum** | mirror of 2 |
| 7 | **PASSING** | (0, +0.01 H) passing | (0, 0) planted | slightly above mediant | mirror of 3 |
| 8 | **UP** | (+S/4, ~0.02 H) swinging forward | (−S/4, 0) planted, heel lifting | **maximum** | mirror of 4 |

**Invariants the guide asserts — what `pose_guide.py` should draw and `gait_oracle.py` should check:**
1. The planted sole's x decreases by **S/4 = 0.105 H per frame**, monotonically, for its four planted frames.
2. Exactly one sole is planted per frame, except frames 1 and 5 where two are.
3. The two legs' plant windows are **disjoint, equal in length (4 frames each), and offset by exactly half the cycle**.
4. Head-top y traverses **two** full minima and two maxima per cycle; minima at 2 and 6, maxima in {3,4} and {7,8}.
5. Frames 5–8 are the **mirror** of frames 1–4 with left/right swapped.
6. The numbered-foot guide is a silhouette with the two soles labelled **`1` (planted)** and **`2` (swinging)** per frame; the labels swap at frames 1 and 5 and nowhere else.

> **Why invariant 5 matters more than it looks.** An 8-direction × 8-frame walk sheet is **not 64 independent images**. It is **32 images plus a mirror relation** — and the mirror relation is itself a free correctness gate. In a lane paying an image call per frame that is a real budget finding; it is also exactly the structure that would have caught the K2 near/far inversion (ledger R-15) by construction rather than by eye.

---

## 6. R10b ADDENDUM — oracle candidates in BOTH forms (frame sheet + video)

> **Matt's addendum, 2026-09-12:** every oracle candidate must exist as **both** a frame sheet and a video Matt can put side by side — either sourced as both, or one derivable from the other (video → frames at a stated fps; sheet → an assembled loop). The extraction/assembly is conductor tooling (ffmpeg); my job is to make sure the inputs exist and are legally usable.

### 6.1 Sourcing classes — aligned to the OPEN queue row, not to a presumed ruling

`canonical/matt_decision_needed/2026-08-25-youtube-frame-extraction-sourcing-class.md` is **OPEN**. It asks whether frame extraction from published YouTube videos is an authorized sourcing class, offering **(a) YES broadly** · **(b) YES narrow — publisher-official channels only** · **(c) NO — the donor/CDN structure is the ceiling**. The conductor's lean is **(b)**; the filing explicitly says *"this is sourcing posture, not design"* and *"Your call."* **I do not assume a ruling and nothing below depends on one.** Note the row's own framing of intended use — *"internal measurement only (frame forensics, blind-extraction input, judge-panel input). Nothing republished, nothing shipped"* — which is exactly our use here.

I classify every candidate into one of five classes, and only class **E** is gated on that row:

| Class | Meaning | Measurement? | Showable as a visible reference? | Gated on the open row? |
|---|---|---|---|---|
| **A — Public domain / CC0** | no rights reserved | ✔ | ✔ | **no** |
| **B — CC-BY / CC-BY-SA** | open, attribution (and for SA, share-alike) required | ✔ | ✔ with attribution; **SA is viral — prefer BY** | **no** |
| **C — Vendor freeware, use-only** | use permitted, redistribution forbidden, silent on AI | ✔ | ✘ do not redistribute | **no** |
| **D — Vendor freeware, AI-prohibited** | licence names "testing, validating" AI systems as forbidden | **✘** | ✘ | **no — it is simply excluded** |
| **E — Published-video frame extraction** | frames cut from a published gameplay/showcase video | **GATED** | **✘ assume not** | **YES** — and sub-split: **E1** publisher-official channel (authorized if Matt rules **b** or **a**) vs **E2** third-party upload (authorized only under **a**) |

> **The one thing I would put in front of Matt before he rules:** class **D** is not hypothetical. **CraftPix's licence forbids using its assets for "testing, validating" AI systems by name** (§ 5.2, verbatim and verified). That means *judge-anchoring* can be prohibited by a licence **even when generation-conditioning is not at issue** — so the judge-anchor refinement and the generation-reference rule are **two separate questions**, and at least one vendor has already answered one of them for us. **Class A is the only class that is unconditionally clean on every axis**, which is an independent third reason (after "frame-accurate" and "free") to make Muybridge the first-choice oracle.

### 6.2 The candidate table — every row in both forms

**Every licence below was read by me on the source page or via the Commons API.** "Derivable" means the other form does not exist as published but can be produced by conductor tooling from what does.

| # | Candidate | Sheet form | Video form | Native fps / frames | Resolution | Camera | Register | Licence | Class |
|---|---|---|---|---|---|---|---|---|---|
| **M1** | **Muybridge plate 2 — man walking** | ✔ **have it**: `refs/B19801099.jpg`, Wellcome `b19801099` | ✔ **exists**: [`Muybridge human male walking animated.gif`](https://commons.wikimedia.org/wiki/File:Muybridge_human_male_walking_animated.gif) — **the lateral row of the same plate 2**, 12 frames | **12 frames/stride; native 0.120 s/frame ⇒ 8.33 fps** (Prospectus, § 5.1.2). ⚠ the Commons GIF plays at ~0.33 s/frame ≈ 3 fps — **slowed by the uploader, not Muybridge's rate** | sheet **7628 × 6049**; GIF 404 × 725 | **profile (lateral)** | photographic | sheet **PDM 1.0**; GIF **Public domain**, no restrictions | **A** |
| **M2** | **Muybridge plate 13 — woman walking** | ✔ **have it**: `refs/B19801555.jpg`, Wellcome `b19801555` | **derivable** — assemble the lateral row at **8.33 fps** | 12 frames/stride | **7628 × 6049** | **profile + front + rear** on one plate | photographic | **PDM 1.0** | **A** |
| **M3** | **Muybridge plate 34 — woman walking with a head load** | derivable from the GIF, or from the BPL/Wellcome plate | ✔ **[Full plate animated](https://commons.wikimedia.org/wiki/File:Animal_Locomotion_I,_Plate_34_-_Nude_woman_walking_and_carrying_basket_on_head_-_Full_plate_animated.gif)** — **animates all THREE camera rows simultaneously**; also a [top-row-only](https://commons.wikimedia.org/wiki/File:Animal_Locomotion_I,_Plate_34_-_Nude_woman_walking_and_carrying_basket_on_head_-_Top_row_animated.gif) version | 12 phases | 485 × 1194 (full) / 518 × 1194 (top row) | **profile + ~60° front-oblique + 90° rear, synchronised** | photographic | **Public domain**, no restrictions | **A** |
| **M4** | **Muybridge plate 175 — crossing a brook with a fishing pole** | ✔ NGA scan **3985 × 1628** | derivable | not read | 3985 × 1628 | profile | photographic | **CC0** (NGA open access) | **A** |
| **M5** | Muybridge plates **530 / 531** "Various poses" — the nearest thing to an idle | ✔ BPL 5044 × 3996 / 4964 × 3976 | derivable | not read | ~5000 × 4000 | profile + others | photographic | public domain | **A** |
| **P1** | **Isometric Painted Game Assets** — laetissima, [OGA](https://opengameart.org/content/isometric-painted-game-assets) | ✔ sheet in the pack | ✔ **`walking.gif` served on the page** | not stated | not stated | isometric | **genuinely painted** | **CC0** | **A** |
| **P2** | **Isometric: Mini-Crusader** — Bleed, [OGA](https://opengameart.org/content/isometric-mini-crusader) | ✔ 8-direction sheets, **idle + walk + run + attack** | **derivable** — assemble each direction's strip into a loop | not stated | not stated (24.3 MB pack) | **elevated 3/4 — the correct camera** | pre-rendered 3D, reads illustrated | **CC-BY 4.0**, attribution `Bleed - http://remusprites.carbonmade.com/` | **B** |
| **P3** | **KayKit Character Animations** — Kay Lousberg, [OGA](https://opengameart.org/content/kaykit-character-animations) | **derivable** — render the rig at our camera and slice | ✔ **three GIFs served on the page**; also itch previews from multiple angles | you choose | you choose | **you choose** — park the camera at our elevation | rendered 3D | **CC0** | **A** |
| **P4** | **Hand-Drawn Square Characters** — rgsdev, [OGA](https://opengameart.org/content/hand-drawn-square-characters-animated-8-directions-top-down-free-cc0) | ✔ 8-direction sheets, idle + walk | ✔ **five GIFs** | not stated | 128 × 128 | top-down (wrong camera) | hand-drawn; *"No generative AI was used"* | **CC0** | **A** |
| **P5** | **Isometric Hero and Heroine** — Clint Bellanger, [OGA](https://opengameart.org/content/isometric-hero-and-heroine) | ✔ 8 dir, Stance 4 f + Run 8 f | **derivable**; and the **`.blend` source ships** (14.8 MB) so it can be re-rendered at any elevation and any frame count | 4 f / 8 f | 128 × 128 | isometric | Blender-rendered | **CC-BY 3.0** | **B** |
| **X1** | Reiner's Tilesets — 2D Humans | ✔ ~80 characters, `Stopped` + `Walking`, 8 dir | derivable **for internal viewing only** | not stated | not stated | **`Isoformat 4:3`** | pre-rendered 3D, painterly-soft | freeware: commercial use OK, credit requested, **redistribution forbidden** | **C** |
| **X2** | SmallScaleInt HD 8-Directional Pack 1 | ✔ idle ×3 + walk + run + strafe, 8 dir | ✔ GIFs on the page | not stated | 128 × 128 | top-down | 3D over-painted | invented "Standard Commercial License", **$9.95**, no redistribution | **C** |
| **X3** | CraftPix free tier | ✔ | ✔ | — | — | side-view | pixel | ⛔ *"may not be used… for the purposes of training, fine-tuning, developing, **testing, validating**, or improving any artificial intelligence…"* | **D — EXCLUDED** |

### 6.3 The recommendation, in one line each

- **Measurement oracle, first choice: M1 + M2 (Muybridge plates 2 and 13).** Frame-accurate by construction, public domain on both forms, already downloaded with licence sidecars, and **M3 additionally gives the profile / ~60°-oblique / rear split synchronised on one artifact** — which is exactly the facing split § 4 concluded the gate set needs. **Assembly fps for a faithful loop is 8.33 fps** (Muybridge's own 0.120 s interval), *not* the ~3 fps the Commons GIF happens to play at.
- **Painted-register candidate in both forms: P1 (laetissima, CC0, sheet + `walking.gif`).** It is the only genuinely *painted* isometric character under CC0 with a published loop. Its limits are real and must travel with it: **4 directions, walk only, no idle.**
- **Best camera match: P2 (Mini-Crusader, CC-BY 4.0).** Correct elevated three-quarter, 8 directions, **real idle and real walk** — the video form is assembled, not sourced. If only one painted-ish asset is pulled, this is the one; record the attribution string.
- **Most flexible: P3 (KayKit, CC0).** Not painted, but a CC0 *rig* can be parked at our exact camera elevation and scrubbed frame by frame — for the question actually being asked (*how does motion distribute across a cycle*), a rig beats any baked sheet.
- **Staff-carry reference: M4 (plate 175, CC0)** is the only public-domain frame sequence of a figure locomoting while carrying a long shaft — and it is stepping-stone walking, not level walking. **There is no clean public-domain level-walk-with-a-staff reference. That gap is real and I could not close it.**

### 6.4 Class-E — published-video frame extraction

Matt's addendum names painted-2D animation **videos** (developer showcase reels, gameplay captures, animator breakdowns) as a first-class sourcing path. **Everything in that path is class E and therefore gated on the open 2026-08-25 queue row.** What I can say without pre-empting the ruling:

- **Under (c) NO**, the path closes entirely and classes A–C above are the ceiling. **The deliverable survives that ruling** — M1–M5 and P1–P3 are all class A or B and none of them depends on video extraction.
- **Under (b) YES-narrow**, only **publisher-official channels** qualify (E1). For our register that means a studio's own channel — Supergiant's own Hades material, a developer's own devlog — and **not** a third-party gameplay upload, however good the footage.
- **Under (a) YES-broad**, E2 opens as well.
- **In all three cases the row's own scope holds: internal measurement only, nothing republished, nothing shipped.** So even under (a), class-E frames tune thresholds and inform prompts; they are **not** showable as a visible reference and they never condition a mint (`ref_provenance.py`, unchanged).

**The practical consequence, and it is a comfortable one:** the oracle does not need the ruling. Muybridge is public domain in both forms, and a CC0/CC-BY painted candidate exists in both forms. **Class E would widen the reference base; it does not gate the lane.** That is worth saying plainly, because it means the R10b oracle can be stood up now and the queue row can resolve on its own timetable.

---

## 7. Knowledge gaps not resolved

Two passes each, then recorded. Grouped by whether the gap is *closable* (someone has the number and I could not reach it) or *open* (nobody has published it).

### 7.1 Closable — the number exists, I could not reach it

| # | Gap | What I tried | Next source |
|---|---|---|---|
| G1 | **Orendurff et al. 2004 primary text** — the vertical (2.74 → 4.83 cm) and mediolateral (6.99 → 3.85 cm) CoM excursions are the spine of § 1.4/§ 1.5 and I have them only as search extracts | PubMed 15685471 returned a cookie wall; the CiteSeerX "PDF" served HTML; Europe PMC served a nav shell | *J Rehabil Res Dev* 41(6), Nov–Dec 2004, doi **10.1682/JRRD.2003.10.0150** — the journal is open-access at its own site |
| G2 | **Arm-swing normative amplitude in degrees.** I report **24.6° ± 3.4°** (and a 20–26° band) as **SECONDARY** because **I opened two candidate primaries and neither prints it**: Leardini et al., *PLoS One* 8(10):e77168 reports only group differences; Killeen et al., *Sci Rep* 8:12803 reports asymmetry indices and speeds (1.29 / 1.57 / 1.30 m/s), not absolute amplitudes | both fetched and read | Hejrati et al., *Human Movement Science* (the comprehensive arm-swing-vs-speed-and-slope study) — the PDF I fetched was unparseable; get it via the publisher |
| G3 | **Hirasaki, Moore, Raphan & Cohen (1999)** head-translation amplitudes per walking velocity | Springer redirected to an auth wall | Exp Brain Res 127(2); or the authors' institutional copy |
| G4 | **Pozzo, Berthoz & Lefort (1990)** head-pitch ~4–5° figure | same auth wall | Exp Brain Res 82 |
| G5 | **The Lissajous figure-8 paper** — quoted from a search extract of the abstract, which is the load-bearing citation under § 5.4's reconciliation | ScienceDirect returned 403 | *J Biomech* (2020), S0021929020303705 |
| G6 | **Hades' engine-default `PlaySpeed`** — without it `ZagreusIdle` (120 frames) is **either 2.0 s or 4.0 s** and I cannot say which | read the whole 731-record sjson; the field is simply absent on that record | the engine binary, or a Supergiant statement |
| G7 | **A Diablo II player `.cof` header parsed directly** — "16 directions" rests on two d2mods statements plus the arithmetic agreement (128 total ÷ 16 = 8, which matches the VERIFIED frame count) | parsed `AnimData.D2` (which has no direction field) and `monstats2.txt` (which covers monsters only) | any player `.cof`; byte 2 is the direction count |
| G8 | **Muybridge's per-plate intervals for plates 2, 13, 175, 530, 531.** I have plate 14's (0.120 s) from the worked example; the catalogue prints every plate's in a table I did not read | located the catalogue scan and confirmed IIIF resolves | `archive.org/details/animallocomotion00muyb`, the interval column |
| G9 | **D2R's GDC 2022 "Bringing Diablo II into the 3rd Dimension"** | paywalled; abstract only | GDC Vault subscription |
| G10 | **PoE's `.ast` per-clip framerate byte** — the field is confirmed by three independent parsers; **no one has published a value** | three parser sources read | a GGPK extraction |

### 7.2 Open — nobody appears to have published it

| # | Gap | Evidence that it is genuinely open |
|---|---|---|
| **G11** | ⚑ **THE EXAGGERATION MULTIPLIER.** Williams states plainly that a faithfully traced walk *"floats"* and that the animator must *"increase the ups and the downs."* **Nowhere does he, or anyone I found, say BY HOW MUCH.** Every amplitude threshold in § 5.4 has a defensible *floor* (the biomechanical value) and a ceiling I set by judgement. **This is the single most consequential unquantified number in the document**, and the only way to close it is to measure our own approved anchors — which is precisely what pre-registration on K1/K3 would produce. |
| G12 | **Per-clip frame counts for Grim Dawn and Titan Quest.** The fps is known (30, from the file headers); the counts are not published for any named clip. |
| G13 | **Last Epoch — nothing numeric anywhere.** No asset dumps, no clip names, no fps, no blend-tree description. Dev posts are qualitative by design. Two passes, both empty. |
| G14 | **Any shipped ARPG animating EYES during locomotion.** Two passes, both negative — and § 1.8 gives a structural reason (at 50–400 px figure height an eye is 1–4 px). I report the negative as a negative, not as a finding that it never happens. |
| G15 | **A published artifact taxonomy for painted / illustrated generation.** Carried forward unchanged from R6–R8: CHI 2025 "exclusively examined photorealistic diffusion model outputs." |
| G16 | **Any published QA practice for validating a GENERATED cycle**, as opposed to an authored one. Every source in § 3 assumes an animator who cannot accidentally redraw the character between frames. **Our dominant failure mode is outside the entire literature.** |
| G17 | **Any published per-frame numeric tolerance** for onion-skin drift, arc smoothness, loop-seam magnitude or key distinctness. The trade's checks are all ordinal ("smoother", "reads better"). Every number in § 5.4 is mine. |
| G18 | **A clean public-domain level-walk-with-a-staff reference.** Muybridge plate 175 is the only PD sequence of a figure locomoting with a long shaft and it is stepping-stone walking. Plates 49/552 are canes, which are supports not staves. |
| G19 | **The four-way intersection** painted register × elevated 3/4 camera × idle AND walk × 8 directions × named open licence. **Empty set** across nine surveyed sources (§ 5.2). This is a *result*, not a failure to look. |
| G20 | **Whether D2's 8-frame `WL` encodes one step or two.** 8 frames at 25 fps = 0.32 s; read as a full cycle that is 6.25 steps/s (a sprint), read as one step it is 3.1 steps/s — which lands *exactly* on Williams' "cartoon walk, 3 steps a second." A looping game walk normally contains both steps, which argues for the first reading; the tempo argues for the second. **I could not settle it and I am not going to guess.** |
| G21 | **Whether a licensed reference may serve as a JUDGE ANCHOR.** Not mine to resolve — but § 5.2 and § 6.1 establish that *the licences already differ on it* (CraftPix forbids "testing, validating"; CC0/CC-BY do not), so the question is factual before it is a matter of policy. |

---

## 8. Source list

All accessed **2026-09-12** unless stated. Grade is for *my access to the source*, not for the source's own quality.

### 8.1 Animation practice — primary

| ID | Source | Read | Grade |
|---|---|---|---|
| S01 | **Richard Williams, *The Animator's Survival Kit*, "WALKS", pp. 102–125.** Scanned excerpt, Carnegie Mellon: `https://graphics.cs.cmu.edu/nsp/course/15464-s17/lectures/Animators_Survival_Kit_walks.pdf` (mirror `https://www.cs.cmu.edu/~15464-s13/handouts/Animators_Survival_Kit_walks.pdf`) | **24 pages read as images**; every quote transcribed from the page | **VERIFIED** |
| S02 | Monmouth University animation instruction — walk cycle key frames `https://animation.monmouth.edu/instruct/animation/walk-cycle/` | full fetch | PRACTITIONER-REPORT |
| S03 | MoCap Online, *Idle Animation for Games: Design Guide* `https://mocaponline.com/blogs/mocap-news/idle-animation-game-dev-guide` | full fetch | PRACTITIONER-REPORT |
| S04 | MoCap Online, *Walk Cycle Animation: Game Engine Integration* `https://mocaponline.com/blogs/mocap-news/walk-cycle-animation` | via search extract | PRACTITIONER-REPORT |
| S05 | Animation Mentor / AnimSchool / CAVE Academy / Trau Studios — breathing loops, arcs, onion-skin, squint test | via search extracts | PRACTITIONER-REPORT |
| S06 | Yacht Club Games, *Creating a Shovel Knight Character Sprite* — *"Our idles are generally all 2 frames… Just a gentle bob."* | via agent, quoted | VERIFIED† |
| S07 | Pedro Medeiros (saint11) pixel walk/idle tutorials | via agent | VERIFIED† |

### 8.2 Biomechanics

| ID | Source | Read | Grade |
|---|---|---|---|
| S08 | **Ling, Zinno, Cheng & van de Panne, *Character Controllers Using Motion VAEs*, ACM TOG 39(4) Art. 40 (SIGGRAPH 2020)** — the foot-skate metric `s = d(2 − 2^(h/H))`, **H = 3.3 cm**, mocap baseline **0.10 cm/frame** | **PDF downloaded and text-extracted; § 7.2 + Table 1 quoted verbatim** | **VERIFIED** |
| S09 | **Drillis & Contini (1966)**, reproduced as Figure 4.1 in Winter, *Biomechanics and Motor Control of Human Movement* `https://courses.grainger.illinois.edu/me481/sp2021/Anthro-Winter.pdf` | **figure read as an image**; all ×H constants transcribed | **VERIFIED** |
| S10 | Orendurff et al., *The effect of walking speed on center of mass displacement*, J Rehabil Res Dev 41(6), 2004, doi 10.1682/JRRD.2003.10.0150 | **two independent search extracts agreeing exactly**; primary blocked (G1) | SECONDARY |
| S11 | Orthofixar, *Gait Cycle: Phases, Biomechanics and Common Abnormalities* `https://orthofixar.com/basic-science/gait-cycle/` — stance/swing 60/40, double support 12 %, vertical 5 cm, lateral 5–6 cm (**internally inconsistent — flagged, not averaged**) | full fetch | SECONDARY (tertiary teaching page) |
| S12 | *Speed- and mode-dependent modulation of the center of mass trajectory in human gaits as revealed by Lissajous curves*, J Biomech 2020, S0021929020303705 — the **1-cycle ML / 2-cycle vertical → figure-8** result | abstract via search extract; ScienceDirect 403 (G5) | SECONDARY |
| S13 | Hirasaki, Moore, Raphan & Cohen, *Effects of walking velocity on vertical head and body movements during locomotion*, Exp Brain Res (1999) | abstract via search extract; Springer auth wall (G3) | SECONDARY |
| S14 | Pozzo, Berthoz & Lefort, *Head stabilization during various locomotor tasks in humans I*, Exp Brain Res (1990) | via search extract (G4) | SECONDARY |
| S15 | Minimum-toe-clearance literature — *Minimum toe clearance: probing the neural control of locomotion*, Sci Rep 2017 (s41598-017-02189-y); MTC mean 14.1 ± 8.3 mm via PMC4499197 | search extracts | SECONDARY |
| S16 | Leardini, Berti, Begon & Allard, *PLoS One* 8(10):e77168 (2013); Killeen et al., *Sci Rep* 8:12803 (2018) | **both fetched and read — neither prints a normative arm-swing amplitude** (G2) | VERIFIED (as negatives) |
| S17 | Wurdeman et al., Sci Rep 2017 (s41598-017-17532-6) — CoM vertical displacement, curved vs flat treadmill; the Saunders six-determinants framing | PMC5719393 fetched | SECONDARY |
| S18 | Load-carriage gait literature (unilateral/asymmetric load → arm-swing restriction, phase asymmetries) | search extracts | SECONDARY |

### 8.3 Shipped-game data — read from files, not articles

| ID | Source | Read | Grade |
|---|---|---|---|
| S19 | **Diablo II `AnimData.D2`** — binary, 3,558 × 160-byte records parsed to EOF; cross-checked against the independent text decompile at `https://github.com/youbetterdont/pydiablo/blob/master/pydiablo/data2/animdata.txt` | via agent; **two independent parses agree byte-for-byte** | **VERIFIED†** |
| S20 | **Phrozen Keep, *Diablo II Animation Conversion Extended Tutorial*** `https://d2mods.info/resources/infinitum/tut_files/dcc_tutorial/chapter2.html` — the `.cof` naming scheme, mode codes, weapon-class codes (`staf` and `club` are **separate** classes), "For every direction an animation has the same number of frames" | **full fetch by me** | **VERIFIED** |
| S21 | `monstats2.txt` direction columns (dNU/dWL/dRN = 8 on 509–553 of 610 monster rows) | via agent | VERIFIED† |
| S22 | Paul Siramy, *Extracting Diablo II Animations* (archive.org) + OpenDiablo2 `animdata.go` (`speedDivisor = 256`, `speedBaseFPS = 25`) | via agent | VERIFIED† |
| S23 | **Hades `CharacterAnimationsHero.sjson`** (731 records) + `CharacterAnimationsNPCs.sjson` | via agent; **cross-validated against Supergiant's own published "104 frames × 32 angles = 3,328"**, which matches `ZagreusBowDash*` exactly | **VERIFIED†** |
| S24 | Jen Zee (art director, Supergiant), MCV/DEVELOP *"Behind the art of Hades"* — *"We relied completely on Photoshop… The 3D work was modeled and animated with Maya"*; *"our animator, Thinh used mocap as a basis for a large chunk of animation"*; *"32,494 FX animation frames and 942,489 character and enemy animation frames"* | **full fetch by me** | **VERIFIED** (quotation); PRACTITIONER-REPORT (content) |
| S25 | Grim Dawn `anm_malepc.dbr` / `anm_femalepc.dbr` — 9 stance families; **`staff*` and `spear*` all point at `hero01_sword1h_*`**; walk shared across 7 of 8 stances | via agent | VERIFIED† |
| S26 | GrimDawner `GameData.md` — **30 fps in every one of the 2,021 shipped `.anm` files** | via agent, **spot-checked at line 361** | VERIFIED† |
| S27 | Torchlight II `Ogre.log` v1.25.9.5 — player rig **23 `IDLE_*` (incl. `IDLE_STAFF`), 14 `RUN_*`, 0 `WALK`** | via agent, **log re-grepped** | VERIFIED† |
| S28 | Path of Exile `DexInt.aoc` / `StrDexInt.aoc` — **24 `run_*` per class incl. `run_staff`; zero `walk`, zero `idle` strings** | via agent | VERIFIED† |
| S29 | Titan Quest `.anm` header (u32 numBones / numFrames / **fps**; fps = 30) via Noesis `fmt_TQ_msh.py` and `tqvaultc anm.h` | via agent | VERIFIED† (format) / SECONDARY-derived (the value) |
| S30 | Rob Gallerani / Andre Abrahamian / Chris Amaral on D2R — *"all of the logic and the simulation is still being run by sprites… at the original framerate"*; *"we are still being true to that 25 FPS"* (Eurogamer + community transcript) | via agent | VERIFIED (Eurogamer) / SECONDARY (transcript) |
| S31 | Celeste `Sprites.xml` — idle 9 f @ 10 fps, walk 12 f @ 16.7 fps, runFast 12 f @ 20 fps | via agent (skin template, not an install — caveat recorded) | VERIFIED† |
| S32 | Unity `SpriteUtility.cs` `newClip.frameRate = 12;`; Godot `sprite_frames.h` 5.0; GameMaker 30; Aseprite 100 ms | via agent | VERIFIED† |
| S33 | Path of Exile official forum, "Staff Animation" thread — *"sorcerer characters in Path of Exile 2 hold their staff like a club"* (player; no GGG reply) | **full fetch by me** | TERTIARY |

### 8.4 Camera / projection

| ID | Source | Read | Grade |
|---|---|---|---|
| S34 | Wikipedia, *Isometric video game graphics* — 2:1 ratio ⇒ **≈26.565° (arctan ½)**; dimetric (116.565° / 116.565° / 126.870°); Diablo II fixed-perspective 2D | **full fetch by me** | **VERIFIED** |
| S35 | Pixel Parmesan, *Fundamentals of Isometric Pixel Art* — *"26.5 degrees rather than the mathematically accurate 30"* | **full fetch by me** | PRACTITIONER-REPORT |

### 8.5 Oracle artifacts — plates, sheets, licences

| ID | Source | Read | Grade |
|---|---|---|---|
| S36 | **Wellcome Collection IIIF manifests `b19801555` (plate 13) and `b19801099` (plate 2)** — 7628 × 6049, **PDM 1.0**, plate numbers from each record's own Prospectus citation | **manifests fetched and parsed by me**; both images downloaded to `refs/` | **VERIFIED** |
| S37 | **Muybridge, *Animal Locomotion: Prospectus and Catalogue of Plates* (Lippincott, 1887)** — `archive.org/details/animallocomotion00muyb` (Getty, 52 canvases, 3319 × 4638) and `cu31924024580353` (Cornell). **12 phases; 0.120 s interval; 36 figures; lateral battery of 24; E at 90°; F averaging 60°** | via agent, quoted from the scan | **VERIFIED†** |
| S38 | Muybridge 1888 Penn monograph `animallocomotion00univ` — the plate 549/555/558/559 errata | via agent | VERIFIED† |
| S39 | **Wikimedia Commons `Muybridge human male walking animated.gif`** — plate 2, lateral row, 12 frames, 404 × 725, **Public domain, no restrictions** | **Commons API read by me** (`iiprop=extmetadata`) | **VERIFIED** |
| S40 | **Commons `Animal Locomotion I, Plate 34 — Full plate animated.gif`** (485 × 1194) and **Top row animated** (518 × 1194) — **Public domain**; the full-plate version animates all three camera rows | **Commons API read by me** | **VERIFIED** |
| S41 | **Commons / NGA `Plate 175. Crossing brook on stepping-stones with a fishing pole and can`** — 3985 × 1628, **CC0** | **Commons API read by me** | **VERIFIED** |
| S42 | Boston Public Library Muybridge collection — plates 7, 13, 16, 176/177, 530, 531 at ~5000 × 4000 | via agent | VERIFIED† |
| S43 | **OGA `isometric-mini-crusader`** — **CC-BY 4.0**, attribution `Bleed - http://remusprites.carbonmade.com/`; 8 dir; idle+walk+run+attack; no GIF | **full fetch by me** | **VERIFIED** |
| S44 | **OGA `kaykit-character-animations`** — **CC0**, *"Free for personal and commercial use, no attribution required. (CC0)"*; Idle + Walk present; three GIFs on page | **full fetch by me** | **VERIFIED** |
| S45 | **OGA `isometric-painted-game-assets`** (laetissima) — **CC0**; painted; 4 dir; walk only, no idle; `walking.gif` on page | **full fetch by me** | **VERIFIED** |
| S46 | **Reiner's Tilesets licence page** `reinerstilesets.de/graphics/lizenz/` — commercial use OK, credit requested, **redistribution forbidden**, no AI clause | **full fetch by me** | **VERIFIED** |
| S47 | **CraftPix file licences** `craftpix.net/file-licenses/` — ⛔ *"may not be used… for the purposes of training, fine-tuning, developing, **testing, validating**, or improving any artificial intelligence…"* | **full fetch by me** | **VERIFIED** |
| S48 | OGA `hand-drawn-square-characters…` (rgsdev, CC0), `isometric-hero-and-heroine` (Bellanger, CC-BY 3.0), itch `8-directional-knight` (Hormelz, CC0), itch SmallScaleInt ("Standard Commercial License") | via agent, each licence string read from page HTML | VERIFIED† |
| S49 | Universal LPC Spritesheet Generator — `DIRECTIONS = ["up","left","down","right"]` read from `sources/state/constants.ts`; per-asset CC0/CC-BY/CC-BY-SA/OGA-BY/GPL | via agent | VERIFIED† |

### 8.6 Project documents consulted

`canonical/00-ground-state.md` · `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` · `astra_test_01/burst/SPEC.md` §§ 1, 6 (T1 row, T0-e) · `canonical/reap-die-rise-story/style-register.md` · `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md` § 0 (grading key, R8 oracle shortlist) · `canonical/matt_decision_needed/2026-08-25-youtube-frame-extraction-sourcing-class.md` (**OPEN**) · `agentic_orchestration/operating-procedures/legolas.md` § 1.

**Not read, per the commission:** `astra_test_01/design/` (HISTORICAL), `astra_test_01/burst/runs/`, `astra_test_01/burst/briefs/`.
