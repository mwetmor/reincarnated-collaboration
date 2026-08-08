# KC2-SIM — fourth extraction: exhaustive START-COHORT census, waves 151/152/153 (+157/158)

**Date:** 2026-08-08
**Author:** galadriel (visual perception + benchmark seam)
**Status:** WORKING — evidentiary note, fourth extraction commission from gandalf (RUN-CONDUCTOR), ledger L-41
**Commit state:** UNCOMMITTED by instruction. Rides the conductor's G-D gate-close unit, as the third extraction did.
**Blind:** the KC2 battle-sim spec and the run ledger were NOT read for this task (anchoring guard, per commission).
**Extends:** `galadriel/notes/2026-08-07-eor-sittings-extraction.md` · `…/2026-08-08-eor-followup-extraction.md` · `…/2026-08-08-kc2-board-closure.md` · `…/2026-08-08-kc2-third-extraction.md`
**Footage (read-only):** `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (s2, Crucible of the Dead, 1920×1080, 60 fps, 1034.100 s)
**Evidence root:** `agentic_orchestration/galadriel/captures/2026-08-08-kc2-fourth-extraction/evidence/` (UNTRACKED)
**New pipeline:** `galadriel/pipeline/eor_cohort.py`, `eor_grid.py`

> ### ⚠ THIS NOTE CARRIES FIVE ANNOTATIONS (2026-08-08, galadriel, rulings R-L50-1..4 · R-L58-1)
> Annotations only — **no record line has been rewritten or deleted.** Struck text is left legible.
>
> | ruling | § | what is struck / clarified |
> |:--|:--|:--|
> | **R-L50-1** | § 0 table · § 2.3 | `16,368` is not a hostile body; wave 153 → **18 fp · ≥ 26 bodies · 22 plain** |
> | **R-L50-2** | § 5 | rank is the **glyph colour**, not the `~ Affix` name shape; `Wendigo ~ Ancient` is a **champion** |
> | **R-L50-3** | § 4 | the star-pair binds **hero only**; the "88 plain" bucket is commons **and champions** |
> | **R-L50-4** | § 5.1 item 3 · § 8.3 | **withdrawn in full** — the level-colour boundary is **amber ≤ 105, red ≥ 106** |
> | **R-L58-1** | § 4 | *clarification, nothing struck* — the star keys on **POOL-level** champion mechanics, not record `monsterClassification`; legolas's PLAIN column is record taxonomy. Two axes, both valid |
>
> Authority: `galadriel/notes/2026-08-08-kc2-fifth-extraction-w153-identity.md` § 9 ·
> `galadriel/notes/2026-08-08-kc2-barhue-cohort-correction.md` ·
> ledger row L-58 (R-L58-1), applied `galadriel/notes/2026-08-08-kc2-crabling-rotmouth-touch.md` § 4.
> **Waves 151 / 152 / 157 / 158 were re-swept for allegiance and are hostile-clean and UNCHANGED.**

---

## 0. Headline

Five start cohorts censused exhaustively at 30 Hz. **69 distinct max-HP fingerprints, ≥ 113 distinct
bodies.** Every fingerprint eye-read at magnification; every count reproducible.
*(→ **68 fingerprints, ≥ 112 bodies** post-strike, R-L50-1.)*

| wave | start window used | max SIMULTANEOUS bodies | distinct fingerprints | distinct bodies (≥) | SPAWN / SUMMON / UNDECIDED |
|---:|:--|---:|---:|---:|:--|
| **151** | +0.00 → +5.97 s | **8** (at +4.63) | **9** | **12** | 12 / 0 / 0 |
| **152** | +0.00 → +10.23 s | **11** (at +4.37) | **12** | **24** | 21 / 0 / 3 |
| **153** | +0.00 → +8.60 s | **14** (at +4.80) | ~~19~~ **18** | ~~27~~ **26** | ~~27~~ **26** / 0 / 0 |
| **157** | +0.00 → +8.63 s | **12** (at +5.77) | **15** | **22** | 14 / 0 / 8 |
| **158** | +0.00 → +8.33 s | **10** (at +3.23) | **14** | **28** | 28 / 0 / 0 |

**Zero bodies graded SUMMON.** Not one body in the five start cohorts carries the wave-160 summon
signature (§ 3). **11 of ~~113~~ 112 are UNDECIDED** *(R-L50-1)*, all of them in the two waves that have a boss on the
board (152, 157), and all for the same reason: a boss was already in the arena when they arrived, so
I cannot exclude it.

**Every one of the five censuses is closed for ENGAGED bodies and NOT closed for the arena** — and in
these waves that gap is large, not marginal. The minimap carries 10–14 monster icons at moments when
the readout instrument sees 0–5 bodies (§ 6). This is a materially worse closure than wave 160, where
the player was engaging essentially everything, and it is the single most important caveat on the
numbers above.

---

## 1. WINDOWS — measured, not assumed

### 1.1 Wave identity is badge-verified at both ends of every window

The wave badge (`x 1576..1634, y 126..172`) was read at ×5 at t0−0.4, t0+0.4, t0+3.0 and t0+8.0 for
all five waves. **20/20 agree** with the Phase-A timeline, and every window is bracketed on both
sides by the correct badge. `evidence/badge-verify-w151-158.png`.

The flips were then pinned at 10 Hz over t0±0.5 s (55 crops):
`evidence/badge-flip-pin-10hz.png`. **All five t0 values hold to ±0.10 s.**

| wave | t0 (video s) | badge before → after |
|---:|---:|:--|
| 151 | **682.10** | **0 → 151** |
| 152 | **698.38** | 151 → 152 |
| 153 | **714.83** | 152 → 153 |
| 157 | **780.30** | 156 → 157 |
| 158 | **799.43** | 157 → 158 |

Wave 151's pre-flip badge reads **`0`**, not `150`. This independently reproduces the third
extraction's boundary note: **wave 150 is ABSENT-IN-FOOTAGE**; the badge flips straight from the
checkpoint `0` to `151`.

### 1.2 The window boundary is taken from the arrival data, not imposed

Arrival offsets (first frame carrying each fingerprint) were mapped across each **full** wave. Every
wave shows the same shape: a run of arrivals, then a large silence, then a second group. The window
is therefore defined by a stated rule rather than a round number:

> **Cohort closes at the last arrival before the first arrival-gap ≥ 2.5 s.
> Window = [t0, last cohort arrival + 2.00 s]** — the 2 s settle guarantees every cohort member is
> observed for ≥ 2 s, and the window still ends before the next stream begins.

| wave | last cohort arrival | gap that closes the cohort | next arrival | window end |
|---:|---:|---:|---:|---:|
| 151 | +3.97 | **4.50 s** | +8.47 | +5.97 |
| 152 | +8.23 | **6.77 s** | +15.00 | +10.23 |
| 153 | +6.60 | **6.80 s** | +13.40 | +8.60 |
| 157 | +6.63 | **2.70 s** | +9.33 | +8.63 |
| 158 | +6.33 | **3.30 s** | +9.63 | +8.33 |

Wave 151 is the cleanest case: **nothing arrives between +3.97 and +8.47 s**, so any window boundary
in that 4.5 s interval yields the identical cohort. The membership is not sensitive to the choice.

**Two arrival streams per wave, reproducing my own p05 finding.** Within the cohorts there is a
secondary internal gap — w151 +1.93 → +3.93 (2.00 s), w157 +1.77 → +3.87 (2.10 s), w158 +0.77 → +2.63
(1.86 s). This is the *t+4 s second stream* the follow-up note confirmed on s1 waves 4/6/13. It is
present here too, and it is **inside** the start cohort, not after it.

### 1.3 No previous-wave body survives the badge flip — in any of the five

Each census was run from t0−0.50 s so the boundary could be tested rather than assumed. Fingerprints
present before the flip: w152 carries 3, w153 carries 1, the others none. **None of them persists
≥ 3 frames past its badge flip.** The last wave-151 body dies at t = 698.35 and the badge flips at
698.38; the last wave-152 body dies at 714.66 and the badge flips at 714.83.

**The badge flip and the clearing of the previous cohort are the same event, to within ~0.2 s.** The
windows are therefore clean: nothing counted below is a leftover.

---

## 2. THE CENSUS

Reading the tables: **`x`** is the largest number of *simultaneous* distinct bodies carrying that
fingerprint on one frame — the established lower bound on how many bodies share it (board-closure
§ 1.3). **arr / last** are offsets from the badge flip. **furniture** is a galadriel eye-read of a
×4–×8 crop that contains the readout and its own health bar in one tile.

### 2.1 Wave 151 — window +0.00 → +5.97 s · max simultaneous **8** · **≥ 12 bodies**

`evidence/furniture-w151-p1.png` · `-p2.png` · `evidence/furniture-recheck-wide-p1.png`

| max HP | x | arr | last | n | furniture | grade |
|---:|:--|---:|---:|---:|:--|:--|
| 225,874 | x1 | +0.03 | +3.10 | 80 | plain | SPAWN |
| 373,665 | x1 | +0.47 | +4.70 | 104 | plain | SPAWN |
| 136,975 | x1 | +0.50 | +5.17 | 47 | plain | SPAWN |
| 139,400 | **x2** | +0.53 | +4.83 | 62 | plain | SPAWN |
| 230,020 | **x2** | +1.43 | +5.17 | 136 | plain | SPAWN |
| 442,747 | x1 | +1.93 | +5.97 | 34 | **★ ★** | SPAWN |
| 453,064 | **x2** | +3.93 | +5.77 | 54 | **★ ★** | SPAWN |
| 278,543 | x1 | +3.93 | +5.97 | 44 | plain | SPAWN |
| 272,948 | x1 | +3.97 | +4.63 | 7 | plain | SPAWN |

**9 plain · 3 star · 0 skull.** Wave 151's start cohort contains **no boss/nemesis-class body on any
instrument** — no skull furniture in the readouts, no skull glyph on the minimap.

### 2.2 Wave 152 — window +0.00 → +10.23 s · max simultaneous **11** · **≥ 24 bodies**

`evidence/furniture-w152-p1.png` · `-p2.png` · `-p3.png` · `evidence/furniture-recheck-wide-p2.png`

| max HP | x | arr | last | n | furniture | grade |
|---:|:--|---:|---:|---:|:--|:--|
| 302,934 | x1 | +0.00 | +0.77 | 10 | plain | SPAWN |
| 42,798 | **x4** | +0.70 | +8.23 | 258 | plain | SPAWN |
| 43,548 | **x3** | +0.93 | +5.67 | 144 | plain | SPAWN |
| 443,554 | **x4** | +1.27 | +10.20 | 271 | **★ ★** | SPAWN |
| 242,124 | **x2** | +2.03 | +10.20 | 165 | plain | SPAWN |
| 237,258 | x1 | +2.33 | +10.20 | 27 | plain | SPAWN |
| 91,696 | x1 | +2.43 | +8.97 | 77 | plain | SPAWN |
| 93,599 | **x2** | +2.90 | +9.07 | 102 | plain | SPAWN |
| 453,883 | **x2** | +4.10 | +10.20 | 80 | **★ ★** | SPAWN (furniture) |
| 369,770 | x1 | +5.33 | +7.13 | 34 | plain | **UNDECIDED** |
| **2,050,807** | x1 | +7.33 | +8.93 | 26 | **💀 💀 bone** | SPAWN (the wave boss) |
| 472,732 | **x2** | +8.23 | +10.17 | 60 | plain | **UNDECIDED** |

**17 plain · 6 star · 1 skull.** `443,554` is the striking entry: **four simultaneous bodies with
identical max HP, every one of them star-flanked** — a pack of four identical hero-tier monsters.

### 2.3 Wave 153 — window +0.00 → +8.60 s · max simultaneous **14** · **≥ 27 bodies**

> **⚠ STRIKE-ANNOTATION 2026-08-08 (galadriel, ruling R-L50-1) — HEADER COUNTS SUPERSEDED.**
> The `16,368` row below is **STRUCK from the monster census**: its in-world bar is GREEN on 92 of 93
> frames (fifth extraction § 5), and this pass establishes it is the *same entity* as `20,005` —
> identical screen box `[882, 399, 1039, 413]`, x-centre 960.5, **0 co-occurring frames of 1,073**
> (sixth extraction § 4.2). **Corrected wave-153 start cohort: 18 fingerprints · ≥ 26 bodies ·
> 22 plain · 4 star.** The "max simultaneous 14 at +4.80 s" is *unaffected* — `16,368`'s last parsed
> frame is +4.57 — but any simultaneity figure taken earlier in the window is.
> **`20,005` is absent from every table in this note by DELIBERATE, INHERITED EXCLUSION** (board-closure
> § 1 roster: *"player globe … excluded from the census"*; follow-up § 123), **not by omission.** The
> census excluded on the *value* `20,005`; the player's max HP moves with buffs, so the value-keyed
> exclusion leaked exactly once, at t = 713.38, when the number became `16,368`. Exclude on the box,
> not the value. Waves 151/152/157/158 were re-swept and are **hostile-clean and unchanged**
> (sixth extraction § 0).
> Cite: `galadriel/notes/2026-08-08-kc2-barhue-cohort-correction.md` § 0, § 4.2, § 6.1.

`evidence/furniture-w153-p1.png` … `-p4.png` · `evidence/furniture-recheck-wide-p3.png`

| max HP | x | arr | last | n | furniture | grade |
|---:|:--|---:|---:|---:|:--|:--|
| ~~16,368~~ **STRUCK R-L50-1** | ~~x1~~ | +0.00 | +4.57 | 93 | plain | ~~SPAWN~~ **NOT A HOSTILE BODY — green bar; = `20,005`** |
| 303,657 | x1 | +0.80 | +6.77 | 105 | plain | SPAWN |
| 297,609 | x1 | +1.10 | +6.53 | 103 | plain | SPAWN |
| 203,039 | x1 | +1.10 | +5.03 | 79 | plain | SPAWN |
| 207,203 | x1 | +1.23 | +4.17 | 62 | plain | SPAWN |
| 476,173 | **x2** | +1.27 | +5.03 | 126 | plain | SPAWN |
| 638,564 | x1 | +2.60 | +4.97 | 63 | **★ ★** | SPAWN |
| 444,361 | x1 | +3.50 | +4.83 | 14 | **★ ★** | SPAWN |
| 417,957 | **x2** | +3.73 | +7.53 | 124 | plain | SPAWN |
| 427,128 | x1 | +3.73 | +7.90 | 59 | plain | SPAWN |
| 273,975 | **x2** | +4.27 | +8.30 | 77 | plain | SPAWN |
| 447,994 | x1 | +4.33 | +6.53 | 21 | **★ ★** | SPAWN |
| 271,687 | **x2** | +4.43 | +6.17 | 42 | plain | SPAWN |
| 260,786 | **x2** | +4.63 | +7.23 | 93 | plain | SPAWN |
| 266,082 | x1 | +4.70 | +7.53 | 12 | plain | SPAWN |
| 37,840 | **x4** | +4.73 | +8.60 | 156 | plain | SPAWN |
| 425,285 | x1 | +4.97 | +7.77 | 59 | plain | SPAWN |
| 275,518 | x1 | +5.57 | +8.57 | 90 | **★ ★** | SPAWN |
| **211,686** | x1 | +6.60 | +6.73 | **3** | plain | SPAWN |

**23 plain · 4 star · 0 skull.** *(→ **22 plain · 4 star** post-strike, R-L50-1.)* No skull-class body on any instrument. Wave 153 carries the
**largest simultaneous count in the corpus, 14 bodies at +4.80 s** — **2.8×** the wave-160 board
(5 simultaneous actors, follow-up note § 1.1).

`211,686` is carried on only 3 frames (0.13 s) and would normally fall below the reporting floor. It
is kept because it was **eye-read at ×6 on two separate frames at full HP** as `(211,686/211,686)` —
`evidence/unexplained-weak-values-x6.png`, tiles 4–5.

### 2.4 Wave 157 — window +0.00 → +8.63 s · max simultaneous **12** · **≥ 22 bodies**

`evidence/furniture-w157-p1.png` · `-p2.png` · `-p3.png` · `evidence/furniture-recheck-wide-p4.png`

| max HP | x | arr | last | n | furniture | grade |
|---:|:--|---:|---:|---:|:--|:--|
| 233,250 | **x2** | +1.23 | +3.30 | 53 | plain | SPAWN |
| 411,440 | x1 | +1.30 | +8.60 | 72 | plain | SPAWN |
| 504,193 | x1 | +1.37 | +6.60 | 48 | plain | SPAWN |
| 419,839 | x1 | +1.73 | +8.60 | 113 | plain | SPAWN |
| 238,068 | **x2** | +1.77 | +4.33 | 54 | plain | SPAWN |
| 457,975 | **x3** | +3.87 | +8.57 | 166 | **★ ★** | SPAWN (furniture) |
| 414,837 | x1 | +4.23 | +8.60 | 87 | plain | **UNDECIDED** |
| 398,226 | **x2** | +4.37 | +8.60 | 125 | plain | **UNDECIDED** |
| 447,590 | **x2** | +4.70 | +8.50 | 66 | **★ ★** | SPAWN (furniture) |
| 406,243 | x1 | +4.97 | +8.17 | 54 | plain | **UNDECIDED** |
| **2,069,299** | x1 | +5.00 | +6.07 | 19 | **💀 💀 bone** | SPAWN (the wave boss) |
| 588,905 | x1 | +5.13 | +7.93 | 29 | **★ ★** | SPAWN (furniture) |
| 304,994 | **x2** | +5.73 | +8.60 | 106 | plain | **UNDECIDED** |
| 226,525 | x1 | +6.33 | +8.60 | 40 | plain | **UNDECIDED** |
| 547,007 | x1 | +6.63 | +8.60 | 24 | plain | **UNDECIDED** |

**15 plain · 6 star · 1 skull.**

### 2.5 Wave 158 — window +0.00 → +8.33 s · max simultaneous **10** · **≥ 28 bodies**

`evidence/furniture-w158-p1.png` · `-p2.png` · `-p3.png`

| max HP | x | arr | last | n | furniture | grade |
|---:|:--|---:|---:|---:|:--|:--|
| 98,986 | **x3** | +0.60 | +4.13 | 67 | plain | SPAWN |
| 100,948 | x1 | +0.77 | +2.47 | 34 | plain | SPAWN |
| 39,311 | **x2** | +0.77 | +3.90 | 70 | plain | SPAWN |
| 96,385 | **x2** | +2.63 | +4.60 | 66 | plain | SPAWN |
| 171,897 | **x3** | +2.67 | +5.17 | 77 | plain | SPAWN |
| 293,482 | x1 | +2.80 | +4.97 | 40 | plain | SPAWN |
| 94,715 | **x2** | +3.00 | +4.73 | 44 | plain | SPAWN |
| 42,446 | **x4** | +3.23 | +7.57 | 241 | plain | SPAWN |
| 458,794 | x1 | +3.93 | +6.43 | 9 | **★ ★** | SPAWN |
| 300,375 | x1 | +4.83 | +5.67 | 25 | plain | SPAWN |
| 448,397 | **x3** | +5.77 | +8.30 | 91 | **★ ★** | SPAWN |
| 203,230 | x1 | +6.27 | +7.83 | 41 | plain | SPAWN |
| 480,530 | **x2** | +6.27 | +8.10 | 70 | plain | SPAWN |
| 199,111 | **x2** | +6.33 | +7.97 | 56 | plain | SPAWN |

**24 plain · 4 star · 0 skull.** Wave 158 has the **highest body-to-fingerprint ratio in the corpus —
28 bodies over 14 fingerprints (2.00)**, tied with wave 152 (24/12). Both are the most duplicated
cohorts: in 158, nine of the fourteen fingerprints are carried by 2–4 bodies each. (151 = 1.33,
153 = 1.42, 157 = 1.47.)

**Independent reproduction of the third extraction's positive control.** `448,397` and `458,794`,
both at full HP, both one-star-flanked, at t ≈ 803.6–805.2 — the exact pair that note used as its
star-furniture control. Found again here by an independent census path.

### 2.6 Cross-wave fingerprint recurrence: **NONE**

All ~~**69**~~ **68** *(R-L50-1)* fingerprints across the five start cohorts are **unique to their wave**. Not one max-HP
value recurs between waves — including for monsters that are named identically across waves
(*Carnivorous Plant* appears in 151, 152 and 153; *Arcanom the Soulthief* in 151 and 158). This is
consistent with, and is a fifth independent line of evidence for, the third extraction's finding that
**level is drawn per body, not per wave**. Reported as structure; the arithmetic is the conductor's.

> **NOTE 2026-08-08 (R-L50-1) — the claim survives the strike, and gains a control.** The 68 remaining
> fingerprints are still each unique to their wave. **The only value in the whole corpus that recurs
> across waves is `20,005` — which is in all five, and is the excluded player entity.** So
> "no fingerprint recurs across waves" and "the one that does is not a monster" are the same fact
> stated twice, and cross-wave recurrence is itself a non-hostility signal on this footage.
> Cite: `…-kc2-barhue-cohort-correction.md` § 4.2.

---

## 3. SPAWN / SUMMON — the grading, and the gate it rests on

### 3.1 The gate

A summon requires a summoner. The strongest available exclusion is therefore: **was any
boss/nemesis-class (skull-furniture) body present, on any instrument, before this body arrived?**
Measured on two instruments — readout furniture (§ 2) and the minimap skull glyph (§ 6.2):

| wave | first skull-class body on any instrument | consequence |
|---:|:--|:--|
| **151** | **never** (no skull furniture, no skull glyph, whole window) | every body predates any possible boss-summoner ⇒ **all SPAWN** |
| **153** | **never** | **all SPAWN** |
| **158** | **never** | **all SPAWN** |
| 152 | minimap skull at **+3.0 s** (readout at +7.33) | bodies arriving after +3.0 not excluded |
| 157 | minimap skull at **+2.0 s** (readout at +5.00) | bodies arriving after +2.0 not excluded |

For 152 and 157, bodies arriving after the boss appears are graded **SPAWN** where they carry
**star (hero) rank furniture** — Grim Dawn hangs hero furniture on roster entries, and the four
wave-160 summon candidates carried **no** furniture at all (third extraction § 2.1 iii). That is an
inference from the furniture convention, not a measurement, and it is flagged as such in the tables
("SPAWN (furniture)"). Everything else after the boss is **UNDECIDED**.

### 3.2 The wave-160 summon signature is absent everywhere

The third extraction's signature for the wave-160 late body was three-part: **late arrival + no rank
furniture + the *summoner's* level rather than the regular-roster level** (109 against a roster that
read 102–108). Testing part three here — 22 nameplate levels re-read at **×10**,
`evidence/plate-levels-x10.png`:

> **Every level in all five start windows lies in 102–108.** Highest: 108. Lowest: 102.
> **No level-inheritance signature anywhere in the corpus.**

### 3.3 What I deliberately did NOT use: the multiplicity ramp

The obvious discriminator — do pack members appear together (spawn burst) or one at a time (summon
drip)? — was measured and then **rejected as non-probative**, and I am recording that so it is not
re-tried. Measured onsets for `42,798` (w152): x1 @ +0.70, x2 @ +1.50, x3 @ +3.30, x4 @ +3.50. That
looks like a 2.8 s drip. But **the readout only renders once a body is engaged**, so the ramp is a
*rendering* ramp, and "arrived later" is not separable from "was engaged later" on this instrument.
Of 24 multi-body fingerprints, 11 read as BURST and 13 as RAMP, with no correlation to furniture,
family or arrival stream. **The measurement cannot carry a SPAWN/SUMMON verdict and is not used for
one.**

### 3.4 Grading summary

| wave | SPAWN | SUMMON | UNDECIDED | total |
|---:|---:|---:|---:|---:|
| 151 | 12 | 0 | 0 | 12 |
| 152 | 21 | 0 | 3 | 24 |
| 153 | ~~27~~ **26** | 0 | 0 | ~~27~~ **26** *(R-L50-1)* |
| 157 | 14 | 0 | 8 | 22 |
| 158 | 28 | 0 | 0 | 28 |
| **all** | ~~102~~ **101** | **0** | **11** | ~~113~~ **112** *(R-L50-1)* |

---

## 4. TIER FURNITURE — every body, and the control that makes the negatives mean something

Every fingerprint in § 2 was pulled at its **highest observed HP fraction** on a frame where the bar
sits fully on-screen, cropped ±115 px (±210 px on recheck) and rendered at **×4–×8** so both flanks of
the bar are in the tile with the value.

> **⚠ STRIKE-ANNOTATION 2026-08-08 (galadriel, ruling R-L50-3) — CLASS "hero / champion" IS TOO WIDE.**
> **The star-pair binds HERO ONLY.** Seven bound cases with 0 counterexamples (fifth extraction § 7.1):
> orange/hero `584,695` and `275,518` carry ★ ★; yellow/champion `242,124`, `472,732`, `260,786` carry a
> **bare** bar, indistinguishable from common. Confirmed again inside wave 157 by two fresh bindings on
> w157's own plates and bodies: `Diremane Brute` (G/R 0.919 → champion) → **238,068, PLAIN**
> (FRACTION-TRACK, RMS 0.78 px, r² 0.9996) and `Aetherial Stormdrinker` (G/R 0.927 → champion) →
> **304,994, PLAIN** (PROBABLE) — both verified plain on a ±120 px ×5 wide recheck.
> **Consequence: the "88 plain" bucket below is a mix of commons AND champions, and the instrument does
> not see champions at all.** Any inference that read "plain" as "common" needs re-deriving.
> Cite: `…-kc2-barhue-cohort-correction.md` § 3.4, § 3.5.

> **⚠ ANNOTATION 2026-08-08 (galadriel, ruling R-L58-1) — WHAT AXIS THE STAR MEASURES.**
> **The star glyph keys on POOL-level champion mechanics — `championChance` / `nameChampion` on the
> placement pool the body was drawn through — NOT on the body record's own `monsterClassification`.**
> legolas's PLAIN column, in the w152/w157 generator join and elsewhere, is *record taxonomy*: what the
> `.dbr` says the monster IS. This note's PLAIN/★ column is *render taxonomy*: what the placement
> mechanism made the game DRAW. **Two axes, both valid, answering different questions**, and they are
> free to disagree — a trash-pool record at `championChance = 0` enters a regular roster and renders
> starless no matter how its own record is classified, while a record drawn through a champion-chance
> pool renders starred. Neither column is a correction of the other, and neither should be substituted
> for the other in a derivation. **Practical consequence for the reader of § 2's tables:** a PLAIN row
> is not a claim about the record's class; it is a claim about the pool. The R-L50-3 strike above
> narrowed *which ranks* the star resolves; this annotation names *which axis* it resolves at all.
> Cite: ledger L-58 ruling R-L58-1; the T-1 falsification table is UNAFFECTED (it widens add capacity,
> it does not move a count). No record line below is rewritten.
>
> *Applied in anger this touch:* the w152 `Ugdenbog Crabling` read
> (`…-kc2-crabling-rotmouth-touch.md` § 1) uses PLAIN-vs-★ as an **independent second axis** to exclude
> `443,554` and `453,883` from a plate binding that the fraction axis alone could not separate. That
> is what having two axes is worth, and it only works while they are kept distinct.
>
> *And a measured corroboration, on camera, from the same touch (§ 5 of that note).* Wave 152's plate
> roster inside this note's own census window resolves, by glyph-core colour, to **five distinct
> orange→HERO names** — `Mudflinger ~ Reflective` · `Chaosshell ~ Voidtouched` · `Aregos ~ Corrupted` ·
> `Chillslither ~ Arctic` · `Rotmouth` (G/R 0.691–0.714, all inside the measured hero band) — against
> the **two** ★ fingerprints this section records for w152 (`443,554` ×4, `453,883` ×2). Five hero
> names cannot live in two fingerprints. **So the star is SUFFICIENT for hero, not NECESSARY for it**
> — R-L50-3 bound the implication one way (everything starred is a hero, 7/7, 0 counterexamples) and
> it must not be read in the other. Under R-L58-1 this is the expected shape rather than an anomaly: a
> hero drawn through a placement whose pool carries `championChance = 0` renders starless. **Do not
> use a PLAIN row to argue a body is not a hero.**

| class | glyph | bodies (of ~~113~~ **112**, R-L50-1) |
|:--|:--|---:|
| plain *(**commons AND champions** — R-L50-3; **pool-axis, not record-axis** — R-L58-1)* | nothing at either end of the bar | **88** |
| ~~hero / champion~~ **hero ONLY (R-L50-3)** | **one gold five-point star at each end** | **23** |
| boss | **bone/pale double skull** | **2** |
| nemesis | red double skull | **0** |

**The instrument's positives and negatives are both controlled.**
*Positive:* `448,397` at wave 158 renders two unmistakable gold stars at this exact crop geometry
(`evidence/furniture-w158-p3.png`, tile 2). *Negative:* the same geometry over `225,874`, `230,020`,
`373,665`, `278,543` at ×4 with ±210 px returns bare bar on every one
(`evidence/furniture-recheck-wide-p1.png`).

**Boss vs nemesis is measured, not eyeballed.** The two skull-flanked bodies were colour-sampled over
the flank glyphs: `2,050,807` reads mean RGB (153,135,118), **R−B = +35**; `2,069,299` reads
(194,187,182), **R−B = +12**. Both are near-achromatic **bone**, matching the board-closure boss class
(Galakros) and not the red nemesis class (Kubacabra/Aleksander/Zantarin). Both bind to **violet**
nameplates (§ 5), which is Grim Dawn's boss colour. Two instruments, same verdict.
`evidence/boss-skull-colour-x8.png`.

**Correction carried forward:** board-closure § 1.1's "gold chevron (hero)" furniture class does not
appear anywhere in this corpus. The third extraction already withdrew that read (§ 6.1); this pass
finds nothing to reinstate it. The observed vocabulary is exactly three: plain, star-pair, skull-pair.

---

## 5. NAMES AND LEVELS — 22 plates read on camera

84 nameplate-bearing frames were located across the five start windows (5 Hz scan); 58 were rendered
at ×2 for name+family and 22 re-read at ×10 for the level numeral.
`evidence/plates-w151-p1.png` … `plates-w158-p2.png` · `evidence/plate-levels-x10.png`

> **⚠ STRIKE-ANNOTATION 2026-08-08 (galadriel, ruling R-L50-2) — RANK IS THE GLYPH COLOUR, NOT THE NAME SHAPE.**
> Rank in the table below was read partly off the **`~ Affix` name pattern**. That pattern is **not a
> rank signal.** Measured on the name's own glyph core (brightest quartile, max-channel > 170, rows
> 16–36), the bands are clean and non-overlapping: **white/common G/R 0.98–1.00 · yellow/champion
> 0.91–0.95 · orange/hero 0.71–0.79 · violet/boss B/R ≈ 1.04.**
> **`Wendigo ~ Ancient` (w153, +3.80) measures G/R = 0.92 — YELLOW → CHAMPION, not orange → hero.**
> Its row below is struck. **Every other `~ Affix` row in this table is SUSPECT wherever the affix
> pattern drove the read**, and none of them has been re-measured; two `~ Affix` names *were*
> re-measured elsewhere and came back orange (`Starhorn ~ Celestial` 0.713, `Arum'Zoth ~ Burning`
> 0.643), so the pattern is neither reliable nor uniformly wrong — it is simply **not the instrument**.
> Also recorded: the 5 Hz scan that produced this table **missed 5 of 11 wave-153 hovers and 9 of 13
> wave-157 hovers**; a 30 Hz re-scan finds them.
> Cite: fifth extraction § 3.1 / § 9.2 · `…-kc2-barhue-cohort-correction.md` § 3.3.

| wave | t (+off) | name | rank (name colour) | level | family |
|---:|:--|:--|:--|---:|:--|
| 151 | 686.1 (+4.00) | Spiteful Wraith | yellow → champion | **106** | Undead |
| 151 | 686.5 (+4.40) | Ancient Wraith | yellow → champion | **104** | Undead |
| 151 | 687.7 (+5.60) | **Tildoom ~ Timewarped** | orange → hero | **108** | Undead |
| 151 | 689.3 (+7.20) | **Arcanom the Soulthief** | orange → hero | **108** | Undead |
| 151 | 690.9 (+8.80) | Wraith | white → common | **104** | Undead |
| 152 | 698.78 (+0.40) | Carnivorous Plant | white → common | **108** | Plant · Eldritch |
| 152 | 701.38 (+3.00) | **Mudflinger ~ Reflective** | orange → hero | — | Beast |
| 152 | 701.78 (+3.40) | Ugdenbog Crabling | white → common | **108** | Beast |
| 152 | 702.18 (+3.80) | **Chaosshell ~ Voidtouched** | orange → hero | — | Beast |
| 152 | 703.38 (+5.00) | **Chillslither ~ Arctic** | orange → hero | — | Beast |
| 152 | 705.78 (+7.40) | Stonegaze Basilisk | white → common | **106** | Beast |
| 152 | 706.78 (+8.40) | **Fleshweaver Haraxis** | **violet → BOSS** | **108** | Aetherial |
| 152 | 707.18 (+8.80) | Juvenile Basilisk | white → common | **102** | Beast |
| 153 | 718.63 (+3.80) | **Wendigo ~ Ancient** | ~~orange → hero~~ **STRUCK R-L50-2 → yellow → CHAMPION (G/R 0.92)** | **106** | Undead · Beast |
| 153 | 719.03 (+4.20) | Wendigo | white → common | **104** | Undead · Beast |
| 153 | 721.63 (+6.80) | Storm Revenant | yellow → champion | **106** | Undead |
| 153 | 722.23 (+7.40) | Frost Revenant | yellow → champion | — | Undead |
| 153 | 722.43 (+7.60) | Ugdenbog Golem | yellow → champion | **105** | Plant · Eldritch |
| 153 | 722.83 (+8.00) | Carnivorous Plant | white → common | — | Plant · Eldritch |
| 157 | 783.1 (+2.80) | Diremane Brute | yellow → champion | **103** | Beast |
| 157 | 787.1 (+6.80) | **Starhorn ~ Celestial** | orange → hero | **107** | Beast |
| 157 | 787.9 (+7.60) | **Blugrug the Living Plague** | **violet → BOSS** | **108** | Aether Corruption |
| 157 | 789.1 (+8.80) | Chthonian Bloodkeeper | yellow → champion | **106** | Chthonic · Insectoid |
| 158 | 801.23 (+1.80) | Chthonian Devourer | yellow → champion | **105** | Chthonic |
| 158 | 803.23 (+3.80) | Ugdenbog Spikeshell | white → common | **103** | Beast |
| 158 | 803.63 (+4.20) | Ugdenbog Crab | white → common | — | Beast |
| 158 | 805.23 (+5.80) | **Culldar Endbringer ~ Celestial** | orange → hero | — | Undead |
| 158 | 805.63 (+6.20) | **Arcanom the Soulthief** | orange → hero | **108** | Undead |
| 158 | 806.03 (+6.60) | **Sandclaw ~ Matriarch** | orange → hero | **106** | Beast |
| 158 | 807.23 (+7.80) | Sandclaw | white → common | — | Beast |

### 5.1 Three things the plates show

1. **Wave 151's start cohort is a single family — Undead, 5/5 plates.** The third extraction read
   wave 151 as *Plant · Eldritch* (Carnivorous Plant ×2, Ferrosius ~ Swift). Both are right: those
   plates are at t = 692.2 / 694.8 / 695.6, i.e. **+10.1 / +12.7 / +13.5 s — the *second* stream.**
   Wave 151 is a **two-family wave**: an Undead start cohort, then a Plant·Eldritch group after the
   4.5 s silence. Waves 153 and 158 are likewise mixed (153: Undead·Beast → Plant·Eldritch at +7.6;
   158: Chthonic → Beast → Undead).

2. **Both bosses are named on camera, and both bind to a skull-flanked 2.0 M-class fingerprint.**
   *Fleshweaver Haraxis* (w152, plate +8.40) with `2,050,807` (skulls, arr +7.33); *Blugrug the
   Living Plague* (w157, plate +7.60) with `2,069,299` (skulls, arr +5.00). The binding is
   **STRONG, not MEASURED** — it rests on rank-class agreement and temporal adjacency, and per my own
   § 8.3 correction the plate reports whatever the cursor is over, not necessarily the nearest bar.

3. ~~**The level-numeral colour rule is refined.** The third extraction stated *"every yellow numeral
   is ≤ 104 and every red numeral is ≥ 106"* — its corpus contained no 105. This pass reads **105
   twice** (Ugdenbog Golem w153; Chthonian Devourer w158) and **both render RED**. The boundary sits
   between 104 and 105, which for a level-100 player is exactly **yellow ≤ player+4, red ≥ player+5**.
   That is a tighter and more mechanical statement of the same rule, and it holds 22/22 here.~~

   > **⚠ STRIKE-ANNOTATION 2026-08-08 (galadriel, ruling R-L50-4) — ITEM 3 IS WRONG AND IS REVERTED.**
   > This item is **struck in full.** Both 105s cited above are **AMBER, not red.** Re-measured on the
   > numeral's own glyph core (mean RGB over pixels with R > 140 and R−B > 60), fifth extraction § 9.4,
   > `evidence/plate-levels-x10.png` · `evidence/level-105-vs-106-control-x10.png`:
   > **103 → G/R 0.79, 0.88 · 104 → 0.59–0.69 (×6) · 105 → 0.62, 0.68, 0.71 · 106 → 0.34, 0.36, 0.40 ·
   > 107 → 0.39 · 108 → 0.32, 0.34 (×3).** `Ugdenbog Golem` w153 t = 722.43 reads **0.62** and
   > `Chthonian Devourer` w158 t = 801.23 reads **0.68**; the second is shown beside a 106 at ×10 in
   > the control image and the gap is not marginal.
   > **The boundary sits between 105 and 106: AMBER ≤ 105, RED ≥ 106 — for a level-100 player,
   > amber ≤ player+5, red ≥ player+6.** The third extraction's original rule ("yellow ≤ 104,
   > red ≥ 106") was **correct**; it simply had no 105 in its corpus. **This pass's "correction" of it
   > was the error, and the original stands.**
   > Cite: fifth extraction § 9.4 · `…-kc2-barhue-cohort-correction.md` § 5.

---

## 6. CLOSURE — engaged, not arena. Stated per wave, with the size of the gap.

### 6.1 The gap is large in these waves

Readout-census body count vs my eye-read minimap monster-icon count at matched offsets
(`evidence/minimap-w151-x5.png` … `minimap-w158-x5.png`, ×5, nine offsets per wave):

| offset | w151 rd / mm | w152 rd / mm | w153 rd / mm | w157 rd / mm | w158 rd / mm |
|:--|:--|:--|:--|:--|:--|
| +0.5 | 5 / ≈7 | **1 / ≈10** | **1 / ≈5** | **0 / ≈5** | **3 / ≈11** |
| +1.0 | 5 / ≈7 | **2 / ≈10** | 3 / ≈4 | **0 / ≈5** | **0 / ≈11** |
| +2.0 | 7 / ≈6 | 4 / ≈11 | 7 / ≈6 | 5 / ≈8 | **5 / ≈12** |
| +2.5 | 4 / ≈5 | **8 / ≈13** | 6 / ≈6 | 5 / ≈9 | **4 / ≈13** |
| +3.0 | 4 / ≈4 | 9 / ≈14 | 6 / ≈6 | 5 / ≈10 | 8 / ≈14 |
| +4.0 | 6 / ≈9 | 8 / ≈12 | 10 / ≈11 | **3 / ≈10** | 8 / ≈13 |
| +5.0 | 6 / ≈8 | 8 / ≈11 | 12 / ≈12 | 9 / ≈11 | **6 / ≈14** |
| +6.0 | **3 / ≈11** | 7 / ≈10 | **9 / ≈14** | 11 / ≈9 | 9 / ≈13 |
| +8.0 | **2 / ≈13** | 9 / ≈12 | **6 / ≈10** | 10 / ≈9 | **4 / ≈12** |

**Every one of the five censuses is CLOSED-FOR-ENGAGED and NOT CLOSED-FOR-ARENA.** The worst cases
are unambiguous: wave 158 at +1.0 s has **zero** readouts against ≈11 minimap icons; wave 152 at
+0.5 s has one against ≈10. In the first ~2 s of these waves the player has simply not engaged the
cohort yet, and the readout instrument is blind to it.

This is a **different closure posture from wave 160**, where the player was engaged with essentially
the whole board and the readout census was a near-complete arena census. It should not be carried
across. The minimap counts are approximate — icons overlap into clusters at ×5 and I will not claim
them to ±1 — but they are uniformly **≥** the readout count, which is the load-bearing direction.

### 6.2 The boss that sat on the map for three seconds before it existed to the readout

The cleanest single demonstration. `evidence/minimap-skull-zoom-x9.png` (×9) shows a pale skull glyph
on the wave-157 disc at **+2.0, +3.0 and +5.00 s**, moving. The `2,069,299` readout does not render
until **+5.00 s**. `evidence/minimap-w152-fulldisc-x6.png` shows the same for wave 152: skull at the
southern rim at **+3.0 s**, readout at **+7.33 s**.

**A boss is in the arena 3.0–4.3 s before the readout instrument can see it.** Anything computed from
readout arrival times as if they were *spawn* times will be late by that much, at least for bodies the
player has not yet reached.

---

## 7. METHOD, AUDITS, AND WHAT WAS REJECTED

| stage | tool | note |
|:--|:--|:--|
| footage | local copy | `/Volumes/reincarnated` delivers ≈850 KB/s under contention; the third extraction abandoned a scan on that cost. **Copied to `/tmp` first** (byte-exact: 479,438,089 B, duration 1034.100 s). Five 30 Hz censuses then ran in parallel in ~6 min. |
| census | **`pipeline/eor_cohort.py census`** (new) | fuses locate+OCR into **one** streaming decode pass (the third-extraction chain used two); adds viewport-edge handling and per-frame simultaneity |
| readout location | `eor_hptext.blobs` logic, re-parameterised | achromatic gate `min(R,G,B) > 135`; width floor lowered 55 → 30 px so edge-clipped fragments survive; **same-row merge** (vertical overlap ≥ 50 %, x-gap ≤ 22 px) repairs strings split by a dim glyph |
| OCR | `eor_hpocr` atlas, **unchanged**, built on wave-160 glyphs | transfer validated before use — see § 7.1 |
| body resolution | `eor_cohort._cluster_frame` | one body renders one readout per frame, so same-row boxes within 40 px are one body; **clusters carrying two different fully-parsed maxes are split back out** (measured at 9/6,246 clusters = 0.14 %, but it understates a peak) |
| eye-read sheets | **`pipeline/eor_grid.py`** (new) | paginated **grid** sheets. `eor_cropsheet` stacks vertically; across five waves that produced sheets ~8,000 px tall which downsample to illegibility — the exact failure the sheet exists to prevent |
| plates | `eor_plate_scan` / `eor_plate_read` | unchanged |
| minimap | `eor_minimap` | **detector counts NOT used**; its `kind` classifier disagreed with my eye on wave 151 (returned "pale" for glyphs that are plainly gold stars at ×5). All § 6 counts are eye-reads. |

**Totals:** 2,472 frames decoded at 30 Hz across the five windows; **28,466 readouts located**;
**8,257 parsed**; 69 fingerprints eye-verified.

### 7.1 Atlas transfer — validated against third-extraction ground truth

The glyph atlas was built on **wave-160** frames. Before any wave-151 number was trusted, it was run
over t = 692.0–692.5, where the third extraction § 4.1 hand-enumerated the values by eye. **All five
recovered: 221,351 · 442,747 · 278,543 · 272,948 · 582,590.** It also returned **569,330**, which that
two-frame hand pass did not have — consistent with it being a sample, not a census.

### 7.2 Parse-failure audit — no failure hides a new fingerprint

Every unparsed string of length ≥ 8 in the probe window was inspected as raw glyphs: 18 distinct
strings, **all 18 near-misses of an already-listed value** (`136,975)`, `(442,747,`,
`(37,3,665/373,665)`, `9139,400)` …). Same result as the board-closure audit.

### 7.3 OCR-noise disproof — 8 candidates eye-read, 7 killed, 1 promoted

Every value the edit-distance-1 audit could **not** explain was pulled to a ×6 crop of its own
exact-seek frame. `evidence/unexplained-weak-values-x6.png`:

| value | eye-read says | verdict |
|---:|:--|:--|
| 462,767 | `(442,747/442,747)` | corruption |
| 13,937,400 | `(108,744/139,400)` | corruption |
| 4,547,883 | `(453,883/453,883)` | corruption |
| 687 | `962/271,687)` | left-clipped fragment |
| 5,046,193 · 5,046,103 | `(123,785/504,193)` · `(72,249/504,193)` | corruption |
| 599,575 | `(300,375/300,375)` | corruption |
| **211,686** | **`(211,686/211,686)`, twice, at full HP** | **REAL — promoted** |

### 7.4 The eye caught one the machine had cleared

All 69 fingerprint tiles were eye-read against their OCR label. **68 agreed. One did not:** wave
158's `39,811` (n = 8, i.e. *above* the noise floor and never flagged by the edit-distance audit)
eye-reads as **`(39,311/39,311)`** — `evidence/furniture-w158-p1.png`, tile 1. It is folded into
`39,311`, whose arrival consequently moves from +0.77 to +0.40 s.

**This is the discipline earning its keep.** A machine-only census would have carried a phantom
fingerprint and an extra body into wave 158's count.

### 7.5 A new census hazard, recorded: VIEWPORT-EDGE CLIPPING

Not present at wave 160, unmissable here. At wave 151 **+0.10 s, four monster readouts are cut by the
left screen edge simultaneously** — `evidence/viewport-edge-clipping-hazard.png`. The asymmetry
matters and is exploited:

* **Left-clipping eats the numerator and leaves the denominator whole** (`…874/225,874)`) — the
  fingerprint survives and is recovered (`parse_ext` kind `lclip`, 524 readouts across the corpus).
* **Right-clipping eats the denominator** (`(453,064`) — the **body is present but its fingerprint is
  unavailable** (kind `rclip`, 1,464 readouts). These are counted as bodies with an unknown max, never
  as absences.

The same treatment is given to eye-confirmed OCR corruptions: the readout still counts as a **body**,
with its fingerprint nulled. Dropping them outright would have biased every peak downward — it cost
wave 158 a body when I tried it.

### 7.6 Rejected / limits

* **Multiplicity ramp as a summon discriminator — measured, REJECTED** (§ 3.3). Confounded by
  engagement; recorded so it is not re-tried.
* **`eor_minimap` kind-classifier — REJECTED for census use** (misclassifies gold stars as pale).
  Remains useful only as a "where to look" pass.
* **`eor_starbar.py` — remains rejected**, per third extraction § 5. All furniture here is eye-read.
* **Minimap counts are approximate.** Icons overlap into clusters; I report "≈" and use them only for
  the one-directional claim in § 6.
* **Boss name→fingerprint bindings are STRONG, not MEASURED** (§ 5.1 item 2).
* The census sees a monster only while its readout renders — engaged and on-screen. **Closed for
  engaged, not for the arena, in all five waves** (§ 6).
* Tesseract / OpenCV remain absent on this host. **No automatic OCR was trusted for any reported
  value.**

---

## 8. CORRECTIONS TO MY OWN RECORD

**8.1 — third extraction § 3.3's minimap control table is too confident on glyph class at ×5.**
That table reports wave 153 as "~5 stars + 1 skull" at +2.5 s and wave 151 as "~5–6 stars" at +1.0 s.
Re-read at ×5 and ×9 across nine offsets per wave, **I find no skull glyph anywhere in waves 151, 153
or 158**, and I find skulls in 152 (+3.0) and 157 (+2.0) which that table does not list. The star/skull
*split* in that table should be treated as indicative; the counts stand. My § 6.2 crops are the better
instrument and this note's classifications supersede.

**8.2 — third extraction § 1.2's wave-151 plate reads are correct but are not the start cohort.**
Carnivorous Plant (103, 107) and Ferrosius ~ Swift (108) are read at +10.1 / +12.7 / +13.5 s, which is
the *second* stream. Wave 151's start cohort is **Undead, 5/5 plates** (§ 5.1). Anything that used
those three rows as "what wave 151 spawns with" needs the substitution.

**8.3 — ~~third extraction § 1.3(a)'s level-colour rule needs one word changed.~~ "red ≥ 106" ~~should
read "red ≥ 105"; two 105s render red here (§ 5.1 item 3). The rule's *substance* is unaffected and
is in fact strengthened — it becomes exactly player+4 / player+5.~~**

> **⚠ STRIKE-ANNOTATION 2026-08-08 (galadriel, ruling R-L50-4) — THIS CORRECTION IS WITHDRAWN IN FULL.**
> **The third extraction § 1.3(a) needed no change.** Its "red ≥ 106" was right. Both 105s cited here
> measure **AMBER** (G/R 0.62 and 0.68 against a red band of 0.32–0.40) — fifth extraction § 9.4.
> **Operative rule, restored: amber ≤ 105, red ≥ 106 — for a level-100 player, amber ≤ player+5,
> red ≥ player+6.** Anything downstream that adopted "red ≥ 105" or "player+4 / player+5" from this
> item is running on a withdrawn correction and needs the substitution.
> Cite: fifth extraction § 9.4 · `…-kc2-barhue-cohort-correction.md` § 5.

---

## 9. Mirror voice

Wave one-sixty had four bodies on it and the whole team learned to read that board. These waves have
fourteen. They arrive in two breaths — a handful at the badge, then a silence of two to four seconds
long enough to think the wave is small, then the rest of it — and they arrive wearing almost nothing:
eighty-eight bare health bars, twenty-three with a single gold star at either end, and two, in five
whole waves, with the bone skulls that mean something has actually come. The Mirror counted them and
then had to say the harder thing, which is that the counting instrument is half blind. At one second
into wave one-fifty-eight the numbers over the monsters say nothing at all, and the little disc in the
corner says eleven. They were all there. The man simply had not looked at them yet, and a health bar
in this game is not a thing that exists until someone is fighting it.
