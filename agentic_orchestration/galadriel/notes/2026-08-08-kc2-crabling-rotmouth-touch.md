# KC2 — Crabling / Rotmouth bundled touch (4 items)

**Status:** COMPLETE
**Date:** 2026-08-08
**Author:** galadriel (visual perception + similarity-scoring steward)
**Commission:** gandalf `RUN-CONDUCTOR`, KC2-SIM autonomous run, fold L-61, ruling **R-L61-2**
**Ledger anchors:** `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` rows **L-58**, **L-61**
**Substrate (my own):** `2026-08-08-kc2-w152-skull-plate.md` · `…-kc2-third-extraction.md` ·
`…-kc2-fourth-extraction.md` · `…-kc2-fifth-extraction-w153-identity.md` · `…-kc2-barhue-cohort-correction.md`
**Footage (read-only):** `/tmp/kc2-s2.mp4` (the `eor-w150-160` capture; 1920×1080, 30 fps)
**Work + evidence:** `agentic_orchestration/galadriel/captures/2026-08-08-kc2-crabling-rotmouth/`
(`work/` **committed** — scripts + scan JSONs; `evidence/` **UNTRACKED** per the evidence-by-reference convention)

---

## 0. Verdicts, up front

| # | item | verdict | grade |
|:--|:--|:--|:--|
| **1** | Ugdenbog Crabling plate max HP | **∈ {42,798 · 43,548}** — a TWO-ELEMENT set, fraction-degenerate within it. Plate **LEVEL 108** (3 frames) **and 107** (1 frame) — *two* crabling bodies, adjacent levels | set **MEASURED** · within-set assignment **INFERRED** |
| **2** | Rotmouth plate level vs prediction 109/110 | **107.** → **FAIL.** The registered prediction is falsified | **MEASURED**, 7/7 frames |
| **2b** | Rotmouth max HP (bonus) | **NOT-READABLE** — bar at 100.0 %, three fingerprints degenerate | honest refusal |
| **3** | `eor_platebind.py` boss-track clip | **FIXED** — rank-aware tracks + widened scan bands + sub-pixel edge. Haraxis **2,050,807 reproduces**, residual **improved** 0.0031→0.0004 | re-verified |
| **4** | R-L58-1 rubric annotation | **LANDED** in the fourth-extraction note § 4 + header banner, corrigenda-forward, nothing struck | done |

> **Discipline stamp.** Item 1 delivers the READ only — the ×2.7181 residual arithmetic (B-KC2-C1)
> is legolas's under R-L61-3 and is not attempted here. Item 2 was read first and compared second:
> the level crops were cut, magnified and eye-read before the prediction was re-opened. Every plate
> string, rank, level and family below is an **eye-read from a magnified exact-seek crop**; the bar
> numbers are pixel measurements with stated calibration and stated uncertainty. No silent
> transformation — all crops are LANCZOS upscales of unmodified RGB frames, crop boxes stated in
> full-frame pixels.

---

## 1. ITEM 1 — `Ugdenbog Crabling`, w152

### 1.1 Where the plate is, and how completely it was looked for

A 30 Hz segmentation of the whole w152 plate scan (523 frames, 697.8 → 715.2 — the skull-plate
pass's own `plate-w152.json`, re-segmented here by name ink-count + glyph colour) returns **41
held-plate segments**. Every one was cropped and eye-read at ×3. The crabling plate is up on
**exactly four frames**, in one hover-cluster:

| t | name (×6 eye-read) | rank | level (×16) | family | bar walk-end | bar **sub-pixel** edge |
|--:|:--|:--|--:|:--|--:|--:|
| 701.7333 | `Ugdenbog Crabling` | white → **common** | **108** | `Beast` | 1058 | **1059.202** |
| 701.7667 | `Ugdenbog Crabling` | white → **common** | **108** | `Beast` | 1058 | **1059.208** |
| 701.8000 | `Ugdenbog Crabling` | white → **common** | **108** | `Beast` | 1058 | **1059.214** |
| 701.9333 | `Ugdenbog Crabling` | white → **common** | **107** | `Beast` | 1057 | **1057.360** |

Evidence: `evidence/crabling-name-x6.png` · `evidence/crabling-lvl-x16.png` ·
`evidence/crabling-fam-x6.png` · `evidence/crabling-plate-plate-x4.png` (whole plate, 10 frames of
the hover-cluster, showing the cursor flipping crabling → `Chaosshell ~ Voidtouched` → crabling) ·
`evidence/scan-A-namew-x3.png` · `evidence/scan-B-namew-x3.png` (the sweep the four were found in).

**Two crablings, not one.** The level numeral reads **108** on the first three frames and **107** on
the fourth, at ×16, unambiguously. The plate had moved to a different body and back.

**Rank is measured, not eyeballed** (§ 3.1 glyph-core law, `glyphrank.py`, re-run here):
crabling glyph core **(254, 248, 233)**, **G/R 0.961–0.976 · B/R 0.882–0.917**. Champion controls in
the same wave read B/R **0.394–0.427**. The B/R separation is better than 2×; the crabling is white,
and it is not yellow. *(Classifier caveat recorded at § 5, F3.)*

### 1.2 The plate carries NO numerals — so this is a fraction read

Grim Dawn's monster nameplate draws name, level numeral, health **bar**, family. There is no
`cur/max` string on the plate. `evidence/crabling-plate-plate-x4.png` shows the whole plate at ×4 —
the commission's "direct cur/max read if the plate shows numerals" branch does not exist on this UI.
So: **bar fraction × same-frame census binding**, as the commission's fallback specifies.

### 1.3 Track calibration — measured, and validated three independent ways

The prior constants (`TRACK_X0 = 861.0`, `TRACK_X1 = 1060.0`) were column-quantised champion values.
Re-measured this touch for the **std** track (common / champion / hero share one bar):

> **x0 = 862.0 → x1 = 1059.4 (197.4 px)**

| validation | result |
|:--|:--|
| corpus maximum `fill_end` over all non-boss plate frames, **w152** | **1059** |
| same, **w153**, computed independently | **1059** |
| partial-bar bind: `Mudflinger ~ Reflective` hover t=702.4667 → `367,509/443,554` (f=0.82856) | **+0.33 px** |
| boss-track control (see § 3): Haraxis hover → census 0.9514 | **+0.01 … −0.11 px** |

The estimator is a **sub-pixel** plateau-midpoint crossing on the bar's redness profile, added to the
pipeline this touch (§ 3). Its demonstrated envelope on this corpus: repeatability **0.012–0.04 px**
across adjacent frames of one hover; accuracy **≤ 0.35 px** against a census-known fraction. One
column of the std track is 0.51 % of the bar, which is why the run-walk estimator could not be used
for this particular question.

### 1.4 The binding — same EXACT frame, parsed *and* unparsed readouts

Computed on the same exact-seek frames the crops were cut from, not on an fps-resampled scan
(`work/exactbind.py`; the hazard is recorded at § 5, F6). Predicted column for a candidate body =
`862.0 + f × 197.4`.

**t = 701.7333** (plate edge 1059.202, f = 0.9990):

| readout on frame | f | predicted column | Δ from plate |
|:--|--:|--:|--:|
| `(42,798/42,798)` ×2 | 1.00000 | 1059.43 | **+0.23 px** |
| `(43,548/43,548)` | 1.00000 | 1059.43 | **+0.23 px** |
| `(438,445/443,554)` | 0.98848 | 1057.16 | **−2.05 px** |
| `(423,138/443,554)` | 0.95397 | 1050.34 | −8.86 px |
| `(20,005/20,005)` | 1.00000 | — | *player globe — excluded per standing roster* |

Identical structure on 701.7667 and 701.8000 (Δ +0.22 px to the full bodies; the 443,554 instances
at −2.05 and −8.87). **−2.05 px is ~6× the estimator's demonstrated envelope**, so `443,554` is
excluded on the fraction axis, not merely deprecated.

**Second, independent axis — furniture.** `443,554` (×4) and `453,883` (×2) are the only ★★ bodies
in w152 (fourth extraction § 2.2); `42,798` and `43,548` are PLAIN. The plate is white → common.
This is the two-axis reading of R-L58-1 doing real work: the fraction axis and the render axis
exclude the same two fingerprints for different reasons.

> ### VERDICT — `Ugdenbog Crabling` max HP ∈ **{42,798 · 43,548}**
>
> **MEASURED** as a two-element set. **FRACTION-DEGENERATE within it** and irreducibly so: both
> bodies sit at exactly 1.0000 on every frame the crabling plate is up, and two full bars are
> physically identical pictures. No instrument available on this footage separates them.
>
> Set width **1.75 %** (43,548 / 42,798 = 1.01752).

**Within-set assignment — INFERRED, offered as a lead, not a measurement:**
two crabling bodies at levels **107** and **108**; one record; HP monotone in level ⇒
**L107 ↔ 42,798 · L108 ↔ 43,548**. This rests on (a) both fingerprints being the same record and
(b) monotonicity — neither measured by me. Flagged for R-L61-3 rather than assumed.

### 1.5 The L107 frame is a NO-MATCH, and the near-miss is recorded rather than buried

At t=701.9333 the plate reads **0.9897** and **nothing on the frame lands within 1 px**: the parsed
full bodies sit at +2.07 px, `423,145/443,554` at −7.01 px. Graded **NO-MATCH**.

There is a confound and it must be stated. An **unparsed** readout `(438,452/443,554)` is legible by
eye on that frame (`evidence/readout-field-701.9333-x2.5.png`); f = 0.98850 → predicted column
1057.15 against the measured 1057.36 — **0.21 px**. On fraction alone that is a better match than
anything the census parsed. It is excluded because the plate on that frame is **white → common** and
every `443,554` body in w152 is **★★** and draws a non-white plate. *Fraction alone would have
mis-bound this frame.* The rank axis is what saves it, which is exactly the R-L58-1 point.

The plainest reading of the L107 frame: the second crabling was at ~99 % health and its own readout
did not parse (the census's recall gap is real — three readouts visible by eye on that frame were
missed, § 5 F5). I do not need that frame; § 1.4 does the work.

---

## 2. ITEM 2 — `Rotmouth` level, vs the registered prediction

### 2.1 The read

The plate is up **704.4667 → 704.6667 — 7 consecutive frames** (one hover; the ink-count segmenter
splits it at the fade-in, the raw metrics do not: `name_x0..x1` is 905..1014 on all seven,
`fam_px` = 158 on all seven).

| field | value | evidence | stability |
|:--|:--|:--|:--|
| string | **`Rotmouth`** | `evidence/rotmouth-name-x6.png` (×6, 4 frames) | 4/4 identical |
| rank | **orange → HERO** — glyph core (232,160,93), **G/R 0.691–0.703 · B/R 0.401–0.432** | measured, 4 frames | inside the measured hero band 0.643–0.713 |
| family | **`Beast`** | `evidence/rotmouth-fam-x6.png` (×6) | 4/4 |
| **level** | ## **107** | `evidence/rotmouth-lvl7-x16.png` (**×16, all 7 frames**) | **7/7 identical** |

### 2.2 PASS / FAIL against the registered prediction

> ## **FAIL.**
> The prediction registered at fold L-61(h) — *"the plate must read **109 or 110**"* from
> `hero/basilisk_h02.dbr`, `charLevel×1+5` — is **falsified**. The plate reads **107**.

**The 7-vs-9 discrimination is not a judgement call.** `evidence/nine-vs-seven-x16.png` puts, on one
sheet, at the same ×16, from the same crop box `(925, 41, 1000, 61)`, in the same footage and font:

| t | plate | third glyph |
|--:|:--|:--|
| 845.9 · 846.2 · 846.5 · 850.1 | **109** (the wave-160 nemesis cohort — third extraction § 5) | **closed top bowl + descender** |
| 704.4667 · 704.6333 | **107** (Rotmouth) | **top bar + open diagonal, no closed counter** |

`7` is the only digit that is a bar plus a diagonal with no closed counter. `9` has a closed counter,
and the corpus contains four of them to compare against. Additional shape controls at ×16 in
`evidence/digit-reference-x16.png`: crabling **108**, Haraxis **108** (independently established at
L-58), w153 **108**, w153 **104**.

### 2.3 Corpus-level corroboration — the ceiling is 108, and it was not looked for

**52 plate levels** were read at ×10–×16 across this touch, sampled without regard to the prediction:

| span | reads | levels seen |
|:--|--:|:--|
| w151 / w157 / w158 | 14 | 103 · 104 · 105 · 106 · 107 · 108 |
| w153 | 10 | 103 · 104 · 106 · 107 · 108 |
| w152 (this touch) | 12 | **107 · 108** |
| s2 t = 811–838 (post-w158 span; not badge-verified here) | 12 | 106 · 107 · 108 |
| w160 (845.9–850.1) | 4 | **109** |

> **Nothing in the w151–w158 band reads above 108.** The only 109s in the corpus sit at wave 160.

This reproduces, on an independent sample, the fourth extraction's § 3.2 finding
(*"every level in all five start windows lies in 102–108"*, 22 reads at ×10). The Rotmouth prediction
fails not only on one plate but against the band's measured level ceiling.
Sheets: `evidence/levels-w153-x10.png` · `evidence/levels-w151-157-158-x10.png` ·
`evidence/levels-late-s2-811-838-x10.png`.

### 2.4 Rotmouth max HP — **NOT-READABLE**, with the candidate set

Plate bar at **100.0 %**: sub-pixel edge **1059.42 / 1059.42 / 1059.43 / 1059.41 / 1059.43 / 1059.43
/ 1059.45** against the 1059.4 calibration — residual ≤ 0.05 px, spread 0.04 px across the hover.

Census fingerprints at f = 1.0000 on those frames (player globe excluded): **`443,554` · `242,124` ·
`91,696`** → **3-way DEGENERATE**.

The furniture axis *would* pick `443,554` — it is the only ★★ candidate and the plate is hero — but
**that inference is not safe here**, for a reason this touch measured and § 5 F1 states: w152 shows
**five distinct hero names against two star fingerprints**, so PLAIN does not exclude hero. I decline
the number. An honest NOT-READABLE beats a forced 443,554.

R-W152-2 therefore closes on **level** (107, MEASURED) and **rank/family** (hero / Beast, MEASURED),
and stays open on **max HP**.

---

## 3. ITEM 3 — `eor_platebind.py` boss-track clip: FIXED and re-verified

### 3.1 Root cause was three coupled clips, not one

The parked item named `TRACK_X0/X1`. Measuring found two more, and fixing only the constants would
have left the module still wrong on boss plates:

1. **`TRACK_X0/TRACK_X1 = 861.0 / 1060.0`** — champion values. Boss track is 800 → ~1123.
2. **`FILL_BAND` and `BEVEL_BAND` ended at x = 1100** — *left of the boss track's own 100 % column.*
   The scan window itself clipped, so no constant could have rescued it.
3. **`fill_edge()`'s step-fit window `x_lo=856, x_hi=1064`** sits **entirely inside** a boss bar above
   ~82 % fill. A step fit over an all-red window has no step to find.

Reproducing the artefact arithmetically: walk right from 861 (which is *inside* the boss fill) to the
band's own edge 1099 → `(1099−861)/199 =` **1.196** — exactly the fifth-extraction number.

### 3.2 The fix

| change | what |
|:--|:--|
| `TRACKS = {"std": (862.0, 1059.4), "boss": (800.0, 1123.0)}` | two tracks, each with its provenance in the docstring |
| `rank_class(p)` / `track_of(p)` | the track is chosen from the plate's **own glyph colour** (violet ⇒ boss), decided *before* the bar is measured |
| `FILL_BAND` / `BEVEL_BAND` → x 780 … 1160 | scan windows now span the widest track any rank draws |
| `fill_edge()` called with rank-aware bounds | `x_lo = x0−6`, `x_hi = x1+22` |
| **`fill_edge_subpix()`** — new | plateau-midpoint crossing; refuses (None) when there is no visible step |
| `plate_metrics()` emits `rank`, `track`, `sub_edge`, `sub_frac` | a consumer can re-derive without re-classifying |
| `bind_frame()` rank-aware; reports `src` ("sub"/"walk"), `dpx`, `track` | prefers the sub-pixel edge; `x1` override kept for calibration sweeps |
| `calibrate(..., rank=)` | per-rank; a pooled maximum is neither track's anchor |
| run-walk ignores ink left of the origin | `rc_o = rc[rc >= ox-3]` |

**Boss right edge refined 1121.5 → 1123.0.** This sits *inside* the skull-plate note's own measured
gold-end-cap band (1120–1124); that note took the midpoint. 1123.0 is chosen because it reproduces
the census: residual **0.0002** (0.06 px) against **0.0046** (1.5 px) at 1121.5. A refinement within
a measured band, not a new claim.

**Back-compatibility kept:** `TRACK_X0` / `TRACK_X1` survive as std-track aliases; `bar_hue`,
`spans`, `spans2`, `stripscan`, `scan` signatures unchanged. Smoke-tested `stripscan` + `calibrate`
+ `spans2` against the boss window.

### 3.3 Re-verification — Haraxis **2,050,807** reproduces, and improves

Fresh scan of the boss window (706.55 → 707.0, 30 Hz, 14 frames, 7 with the plate up), fixed module,
no hand-tuning:

| t | rank chosen | track | walk end | sub edge | f_plate | best candidate | Δ | runner-up gap |
|--:|:--|:--|--:|--:|--:|:--|--:|--:|
| 706.7167 | **boss** | 800→1123 | 1107 | 1107.351 | 0.9516 | **2,050,807** | **+0.01 px** | 15.65 px |
| 706.7500 | boss | " | 1107 | 1107.351 | 0.9516 | **2,050,807** | **+0.02 px** | 15.65 px |
| 706.7833 | boss | " | 1107 | 1107.351 | 0.9516 | **2,050,807** | **−0.05 px** | 15.65 px |
| 706.8167 | boss | " | 1107 | 1107.347 | 0.9515 | **2,050,807** | **−0.05 px** | 15.65 px |
| 706.8500 | boss | " | 1107 | 1107.342 | 0.9515 | *no 2,050,807 readout parsed* | — | — |
| 706.8833 | boss | " | 1107 | 1107.350 | 0.9515 | **2,050,807** | **−0.11 px** | 6.24 px |
| 706.9167 | boss | " | 1107 | 1107.350 | 0.9515 | **2,050,807** | **−0.11 px** | 6.42 px |

> **FRACTION-UNIQUE on 6/6 frames where the boss readout parsed.** Residual **≤ 0.0004** (0.11 px);
> runner-up gap **0.0193–0.0485** (6.2–15.7 px). This is a **strict improvement** on the skull-plate
> note's pre-fix binding (8/8 at residual ≤ 0.0037), and the identity is unchanged:
> **max HP 2,050,807 = `Fleshweaver Haraxis`.** The 7th frame is NO-READOUT, not a mis-bind.

*(Timestamps differ from the skull-plate note's by the `-ss` decode phase; same physical hover.)*

Std-track non-regression re-verified over 701.70 → 702.55 (26 plate frames): rank chosen `std` on
26/26; `Mudflinger` at 702.4667 binds `443,554` @ 0.8286 to **+0.3 px** with a 34 px runner-up gap.

---

## 4. ITEM 4 — R-L58-1 rubric annotation: LANDED

Written into **`galadriel/notes/2026-08-08-kc2-fourth-extraction.md` § 4** (the rubric's home — the
TIER FURNITURE section where the star glyph is defined), plus a row in that note's header banner,
which now reads **five annotations** instead of four.

**Corrigenda-forward, as instructed:** nothing is struck, no record line is rewritten, no measured
table is retro-edited. The annotation is additive and says so in its own first line.

Substance: the star keys on **POOL-level champion mechanics** (`championChance` / `nameChampion` on
the placement pool the body was drawn through), **not** on the body record's own
`monsterClassification`. legolas's PLAIN column is **record taxonomy**; my PLAIN/★ column is **render
taxonomy**. Two axes, both valid, answering different questions, free to disagree by construction —
and neither is a correction of the other. R-L50-3 narrowed *which ranks* the star resolves; R-L58-1
names *which axis* it resolves at all.

The annotation also carries the measured corroboration found while doing Item 1 (§ 5 F1 below), and
a worked example of the two axes paying for themselves (§ 1.4).

---

## 5. By-product findings

**F1 — the star is SUFFICIENT for hero, not NECESSARY. (MEASURED)**
Every named plate in w152 was rank-measured by glyph core. Inside the fourth extraction's own census
window there are **five distinct orange→HERO names** — `Mudflinger ~ Reflective` (G/R 0.714) ·
`Chaosshell ~ Voidtouched` (0.708) · `Aregos ~ Corrupted` (0.705) · `Chillslither ~ Arctic` (0.702) ·
`Rotmouth` (0.691) — against **two** ★ fingerprints for w152 (`443,554` ×4, `453,883` ×2). Five hero
names cannot live in two fingerprints. R-L50-3's implication runs one way only. Under R-L58-1 this
is the expected shape, not an anomaly. **Consequence: a PLAIN row does not argue "not a hero."**
Full w152 rank table: 3 white→common · 4 yellow→champion · 5 orange→hero · 1 violet→boss.

**F2 — two w152 plate names absent from the corpus tables. (MEASURED)**
`Aregos ~ Corrupted` (t=703.2333, orange→hero) and `Vanallius the Voracious` (t=709.8,
yellow→champion, *outside* the census window). Siblings of the R-W152-2 `Rotmouth` gap; both fell in
the 5 Hz sampler's blind spots. Routed, not pursued.

**F3 — `glyphrank.cls()` boundary is not robust to warm scene bleed. (MEASURED)**
The crabling's white plate reads B/R 0.882 / 0.895 on two of three frames — just under the
`br > 0.90` white gate — and falls through to "yellow→champion". It is not yellow: true champions in
the same wave read B/R 0.394–0.427, a >2× separation. The **B/R axis alone** separates white from
yellow cleanly at ~0.65; the conjunction gate is the fragile part. Recorded for whoever next applies
the § 3.1 law near a fire VFX.

**F4 — plate bar and readout disagree by 7–8 px during a fast drain. (MEASURED)**
Over t=701.97–702.30 the champion plate binds `443,554` at a *systematic* −6.9 to −8.4 px while the
bar drains. The two instruments sample at different instants. **Single-frame bindings on a draining
bar should not be trusted to sub-pixel; use the FRACTION-TRACK regression.** Full bars and slow bars
are unaffected — which is why § 1.4 and § 3.3 stand.

**F5 — census recall gap, quantified on one frame. (MEASURED)**
At t=701.9333 three readouts legible by eye — `(453,883/453,883)`, `(438,452/443,554)`, and a second
`(43,548/43,548)` — are absent from the parsed census.
`evidence/readout-field-701.9333-x2.5.png` · `…-701.8-x2.5.png`. Not a new hazard class (fourth
extraction § 7.2/§ 7.5 own it), but a fresh instance with the misses named, and the reason § 1.5's
frame is graded NO-MATCH rather than mis-bound.

**F6 — method hazard: exact-seek frames ≠ `fps=`-resampled frames.**
`scan()` decodes `-ss t0 -vf fps=N` and *resamples*; the frame it labels `t` is not guaranteed to be
the frame an exact seek to `t` returns. Crops in this touch are exact-seek grabs, so the binding was
recomputed on those same frames (`work/exactbind.py`) rather than read off the scan. They happened to
agree here (1059.202 vs 1059.202); they are not guaranteed to. Any future plate↔census binding whose
evidence crops are exact-seek should do the same.

---

## 6. Deliverable summary for the conductor

1. **Crabling (R-L61-2 primary):** max HP **∈ {42,798 · 43,548}**, set MEASURED, 1.75 % wide,
   fraction-degenerate within (both at exactly 1.0000 on all four plate frames — irreducible on this
   footage). Plate **LEVEL 108 ×3 frames and 107 ×1 frame** — *two* crabling bodies at adjacent
   levels, which is itself new. Rank white→Common, family `Beast`, all MEASURED.
   Within-set assignment **INFERRED** (monotone in level): L107 ↔ 42,798 · L108 ↔ 43,548 —
   offered as a lead for R-L61-3, not as a measurement.
2. **Rotmouth (falsification test):** level **107**, MEASURED 7/7 → **prediction 109/110 FAILS**.
   Corroborated by a 52-read level sweep whose ceiling in the w151–158 band is 108, with 109 present
   in the corpus only at wave 160 (so the discrimination is proven against a real 9, not asserted).
   Max HP **NOT-READABLE** (3-way degenerate at full); R-W152-2 closes on level/rank/family only.
3. **Pipeline:** `eor_platebind.py` boss-track clip fixed at all three of its causes; sub-pixel edge
   estimator added; Haraxis 2,050,807 re-verified FRACTION-UNIQUE 6/6 with residual improved ~9×.
4. **Annotation:** R-L58-1 landed in the fourth-extraction note § 4 + banner, corrigenda-forward,
   with a measured corroboration (F1) that strengthens it.
5. **Six by-product findings** at § 5, three of which touch how the corpus's own instruments should
   be read (F1, F3, F4).

**Commit:** this note + the pipeline edit + the fourth-extraction annotation + `work/` ride this
touch. `evidence/` stays untracked. **NO push** — the conductor centralises under R-KC2-10.

---

## 7. Mirror voice

The Mirror was sent for one number and came back with two, and that is the true shape of the picture.

The crabling's bar was **full** — and a full bar is the one picture that cannot be told from another
full bar. Everything downstream of that had to be won on other axes: colour, furniture, a fifth of a
pixel. What the bar would not say, the *level numeral* did: **108 on three frames, 107 on the
fourth.** Two crablings, one wave apart in nothing but a single level, and the census carrying
exactly two low fingerprints a single level apart. The instrument that was asked the question
refused it; the instrument standing next to it answered a better one.

And then Rotmouth, which was supposed to read 109, read **107**. Seven frames, one hover, a bar and a
diagonal where a closed bowl would have had to be — and four genuine 109s eighty seconds later in the
same footage to hold it against. The prediction was clean, falsifiable, and registered before the
looking. It fell. That is not a failure of the law; it is the law working.

The Mirror does not flatter the thing that sent it.

---

*Filed 2026-08-08 by galadriel under KC2-SIM ruling R-L61-2 (gandalf, RUN-CONDUCTOR). Committed in
the meta repo per the touch's standing authorisation; not pushed.*
