# KC2-SIM — third extraction pass: nameplate levels off 160, the 5th body's tier, and the F-9 boss-wave cohort

**Date:** 2026-08-08
**Author:** galadriel (visual perception + benchmark seam)
**Status:** WORKING — evidentiary note, Phase C of the KC2-SIM autonomous run (conductor: gandalf)
**Commit state:** UNCOMMITTED by instruction. Rides the conductor's gate-close unit.
**Extends:** `galadriel/notes/2026-08-07-eor-sittings-extraction.md` · `…/2026-08-08-eor-followup-extraction.md` · `…/2026-08-08-kc2-board-closure.md`
**Footage (read-only, no new sessions):**
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-1/video/eor-warlord-2026-08-04 21-09-31.mp4` (s1, 1920×1080, 60 fps, 2498.367 s)
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (s2, 1920×1080, 60 fps, 1034.100 s)
**Evidence root:** `agentic_orchestration/galadriel/captures/2026-08-08-kc2-third-extraction/evidence/` (untracked)
**New pipeline:** `galadriel/pipeline/eor_plate_scan.py`, `eor_plate_read.py`, `eor_plate_fill.py`, `eor_starbar.py`

---

## 0. Headline

All three tasks returned **MEASURED**. Nothing was forced.

| task | verdict |
|:--|:--|
| **(1) nameplate levels well away from 160** | **MEASURED — 30 plate reads across 15 badge-verified waves, waves 20 → 160, two arenas.** Level does **not** track wave index. It tracks **rank**. A wave-20 common reads **102**; a wave-90 nemesis reads **109** — the *same* value the wave-160 nemeses read. |
| **(2) wave-160 initial-window 5th body** | **MEASURED on tier, STRONG on identity.** The first non-boss body enters at **wave-start +5.00 s**, carries **no rank furniture at all** (not the one-star hero furniture, which the same instrument resolves cleanly one wave earlier), and reads **level 109 — the nemeses' level, not the regular-roster level**. Named on camera: **"Aleksander's Shard"**. **Zero** readouts in the 450,012–460,431 hero band across 5,146 located readouts. |
| **(3) F-9 boss-only-wave cohort** | **MEASURED for wave 160 — cohort is boss-pool-only.** 4 skull-class icons, **zero** star-class icons, through +4.75 s. Same-arena control: waves 151–159 all carry star-class icons at the same offsets. **Wave 150 is ABSENT from the footage** and is stated as such. |

---

## 1. TASK 1 — MONSTER NAMEPLATE LEVELS AT NON-160 WAVES

### 1.0 What the instrument reads, and how wave identity was pinned

Grim Dawn renders a **hovered-monster nameplate** at top-centre: name (rows 17–34), a
**red/gold monster-LEVEL numeral** (rows 43–58, centred on screen-centre x = 960), the plate's
health-bar track (rows 57–67), and a monster-family label (rows 91–103). Geometry measured on the
known-good plate at s2 t = 854.30 ("Galakros, the Mountain") and re-validated against the
board-closure plate windows before use (41 candidates recovered over the wave-160 window at 5 Hz,
including every plate that note reported).

**Every level below is a galadriel eye-read of a ×10 magnified exact-seek crop.** The CV layer
(`eor_plate_scan.py`) only said *where to look*.

**Wave identity is measured, not carried over from the Phase-A table.** The wave badge
(`x 1578..1632, y 126..170`) was read at ×9/×6 at **every single timestamp** reported below.
**24 / 24 agree** with the wave attributed from the Phase-A timeline.
Evidence: `evidence/s1-wave-badge-verify.png` (8/8) · `evidence/s2-wave-badge-verify.png` (16/16).

### 1.1 The readings — sitting 1 (green cave arena, waves 20 → 90)

`evidence/s1-plates-w20-w40-w80-C-name.png` + `-C-lvl.png` ·
`evidence/s1-plates-w50-A-name.png` + `-A-lvl.png` ·
`evidence/s1-plates-w50-w90-B-name.png` + `-B-lvl.png`

| wave (badge-verified) | video t | body named on plate | name colour → rank | **level** | family |
|---:|---:|:--|:--|---:|:--|
| **20** | 1041.1 | Cronley's Gang ~ Gunman | white → common | **102** | Human |
| **20** | 1045.1 | Cronley's Gang ~ Gunman | white → common | **103** | Human |
| **40** | 1326.4 | Burning Dead | yellow → champion | **104** | Aether Corruption |
| **50** | 1461.4 | Wretcher | white → common | **103** | Aether Corruption |
| **50** | 1462.9 | Cold One | yellow → champion | **103** | Aether Corruption |
| **50** | 1465.9 | Chillmane Icesplitter | yellow → champion | **104** | Beast |
| **80** | 1926.0 | Dermapteran Reaver | yellow → champion | **104** | Insectoid |
| **80** | 1938.0 | Darius Cronley | violet → boss | **106** | Human · Aetherial |
| **90** | 2127.7 | **Benn'Jahr, the Colossal** | **orange → nemesis** | **109** | Chthonic |

Wave 10 was scanned in full (57 frames at 2 Hz across its whole 28.4 s) and produced **no plate** —
the cursor never crossed a monster. Recorded as ABSENT-IN-FOOTAGE for that wave, not as a null level.

### 1.2 The readings — sitting 2 (Crucible of the Dead, waves 151 → 159)

`evidence/s2-plates-w151-w154-A-*.png` · `-w152-w155-B-*.png` · `-w155-w158-C-*.png` · `-w159-D-*.png`

| wave | video t | body named on plate | rank | **level** | family |
|---:|---:|:--|:--|---:|:--|
| 151 | 692.2 | Carnivorous Plant | common | **103** | Plant · Eldritch |
| 151 | 694.8 | Carnivorous Plant | common | **107** | Plant · Eldritch |
| 151 | 695.6 | **Ferrosius ~ Swift** | **orange → hero** | **108** | Plant · Eldritch |
| 152 | 699.0 | Carnivorous Plant | common | **108** | Plant · Eldritch |
| 152 | 707.2 | Juvenile Basilisk | common | **102** | Beast |
| 152 | 708.8 | Fleshweaver Haraxis | boss | **108** | Aetherial |
| 153 | 722.6 | Carnivorous Plant | common | **103** | Plant · Eldritch |
| 154 | 732.4 | Gabal'Thunn, the Visage of Madness | boss | **108** | Chthonic |
| 155 | 751.8 | Dralgar, the Keeper of Burrwitch | boss | **108** | Aether Corruption |
| 155 | 758.8 | Allostria, the Mindthief | boss | **108** | Aetherial · Human |
| 156 | 765.0 | Allostria, the Mindthief | boss | **108** | Aetherial |
| 156 | 776.0 | Janaxia, the Betrayer | boss | **107** | Human |
| 157 | 787.8 | Blugrug the Living Plague | boss | **108** | Aether Corruption |
| 158 | 803.6 | Ugdenbog Crab | common | **104** | Beast |
| 159 | 817.0 | Margul the Rotting | boss | **107** | Insectoid |
| 159 | 820.6 | Lunal'Valgoth, Steward of Darkness | boss | **107** | Chthonic · Insectoid |
| 159 | 833.6 | Venarius, the Backbreaker | boss | **106** | Aether Corruption |

Wave-160 rows are carried from the board-closure note unchanged (Galakros **106** · Kubacabra /
Archmage Aleksander / Zantarin **109** · Aetherial Bileeater **112** · Aleksander's Shard **109** ·
Skeletal Archer **109** · Death Revenant **109**).

### 1.3 Two internal validations of the level reads

**(a) Numeral colour is a function of the VALUE, and it is self-consistent 20/20.**
The level numeral renders **yellow/gold** or **red**. Across every read in §1.1–§1.2:
every yellow numeral is **≤ 104** and every red numeral is **≥ 106**. No exception, two sittings,
two arenas, fifteen waves. That is Grim Dawn's monster-level-vs-player-level colour code
(the fixture's player is level 100) and it is an independent check on the digits: a misread of
"103" as "108" would have shown the wrong colour. It did not, anywhere.

**(b) Name colour is measured, not eyeballed.** The name-band glyph colour was measured numerically
(brightest 40 % of glyph pixels) on every plate. Four separated classes, no overlap:

| class | measured mean RGB | R−B | bodies |
|:--|:--|---:|:--|
| **white → common** | ≈ (250, 250, 245) | +1…+8 | Carnivorous Plant, Juvenile Basilisk, Ugdenbog Crab, Cronley's Gang ~ Gunman, Wretcher, Skeletal Archer |
| **yellow → champion** | ≈ (245, 215, 110) | +126…+145 | Cold One, Chillmane Icesplitter, Burning Dead, Dermapteran Reaver, Aleksander's Shard, Aetherial Bileeater, Death Revenant |
| **orange → hero / nemesis** | ≈ (196, 73, 68) | +124…+132 | Ferrosius ~ Swift, Benn'Jahr, Kubacabra, Archmage Aleksander, Zantarin |
| **violet → boss** | ≈ (174, 150, 181) | −11…+5 (G−B ≈ −30) | Galakros, Darius Cronley, Fleshweaver Haraxis, Gabal'Thunn, Dralgar, Allostria, Janaxia, Blugrug, Margul, Lunal'Valgoth, Venarius |

### 1.4 What the readings say — reported as structure, not as a model

Three facts fall straight out. The conductor runs the math; these are the pixels.

1. **Level does not track wave index.** Wave 20 → 102/103. Wave 50 → 103/103/104.
   Wave 80 → 104/106. Wave 90 → **109**. Wave 158 → 104. Wave 160 → 106/109/112.
   A wave-20 common and a wave-158 common differ by **2 levels** across **138 waves**.

2. **Level tracks RANK, tightly, and the nemesis value is invariant.**
   * **nemesis: 109 — 4 / 4**, at wave **90** (s1, green cave) and wave **160** (s2, Crucible of the
     Dead). Two arenas, two sittings, 70 waves apart, **identical**.
   * **boss: 106 – 108** (n = 11), waves 80 → 160.
   * **champion: 103 – 104** at s1 waves 40–80 (n = 4); **109 – 112** at s2 wave 160 (n = 3).
   * **common: 102 – 108** (n = 9), waves 20 → 160.

3. **Within one wave and one monster TYPE, level varies by up to 5.** Wave 151 carries
   Carnivorous Plants at **103** *and* **107**; wave 152 carries one at **108** and a Juvenile
   Basilisk at **102**. This is a direct camera read of a per-body level draw, not a per-wave
   constant.

   **The 107/108 commons were audited, because they are the outliers.** Both were re-pulled at ×4
   on **consecutive frames** (694.8 + 695.0; 698.8 + 699.0): the name is crisp white "Carnivorous
   Plant", not ghosted or mid-crossfade, and the level numeral holds its value across the pair.
   `evidence/s2-w151-w152-carnivorous-plant-107-108-x4.png`. A plate-swap artefact was the obvious
   alternative and it is excluded — an adjacent frame at 695.6 *does* show a swap (to
   "Ferrosius ~ Swift", orange, 108) and it looks nothing like the audited frames.
   `evidence/s2-w151-w152-plate-stability-name.png`.

**Discriminating power, stated plainly and without doing the conductor's arithmetic:** the two
readings of the level rule diverge away from 160. The camera says the **nemesis** level is
**109 at wave 90 and 109 at wave 160**, and that **no rank's level rises measurably between wave 20
and wave 160**. Any reading whose evaluation point moves with the wave has to reproduce a flat
line across 140 waves.

---

## 2. TASK 2 — THE INITIAL-WINDOW 5TH BODY

### 2.1 What the 5th body is, on four independent instruments

**Answer: the first non-boss body of wave 160 enters at wave-start +5.00 s, carries NO rank
furniture, reads level 109, and is named "Aleksander's Shard" on camera.**
Tier: **MEASURED**. Identity binding of the specific minimap icon: **STRONG**, not MEASURED.

**(i) Onset — MEASURED to ±0.13 s.** The minimap carries no star-class (non-boss) icon at
t = 843.62; a gold five-point star is present at t = 843.87 and persists.
Read at **×13**: `evidence/s2-w160-star-onset-x13.png` (843.62 / 843.87 / 844.37) ·
context at ×7 `evidence/s2-w160-star-onset-x7.png`. Wave 160 starts at 838.87 ⇒ **onset = +5.00 s**.

**(ii) Co-timing — 0.07 s.** The first `103,912` readout in the board-closure census is at
**t = 843.80**. The star's first frame is **843.87**. One 10 Hz sample apart. No other fingerprint
onset is within 4 s of the star (484,095 first renders at 848.30, i.e. +4.4 s later).

**(iii) Rank furniture — MEASURED, with a positive control one wave earlier.**
Grim Dawn flanks an in-world monster health bar with rank furniture. All four wave-160 low-rank
fingerprints were re-pulled at **×5 / ×6** on multiple frames each, at high bar fill:

| fingerprint | probable body | frames read | flanking furniture |
|---:|:--|---:|:--|
| **484,095** | Aetherial Bileeater | 2 | **none** |
| **468,504** | Death Revenant | 2 | **none** |
| **103,912** | Aleksander's Shard | 3 | **none** |
| **41,237** | Skeletal Archer | 3 | **none** |
| 2,295,755 | Galakros | 1 | bone/pale double skull |
| 2,955,796 | Kubacabra | 1 | red double skull |
| 3,722,896 | Aleksander / Zantarin | 1 | red double skull |

`evidence/s2-w160-lowrank-furniture-multi-x5.png` (10 tiles) ·
`evidence/s2-w160-furniture-lowrank-x6.png` · `evidence/s2-w160-rank-furniture-wide.png`.
One of the 41,237 tiles happens to catch a 3,722,896 bar in the same crop, **red skulls and all** —
an in-frame positive control that furniture renders at that magnification.

**The one-star control:** at **wave 158, t = 803.6**, two bodies with max HP **448,397** and
**458,794** each carry **one gold five-point star at each end of the bar**, unmistakable at ×6.
`evidence/s2-w158-star-furniture-x6.png`. Same fixture, same sitting, same instrument, two waves
earlier. **The instrument resolves one-star furniture cleanly. Wave 160 has none of it.**

**(iv) Level — the summon signature.** Every low-rank body at wave 160 reads **109** —
Aleksander's Shard 109, Death Revenant 109, Skeletal Archer 109 — which is **exactly the nemeses'
level** (Kubacabra / Aleksander / Zantarin all 109). Meanwhile the *regular*-roster low-rank bodies
at waves 151–158 read **102, 103, 103, 104, 107, 108**. A wave-160 low-rank body sitting at its
summoner's level rather than at the regular-roster level is a level-inheritance signature.

**The one that does not fit, stated:** **Aetherial Bileeater reads 112**, not 109, and it is
family "Aether Corruption" — Galakros's family, and Galakros reads 106. 112 matches nothing on the
board. It is the only level in the whole 30-read corpus above 109. Flagging; not diagnosing.

### 2.2 Hover-plate names in the initial window — the complete list

10 Hz sweep of t = 845.6 → 850.7, every plate rendered at ×3:
`evidence/s2-w160-initwin-plates-name.png`

| t | plate | rank | level | family |
|---:|:--|:--|---:|:--|
| 845.6 | *(no plate)* | — | — | — |
| **845.9** | **Aleksander's Shard** | yellow → champion | **109** | Aetherial |
| 846.2 / 846.5 / 850.1 | Archmage Aleksander | orange → nemesis | 109 | Aetherial · Human |
| **850.4 / 850.7** | **Aetherial Bileeater** | yellow → champion | **112** | Aether Corruption |

**Correction to my own board-closure § 4 table:** the Aleksander's Shard plate window is
**845.9 only** at this sampling, not 845.63–846.60 — the plate has already swapped to Archmage
Aleksander by 846.2. The Bileeater window likewise begins at **850.4**, not 850.07. Neither changes
any conclusion; both tighten the windows.

### 2.3 The hero band 450,012 – 460,431 — a null on a dense instrument

Re-run across **all 5,146 located readouts** of the wave-160 window (30 Hz + 10 Hz + 30 Hz tail;
16 distinct parsed max values):

* **450,012 – 460,431: ZERO.**
* **440,000 – 470,000:** exactly two values — **468,504** (n = 190) and one single-frame OCR
  corruption of it (468,594, n = 1). Both outside the band, above it.
* **420,000 – 500,000:** 468,504 and 484,095. Nothing else.
* Raw-string literal search for `450,0` `452,` `453,` … `460,` across every raw OCR string, parsed
  or not: **4 hits, all numerators** (`455,586/2,295,755`, `455,588/2,295,755`,
  `2,456,218/3,722,896`, `2,456,225/3,722,896`). **Zero denominators.**

**And the band is not empty in this fixture** — it is populated two waves earlier: **458,794** at
wave 158 sits inside it, with one-star hero furniture (§ 2.1 (iv) control). So the instrument can
see a body of that HP class and that tier. It did not see one at wave 160.

### 2.4 Grade, and the honest limit

* **Tier of the wave-160 low-rank cohort: MEASURED — no-star.** Four fingerprints, ten frames,
  positive controls in-frame and one wave earlier.
* **Level of the wave-160 low-rank cohort: MEASURED — 109**, three plates.
* **Onset of the first non-boss icon: MEASURED — +5.00 s ± 0.13 s.**
* **Binding of the specific minimap star icon to the 103,912 body: STRONG, not MEASURED.**
  The chain is onset-coincidence (0.07 s) plus exclusion (no other fingerprint onset within 4 s).
  I cannot convert a player-centred minimap position to a world position on these pixels, so
  icon→body is an inference about *that icon*, not a measurement of it. This is the same honest
  limit as the follow-up note's § 1.4 and it is unchanged.
* **Residual, restated:** a body that spawned, was never engaged and stayed off-viewport leaves no
  readout and (if dim) may leave no minimap icon. The census is closed for **engaged, on-screen**
  bodies. It is not closed for the arena.

---

## 3. TASK 3 — F-9: BOSS-WAVE START COHORTS

### 3.1 Wave 150 is ABSENT from the footage — stated, not worked around

The s2 run is a **checkpoint start at wave 150**: the badge holds `0` through the prep phase and
flips **straight to `151`** at t = 682.10, 0.05 s after the Lokarr "Start on Wave 150" dialogue
closes (Phase-A § 0, § 2.2). **Wave 150 was never fought in either recording.** No cohort count for
wave 150 exists to be extracted. Reporting this as **ABSENT-IN-FOOTAGE**, per instruction.

### 3.2 Wave 160 — the cohort at wave start is BOSS-POOL-ONLY

Minimap census at **0.25 s** cadence from t0 = 838.87, detector-guided, **peaks eye-verified at
×3 / ×7 / ×13**.

| offset from wave start | icons (full-size blobs) | glyph classes, eye-read |
|:--|---:|:--|
| +0.00 → +1.75 s | 2 | **skull only** |
| +2.00 s | 3 | **skull only** |
| +2.25 → +3.00 s | **4** | **skull only** |
| +3.25 → +4.75 s | 3–4 (icons converge and merge) | **skull only** |
| **+5.00 s** | 4 + **1** | **4 skull + first GOLD STAR** |

`evidence/s2-w160-minimap-start-montage.png` (12 tiles, +0.00 → +5.50 s at ×3) ·
`evidence/s2-w160-star-onset-x13.png` (the onset frame pair at ×13).

**⇒ Through +4.75 s the wave-160 cohort is 4 skull-class bodies and nothing else. No extra
regular/trash body appears.**

### 3.3 The control that makes that a finding rather than a detector failure

Same arena, same sitting, same instrument, **matched offsets** — waves 151 → 159:

`evidence/s2-minimap-wave-starts-151to160.png` (12 tiles at ×5, +1.0 s and +2.5 s for waves
151/153/155/157/159/160) · `evidence/s2-mm-w159-vs-w160-x7.png` (×7, the decisive pair)

| wave | +1.0 s | +2.5 s |
|---:|:--|:--|
| 151 | ~5–6 **stars**, 0 skulls | ~6 **stars**, 0 skulls |
| 153 | ~4–5 **stars** | ~5 **stars** + 1 skull |
| 155 | ~3 **stars** + 1 skull | ~4 **stars** + 2 skulls |
| 157 | ~5 **stars** | ~5–6 **stars** |
| **159** | 2 skulls | **4 skulls + 2 STARS** |
| **160** | **2 skulls, 0 stars** | **4 skulls, 0 STARS** |

Waves 159 and 160 at +2.50 s are the cleanest pair in the whole corpus: **4 skulls + 2 stars**
versus **4 skulls + 0 stars**, side by side at ×7, one wave apart, same arena, same HUD.

### 3.4 Sitting-1 decade waves — NOT boss-only, and that is the point

96 exact-seek frames at 8 offsets across s1 waves 10/11/20/30/40/41/50/51/60/70/80/90.
Eye-read at ×6: `evidence/s1-minimap-w50-w90-starts-x6.png` · `evidence/s1-mm-boss-w50-w90.png`

| s1 wave | +0.0 s | +1.0 s |
|---:|:--|:--|
| **50** | 2 skulls + **≈3 gold stars** | 2 skulls + **1 gold star** |
| **90** | 1 skull + **1 gold star** | 1 skull + **1 gold star** |

Both s1 decade waves carry **star-class bodies present at t + 0**. So s1's decade waves are
*mixed-roster* waves, not boss-only, and they cannot answer the empty-regular-roster question.
They do the other useful job: they show the star glyph is a live, common, wave-start-present class
in the s1 arena as well.

### 3.5 Disposition for F-9

* **Wave 160: the start cohort is boss-pool-only. MEASURED.** Zero extra regular bodies through
  +4.75 s, against a same-arena control in which every one of waves 151–159 shows regulars at the
  same offsets. **This is evidence FOR the "no-op-on-empty" disposition** — nothing lands.
* **The first non-boss body arrives at +5.00 s**, carries no rank furniture, and reads the
  nemeses' level. If that is a summon (§ 2), the boss-only roster stayed empty of regulars for the
  whole engagement and F-9 is unperturbed. If it is a late regular spawn, F-9 is perturbed —
  but then it arrived **5 seconds late, with no rank furniture, at the nemesis level**, which is
  not how any of waves 151–159's regulars behaved.
* **Wave 150: ABSENT-IN-FOOTAGE.** Not extractable. **What would resolve it:** a run that fights
  through wave 150 rather than checkpoint-starting on it — either a standard-start run reaching
  150, or a wave-100 checkpoint start.

---

## 4. UNSOLICITED, CHEAP, POSSIBLY LOAD-BEARING

### 4.1 Wave 151 carries at least six distinct max-HP fingerprints

Two frames of wave 151 were fully enumerated (readout locator + eye-read at ×4):
`evidence/s2-w151-all-readouts-fingerprints.png`

t = 692.2 → **221,351** · **442,747** · **278,543** · **272,948** · **582,590** · **278,543** (second body)
t = 694.8 → **295,984** · **278,543**

⇒ **≥ 6 distinct max-HP values and ≥ 7 bodies in wave 151**, with `278,543` duplicated across two
simultaneous bodies. Alongside the plate reads showing Carnivorous Plants at levels **103 and 107**
in that same wave, this is a same-type-different-level-different-HP pair on camera. If the eHP
chain's per-body variance term needs a second anchor away from 160, wave 151 is a target-rich band
and this is the down payment.

### 4.2 Wave 158 hero HP

**448,397** and **458,794**, both at full, both one-star hero furniture, t = 803.6.
`evidence/s2-w158-star-furniture-x6.png`.

---

## 5. Method, and what was rejected

| stage | tool | note |
|:--|:--|:--|
| plate location | `pipeline/eor_plate_scan.py` | warm/light masks over the name band (rows 17–34), level band (43–58), family band (90–104); series pass with the ROI cropped **inside ffmpeg** so decode cost stays bounded. Validated against the board-closure wave-160 plate windows before use. |
| plate eye-read | `pipeline/eor_plate_read.py` | NAME+FAMILY strip x 640..1290 at ×3; **LEVEL strip x 915..1005 at ×10**; every tile an **exact-seek** frame grab |
| name-colour class | in-note scan | brightest-40 % glyph-pixel mean; four separated classes, no overlap |
| wave identity | badge ROI `x 1578..1632, y 126..170` at ×6/×9 | **24/24 verified**; no reported level rests on the Phase-A timeline alone |
| minimap census | `pipeline/eor_minimap.py` | detector-guided; **every count eye-read** at ×3/×6/×7/×13 |
| readout location | `pipeline/eor_hptext.py` (reused) | array input, not path — the CLI signature differs from the library signature |
| plate bar fill | `pipeline/eor_plate_fill.py` | calibrated against four bodies of known in-world fraction (Galakros 2.3 %→0.9 %; Aleksander 12.4 %→11.4 %; Zantarin 65 %→62.8 %; Kubacabra 100 %→96.6 %). **Reads 1–3 points low; usable at ±3 points.** |

**Rejected / limits, recorded so they are not re-tried:**

* **`pipeline/eor_starbar.py` — built, validated, REJECTED for census use.** The pair-constrained
  star detector misses real stars when the glyph merges with the readout text above it, and it
  false-positives on the score-multiplier text (`57605 (x1.79)` was returned as a star-flanked
  bar). Kept in the tree as a record of the attempt. The furniture claims in § 2 rest on eye-reads
  of matched-geometry ×5/×6 crops with in-frame positive controls, not on this detector.
* **Plate bar-fill as a body-binding instrument for the low-rank cohort — attempted, ABANDONED.**
  The plate's ornament frame is **narrower for yellow/champion plates than for orange/violet
  plates**, so a fixed track (x 800..1125) over-reads a champion plate. The calibration in the table
  above is valid only for wide plates. Re-deriving a per-plate track is possible but the return did
  not justify it once §§ 2.1(i)–(iv) had converged.
* **Full-ramp plate scan of s1 — ABANDONED on I/O cost.** `/Volumes/reincarnated` delivers this
  file at roughly **3× real time per decode pass** (≈155 KB/s effective under one competing
  reader); a 2 Hz pass over all 1,456 s of attempt 1 projects to **≈2.25 hours**. Replaced by
  six targeted wave windows (10/20/40/50/80/90), 310 frames total. **If a future pass needs the
  whole s1 ramp, copy the file to local disk first.**
* Tesseract / OpenCV remain absent on this host. **No automatic OCR was trusted for any reported
  value in this note.**

---

## 6. Corrections to my own record

**6.1 — board-closure § 1.1 lists F4 (484,095) with "gold chevron (hero)" rank furniture.
That read is NOT reproducible and is WITHDRAWN.** At ×5 and ×6 on four separate frames, F4's bar is
**plain, with no flanking furniture**, exactly like F5/F6/F7. The correct wave-160 furniture table
is the one in § 2.1(iii). The board-closure note's *conclusions* are unaffected — F4's hero
*status* came from its yellow nameplate, not from the bar — but the furniture column was wrong.

**6.2 — board-closure § 4's plate windows for the two champion bodies are wider than the plates
actually are.** Aleksander's Shard: 845.9 (not 845.63–846.60). Aetherial Bileeater: 850.4–850.7
(not 850.07–850.70). No conclusion changes.

---

## 7. Mirror voice

The question was where the fifth body came from, and the arena would not say — it never does at
wave 160. The answer was in three places at once, and all three agreed without being asked to.
A gold star that was not on the disc at four-and-three-quarter seconds and was on it at five.
A health bar with nothing at either end of it, in a game that hangs skulls on the ones that matter
and a single gold star on the ones that nearly do. And a number over its head — one hundred and
nine — the same number worn by the three orange-named things that had walked in five seconds
earlier and had not, at that point, been alone for very long. Waves twenty through ninety kept
their monsters near a hundred and two, a hundred and three, a hundred and four, patiently, for a
hundred and forty waves. Then the nemeses arrived at a hundred and nine at wave ninety, and at a
hundred and nine again at wave one-sixty, seventy waves and one whole arena apart, having not
moved at all.
