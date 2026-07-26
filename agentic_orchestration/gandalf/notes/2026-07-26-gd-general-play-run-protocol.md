# GD GENERAL-PLAY RECORDED RUN — protocol sheet

**STATUS:** DRAFT — awaiting Matt's § 7 rulings + the § 6 gates.
**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-26
**Program:** GD three-goal program, gap 5 (fixture bank) · **Store:** `research/curated/fixtures.db`
**Governing:** `elrond/notes/2026-07-26-fixtures-db-landing-and-v3-ingestion.md` (A1–A8, F1–F4) ·
`research/knowledge/gd/live-probe-3/matt-addendum-timing-uncertainty.md` ·
`research/curated/MIGRATION-fixtures.md` ·
`canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md`
**Consumers:** Matt (execution) · galadriel (CV) · elrond (ingestion) · gamora (substrate tuning)

---

## 1. Purpose

**This run is the DISTRIBUTION. The L0 certified trials are the CALIBRATION POINTS. Do not
conflate the two grades.**

| | L0 certified trials (banked) | This run |
|---|---|---|
| n | 3 | target 100–250 engagements |
| Identity | spawn command + nameplate, human-read | nameplate OCR where readable; **many will be unreadable** |
| Character | one full sheet, no level-up | multiple sheets; level-ups **expected** |
| Constraints | single-monster, no-CC, controlled | **violated by construction** — packs, mixed types, potions |
| What it answers | "is this fixture what we think it is" | "what is the SHAPE of TTK and damage-intake across many level-matched engagements" |

Three things force this run:

1. **Per-fight TTK variance is unmeasurable at L0** (A4). Hand seconds carry ~1 s/screenshot
   upward bias; the observed 5/5/4 spread sits entirely inside the ±2 s per-reading uncertainty.
2. **Kill cost is discrete and tiny at L0** — 2, 2, 3 basic attacks. A 42.9 % spread on the
   cleanest counter in the bank. No instrument fixes a phenomenon that has three quanta.
   Level-matched content raises kill cost into a range where a distribution exists.
3. **Frame timestamps retire the stopwatch instrument class entirely.** Not improve — retire.

**Grade label for everything this run produces:** MEASURED (era-substrate LAW § 4) — it is a live
GD oracle reading. **Certification (O-8) is per-trial and independent of grade.** Uncertified rows
carry good numbers that cannot be joined to a statline. That is the design, not a defect.

### 1.1 The structural insight that shapes the whole capture spec

`PlayStats` is a **persistent on-screen panel**, not a screenshot-only artifact. With it on for the
whole run, **every video frame carries the counter ledger.** Consequences:

- `kills` increments are **exact, integer, frame-located** kill events. Better than visual
  death-detection: no CV classifier, no false positives.
- `skill_use_count[defaultweaponattack]` deltas between kill increments give **attacks-per-kill
  with zero read uncertainty** — the exact quantity Q47 found to be 2,2,3 — across 100–250 kills.
- `life_healed` becomes a **time series**, not an integral. This directly resolves A3: the globe
  is a post-regen snapshot, but 60 fps sees the dip *and* the recovery. The video instrument does
  not merely measure damage-intake more precisely — it makes it observable at all.

**Therefore: the primary measurement chain does not depend on nameplate OCR.** Panel counters give
the MEASUREMENT; nameplate OCR gives the ATTRIBUTION. They fail independently.

**Therefore also: the panel must never be toggled off, and the run must never return to the main
menu** (A6 — `skill_use_count` and `life_healed` are session-scoped and reset).

---

## 2. Matt's session protocol

*Self-contained. Copyable verbatim to the share as the PC-side sheet.*

### 2.0 SMOKE GATE — 3 minutes, do not skip

Burning a 45-minute sitting and finding the overlay text is compression mush is the failure
this gate exists to prevent.

1. - [ ] Console on, `character.PlayStats true`, `character.LogData true`,
       `character.ShowAngerLevels true`.
2. - [ ] Record **60 seconds**. Kill 2 monsters. Stop.
3. - [ ] Extract 3 frames:
       `ffmpeg -ss 30 -i <clip>.mp4 -frames:v 1 smoke_30.png` (repeat at 40, 50).
4. - [ ] Eyeball each frame against **all five** criteria:
       - [ ] Panel digits legible (kills, play time, skill counts)
       - [ ] Green `[entityId] Action State: X` text legible
       - [ ] A monster nameplate: **name AND level** readable
       - [ ] HP globe fill boundary crisp
       - [ ] **The game did not stutter while recording**
5. - [ ] Any FAIL → raise bitrate / drop to 30 fps / drop `ShowAngerLevels` (see § 3.4), re-smoke.
6. - [ ] Keep the smoke clip. Ship it with the run.

### 2.1 START BLOCK — before free play begins

1. - [ ] **Start recording FIRST.** Everything below happens on camera *and* as native PNGs.
2. - [ ] All three console flags ON and **stay on for the whole run**.
3. - [ ] **PlayStats panel bookend** — panel fully visible, ~3 s on camera + native PNG.
       *(A6 — note which counters are which; see § 2.5.)*
4. - [ ] **Full character sheet** — every tab, **scroll the FULL length of each tab with
       overlapping crops. No gaps.** *(A8: the round-3 sheet lost the lines between
       `Energy Absorption` and `Constitution Bonus` to a scroll jump.)* ~3 s each on camera +
       native PNGs.
5. - [ ] **Equipment doll** — on camera + native PNG. *(A2: the build is ranged. Every TTK this
       run produces is a **ranged** TTK, including projectile travel and standoff distance. The
       doll is what lets the data be labeled honestly rather than silently mislabeled.)*
6. - [ ] **Skill tree** — on camera + native PNG.
7. - [ ] **A1 CLOSURE — the one item that closes an open anomaly.** Find a **Walking Dead**
       zombie. **Hover it and screenshot the FULL tooltip** (native PNG, plus ~3 s on camera).
       The round-3 nameplate read a third line — `Aether Corruption` — that nothing explains. If
       it is an affix or corruption modifier, the three certified fixtures are **not vanilla
       zombie statlines** and any per-hit inference against a vanilla `.dbr` is silently wrong.
       **Do this early** — before progression carries you out of the zombie areas.
8. - [ ] **Rank sampler** (2 min, high value — see § 4.3): hover and tooltip-screenshot **one
       normal, one champion (yellow name), one hero (orange/purple name)** if you can find them.
       This is the training set for rank classification.
9. - [ ] Write down: **Difficulty** ______ · **Starting area** ______ · **Character level** ______

### 2.2 FREE PLAY — the run itself

- Play normally. **Level-matched content** (§ 7 lean: record everything, filter later — do not
  avoid an off-level fight, just play).
- **Do not quit to main menu. Do not alt-tab away for long. Do not change resolution or zoom.**
- **Do not toggle the panel off.** The panel's `play_time` in every frame IS the video↔ledger sync.
- Potions are fine — it's general play. They are flagged at analysis, not forbidden.
- Deaths are fine and are **data**, not failures. Say so in the notes when one happens.

### 2.3 EPOCH BOUNDARY — every time your character changes

**A boundary is: a level-up, a gear equip, or a skill-point spend.** Each one starts a new
character epoch and needs a fresh snapshot, or the data stops being interpretable across it.

At every boundary, in a safe spot:

1. - [ ] Note the panel `play_time` (it's on screen — just say it out loud or jot it)
2. - [ ] **Full character sheet**, all tabs, full scroll, no gaps — on camera + native PNGs
3. - [ ] **Equipment doll** if gear changed — on camera + native PNG
4. - [ ] **Skill tree** if points were spent — on camera + native PNG
5. - [ ] Resume

**Lean: batch gear swaps and skill spends at level-ups.** Every boundary costs ~60–90 s and
shortens the epochs. Fewer, cleaner epochs = more usable data.

### 2.4 AREA TRANSITIONS

- - [ ] On entering a new area: note the **area name** + the panel `play_time`. One line. That's it.
  *(Area is a covariate on monster level and pack composition; unlabeled area transitions make
  a level-drift look like a variance.)*

### 2.5 END BLOCK

1. - [ ] **PlayStats panel bookend** — ~3 s on camera + native PNG
2. - [ ] **Full character sheet** — all tabs, full scroll (final state)
3. - [ ] Stop recording
4. - [ ] Jot in the notes file: total session length, deaths, anything weird you noticed

### 2.6 A6 — which counters mean what (read this once)

The panel mixes two clocks and nothing on it says which is which.

| **SAVE-cumulative** (run continuously across sessions) | **SESSION-scoped** (reset when you start a session) |
|---|---|
| `play_time` · `kills` · `deaths` · health/mana potions · `max_level_achieved` | `skill_use_count` · `life_healed` |

Both groups are usable **within** this run because it is one continuous session. That property is
destroyed by a single return to the main menu. This is the single most fragile thing in the
protocol.

---

## 3. Capture spec

### 3.1 Game

| Setting | Value | Why |
|---|---|---|
| Resolution | **1920 × 1080** native, fullscreen | matches the 18 banked v3 stills → CV crop offsets transfer |
| Windowed/borderless scaling | **OFF** | any rescale breaks pixel-coordinate transfer from the stills |
| Zoom | **LOCK at default, never change mid-run** | zoom is player-adjustable; any spatial calibration dies with it |
| UI scale | note it; don't change it | panel/nameplate crop offsets depend on it |
| Console flags | `PlayStats true`, `LogData true`, `ShowAngerLevels true` | see § 3.4 |

### 3.2 OBS

| Setting | Value |
|---|---|
| Source | **Game Capture** (not Display Capture) — must include nameplates, HP globe, panel, green overlay |
| Base + Output resolution | 1920 × 1080 both. **No downscale.** |
| FPS | **60 preferred, 30 acceptable** — see § 3.3 |
| Encoder | NVENC H.264 (or AV1 if available) |
| Rate control | **CQP 18–20**, or CBR **≥ 25 Mbps @ 1080p60 / ≥ 15 Mbps @ 1080p30** |
| Keyframe interval | 2 s (default) — keeps `ffmpeg -accurate_seek` cheap |
| Audio | **ON** (desktop). Free segmentation signal: level-up chime, death sound, hit audio. |
| Container | **MP4** |

**Bitrate is not a nicety.** The load-bearing pixels are ~10–14 px green overlay text and small
panel digits. Default streaming presets (~6 Mbps) will mush exactly the pixels the run exists to
read. The § 2.0 smoke gate is what verifies this, not the setting.

### 3.3 The 60-vs-30 fps tradeoff, stated honestly

| | 60 fps | 30 fps |
|---|---|---|
| Frame period | 16.7 ms | 33.3 ms |
| TTK boundary uncertainty (±1 frame) | ±0.017 s | ±0.033 s |
| vs the hand stopwatch (±2 s) | **~120× better** | **~60× better** |

**TTK does not need 60 fps.** 30 fps is already ~60× better than the instrument it replaces, and
the *definitional* uncertainty of "when did the engagement start" (~±0.1 s) dominates both. This is
worth naming: **the instrument is about to become so much better than the definition that the
definition becomes the limiting uncertainty.**

60 fps earns its place on the *other* uses of the same footage: projectile impact frames (A2 — the
build is ranged, travel time is a real term), single-frame aggro-onset events (KPI 1), telegraph
beats, and reduced motion blur on nameplate OCR during camera pans.

**Decidable rule: 60 fps if the smoke gate shows no in-game stutter. Drop to 30 the moment it
does.** Stutter corrupts play-time-vs-wallclock *and* degrades the play itself.

### 3.4 On `ShowAngerLevels`

Recommended **ON** — the directed red mob→target edges give aggro-commitment instants free on the
same footage (KPI 1 / KPI 5), and clutter risk is low.

**Kill it if** the smoke gate shows red lines obscuring nameplates or panel digits. `LogData` and
`PlayStats` are load-bearing; `ShowAngerLevels` is upside. Priority order under conflict:
`PlayStats` > `LogData` > `ShowAngerLevels`.

### 3.5 Files and drop location

Convention consistent with `GD-matt-test/test-vN/`:

```
/Volumes/reincarnated/visual-artifacts/GD-general-play/run-01/
  gd-gp-run01.mp4              ← the session recording
  gd-gp-run01-smoke.mp4        ← the § 2.0 smoke clip (keep it)
  stills/
    00-start-panel.png
    01-start-sheet-tab1-a.png … (overlapping scroll crops, no gaps)
    02-start-doll.png
    03-start-skills.png
    04-a1-zombie-tooltip.png   ← the anomaly closure
    05-rank-normal.png / 06-rank-champion.png / 07-rank-hero.png
    1x-epoch<N>-sheet-*.png    ← one set per level-up / gear / skill boundary
    9x-end-panel.png / 9x-end-sheet-*.png
  notes.md                     ← difficulty, areas + play_time, epoch boundaries, deaths, oddities
```

Native PNGs are **compression insurance**, not the primary instrument. The 175-row character sheet
is dense small text and is the one thing video compression genuinely threatens.

**Size note:** 45 min at 1080p60 CQP20 ≈ 7–12 GB. Confirm free space on the share before the run;
consider recording locally and copying after rather than recording straight to the network share.

---

## 4. galadriel CV requirements

**Pipeline need NOT be realtime.** Everything here is post-hoc. Frames are extracted from the MP4
by PTS with `ffmpeg -accurate_seek`.

### 4.1 Extraction tiers (do not analyze 162,000 frames)

| Tier | Rate | Applied to |
|---|---|---|
| **T-A ledger** | 2 fps continuous | panel-counter OCR (the whole run) |
| **T-B engagement** | 10–15 fps | windows flagged by T-A as containing a `kills` increment ± 15 s |
| **T-C event** | native (30/60) | ±0.5 s around a kill increment, a globe drop, or an aggro-onset edge |

T-A is the spine. It is cheap and it *finds* the events; T-B/T-C only refine them.

### 4.2 Per-frame extraction targets

| # | Target | Grade | Notes |
|---|---|---|---|
| E1 | **Panel counters** — `play_time`, `kills`, `deaths`, `skill_use_count` (per-skill), `life_healed`, potions, `max_level_achieved`, `dps_field` | **exact** | The measurement spine. `dps_field` stays O-6 **oracle-only colour**. |
| E2 | **Kill events** = `kills` integer increment, frame-located | **exact** | Preferred over visual death-detection. |
| E3 | **HP-globe fraction** | estimate | Fill-boundary pixel measurement. See § 4.4 calibration. |
| E4 | **Nameplate OCR** — monster **name + level + rank** | OCR-attested | Attribution channel. See § 4.3. |
| E5 | **Overlay text** — `[entityId] Action State: X` + controller-state line | exact-ish | F2: live (controller, action) pairs with entity IDs, from the game rather than from inference. Feeds the gap-9 mapping table AND per-entity attribution. |
| E6 | **Anger edges** — mob→target directed lines | detection | Aggro-commitment instants (KPI 1/5). Upside channel. |
| E7 | **Engagement segmentation** — start/end boundaries | **definitional** | § 4.5 — the hard one. |

### 4.3 Monster RANK is mandatory, not optional — the A1 lesson at scale

A1 is a single unexplained nameplate line on one monster type. In general play the same failure
mode arrives **by the hundred**: GD's champion (yellow-name) and hero (orange/purple-name) monsters
carry affixes and multiples of normal HP.

**An unfiltered TTK distribution over mixed ranks is a mixture of at least three distributions, and
its variance means nothing.** The nameplate encodes rank in its **text colour and label**.

**Requirement: E4 emits `monster_rank ∈ {normal, champion, hero, boss, unknown}`**, from nameplate
colour classification, with the § 2.1 item 8 tooltips as the labeled training set. `unknown` is
first-class and must not be silently binned as `normal`.

### 4.4 Calibration — starts NOW, before any MP4 exists

The 18 banked v3 stills at `agentic_orchestration/research/knowledge/gd/live-probe-3/` are a
ready-made labeled set:

| Capability | Calibration source | Ground truth |
|---|---|---|
| **Panel OCR (E1)** | 6 trial shots + the round-1/2 panels | every digit already banked in `fixtures.db`, human-read at 4× crop — **exact labels** |
| **Character-sheet OCR** | `Screenshot (19)`–`(30)` | 175 `character_stat` rows, per-field provenance |
| **Globe fraction (E3)** | round-3 trial end frames | **two labeled points: 282/282 (100 %) and 269/282 (95.4 %)** |
| **Nameplate OCR (E4)** | 6 zombie trial frames | `Walking Dead` / level `6` / the A1 third line |
| **Overlay text (E5)** | round-3 trial start frames | `(Pursue, Move)` ×3, `(LongIdle, Fidget)` ×1, entity ids 68957 / 75289 / 77775 |

**Rank classification (§ 4.3) has NO calibration source in the banked stills** — which is precisely
why § 2.1 item 8 asks for the three tooltips. That item is the only calibration blocker in the run.

**Method law inherited from M3: no digit is ever read off a downscaled frame.** Crops at native
resolution, upscale for legibility only. Video frames extracted at 1920×1080 satisfy this; any CV
step that downscales before OCR violates it.

### 4.5 Engagement segmentation — the definitional problem, named

There is no clean "engagement start" in pack combat. Do not pretend otherwise. Emit **three**
segmentations and let the analyst choose:

1. **S1 — kill-to-kill** (`kills` increment n → n+1). Exact, mechanical, no judgment. **The
   default.** Contaminated by travel time between fights.
2. **S2 — combat-window.** First `skill_use_count` increment after an idle gap → last kill before
   the next idle gap. Removes travel; requires an idle-gap threshold (propose 3 s, banked as a
   parameter, not a constant).
3. **S3 — per-entity** (experimental). Entity id first appears in E5 overlay → that entity's
   `Dying` action state. This is the only route to per-monster TTK inside a pack, and F4 already
   proved entity ids distinguish individuals. **Low confidence** — "when the player committed to
   *that* target" is unobservable for a ranged build.

**Attacks-per-kill under S1 is the highest-value derived measure in the run** and needs no
segmentation judgment at all: `skill_use_count[defaultweaponattack]` delta between consecutive
`kills` increments. Exact integer, per kill, across the whole session. It is the direct successor
to Q47's 2/2/3.

### 4.6 CV self-validation gates — the run validates its own instrument

Because two channels measure overlapping things, the pipeline can be audited without ground-truth
labeling:

- **G-a** CV-counted kill events **must equal** the panel `kills` bookend delta. Exact integer test.
  Any mismatch is an OCR defect, located to the frame.
- **G-b** CV-summed `skill_use_count` deltas **must equal** the session bookend delta.
- **G-c** Human spot-check **N = 20 random nameplate OCR reads** against their raw frames → bank an
  **OCR error rate**. Certification-by-OCR must carry a measured error rate or it is a weaker claim
  than the human nameplate reads it inherits its predicate from.
- **G-d** Globe-fraction estimates at frames where the panel is also readable → cross-check against
  the `life_healed` time series (A3's two disagreeing instruments, now both continuous).

---

## 5. Data contract — how this lands in `fixtures.db`

*Written against `fixtures-v0.1` (MIGRATION-fixtures.md M1). Schema asks are marked
**REQUEST → elrond (v0.2)** — elrond owns the store; these are commission asks, not rulings.*

### 5.1 Row shape

| Table | This run |
|---|---|
| `fixture_session` | **one row.** `lane` = oracle. id `GP-gd-<date>-s1`. `notes` carries the A6 clock split, the whole-run constraint declaration (§ 5.3), and the OBS settings. |
| `capture` | the MP4 (**REQUEST: `capture.kind += 'video-session'`**) + every native PNG + per-engagement extracted frames as `trial-frame` with **PTS recorded** (**REQUEST: `capture.pts_ms`**) |
| `fixture_character` | **one per EPOCH** (level-up / gear / skill boundary), each with its full-sheet `character_stat` block |
| `fixture_set` | partitioned by `(epoch, monster_display_name, monster_level, monster_rank, area, difficulty)`. **REQUEST: `fixture_set.monster_rank`** (§ 4.3) and **`monster_affix` / `monster_variant`** — already on elrond's own v0.2 list, A1 is the reason. Propose `rung = 'GP'`. |
| `fixture_trial` | **one per engagement.** Segmentation variant recorded (**REQUEST: `fixture_trial.segmentation` ∈ S1/S2/S3**, § 4.5). `monster_entity_id` from E5 where available. |
| `trial_measurement` | every number a reading, per-field provenance, as always |
| `trial_trace` | E5 (controller, action, entity_id) triples — the F2 channel at volume |

### 5.2 Provenance values for this run

| Field | Value | Note |
|---|---|---|
| `read_method` | **`video-frame-ocr`** (new) for CV reads; `screenshot-fullres` for native PNGs; `hand-noted-band` for Matt's notes.md lines | New method must be distinguishable so certified-by-OCR rows are auditable as a class (G-c) |
| `uncertainty_abs` on `fight_seconds` | **0.1 s** | ±1 frame is 0.017–0.033 s; the **definitional** boundary term dominates. Bank the honest larger number and say why. |
| `uncertainty_abs` on counter deltas | **0** | integer counters, exact — subject to the G-a/G-b gates passing |
| `uncertainty_abs` on globe fraction | per § 4.4 calibration residual | not asserted before calibration |
| `confounds` on damage-intake | **potion events** + regen | any engagement containing a potion event: globe-derived intake is a **lower bound**, flagged |

### 5.3 Constraints — declared violated UP FRONT, not discovered later

Every L0 constraint is broken here by design. Declaring it at ingestion is what keeps this run from
being mistaken for a bigger L0.

| Constraint | `held` |
|---|---|
| `single-monster` | **violated** (packs) |
| `no-level-up-mid-set` | **held per epoch by construction** — epochs *are* the level partition (the M2 precedent: round 2's 5→6 split the set) |
| `player-melee-only` | **violated** (A2 — ranged build; every TTK is a ranged TTK) |
| `no-CC-test-character` | `expired` (O-9, carried) |
| `ledger-isolated-trial` | **violated** — the whole run is ONE continuous ledger. A5-style discontinuity flagging is meaningless here; continuity is the *design*. |

### 5.4 Certification (O-8) — per trial, and most will fail

A trial in this run **MAY certify** when: (a) nameplate OCR yields name + level + rank, (b) its
epoch has a full-sheet `fixture_character`, (c) it does not straddle an epoch boundary. That is the
same predicate the round-3 trials passed, with a new attestation instrument.

**Most engagements will fail (a)** — camera angle, pack overlap, no hover. **They bank uncertified,
with their numbers intact.** O-8's whole point: NULL identity is admitted; the certified *view*
filters. Uncertified rows still carry exact attacks-per-kill and exact TTK — they just cannot be
joined to a statline.

**The distribution question does not require certification.** Q47-successor questions about TTK
*shape* run against the full bank; questions about a *specific monster's* statline run against
`v_fixture_bank_certified`. Two questions, two views, one run.

### 5.5 What this run supersedes and what it does not

- **Supersedes:** the hand-stopwatch instrument class. `fight_seconds` at `uncertainty_abs = 2.0`
  is retired going forward. The three banked L0 readings stay as-is (raw evidence governs, C10).
- **Does NOT supersede:** the three certified L0 trials. They remain the **identity-attested
  calibration points** — the only fixtures whose monster is known by spawn command *and* nameplate.
  If A1 resolves to "affixed variant," they get relabeled, not deleted.
- **Does NOT resolve:** `monster_record` NULL. The display-name → `.dbr` bridge (elrond v0.2 item 2)
  is still the last link between a certified fixture and the `.arz` statline it predicts. This run
  makes that bridge *more* valuable, not less — it will surface dozens of display names.

---

## 6. Gates before execution

| # | Gate | Owner | Blocks |
|---|---|---|---|
| **G1** | **OBS installed + configured on Matt's PC** per § 3.2 | Matt — **FILED as `matt_to_do` row T10** (2026-07-26, gandalf-prime; carries Steam + obsproject.com install paths and the one-time settings) | the whole run |
| **G2** | **§ 2.0 smoke gate passes** (5 criteria) | Matt, 3 min | the full session |
| **G3** | **galadriel pipeline ready for post-hoc** — T-A panel OCR + E4 nameplate OCR at minimum. **Realtime NOT required.** | galadriel | *analysis only, not capture* |
| **G4** | **§ 4.4 calibration started against the 18 banked v3 stills** | galadriel | **nothing — can start immediately, no MP4 needed** |
| **G5** | § 7 forks ruled | Matt | run parameters |

**G3 does not block G1/G2.** Footage is durable and re-analyzable; the capture and the pipeline can
proceed in parallel. **G4 should start now** — five of six CV capabilities have exact labels sitting
in `fixtures.db` already, and the sixth (rank) is exactly what § 2.1 item 8 goes to fetch.

Optional: ship the smoke clip for a galadriel pre-check if G3 is ready. Otherwise Matt's own
five-criteria eyeball is the gate — all five are human-checkable, and the round trip costs more
than it buys.

---

## 7. Open forks for Matt

### F-1 — Session length

**Lean: 30–45 min of continuous play, one sitting.**

At level-matched content, expect ~3–6 kills/min including travel → **~100–250 engagements.** That is
enough for a distribution with real tails, not just a mean. Below ~20 min the champion/hero tail is
undersampled and the run answers the same question L0 already answered, with more machinery. Above
~60 min the file passes ~15 GB, epoch count climbs, and the marginal engagement stops adding shape.

Cost: file ~7–12 GB; expect 2–4 epoch boundaries at ~60–90 s each.

### F-2 — Single-area vs natural progression

**Lean: NATURAL PROGRESSION**, with area + `play_time` logged at every transition (§ 2.4).

Reasoning: a single-area run gives one monster family's TTK — which is **structurally the same thing
the L0 zombie set already is, only larger**. It would not be a distribution oracle; it would be a
bigger calibration point. The substrate this feeds is *every era's* substrate
(`era-substrate-architecture` § 6) and its era profiles are dial-sets over pack composition, aggro
and telegraph — none of which vary within one area.

Natural progression also keeps the *play* authentic. Farming a single spawn distorts pack behavior
and aggro patterns, which are the AI channels (E5/E6) this footage carries for free.

Cost accepted: level-ups and area drift. Both are handled by epoch partitioning (§ 5.1) — a
mechanism the bank already proved on round 2's 5→6 split.

### F-3 — Level-matched only vs record everything

**Lean: RECORD EVERYTHING, FILTER AT ANALYSIS.** Strongest lean of the three.

This is the **catalogue-not-prefilter principle** the project already runs on: Legolas crawls broad
and scores; Elrond curates at consumption; the visual style register is a consumption-time filter on
a scored catalogue, not a crawl-scope constraint — which is exactly why a register pivot stays
viable. Same logic here.

- Off-level engagements are **free calibration points on the level-differential axis** — the very
  axis era-profile statline scaling needs (`era-substrate-architecture` § 5).
- Filtering at capture destroys data that costs **nothing** to keep and **cannot be recovered**
  without another sitting of Matt's time.
- `monster_level` is OCR'd per nameplate (E4) and `character_level` is per epoch → **the filter is a
  `WHERE` clause.** Building it into the protocol buys nothing and forecloses everything.
- It also removes a live protocol burden: Matt would otherwise be judging level-match mid-fight,
  which distorts the play the run is trying to observe.

Matt's stated intent — *"it would be a better test for me to fight enemies of my level"* — is fully
served: level-matched engagements will dominate the sample naturally, because that is what natural
progression produces. Recording the rest costs one `WHERE` clause and buys an axis.

---

## 8. What this run is worth if it works

Q47's per-fight ±5 % tier is **empirically unreachable at L0** — not from instrument coarseness, but
because a 2–3-attack kill has three quanta. This run does not chase that tier with a better
stopwatch. It moves to a regime where the phenomenon **has** a distribution, and brings an
instrument whose error is two orders of magnitude below the old one — at which point the limiting
uncertainty stops being the instrument and becomes the *definition of an engagement*.

That is the honest end state of a measurement program: you stop arguing about the ruler and start
arguing about what you meant.

---

**Signed:** gandalf, 2026-07-26 (SPEC-AUTHOR). Three forks stand open for Matt; G4 can start before
any of them are ruled.
