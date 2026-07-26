# TCP-L8-U3c (RE-DISPATCH) — the box is retired, the backing is a MATERIAL, and the instrument was the cell

**Agent:** drax (presentation seam) · **Dispatch:** `2026-07-25-drax-l8u3c-r-hotbar-backing.md`
**Supersedes execution of:** `2026-07-25-drax-l8u3c-hotbar-unbox.md` (read for lineage only)
**Floor:** `~/Games/mcp-lab/l8ui/`, extending `ui3b/` as `ui3c/`. Arms 1, 2, 3, 3b byte-identical at close.
**Status:** COMPLETE

---

## §1 — CLOCK, DECLARED IN TWO SEGMENTS (TCP-52 ⑦), AND THE DISPATCH'S OWN CLOCK IS WRONG BY 5×

| segment | span (UTC) | wall | attribution |
|---|---|---|---|
| **1 — prior, stopped** | 02:38:11Z → 03:09:05Z | **30 m 54 s** | **UNATTRIBUTABLE** |
| GAP | 03:09:05Z → 03:15:34Z | 6 m 29 s | not work |
| **2 — this segment** | 03:15:34Z → **03:40:47Z** | **25 m 13 s** | attributable |

**Not summed**, per arm 3's two-segment precedent.

★ **§0 and §3.1 both call segment 1 "~6 minutes." Measured from disk it is ~31.** Segment
1's FIRST_INTENT is timestamped 02:38:11Z and its last write — `ninepatch_probe2.py` — is
03:09:05Z. **The only ~6-minute interval on the whole clock is the gap between that last
write and my relaunch (6 m 29 s).** I do not know which gandalf measured and I am not
asserting a cause I have not measured (L-Q). It matters twice, and §9.2 carries it.

**FIRST_INTENT is banked twice and NEITHER is reconstructed.**
Segment 1's — genuinely pre-work, written against the superseded dispatch — is at
`…/2026-07-25-tcp-l8u3c-FIRST_INTENT.md`, unedited.
Segment 2's — a new cell under L-R — is at `…/2026-07-25-tcp-l8u3c-R-FIRST_INTENT.md`,
**labelled with exactly what I had already read when I wrote it.** It was not possible to
write a pure pre-work intent for a re-dispatch of a cell I had already run, and dressing
one up would have been worth less than saying so.

---

## §2 — ★ THE STOPPED CELL HAD ALREADY SHIPPED THE FORBIDDEN THING. IT IS NOT A COUNTERFACTUAL; IT IS ON DISK

The re-dispatch predicts I would optimise toward deletion. **Two independent receipts say
it was right, and the second is not an inference.**

**Receipt 1 — the framing landed on the first sentence.** Segment 1's FIRST_INTENT opens:
*"I am going to delete a box and then discover that the box was load-bearing."* The verb is
**delete**. That is v1's §2 arriving intact before I had opened a file. (The same document
partly resisted it — *"I am not removing a family, I am swapping one"* — so the steer
captured the framing and not the analysis.)

**★ Receipt 2 — the deletion was rendered.** `out3c/T2_wings.png` and `out3c/T2_candles.png`,
written 03:07:47Z and 03:07:50Z — **two minutes before the stop** — are 1920×1080 stills at
the play camera showing **nine skill slots sitting on bare stone with no plate behind them
and the wings-and-skull crest floating unattached above the row.** That is zero-backing,
the outcome §1.2 declares out of scope, at the owner's eye.

**In my segment-2 FIRST_INTENT I wrote that gandalf's counterfactual was unproven and that
I would rather say so than accept a compliment I could not support. I was wrong, and the
correction goes the other way: it is proven.** Both stills are kept.

**Why the build got there is worth more than the fact that it did.** The candles branch
**was already drawing the plate** — `_np(T, P.TRAY_C_PLATE, r, 40, 40, 0, 0, P.PLATE)` was
on line 544 the whole time. The plate was not missing. It was tinted to `P.PLATE`, Y =
0.054, and it was invisible. **A cell steered toward subtraction removed the object it
believed it had removed, and did not check that the object it kept was doing anything.**

---

## §3 — THE FORK RESOLVED: **CANDLES**. Veto-open, with four reasons and none of them taste

I looked at both panels before reading anything about them, formed a read, and **my banked
read was wrong about the bat wings**, which is why the picture goes in the report and not
the impression.

**What I banked:** *"The bat-wings panel is a hotbar with NO OUTER BRACKET AT ALL … what
sits behind the row is a dark plate barely wider than the slots."*

**What the 2× overlay shows:** a **continuous dark backing that spans the full strip, passes
behind the globes, and rises into the wing silhouettes around the centre skull.** It is
there, it is large, and I missed it at thumbnail scale **because it is dark and
low-contrast — which is the same property that made our own plate invisible.** The two
failures have one cause and it is the cause Matt's second ruling is about.

**The reasons, in decreasing strength:**

1. ★ **The candles exemplar is the only one whose globe treatment matches our ratified
   build.** `PANEL_candles` has lit candles crowning both globes. `PANEL_batwings` has
   none — it has wings there instead. §1.1 forbids regressing the candle VFX, so choosing
   bat wings means either dropping ratified work or shipping a composition **the sheet's
   own author never shows**. That is a structural argument, not a preference.
2. ★ **The kit ships the candles exemplar's structure as a matched pair and ships nothing
   equivalent for the wings.** `Frame_Hotbar_03` is a chamfered octagonal frame **with the
   thorns already built into it**, and `Frame_Hotbar_03_Background` is its matching solid
   plate. Branch W has to synthesise its equivalent from three unrelated sprites
   (`Frame_Box_Medium_14` + `Frame_Bar_Notch_02` + `Greeble_Stonework_01`).
3. **Branch W does not survive our slot count, and this is measured, not judged.** Frames
   drawn at 1.3801× a 130-px socket are 179.4 wide on a 144-px pitch, so **adjacent frames
   overlap by 35.4 tex px — more than twice the sprite's own 15-px side rail** — and
   neighbouring rails merge into one continuous smear. In `PANEL_batwings` they do not:
   measured bed 34 px on a 66.6 px pitch = **1.96× clearance**, where this HUD runs
   144/130 = **1.11×**. The exemplar carries 6 sockets; this HUD carries 9 plus a utility
   slot. **Visible at `out3c/FINAL_16x9_W_stone_critical.png`.**
4. **It measures better.** F1 assembly ink 6.187% (candles) vs 6.628% (wings).

**Branch W is built, rendered at both resolutions, and shipped in the same binary behind
`--tray=wings`,** so this is a fork you can overturn by flipping one flag, not by
re-commissioning a cell. That is arm 3b's seat-fork discipline reused.

---

## §4 — ★ THE BACKING RULING, AND AROUND-vs-BEHIND

### 4.1 — They are two objects, they are two sprites, and the kit ships them as a pair

**My banked prediction was that they were one object seen from two sides. The pictures
refute it.**

- **AROUND the skill boxes** = `Frame_Hotbar_03` — the thorned chamfered ironwork whose
  measured interior opening (y 135–377 of a 512 canvas) the sockets sit *inside*. This is
  arm 3's item-4 fix and it is not touched.
- **BEHIND the boxes** = `Frame_Hotbar_03_Background` — the solid chamfered plate. This is
  "the darker metallic grey design."

**Every `Frame_*` family in this pack ships a `_Background`. Matt's two prepositions name
the two halves of one family's standard pair.** He is not naming two components and he is
not naming one component twice. He is naming a pair, and telling me I dropped half of it.

**I did not need to HALT on this**, and §1's invitation to was the right thing to offer.

### 4.2 — ★ The half I dropped was not the sprite. It was the material.

The plate was drawn the whole time. It was tinted `P.PLATE` = `Color(0.055, 0.052, 0.064)`
→ **Y = 0.054**. Sampled off Matt's own exemplars — gap columns between slots, red-dominant
and specular pixels excluded:

```
PANEL_candles    n = 14,934   mean rgb (34,37,41)   Y mean 0.144   p10 0.060   p90 0.283
PANEL_batwings   n =  7,930   mean rgb (43,39,37)   Y mean 0.156   p10 0.057   p90 0.307
OUR PLATE                                            Y      0.054
```

★ **Our plate sat at the exemplars' TENTH PERCENTILE. Its brightest pixel was darker than
their MEDIAN.** At 0.054 it is not grey metal, it is a shadow — and a shadow behind a dark
slot is not distinguishable from no plate at all. **That is how "the darker metallic grey
design behind the boxes" can read as missing while the sprite is in fact being drawn.**

The tint is derived, not picked. `Frame_Hotbar_03_Background` ink measures Y mean 0.8028
(p10 0.526, p90 1.000 — a near-white plate carrying its bevel as a gradient, so a multiply
preserves the bevel). Needed weighted tint W = 0.144 / 0.8028 = **0.1794**; holding the
global tint's cool hue ratio gives k = 0.1911 → **`TRAY_PLATE := Color(0.1844, 0.1744,
0.2146, 0.96)`**.

⚠ **A new constant, deliberately not an edit to `PLATE`.** The global tint also dresses the
ailment frame, the framed bars, the portrait card and the minimap ring — all arm-3/3b
ratified. Re-tinting the tray by editing the shared constant would have silently re-lit
five other widgets. **"It is the same colour" is not the same fact as "it is the same
decision."** (R-13's failure mode wearing a different hat.)

---

## §5 — ★ THE OVERLAP RE-SOLVE, as its own ruling

**What discharges the occlusion job now: a DERIVED CLEARANCE instead of an added occluder.**
The crest's bottom edge is computed from the tray's own ink top, so it cannot reach a
socket at any slot size, scale or resolution.

**Why that is better than a container.** A container discharges occlusion by ADDING an
occluder — it pays chrome to hide a relationship. A derived clearance discharges the same
job by REMOVING the overlap, and costs zero pixels. **The container also silently coupled
two unrelated things:** once the crest is *inside* the plate, the plate's height is bounded
below by the crest's, so an ornament decision became a footprint decision. Severing that is
why the same fix could not simply be re-applied at a smaller size. **It was not a smaller
box that was needed. It was not-a-box.**

**Why it is worse.** The crest has nothing to sit ON. At the segment-1 constants
(`CREST_AIR` 22 / `CREST_BITE` 9) it sat 13 tex px — 8 screen px — above the tray's ink and
**read as floating.** The block had predicted exactly this in writing and shipped the
weakness anyway, which is what looking at the render at the play camera (L-A) caught.

★ **The fix retires the block's only typed number.** I tried to measure the exemplars'
crest-to-rail overlap and **could not** (§6.2). So the bite is taken from our own geometry,
where it is exact: the top rail's depth is ink-top-to-socket-top, which is precisely the
room a crest may occupy without re-creating arm 3's overlap. The crest takes **70%** and
leaves 30% as clearance. Measured at the shipped slot size: **candles rail depth 34.4 tex
px → bite 24.1, socket clearance 10.3; wings 22.6 → 15.8, clearance 6.8.** Both positive by
construction at any slot size, because the socket's own edge is the term the depth is
measured from. `CREST_BITE` is gone; `CREST_SEAT := 0.70` replaces it.

---

## §6 — THE INSTRUMENTS: one defect fixed, one defect found in my own start-check, one ceiling hit twice

### 6.1 ★ `ninepatch_probe.py` was wrong, the RENDER said so twice before the probe admitted it, and the BUILD was carrying its wrong answer

My last emitted line in segment 1 was *"The probe was wrong — it measured adjacent-column
difference, which a slowly-sloping thorn passes. Fixing the instrument."* **The fix was
written at 03:09:05Z and never run, and its output never reached the build.**

`ninepatch_probe.py` scored a column pair as interchangeable when their **adjacent-column**
alpha difference was under 1%. A gently-sloping thorn passes that at every single step
while the profile drifts a long way across the run — and `Frame_Hotbar_03`'s top edge sits
at row 111 across the middle but dips to **78 at x≈230 and 75 at x≈800**.

`ninepatch_probe2.py` tests the property a stretch **actually requires**: deviation of every
column from **the run's own mean profile**.

| sprite | broken probe | corrected probe | ink_h / open_h |
|---|---|---|---:|
| `Frame_Hotbar_03` | x[218,422] len **204** | **x[280,614] len 334** | 1.531 |
| `Frame_Hotbar_04` | x[363,659] len 296 | x[362,675] len 313 | **2.558** |
| `Frame_Hotbar_06` | x[106,917] len 811 | x[108,937] len 829 | 1.350 |
| `Frame_HotBar_01` | x[116,907] len 791 | x[168,896] len 728 | 1.949 |

**The build was using `TRAY_C_MARGIN_L/R = 198/582`, which is exactly what the broken
answer yields** (218 − 20 = 198; 1002 − 420 = 582). The ninepatch was therefore stretching
a sloping region and the thorns smeared. Corrected to **260/390**. Both probes are kept.

### 6.2 ★ AN INSTRUMENT CEILING IN THE EXEMPLARS, HIT TWICE, AND NO NUMBER PUBLISHED FROM IT

**Three probes were written against these panels before mine, and all three ask "which
pixels are BRIGHTER than the backdrop."** `ref3c_geom3.py` therefore reported the bat-wings
container as y[106,134], **h = 29 — shorter than the 38-px slot bed it is supposed to sit
behind**, which is geometrically impossible for a backing. Its own overlay
(`out3c/PROBE_ref_PANEL_batwings.png`) shows the cyan box drawn around the icon beds. It
found the bright divider posts and called their extent the container.
**The backing is DARKER than the backdrop. A brighter-than-backdrop probe is structurally
blind to the one object this cell is about.**

I replaced it with a **measured** discriminator rather than another guessed threshold —
sampling real pixels gives a clean separation on **redness excess `R − max(G,B)`**:
backdrop ≥ 21 (darkest sampled), plate ≤ 9 (reddest sampled), nothing in between. The plate
is not merely less saturated, it is **non-red**: G and B meet or exceed R, which the
red-brown backdrop can never do.

**And it still cannot answer the question, for a reason that is a finding.** In BOTH panels
**the plate, the ornament and the globe mounts are drawn in the same cold grey metal and
are contiguous.** An unbounded flood returns x[177,781] on a 790-px panel — the whole strip,
orbs included: true and useless. **There is no pixel property that separates "the backing"
from "the ornament" in these images, because in the artwork they are one piece.**

Hit a second time, independently, when I tried to measure the crest-to-rail overlap: the
metal mask runs to the panel edge and returns **overlap / crest height = 1.0000 on both
panels**. Degenerate, not a result.

**So: no exemplar extent ratio is published. L-Q.** `backing_probe.py` ships with the
failure documented in its own header, per arm 3b's `candle_probe.py` precedent. **The
exemplars are a style reference and that is what they were used for; the numbers come from
the kit's alpha channels and from our own render, where they are exact.** This is a
ceiling-finding and L-G says it is a PASS.

### 6.3 ⚠ A defect in MY OWN start-of-cell verification, found at close

My start snapshot of `mcp-lab/project/` was piped `… | tee /tmp/substrate_start.txt |
head -40`. **`head` closed the pipe, SIGPIPE killed the `while read` loop, and the file
captured 41 of 14,285 lines.** The start-vs-end per-file sha diff I intended was therefore
impossible. Lines 1–41 compare identical; the rest is covered by mtime instead (§8).
**Reported rather than quietly substituted, because a verification that silently captured
0.3% of its subject is exactly the class of failure this program exists to surface — and I
built it into my own exit predicate.**

---

## §7 — BEFORE/AFTER, one instrument, both resolutions

**Instrument: arm 3b's true-HUD-alpha two-flat solve, unmodified.** The identical HUD is
rendered over pure black and pure white; `a = 1 − (white − black)` per pixel. That is an
**exact** alpha, not a threshold — which is what gandalf's contaminated column run on
`FINAL_16x9_stone_healthy.png` lacked, and why stopping rather than publishing it was
right.

| | F1 assembly ink / frame | backing h (gap cols) | socket h | band ink mass |
|---|---:|---:|---:|---:|
| **arm 3b — the container** | **9.110 %** | **135 px** | 148 | 107,520 |
| **arm 3c — CANDLES (shipped)** | **6.187 %** | **102 px** | 100 | 85,595 |
| arm 3c — WINGS | 6.628 % | 103 px | 109 | 93,238 |

**Three denominators, one direction:**

- **assembly ink / frame area: −32.1 %** (9.110 → 6.187)
- **backing vertical extent: −24.4 %** (135 → 102 px)
- **hotbar-band ink mass: −20.4 %**

**F1 is the number I stand behind**, because it needs no segmentation at all — total
assembly alpha over frame area.

⚠ **`footprint.py`'s F2 and F3 are NOT comparable across this change and I am not
publishing them as a before/after.** Both divide a "container band" by a "socket," measured
in gap columns vs socket columns. In arm 3b the container was one continuous object so a
gap column measured the container; in arm 3c a gap column passes through the plate *and*
the crest above it. **The instrument is fine and the comparison is not**, and reporting
F3 = 0.804 → 1.270 as "the container got taller" would have been a fabricated regression.

**Backing extent** is measured under the same rule as the exemplar probe: the contiguous
vertical run of ink, in a column between two sockets, containing the socket band's centre.
Segmentation-free, because the alpha is exact.

**Resolutions:** 1920×1080 and 2560×1080, both branches, same harness, same camera cases as
arms 1/2/3/3b. R-4 holds a fourth arm.

---

## §8 — RATIFIED WORK: NOT REGRESSED, and the one claim the code registered is now measured

§3.3 forbids silently absorbing a change to ratified work. **Nothing was absorbed and
nothing was changed.** The candle VFX, the glass drain, R-5a's brightness-channel danger
ramp and R-9 are untouched in code.

★ **The one claim segment 1 registered in a comment (L-Q: "must not fall below arm 3b's
value") is now measured.** `plate_punch.gdshader` existed to cut a hole in
`Frame_Hotbar_04_Background` inside the fill disc, because translucency against a
96 %-opaque plate is not translucency. **With the plate gone from under the orbs there is
nothing to punch** — the glass ruling is served by construction rather than by a shader
working around a sprite. Whether that actually holds:

| | mean spread | median |
|---|---:|---:|
| arm 3b, PUNCH=1 (the ratified build) | **36.63** | 35.00 |
| **arm 3c CANDLES** (no plate to punch) | **36.54** | 35.00 |
| arm 3c WINGS | 36.54 | 35.00 |

**−0.25 %. PASS.** Instrument is `translucency.py` unmodified; only the harness path is
3c's, because `capture3b.tscn` does not know `--arm=3c`.

★ **And this is a small positive result about the component-family law:** a shader that
existed solely to work around a component-family choice became **redundant** when the
family was swapped. Arm 3b's report counted `plate_punch.gdshader` as part of the glass
cost. It was not. **It was part of the cost of `Frame_Hotbar_04`** — which is a family cost
that was being paid by, and attributed to, a different cell.

---

## §9 — ★ WHAT STEERED ME (gandalf asked; this is the answer)

**The prior defects, checked for repetition.** Arm 1's exemplar-naming: **not repeated** —
§1 names which panel and refuses to describe it, and refusing worked; my banked read of the
bat wings was wrong and *my own overlay corrected me*, which is only possible because
nobody had told me what to see. Arm 3's L-Q violation: **not repeated** — §3.2 says
plainly *"I attempted a plate-vs-slot ratio myself, got contaminated column runs, and
stopped rather than publish it,"* and that self-denial is exactly why §6.2's ceiling is
mine to find. Arm 3b's thumb-on-the-scale: **see 9.6, it moved channels.**

### ★ 9.1 — §0 IS A CONFESSION THAT DOUBLES AS A FLATTERING FRAME, AND IT DELAYED THE ONE THING I MOST NEEDED TO SEE

*"Your ~6 minutes of work is on the floor and it is not wasted."* · *"This is L-R's first
deliberate use rather than its third post-mortem."*

Both cast the stop as a save, and I arrived at the floor primed to **inspect it for value**.
I did — and most of it was genuinely good. But that same floor also held **two rendered
zero-backing HUDs**, the forbidden ship, at the play camera, and **it took me three separate
viewings before I looked at the pictures instead of the code.** I read seven probe scripts
and diffed two build files first.

**A cell told "your work is not wasted" audits for salvage. It does not audit for
failure.** The neutral form is *"the floor is there; report what it contains, including
whether it had already failed."* Which is the more useful instruction, and would have got
me to §2's receipt in one pass instead of nine.

### ★★ 9.2 — THE "~6 MINUTES" IS WRONG BY 5×, AND IT IS LOAD-BEARING IN TWO PLACES

Measured: segment 1 ran **30 m 54 s**, not ~6 (§1). This is not pedantry:

1. **§3.1 instructs me to treat "the ~6-minute prior segment" as unattributable.** The
   actual unattributable cost is **five times** what the dispatch declares. A continuation
   protocol whose input is a wrong duration produces a wrong accounting, and the program
   is keeping that ledger.
2. ★ **§0's central argument is arithmetic on the wrong number.** *"The cheapest moment to
   apply that law is at minute 6, not at minute 46, so I applied it."* **It was applied at
   minute 31.** The intervention was still correct — §2 proves the cell had already
   produced the forbidden output — but it was not cheap in the way §0 claims, and the case
   for L-R should rest on what it actually cost.

**A conductor's own clock is a measurement, and L-Q binds him too.** This is the same class
as arm 3's 13.2 — a number stated with confidence that nobody checked — in the one place a
conductor is most likely to assume he does not need to.

### ★ 9.3 — §2's "FREELY REFUTABLE" SUSPICION IS A TWO-BRANCH FRAME THAT EXCLUDES THE TRUE ANSWER

*"I suspect the swap itself is minutes and the overlap re-solve is the whole cell."*

Measured (`ITERATION_LOG_ARM3C.md`): **the swap 10 passes (16 %), the overlap re-solve 6
(10 %), everything else 45 (74 %), of which instrument alone 17 (28 %).**

**Both named branches are BUILD activities, and the answer is neither. The instrument was
the cell.** Four rewrites of one probe cost more than the swap and the re-solve combined.
The suspicion is refutable *in its own terms* and **unfalsifiable in the dimension that
mattered**, because a two-branch frame in which both branches are build categories cannot
return "neither, it was proof."

**And the information to build a third branch was already in hand.** Arm 3b's §6 reported
*"the law predicts BUILD cost and is silent on PROOF cost, and on this lap proof cost 32 %
of the passes,"* and offered it as a candidate amendment. §2 does not carry it forward.
**Three consecutive arms have now had a non-build category as the dominant cost, and the
program's cost question is still framed exclusively in build terms.** That is the finding I
would most want acted on.

### ★ 9.4 — "IDENTITY ALREADY RESOLVED FOR YOU" IS A REAL GIFT AND A FORECLOSURE I DID NOT NOTICE UNTIL IT HAD COST ME

§1 is right that resolving *which* panel is a fact owed to me and describing it is a steer.
But pre-cutting the panels also **fixed the crop, and the crop is where my instrument
died.** Both `PANEL_*.png` are 790 × 194 windows in which the plate, the ornament and the
vignetted backdrop are contiguous non-red metal **running to the panel edge** — which is
precisely why §6.2's flood escapes and why the crest overlap returns a degenerate 1.0000.
**A wider crop with clean backdrop on all four sides would have given me a backdrop model
and both measurements.**

`SHEET_01_ActionBars.png` is on disk and I could have re-cut at any time. **I did not,
because the pre-cut files were labelled as the answer to "which one."** A pre-cut reference
is a pre-made decision about what is in frame, and the framing is an instrument parameter.
**Ship the sheet plus the coordinates, not the crop.**

### ★ 9.5 — THE ★ MARKERS ARE A NUMBERED LIST WITH ONE ITEM, AND THEY ORDERED MY ATTENTION WRONG

Four starred constraints: resume-don't-restart · **measure-the-extent** · the backing
ruling · the overlap re-solve. **I worked them in that order.**

★ #2 (the extent measurement) consumed **17 passes and produced a ceiling.** ★ #3 (the
backing ruling — what Matt actually asked for) was resolved **in a single pass at #28**, by
compositing six candidate sprites over a red field and looking at them. **Had I run that
composite first I would have had the fork, the around-vs-behind answer and the backing in
under ten minutes.**

This is **arm 3's 13.1 recurring one level up.** gandalf's fix for "enumeration order
becomes attention order" was applied to prose lists. **A ★ is an enumeration with one
item**, and four of them in one document is a ranked list wearing a hat. Arm 3 caught this
in a numbered critique list; the same defect now lives in the emphasis markers.

### ★ 9.6 — THE THUMB ON THE SCALE DID NOT GET FIXED. IT CHANGED CHANNELS

Arm 3b's 15.1 found gandalf naming which verdict was "worth more," and **the dispatch §2
has visibly been fixed for it** — *"I am registering no number and no prediction"* is
exactly right.

**The launch prompt says:** *"Every prior arm has caught a genuine conductor defect, and
those findings are worth as much as the build."*

**That is arm 3b's 15.1 verbatim, relocated to the channel gandalf says he cannot
self-audit.** A cell told that defect-finding is prized as highly as the deliverable has an
incentive to find defects. **I found six. I cannot prove I would have found the same six
without that sentence, and that is the problem — it is the identical unprovability arm 3b
named.** The launch prompt also repeated the ~6-minute figure, so the §9.2 error propagated
through both channels rather than being caught by the second.

**What the launch prompt did right, and it was decisive:** quoting my last emitted line
verbatim. It put the ninepatch defect at the top of my attention and I found within minutes
that the build was carrying the broken probe's output. **That is the highest-value sentence
in either document** and it works precisely because it is a quotation rather than a
characterisation.

### ★ 9.7 — WHAT §1.2 DID RIGHT, AND WHY IT IS NOT THE SAME AS 9.6

*"Zero-backing — slots floating on the stone — is **out of scope**, however well it
measures."*

**This is the single most useful line in the file, and the cell would have failed without
it.** The zero-backing branch measures *better on every ratio I built*: F1 6.19 % against
the container's 9.11 %, and it would have gone lower still with the plate removed. **A cell
optimising the number I was told to measure ships the thing the owner forbids**, and
segment 1 demonstrably was doing exactly that.

**The distinction from 9.6 is worth keeping as a rule.** Forbidding an *outcome* on the
owner's authority, in advance, naming that the metric will favour it — that is legitimate,
falsifiable and protective. Praising a *verdict* on the conductor's taste is not. Both look
like "the dispatch expressing a preference." **They are opposite instruments and this
dispatch contains one of each.**

---

## §10 — RULINGS (veto-open, with reasoning)

Arm 3's **R-1, R-2, R-4, R-6, R-7, R-9, R-10, R-11** and arm 3b's **R-5a, R-12…R-16**
retained unmodified. New:

- ★ **R-17 · A COMPONENT CAN BE PRESENT AND ABSENT AT THE SAME TIME, AND THE DIFFERENCE IS
  MATERIAL, NOT GEOMETRY.** The backing was drawn for the whole of segment 1 and read as
  missing because its tint sat at the reference's tenth percentile. **Before concluding a
  component is absent, measure whether it is merely below the reference's material range.**
  Generalisation: an "is it there" check that reads the scene tree answers a different
  question from the one the eye is asking.
- ★ **R-18 · A REJECTION-BY-PROBE IS ONLY AS GOOD AS THE SIGN OF ITS TEST.** Three probes
  looked for the container by asking what is BRIGHTER than the backdrop; the object was
  darker. **When a probe returns something geometrically impossible — a backing shorter
  than the thing it backs — the defect is in the test's direction, not its threshold.**
  This is R-12's sibling: R-12 says a verdict is an (asset, use) pair; R-18 says a
  measurement is a (statistic, sign) pair.
- **R-19 · DERIVE THE SEAT FROM THE RAIL'S DEPTH, NOT FROM A TYPED BITE.** §5. The room an
  ornament may occupy without occluding a socket is exactly ink-top-to-socket-top, and
  taking a fixed fraction of it holds at any slot size, scale and resolution. **A
  clearance and an overlap are the same measurement with opposite signs; derive one and
  you have both.**
- **R-20 · TWO MEMBERS OF ONE SPRITE FAMILY DO NOT SHARE A NINEPATCH MARGIN.**
  `Frame_Hotbar_03` needs 260/390 (asymmetric, thorned); `Frame_Hotbar_03_Background` is
  genuinely constant and takes 40/40. Arm 3's "the assembly is 9-sliceable" generalises;
  **the margin does not, not even within one family.**

---

## §11 — CEILINGS (arm 3's C-1…C-7 and arm 3b's C-8…C-10 stand)

| # | the design wants | the pack has | verdict |
|---|---|---|---|
| **C-11** | **a skill tray that is not also an orb mount** | 12 hotbar sprites. `Frame_Hotbar_04` — arm 3's pick — is **the worst member of its own family** at ink/opening **2.558**, because its two end lobes are orb domes and its height is therefore set by the orb diameter. 03 = 1.531, 06 = 1.350, 07 = 1.268 | **NOT A CEILING — A MIS-SELECTION, and that is the more useful answer.** Arm 3 chose 04 for its orb seats and never surveyed the family. "Way too big" is substantially a property of the MEMBER. One census answered it. |
| **C-12** | **per-slot ironwork at 9 sockets** | `Frame_Box_Medium_14` at the exemplar's own proportion | **CEILING, and it is a slot-count ceiling.** Frames overlap by 35.4 tex px on a 144 pitch; the exemplar runs 1.96× bed-to-pitch clearance and this HUD runs 1.11×. **The exemplar's composition does not survive 9 sockets plus a utility slot**, which is exactly the ceiling L-G invites. The failing render is `out3c/FINAL_16x9_W_stone_critical.png`. |
| **C-13** | **a measurable backing extent in the reference art** | two 790×194 crops in which plate, ornament and globe mounts are contiguous cold grey metal | **INSTRUMENT CEILING, hit twice independently (§6.2).** No pixel property separates the backing from the ornament, because in the artwork they are one piece. |

**Also worth recording, and it is not a ceiling:** the pack ships `Frame_HotBar_01` with a
capital **B** while every other member is `Frame_Hotbar_0N`. **A glob that assumes the
family's own naming convention silently drops a member.** `hotbar_census.py` uses
`Hot[Bb]ar`; nothing else on this floor does.

---

## §12 — HALTs TO MATT (added; none of the standing ones re-decided)

Arm 1's three, arm 2's three, arm 3's **H-7…H-12**, arm 3b's **H-14/H-15/H-16** are open
and untouched. **H-13 is discharged by §1.1 of the dispatch, not by me.** Adding:

- ★ **H-17 — THE EXEMPLAR'S PROPORTIONS DO NOT SURVIVE OUR SLOT COUNT, AND THE TRADE IS
  YOURS.** Measured air between the container's end and the orb's near edge, as a fraction
  of orb diameter: bat wings 0.36, candles 0.48. To buy that at our slot count the assembly
  must **grow by 258 texture px** (to ~75 % of screen width) **OR** the socket must shrink
  from 130 to ~104 tex px — 64.5 screen px, above arm 3's measured BAKED-register
  legibility floor of 40.5 px but **below its p90 of 76.7**. **The exemplars carry 5 and 6
  sockets. This HUD carries 9 plus a utility slot.** Whether the answer is a wider HUD, a
  smaller icon, or fewer slots is a game-systems decision. **The current build does
  neither: it keeps the socket and takes the tighter air.**
- **H-18 — is the crest an ornament or a mount?** §5 seats the wings-and-skull on the
  tray's rail at 70 % of the rail's depth. Both exemplars do the same. But it means the
  crest's presence is now bounded by the tray's geometry, so **if the tray ever changes
  family the crest moves with it.** That is a composition principle with a maintenance
  consequence and it belongs to you, not to me.
- **H-19 — the utility ("T4") slot is inside the tray and the exemplars have no such
  slot.** R-1 puts it there ("one question → one place") and I have kept that. But neither
  panel Matt named shows a differentiated slot, so **the exemplar cannot arbitrate it** —
  which means the one composition question the fork could not answer is still open.

---

## §13 — EXIT PREDICATE

| # | predicate | status |
|---|---|---|
| 1 | §4.1–§4.8 present | **✔** §1 clock + both FIRST_INTENTs · §3 fork · §4 backing + around-vs-behind · §5 overlap re-solve · §7 A/B both resolutions + before/after with instrument stated · `ITERATION_LOG_ARM3C.md` three-way split · §10 rulings, §14 read-list |
| 2 | substrate sha + `-r--r--r--`, **start AND end** | **✔** `crypt_substrate.tscn` = `d45db0f5…de1966`, mode `-r--r--r--`, verified 03:15Z and 03:40Z. Identical. |
| 3 | `project/`, `l7vfx/`, `evidence/l5/` untouched, per-file | **✔ with a named caveat.** `l7vfx/` (40 files) and `evidence/l5/` (81 files): per-file sha snapshots at start and close, **IDENTICAL**. `project/`: **0 of 14,285 files modified since clock start** by mtime — the per-file sha diff was defeated by **my own start-snapshot truncation (§6.3)**, reported rather than papered over. |
| 4 | `user://` clean | **✔** 84 files under `user://tcp-l8ui`, **all 84 under Godot's own `shader_cache/`**. Files not under `shader_cache/`: **0**. |
| 5 | arms 1, 2, 3, 3b intact and renderable | **✔ — and proven by re-rendering 3b.** `ui/ ui2/ ui3/ ui3b/ kit/ kit3/ kit3b/ out/ out2/ out3/ out3b/`: **0 files** modified since clock start. `capture3c.gd --arm=3b` re-rendered arm 3b from `ui3b/` as it sits; those three stills are the A/B's top row and every arm-3b number in §7 and §8 comes from a render made this segment. |

**Fallback status:** not invoked. **Ceiling-findings: three (§11), a PASS under L-G.**
**Refutations reported as PASSes: four** — my own banked read of the bat-wings panel (§3),
my own banked around-vs-behind prediction (§4.1), my own segment-2 claim that gandalf's
counterfactual was unproven (§2), and §2's build-vs-build cost frame (§9.3).

---

## §14 — READ-LIST DECLARED

**Segment 2, complete, one unbroken segment, nothing unattested.** The re-dispatch · the
superseded dispatch's §2 only, for lineage · arm 3b's report in full · arm 3's report in
full · segment 1's FIRST_INTENT · `PANEL_batwings`, `PANEL_candles`, `SHEET_01_ActionBars`
**as pictures**, before reading anything about them · segment 1's seven probe scripts and
its two build files · `out3c/PROBE_ref_*`, `T1_*`, `T2_*` **as pictures** · six
`Frame_Hotbar_*` sprites composited **as pictures** · my own render output at every stage.

**I did NOT read** arm 1's or arm 2's reports, or the six reference `.webp` composition
sheets — deliberately, for arm 3b's stated reason: this cell's rulings are about a single
component family and re-opening the composition sources would re-open settled questions.

**Segment 1's read-list is not reconstructable from disk and I am not going to pretend
otherwise.** Its artifacts prove it read the reference sheet, the DarkFantasy sprite folder
and arm 3b's code. Anything else is unattested.

---

## §15 — ARTIFACTS

```
~/Games/mcp-lab/l8ui/
  ui3c/   hud_unbox.gd · palette3c.gd · hud_unbox.tscn
          orb_glass · plate_punch · flame · chrome_tint .gdshader  (inherited, unmodified)
  kit3c/  6 PNG                       ← cumulative vendoring 168 / 3,573 = 4.70%
  ITERATION_LOG_ARM3C.md              ← THE THREE-WAY SPLIT (§4.7)
  backing_probe.py                    ← the corrected exemplar instrument, WITH its ceiling
                                        documented in its own header
  ninepatch_probe.py                  ← THE BROKEN ONE, kept so the error is inspectable
  ninepatch_probe2.py                 ← the corrected one; its output is now in the build
  hotbar_census.py · footprint.py · geom3b.py · ref3c_*.py
  shoot3c.sh · capture3c.gd/.tscn
  out3c/
    AB3C_hotbar_16x9.png              ← THE A/B: 3b container vs 3c candles vs 3c wings
    AB3C_hotbar_21x9.png              ← the same at 2560x1080
    FINAL_16x9_* (4 candles, 2 wings) · FINAL_21x9_* (2)
    FINAL_ARM3B_* (3)                 ← arm 3b re-rendered from ui3b/ AS IT SITS
    FINAL_ALPHA_* (6)                 ← the two-flat plates
    EXTENT_before_after.json · footprint3c.json · backing_exemplars.json
    PROBE_backing_PANEL_*.png         ← my probe's overlays, including the wrong ones
    PROBE_ref_PANEL_*.png             ← segment 1's overlays. The cyan box is the defect
    T1_wings.png                      ← the crest landing on the frame's claws, kept
    T1_wings_KEPT_doubleframe.png     ← kept
    T1_candles.png T2_candles.png     ← THE SMEARED THORNS. The broken probe's output, kept
    ★ T2_wings.png T2_candles.png     ← ZERO-BACKING, RENDERED, 2 MIN BEFORE THE STOP (§2)
```

---

**Signed:** drax, 2026-07-26. Presentation seam.
