# KC2-PLAY · THE ENERGY GLOBE, RE-READ WITH THE HP GLOBE'S READER

**Date:** 2026-09-21 · **Author:** galadriel (visual-perception seam) · **Run:** KC2-PLAY, conductor gandalf
**Commission:** conductor dispatch 2026-09-21 — *"Re-read the energy globe with Apple Vision… do the
`eor_release.clean()` `marg` gate as part of this… if the frames are not committed and this genuinely
needs the MP4, stop and say so in one line."*
**Instruments:** `pipeline/kc2_energy_reread.py` (new) · `pipeline/ocr_vision.swift` (the pinned reader,
byte-identical) · `pipeline/eor_release.py` **v2** (versioned `marg_min`, default 0.0)
**Output of record:** `notes/2026-09-21-kc2-play-energy-globe-reread.json`
**New capture:** NONE. **No push.**

---

## ⚑ § 0 · THE ONE LINE THE DISPATCH ASKED FOR — AND A CORRECTION TO IT

> **The per-frame crops were never committed and the full re-read needs the MP4: `T30`.** ⚑ **But the
> standing account of `T30` is wrong and I am correcting my own: the footage is not destroyed — it is
> on an unmounted external volume, and its identity is pinned by a full sha256.**

| | |
|---|---|
| what I said 2026-09-21 | *"`~/gd-scratch/eor-test-2/` does not exist. gamora's 'MP4 gone' is correct and I checked rather than assumed."* |
| ⚑ what I checked this lap | **I checked ONE path — the one my own trace JSON records.** legolas's Lap Q pre-registration records a **different** home: `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`, **479,438,089 B, sha256 `4c60960d…4de8`.** `/Volumes` holds only `Macintosh HD`: **the volume is not mounted.** |
| the local copy | legolas hash-verified it at `~/gd-scratch/` on 2026-09-10 and wrote *"this file must survive any future sweep — it is the sole reachable regeneration source for 1.68 G of deletable frames."* ⚑ **It did not survive. `~/gd-scratch` is gone entirely.** |

⚑ **So `T30` is not *"re-shoot the footage."* It is *"mount the drive"* — and because the digest is
pinned, a remounted copy is **verifiable, not merely plausible.** That is a materially cheaper ask of
Matt than the one the run has been carrying, and it was reachable by reading the other seat's
pre-registration. **Third instance this run of the instrument already being on the page.**

**Everything below is what the strong reader could do WITHOUT the MP4 — and it was more than I expected.**

---

## TOP LINE

**Sixteen energy-readout frames are committed. The strong reader runs on those.** Pointing it at them
did not sharpen the fork. ⚑ **It refuted the premise of my own previous note, and then repaired the
gross-drain figure by a route that does not need the refutation settled.**

| | ⚑ finding |
|---|---|
| **1 · the reader gap is REAL and MEASURED** | Apple Vision reproduces **16 of 16** independent hand reads in this corpus, exactly. The glyph atlas, on the same frames: **3 wrong values and 5 parse failures out of 20.** |
| **2 · ⚑ MY "PHYSICALLY IMPOSSIBLE" LABEL IS WITHDRAWN** | The frame at `t = 735.0` displays **1610**, sixteen points above the ceiling — and **three independent readings agree**: the 2026-08-25 hand read (it is `atlas-spec.json` row 7, **the atlas's own training data**), Apple Vision at confidence **1.000**, and my eye at ×12. **The corpus's best-attested energy frame is one my note called impossible.** |
| **3 · ⚑ AND THE GROSS DRAIN IS REPAIRED ANYWAY** | Every tick splits **exactly** into a **SPEND** limb (below the ceiling) and a **SPILL** limb (over-ceiling excess given back). **A spill is not a cost under EITHER hypothesis** — a real clamp costs nothing, and a misread never had the energy. **Spill is 39.4 % of the published gross.** Spend is **112.0 /s**, against the published **184.8**. |
| **4 · the verdict does not move** | **`u` stays `UNPINNABLE-FROM-COMMITTED-PIXELS`.** The repaired gross lands at **104–112 /s**, which agrees with **neither** 176.4 nor ≈190 — the pixel instrument is not a rival to either, which is what § 7 of the previous note already concluded and this lap makes firmer. |
| **5 · ⚑ the `marg` gate should NOT be run as a cleaning step** | Versioned and swept. **It removes 3 of 3 wrong values, discards 4 of 12 true ones, and keeps 4 of the 5 parse failures.** And the control that matters: ⚑ **removing the SAME NUMBER of frames AT RANDOM reproduces its effect on the net to within 1.3 sd at every gate ≥ 3.** The gate is not cleaning. It is deleting. |

**Nothing silently restated: `clean()`'s default is `marg_min = 0.0` and is bit-identical to v1 —
verified by diff against the committed JSON, not asserted. No figure in `P-b` or `s2-releases.json`
moves. Law 3 held; no branch chosen; no constant touched in any seam.**

---

## § 1 · THE CROSS-READER CONTROL — the strong reader, on the frames that exist

**Reader:** `pipeline/ocr_vision.swift`, sha256 `1a96036d…4ec1` — **byte-identical to legolas Lap Q's
`method/ocr.swift`**, the pinned digest in `pm4q_digests.json`, i.e. **the very reader that produced
the HP trace at 100.00 % acceptance.** Apple Vision `VNRecognizeTextRequest`, `.accurate`,
`usesLanguageCorrection = false`, `minimumTextHeight = 0.004`.

**Population:** every committed image carrying the energy readout — the ×6 atlas build sheet
(14 crops, 10 of them hand-labelled in `atlas-spec.json`), the ×7 blind-gap strip (4 crops, hand-read
in MD-B4app-2b § 1.3), and 6 single frames. **n = 20 after de-duplication; 16 carry an independent
hand read.**

| frame | t | **hand, 2026-08-25** | **Apple Vision** | the glyph atlas | `marg` | verdict |
|---|---:|---:|---:|---|---:|---|
| sheet row 0 | 686.00 | 1466 | **1466** | `1466/2576` | 6.4 | AGREE |
| sheet row 1 | 692.00 | 1314 | **1314** | `1314/2576` | 8.5 | AGREE |
| sheet row 2 | 695.00 | 1370 | **1370** | ⚑ `13//0/2576` | **10.7** | **ATLAS-PARSE-FAIL** |
| sheet row 3 | 705.00 | 1376 | **1376** | `1376/2576` | 7.9 | AGREE |
| sheet row 4 | 712.00 | 1509 | **1509** | `1509/2576` | 10.7 | AGREE |
| sheet row 5 | 725.00 | 1594 | **1594** | `1594/2576` | 10.7 | AGREE |
| ⚑ **sheet row 6** | **735.00** | ⚑ **1610** | ⚑ **1610** | `1610/2576` | **2.6** | **AGREE** |
| sheet row 10 | 805.00 | 1541 | **1541** | `1541/2576` | 8.5 | AGREE |
| sheet row 11 | 820.00 | 1588 | **1588** | `1588/2576` | 10.7 | AGREE |
| sheet row 13 | 855.00 | 1591 | **1591** | `1591/2576` | 3.5 | AGREE |
| blind row 0 | 702.05 | 1399 | **1399** | ⚑ `1349/2476` | 0.6 | **ATLAS-WRONG-VALUE** |
| blind row 1 | 702.60 | 1430 | **1430** | `1/0/2576` | 7.5 | ATLAS-PARSE-FAIL |
| blind row 2 | 703.15 | 1434 | **1434** | `1/4/2576` | 9.0 | ATLAS-PARSE-FAIL |
| blind row 3 | 703.70 | 1417 | **1417** | `1417/2576` | 0.1 | AGREE |
| crop-energy-t690 | 690.00 | — | **1456** | `1456/2576` | 2.5 | AGREE |
| exc_688.18 | 688.18 | 1497 | **1497** | ⚑ `107/2576` | 3.0 | **ATLAS-WRONG-VALUE** |
| exc_702.90 | 702.90 | 1437 | **1437** | `1/7/2576` | 0.9 | ATLAS-PARSE-FAIL |
| exc_703.90 | 703.90 | — | **1412** | `1412/2576` | 8.6 | AGREE |
| exc_780.66 | 780.66 | — | **1485** | ⚑ `105/2576` | 2.6 | **ATLAS-WRONG-VALUE** |
| exc_836.90 | 836.90 | — | **1475** | `14/5/2576` | 4.4 | ATLAS-PARSE-FAIL |

**Apple Vision vs the hand: 16 / 16 exact. Zero disagreements.**

⚑ **The selection bias, stated before the rate is quoted, because it is large.** Ten of these frames
(the blind strip and the `exc_*` set) were **selected in 2026-08-25 precisely because the atlas failed
on them.** On that adversarial half the atlas scores **1 clean read of 10.** On the **non-adversarial**
half — the atlas sheet, chosen for glyph coverage, not for failure — it scores **9 of 10, with one
parse failure and no wrong value.** *The 20 % wrong-value rate is not a population rate and must not be
quoted as one.* What the table **does** establish is that the strong reader **recovers every frame the
weak one lost**, which is the claim the dispatch was testing.

⚑ **One instrument note, recorded because it moved a reading.** The sheet was first cut into 14 equal
rows and each row read separately. The row-2 crop came back **1570**; the **whole** sheet, read once and
ordered by Vision's own bounding boxes, comes back **1370** at confidence 1.000. **A horizontal slice
clips glyph extrema and manufactures a substitution.** The cut was unnecessary — Vision returns a box
per line — and it is the cut that was wrong, not the reader. **The version of record reads the sheet whole.**

---

## ⚑ § 2 · THE REFUTATION, AND IT IS OF MY OWN NOTE

MD-B4app-2b § 2.2 (mine, 2026-09-21) reads:

> *"Energy cannot rise 16 and fall 16 in 17 ms while clipped at a ceiling. These are glyph misreads
> under combat VFX crossing the HUD box."*

⚑ **The exemplar that sentence was built on is `t ≈ 735.2`. The atlas's own training frame at
`t = 735.0` reads 1610 — and I typed that label myself, into `atlas-spec.json`, on 2026-08-25.**

| reading | source | value |
|---|---|---|
| hand, ×6 crop | `atlas-spec.json` row 7, **authored by me 2026-08-25** | **1610** |
| Apple Vision, conf 1.000 | this lap, the pinned HP-globe reader | **1610** |
| eye, ×12 | this lap | **1610** — crisp, unambiguous, no VFX over the glyphs |
| the glyph atlas | `s2-energy-60hz.json`, `t = 735.0000` | `1610/2576`, `marg` 2.6 |

> ⚑ **I trained the reader on a frame, published the frame's value as ground truth, and eleven months
> of laps later declared that value physically impossible — using a control printed four paragraphs
> away in the same note. The label is withdrawn.**

**What the pixels support now, stated precisely:**

- `1594` **is** the out-of-combat resting level: 4,800 control samples, 100 % parsed, every one `1594`,
  across two 40-second windows whose `marg` varies 7.2–11.2 (so the frames are live, not a frozen HUD).
  `eor_release.py` already calls it *"the reserved-adjusted operating ceiling"* — **max minus a reserve**,
  not the max.
- The trace **exceeds it**, and the excess is **tight**: median **+12**, p75 **+20**, **85.3 % within +21**.
- ⚑ **63.3 % of the above-ceiling reads are NOT reachable from `1594` by any single glyph substitution**
  (the cluster is 1603–1619; the reachable set is 1595–1599 plus 1694/1794/1894/1994). *A reader that
  fails by substituting one glyph cannot produce 1610 from 1594.*
- The reachable 36.7 % (`1595`–`1599`) carry a **median `marg` of 9.00**, against **3.60** for the
  unreachable cluster and **10.40** at `1594`. **The two sub-populations do not behave alike and this
  lap does not merge them.**

⚑ **What I do NOT claim: that all 1,187 above-ceiling samples are real.** One frame is confirmed. The
real/artifact split of the rest is **not determinable from committed pixels**, and the mechanism — a
clamp on an over-cap grant, a moving reserve, something else — **is not mine to adjudicate.** It is
surfaced, not decided. **Law 3: an absence, declared.**

---

## ⚑ § 3 · THE CLAMP DECOMPOSITION — the repair that does not need § 2 settled

The previous note handled the above-ceiling ticks by **deleting** them, and honestly labelled the
result an over-correction. That was the wrong shape of repair. **Here is one that is exact.**

> **Every drain tick splits into two limbs, and the split is an identity, not an estimate:**
> `spend = min(start, 1594) − min(end, 1594)` — the fall that happens **below** the ceiling.
> `spill = start − max(1594, end)` — the fall that happens **above** it.
> **`spend + spill = |ΔE|` for every tick. Maximum residual across 1,626 ticks: `0.0`.**

⚑ **A SPILL IS NOT A COST UNDER EITHER HYPOTHESIS.** If the read is real, it is over-cap excess being
clamped back and the pilot never owned it. If the read is a misread, there was never any energy there
to lose. **The decomposition therefore answers the gross-drain question WITHOUT first settling § 2** —
which is the whole reason to prefer it.

| limb | Σ | over 182.65 s | **over 161.0 s** *(the note's classified duration)* |
|---|---:|---:|---:|
| **SPEND** — the real cost | 18,025 | 98.7 /s | ⚑ **112.0 /s** |
| **SPILL** — over-ceiling give-back | 11,723 | 64.2 /s | 72.8 /s |
| **TOTAL, as published 2026-08-25** | 29,748 | 162.9 /s | **184.8 /s** |

**Spill is 39.4 % of the published gross.**

**The clamp signature, which is why "spill" is the right name:**

| | |
|---|---:|
| ticks starting above the ceiling | **615** (37.8 % of count, **43.7 % of mass**) |
| ⚑ of those, landing **EXACTLY** on 1594 | ⚑ **424 — 68.9 %** |
| median size, ticks starting **above** | ⚑ **−16.0** |
| median size, ticks starting **at or below** | **−13.0** |

⚑ **A fall that terminates exactly at the operating ceiling in 69 % of cases, with its own
characteristic quantum of −16 against the −13 of the below-ceiling population, is two different
quantities sharing one tick rule.** And the confirmed-real frame's excess — `1610 − 1594 = 16` — **is
that quantum exactly.**

### 3.1 The gross-drain bracket, restated

| treatment | /s over 161.0 s | |
|---|---:|---|
| all ticks, **as published 2026-08-25** | **184.8** | contaminated: 39.4 % of the mass is spill |
| ⚑ **SPEND limb** (the principled point estimate) | ⚑ **112.0** | |
| drop every tick starting above the ceiling | **104.1** | over-corrects: throws away the spend limb of the 93 mixed ticks |
| ⚑ **honest interval** | ⚑ **[104.1, 112.0]** | **was `[104, 190]` — an 82-unit bracket collapses to 7.9** |

> ⚑ **AND IT CONTAINS NEITHER CANDIDATE.** 176.4 and ≈190 both sit **far above** it. **The previous
> note said the pixel bracket "contains 176.4 and separates the two worlds not at all"; the corrected
> reading is stronger and stranger — the pixel gross agrees with NEITHER world.** It is not a rival
> figure and it is not a consistency check that 176.4 passes. It is a third number, and what it most
> likely measures is a *visible* drain cadence the 60 Hz integer readout can resolve, which is not the
> same object as a client-printed per-tick cost. **Reconciling them is a sim-side question, routed.**

---

## § 4 · DOES THE VERDICT CHANGE? — **NO, AND I am not arguing around it**

The dispatch asked me to be as willing to keep `UNPINNABLE` as to lift it. **I keep it**, and the
reasons are sharper than they were:

1. **World B's premise is dead twice over.** *"galadriel's pixel gross ≈ 190 is right"* required a
   measurement. It was a contaminated sum before; it is now a sum **39.4 % of which is a give-back the
   pilot never paid.** The corrected figure is 112.0.
2. **World A is not handed the win**, because **both** worlds compute `u` from the **same** `net`, and
   § 4 of the previous note showed that `net` is a **selection artifact** whose sign is chosen by where
   the interval label is taken (END −80.51 / START +64.70 / MIDPOINT −6.71 — a **158 /s swing with no
   fight in it**). **Nothing in this lap touches that, and nothing repairs it.**
3. **The bypass instrument still has 4.9 seconds.** Off channel there is no drain term, so
   `income = 75.37 + 100u` inverts directly — and across the OCR margin gate the implied `u` runs
   **0.3035 → 0.1446 → 0.1918 → 0.1531**, ⚑ **non-monotonically**, on **4.90 → 6.65 s** of a 182.65 s
   fight. The conductor's line holds exactly: **a better reader sharpens five seconds; it cannot
   manufacture a sixth.**
4. ⚑ **And the excluded gap stays excluded-by-assumption, not by evidence.** `0.2980` is forbidden by
   both branches; the direct instrument's loosest reading, `0.3035`, lands inside that gap. **The
   widening stands.**

> **`u` (`leech_uptime`) remains `UNPINNABLE-FROM-COMMITTED-PIXELS`.** No branch chosen. No narrowing
> offered. **The one thing this lap does change is that the pixel gross is no longer an argument for
> either side — it is a third measurement of a different object, and it is now precise enough
> (`[104.1, 112.0]`) for that disagreement to be a finding rather than noise.**

---

## § 5 · THE `marg` GATE — versioned, swept, and NOT recommended as a cleaning step

**The amendment (`eor_release.py` v2):** `clean(erows, marg_min=0.0)`. The gate sits at the **same
stage as the max gate** — per-row acceptance, before any neighbour statistic — so a low-confidence row
cannot participate in its neighbours' medians. The census gains `marg_min` and `margin_rejected`.

⚑ **NOTHING SILENTLY RESTATES, AND THIS IS VERIFIED RATHER THAN ASSERTED.** Re-running
`kc2_energy_shape.py` under v2 and diffing against the committed
`2026-09-21-kc2-play-energy-globe.json` gives **exactly two differences, both NEW census keys**
(`marg_min: 0.0`, `margin_rejected: 0`) **and no numeric change anywhere.** Every figure in `P-b` and
in `s2-releases.json` stands where it stood.

### 5.1 ⚑ `marg` scored as a correctness classifier — on the labelled set, not assumed

| gate | kept | correct | **WRONG VALUE kept** | **parse-fails kept** | ⚑ **TRUE VALUES DISCARDED** |
|---:|---:|---:|---:|---:|---:|
| **0** *(as committed)* | 20 | 12 | **3** | 5 | **0** |
| 2 | 17 | 11 | 2 | 4 | 1 |
| 3 | 14 | 9 | 1 | 4 | 3 |
| **4** | 12 | 8 | ⚑ **0** | ⚑ **4** | ⚑ **4** |
| 5 | 11 | 8 | 0 | 3 | 4 |
| 7 | 10 | 7 | 0 | 3 | 5 |

⚑ **The smallest gate that removes every wrong value is 4. It costs four true values — including
`t = 735.0`, the best-attested frame in the corpus — and it still keeps four of the five parse
failures**, because parse failures carry **high** margins (`t = 695.0` fails at `marg` **10.7**, the top
of the scale). **The margin is not monotone in correctness.** It is not a correctness gate, and a
reader who runs it as one is buying precision with true values and getting no protection at all against
the failure mode that returns `None`.

### 5.2 Every headline figure at every gate — pre-amendment value in the first column

| figure | ⚑ **`marg ≥ 0`** *(committed)* | `≥ 2` | `≥ 3` | `≥ 4` | `≥ 5` | `≥ 7` |
|---|---:|---:|---:|---:|---:|---:|
| samples used | **9,959** | 9,277 | 8,789 | 8,393 | 7,860 | 7,104 |
| margin-rejected | **0** | 807 | 1,394 | 1,836 | 2,404 | 3,222 |
| **ceiling duty** (`E == 1594`) | **0.2801** | 0.2983 | 0.3128 | 0.3254 | 0.3402 | 0.3505 |
| occupancy `E ≥ 1560` | **0.6363** | 0.6502 | 0.6597 | 0.6675 | 0.6852 | 0.6993 |
| frac above ceiling | **0.1189** | 0.1117 | 0.1002 | 0.0875 | 0.0793 | 0.0745 |
| **saw-tooth period** (gate-free) | **0.100 s** | 0.100 | 0.100 | 0.100 | 0.0833 | 0.0833 |
| teeth `prom=20`, n | **491** | 380 | 291 | 215 | 159 | 125 |
| ⚑ **median tooth period** | **0.1167 s** | 0.200 | 0.300 | 0.5166 | 0.800 | ⚑ **1.050** |
| median tooth depth | **33.0** | 33.0 | 33.0 | 36.0 | 38.0 | 41.0 |
| median recovery slope | **620.0** | 530.0 | 449.8 | 293.0 | 195.8 | 126.7 |
| gross, all ticks (161 s) | **184.8** | 142.3 | 113.3 | 90.2 | 70.5 | 49.7 |
| ⚑ **gross, SPEND limb** | ⚑ **112.0** | 86.6 | 73.3 | 66.2 | 56.9 | 42.2 |
| ⚑ **channelling net, below cap** | ⚑ **−3.13** | −28.40 | −29.80 | −42.16 | −67.27 | ⚑ **−83.77** |
| off-channel sampled | **4.90 s** | 5.27 | 5.80 | 5.88 | 5.93 | 6.65 |
| off-channel implied `u` | **0.3035** | 0.3210 | 0.1446 | 0.1727 | 0.1918 | 0.1531 |

⚑ **Read the tooth-period row and the net row together and the gate condemns itself.** The median tooth
period moves **9×**; the channelling net moves **27×** and lands within a few points of the published
**−78** — the very number § 4 of the previous note proved to be a labelling artifact. **A gate that
"cleans" its way back to a number already shown to be an artifact deserves the control in § 6, not
adoption.**

---

## ⚑ § 6 · THE CONTROL THE SWEEP IS WORTHLESS WITHOUT — is the gate cleaning, or just deleting?

**Method:** for each gate, remove the **same number** of frames **uniformly at random** (20 draws, seed
`20260921`) and recompute the net. If the gated figure sits inside the random band, the gate explains
nothing that deletion does not.

| gate | frames removed | **GATED net** | pairs | sampled | **RANDOM net** (mean ± sd) | ⚑ **distance, in sd** |
|---:|---:|---:|---:|---:|---:|---:|
| — | 0 | **−3.13** | 2,454 | 40.90 s | — | — |
| 2 | 6.9 % | −28.40 | 1,684 | 28.07 s | −10.65 ± 6.25 | **−2.84** |
| 3 | 11.8 % | −29.80 | 1,341 | 22.35 s | −23.36 ± 10.12 | **−0.64** |
| 4 | 15.7 % | −42.16 | 1,046 | 17.43 s | −32.42 ± 11.83 | **−0.82** |
| 5 | 21.1 % | −67.27 | 718 | 11.97 s | −48.65 ± 14.44 | **−1.29** |
| 7 | 28.7 % | −83.77 | 366 | 6.10 s | −71.25 ± 24.77 | ⚑ **−0.51** |

> ⚑ **AT EVERY GATE FROM 3 UP, THE MARGIN GATE IS INDISTINGUISHABLE FROM THROWING THE SAME NUMBER OF
> FRAMES AWAY AT RANDOM.** Only gate 2 carries a component deletion does not explain. **The net is not
> a robust statistic — it is a function of how much of the trace survives**, and a 28.7 % sample loss
> costs the estimator **85 % of its adjacent pairs** and **85 % of its sampled time**: two compounding
> losses, since a pair needs both its frames and a channel-active window needs three surviving ticks.
>
> ⚑ **The consequence is a standing warning, not a one-off: ANY future attempt to clean this trace
> harder will manufacture ≈ −78 by decimation alone.** The published −78 is now reachable by **two
> independent wrong routes** — END-labelling and sample loss — and by no right one this lap can find.

**Isolating arm, for completeness:** dropping *only* the above-ceiling frames, with no margin gate at
all, gives **−18.59 /s** on 2,308 pairs and 38.47 s — i.e. most of the swing is the deletion, not the
above-ceiling reads.

### 6.1 A hypothesis I formed, tested, and lost — recorded rather than quietly dropped

I expected the gate to be an **intensity** gate: low margin marks frames where combat VFX crosses the
HUD, so gating on it would condition every rate on the thing being measured — § 4's conditioning law in
a new costume. ⚑ **REFUTED by the cheapest test.** A `marg ≥ 4` gate keeps **84.1 %** of channel-ACTIVE
samples and **88.6 %** of channel-IDLE ones, and the channel-active share of the surviving trace moves
**0.8094 → 0.8110.** The gate is close to intensity-blind. **The elegant explanation was wrong and the
boring one — it just deletes — is right.**

---

## § 7 · WHAT MOVES, AND WHAT DOES NOT

| artifact | status |
|---|---|
| `P-b` energy rows · `s2-releases.json` · every figure in `2026-09-21-kc2-play-energy-globe.json` | ⚑ **UNMOVED.** `clean()`'s default is bit-identical; verified by diff. |
| `MD-B4app-2b § 2.2`'s *"physically impossible"* | ⚑ **WITHDRAWN** (§ 2). Superseded by this note. |
| `MD-B4app-2 § 4.4`'s `≈190 /s` gross | ⚑ **SUPERSEDED** by the spend/spill decomposition: **112.0 /s** (§ 3). |
| the `[104, 190]` bracket of 2026-09-21 | ⚑ **SUPERSEDED** by **`[104.1, 112.0]`** (§ 3.1). |
| `T30`'s standing description | ⚑ **CORRECTED** (§ 0): unmounted volume, pinned digest — not a destroyed file. |
| ceiling duty **0.2801** · gate-free period **0.100 s** · median tooth depth **one tick** · channel uptime **0.8375** | **UNCHANGED.** |
| `MO_DRAWDOWN_BAND` · the `−1.03 /s` boot gate · `leech_uptime` | **UNTOUCHED.** Math-before-code: nothing here authorises a constant to move. |

---

## § 8 · ROUTED, NOT ADJUDICATED

1. ⚑ **The gross-drain triangle is now three numbers, not two.** Tooltip **176.4** · my earlier pixel
   **≈190** · the corrected pixel **112.0**. **The pixel instrument measures the drain the 60 Hz integer
   HUD can resolve, which need not be the client's per-tick cost.** → gamora / conductor. **I do not
   grade the sim.**
2. ⚑ **The above-ceiling mechanism.** Something puts energy **+16 to +21** above a resting level that
   4,800 control samples pin at 1594, in runs of median one frame, returning to exactly 1594 in 69 % of
   cases. `eor_release.py` already names 1594 *"reserved-adjusted."* **Whether that is an over-cap grant
   being clamped, or a reserve that moves, is a save/sim question.** → gamora / legolas.
3. **The net is still a selection artifact** (§ 4), and § 6 shows it is **also** coverage-fragile.
   **Any interval derived from it — the disjoint union included — needs re-deriving on an input that
   survives both, or withdrawing.** → gamora. *Recommendation offered, not asserted: the absence.*
4. ⚑ **`T30` re-priced** (§ 0): **mount `/Volumes/reincarnated`**, verify against sha256
   `4c60960d…4de8`, and the full Apple Vision re-read of the energy ROI becomes a few minutes' work —
   the reader is committed and compiles. → Matt, via the conductor.
5. **A provenance gap in my own 2026-08-25 lap:** `energy-sheet.png` carries **14** crops and
   `atlas-spec.json` labels **10**; the four unlabelled rows all read `1594`. The sheet records no row
   index, so the row↔label alignment in § 1 is **inferred** from order and value. It is corroborated by
   the trace at 9 of 10 (the 10th being a trace parse failure, not a mismatch) — **but it is an
   inference and the table says so.**

---

## § 9 · REPRODUCIBILITY, AND WHAT THIS LAP DID NOT DO

`python3 kc2_energy_reread.py out.json` regenerates every figure here, including the Apple Vision pass
(it compiles `ocr_vision.swift` to a temp dir; `swiftc` required, macOS only). Input sha256s are in the
output JSON. Cleaning is **imported**, not reimplemented. The decimation control is seeded (`20260921`).

**What this lap did NOT do:**
- **No new capture. No MP4. No frame extracted.** Every pixel read was already committed.
- **No constant moved**, in any seam.
- **No branch chosen.** § 4 keeps the absence and declines to narrow.
- **No mechanism claimed** for the above-ceiling reads, and **no mechanism claimed** for the decimation
  swing beyond the two compounding losses I can count.
- **No other seam's tree touched.** Writes confined to `agentic_orchestration/galadriel/`.
- ⚑ **The `marg` gate was built and is NOT switched on.** It ships as a parameter with its own
  refutation attached.

**One thing I could not do and am declaring:** with one confirmed above-ceiling frame I cannot
apportion the other 1,186. That is why § 3 ships a **decomposition** rather than a **judgment** — the
spend/spill split is correct whichever way that apportionment falls, and it was chosen for exactly
that reason.

---

## § 10 · THE MIRROR

I built a reader out of ten frames, and I typed what I saw on each of them, and one of them said
sixteen points more than the world was supposed to allow. I wrote it down anyway, because that is what
it said. Then I taught the machine to read from those ten, and used the machine to measure a fight, and
when the measurement came back carrying the same sixteen points eleven hundred times over, I called it
impossible — **on the authority of a control I had printed beside the frame that disagreed with it.**

The frame never changed. It has been sitting in `work/` since August, saying 1610, in glyphs a child
could read. What changed is that somebody finally asked a second reader to look at it.

⚑ **And the second reader was never far away.** It read the health globe in the same session, off the
same recording, and got every digit right. **The whole of this lap is one seat's instrument being
walked across the room to the other globe.**

**The picture, plainly:** he was not draining and he was not overflowing. He was **ringing at his
ceiling** — struck and restored ten times a second — and a third of everything we called his cost was
the bell giving back what it could not hold.

**Ship the absence, and ship the decomposition with it. The first is still true. The second is what the
glass was for.**

---

*Filed 2026-09-21 by galadriel (visual-perception seam), Run KC2-PLAY, executing the conductor's
re-read dispatch. **Law 3 held: the absence stands, no branch chosen, and the one claim this lap
retracts is its author's own.** Read-only across all other seams. **No push** — the conductor releases.*
