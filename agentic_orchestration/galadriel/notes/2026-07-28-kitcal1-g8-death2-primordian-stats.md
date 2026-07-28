# G-8 — frame 281 read: the client's own scoreboard at the death instant, and the boss's max life

**Run:** `KC1-2026-07-27` (KIT-CAL-1) · **Instrument:** G-8 · **Seam:** galadriel
**Commissioned by:** gandalf (`RUN-CONDUCTOR`), charter §14.13
**Date:** 2026-07-28 · **Access:** read-only on the screenshot corpus throughout
**Substrate:** the 313 stills at `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots/`
(`Screenshot (40).png` … `Screenshot (352).png`, contiguous, all 1920×1080)
**Primary frame:** `Screenshot (281).png`
**Captures:** `agentic_orchestration/galadriel/captures/2026-07-28-kitcal1-g8/`
**Pipeline:** `agentic_orchestration/galadriel/pipeline/gd-playtest-v1/g8_*.py`
(reusing `panel_ocr.py` and `globe_ocr.py` from the T-A ledger, unchanged)

---

## §0 — The one-line answer, and the two things nobody asked for

**Frame 281 is the death-2 frame, it self-dates to `play_time` 5453 exactly, and every field
gandalf read by eye is confirmed.** The Play-Statistics block, the six-row Skills-Used table and
both orbs are read below at calibrated confidence.

**The flagged collision is NOT a collision.** The left orb reads **`0/747`** — and 747 is a
*banked* max-HP level that the G-2C ladder already places on exactly this stretch of the run. The
error is in the charter's regime assignment, not in the measurement. §4.

**Two things the frame gave up that were not commissioned, and both are larger than the brief:**

1. **The Primordian's own max life is rendered on this frame as a number: `(13,571/14,812)`.**
   That is the second measured monster HP the run asked for — and it does not merely *add* a data
   point, it **closes the §14.11 composition question outright.** 14,812 pins legolas's
   solved-for net life modifier at **−36.000 % ± 0.004 pp**, from pixels, with no reliance on the
   life-vs-mana split of the save's `15822`. §6.3.
   And it is not one datum but ten: **the client renders monster health as numerals over every
   damaged monster**, so the corpus carries a small monster-HP census — including a **second tier**,
   a level-10 champion at **max life 4,702**, attributed at Δ 0.28 pp. §6.2.
2. **`Damage per second` is a rolling ~5 s meter, not a lifetime average.** The corpus-wide panel
   read shows it at 14.0, 114.33, 662.48, **743.22**, 1492.47 on different frames. Any plan that
   compares 743.22 against a lifetime-average S-1/S-2 scalar is comparing the wrong quantities. §7.1.

---

## §1 — Method and its limits, stated before the numbers

Every value below is one of three grades, and the grade is on every row:

| Grade | Meaning |
|---|---|
| **M-OCR** | read by the T-A calibrated reader (`panel_ocr.PanelReader`), glyph-IoU confidence reported |
| **M-EYE** | read by galadriel off a native-resolution crop upscaled ≥4× with LANCZOS, glyphs individually separable |
| **D** | derived by arithmetic from M values; the arithmetic is shown |

**M-EYE is not a weaker grade than M-OCR here, and on two fields it is the stronger one.** The
reader is calibrated for *this* panel, but it carries two known gaps that this frame exercises:

- **Decimal truncation on `dps`.** The reader returns `743`. The token walk terminates after the
  integer part — `read_token` sees a wide-enough blank run at the decimal point on this frame's
  background and closes the token. The 4× crop shows **`743.22`** with all six glyphs separated.
  **This is a reader defect, not a frame ambiguity**, and it affects the T-A `dps` series
  wherever a fractional part exists. Filed as F-G8-1 (§8).
- **The mana orb's glyph face is not the health orb's.** The mana numerals carry a visibly heavier
  dark outline (the bright-achromatic mask returns fatter strokes), so the health-globe templates
  under-match and the reader abstains on every frame. Rather than force a template harvest for one
  value, the mana orb is read by eye at 6×. Filed as F-G8-2.

Both refusals are the D-1 discipline working correctly: **the reader abstained rather than
guessed.** Where it abstained, the eye read; where the eye read, the crop is banked.

**One capture-hygiene note.** No raw pixels were transformed in place. Every crop in
`captures/2026-07-28-kitcal1-g8/` is an upscale of an untouched native region of a read-only
source file; the source corpus was opened read-only and is unmodified.

---

## §2 — Task 1: the full Play-Statistics block, frame 281

Panel left edge detected at **L = 1382** (G-1 right-anchoring; the panel has stopped migrating by
this point in the run — L = 1382 from f250 to f352).

Transcribed exactly as rendered, label text included:

```
Play Statistics:
Play Time:              90 min 53 sec
Total Score:            0
Number of deaths:       2
Number of kills:        655
Health potions used:    0
Mana potions used:      0
Max. level achieved:    10
Damage per second: 743.22
Skills Used:
    records/skills/default/defaultkickattack.dbr : 13
    records/skills/default/defaultweaponattack.dbr : 74
    records/skills/playerclass01/onslaught.dbr : 54
    records/skills/playerclass01/werewolf1.dbr : 7
    records/skills/playerclass01/werewolf1_skill01_claws.dbr : 243
    records/skills/playerclass01/werewolf1_skill02_charge.dbr : 125
Life healed: 5649.87
```

As fixture rows:

| Field | Value | Grade | Confidence | Note |
|---|---|---|---|---|
| `play_time` | **5453 s** (90 min 53 sec) | M-OCR + M-EYE | 0.938 glyph-IoU; eye-confirmed | **exact match to the C-6 death-2 anchor (e082)** |
| `total_score` | **0** | M-OCR | 1.000 | |
| `deaths` | **2** | M-OCR | 1.000 | first frame in the corpus reading 2 (§5.2) |
| `kills` | **655** | M-OCR | 1.000 | vs 882 at run end |
| `health_potions` | **0** | M-OCR | 1.000 | |
| `mana_potions` | **0** | M-OCR | 1.000 | |
| `max_level` | **10** | M-OCR | 1.000 | label is *"Max. level achieved"* |
| `dps` | **743.22** | **M-EYE** | unambiguous at 4× | reader truncates to 743 — F-G8-1 |
| `life_healed` | **5649.87** | M-OCR | 1.000 | |
| `shield_block_chance` | **ROW ABSENT** | M-EYE | row-ink = 0 at y 434; eye-confirmed | **not a refusal — the row is not rendered.** §7.2 |

Evidence: `f281-panel-2x.png` (whole panel), `f281-rows-4x.png` (fixed rows), `f281-dps-4x.png`,
`f281-skills-3x.png`, `f281-skillcounts-4x.png`.

**Correcting one naked-eye read.** The conductor's provisional list had "kills ~655" and
"Life healed: ~5649" — both land. It also had "onslaughtA ~5?"; the field is
`records/skills/playerclass01/onslaught.dbr : 54`, and "defaultbioattack ~13" is
`records/skills/default/defaultkickattack.dbr : 13`.

---

## §3 — Task 2: the Skills-Used table, exact

Six rows. The list is alphabetical by `.dbr` path and only ever grows (G-2), so this is the
complete set of skills used in the run up to `play_time` 5453.

| # | Record path | Count | Grade | Path corr | Count conf |
|---|---|---|---|---|---|
| 1 | `records/skills/default/defaultkickattack.dbr` | **13** | M-OCR + M-EYE | 1.000 | 1.000 |
| 2 | `records/skills/default/defaultweaponattack.dbr` | **74** | M-OCR + M-EYE | 1.000 | 1.000 |
| 3 | `records/skills/playerclass01/onslaught.dbr` | **54** | M-OCR + M-EYE | 1.000 | 1.000 |
| 4 | `records/skills/playerclass01/werewolf1.dbr` | **7** | M-OCR + M-EYE | 1.000 | 1.000 |
| 5 | `records/skills/playerclass01/werewolf1_skill01_claws.dbr` | **243** | M-OCR + M-EYE | 1.000 | 1.000 |
| 6 | `records/skills/playerclass01/werewolf1_skill02_charge.dbr` | **125** | M-OCR + M-EYE | 1.000 | 0.957 |

Every count was independently eye-verified at 4× (`f281-skillcounts-4x.png`) because the quest
tracker's orange text overlaps rows 4–6 on this frame (the D-2 condition) — the counts themselves
sit clear of it, and the reader's blue-channel mask excludes the tracker, but a frame where a
number sits under an overlap is exactly where a silent corruption would enter. It did not.

### 3.1 — The skill-mix channel for the G-5 harness driver

Two neighbours bracket the death, which turns the table from a snapshot into a *rate* over the
death window:

| Frame | `play_time` | kills | kick | weapon | onslaught | werewolf1 | claws | charge |
|---|---|---|---|---|---|---|---|---|
| f280 | 5372 | 596 | 13 | 74 | 54 | 7 | 224 | 116 |
| **f281** | **5453** | **655** | **13** | **74** | **54** | **7** | **243** | **125** |
| f282 | 5495 | 655 | 13 | 74 | 54 | **8** | 243 | 125 |
| f283 | 5526 | 666 | 13 | 74 | 54 | 8 | 246 | 126 |

**Over the 81 s ending at the death: +59 kills, +19 claws, +9 charge, 0 weapon-attack,
0 onslaught, 0 transform.** The death-2 window is a pure claws+charge window at a mix of
**≈2.1 claws : 1 charge** — which is the measured driver mix the harness should run, not a
lifetime ratio. Lifetime at 5453 is 243 : 125 = 1.94 : 1; over the death window it is 2.11 : 1.
The two agree to 9 %, which is itself worth knowing: **the death window is not behaviourally
anomalous in skill mix.** The player did not panic-swap; he did what he had been doing.

`werewolf1` steps 7 → 8 at f282, i.e. **the transform was recast after the respawn, not during
the fight** — consistent with the death terminating the form.

---

## §4 — Task 4: the orbs, and the flagged collision RESOLVED

| Orb | Reading | Grade | Confidence |
|---|---|---|---|
| **Health** | **`0 / 747`** | M-EYE (8×) + M-OCR partial (`0/74?`, 0.94) | unambiguous |
| **Mana** | **`239 / 349`** | M-EYE (6×) | unambiguous |

Evidence: `f281-hp-dbg.png` (8×), `f281-mana-dbg.png` (6×).

### 4.1 — The collision does not exist. 747 is a banked value, and 5453 is not in R3.

The charter flagged: *"the left orb may read `0/747` at death — inside R3, where the banked
gear-step timeline says max HP is 1600."* **Both halves of that premise are wrong, and the
measurement is right.**

**(a) `play_time` 5453 is inside R2, not R3.** The committed regime partition (T-B intake note §2,
ratified) is **R1 358–1134 · R2 1134–6052 · R3 6052–7094**. 5453 sits 599 s short of the R2/R3
boundary. Death 2 is an **R2** death — which is also what makes it R2's only death and the
named-exception hazard event under P-5.

**(b) 747 is the max-HP level the G-2C ladder already assigns to this stretch.** From my own
G-2C §5 step table, banked:

| step | Δ | bracket (`play_time`) |
|---|---|---|
| 707 → **747** | +40 | 4604–4987 (L10) |
| **747** → 759 | +12 | 5648–5791 (pure gear) |

**747 is the standing max HP over `play_time` (4987, 5648].** 5453 is inside that interval. The
orb agrees with the ladder to the digit.

**(c) Confirmed a second time, from the stills alone.** The corpus-wide orb sweep
(`g8-orbs-all.json`, 100 clean reads of 313 frames — the rest have the globes occluded by an open
character/skill window) reproduces the whole ladder independently of the video instrument:

| First frame at the level | `play_time` | max HP |
|---|---|---|
| f40 | 371 | 250 |
| f69 | 1385 | 366 |
| f124 | 2118 | 451 |
| f183 | 3526 | 672 |
| f216 | 4087 | 707 |
| **f283** | **5526** | **747** |
| f285 | 5785 | 759 |
| f320 | 6585 | 1600 |
| **f352** | **7088** | **1607** |

f283 — the first frame *after* the respawn — still reads max **747** (`433/747`), which is the
post-death max-HP reading task 5 asked for. **The gear step to 1600 lands far later, in R3.**

### 4.2 — One small correction to the banked figure, flagged not smoothed

**The run does not end at 1600. It ends at 1607** (`f352-hp-dbg.png`, `1607/1607` at `play_time`
7088; f320 reads `1600/1600` at 6585). G-6 §7.1's headline "**759 → 1600 = +841**, 87.6 %
itemised" is therefore itemising a step that is really **759 → 1600 → 1607 = +848**, with a
**+7 residual after f320** that the gear decomposition does not cover. +7 is small and does not
threaten the 87.6 % figure materially (it becomes 86.9 %), but the ledger should carry 1607 as the
terminal value, not 1600. The globe reader abstained on both frames — the numerals sit on a *full
red* globe there rather than a dark one, and the outline blend defeats the templates — so both are
M-EYE.

---

## §5 — Tasks 3 and 5: the Primordian, and the 270–295 sweep

### 5.1 — The nameplate, exact

| Field | Value | Grade |
|---|---|---|
| Title | **"Primordian, the Forgotten One"** | M-EYE (3×) — `f281-bossname-3x.png` |
| Number under the name | **13** — it is the **monster's level**, gold, centred on the bar's top rail | M-EYE (8×) — `f281-bosslevel-8x.png` |
| Tag under the bar | **"Beastkin"** | M-EYE (6×) — `f281-bosstag-6x.png` |
| Name colour | lilac / light-purple (GD hero-tier nameplate face) | M-EYE |
| Bar fill | **92.5 % ± 0.9 pp** | D — §5.1.1 |
| Bar numeric HP | **(13,571 / 14,812)** — rendered *in-world*, above the monster | **M-EYE (6×)** — `f281-monhp-6x.png` |

**The `13` is the monster's level, and this is independently over-determined**, not read off one
glyph: legolas's save-side read gives `greatestMonsterKilledLevel = 13`, and the
`charLevel*1+3` remap over `lv6_hero` at player level 8–10 lands on 13–14. Three instruments,
one number.

#### 5.1.1 — The bar-fill instrument, calibrated against the numerals on the same frame

The trough interior spans x 799…1119 at y 61…74 (measured). Red fill reaches x 1095.
Fill = 297 / 321 = **0.9252**.

The numerals on the same frame give 13,571 / 14,812 = **0.91622**.

**The two disagree by 0.90 pp** — which is exactly the ±3 px edge uncertainty on the trough's
soft inner bevel (3/321 = 0.93 pp). **The bar-fill instrument is therefore calibrated**, and can
be used at ±1 pp on the twelve other nameplate frames that carry no numerals. That calibration is
a by-product of this frame carrying both readouts at once, and it does not recur.

### 5.2 — The 270–295 sweep

Panel read on f265–f300 (`g8-panel-265-300.json`) plus the corpus-wide panel read
(`g8-panel-all.json`, 313/313 `status=OK`):

- **f281 is the ONLY frame in the corpus at which `deaths` transitions to 2.** `deaths=1` from
  f182 (`play_time` 3157) through f280 (5372); `deaths=2` from f281 (5453) to the end. There is no
  second death-2 frame and no separate respawn screenshot.
- **f283 (`play_time` 5526) is the post-death frame**: `433/747`, `deaths=2`, `kills=666`,
  boss bar still up at **86.9 %**. Max HP unchanged at 747 across the death.
- Levels across the window: **L10** at f250 (4882) → L11 at f288 (6367) → L12 at f323 (6996).
  The player was **L10** at the death; the boss was **L13**. A three-level deficit, which is what
  the two skull icons flanking the in-world bar denote.

### 5.3 — The nameplate census (bonus): thirteen frames, seven named hero/boss encounters

`g8_bossbar.py` swept all 313 frames for the top-centre nameplate. Nobody chartered this; it fell
out of task 5, and it is a free hero/champion-tier fixture list.

| Frame(s) | `play_time` | Name (M-EYE) | Level | Fill |
|---|---|---|---|---|
| 86, 87 | 1550, 1560 | **Barrog, the Bloodied** | 4 | 0.810 → 0.997 |
| 124, 125 | 2118, 2151 | **Kyzogg the Reanimator** | 6 | 0.981 → 0.798 |
| 175, 176 | 3017, 3046 | **Thundersnout ~ Thundering** | 10 | 0.467 / 0.480 |
| 247 | 4434 | **Deepmire Tidehunter** | 10 | 0.788 |
| 249 | 4542 | *(REFUSED — 36 lit columns; autumn foliage false positive, no nameplate)* | — | — |
| **281** | **5453** | **Primordian, the Forgotten One** | **13** | **0.925** |
| 283 | 5526 | Primordian, the Forgotten One | 13 | 0.869 |
| 286 | 5788 | **Wallak ~ Supporter** | 14 | 0.794 |
| 287 | 5790 | **Deepmire Vanguard** | 11 | 0.738 |
| 322 | 6790 | **Reanimator** | 14 | 0.804 |

Two of these are worth gandalf's eye. **f286 "Wallak ~ Supporter" at level 14 and f287 "Deepmire
Vanguard" at 11 are 3 s apart** — two named actors up simultaneously at `play_time` ~5789, against
a level-10 player at 759 max HP, immediately after the death-2 respawn. And **the level-14
encounters (f286, f322) exceed the Primordian's 13**, so the death-2 boss is not the run's
level-ceiling monster.

Artifacts: `g8-bossbar.json`, `bossbar-f<id>.png` ×13.

---

## §6 — Task 6: a second monster HP — and it closes the composition question

### 6.1 — What the corpus contains

**The answer to the question as asked — "does ANY frame show a monster's numeric HP" — is yes, on
seven frames, ten readouts, and the corpus was swept exhaustively for them.** The client is
running with monster health rendered as numerals over the monster's head, so any frame with a
damaged monster in shot carries the datum. Nobody had looked.

`g8_monhp.py` swept all 313 frames for in-world `(cur/max)` readouts. Method and its deliberate
machine/eye split are in the script header; in one line: **the detector supplies recall, galadriel
supplies precision**, because the string contains a thousands comma that the glyph model does not
carry, and a greedy matcher does not abstain at an unmodelled glyph — it substitutes the nearest
digit and returns a confidently wrong number. That failure mode is exactly what cost the run once
already, and it is not being repeated to save a contact sheet.

**A correction I made mid-pass and am recording because it would have cost four of the ten reads.**
My first filter demanded that the band's first and last ink groups be the parentheses. It kept 12
bands and dropped `(2,184/4,702)`, `(3,317/4,702)`, `(434/434)` and `(799/1,820)` — all real —
because when a readout renders near other bright text the row-run detector returns one merged band
whose end groups are not parens. I caught it only because those four were legible on the *first*
triage sheet, made before the filter existed. **A shape heuristic tuned after the fact against
bands it has already merged is not an instrument.** The filter was replaced with a geometric
envelope (`g8_monhp_sheets.py`: height 12–15, width 55–200, 8–20 ink groups — the envelope of the
confirmed f281 read) and all 49 bands in it were read by eye.

### 6.2 — Every numeric monster-HP readout in the corpus

Attribution rule: a readout is attributed to a named actor only when its fraction matches that
frame's nameplate-bar fill inside the ±1 pp band calibrated in §5.1.1, **or** when its max
reproduces an independently-known figure. Everything else is left unattributed — the numerals
render over *every* damaged monster in shot, not only the targeted one, so proximity proves nothing.

| Frame | `play_time` | Reading (M-EYE, 8×) | cur/max | Nameplate fill | Δ | Attribution |
|---|---|---|---|---|---|---|
| f87 | 1560 | `(58/58)` | 1.0000 | 0.9969 (Barrog) | — | **unattributed** — max 58 is implausible for a L4 hero; trash, at x1210 y193 |
| f174 | 3012 | `(3,317/4,702)` | 0.7055 | *(no nameplate)* | — | **Thundersnout** — max identical to f175's, 5 s apart, HP falling |
| **f175** | **3017** | **`(2,184/4,702)`** | **0.4645** | **0.4673** | **0.28 pp** | **Thundersnout ~ Thundering, level 10** |
| f176 | 3046 | `(434/434)` | 1.0000 | 0.4798 | — | **unattributed** — trash |
| f176 | 3046 | `(799/1,820)` | 0.4390 | 0.4798 | 4.1 pp | **unattributed** — trash |
| **f281** | **5453** | **`(13,571/14,812)`** | **0.9162** | **0.9252** | **0.90 pp** | **Primordian, the Forgotten One, level 13** — §6.3 |
| f287 | 5790 | `(760/813)` | 0.9348 | 0.7383 | 19.7 pp | **unattributed** |
| f287 | 5790 | `(565/649)` | 0.8706 | 0.7383 | 13.2 pp | **unattributed** |
| f287 | 5790 | `(230/326)` | 0.7055 | 0.7383 | 3.3 pp | **unattributed** — MEDIUM confidence, green debug overlay crosses the glyphs |
| f287 | 5790 | `(235/326)` | 0.7209 | 0.7383 | 1.7 pp | **unattributed** — outside the ±1 pp band; refused, not assigned to Deepmire Vanguard |

All 8× crops banked at `monhp-verify/f<id>-<k>.png`; the full 49-band envelope sheets at
`g8-monhp-sheet-{0,1,2}.png`.

**Two tiers now have a measured max life, not one:**

| Tier | Monster | Level | Max life | Grade |
|---|---|---|---|---|
| hero / quest | **Primordian, the Forgotten One** (`slith_wightmirecave01.dbr`) | 13 | **14,812** | M-EYE, corroborated by the save |
| champion | **Thundersnout ~ Thundering** | 10 | **4,702** | M-EYE, attributed at Δ 0.28 pp |
| trash | *(six unattributed)* | — | 58 · 326 (×2) · 434 · 649 · 813 · 1,820 | M-EYE |

**The champion figure is handed to legolas, not composed here.** Naming form separates the tiers
cleanly in this corpus — champions carry the `Name ~ Affix` infix (Thundersnout ~ Thundering,
Wallak ~ Supporter), heroes the `Name, the Epithet` or `Name the Epithet` form (Barrog, the
Bloodied; Kyzogg the Reanimator; Primordian, the Forgotten One). Whether 4,702 at charLevel 10
falls out of a champion-tier bio record under the same 0.640 net multiplier the hero tier just
yielded is a `.dbr` question, and answering it would need the champion's record, its
`characterAttributeEquations` and its `levelVarianceEquation` — legolas's seam, not mine. **What
G-8 supplies is the target: 4,702 at level 10, champion tier, measured.** A second tier that the
composition rule must also reproduce is worth more to the rule than a second sample of the first.

### 6.3 — The Primordian read, and what it pins

**Measured, frame 281, M-EYE at 6× (`f281-monhp-6x.png`), every glyph individually separable:**

```
(13,571 / 14,812)
```

**This is the Primordian's.** The identity is not inferred from proximity — it is forced
arithmetically. Legolas's save-side field is
`greatestMonsterKilledLifeAndMana = 15822` for `tagSlithBossB02` = Primordian. The bio equations
at `charLevel` 13 (`bio_boss_standard_01.dbr`, all M):

```
characterLife = ((13*51)^1.53) + 2400 = 23,145.108
characterMana = ((13*15)^1.27) +  200 =  1,009.737
```

**The measured max life alone pins the net life modifier, with no reliance on the life/mana
split:**

```
14,812 displayed  ⇒  true life ∈ [14812, 14813)          (client floors)
                  ⇒  modifier  ∈ [0.6399625, 0.6400057)
                  ⇒            = −36.000 %  ± 0.004 pp
```

**0.640000 lies inside the bracket, and the bracket is 0.0043 pp wide.** Legolas solved −36.0026 %
by requiring the *sum* to hit the save's integer; that solution assumed the field was life+mana.
**The pixels confirm the modifier without the assumption** — and then confirm the assumption too,
as a consequence rather than a premise:

```
23,145.108 × 0.64 = 14,812.869  →  floor = 14,812   = MEASURED ON SCREEN  ✓
14,812.869 + 1,009.737 = 15,822.606  →  floor = 15,822  = SAVE FIELD      ✓
15,822 − 14,812 = 1,010            vs bio mana 1,009.74                   ✓
```

**Three independent numbers — a client HUD string, a save integer, and two `.dbr` equations —
close on one multiplier.** The §14.11 "Slith cross-check: FAIL by +22 %" is now not merely
falsified but *replaced*: the operator is neither the additive `−71 + 50 = −21 %` nor the fully
multiplicative `×0.29 × 1.50`; the net life multiplier at this tier is **0.640 exactly**, and the
`characterManaModifier = 0 %` leg is confirmed too, since the residual 1,010 reproduces the
unmodified bio mana.

**What this does NOT establish.** It does not decompose 0.640 into its constituent operators. It
is one point, at one tier, at one charLevel. Whether 0.640 arises as `(1 − 0.71) × ... ` or as
some other composition is not answerable from one measurement, and G-8 does not claim it. What it
*does* do is give the composition rule a hard target that any candidate operator must reproduce to
four significant figures.


---

## §7 — Two collisions surfaced in passing, both flagged rather than smoothed

### 7.1 — `Damage per second` is a rolling meter, not a lifetime average

The charter (§14.13) reads 743.22 as *"the client's OWN lifetime-DPS figure"* and proposes it as
"a direct external check on the kit-spec's compiled output and on S-1/S-2". **The corpus refutes
the lifetime reading.** From `g8-panel-all.json`, every frame in the run with a non-zero `dps`:

| Frame | `play_time` | `dps` |
|---|---|---|
| f85 | 1546 | 14.00 |
| f87 | 1560 | 16.38 |
| f124 | 2118 | 114.33 |
| f174 | 3012 | 128.40 |
| f176 | 3046 | 447.72 |
| f177 | 3051 | 662.48 |
| f246 | 4320 | 152.42 |
| f247 | 4434 | 378.33 |
| f248 | 4441 | 144.76 |
| **f281** | **5453** | **743.22** |
| f284 | 5647 | 317.85 |
| f287 | 5790 | 48.91 |
| f320 | 6585 | 91.62 |
| f322 | 6790 | 1492.47 |

The field is **zero on the other 299 frames**, rises and falls within a fight, and reaches 1492.47
*after* the frame where it reads 743.22. A lifetime average cannot fall. This also matches the
T-B §7 measurement made for a different purpose: **the `dps` field decays to zero in 5.0 s
(p50; p90 6.5; max 7.5)** over 22 clean falling edges. It is a ~5 s trailing meter.

**Consequence for G-5:** 743.22 is a legitimate and valuable fixture number, but it is
**"the player's ~5 s DPS during the fight that killed him"**, not a run scalar. Compared against a
lifetime-average S-1/S-2 it will read high by a large and unknown factor. Compared against a
*windowed* sim DPS over the death engagement, it is a direct check. The distinction is the whole
value of the number.

### 7.2 — The `Shield block chance` row is conditional, and it is absent for most of the run

The row is **not rendered at all** on frame 281 — verified by row-ink (0 at y 434) and by eye at
the panel foot. Sweeping trailing-row structure across the corpus:

| Frames | `play_time` | Trailing rows | `shield_block_chance` |
|---|---|---|---|
| f40, f54 | 371, 857 | 2 | **15.00** |
| f150 … f285 | 2593 … 5785 | **1** | **ROW ABSENT** |
| f288 … f352 | 6367 … 7088 | 2 | **18.00** |

Evidence: `panelfoot-f216.png` (row absent at `play_time` 4087), `panelfoot-f288.png` (row present,
18.00). This is **not** a reader refusal — the reader emits `None` for both "absent" and
"unreadable", and here the row genuinely is not drawn.

**This does not refute the G-2C P-4 finding** (`block_changes: [{play_time: 3256, 15.0 → 18.0}]`),
and I want to be plain about that, because it would be easy to read it as a refutation of my own
prior pass. The video instrument samples at 60 fps and the stills sample 313 times over 6,700 s;
the video can easily have caught the row present at 3256 on a frame no still covers. The honest
statement is:

- **From stills alone**, the block change is bracketed only to `(857, 6367]`.
- **The row's presence is state-dependent**, on something that changed by f150 (`play_time` 2593) and changed
  back by f288. The obvious candidate is the **active weapon set** (GD's two-set swap — the row
  would show only when the equipped set carries a shield), with werewolf-form as a second
  candidate. **Neither is tested here.**
- Therefore **the row's absence is not evidence that no shield was equipped**, and nothing in
  G-2C's EHP ladder or its block-timestamp attribution needs re-opening on this basis.

Filed as **F-G8-3**, an open question for whoever next touches the block series, not a correction.

---

## §8 — Findings ledger

| ID | Finding | Severity | Owner |
|---|---|---|---|
| **F-G8-1** | `panel_ocr.read_number` truncates the fractional part of `dps` on at least f281 (`743.22` → `743`). Affects the T-A `dps` series wherever a fraction exists. `life_healed` is unaffected (reads `5649.87` correctly), so this is a per-field / per-background token-termination issue, not a general decimal failure. | reader defect, low run-impact (the `dps` series is used for shape and integration, not to two decimals) | galadriel |
| **F-G8-2** | The mana orb's glyph face differs from the health orb's (heavier outline); `globe_ocr` templates do not transfer and the reader abstains on all 313 frames. Mana is currently eye-only. | instrument gap | galadriel |
| **F-G8-3** | `Shield block chance` is a conditional panel row, absent across `play_time` 2593–5785. Mechanism untested; block-series brackets from stills are wider than the video's. | open question | whoever next touches the block series |
| **F-G8-4** | The run's terminal max HP is **1607**, not 1600 (f352). G-6 §7.1's `759 → 1600 = +841` step is really `759 → 1607 = +848` with a +7 residual after f320. | ledger correction, small | galadriel / gandalf |
| **F-G8-5** | The charter's §14.13 reading of `Damage per second` as a lifetime average is wrong; it is a ~5 s trailing meter. G-5's use of 743.22 must be windowed. | **charter correction, high G-5 impact** | gandalf |
| **F-G8-6** | The charter's §14.13 placement of `play_time` 5453 "inside R3" is wrong; the ratified partition puts it in R2, 599 s short of the boundary. The `0/747` orb reading is consistent with the banked ladder and no collision exists. | charter correction | gandalf |
| **F-G8-7** | **Primordian max life = 14,812 (measured).** Pins the net life modifier at −36.000 % ± 0.004 pp *without* assuming the save's `15822` is life+mana — and then confirms that split as a consequence (residual 1,010 vs bio mana 1,009.74). The §14.11 composition question is closed at the hero/quest tier. | **run-level, unblocks the HP-composition gate** | legolas / gandalf |
| **F-G8-8** | **A second tier is measured: Thundersnout ~ Thundering, champion, level 10, max life 4,702.** Plus six unattributed trash maxima (58, 326×2, 434, 649, 813, 1,820). Whether 4,702 falls out of a champion bio under the same 0.640 multiplier is a `.dbr` question and is handed over, not answered. | evidence supply | legolas |
| **F-G8-9** | The client is running with **monster health rendered as numerals** over every damaged monster. This is a standing instrument, not a one-frame accident: any future capture pass can harvest monster HP directly. | instrument availability | galadriel / gandalf |

---

## §9 — Artifacts

All under `agentic_orchestration/galadriel/captures/2026-07-28-kitcal1-g8/`:

| Artifact | Contents |
|---|---|
| `g8-panel-all.json` | calibrated panel read, all 313 frames, 313 × `status=OK` |
| `g8-panel-265-300.json` | the death neighbourhood at full field detail |
| `g8-orbs-all.json` | both-orb sweep, all 313 frames (100 clean HP reads; mana abstained — F-G8-2) |
| `g8-bossbar.json` | nameplate-bar detection + fill fraction, 13 frames |
| `g8-monhp-candidates.json` | in-world numeric-HP band detection, all 313 frames — 161 bands over 88 frames |
| `bossbar-f<id>.png` ×13 | 2× nameplate strips |
| `g8-monhp-sheet-{0,1,2}.png` | 4× contact sheets of all 49 bands in the health-readout geometric envelope |
| `monhp-verify/f<id>-<k>.png` | **8× crops of the ten confirmed monster-HP readouts** |
| `f281-*.png` | the frame-281 evidence set (panel, rows, dps, skills, counts, orbs, nameplate, level, tag, boss bar, monster HP, debug overlay) |
| `panelfoot-f182/216/288.png` | the F-G8-3 evidence |
| *(gitignored, regenerable)* | `g8-sheet-270-295.png` (26-frame neighbourhood sheet), `f281-full-half.png`, `f281-center.png`, `f87-half.png`, `monhp-candidates/` — see the directory's `.gitignore` |

Pipeline, all new this pass, under
`agentic_orchestration/galadriel/pipeline/gd-playtest-v1/`: `g8_orbs.py`, `g8_monhp.py`,
`g8_monhp_filter.py` (superseded — see §6.1), `g8_monhp_sheets.py`, `g8_bossbar.py`.
`panel_ocr.py`, `globe_ocr.py` and `g6_panel_stills.py` were reused **unmodified**.

---

**The Mirror, briefly.** He is standing still at zero out of seven hundred and forty-seven, and the
thing that killed him has lost eight percent. The frame he took to record his own death recorded
the monster's constitution instead — fourteen thousand eight hundred and twelve, a number nobody
could get out of the save, sitting in plain sight above the body. The scoreboard was open because
he wanted to see what he had done. What it shows is what was done to him, and the arithmetic of
why.
