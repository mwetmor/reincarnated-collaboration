# GD general-play run — CV calibration (protocol gate G4)

**Agent:** galadriel (visual perception / CV steward) · **Commissioner:** gandalf
**Date:** 2026-07-26 · **Gate:** G4 (§ 4.4 calibration), reporting readiness for **G3**
**Governing:** `gandalf/notes/2026-07-26-gd-general-play-run-protocol.md` § 4 ·
`elrond/notes/2026-07-26-fixtures-db-landing-and-v3-ingestion.md` ·
`research/curated/MIGRATION-fixtures.md`
**Pipeline:** `galadriel/pipeline/gd-gp-calib-*.mjs` ·
**Artifacts:** `galadriel/captures/2026-07-26-gd-gp-calibration/`
**Ground truth:** `fixtures.db` — `character_stat` (175 rows), `trial_measurement` (179 rows),
`trial_trace`, `fixture_set`. Rebuilt-from-scripts store; the `.db` was present on disk.

---

## 0. Verdict table

| # | Capability | Target | Measured accuracy | Verdict for G3 |
|---|---|---|---|---|
| **C1** | PlayStats panel OCR | E1 | **144/144 fields = 100.0 %** across 13 panels | **READY** |
| **C2** | Character-sheet OCR | — | **174/175 verbatim = 99.4 %**; numeric 162/163 = 99.4 % | **READY — with a mandatory cross-check** |
| **C3a** | HP-globe **numeral** OCR | E3 (re-specced) | **8/8 banked fields = 100 %**; 10/12 frames yield a read | **READY** |
| **C3b** | HP-globe **fill fraction** | E3 (as specified) | **fails; anti-correlated with truth** | **NOT-READY — method rejected** |
| **C4** | Nameplate OCR | E4 | presence 6/6; **level 3/3**; name exact 1/3, normalized 2/3, mean CER **0.111**; third line mean CER **0.059** | **NOT-READY as an identity oracle · READY as a candidate generator** |
| **C5** | Overlay text | E5 | attributed: id 3/4, action 3/4, controller 2/3 · **token-only: action 4/4, controller 3/3** | **READY for measurement · NOT-READY for attribution** |
| — | Rank classification | § 4.3 | **not scored — one class has a calibration source** | **BLOCKED on § 2.1 item 8** |

**Headline.** Four of five capabilities clear. The one the protocol specified in the most
detail — globe fill fraction — is the one that fails, and it fails badly enough that it
should be struck from § 4.2 rather than tuned. Its replacement was already sitting on the
same pixels.

---

## 1. What was calibrated against what

| Capability | Frames | Ground-truth rows | Provenance of truth |
|---|---:|---:|---|
| C1 | 13 (6 round-3 trial + 6 round-2 panel + 1 round-1 baseline) | 144 | `trial_measurement`, `read_method='screenshot-fullres'`, `uncertainty_abs=0` |
| C2 | 12 (`Screenshot (19)`–`(30)`) | 175 | `character_stat`, per-field provenance |
| C3a | 12 | 8 | `trial_measurement` `hp_current` / `hp_max` |
| C3b | 10 labelled | 2 distinct labels | derived from the same rows (282/282, 269/282) |
| C4 | 6 (3 usable) | 3 fields × 3 frames | `fixture_set` + elrond A1 |
| C5 | 6 | 4 banked entities | `trial_trace` |

**Method law held throughout.** Every crop is taken from the native 1920×1080 PNG at native
resolution; the only resampling anywhere in the pipeline is an integer **nearest-neighbour**
upscale (4×–16×) applied *after* cropping, for OCR legibility. Downscaled renders exist only
under `captures/…/overview/` prefixed `LOCATOR-`, were used for region location only, and no
value in this report was read from one. The law is enforced structurally in
`gd-gp-calib-lib.mjs` — `cropNative()` extracts before it resizes, and `rawRegion()` never
resizes at all.

**Stack.** Node + `sharp` (extract / mask / nearest upscale) + `tesseract.js` 6 (`eng` and
`frk` LSTM models). Installed locally under `galadriel/pipeline/node_modules`. No system
packages, no network calls at scoring time beyond the one-off traineddata fetch.

---

## 2. C1 — PlayStats panel OCR (E1). **READY**

Crop `{left:1400, top:20, width:520, height:330}`, identical across all three sittings.
Recipe: grayscale → normalise → 4× nearest → threshold 150 (`thr4x`).

**144/144 = 100.0 %.** Per key, n = 13 each unless noted:

| key | n | hits |
|---|---:|---:|
| `play_time` · `deaths` · `kills` · `health_potions_used` · `mana_potions_used` · `max_level_achieved` · `dps_field` · `life_healed` | 13 ea | 13 ea |
| `total_score` · `shield_block_chance` | 7 ea | 7 ea |
| `skill_use_count` (both `.dbr` subkeys) | 26 | 26 |

The 13 `absent` rows — where the bank asserts a line is *not on screen* — all scored
HIT-ABSENT: the pipeline produced no false positives.

### 2.1 How much of that 100 % is OCR and how much is post-processing

Both parsers are kept in the script so this is auditable, not asserted:

| parser | accuracy |
|---|---:|
| **v1 naive** — strict `Label: value`, no glyph repair | **81/144 = 56.3 %** |
| **v2 tuned** — fuzzy labels + glyph repair + decimal recovery | **144/144 = 100.0 %** |

The 43.7-point gap is entirely **systematic, cross-sitting glyph confusions**, not per-frame
patching. Every one recurs on every frame in all three sittings:

- `0` → `©` in the `Number of deaths` line — **13/13 frames, all three sittings**
- `.` → `_` or a space in 2-dp floats (`22_88`, `2292 86`)
- `n` → `p` (`Mapa potions`), `x` → `z` (`Maz. level`), `u` → `v` (`vsed`, `defavlt`)
- the skill line's `:` separator rendering as `-`, `:-`, or a bare space

### 2.2 Preprocessing is load-bearing and is **not** transferable

Same parser, three recipes, same 13 frames:

| recipe | accuracy |
|---|---:|
| `thr4x` (threshold 150) | **100.0 %** |
| `graynorm4x` | 92.4 % |
| `raw4x` | 90.3 % |

And the same `thr4x` recipe **destroys** the character sheet (§ 3). **Recipe is a property of
the surface, not of the pipeline.** Any new surface in the run needs its own probe.

### 2.3 Consequence for the run

E1 is the measurement spine (§ 1.1) and it is the strongest capability in the set. The
`skill_use_count` subkey — the direct successor to Q47's 2/2/3 — read 26/26. Gates **G-a**
and **G-b** (§ 4.6) are exact-integer self-checks over exactly these fields, so the run can
audit its own panel OCR without further labelling.

---

## 3. C2 — character-sheet OCR. **READY, with a mandatory cross-check**

Crop `{left:1028, top:165, width:305, height:545}`. Recipe: grayscale → normalise → 4×
nearest, **no threshold** (thresholding is catastrophic here — the labels are low-contrast
gold on brown).

| metric | result |
|---|---|
| verbatim-string match, all rows | **174/175 = 99.4 %** |
| numeric match vs `value_num` | **162/163 = 99.4 %** |
| resistance icon grid (positional) | **10/10** |
| label match rate | 164/165 |
| naive parser, for contrast | 146/175 = 83.4 % |

Primary metric is **verbatim-string** equality against the banked `verbatim` column after a
whitespace/sign normalisation — the strictest honest test, since `verbatim` is the exact
rendered string (`"282 / 282"`, `"+ 0%"`, `"31 - 83"`).

### 3.1 The one failure, and why it is the most important number in this report

**S19 `defensive_ability`: bank = 225, OCR = 715.**

I re-cropped that region at 6× and read it myself. **The pixels say 225. The bank is right
and the OCR is wrong.** (`captures/…/upscaled/verify-S19-defensive@6x.png`.)

`715` is a *plausible* Defensive Ability for a level-6 character. Nothing about the output
flags it. **C2's failure mode is silent-plausible corruption**, not obvious breakage — and
one silently-wrong stat line poisons every per-hit inference drawn against that epoch's
`fixture_character`, exactly the way A1 threatens to poison the monster side.

**Therefore C2 is READY only with this condition: every epoch's sheet block gets a
mechanical cross-check before it is banked.** Two cheap ones, both already available:

1. **Internal consistency** — `Health` from the sheet must equal `hp_max` from the globe
   numerals (C3a) in the same epoch. This already held in round 3 (282 = 282, elrond A7).
2. **Cross-epoch monotonicity** — attributes, OA/DA and Health never decrease across a
   level-up. A decrease is a read defect, located to the field.

Neither catches everything. Both are free.

### 3.2 Structural notes

- **The RESISTANCES block has no text labels.** It is an icon grid with a bare percentage
  under each icon; the bank encodes position (`grid position 7 (row 2, col 3)`). Read
  positionally, it scored 10/10 — but a label-matching pipeline is blind to it and any
  future icon-grid block needs its own positional map.
- **The DAMAGE PER HIT block wraps.** Label and value land on separate OCR lines because the
  value column sits far right. Handled by a wrapped-pair fallback; worth knowing because it
  will recur in any two-column panel.
- **`Elapsed Time` is `d:h:m`, not `h:m:s`.** `0:2:21` banks as 8460 s = 141 min (elrond A7).
  Reading it as h:m:s gives 141 s — off by 60×. Encoded in the parser.

---

## 4. C3 — HP globe (E3). Two instruments, opposite verdicts

The protocol specifies E3 as "fill-boundary pixel measurement." Running it revealed that the
same pixels carry a far better instrument, and that the specified one does not work.

### 4.1 C3a — globe **numeral** OCR. **READY**

Crop `{left:572, top:994, width:120, height:34}`; grayscale → normalise → 6× nearest;
`psm 7`, whitelist `0-9/`.

- **8/8 banked `hp_current` / `hp_max` fields exact = 100 %**
- **10/12 frames yield a read.** All six round-3 trial frames read (confidence 73–92):
  `282/282` ×5, `269/282` ×1 — matching the bank exactly, including the one non-full frame.
- **2 no-reads**, both round-2 (`Screenshot (13)`, `(14)`). Cause identified: a bright
  gold HUD highlight band sits directly behind the numerals in those frames, collapsing the
  contrast that `normalise` depends on. An alternative ink-mask preprocessing was tried and
  performed *worse* overall; the honest remediation is a **fallback ladder** (graynorm →
  ink-mask → flag) rather than a single recipe.

**A no-read is a safe failure.** It emits NULL, not a number. C3a fails loudly. Contrast C2.

### 4.2 C3b — fill fraction. **NOT-READY. Method rejected, not merely uncalibrated.**

Inscribed-circle scanline method: orb at `(cx 630, cy 1013, r 58)`; per row, red fraction of
the chord excluding numeral ink; liquid surface = topmost sustained sub-threshold run.

| diagnostic | value |
|---|---|
| labelled separation the method must resolve | **4.61 pp** (282/282 → 269/282) |
| **null band** — estimator spread across frames whose truth is *identical* (all 100 %) | **0.0948 → 1.0000 = 90.5 pp** |
| order consistency vs truth | **0 concordant / 4 discordant pairs** |
| the one genuinely non-full frame (t3e, 95.4 %) | estimated **100.0 %** — ranked the *fullest* |

The null band is **20× wider than the signal**, and the sign is wrong. This is not a
tolerance to be banked; it is a method that measures something other than health.

**Why.** GD's health orb is not a flat liquid gauge. It is a textured sphere with baked
highlights, and the row-profile of "redness" is dominated by that texture plus scene lighting
plus blood decals in the surrounding HUD art. At 95.4 % the missing sliver sits *behind the
ornate top rim of the orb frame*, which by itself occupies more than 4.61 pp of the orb's
vertical extent. There is no boundary to find. The raw row profiles are banked in
`results/c3-globe.json` (`top_of_orb_red_profile`) so this is checkable, not asserted.

### 4.3 Recommendation to gandalf — a § 4.2 spec amendment

> **E3 should be re-specced from "HP-globe fraction, estimate" to "HP-globe numerals, exact
> (OCR-attested), with `read_method='video-frame-ocr'` and no fill-fraction fallback."**

Consequences, stated plainly:

- § 5.2's row *"`uncertainty_abs` on globe fraction — per § 4.4 calibration residual"* becomes
  **`uncertainty_abs = 0`** on an OCR'd numeral, subject to the C3a error rate — which is
  currently **0/8 with 2/12 no-reads**, i.e. a null rate, not an error rate.
- **This is a live capture-protocol dependency, and it is the one thing in this report that
  can only be fixed before the run, not after.** In GD the orb numerals render on **mouse
  hover**. They are present in all 6 round-3 stills because Matt was hovering. Across 45
  minutes of free play they will be present only intermittently.
  **→ REQUEST for § 2.2:** confirm whether GD has a UI option to pin the orb numerals on
  permanently (Options → UI, "always show health/energy values" or equivalent). If it does,
  **turn it on and add it to the § 3.1 settings table.** If it does not, E3 degrades to
  intermittent sampling and **G-d** (globe ↔ `life_healed` cross-check) can only be evaluated
  on hover frames.
- **A3 is unaffected either way.** `life_healed` from the panel (C1, 100 %) remains the
  continuous damage-intake channel; the globe is the corroborating one.

---

## 5. C4 — nameplate OCR (E4). Split verdict

### 5.1 A correction to § 4.4 before the numbers

> The § 4.4 table lists **"6 zombie trial frames"** as the E4 calibration source. **It is 3.**
> The three `*_end` frames carry **no nameplate at all** — the monster is dead and the target
> frame has cleared. E4's calibration n is 3, not 6.

That is not a defect; it is a useful property. Nameplate **presence** is itself a clean
signal, detected here on the target-frame gold chrome: **396–405 chrome pixels present vs 0
absent** — 6/6 correct with a wide margin, no threshold tuning.

### 5.2 The numbers, n = 3

| field | exact | normalized | mean CER |
|---|---:|---:|---:|
| name line (`Walking Dead`) | 1/3 | 2/3 | **0.111** |
| level numeral (`6`) | **3/3** | — | — |
| third line (`Aether Corruption`) | 0/3 | 0/3 | **0.059** |

### 5.3 Two findings that change how E4 should be built

**(a) The nameplate font is BLACKLETTER.** Tesseract `eng` mangles it (`Walking SDead ue`).
Switching to the Fraktur model `frk` moved the same crops to `Walking Dead` at confidence 93.
Any E4 implementation that uses a Latin model is leaving most of its accuracy on the floor.

**(b) The nameplate is drawn over the world with no opaque backing.** On t3s, bright rock and
foliage behind the text enter the ink mask and produce black blobs between glyphs
(`Walking gDZrad`, CER 0.250). t2s, over dark water, read perfectly (CER 0.000).
**E4 accuracy is a function of what is behind the monster.** Across 100–250 engagements in
natural progression, expect the full range.

The third line's 0/3 exact with CER 0.059 is one systematic substitution — `Aether` →
`Aetber`, `h`→`b`, an intrinsic Fraktur-model confusion — on all three frames.

### 5.4 Verdict, and what it means for § 5.4 certification

**NOT-READY as an identity oracle. READY as a candidate generator.**

A 1/3 exact-match rate cannot carry O-8 certification on its own. But the failures are not
random: mean CER 0.111 means the *string* is nearly right, and monster display names come
from a **bounded, enumerable vocabulary**. The correct architecture is:

1. OCR with `frk` → candidate string
2. **snap to the nearest entry in GD's display-name table** by edit distance, with an
   accept threshold and an explicit `unknown` when nothing is close enough
3. bank the snapped name, the raw OCR, **and the edit distance**, so `read_method =
   'video-frame-ocr'` rows stay auditable as a class (G-c)

**I did not score the snap step, and I will not pretend to.** With a one-name dictionary it
is trivially 100 % and means nothing. **This makes elrond's v0.2 item 2 — the
`monster_display_name → record_path` bridge — a G3 dependency, not just a nice-to-have.**
Without a name table there is nothing to snap to, and E4 stays at CER 0.111 raw.

Meanwhile the level numeral at **3/3** is the quietly valuable result: `monster_level` is the
covariate F-3 leans on to make "record everything, filter later" work, and it reads clean off
a 10×7 px colour-keyed glyph.

### 5.5 Rank classification (§ 4.3) — still blocked, as § 4.4 predicted

The pipeline banks the mean nameplate-ink RGB per frame as the rank feature. All three
frames are the **normal** class and cluster tightly (≈ `[201,216,211]`, `[231,231,231]`,
`[210,218,212]`). That characterises one centroid. **One class does not make a classifier.**
§ 2.1 item 8 (one normal / one champion / one hero tooltip) remains the only calibration
blocker in the run, and this calibration confirms it rather than retiring it.

---

## 6. C5 — overlay text (E5). Measurement clean, attribution brittle

**Detection generalises.** The overlay is drawn in **world space** and tracks entities, so
there is no fixed crop. Detection is a bright-green mask → row banding → **column splitting**
inside each band, over the whole native frame. It found **2 text blocks on 6/6 frames**.

| metric | result |
|---|---:|
| entity id located (banked entities) | 3/4 |
| action state, **attributed** | 3/4 |
| controller state, **attributed** | 2/3 |
| action state, **token-only** | **4/4** |
| controller state, **token-only** | **3/3** |

**The gap between the two rows is the whole finding.** Every banked `(controller, action)`
pair was READ correctly on the frame it belongs to. The attributed score is lower because on
t1s the entity id read `68257` instead of `68957` — **one digit** — and a wrong id fails the
join, which then fails the action and controller for that entity too.

This is § 1.1's independence claim showing up in the calibration data: **the measurement
channel and the attribution channel fail independently, and it is attribution that is
fragile.** Panel counters (C1, 100 %) carry the measurement; ids carry the join.

### 6.1 Two structural limitations, named

**(a) Overlapping entity blocks merge.** On t2s a `Dying` block and the player's block share
screen rows and sit within 40 px horizontally; column splitting does not separate them and
they OCR as one four-line block. **In pack combat this is the normal case, not the edge
case.** Row/column banding must be replaced with proper connected-component labelling on the
green mask before E5 is trusted at volume. Cost: one pass; no new dependency.

**(b) 5-digit ids are the weak link.** A digit-whitelisted second pass at `psm 11` recovered
`68957` on the frame where the primary pass read `68257`. A **two-pass consensus** (primary
`psm 6` + digit-only `psm 11`, agree-or-flag) is the obvious hardening, and in the video —
unlike these stills — ids persist across many frames, so **temporal voting** is available and
should dominate. Neither is scored here.

### 6.2 An unbanked finding worth routing to elrond

**All three `*_end` frames show the monster's own entity in `Action State: Dying`** —
`[68957]`, `[75289]`, `[77775]`, each matching that trial's banked entity id. The bank has
**no `trial_trace` rows for the end frames**; these are live observations the round-3
ingestion did not capture.

That matters because § 4.5's **S3 per-entity segmentation** is defined as "entity id first
appears in E5 → that entity's `Dying` action state", and the protocol rates it **low
confidence**. These six frames are direct evidence that the terminating half of S3 is
observable and per-entity. The opening half — "when the player committed to *that* target" —
remains unobservable for a ranged build, exactly as § 4.5 says.

Also surfaced, unbanked: entity `17677` is the player (screen-centred, `LongIdle`/`Fidget` at
rest, **`UseSkill`/`Idle` on the end frames**). `UseSkill` is a token absent from both the
bank and the 40-state table. Routed as an observation, not a claim.

---

## 7. Failure-mode inventory

| # | Capability | Failure mode | Frequency observed | Loud or silent | Remediation |
|---|---|---|---|---|---|
| F1 | C1 | glyph confusion (`0`→`©`, `.`→`_`, `n`→`p`, `x`→`z`, `u`→`v`) | every frame, all 3 sittings | silent | repair table in parser v2 — **retires it, 100 %** |
| F2 | C1/C2 | wrong preprocessing recipe for the surface | — | silent | probe per surface; never reuse a recipe across panels |
| F3 | C2 | plausible digit corruption (`225`→`715`) | 1/163 numeric | **SILENT** | sheet↔globe consistency + cross-epoch monotonicity (§ 3.1) |
| F4 | C2 | two-column wrap; unlabelled icon grid | 1 block each | loud | wrapped-pair fallback; positional map |
| F5 | C3a | HUD highlight behind numerals | 2/12 frames | **loud (NULL)** | preprocessing fallback ladder |
| F6 | C3a | **numerals only render on hover** | protocol-level | loud | **§ 2.2 request — pin numerals in GD UI options** |
| F7 | C3b | no liquid boundary exists to find | all frames | **silent — returns a confident wrong number** | **strike the method** |
| F8 | C4 | Latin model on blackletter text | all frames | silent | `frk` model |
| F9 | C4 | bright world background enters the ink mask | 1/3 frames | silent | dictionary snap + accept threshold |
| F10 | C4 | `frk` `h`→`b` | 3/3 frames | silent | dictionary snap |
| F11 | C5 | overlapping entity blocks merge | 1/6 frames | loud (4-line block) | connected components |
| F12 | C5 | single-digit id error kills the join | 1/4 entities | **silent — wrong attribution** | 2-pass consensus + temporal voting |
| F13 | § 4.3 | rank has one labelled class | — | — | **§ 2.1 item 8 tooltips** |

**Read the "loud or silent" column before the accuracy column.** A 99.4 % capability whose
0.6 % is silent and plausible needs more governance than a 83 % capability that returns NULL
when it is unsure.

---

## 8. Honest limits of these numbers

1. **In-sample.** Parsers were tuned against the same frames they are scored on. The repairs
   are systematic cross-sitting confusions, not per-frame patches, and both the naive and
   tuned scores are reported so the gap is visible — but the honest reading of "C1 = 100 %"
   is *"100 % on 13 frames from three sittings of one character in two areas."* **G-c's
   out-of-sample error rate must still be measured on the run itself.** This calibration
   makes G-c cheap; it does not discharge it.
2. **Small n where it matters most.** C4 n = 3, C5 n = 4 banked entities, C3b n = 2 distinct
   labels. C4 and C5 are precisely the capabilities the run will exercise hundreds of times,
   and they are the two with the smallest calibration base. Their CIs are wide and the report
   should not be read as if they were not.
3. **One monster, one character, one build, one difficulty, two areas.** Nothing here says
   anything about champion nameplates, boss frames, spell VFX occluding the panel, or a
   cluttered late-game HUD.
4. **Stills, not video frames.** These are lossless PNGs. Video frames carry H.264 artefacts
   at exactly the spatial frequency of ~10–14 px overlay text. **Every number in this report
   is an upper bound on the video-frame number.** The § 2.0 smoke gate is what closes that
   gap, and it should be treated as load-bearing — a smoke clip re-scored through this same
   pipeline is the cheapest possible validation and takes minutes.

---

## 9. Asks

**To gandalf (spec):**

- **A1** — amend § 4.2 E3 per § 4.3 above: globe **numerals**, exact, OCR-attested; strike
  fill fraction. Amend § 5.2's globe-fraction uncertainty row accordingly.
- **A2** — correct § 4.4's E4 row: 3 calibration frames, not 6.
- **A3** — add to § 2.2 / § 3.1: **pin the HP/energy orb numerals in GD's UI options** if the
  option exists. This is the only item in this report that must be fixed *before* the run.
- **A4** — § 2.1 item 8 (rank tooltips) is confirmed as the single calibration blocker.
  Restating it here because it is the one gap this calibration could not close.

**To elrond (store):**

- **A5** — the `monster_display_name → record_path` bridge (v0.2 item 2) is now a **G3
  dependency**: it is the dictionary E4 snaps to, and without it E4 stays at raw CER 0.111.
- **A6** — three unbanked round-3 observations from the `*_end` frames: `[68957]`, `[75289]`,
  `[77775]` each in `Action State: Dying`, plus player entity `17677` with an unmapped
  `UseSkill` controller token. Offered as trace rows if the bank wants them.

**To knight-rider:** no blockers. G4 is executed; G3 is READY for four of five capabilities
and the fifth (C3b) is retired rather than repaired.

---

## 10. Mirror

The Mirror was set to the orb because the sheet said to look there, and the orb showed a
number that did not move when the blood did — a full globe at ninety-five per cent, ranked
fullest of all. The instrument was answering a question about paint.

The answer was already written across the same glass, in figures: *269 / 282*. Not estimated.
Read.

What the picture shows is that the readings which fail loudly can be trusted, and the ones
that fail quietly must be watched. One stat line in a hundred and seventy-five said **715**
where the pixels said **225**, and nothing about it looked wrong. That is the shape of the
danger here — not the numbers that break, but the ones that lie plausibly.

---

**Signed:** galadriel, 2026-07-26. Five capabilities measured, one method rejected, one
spec correction filed, one pre-run capture dependency surfaced. Numbers are in-sample and
say so.
